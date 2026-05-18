# ChatGPT Usage Guide

How to use ChatGPT as your screenshot OCR assistant for Apeirogon Logistics.
This guide covers the AI vision extraction workflow from start to finish.

---

## What ChatGPT Does in This Workflow

ChatGPT reads your in-game mission terminal screenshots and extracts mission
data into JSON that the Apeirogon Logistics tools can score. It does **not**
make route decisions — that's the scorer's job. ChatGPT is strictly a vision
extraction tool in this workflow.

**Important**: ChatGPT will hallucinate numbers if not constrained. In testing,
more than half of unconstrained AI responses invented or modified game values —
reward amounts, SCU counts, fees — producing confident-looking but wrong output
that wastes contracts and in-game time. The strict prompt below prevents this.

---

## Before You Start

You need:
- A ChatGPT account (free or paid — both support image attachments)
- Your in-game screenshot(s) of the mission terminal
- Python and this repository (for running the scoring tools)

You do **not** need ChatGPT Plus for this workflow, but GPT-4o gives better
image reading than GPT-3.5.

---

## Step 1 — Start a New Chat

Open ChatGPT. Start a **new chat** — do not continue from a previous session.
Prior context can bleed into the extraction and introduce invented values.

---

## Step 2 — Paste the Strict Guardrail Prompt

Open `prompts/STRICT_AI_SESSION_PROMPT.md` from this repository.
Copy the entire contents and paste it into the ChatGPT chat. Send it.

Wait for ChatGPT to respond with:

> **STRICT MODE ACTIVE** — I will not invent, estimate, or adjust any numeric values.

If ChatGPT does not acknowledge with those words, paste the prompt again before
continuing. Do not proceed until you get the acknowledgement.

**Why this step is mandatory**: Without the strict prompt, ChatGPT fills in
missing or unclear values from its training data. Star Citizen prices, fees, and
capacities change with every patch — training data is always wrong. The strict
prompt forces ChatGPT to output `"UNRESOLVED"` instead of guessing.

---

## Step 3 — Tell ChatGPT Your Ship

In the same chat, type: *"I am flying a Hull-B."*

This tells ChatGPT which ship context to apply to the extraction. Replace
"Hull-B" with your actual ship if different.

---

## Step 4 — Paste the Extraction Prompt and Attach Your Screenshot

Open `prompts/AI_VISION_EXTRACTION_PROMPT.md`. Copy the extraction instructions
block (everything inside the document). Paste it into the chat.

Then attach your screenshot by clicking the paperclip / image icon in ChatGPT.

Send the message with both the extraction prompt and the image attached.

---

## Step 5 — Review ChatGPT's Output

ChatGPT will return a JSON block. **Before saving it**, check every value:

| Field | Check |
|-------|-------|
| `reward_usc` | Does this match the number on your screen exactly? |
| `cargo_scu` | Does this match the SCU count on your screen exactly? |
| `fee_usc` | If shown on screen, does it match? If not visible, should be `"UNRESOLVED"` |
| `pickup` | Is this the exact location shown? |
| `delivery` | Does this match all delivery locations shown? |

**Red flags — tell ChatGPT to correct these:**
- Any suspiciously round number you don't recall seeing (50,000, 100, etc.)
- A fee or reward that wasn't on screen at all
- A location that wasn't in the terminal

If anything is wrong, tell ChatGPT exactly what to fix:

> *"You invented [field name]. I did not give you that value. Replace it with UNRESOLVED."*

Do not accept "I approximated" or "based on typical values" as a response.
Every number must come from your screen or be marked UNRESOLVED.

---

## Step 6 — Save the JSON

Once verified, copy the JSON block ChatGPT returned. Save it as a file:

```
raw_extraction.json
```

Place it in your Apeirogon Logistics folder (or anywhere you can reference it).

---

## Step 7 — Run the Pipeline

```bash
python tools/OCR_result_normalizer.py -i raw_extraction.json -o missions_norm.json
python tools/ingest_mission_batch.py -i missions_norm.json
```

The normaliser resolves location aliases and issuer name variants.
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
when combined — this is the primary reason to use the batch tool.

---

## Common Problems

**ChatGPT returns text instead of JSON**

Ask it: *"Please return the extraction result as a JSON code block only."*

**ChatGPT returns partial JSON (cuts off mid-structure)**

Ask: *"The JSON was cut off. Please continue from where it stopped."* Or start
a new chat — very long responses sometimes truncate.

**ChatGPT says it can't read the screenshot**

Try: a higher-resolution screenshot, cropping to the mission terminal area only,
or screenshot with increased in-game UI scale.

**JSON parse error when running the normaliser**

The JSON from ChatGPT may have trailing commas or other syntax issues.
Check the file with a JSON validator. Fix any syntax errors before running
the pipeline.

**Scores look wrong after running the tools**

Check `unresolved_fields` in the output. Every unresolved field costs 2 points
(capped at -12). If SCU and reward are both UNRESOLVED, the score is less
accurate. Go back and verify those values from your screenshot.

---

## What Not to Do

| Don't | Why |
|-------|-----|
| Ask ChatGPT to recommend the best route | It doesn't have the scoring logic — use the tools |
| Use ChatGPT memory across sessions for mission data | Memory can carry over wrong values |
| Skip the strict prompt | Without it, hallucination rate exceeds 50% |
| Accept values ChatGPT "estimated" | Estimates are invented — use UNRESOLVED |
| Reuse an old chat for a new session | Prior context bleeds into extraction |

---

## Faster Repeat Use

Once you know the workflow, use `prompts/QUICK_SESSION_GUARDRAIL.md` instead
of `STRICT_AI_SESSION_PROMPT.md` for repeat sessions. It's a condensed 5-rule
version that still enforces the critical constraints.

---

## File Reference

| File | Purpose |
|------|---------|
| `prompts/STRICT_AI_SESSION_PROMPT.md` | Paste this first, every session |
| `prompts/QUICK_SESSION_GUARDRAIL.md` | Condensed version for repeat use |
| `prompts/AI_VISION_EXTRACTION_PROMPT.md` | Extraction instructions with screenshot |
| `docs/HALLUCINATION_GUARDRAILS.md` | Full explanation of the hallucination problem |
| `tools/OCR_result_normalizer.py` | Normalises raw extraction output |
| `tools/ingest_mission_batch.py` | Scores a batch of missions |
