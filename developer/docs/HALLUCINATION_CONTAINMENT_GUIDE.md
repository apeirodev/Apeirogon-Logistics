# Hallucination Containment Guide

Technical reference for how the Apeirogon Logistics codebase identifies, flags, and limits the impact of AI hallucination on scoring and route decisions.

---

## The Problem

In preliminary testing across multiple AI providers without strict prompting, more than 50% of numeric fields in provider output were hallucinated — that is, the AI produced values that were not present in the source material provided.

Star Citizen game values (prices, rewards, fees, distances, cargo capacities) change on a patch cycle. AI training data is always behind the current patch. When asked to extract or reason about these values, AI providers fill gaps with plausible-sounding invented data that is indistinguishable from real values in format and presentation.

The codebase addresses this with several layered controls described in this document.

---

## The UNRESOLVED Sentinel

`UNRESOLVED` is the string value used throughout the pipeline to represent a field that could not be reliably read from source material.

It is intentionally not a number. This means:
- It cannot be silently passed into arithmetic. Any downstream calculation that receives UNRESOLVED will produce a visible error rather than a quietly wrong result.
- It is explicit. Anyone reading the output knows the value was not obtained.
- It carries a defined scoring penalty (-2 points per UNRESOLVED field, capped at -12 total).

**Why UNRESOLVED is better than a guess:**

A wrong number looks right. A -2 penalty from UNRESOLVED is visible and bounded. A hallucinated `fee_usc` that is off by 40,000 aUEC can flip a mission from profitable to a loss. The scoring system is designed so that UNRESOLVED produces a predictable, visible, limited penalty — while a bad number produces a confidently wrong result.

When AI extraction returns a value for a field that was not present in the source, replace it with UNRESOLVED before running the pipeline.

---

## Source Separation

The codebase enforces strict separation between data of different provenance. The core rule:

**AI output is never merged into sourced_facts.**

Pipeline output structures keep these keys separate at the top level:
- `sourced_facts`: values supplied directly by the operator from the game screen
- `ai_recommendation`: advisory output from an AI provider
- `ocr_extraction`: output from AI-assisted OCR extraction
- `unresolved_fields`: fields that could not be read

The `governance_metadata` block in every output record includes a `source_class` field tracking data origin. Valid values include `deterministic_output`, `ai_output`, `ai_vision_extraction`, `ocr_extraction`, `user_correction`, and `telemetry`.

Merging source classes with `{**sourced_data, **ai_output}` or equivalent destroys provenance and is treated as a security violation (see rule SRC-01 in CLAUDE.md). A field in `sourced_facts` must have come from the operator reading a game screen. It may not be promoted from `ai_output`.

---

## provider_output_validator.py

Before AI extraction output reaches the normalizer or scorer, it passes through the provider output validator. The validator enforces:

1. **`advisory_only` must be `true`.** Any provider output that does not carry this flag is rejected.
2. **`source_class` must be `ai_output` or `ai_vision_extraction`.** The governance metadata block must correctly identify the data's origin.
3. **Unsourced numeric fields are flagged.** The validator compares every numeric field in the AI output against the set of fields the operator actually supplied. Any numeric field present in the AI output that was not in the user-supplied input is added to `hallucination_flags`.

The validator does not auto-reject on hallucination flags — it surfaces them for operator review. Some fields may be correctly derivable (e.g., `profit_usc` = `reward_usc` - `fee_usc` when both were supplied). The operator must review each flag.

---

## The hallucination_flags Field

Every validated provider output record contains a `hallucination_flags` list in its governance metadata:

```json
{
  "governance_metadata": {
    "source_class": "ai_output",
    "advisory_only": true,
    "hallucination_flags": [
      "HALLUCINATION_RISK: fee_usc not in user-supplied data",
      "HALLUCINATION_RISK: distance_km not in user-supplied data"
    ]
  }
}
```

A record with an empty `hallucination_flags` list passed validation cleanly. A record with flags requires operator review before flagged fields are accepted. Do not pass flagged fields downstream without making an explicit decision: either confirm the value against your screen, or replace it with UNRESOLVED.

---

## Scoring Penalty for Unresolved Fields

- **-2 points per UNRESOLVED field**
- **Maximum penalty: -12 points** regardless of how many fields are UNRESOLVED

With a base score of 50, the maximum UNRESOLVED penalty produces a score of 38 (reject). A single UNRESOLVED field on an otherwise strong mission produces a score of 48+, which is defer territory. The operator can then decide whether to read the missing value or proceed with the defer recommendation.

---

## HALLUCINATION_RISK_FIELDS

The following fields are defined as hallucination risk fields throughout the codebase. Any of these appearing in AI output that were not in operator-supplied input will be flagged:

- `reward_usc`
- `fee_usc`
- `profit_usc`
- `cargo_scu`
- `price_usc`
- `distance_km`
- `capacity_scu`

These are the fields where hallucination has the most direct operational impact. A wrong `reward_usc` changes whether a mission is worth taking. A wrong `cargo_scu` means the AI thought you had capacity you do not have.

---

## End-to-End Workflow

1. **Paste the strict prompt.** New chat, paste `prompts/STRICT_AI_SESSION_PROMPT.md`, wait for explicit acknowledgement.
2. **Attach screenshot and extraction prompt.** Provide the image and `prompts/AI_VISION_EXTRACTION_PROMPT.md`.
3. **Verify output against your screen.** Check every value. Check `hallucination_flags` from the validator.
4. **Run OCR_result_normalizer.py.** Normalizes extraction output, applies UNRESOLVED sentinel.
5. **Run ingest_mission_batch.py.** Scored by deterministic_scorer.py.
6. **Read the scored output.** Accept >= 70, defer 45 to 69, reject < 45.

---

## If AI Says It Estimated

If the AI output contains language like "I estimated," "I assumed," "based on typical values," or "approximately," treat every field accompanied by that language as unverified.

Replace those field values with UNRESOLVED and re-run the pipeline. The scoring penalty for UNRESOLVED is bounded and visible. The risk of acting on a plausible-sounding wrong estimate is not.
