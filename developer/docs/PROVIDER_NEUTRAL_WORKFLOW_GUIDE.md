# Provider-Neutral AI Vision Workflow Guide

How to run the AI-assisted extraction workflow in a way that works the same regardless of which provider you use.

---

## Overview

The extraction workflow has three phases. All three are the same whether you are using ChatGPT, Claude, Ollama, LM Studio, or any other vision-capable provider. The provider is interchangeable. The workflow is not.

---

## Phase 1: Paste the Strict Prompt and Get Acknowledgement

Open a new chat session with your chosen provider.

Paste the full contents of `prompts/STRICT_AI_SESSION_PROMPT.md` into the chat. Send it on its own before attaching any images.

Wait for the AI to explicitly acknowledge the constraints, specifically that it will:
- Only return values present in the material you provide
- Use UNRESOLVED for any field it cannot read
- Not estimate, infer, or fill gaps

If the AI responds generically without acknowledging the specific constraints, ask directly: *"Please confirm you have read and will follow all constraints in the prompt I just sent before we continue."*

If it will not confirm, fall back to manual entry rather than proceeding without the guardrails. See `docs/MANUAL_COPY_PASTE_WORKFLOW.md`.

Do not attach a screenshot until you have acknowledgement.

---

## Phase 2: Attach Screenshot and Paste the Extraction Prompt

Once the AI has acknowledged, attach your mission terminal screenshot and paste the extraction prompt from `prompts/AI_VISION_EXTRACTION_PROMPT.md`.

The AI should return a JSON structure with mission fields it can read from the image, and `"UNRESOLVED"` for anything not clearly visible.

If the AI returns values not in the image, or uses language like "I estimated" or "based on typical values," see `docs/HOW_TO_AVOID_BAD_AI_RECOMMENDATIONS.md`.

---

## Phase 3: Verify Output and Run the Pipeline

Before running any pipeline tool, check the AI output against your screen. Confirm `reward_usc`, `fee_usc`, and `cargo_scu` against what is displayed in the game. These have the highest hallucination risk and most direct impact on scoring.

If a value does not match your screen, correct it. If a field appears in `hallucination_flags` in the validator output, either confirm it against your screen or replace it with `"UNRESOLVED"`.

Once verified:

```bash
python tools/OCR_result_normalizer.py -i ai_extraction_output.json -o normalized.json
python tools/ingest_mission_batch.py -i normalized.json
```

---

## Why Provider Does Not Matter for Extraction

When constrained by the strict prompt, all supported providers behave the same for the extraction task. They are reading text from an image and transcribing it to JSON, a transcription task rather than a reasoning task.

The strict prompt is what controls quality. Without it, all providers hallucinate at rates above 50% for numeric fields. With it, all providers reduce that rate significantly. Switching providers does not change your workflow, your prompts, or your verification steps.

---

## The Pipeline After Extraction

The AI is only involved in the extraction step. The rest is fully deterministic:

1. **OCR_result_normalizer.py**: normalizes AI extraction output to pipeline schema, applies UNRESOLVED sentinel, validates `advisory_only` and `source_class`.
2. **ingest_mission_batch.py**: runs normalized mission data through the deterministic scorer, produces ranked output with route suggestions.

---

## Switching Providers Mid-Session

You can switch providers at any point. The pipeline has no state tied to which provider produced the extraction output.

When switching:
- Start a new chat session with the new provider
- Paste `prompts/STRICT_AI_SESSION_PROMPT.md` again
- Get acknowledgement before proceeding
- Do not carry unverified output from one session into another

---

## When the AI Is Unavailable

Fall back to manual entry. See `docs/MANUAL_COPY_PASTE_WORKFLOW.md`.

Manual entry with hand-typed values is the highest-reliability path in the system. It has no external dependencies and zero hallucination risk. Switching to it when AI is unavailable is not a downgrade.

---

## Prompt Files Reference

| File | When to use |
|------|------------|
| `prompts/STRICT_AI_SESSION_PROMPT.md` | Start of every AI session, mandatory |
| `prompts/AI_VISION_EXTRACTION_PROMPT.md` | Phase 2, with screenshot |
| `prompts/QUICK_SESSION_GUARDRAIL.md` | Condensed re-anchor for follow-up messages in the same session |
