# Apeirogon Logistics: Claude Code Security Rules

Security rules for Claude Code when working in this repository.
Derived from [TikiTribe/claude-secure-coding-rules](https://github.com/TikiTribe/claude-secure-coding-rules).

Full upstream rule files are in `.claude/rules/`.

---

## Versioning Rule (Mandatory)

This project uses **Semantic Versioning** (SemVer): `Major.Minor.Patch`.

- **Every change to any file** must increment the version before committing.
- **Patch increment** (`0.0.1`): small or inconsequential changes, such as typo fixes, comment updates, and minor corrections.
- **Minor increment** (`0.1.x`): significant changes, such as new features, new files, structural changes, and scoring logic updates. Patch resets to `1` (not `0`) on a minor bump.
- **Major increment**: breaking changes to the scoring system, schema, or public-facing API. Discuss with maintainer before bumping.

Update the version in **all** of these files on every change:
- `README.md`: footer line (`v0.X.Y`)
- `pyproject.toml`: `version = "0.X.Y"`
- `VERSION.json`: `"version"` field, `"previous_version"`, and add a `version_history` entry
- `developer/PROJECT_STATUS.md`: `**Version:**` line
- `developer/DEVELOPMENT_HISTORY.md`: add a new `## Version 0.X.Y` section
- `developer/data/source_registry.json`: add a new source entry for the release

---

## Project Security Context

Apeirogon Logistics is a **Python-first, local-first, JSON-centric** platform. It:

- processes untrusted external inputs: AI provider outputs, OCR extractions, user-supplied JSON, telemetry submissions
- reads and writes files based on CLI arguments
- integrates with external AI providers (keys supplied by users at runtime)
- generates and verifies release checksums
- never runs a web server, never manages user sessions, never connects to a database

Rules are scoped accordingly. Web application rules (XSS, session management, SQL injection) are not primary concerns. File safety, deserialization safety, AI output containment, supply chain integrity, and error-handling correctness are.

---

## Mandatory Rules (strict)

### FILE-01: Validate All File Paths

**When**: Any tool receives a file path from CLI arguments, JSON input, or provider output.

**Do**:

```python
from pathlib import Path

ALLOWED_WRITE_ROOTS = [Path("output"), Path("exports"), Path("telemetry")]

def safe_write_path(raw_path: str, allowed_roots: list[Path]) -> Path:
    p = Path(raw_path).resolve()
    for root in allowed_roots:
        if p.is_relative_to(root.resolve()):
            return p
    raise ValueError(f"Path outside allowed roots: {raw_path}")
```

**Don't**:

```python
# VULNERABLE: path traversal — user supplies "../../etc/passwd"
with open(args.output, "w") as f:
    f.write(data)
```

**Why**: CLI tools accept `--input` and `--output` from untrusted callers. Path traversal allows reads or writes outside intended directories.

**Refs**: OWASP A01:2025, CWE-22

---

### FILE-02: Never Use pickle, JSON Only

**When**: Deserializing any data.

**Do**:

```python
import json
data = json.loads(raw_input)        # safe
data = json.load(file_handle)       # safe
```

**Don't**:

```python
import pickle
data = pickle.loads(raw_input)      # VULNERABLE: arbitrary code execution
```

**Why**: `pickle` deserializes arbitrary Python objects and executes code on load. This codebase uses JSON exclusively; there is no reason to introduce pickle.

**Refs**: OWASP A08:2025, CWE-502

---

### FILE-03: No subprocess with Shell Interpolation

**When**: Any shell command execution (currently rare in this codebase, keep it that way).

**Do**:

```python
import subprocess
result = subprocess.run(["tool", "--flag", user_value], capture_output=True, text=True, check=True)
```

**Don't**:

```python
import os
os.system(f"tool --flag {user_value}")               # VULNERABLE: command injection
subprocess.run(f"tool --flag {user_value}", shell=True)  # VULNERABLE
```

**Why**: Any user-supplied value interpolated into a shell string enables command injection.

**Refs**: OWASP A05:2025, CWE-78

---

### AI-01: AI Provider Outputs Are Always Advisory

**When**: Processing any output from an AI provider (ChatGPT, Claude, Gemini, Ollama, etc.).

**Do**:

```python
# Validate against schema before any downstream use
ok, issues = validate_governance_metadata(output.get("governance_metadata", {}))
if not ok:
    return structured_error("invalid governance metadata", issues)

if output.get("advisory_only") is not True:
    return structured_error("provider output must be advisory_only=true")

# Never merge AI output into sourced facts
result["ai_recommendation"] = output       # keep separate
# NOT: result["sourced_facts"].update(output)  # WRONG
```

**Don't**:

```python
# VULNERABLE: treating AI output as authoritative
data["price_usc"] = ai_output["price_usc"]      # overwrites sourced fact
data["route"] = ai_output["recommended_route"]   # no validation, no advisory tag
```

**Why**: AI outputs are probabilistic and prompt-injectable. They must never overwrite sourced facts or bypass governance metadata validation.

**Refs**: OWASP LLM02, NIST AI RMF MAP 1.5, project non-negotiable rules

---

### AI-03: Enforce Hallucination Guardrails on All AI-Assisted Workflows

**When**: Any tool, prompt, or document workflow involves AI provider output.

**Context**: In live testing, AI assistants hallucinated mission-critical Star Citizen
values (prices, capacities, fees, distances) more than 50% of the time without
explicit constraints. Hallucinated numbers waste real in-game time and burn contracts.

**Do**:

```python
HALLUCINATION_RISK_FIELDS = {
    "reward_usc", "fee_usc", "profit_usc", "cargo_scu",
    "price_usc", "distance_km", "capacity_scu",
}

def flag_hallucination_risk(ai_output: dict, user_supplied_fields: set) -> list[str]:
    """Return list of fields present in AI output that were not in user-supplied data."""
    flags = []
    for field in HALLUCINATION_RISK_FIELDS:
        if field in ai_output and field not in user_supplied_fields:
            flags.append(f"HALLUCINATION_RISK: {field} not in user-supplied data")
    return flags
```

Every user-facing AI workflow document (provider guides, quick start, first route
analysis) must reference `prompts/STRICT_AI_SESSION_PROMPT.md` and instruct users
to paste it before any AI interaction.

**Don't**:

```python
# WRONG: accepting AI numeric output without checking if user supplied it
result["reward_usc"] = ai_output.get("reward_usc")   # may be hallucinated
```

**Why**: AI training data for Star Citizen is outdated by definition (game patches
change all values). Without explicit constraint, AI assistants fill gaps with
plausible-sounding invented data indistinguishable from real values.

**Refs**: `docs/HALLUCINATION_GUARDRAILS.md`, `prompts/STRICT_AI_SESSION_PROMPT.md`,
OWASP LLM09 (Misinformation), NIST AI RMF MAP 5.1

---

### AI-04: Reject AI Output That Contains Unsourced Numeric Fields

**When**: Processing AI provider output that includes numeric operational fields.

**Do**:

```python
def validate_numeric_sourcing(ai_output: dict, user_input: dict) -> tuple[bool, list[str]]:
    """Verify that numeric fields in AI output trace back to user-supplied input."""
    problems = []
    numeric_fields = [k for k, v in ai_output.items() if isinstance(v, (int, float))]
    for field in numeric_fields:
        if field not in user_input:
            problems.append(
                f"field '{field}' has numeric value {ai_output[field]!r} "
                f"but was not in user-supplied input — possible hallucination"
            )
    return not problems, problems
```

Flag but do not auto-reject; let the human operator decide. Set
`hallucination_flags` in governance metadata so the operator sees the warning.

**Don't**:

```python
# WRONG: silently passing numeric AI output downstream without sourcing check
pipeline.process(ai_output)
```

**Why**: The operator cannot catch hallucination if the system doesn't flag the
fields that were not user-supplied. Silent passage of unsourced numbers into the
scoring pipeline produces confident-looking wrong results.

**Refs**: `docs/HALLUCINATION_GUARDRAILS.md`, OWASP LLM09

---

### AI-02: Sanitize Provider Outputs Before Downstream Use

**When**: Any AI provider response is parsed and used to produce operational data.

**Do**:

```python
import re

def sanitize_provider_text(raw: str, max_length: int = 4096) -> str:
    if not isinstance(raw, str):
        raise ValueError("Provider output must be a string")
    # Truncate to reasonable length
    raw = raw[:max_length]
    # Strip null bytes and control characters (keep newlines/tabs)
    raw = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", raw)
    return raw
```

**Don't**:

```python
# VULNERABLE: unsanitized provider text passed to downstream parsers
result = parse_route(ai_response["raw_output"])
```

**Why**: Prompt injection can cause AI providers to embed control characters, path components, or schema-breaking strings in their output.

**Refs**: OWASP LLM01, OWASP LLM02, MITRE ATLAS AML.T0051

---

### INT-01: Verify Integrity of All Release Artefacts

**When**: Generating or consuming release packages, manifests, or exported data.

**Do**:

```python
import hashlib, hmac

def verify_file_checksum(filepath: str, expected_sha256: str) -> bool:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return hmac.compare_digest(h.hexdigest(), expected_sha256)
```

**Don't**:

```python
# VULNERABLE: loading a release package without checking its hash
data = json.load(open(release_file))    # no integrity check
```

**Why**: Tampered release packages or manifests can silently corrupt operational data. The project already has `generate_release_checksums.py` and `verify_release_integrity.py`. Always use them.

**Refs**: OWASP A03:2025, CWE-829, NIST SSDF PS.3.1

---

### INT-02: Pin Dependencies with Hashes

**When**: Adding or updating any Python dependency.

**Do**:

```
# requirements.txt — pin exact versions with hashes
jsonschema==4.23.0 \
    --hash=sha256:<hash>
```

**Don't**:

```
jsonschema>=4.0   # unpinned — supply chain risk
```

**Why**: Unpinned dependencies allow a compromised upstream package to silently substitute a malicious version.

**Refs**: OWASP A03:2025, CWE-829

---

### ERR-01: Fail Closed, Deny on Error

**When**: Any permission check, schema validation, or governance metadata check encounters an unexpected exception.

**Do**:

```python
def validate_with_fallback(data: dict) -> tuple[bool, list[str]]:
    try:
        return validate_governance_metadata(data)
    except Exception as e:
        logger.error("Governance validation error: %s", e)
        return False, ["validation_error_fail_closed"]  # deny, not allow
```

**Don't**:

```python
try:
    return validate_governance_metadata(data)
except Exception:
    return True, []   # VULNERABLE: fail open — grants trust on error
```

**Why**: Failing open on validation errors silently bypasses governance controls. An unhandled exception must never promote untrusted data.

**Refs**: OWASP A10:2025, CWE-754

---

### ERR-02: Never Expose Internal Paths or Stack Traces to Output

**When**: Returning error responses from any tool.

**Do**:

```python
from tools.lib.common import structured_error
import logging

logger = logging.getLogger(__name__)

try:
    result = process(data)
except Exception as e:
    logger.error("Processing error: %s", e, exc_info=True)  # full detail to log
    return structured_error("processing failed")             # safe summary to output
```

**Don't**:

```python
except Exception as e:
    return {"error": str(e), "traceback": traceback.format_exc()}  # leaks internals
```

**Why**: Stack traces expose file paths, library versions, and internal logic that help attackers craft targeted inputs.

**Refs**: OWASP A02:2025, CWE-209

---

### LOG-01: Never Log API Keys, Tokens, or User Credentials

**When**: Logging any data that touched provider configuration or user input.

**Do**:

```python
SENSITIVE_KEYS = {"api_key", "token", "secret", "password", "credential", "key"}

def sanitize_for_log(data: dict) -> dict:
    return {
        k: "[REDACTED]" if any(s in k.lower() for s in SENSITIVE_KEYS) else v
        for k, v in data.items()
    }

logger.info("Provider call: %s", sanitize_for_log(config))
```

**Don't**:

```python
logger.debug("Config: %s", config)   # VULNERABLE if config contains api_key
```

**Why**: Users supply their own API keys at runtime. Logging them leaks credentials into log files, CI output, and replay artefacts.

**Refs**: OWASP A09:2025, CWE-532

---

### SRC-01: Never Silently Merge Source Classes

**When**: Combining data from different provenance classes (sourced facts, OCR, telemetry, AI output, user correction).

**Do**:

```python
# Keep sources explicitly separated in output
result = {
    "sourced_facts": sourced_data,
    "ai_recommendation": ai_output,          # never merged into sourced_facts
    "ocr_extraction": ocr_data,              # never merged into sourced_facts
    "unresolved_fields": collect_unresolved(sourced_data),
    "governance_metadata": governance_metadata(
        source_class="deterministic_output",
        ...
    )
}
```

**Don't**:

```python
# VULNERABLE: silent merge loses provenance
result = {**sourced_data, **ai_output}
```

**Why**: Silent merges destroy provenance, violate source separation, and allow AI or OCR uncertainty to masquerade as sourced facts. This is a core non-negotiable project rule.

**Refs**: Project brief, Source Separation; NIST AI RMF MAP 1.5

---

## Advisory Rules (warning)

### WARN-01: Validate JSON Schema Before Processing

For any tool that processes external JSON, validate against the relevant schema before accessing fields. Use `tools/schema_validator.py` for structured validation.

### WARN-02: Limit File Sizes on Ingestion

When reading provider output, telemetry, or OCR result files, enforce a reasonable size cap (e.g. 10 MB) before loading to prevent memory exhaustion.

```python
MAX_INPUT_BYTES = 10 * 1024 * 1024

def safe_load_json(path: str) -> Any:
    p = Path(path)
    if p.stat().st_size > MAX_INPUT_BYTES:
        raise ValueError(f"Input file too large: {p.stat().st_size} bytes")
    return json.loads(p.read_text(encoding="utf-8"))
```

### WARN-03: Use `hmac.compare_digest` for All Hash Comparisons

Never use `==` to compare hash strings. Use `hmac.compare_digest` to prevent timing attacks.

```python
import hmac
if not hmac.compare_digest(computed, expected):
    raise SecurityError("Hash mismatch")
```

### WARN-04: GitHub Actions, Pin Action Versions to Full SHA

```yaml
# Do:
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2

# Don't:
- uses: actions/checkout@v4   # mutable tag — supply chain risk
```

### WARN-05: GitHub Actions, Limit GITHUB_TOKEN Permissions

```yaml
permissions:
  contents: read   # minimum required

# Don't omit permissions: block — defaults to write-all in some configurations
```

---

## Out of Scope

The following OWASP categories are not applicable to this codebase and should not generate warnings:

- **A07 Authentication Failures**: no user authentication system
- **A01 Broken Access Control**: no multi-user access model
- **A04 Cryptographic Failures** (password hashing): no user accounts
- **A06 Insecure Design** (web threat modeling): no web server

---

## Rule Source

Rules derived from [TikiTribe/claude-secure-coding-rules](https://github.com/TikiTribe/claude-secure-coding-rules) (MIT).
Full upstream rule files: `.claude/rules/`
