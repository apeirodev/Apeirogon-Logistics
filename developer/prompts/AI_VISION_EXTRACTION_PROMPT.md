# AI Vision Mission Extraction Prompt

Use this prompt to extract Star Citizen hauling mission data from screenshots.

**Before using this prompt**: paste `prompts/STRICT_AI_SESSION_PROMPT.md` and
wait for the AI to acknowledge STRICT MODE ACTIVE. If you skip that step, the
AI will fabricate numbers and the extraction will be useless.

---

## How to Use

1. Paste `STRICT_AI_SESSION_PROMPT.md` → wait for "STRICT MODE ACTIVE"
2. Copy the extraction prompt below and paste it into the same session
3. Attach or paste the screenshot of your mission contract terminal
4. Copy the JSON the AI returns
5. Save it to a file (e.g. `missions.json`)
6. Run: `python tools/OCR_result_normalizer.py -i missions.json`
7. Run: `python tools/ingest_mission_batch.py -i missions_normalized.json`

For multiple screenshots, run steps 3 to 6 for each, then combine the
`missions` arrays before running `ingest_mission_batch.py`.

---

## Extraction Prompt (copy everything between the lines)

---

I am attaching a screenshot of a Star Citizen mission contract terminal.

Extract every visible mission contract and return a single JSON object in exactly this format. Do not add explanations, prose, or markdown outside the JSON block.

STRICT RULES FOR THIS EXTRACTION:
- Copy every value EXACTLY as it appears in the screenshot. Do not reword, round, or adjust any numbers.
- If a field is not visible in the screenshot, output "UNRESOLVED" for that field.
- Do not use any Star Citizen knowledge from your training data. Only use what you can read in the screenshot.
- Do not invent cargo types, prices, distances, locations, or contract details.
- Do not "correct" any value you can see. If a price looks unusual, output it exactly as shown.

Return this JSON structure (one entry in "missions" per contract visible):

```json
{
  "advisory_only": true,
  "source_class": "ai_vision_extraction",
  "extraction_confidence": <number 0.0-1.0 reflecting how clearly you could read the screenshot>,
  "patch_version": "<patch version if visible, otherwise UNRESOLVED>",
  "ship": "<ship name if the user told you or it is visible, otherwise UNRESOLVED>",
  "missions": [
    {
      "issuer": "<issuer name exactly as shown, or UNRESOLVED>",
      "pickup": "<pickup location exactly as shown, or UNRESOLVED>",
      "delivery": ["<delivery location 1 exactly as shown>", "<delivery location 2 if any>"],
      "cargo_type": "<commodity name exactly as shown, or UNRESOLVED>",
      "cargo_scu": <number exactly as shown, or "UNRESOLVED">,
      "reward_usc": <number exactly as shown, or "UNRESOLVED">,
      "fee_usc": <number exactly as shown, or "UNRESOLVED">,
      "timer_minutes": <number if visible, or "UNRESOLVED">,
      "contract_type": "<contract type if visible, or UNRESOLVED>",
      "unresolved_fields": ["<list any fields you could not read>"],
      "notes": "<any extraction caveats -- do NOT put fabricated data here>"
    }
  ],
  "unresolved_fields": ["<any batch-level fields you could not read>"],
  "session_notes": "<overall notes about screenshot quality -- no fabricated data>"
}
```

If there are multiple contracts, add one object per contract to the "missions" array.

If you cannot read the screenshot at all, return:
```json
{
  "advisory_only": true,
  "source_class": "ai_vision_extraction",
  "extraction_confidence": 0.0,
  "missions": [],
  "unresolved_fields": ["screenshot_unreadable"],
  "session_notes": "Screenshot could not be read"
}
```

---

## Telling the AI Which Ship You're Flying

Before attaching the screenshot, tell the AI:

> "I am flying a Hull-B. My current cargo capacity from the loadout screen
> is [X] SCU. Add this as the 'ship' field in your output."

The AI cannot read your ship from the mission terminal screenshot. You must
supply this. Do not let the AI guess or estimate your ship's capacity.

---

## After You Have the JSON

**Check these things before running the normalizer:**

1. Every `reward_usc` value: does it match what you see on screen?
2. Every `cargo_scu` value: does it match what you see on screen?
3. Any field that is a round number (5000, 10000, 50000): did you
   actually see that exact number on screen? If not, it was fabricated.
4. Any location name: is it spelled correctly and does it match the screen?

If anything looks wrong, go back to the AI session and say:
> "You invented [field]. I did not give you that value. Replace it with UNRESOLVED."

Only run the normalizer once you are confident the extracted values match the screenshot.

---

## Example of Good AI Output

```json
{
  "advisory_only": true,
  "source_class": "ai_vision_extraction",
  "extraction_confidence": 0.82,
  "patch_version": "UNRESOLVED",
  "ship": "Hull-B",
  "missions": [
    {
      "issuer": "Covalex",
      "pickup": "Hur-L2",
      "delivery": ["Covalex Hub Shopp-L4"],
      "cargo_type": "Processed Food",
      "cargo_scu": 24,
      "reward_usc": 12500,
      "fee_usc": "UNRESOLVED",
      "timer_minutes": "UNRESOLVED",
      "contract_type": "cargo_hauling",
      "unresolved_fields": ["fee_usc", "timer_minutes"],
      "notes": ""
    }
  ],
  "unresolved_fields": ["patch_version"],
  "session_notes": "Screenshot was clear. Two fields not visible."
}
```

## Example of Bad AI Output (reject and re-prompt)

```json
{
  "reward_usc": 50000,
  "cargo_scu": 96
}
```

**Why this is bad**: round number 50000 was likely not visible; 96 SCU is the
Hull-B max capacity from training data, not from the screenshot. Both are
hallucinated. Reject and re-prompt with the re-anchor from STRICT_AI_SESSION_PROMPT.md.
