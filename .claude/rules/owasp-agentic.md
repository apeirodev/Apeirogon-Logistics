# OWASP Top 10 for Agentic Applications 2026 - Security Rules

Security rules for autonomous AI agent workflows that execute multi-step tasks,
use tools, and take actions based on LLM reasoning.
Source: OWASP Gen AI Security Project -- https://genai.owasp.org/

**Note**: This rule file is based on the OWASP Top 10 for Agentic Applications
(2026 draft, released December 2025). The category numbering and names follow
the OWASP Gen AI Security Project's published draft. Verify against the final
release at https://genai.owasp.org/ as the standard matures.

**Scope**: Any workflow where an AI provider makes sequential decisions, invokes
tools, reads or writes files, or takes actions that persist beyond a single
prompt-response cycle.

---

## Overview

**Standard**: OWASP Top 10 for Agentic Applications (2026 draft)
**Applicability to this codebase**: Apeirogon Logistics does not currently run
an autonomous agent loop. However, users run AI assistants (Claude, ChatGPT, etc.)
with uploaded instruction blocks that direct multi-step route analysis sessions.
ASI01 (Goal Hijacking), ASI06 (Excessive Permissions), and ASI08 (Overreliance)
are the highest-risk categories for this use case.

---

## ASI01: Goal and Instruction Hijacking

**Risk Level**: Critical

### Rule: Treat All External Data as Potentially Adversarial Input

**Level**: `strict`

**When**: An agent processes data from external sources -- OCR output, user-supplied
JSON, provider responses, or content read from files -- and uses that data to
decide what action to take next.

**Do**:

```python
# Enforce structural validation before any agent step uses external data
def validate_agent_input(data: dict, expected_schema: dict) -> tuple[bool, list[str]]:
    """Validate that agent input matches expected structure before acting on it."""
    problems = []
    for required_key in expected_schema.get("required", []):
        if required_key not in data:
            problems.append(f"missing required field: {required_key}")
    for key, value in data.items():
        if isinstance(value, str) and check_injection_risk(value):
            problems.append(f"field '{key}' contains possible instruction injection")
    return len(problems) == 0, problems

# Separate data from instructions -- never interpolate data into the instruction block
def build_agent_context(instruction_block: str, user_data: dict) -> list[dict]:
    return [
        {"role": "user", "content": instruction_block},           # fixed
        {"role": "user", "content": json.dumps(user_data)},       # data only
    ]
```

**Don't**:

```python
# VULNERABLE: user data interpolated into the instruction block
instruction = f"{base_instructions}\n\nContract data: {raw_ocr_text}"
# An attacker who controls raw_ocr_text can override base_instructions
```

**Why**: Goal hijacking occurs when an attacker embeds instructions in data the
agent processes, redirecting it away from its intended task. Structural separation
of instructions and data prevents user-supplied content from modifying agent behavior.

**Refs**: OWASP ASI01:2026, OWASP LLM01:2025 (Prompt Injection), MITRE ATLAS AML.T0051

---

## ASI02: Memory Poisoning

**Risk Level**: High

### Rule: Never Persist Unvalidated Agent Output to Reusable Memory

**Level**: `strict`

**When**: Any agent session produces output that is stored and re-used as context
in future sessions (telemetry, scored routes, session logs).

**Do**:

```python
def persist_session_output(output: dict, session_id: str) -> None:
    # Validate governance metadata before persistence
    meta = output.get("governance_metadata", {})
    ok, problems = validate_governance_metadata(meta)
    if not ok:
        raise ValueError(f"Cannot persist unvalidated output: {problems}")
    # Store with provenance intact -- never strip governance_metadata on save
    output["_persisted_session"] = session_id
    output["_persisted_at"] = timestamp()
    dump_json(output, f"telemetry/{session_id}.json")
```

**Don't**:

```python
# VULNERABLE: stripping governance metadata before persistence
clean_output = {k: v for k, v in output.items() if k != "governance_metadata"}
json.dump(clean_output, open("history.json", "w"))
# Reloaded output will have no provenance -- poisoned data accepted as sourced fact
```

**Why**: Persisted agent output that lacks governance metadata can be reloaded in
future sessions and treated as authoritative, allowing a single compromised session
to propagate hallucinated or injected values across many future sessions.

**Refs**: OWASP ASI02:2026, NIST AI RMF MAP 1.5

---

## ASI03: Cascading Hallucinations

**Risk Level**: Critical (primary risk for this application)

### Rule: Break Reasoning Chains That Depend on Unverified Prior AI Outputs

**Level**: `strict`

**When**: An agent uses the output of one AI step as the input to another AI step
(chain-of-thought, multi-step analysis, sequential provider calls).

**Do**:

