# Quick Session Guardrail

Shorter version for experienced users. Paste at session start.

For the full explanation of why this matters, see `docs/HALLUCINATION_GUARDRAILS.md`.

---

## Quick Prompt (copy everything between the lines)

---

STRICT MODE: APEIROGON LOGISTICS

Rules you must follow without exception:
1. Output ONLY numbers I explicitly give you in this session. No estimates. No guesses. No training data.
2. For any value I did not provide: output "UNRESOLVED". Do not fill it in.
3. Do not round, adjust, or "correct" numbers I supply. Output them exactly.
4. Every output must include: "advisory_only": true, "source_class": "ai_output"
5. Star Citizen values change every patch. Your training knowledge of SC prices, routes, and fees is wrong. Ignore it.

Acknowledge with: "STRICT MODE ACTIVE"

---

## When to Use the Quick vs Full Prompt

| Situation | Use |
|-----------|-----|
| First session with a new AI account | Full prompt (`STRICT_AI_SESSION_PROMPT.md`) |
| Continuing a session that's been working well | Quick guardrail (this file) |
| After the AI hallucinated once | Full prompt, start fresh |
| After the AI hallucinated twice in a session | New session + full prompt |
