> **LEGACY -- this guide describes the old two-step JSON extraction workflow (AI extracts JSON, Python scores it). The current workflow is AI-as-advisor: paste the instruction block from your platform's SETUP file in `player/project_instructions/` and use screenshots directly. This file is kept for historical reference only.**

# Claude Usage Guide

How to use Claude (claude.ai) as your screenshot OCR assistant for Apeirogon Logistics.
This guide covers the AI vision extraction workflow from start to finish.

---

## What Claude Does in This Workflow

Claude reads your in-game mission terminal screenshots and extracts mission
data into JSON that the Apeirogon Logistics tools can score. It does **not**
make route decisions; that's the scorer's job. Claude is strictly a vision
extraction tool in this workflow.

**Important**: Claude will hallucinate numbers if not constrained. In testing,
more than half of unconstrained AI responses invented or modified game values,
including reward amounts, SCU counts, and fees, producing confident-looking but wrong output
that wastes contracts and in-game time. The strict prompt below prevents this.

---

## Before You Start

You need:
- A Claude account at claude.ai (free tier works; Pro gives longer context)
- Your in-game screenshot(s) of the mission terminal
- Python and this repository (for running the scoring tools)

Claude supports image attachments in all tiers. You do not need a Pro account
for screenshot extraction, though Pro's longer context window helps with multiple
screenshots in one session.

---

## Step 1: Start a New Conversation

Go to claude.ai and start a **new conversation**. Do not continue from a previous
session for a new gaming run, as prior context can affect extraction results.

---

## Step 2: Paste the Strict Guardrail Prompt

Open `prompts/STRICT_AI_SESSION_PROMPT.md` from this repository.
Copy the entire contents and paste it into the Claude conversation. Send it.

Wait for Claude to respond with:

> **STRICT MODE ACTIVE**: I will not invent, estimate, or adjust any numeric values.

If Claude does not acknowledge with those words, paste the prompt again before
continuing. Do not proceed until you get the acknowledgement.

**Why this step is mandatory**: Without the strict prompt, Claude fills in
missing or unclear values from its training data. Star Citizen prices, fees, and
capacities change with every patch, so training data is always wrong. The strict
prompt forces Claude to output `"UNRESOLVED"` instead of guessing.

---

## Step 3: Tell Claude Your Ship

In the same conversation, type: *"I am flying a Hull-B."*

This tells Claude which ship context to apply to the extraction. Replace
"Hull-B" with your actual ship if different.

---

## Step 4: Paste the Extraction Prompt and Attach Your Screenshot

Open `prompts/AI_VISION_EXTRACTION_PROMPT.md`. Copy the extraction instructions
block (everything inside the document). Paste it into the conversation.

Then attach your screenshot using the paperclip icon in the Claude chat input.

Send the message with both the extraction prompt and the image attached.

---

## Step 5: Review Claude's Output

Claude will return a JSON block. **Before saving it**, check every value:

| Field | Check |
|-------|-------|
| `reward_usc` | Does this match the number on your screen exactly? |
| `cargo_scu` | Does this match the SCU count on your screen exactly? |
| `fee_usc` | If shown on screen, does it match? If not visible, should be `"UNRESOLVED"` |
| `pickup` | Is this the exact location shown? |
| `delivery` | Does this match all delivery locations shown? |

**Red flags, tell Claude to correct these:**
- Any suspiciously round number you don't recall seeing (50,000, 100, etc.)
- A fee or reward that wasn't on screen at all
- A location that wasn't in the terminal

If anything is wrong, tell Claude exactly what to fix:

> *"You invented [field name]. I did not give you that value. Replace it with UNRESOLVED."*

Do not accept "I estimated" or "based on typical mission values" as a response.
Every number must come from your screen or be marked UNRESOLVED.

---

## Step 6: Save the JSON

Once verified, copy the JSON block Claude returned. Save it as a file:

