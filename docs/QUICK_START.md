# Quick Start

You have Python installed and the repo downloaded. This is the condensed
reference. For full explanations, see `docs/GETTING_STARTED.md`.

---

## Score a Single Route

```bash
echo '{"issuer":"covalex","ship":"hull-b","same_pickup":2,"stops":["Port Olisar","Covalex Hub Shopp-L4","Baijini Point"]}' \
  | python tools/deterministic_scorer.py
```

Output: `score`, `recommendation` (accept/defer/reject), `operational_risk`, `warnings`.

---

## Score a Batch of Missions

```bash
echo '{
  "issuer": "covalex",
  "ship": "hull-b",
  "missions": [
    {"pickup": "Port Olisar", "delivery": ["Covalex Hub Shopp-L4"], "cargo_scu": 24, "reward_usc": 12500},
    {"pickup": "Port Olisar", "delivery": ["Baijini Point"], "cargo_scu": 16, "reward_usc": 9000}
  ]
}' | python tools/ingest_mission_batch.py
```

Output: ranked missions + same-pickup stacking groups + suggested combined route.

---

## Use AI to Read a Screenshot

1. Paste `prompts/STRICT_AI_SESSION_PROMPT.md` into your AI → wait for "STRICT MODE ACTIVE"
2. Paste `prompts/AI_VISION_EXTRACTION_PROMPT.md` + attach screenshot
3. Save the AI's JSON as `missions.json`
4. Run the pipeline:

```bash
python tools/OCR_result_normalizer.py -i missions.json -o missions_norm.json
python tools/ingest_mission_batch.py -i missions_norm.json
```

---

## Score Thresholds

| Score | Recommendation |
|-------|---------------|
| 70–100 | **accept** |
| 45–69 | **defer** |
| 0–44 | **reject** |

---

## Key Score Factors

| Factor | Points | Triggered by |
|--------|--------|-------------|
| same_pickup | +16 | Multiple missions sharing a pickup |
| destination_overlap | +12 | Multiple missions sharing a delivery |
| orbital_loop | +12 | Station-to-station route continuity |
| ship_suitability | +10 | Ship suited to route type |
| dead_leg | -15 | Empty leg between delivery and pickup |
| chain_collapse | -14 | More than 6 stops in one chain |
| fragmentation | -12 | Many spread-out deliveries |
| atmosphere | -12 | Atmosphere-heavy deliveries |

---

## Useful Files

| File | Purpose |
|------|---------|
| `runtime/scoring_config.json` | Tune weights, thresholds, ship/issuer modifiers |
| `runtime/OCR_normalization_rules.json` | Add issuer aliases, location aliases |
| `prompts/STRICT_AI_SESSION_PROMPT.md` | Mandatory AI session guardrail |
| `prompts/AI_VISION_EXTRACTION_PROMPT.md` | AI screenshot extraction prompt |
| `prompts/QUICK_SESSION_GUARDRAIL.md` | Condensed guardrail for repeat use |
| `docs/HALLUCINATION_GUARDRAILS.md` | Why AI invents numbers and how to prevent it |
| `docs/FAQ.md` | Common questions |

---

## Save a Batch to File

```bash
python tools/ingest_mission_batch.py -i missions.json -o results.json
```

---

## Windows Note

Replace single quotes with double quotes and escape inner quotes, or use PowerShell:
```powershell
'{"issuer":"covalex","ship":"hull-b","same_pickup":2}' | python tools\deterministic_scorer.py
```

Or save your input to a `.json` file and use `-i`:
```
python tools\ingest_mission_batch.py -i my_missions.json
```