```python
def chain_provider_calls(step1_output: dict, step2_prompt: str) -> dict:
    # Validate step 1 output before feeding it to step 2
    ok, problems = validate_governance_metadata(
        step1_output.get("governance_metadata", {})
    )
    if not ok:
        return structured_error("step1 output failed governance validation -- chain aborted", problems)

    # Check that no numeric fields were added by the AI in step 1
    _, hallucination_flags = validate_numeric_sourcing(
        step1_output, user_supplied_fields=step2_prompt  # pass original user data
    )
    if hallucination_flags:
        return structured_error("hallucination risk in step1 output -- chain aborted", hallucination_flags)

    # Only pass the validated, sourced fields forward -- not the full AI output
    safe_carry_forward = {k: v for k, v in step1_output.get("sourced_facts", {}).items()}
    return call_provider(step2_prompt, context=safe_carry_forward)
```

**Don't**:

```python
# VULNERABLE: raw step 1 output fed directly to step 2
step2_output = provider.complete(step2_prompt + json.dumps(step1_output))
# Hallucinated values from step 1 become ground truth in step 2
```

**Why**: In multi-step AI workflows, an early hallucination compounds: each
subsequent step treats the previous step's output as fact, amplifying the
error. Validation gates between steps break the cascade.

**Refs**: OWASP ASI03:2026, OWASP LLM09:2025 (Misinformation), project rule AI-03

---

## ASI04: Resource Overuse and Runaway Execution

**Risk Level**: Medium

### Rule: Bound Agent Session Length, Cost, and Side Effects

**Level**: `warning`

**When**: Any workflow executes multiple provider calls or processes large batches
of missions.

**Do**:

```python
class AgentSessionBudget:
    def __init__(self, max_provider_calls: int = 10, max_files_written: int = 5):
        self.provider_calls = 0
        self.files_written = 0
        self.max_provider_calls = max_provider_calls
        self.max_files_written = max_files_written

    def check_provider_call(self) -> None:
        self.provider_calls += 1
        if self.provider_calls > self.max_provider_calls:
            raise RuntimeError(
                f"Session budget exceeded: {self.provider_calls} provider calls "
                f"(max {self.max_provider_calls})"
            )

    def check_file_write(self, path: str) -> None:
        self.files_written += 1
        if self.files_written > self.max_files_written:
            raise RuntimeError(
                f"Session budget exceeded: {self.files_written} files written "
                f"(max {self.max_files_written})"
            )
```

**Refs**: OWASP ASI04:2026, OWASP LLM10:2025 (Unbounded Consumption)

---

## ASI05: Tool and Function Misuse

**Risk Level**: High

### Rule: Validate Tool Inputs Against an Allowlist Before Execution

**Level**: `strict`

**Note**: This maps to the agent-security.md rule "Validate Tool Calls Before
Execution". The ASI05 category is the OWASP Agentic formal reference for that
project rule.

**Do**: See agent-security.md "Validate Tool Calls Before Execution" for the
`ToolCall`, `SecureToolExecutor`, and `ToolPermissionPolicy` patterns required.

**Why**: An agent instructed by a hijacked prompt or a compromised provider
response can invoke tools with malicious parameters. Tool input validation at
the executor level prevents parameter injection regardless of how the tool call
was generated.

**Refs**: OWASP ASI05:2026, OWASP LLM07:2025 (Insecure Plugin Design)

---

## ASI06: Privilege Escalation and Excessive Permissions

**Risk Level**: High

### Rule: Grant Agent Sessions the Minimum Permissions Required for the Task

**Level**: `strict`

**When**: Configuring what files, paths, or external services an agent session
can access.

**Do**:

```python
# Declare permissions explicitly at session start -- do not inherit caller's permissions
SESSION_PERMISSIONS = {
    "read_paths": ["player/uploads/", "developer/data/"],
    "write_paths": ["output/", "telemetry/"],
    "network": False,           # no outbound calls except configured provider
    "shell_execution": False,   # never
    "provider_calls": True,
}

def authorize_agent_action(action_type: str, target: str, permissions: dict) -> bool:
    if action_type == "read_file":
        return any(target.startswith(p) for p in permissions["read_paths"])
    if action_type == "write_file":
        return any(target.startswith(p) for p in permissions["write_paths"])
    if action_type == "shell":
        return permissions.get("shell_execution", False)
    return False
```

**Don't**:

```python
# VULNERABLE: agent inherits full caller permissions
def run_agent(task):
    return agent.execute(task)   # no permission scope defined
```

**Why**: Principle of least privilege limits the blast radius of a compromised
or misbehaving agent session to only the resources it was explicitly granted.

**Refs**: OWASP ASI06:2026, NIST AI RMF GOVERN 1.2, OWASP A01:2025

---

## ASI07: Deceptive Identity and Spoofing

**Risk Level**: Medium (primarily a multi-agent concern)

### Rule: Verify the Source of Any Agent-to-Agent Communication

**Level**: `warning`

**Note**: Apeirogon Logistics does not currently run multi-agent pipelines. This
rule applies if a future phase adds agent orchestration (e.g. a scoring agent
and a route planning agent communicating). File it now as a forward-looking
constraint.

