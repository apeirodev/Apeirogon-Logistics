# First Route Analysis: Step by Step

This is a complete walkthrough of a real Hull-B hauling session using Apeirogon
Logistics. Follow along with the example, then substitute your own mission data.

---

## Scenario

You're at Port Olisar with your Hull-B. You have four Covalex missions on screen:

| Mission | Pickup | Delivery | SCU | Reward |
|---------|--------|----------|-----|--------|
| A | Port Olisar | Covalex Hub Shopp-L4 | 24 | 12,500 aUEC |
| B | Port Olisar | Baijini Point | 16 | 9,000 aUEC |
| C | Port Olisar | Seraphim Station | 20 | 11,000 aUEC |
| D | Microtech | ARC-L1 | 32 | 8,500 aUEC |

Mission D has a different pickup (Microtech). Missions A, B, C all pick up from Port Olisar.

---

## Option 1: Type Missions Manually

Create a file called `my_missions.json` with this content:

```json
{
  "issuer": "covalex",
  "ship": "hull-b",
  "missions": [
    {"pickup": "Port Olisar", "delivery": ["Covalex Hub Shopp-L4"], "cargo_scu": 24, "reward_usc": 12500},
    {"pickup": "Port Olisar", "delivery": ["Baijini Point"], "cargo_scu": 16, "reward_usc": 9000},
    {"pickup": "Port Olisar", "delivery": ["Seraphim Station"], "cargo_scu": 20, "reward_usc": 11000},
    {"pickup": "Microtech", "delivery": ["ARC-L1"], "cargo_scu": 32, "reward_usc": 8500}
  ]
}
```

Then run:
```bash
python tools/ingest_mission_batch.py -i my_missions.json
```

---

## Option 2: Use AI to Read a Screenshot

If you have a screenshot of the mission terminal:

**Step 1: Open your AI account** (ChatGPT, Claude, or Gemini)

**Step 2: Paste the guardrail prompt**
Open `prompts/STRICT_AI_SESSION_PROMPT.md`, copy the full block, paste it into
the AI chat. Wait for the AI to respond with: "STRICT MODE ACTIVE"

If the AI doesn't acknowledge, paste the prompt again before proceeding.

**Step 3: Tell the AI your ship**
Type: *"I am flying a Hull-B."*

**Step 4: Paste the extraction prompt and attach the screenshot**
Open `prompts/AI_VISION_EXTRACTION_PROMPT.md`, copy the extraction prompt
block (everything between the lines), paste it into the chat, and attach your
screenshot.

**Step 5: Verify the AI's output**
The AI returns JSON. Before using it, check:
- Every `reward_usc` matches what you see on screen
- Every `cargo_scu` matches what you see on screen
- No values are suspiciously round (50,000 exactly, 100 SCU exactly)
- No locations are invented

If anything looks wrong, tell the AI: *"You invented [field]. I did not give
you that. Replace it with UNRESOLVED."*

**Step 6: Save and normalize**
Save the AI's JSON as `raw_extraction.json`. Then:
```bash
python tools/OCR_result_normalizer.py -i raw_extraction.json -o missions_norm.json
```

**Step 7: Score the batch**
```bash
python tools/ingest_mission_batch.py -i missions_norm.json
```

---

## Reading the Batch Output

The output has three main sections:

### batch_summary
```json
"batch_summary": {
  "mission_count": 4,
  "accepted": 1,
  "deferred": 2,
  "rejected": 1,
  "issuer": "covalex",
  "ship": "hull-b"
}
```

### ranked_missions
Sorted from highest to lowest score:
```json
"ranked_missions": [
  {"pickup": "Port Olisar", "delivery": ["Covalex Hub Shopp-L4"], "score": 50, "recommendation": "defer"},
  {"pickup": "Port Olisar", "delivery": ["Baijini Point"], "score": 50, "recommendation": "defer"},
  {"pickup": "Port Olisar", "delivery": ["Seraphim Station"], "score": 50, "recommendation": "defer"},
  {"pickup": "Microtech", "delivery": ["ARC-L1"], "score": 35, "recommendation": "reject"}
]
```

### same_pickup_stacking and suggested_combined_route
```json
"same_pickup_stacking": {
  "Port Olisar": [0, 1, 2]
},
"suggested_combined_route": {
  "stops": ["Port Olisar", "Covalex Hub Shopp-L4", "Baijini Point", "Seraphim Station"],
  "score": 82,
  "recommendation": "accept",
  "same_pickup_bonus": 2
}
```

**This is the key insight**: Missions A, B, and C individually score 50 (defer),
but combined they score 82 (accept) because three missions share Port Olisar
as their pickup, adding +32 for the same-pickup stacking bonus.

Mission D (Microtech) scores 35 (reject); it's a dead leg away from your
current location and breaks the orbital chain. Skip it unless the payout
justifies the empty flight to Microtech.

---

## The Decision

Based on this output, the recommended play is:

1. **Accept missions A, B, and C**: they stack at Port Olisar
2. **Skip mission D**: dead leg to Microtech breaks the chain

**Route sequence:**
1. Port Olisar → load cargo for all three missions
2. Covalex Hub Shopp-L4 → deliver A
3. Baijini Point → deliver B
4. Seraphim Station → deliver C

This is one pickup, three deliveries, no dead legs. The system scored it 82/100.

---

## What to Do Next

Go back to the mission terminal and look for more Port Olisar pickups to add
to the stack. The same-pickup bonus rewards stacking; each additional Port Olisar
mission adds more value to the run.

When you're done hauling, save your session for next time:
```bash
python tools/export_session_state.py
```

---

## Adjusting the Score

The score is a starting point, not a final answer. Override it when:

- Server conditions make a normally-good route impractical
- You know a station has freight elevator issues right now
- You're prioritising reputation with a specific issuer over efficiency
- A high-payout mission has other advantages the score doesn't capture

The score tells you about structural route quality. You bring the live game knowledge.

---

## More Resources

- `docs/ROUTE_ANALYSIS_HANDBOOK.md`: Full breakdown of every scoring factor
- `hull_b_covalex_route_playbook.md`: Hull-B stacking strategies in depth
- `ChatGPT_usage_guide.md` or `Claude_usage_guide.md`: Provider-specific AI workflow
- `docs/HALLUCINATION_GUARDRAILS.md`: What to do when AI invents numbers
