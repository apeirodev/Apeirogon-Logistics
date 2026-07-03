# AI Security - Core Security Rules

Foundational security guidelines for AI/ML systems.
Source: https://github.com/TikiTribe/claude-secure-coding-rules (MIT)

**Standards**: NIST AI RMF, ISO/IEC 23894, MITRE ATLAS, Google SAIF

---

## Data Security

### Rule: Validate Training and Operational Data Integrity

**Level**: `strict`

**When**: Loading datasets, telemetry, or any calibration data used by models or scoring engines.

**Do**:

```python
import hashlib, hmac

def verify_dataset_checksum(filepath: str, expected_sha256: str) -> bool:
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return hmac.compare_digest(h.hexdigest(), expected_sha256)
```

**Don't**:

```python
# VULNERABLE: load without integrity check -- data poisoning undetected
data = json.load(open(dataset_path))
```

**Why**: Data poisoning (MITRE ATLAS AML.T0020) compromises model outputs. Checksumming inputs
detects tampering before it influences operational scoring.

**Refs**: MITRE ATLAS AML.T0020, NIST AI RMF MAP 1.5

---

## Model/Scoring Security

### Rule: Protect Scoring Artefacts with Access Controls and Integrity Checks

**Level**: `strict`

**When**: Loading, storing, or distributing deterministic scoring models or calibration data.

**Do**:

```python
# Verify before loading any scoring model
assert verify_dataset_checksum(model_path, manifest["sha256"][model_path])

# Restrict write permissions on scoring artefacts
import os
os.chmod(model_path, 0o444)   # read-only after write
```

**Don't**:

```python
# VULNERABLE: loading unverified scoring artefact
model = json.load(open(model_path))
```

**Why**: Tampered scoring models silently corrupt route recommendations. Integrity verification
and read-only permissions after publish prevent undetected modification.

**Refs**: MITRE ATLAS AML.T0040, NIST AI RMF MANAGE 1.3

---

## Inference / Provider Output Security

### Rule: Validate and Sanitize All LLM/AI Provider Inputs and Outputs

**Level**: `strict`

**When**: Any data flowing to or from an AI provider (ChatGPT, Claude, Gemini, Ollama, etc.).

**Do**:

```python
import re

def sanitize_provider_input(text: str, max_length: int = 8192) -> str:
    if not isinstance(text, str):
        raise ValueError("Input must be a string")
    text = text[:max_length]
    # Strip control characters, preserve newlines and tabs
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)
    return text

def validate_provider_output(output: dict) -> tuple[bool, list[str]]:
    problems = []
    if not isinstance(output.get("governance_metadata"), dict):
        problems.append("missing governance_metadata")
    if output.get("advisory_only") is not True:
        problems.append("advisory_only must be true")
    return len(problems) == 0, problems
```

**Don't**:

```python
# VULNERABLE: passing raw user input to provider without sanitization
response = provider.complete(user_supplied_text)

# VULNERABLE: using provider output without validation
route = ai_response["recommended_route"]   # no advisory check, no schema validation
```

**Why**: Prompt injection (OWASP LLM01) can manipulate provider outputs. Unsanitized outputs
used in HTML rendering, command execution, or as operational facts are injection vectors.

**Refs**: OWASP LLM01, OWASP LLM02, NIST AI RMF MAP 1.5

---

## Infrastructure Security

### Rule: Isolate AI Provider API Key Handling

**Level**: `strict`

**When**: Any tool that accepts or uses an AI provider API key.

**Do**:

```python
import os

def get_api_key(provider: str) -> str:
    # Accept from environment variable only -- never from CLI args or JSON input
    key = os.environ.get(f"{provider.upper()}_API_KEY")
    if not key:
        raise EnvironmentError(f"{provider} API key not set in environment")
    return key
```

**Don't**:

```python
# VULNERABLE: API key from CLI argument (visible in process list)
parser.add_argument("--api-key")

# VULNERABLE: API key in JSON config file (risk of accidental commit)
config = json.load(open("config.json"))
api_key = config["api_key"]
```

**Why**: API keys in CLI args appear in process listings and shell history. Keys in config files
are frequently accidentally committed. Environment variables are the safe standard.

**Refs**: NIST AI RMF MANAGE 1.3, CWE-312

---

## Monitoring

### Rule: Log AI Provider Interactions for Audit

**Level**: `warning`

**When**: Any invocation of an AI provider.

**Do**:

```python
import logging, json
from datetime import datetime

def log_provider_call(provider: str, input_summary: str, output_summary: str, tokens: int):
    logging.getLogger('ai_audit').info(json.dumps({
        'timestamp': datetime.utcnow().isoformat(),
        'provider': provider,
        'input_length': len(input_summary),
        'output_length': len(output_summary),
        'tokens_used': tokens,
        # Never log the actual key or full prompt
    }))
```

**Don't**:

```python
# VULNERABLE: logs full prompt (may contain sensitive operational data or keys)
logger.debug("Provider call: %s", full_prompt)
```

**Why**: Provider call logs support incident investigation and model extraction detection
(MITRE ATLAS AML.T0040) without exposing keys or sensitive inputs.

**Refs**: NIST AI RMF MEASURE 1.1, MITRE ATLAS AML.T0040

---

## Quick Reference

| Rule | Level | Threat | Control |
|------|-------|--------|---------|
| Validate data integrity | strict | Data poisoning (AML.T0020) | Checksums |
| Protect scoring artefacts | strict | Model tampering (AML.T0040) | Integrity + read-only |
| Sanitize provider I/O | strict | Prompt injection (LLM01) | Sanitize + schema validate |
| Isolate API key handling | strict | Credential exposure | Env vars only |
| Log provider interactions | warning | Undetected misuse | Audit log |

---

## Version History

- **v1.0.0** - Initial release