**Do**:

```python
# If multi-agent communication is added, verify provenance on all inter-agent messages
def accept_agent_message(message: dict) -> bool:
    required = {"source_agent_id", "session_id", "payload_hash", "governance_metadata"}
    if not required.issubset(message.keys()):
        return False
    # Verify hash of payload matches claimed hash
    actual = stable_hash(message["payload"])
    return hmac.compare_digest(actual, message["payload_hash"])
```

**Refs**: OWASP ASI07:2026, NIST AI RMF GOVERN 1.2

---

## ASI08: Overreliance on AI Output

**Risk Level**: Critical (primary operational risk for this application)

### Rule: Every AI-Assisted Workflow Must Preserve Human Decision Authority

**Level**: `strict`

**When**: An AI session produces a route recommendation, score, or accept/defer/reject
verdict that the user will act on.

**Do**:

The instruction block and all provider setup guides must:
1. Instruct the AI to produce `advisory_only: true` on all outputs
2. Present Accept / Defer / Reject as recommendations, not commands
3. Explicitly state that numeric values (reward, fee, SCU) must have been
   supplied by the user -- the AI must not invent them
4. Flag any field it could not read from the screenshot as UNRESOLVED rather
   than guessing

From `STRICT_AI_SESSION_PROMPT.md`:
> "Do not invent, estimate, or assume any numeric value. If you cannot read a
> field from the screenshot, mark it UNRESOLVED and ask me before proceeding."

**Don't**:

- Ship a workflow where the AI presents recommendations without an explicit
  advisory-only disclaimer
- Let the AI silently fill UNRESOLVED fields with "typical" or "estimated" values
- Present AI output in a format that implies it is ground truth rather than analysis

**Why**: The core operational risk of this application is a user committing to a
haul based on AI-invented numbers. The contract is real. The time and cargo are
real. A hallucinated reward figure or fee estimate causes a real loss. Mandatory
advisory framing and UNRESOLVED tagging are the primary human-in-the-loop controls.

**Refs**: OWASP ASI08:2026, OWASP LLM09:2025, NIST AI RMF MAP 5.1, project rules AI-03/AI-04

---

## ASI09: Uncontrolled Multi-Agent Escalation

**Risk Level**: Low (not currently applicable)

**Note**: Apeirogon Logistics uses a single AI session per user interaction.
There is no agent spawning or sub-agent delegation. This category is not
applicable to the current architecture. Apply this rule if orchestration is
added in a future phase.

**Refs**: OWASP ASI09:2026

---

## ASI10: Audit and Observability Failures

**Risk Level**: Medium

### Rule: Produce a Complete Audit Trail for Every Agent Session That Writes Output

**Level**: `warning`

**When**: Any agent-assisted session produces output that is saved to disk.

**Do**:

```python
def write_auditable_output(result: dict, session_id: str, output_path: str) -> None:
    # Governance metadata must be present
    if "governance_metadata" not in result:
        raise ValueError("Cannot write output without governance_metadata (ASI10)")

    # Add session trace before saving
    result["_audit"] = {
        "session_id": session_id,
        "written_at": timestamp(),
        "output_hash": stable_hash(result),
    }
    dump_json(result, output_path)
```

**Don't**:

```python
# VULNERABLE: no session traceability
json.dump({"score": 72, "recommendation": "accept"}, open(output, "w"))
```

**Why**: Without audit trails, there is no way to reconstruct which AI session
produced a scored output, what inputs it received, or whether its governance
metadata was present at the time of writing. Replay and integrity verification
tools depend on these fields.

**Refs**: OWASP ASI10:2026, NIST AI RMF MEASURE 1.1, project replay tools

---

## Quick Reference

| Category | Level | Key Risk | Control |
|----------|-------|----------|---------|
| ASI01 Goal Hijacking | strict | Redirected agent behavior | Separate instructions from data |
| ASI02 Memory Poisoning | strict | Persisted bad output as truth | Governance validation before save |
| ASI03 Cascading Hallucinations | strict | Compounding AI errors | Validation gates between steps |
| ASI04 Resource Overuse | warning | Cost/side-effect runaway | Session budget limits |
| ASI05 Tool Misuse | strict | Malicious tool invocation | Input allowlist + executor validation |
| ASI06 Excessive Permissions | strict | Blast radius on compromise | Least privilege scope |
| ASI07 Identity Spoofing | warning | Fake agent messages | Provenance verification (future) |
| ASI08 Overreliance | strict | User acts on invented data | Advisory-only + UNRESOLVED tagging |
| ASI09 Multi-Agent Escalation | n/a | Not applicable | -- |
| ASI10 Audit Failures | warning | No session traceability | Mandatory _audit block |

---

## Version History

- **v1.0.0** - Initial release based on OWASP Top 10 for Agentic Applications (2026 draft, December 2025)
