# How to Avoid Bad AI Recommendations

This guide explains why AI providers produce wrong output for Star Citizen hauling, how to detect it before it costs you a run, and how to get useful output instead.

---

## Why AI Gives Bad Recommendations

AI language models are trained on data with a cutoff date. Star Citizen patches change commodity prices, landing fees, cargo capacities, and terminal availability constantly. No AI provider has current game state.

When an AI is asked about a value it does not have, it does not say "I don't know." It generates a plausible-sounding number based on patterns in its training data. This is not a bug; it is how these models work. The output looks confident and formatted correctly. It is wrong.

Three specific conditions make this worse for Star Citizen:

1. **Training data is stale by definition.** Game values change on a patch cycle. Even a model updated last month has prices that are already wrong.
2. **Hallucination fills gaps.** If the AI was not given a value in the prompt, it invents one rather than leaving the field blank.
3. **The AI has no game state.** It cannot see your terminal, your cargo hold, or current server commodity prices. Every number it produces that was not in your prompt is fabricated.

In preliminary testing across multiple providers, more than 50% of numeric fields were hallucinated when no strict prompt was used.

---

## The Three Failure Modes

### 1. Invented Numbers

The AI produces a reward, fee, or price that was not on your screen and was not in your prompt. These are the most dangerous because they look exactly like real values.

Signs: The number is round (e.g., exactly 50000 aUEC), the fee is a percentage of the reward that "makes sense," or the price matches what a commodity guide says it should be.

### 2. Adjusted Numbers

The AI was given a real number but "corrected" it. It decides the fee seems too low, or the reward is below what it expects for that route distance, and quietly changes it.

Signs: The output number is close to what you typed but not identical. The AI explains it "estimated based on typical values."

### 3. Invented Locations

The AI generates a pickup or delivery terminal that does not exist in the current patch, exists but is not accessible, or exists but does not carry the cargo in question.

Signs: The location name does not appear in your terminal list. The route goes to a station you have not seen in-game.

---

## Using the Strict Prompt

Before any AI session involving extraction or analysis, paste the full contents of `prompts/STRICT_AI_SESSION_PROMPT.md` into the chat. This is mandatory.

The strict prompt instructs the AI to:
- Only return values explicitly present in the image or text you provide
- Use UNRESOLVED for any field it cannot read
- Never estimate, infer, or fill gaps
- Acknowledge these constraints before proceeding

**What to do when the AI does not acknowledge:**

If you paste the strict prompt and the AI responds with extraction output immediately, or responds generically without acknowledging the specific constraints, stop. Start a new message and ask: *"Please confirm you have read and will follow all constraints in the prompt I just sent before we continue."*

If the AI cannot or will not confirm, fall back to manual entry. See `docs/MANUAL_COPY_PASTE_WORKFLOW.md`.

---

## How to Spot Hallucination in AI Output

Check every numeric field in the AI output against what you saw on your screen. Specific warning signs:

- **Fees that were not shown.** If you did not see a fee on the mission terminal, any fee value in the output is hallucinated.
- **Suspiciously round numbers.** Real game values are specific. Round values ending in 000 that were not on your screen are a red flag.
- **Locations not in your terminal.** If the AI lists a location that was not in the mission text you provided, that location is invented.
- **Any numeric field the AI "estimated."** If the AI uses the words "estimated," "approximately," "based on typical values," or "I assumed," that field is not safe to use.

The `provider_output_validator.py` tool flags unsourced numeric fields automatically. Read the `hallucination_flags` list in the validation output before passing anything to the scorer.

---

## Re-Anchoring: How to Tell AI It Invented Something

When you identify a hallucinated value, do not discard the session. Correct it directly:

> *"The fee_usc value you returned (12500) was not in the image I provided. I did not supply that value. Per the constraints you acknowledged, you must return UNRESOLVED for any field you cannot read directly from the source. Please correct your output."*

The AI should return UNRESOLVED for that field. If it instead provides another invented number, or argues that its estimate was reasonable, set that field to UNRESOLVED yourself before running the pipeline. Do not attempt further re-anchoring for that field.

---

## What AI Is Good For vs. What It Should Never Do

### AI is appropriate for:

- **OCR extraction from screenshots** when strictly constrained with the strict prompt. The AI reads text from an image you provide and returns exactly what it sees. This is a transcription task, not a reasoning task.
- **Formatting messy input** into valid JSON structure.
- **Identifying which fields are present** in a screenshot so you know what to fill manually.

### AI should never:

- **Decide route selection without the scorer.** The deterministic scorer exists specifically so that routing decisions are made on verified numbers, not AI reasoning.
- **Invent missing values.** Any field not readable from your source material must be UNRESOLVED.
- **Override what you saw on screen.** If you type a value and the AI "corrects" it, trust your screen.

---

## When to Use Deterministic Mode Instead

If you have your mission data already typed or can type it faster than an AI session takes, use deterministic mode directly. See `docs/MANUAL_COPY_PASTE_WORKFLOW.md`.

Use deterministic mode any time:
- You are tabbing between the game and your terminal and can read values directly
- You already have values and just need to re-score with corrections
- The AI is unavailable or slow
- You distrust a previous AI output and want a clean run

Deterministic mode has zero hallucination risk. It scores exactly what you give it.
