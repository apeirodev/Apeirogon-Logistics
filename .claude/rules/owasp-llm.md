# OWASP Top 10 for LLM Applications 2025 - Security Rules

Security rules for applications that integrate large language model providers.
Source: OWASP Top 10 for LLM Applications v2.0 (2025) -- https://owasp.org/www-project-top-10-for-large-language-model-applications/

**Scope**: Any code path that sends input to or receives output from an LLM provider.

---

## Overview

**Standard**: OWASP Top 10 for LLM Applications v2.0 (2025)
**Categories**: LLM01 -- LLM10
**Applicability to this codebase**: Apeirogon Logistics never runs an LLM itself. It sends user-supplied contract data to external AI providers (Claude, ChatGPT, Gemini, etc.) and parses their outputs. LLM01 (Prompt Injection) and LLM05 (Improper Output Handling) are the highest-risk categories.

---

## LLM01: Prompt Injection

**Risk Level**: Critical

### Rule: Sanitize and Bound All Inputs Sent to Providers

**Level**: `strict`

**When**: Any user-supplied text (OCR extractions, CLI arguments, JSON fields) is included in a prompt sent to an AI provider.

**Do**:

```python
import re

MAX_PROMPT_FIELD_LENGTH = 512

def sanitize_prompt_field(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("Prompt field must be a string")
    value = value[:MAX_PROMPT_FIELD_LENGTH]
    # Strip control characters; preserve newlines and tabs
    value = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", value)
    return value

# Reject values that look like embedded instruction attempts
INJECTION_PATTERNS = [
    r"ignore\s+(previous|above|all)\s+instructions",
    r"system\s*:",
    r"<\s*/?system\s*>",
    r"\bact\s+as\b",
    r"\byou\s+are\s+now\b",
]

def check_injection_risk(value: str) -> bool:
    """Return True if the value looks like a prompt injection attempt."""
    lower = value.lower()
    return any(re.search(p, lower) for p in INJECTION_PATTERNS)
```

**Don't**:

```python
# VULNERABLE: raw user text appended to system prompt without sanitization
prompt = f"{system_prompt}\n\nUser contract data: {raw_ocr_text}"
```

**Why**: Malicious contract data or OCR text could contain instructions that redirect the AI's behavior, causing it to produce false scores, leak system prompts, or ignore governance rules.

**Refs**: OWASP LLM01:2025, MITRE ATLAS AML.T0051

---

## LLM02: Sensitive Information Disclosure

**Risk Level**: High

### Rule: Never Include API Keys or Internal Paths in Prompts

**Level**: `strict`

**When**: Constructing any prompt sent to a provider.

**Do**:

```python
def build_prompt(user_data: dict) -> str:
    # Include only operational fields -- never config, keys, or internal paths
    safe_fields = {k: v for k, v in user_data.items()
                   if k not in {"api_key", "token", "secret", "internal_path", "config_path"}}
    return json.dumps(safe_fields, indent=2)
```

**Don't**:

```python
# VULNERABLE: full config object serialized into prompt
prompt = f"Analyze this: {json.dumps(full_config_including_api_key)}"
```

**Why**: Provider logs, fine-tuning pipelines, or prompt-injection attacks can extract information embedded in prompts. API keys and file paths should never appear in provider-facing text.

**Refs**: OWASP LLM02:2025, CWE-312

---

## LLM03: Supply Chain

**Risk Level**: High

### Rule: Pin Provider SDK Versions with Hashes

**Level**: `strict`

**When**: Any AI provider SDK (openai, anthropic, google-generativeai, etc.) is declared as a dependency.

**Do**:

```
# requirements.txt -- pin exact versions with hashes
anthropic==0.40.0 \
    --hash=sha256:<verified_hash>
```

**Don't**:

```
anthropic>=0.30    # unpinned -- supply chain risk
```

**Why**: Provider SDKs are high-value supply chain targets. A compromised version could exfiltrate prompts, responses, or API keys.

**Refs**: OWASP LLM03:2025, OWASP A03:2025 (Supply Chain), CWE-829

