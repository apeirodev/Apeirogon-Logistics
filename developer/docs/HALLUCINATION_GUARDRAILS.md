# Hallucination Guardrails

## The Problem

In live testing, AI assistants (ChatGPT, Claude, Gemini, and others) hallucinated
mission-critical numbers more than half the time when given Star Citizen hauling
data without strict constraints.

Observed failures:
- Making up cargo prices not present in the provided data
- "Correcting" player-supplied numbers using training-data guesses
- Inventing box counts, capacities, or distances
- Rounding fees to suspiciously clean numbers
- Fabricating stop names that don't exist
- Adjusting profit calculations using numbers the player never supplied

Every hallucinated number wastes real in-game time and burns real contracts.
This is not an acceptable outcome. Strict guardrails are mandatory.

---

## How It Works in This System

All AI interaction in Apeirogon Logistics operates under three non-negotiable rules:

1. **AI output is always `advisory_only: true`**: it is never authoritative
2. **Every AI output must pass governance metadata validation** before use
3. **Every AI session must start with the mandatory session prompt** (see below)

These are enforced in `tools/provider_output_validator.py`. Any output that fails
validation is rejected before it reaches the scoring pipeline.

---

## Mandatory Session Prompt

**Paste this at the start of every AI session before asking anything.**

The full prompt is in `prompts/STRICT_AI_SESSION_PROMPT.md`.

A condensed version for quick use is in `prompts/QUICK_SESSION_GUARDRAIL.md`.

Do not skip this step. The session prompt is what prevents hallucination.
Without it, most AI assistants will fill gaps with plausible-sounding invented data.

---

## Why AI Assistants Hallucinate Star Citizen Data

Star Citizen prices, fees, routes, and capacities change with every major patch.
AI models were trained on older data. When you ask about current values, the model:

- Cannot know current prices (training cutoff may be months or years old)
- Will guess based on patterns from training data
- Will present guesses as confident answers unless explicitly told not to
- Will "adjust" numbers you give it if they seem inconsistent with its priors

The mandatory session prompt overrides this behaviour by explicitly instructing
the AI to treat your supplied data as ground truth and to use `UNRESOLVED` for
anything it doesn't know.

---

## What "UNRESOLVED" Means

When an AI returns `"UNRESOLVED"` for a field, it means:

- The AI does not have that data from what you provided
- It is refusing to guess
- You must supply the value yourself, or leave it unresolved

An `UNRESOLVED` in the output is **correct and safe behaviour**. It is far better
than an invented number.

The scoring system handles `UNRESOLVED` fields gracefully; they are excluded
from scoring calculations and flagged in the `unresolved_field_list`.

---

## Validating AI Output

After receiving output from any AI assistant, run it through the validator:

```bash
echo '<ai_output_json>' | python tools/provider_output_validator.py
```

The validator checks:
- `advisory_only` is `true`
- `governance_metadata` is present and valid
- `source_class` is `ai_output` (not `deterministic_output` or `sourced_fact`)
- No sourced fields have been overwritten

If validation fails, do not use the output. Ask the AI to reformat its response
using the output schema in `schema/ocr_normalization.schema.json`.

---

## Red Flags: Reject and Re-Ask

If you see any of these in an AI response, reject the output and re-prompt:

| Red Flag | What It Means |
|----------|---------------|
| Numbers you didn't provide | Fabricated from training data |
| Suspiciously round numbers (e.g. 50,000 aUEC exactly) | Guessed, not calculated |
| Stop names you didn't mention | Hallucinated locations |
| "Based on typical Star Citizen rates..." | AI is using training data, not your data |
| Confidence without sourcing | Not grounded in what you gave it |
| Missing `advisory_only: true` | Output bypassed the required framing |

---

## Enforcing Guardrails When Re-Prompting

If the AI produces hallucinated output, re-anchor it with:

> "You invented that number. I did not provide it. Remove it and replace it
> with UNRESOLVED. Do not use any Star Citizen knowledge from your training.
> Only use numbers I have explicitly given you in this session."

This re-establishes the constraint without starting a new session.

---

## Operator Responsibility

This platform cannot prevent hallucination; it can only detect it after the fact
through schema validation and governance metadata checks.

**The human operator is the final check.** Before accepting any AI recommendation:

1. Verify every number in the output against what you typed in
2. Reject anything you didn't supply
3. Run the output through `provider_output_validator.py`
4. Treat the score as advisory; your in-game judgment overrides it

---

## Hull-B Specific Notes

The Hull-B has very specific capacity constraints that AI assistants frequently
get wrong:

- Cargo is measured in SCU, not boxes or units
- Hull-B max capacity is patch-dependent; do not trust the AI's stated capacity
- Always supply capacity from your in-game ship loadout screen
- Fee calculations depend on route distance; AI cannot know your current
  quantum route unless you provide it explicitly

Supply these values yourself. Do not let the AI fill them in.
