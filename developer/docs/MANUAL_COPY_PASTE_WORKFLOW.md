# Manual Copy-Paste Workflow

Complete guide to running the pipeline with no AI provider. You type the values, the scorer does the rest.

---

## When to Use This Workflow

- You do not have an AI account or prefer not to use one
- You are playing offline or on a slow connection
- You are tabbing directly between the game and your terminal and can read values faster than an AI session takes
- You ran an AI extraction and want to verify or correct the output before scoring
- You want the highest possible confidence in your numbers (manual entry has zero hallucination risk)

This is a first-class workflow, not a fallback. The deterministic scorer produces the same quality output regardless of how the input JSON was created.

---

## Step by Step

### 1. Open a terminal in the project directory

### 2. Create a missions JSON file

Create a new file — for example, `my_missions.json` — using the template in the next section.

### 3. Fill in values from your screen

Tab into Star Citizen, open the mission terminal or Covalex kiosk, and read each value directly from the screen. Enter exactly what you see. Do not round, estimate, or fill in values you are not sure about.

### 4. Set UNRESOLVED for anything you cannot read clearly

If a value is cut off, unclear, or not shown, use the string `"UNRESOLVED"`. See below.

### 5. Run the pipeline

```bash
python tools/ingest_mission_batch.py -i my_missions.json
```

---

## JSON Template

Copy this and fill in the values from your screen. Remove missions you are not entering. Add more blocks as needed.

```json
{
  "issuer": "covalex",
  "ship": "hull-b",
  "missions": [
    {
      "pickup": "PORT_OLISAR_OR_WHATEVER_YOU_SEE",
      "delivery": ["DELIVERY_LOCATION_FROM_SCREEN"],
      "reward_usc": "UNRESOLVED",
      "cargo_scu": "UNRESOLVED"
    },
    {
      "pickup": "PORT_OLISAR_OR_WHATEVER_YOU_SEE",
      "delivery": ["SECOND_DELIVERY_LOCATION"],
      "reward_usc": "UNRESOLVED",
      "cargo_scu": "UNRESOLVED"
    }
  ]
}
```

Replace the `UNRESOLVED` values with numbers once you have read them from screen. Numbers go without quotes: `"reward_usc": 12500` not `"reward_usc": "12500"`.

---

## What to Fill In

| Field | What it is | Notes |
|-------|-----------|-------|
| `pickup` | Exact location name as shown | Check spelling — it must match for alias resolution |
| `delivery` | Delivery location(s) as a list | Even one location should be in a list: `["Baijini Point"]` |
| `reward_usc` | Total payout in aUEC | Enter as a number, no commas: `12500` |
| `cargo_scu` | Cargo size in SCU | Enter as a number |
| `fee_usc` | Fee shown on screen, if any | If not shown, use `0` if certain, `"UNRESOLVED"` if not sure |

---

## What to Set to UNRESOLVED

Use the string `"UNRESOLVED"` (quoted, in the JSON) when:
- The value is cut off or outside the visible area
- You cannot read the number clearly
- The field is not shown for this mission type
- You are not certain what you read

Do not guess. The -2 point penalty per UNRESOLVED field is bounded and predictable. A wrong number produces a confidently wrong result.

---

## Reading the Output

Key sections in the scored output:

**`same_pickup_stacking`** — missions that share a pickup location. These are your stacking opportunities. Three Port Olisar pickups = +32 stacking bonus.

**`suggested_combined_route`** — the highest-value combination. Often scores higher than any individual mission because the same-pickup bonus only activates at the combined level.

**`ranked_missions`** — individual scores. Accept >= 70, defer 45–69, reject < 45.

---

## Why This Is First-Class

Manual entry with the deterministic scorer is the most reliable workflow in the system:

- **Zero hallucination risk.** Every value came from your screen.
- **No API dependency.** Nothing fails because a provider is down.
- **Reproducible.** The same JSON file produces the same score every time.
- **Fast once familiar.** Typing five missions takes less than two minutes.

The pipeline treats manually-typed JSON and AI-extracted JSON identically. Manual entry simply removes the hallucination risk that AI extraction introduces.