```
raw_extraction.json
```

Place it in your Apeirogon Logistics folder (or anywhere you can reference it).

---

## Step 7: Run the Pipeline

```bash
python tools/OCR_result_normalizer.py -i raw_extraction.json -o missions_norm.json
python tools/ingest_mission_batch.py -i missions_norm.json
```

The normalizer resolves location aliases and issuer name variants.
The batch tool scores each mission individually, identifies same-pickup stacking
opportunities, and suggests a combined route.

---

## Reading the Output

Look for three things:

**1. `same_pickup_stacking`**
Shows which missions share a pickup location. These are your stacking opportunities.

**2. `suggested_combined_route.score`**
The score of the optimal combined run. This is often higher than any individual
mission score because the same-pickup stacking bonus (+16 per stacked mission)
only activates when missions are combined.

**3. `ranked_missions`**
Individual scores. Missions that score "defer" individually often score "accept"
when combined, which is the primary reason to use the batch tool.

---

## Using Claude Projects (Optional)

If you use Claude's Projects feature, you can add the following files as
project knowledge to save pasting them each session:

- `prompts/STRICT_AI_SESSION_PROMPT.md`
- `prompts/AI_VISION_EXTRACTION_PROMPT.md`

With these in project knowledge, Claude loads the guardrail rules automatically.
You still need to confirm at the start of each conversation that strict mode is
active. Type *"Confirm strict mode"* and wait for acknowledgement before
attaching screenshots.

**Note**: Do not add session state files or mission data to project knowledge.
That data changes every run and belongs in the conversation, not the project.

---

## Common Problems

**Claude returns text instead of JSON**

Ask it: *"Please return the extraction result as a JSON code block only, no commentary."*

**Claude adds a disclaimer after the JSON**

The JSON is still valid. Copy only the JSON block, not the disclaimer text.

**Claude says it can't see details in the screenshot**

Try: a higher-resolution screenshot, cropping to the mission terminal area only,
or increasing in-game UI scale before screenshotting.

**JSON parse error when running the normalizer**

Check the file with a JSON validator. Claude occasionally produces minor syntax
issues on complex structures. Fix any syntax errors before running the pipeline.

**Scores look wrong after running the tools**

Check `unresolved_fields` in the output. Every unresolved field costs 2 points
(capped at -12). If SCU and reward are both UNRESOLVED, the score is less
accurate. Go back and verify those values from your screenshot.

---

## What Not to Do

| Don't | Why |
|-------|-----|
| Ask Claude to recommend the best route | It doesn't have the scoring logic; use the tools |
| Add mission data to project knowledge | It changes every session; put it in the conversation |
| Skip the strict prompt | Without it, hallucination rate exceeds 50% |
| Accept values Claude "inferred" | Inferred values are invented; use UNRESOLVED |
| Reuse an old conversation for a new session | Prior context bleeds into extraction |

---

## Faster Repeat Use

Once you know the workflow, use `prompts/QUICK_SESSION_GUARDRAIL.md` instead
of `STRICT_AI_SESSION_PROMPT.md` for repeat sessions. It's a condensed 5-rule
version that still enforces the critical constraints.

If you have added the full strict prompt to project knowledge, you can skip
pasting it each time. Just confirm strict mode is active at conversation start.

---

## File Reference

| File | Purpose |
|------|---------|
| `prompts/STRICT_AI_SESSION_PROMPT.md` | Paste this first, every session |
| `prompts/QUICK_SESSION_GUARDRAIL.md` | Condensed version for repeat use |
| `prompts/AI_VISION_EXTRACTION_PROMPT.md` | Extraction instructions with screenshot |
| `docs/HALLUCINATION_GUARDRAILS.md` | Full explanation of the hallucination problem |
| `tools/OCR_result_normalizer.py` | Normalizes raw extraction output |
| `tools/ingest_mission_batch.py` | Scores a batch of missions |