---

## LLM04: Data and Model Poisoning

**Risk Level**: High

### Rule: Verify Integrity of All Calibration and Scoring Data

**Level**: `strict`

**When**: Loading any JSON file that influences scoring weights, issuer modifiers, ship modifiers, or hallucination guardrails.

**Do**:

```python
import hashlib, hmac

def verify_scoring_data(path: str, expected_sha256: str) -> dict:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    if not hmac.compare_digest(h.hexdigest(), expected_sha256):
        raise SecurityError(f"Scoring data integrity check failed: {path}")
    return json.loads(Path(path).read_text(encoding="utf-8"))
```

**Don't**:

```python
# VULNERABLE: loading scoring weights without integrity check
weights = json.load(open("scoring_weights.json"))
```

**Why**: Tampered scoring data silently corrupts route recommendations. A poisoned weights file could make bad routes score 90 and good routes score 20, producing consistently wrong guidance without any visible error.

**Refs**: OWASP LLM04:2025, MITRE ATLAS AML.T0020 (Training Data Poisoning)

---

## LLM05: Improper Output Handling

**Risk Level**: Critical

### Rule: Parse and Validate All Provider Responses Before Use

**Level**: `strict`

**When**: Any provider response is parsed and used to produce operational data.

**Do**:

```python
import json, re

def parse_provider_response(raw: str, max_length: int = 8192) -> dict:
    if not isinstance(raw, str):
        raise ValueError("Provider response must be a string")
    raw = raw[:max_length]
    raw = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", raw)
    # Strip markdown code fences if present
    raw = re.sub(r"^```(?:json)?\s*", "", raw.strip(), flags=re.IGNORECASE)
    raw = re.sub(r"\s*```$", "", raw)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Provider response is not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("Provider response must be a JSON object")
    return data
```

**Don't**:

```python
# VULNERABLE: exec/eval of provider response
exec(provider_response)

# VULNERABLE: unsanitized response written directly to output file
Path(output_path).write_text(provider_response)
```

**Why**: Provider outputs can contain injected code, malformed JSON, or embedded control sequences. Parsing and schema-validating before use prevents these from propagating downstream.

**Refs**: OWASP LLM05:2025, OWASP LLM01:2025

---

## LLM06: Excessive Agency

**Risk Level**: High

### Rule: Limit What Actions a Provider-Integrated Workflow Can Take

**Level**: `strict`

**When**: Any workflow acts on provider output by writing files, making network calls, or modifying system state.

**Do**:

```python
# Enumerate exactly what actions are allowed after a provider call
ALLOWED_POST_PROVIDER_ACTIONS = frozenset([
    "write_output_json",      # write to output/ only
    "append_telemetry_log",   # append to telemetry/ only
])

def execute_post_provider_action(action: str, payload: dict, output_path: str) -> None:
    if action not in ALLOWED_POST_PROVIDER_ACTIONS:
        raise PermissionError(f"Action '{action}' not permitted after provider call")
    if action == "write_output_json":
        safe_write_path(output_path)   # FILE-01 check
        dump_json(payload, output_path)
```

**Don't**:

```python
# VULNERABLE: acting on arbitrary instructions from provider response
action = provider_response.get("next_action")
globals()[action](**provider_response.get("params", {}))
```

**Why**: If a provider response is prompt-injected, unrestricted action dispatch allows the attacker to execute arbitrary operations via the AI.

**Refs**: OWASP LLM06:2025, OWASP agent-security rule "Limit Agent Autonomy Scope"

---

## LLM07: System Prompt Leakage

**Risk Level**: Medium

### Rule: Never Return System Prompt Contents in Tool Output

**Level**: `strict`

**When**: Any tool outputs provider response data that might contain reflected system prompt content.

**Do**:

```python
SYSTEM_PROMPT_MARKERS = [
    "you are a", "your instructions are", "system prompt:",
    "do not reveal", "ignore previous instructions",
]

