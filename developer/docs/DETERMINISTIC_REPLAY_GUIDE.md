# Deterministic Replay Guide

How to replay a past route scoring and verify that the output is unchanged.

---

## The Replay Guarantee

The deterministic scorer produces the same output from the same input, every time, as long as `runtime/scoring_config.json` has not changed. This is the auditability foundation: any route recommendation can be reproduced months later using only the saved input JSON.

Every scorer output includes a `deterministic_hash`: a SHA-256 of the scored output. This hash is the fingerprint of the scoring decision.

---

## Basic Replay

```bash
# Save your original input
python tools/deterministic_scorer.py -i original_input.json -o original_output.json

# Later, replay it
python tools/deterministic_scorer.py -i original_input.json -o replay_output.json

# Compare hashes manually
python -c "
import json
with open('original_output.json') as f: orig = json.load(f)
with open('replay_output.json') as f: replay = json.load(f)
match = orig['deterministic_hash'] == replay['deterministic_hash']
print('MATCH' if match else 'MISMATCH', orig['deterministic_hash'])
"
```

If the hashes match, the scoring decision is unchanged.

---

## Full Route Analysis Replay

For full route analysis (score + chain analysis combined):

```bash
python tools/route_analysis_runner.py -i original_input.json -o replay_output.json
```

The output includes `replay_manifest.input_hash` and `replay_manifest.output_hash`. The `input_hash` lets you confirm the input was not modified between the original run and the replay.

---

## Why Hashes Might Not Match

| Cause | How to check |
|-------|-------------|
| Scoring config changed | `git log runtime/scoring_config.json` |
| Input file modified | Compare `replay_manifest.input_hash` to original |
| Tool algorithm changed | `git log tools/deterministic_scorer.py` |
| Ship or issuer modifier added | Check `scoring_config.json` modifier blocks |

A mismatch is not necessarily a problem. If you updated the scoring config after calibration, replays of old routes will produce new scores. This is expected. The `deterministic_hash` reflects the state of the config at replay time, not at original scoring time.

---

## Archiving for Reproducibility

To make a route decision permanently reproducible:

1. Save the input JSON: `input_2024-01-15.json`
2. Save the output JSON: `output_2024-01-15.json`
3. Save the scoring config at the time: `scoring_config_3.24.json`

With these three files, you can always recreate the original scoring environment and verify the hash.

---

## Replaying AI-Assisted Sessions

If the original session used AI extraction, the scorer only saw the normalised JSON output of the AI pipeline, not the raw AI response. To replay:

1. Retrieve `missions_norm.json` from the original session (the normaliser output).
2. Run it through the scorer: `python tools/deterministic_scorer.py -i missions_norm.json`
3. The scorer output is deterministic from the normalised input forward.

The AI extraction stage is not deterministic (AI responses vary). Replay auditability begins at the normalised JSON, not at the screenshot.
