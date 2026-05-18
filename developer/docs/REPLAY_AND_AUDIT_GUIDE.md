# Replay and Audit Guide

How to replay a past route analysis and verify that the scorer produces the same output from the same input.

---

## Why Replay Matters

The deterministic scorer always produces the same output from the same input; this is the core auditability guarantee. Replay lets you:

- Verify that a scoring config change did or did not affect a past decision
- Confirm that a route recommendation you acted on matches the current tool version
- Audit AI-assisted sessions by re-running the normalised input through the scorer

---

## Running a Replay

Every scorer output includes a `replay_manifest` with `input_hash` and `output_hash`. To replay:

```bash
# Score the same input again
python tools/deterministic_scorer.py -i saved_input.json -o replay_output.json

# Compare the output hash
python tools/verify_replay_integrity.py \
  --original saved_output.json \
  --replay replay_output.json
```

If the `deterministic_hash` in both outputs matches, the replay is verified. If they differ, either the input changed or the scoring config changed between runs.

---

## What Causes Hash Mismatches

A replay hash mismatch means the scorer produced a different result. Causes:

- **Scoring config changed**: weights in `runtime/scoring_config.json` were modified between the original run and the replay. Check `git log runtime/scoring_config.json`.
- **Input changed**: the input file was edited between runs. The `input_hash` in the `replay_manifest` lets you confirm the input used at original scoring time.
- **Tool version changed**: a bug fix or algorithm change altered scoring logic. Check the git log for `tools/deterministic_scorer.py`.

---

## Auditing AI-Assisted Sessions

If you used an AI provider for OCR extraction, the AI's output went through `OCR_result_normalizer.py` before scoring. To audit:

1. Recover the normalised JSON from your session output directory.
2. Run it through the scorer: `python tools/deterministic_scorer.py -i normalised.json`
3. Compare the `deterministic_hash` to the original session's scoring output.

If you want to audit the AI's extraction itself, compare the raw AI output to what was on your screen. The scorer is deterministic; hallucination risk is in the extraction stage, not the scoring stage.

---

## Batch Replay

The `route_analysis_runner.py` tool outputs a `replay_manifest` with both `input_hash` and `output_hash` for the combined score-and-chain-analysis output:

```bash
python tools/route_analysis_runner.py -i saved_input.json -o replay_output.json
```

The `replay_manifest.tool` field identifies which tool produced the original, so you know which tool to use for replay.

---

## Archiving for Audit

To preserve a scoring decision for later audit:

1. Save the input JSON alongside the output JSON with a date-stamped filename.
2. Record the `deterministic_hash` from the output in your session notes.
3. Note the current `runtime/scoring_config.json` SHA-256 (visible in `git log`).

This gives you everything needed to reproduce and verify the decision on any future date.
