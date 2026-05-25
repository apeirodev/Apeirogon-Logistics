# Deterministic Mode Guide

This guide covers running the scoring pipeline with no AI involvement: pure Python scoring from data you supply directly.

---

## What Deterministic Mode Is

Deterministic mode means the tool scores your missions using only the weights and modifiers in `runtime/scoring_config.json` and the data you provide in your input. No AI provider is contacted. No network connection is needed. No screenshots are processed.

You type in your mission data (or paste it from a previous OCR run), the tool runs the scoring logic, and you get a score, a recommendation, and a breakdown of which factors contributed. Every run with the same input and the same config produces the same output. That is what deterministic means here.

The accept/defer/reject thresholds are: accept >= 70, defer 45 to 69, reject < 45.

---

## When to Use It

Use deterministic mode when:
- You have no internet connection.
- You prefer not to send data to an AI provider.
- You are in active gameplay and typing fast; manual entry is faster than the OCR pipeline when you already know the values.
- You want to re-score a previous mission set with different config weights.
- You are testing config changes and want immediate feedback without waiting for AI processing.

Deterministic mode is the default way to use this tool in live play. The AI-assisted path is an optional enhancement for when you have screenshots and want to avoid transcription.

---

## The Two Entry Points

### Single Route: deterministic_scorer.py

Use this for scoring one mission or one route in a single call.

```bash
echo '{"issuer":"covalex","ship":"hull-b","same_pickup":2,"stops":["Hur-L2","Covalex Hub Shopp-L4","Baijini Point"]}' \
  | python tools/deterministic_scorer.py
```

Output: `score`, `recommendation` (accept/defer/reject), `operational_risk`, `warnings`, `score_breakdown`.

### Batch of Missions: ingest_mission_batch.py

Use this when you are choosing from multiple missions at the terminal.

```bash
python tools/ingest_mission_batch.py -i my_missions.json
```

The batch tool:
- Scores each mission individually.
- Detects same-pickup stacking opportunities.
- Builds an optimal combined route from the accepted and deferred missions.

Combined routes often score higher than individual missions because the same-pickup stacking bonus (+16 per stacked mission) only activates when missions are combined. This is the primary reason to use the batch tool.

---

## How to Enter Mission Data

The minimal input for a batch:

```json
{
  "issuer": "covalex",
  "ship": "hull-b",
  "missions": [
    {
      "pickup": "Hur-L2",
      "delivery": ["Covalex Hub Shopp-L4"],
      "cargo_scu": 24,
      "reward_usc": 12500
    },
    {
      "pickup": "Hur-L2",
      "delivery": ["Baijini Point"],
      "cargo_scu": 16,
      "reward_usc": 9000
    }
  ]
}
```

### Required fields (per mission)

| Field | Description |
|-------|-------------|
| `pickup` | Pickup location name |
| `delivery` | Delivery location(s) as a list |

### Optional but recommended

| Field | Description | If omitted |
|-------|-------------|------------|
| `reward_usc` | Mission reward in aUEC | UNRESOLVED: -2 score penalty |
| `cargo_scu` | Cargo size | Not used in current scoring |
| `issuer` | Mission company | No issuer modifier applied |
| `ship` | Ship name | No ship modifier applied |

Use `"UNRESOLVED"` as a value when you cannot read a field from screen. The tool handles it gracefully and flags it as a confidence issue.

---

## What Happens to Unresolved Fields

Each UNRESOLVED field:
- Applies a -2 point penalty to the score.
- Penalties are capped at -12 total (6 or more UNRESOLVED fields all trigger the same maximum).
- Drops the confidence rating to `medium`.

A result with unresolved fields is still returned; the tool does not refuse to score. But the recommendation is less reliable. Verify any UNRESOLVED field before acting on the score.

To fix an UNRESOLVED field: add the correct value to your JSON and re-run. The scorer is fast enough that re-running with corrected data is always the right approach.

---

## Tuning Weights

All scoring factor weights are in `runtime/scoring_config.json`. The main factors:

| Factor | Base Weight |
|--------|-------------|
| same_pickup | +16 |
| destination_overlap | +12 |
| orbital_loop | +12 |
| ship_suitability | +10 |
| dead_leg | -15 |
| chain_collapse | -14 |
| fragmentation | -12 |
| atmosphere | -12 |

Base score before factor adjustments: 50.

To change a weight, edit the value in `scoring_config.json` and re-run. Changes take effect immediately. Use `tools/weight_sensitivity_analyzer.py` to see how much a given factor is affecting your current route before adjusting.

---

## Comparison to AI-Assisted Mode

| | Deterministic (manual entry) | AI-Assisted (screenshot OCR) |
|---|---|---|
| Network required | No | Yes (unless local AI) |
| Speed | Fast | Slower (AI round-trip) |
| Data entry | Manual JSON | Screenshot + AI extraction |
| Best when | You know the values | You have screenshots and want to skip typing |
| Hallucination risk | None | Present; see HALLUCINATION_GUARDRAILS.md |
| Reliability | High | Depends on OCR quality and strict prompt compliance |

Both modes use the same scorer. The difference is only in how input data arrives. Use whichever fits your current session.