def check_for_system_prompt_leakage(text: str) -> bool:
    lower = text.lower()
    return any(marker in lower for marker in SYSTEM_PROMPT_MARKERS)

def sanitize_provider_output_for_display(text: str) -> str:
    if check_for_system_prompt_leakage(text):
        return "[provider output redacted -- possible system prompt reflection]"
    return text
```

**Why**: Some providers echo or reflect portions of system prompts in their responses, especially under adversarial prompting. Leaking internal system prompts exposes the governance and safety logic to attackers.

**Refs**: OWASP LLM07:2025

---

## LLM08: Vector and Embedding Weaknesses

**Risk Level**: Low (not currently applicable)**

**Note**: Apeirogon Logistics does not use embeddings, vector stores, or RAG pipelines. This category is not applicable to the current architecture. If a vector store or semantic search component is added in a future phase, add rules here at that time.

**Refs**: OWASP LLM08:2025

---

## LLM09: Misinformation

**Risk Level**: Critical (primary risk for this application)

### Rule: Enforce Hallucination Guardrails -- Do Not Trust Unsourced Numerics

**Level**: `strict`

**Note**: This maps directly to project rules AI-03 and AI-04. The OWASP LLM09 category is the formal standard behind those project-specific rules.

**Do**: See AI-03 and AI-04 in CLAUDE.md. The `HALLUCINATION_RISK_FIELDS` and `validate_numeric_sourcing()` patterns required there are the LLM09 controls for this codebase.

**Why**: Star Citizen values (prices, distances, capacities, fees) are patched frequently. AI training data is always out of date. Any numeric field that was not explicitly supplied by the user and appears in provider output is an unsourced claim that must be flagged.

**Refs**: OWASP LLM09:2025, NIST AI RMF MAP 5.1, project rules AI-03 and AI-04

---

## LLM10: Unbounded Consumption

**Risk Level**: Medium

### Rule: Enforce Token and Request Limits on Provider Calls

**Level**: `warning`

**When**: Any code path invokes a provider API.

**Do**:

```python
MAX_INPUT_TOKENS = 4096
MAX_OUTPUT_TOKENS = 2048
MAX_PROVIDER_CALLS_PER_SESSION = 10

def call_provider_with_limits(
    client,
    messages: list,
    model: str,
    call_counter: list,  # mutable counter passed by reference
) -> dict:
    if call_counter[0] >= MAX_PROVIDER_CALLS_PER_SESSION:
        raise RuntimeError("Provider call limit reached for this session")
    call_counter[0] += 1
    return client.messages.create(
        model=model,
        max_tokens=MAX_OUTPUT_TOKENS,
        messages=messages,
    )
```

**Why**: Runaway loops, adversarial inputs designed to trigger large completions, or bugs in session logic can generate unexpected API costs. Explicit per-session limits prevent bill shock.

**Refs**: OWASP LLM10:2025, OWASP LLM04:2025 (resource exhaustion variant)

---

## Quick Reference

| Category | Level | Key Risk | Control |
|----------|-------|----------|---------|
| LLM01 Prompt Injection | strict | Redirected AI behavior | Sanitize + pattern check |
| LLM02 Sensitive Info Disclosure | strict | Keys/paths in prompts | Field allowlist |
| LLM03 Supply Chain | strict | Compromised SDK | Hash-pinned deps |
| LLM04 Data Poisoning | strict | Corrupted scoring | Integrity check on load |
| LLM05 Improper Output Handling | strict | Code injection, bad JSON | Parse + validate |
| LLM06 Excessive Agency | strict | Arbitrary action dispatch | Action allowlist |
| LLM07 System Prompt Leakage | strict | Governance exposure | Reflection check |
| LLM08 Vector Weaknesses | n/a | Not applicable | -- |
| LLM09 Misinformation | strict | Hallucinated numerics | AI-03 / AI-04 guardrails |
| LLM10 Unbounded Consumption | warning | Cost runaway | Call + token limits |

---

## Version History

- **v1.0.0** - Initial release based on OWASP Top 10 for LLM Applications v2.0 (2025)
