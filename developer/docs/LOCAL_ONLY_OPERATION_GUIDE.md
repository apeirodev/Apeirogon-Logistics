# Local-Only Operation Guide

Everything in this toolset runs on your machine with no network connection required. This guide explains what is local, what is optional network, and how to run a full session without touching the internet.

---

## What Runs Offline

Everything in `tools/` runs locally with no network dependency:

| Tool | What It Does | Offline |
|------|-------------|---------|
| `deterministic_scorer.py` | Scores a single route | Yes |
| `ingest_mission_batch.py` | Scores a batch and finds stacking | Yes |
| `OCR_result_normalizer.py` | Normalises OCR/AI extraction output | Yes |
| `calculate_traversal.py` | Analyses stop sequence and risks | Yes |
| `weight_sensitivity_analyzer.py` | Shows score sensitivity to weight changes | Yes |
| `session_state_manager.py` | Validates and tracks session state | Yes |
| `user_profile_loader.py` | Loads and validates your user profile | Yes |
| `bundle_telemetry.py` | Packages telemetry for optional submission | Yes |

The config (`runtime/scoring_config.json`) is a local file. All outputs are written locally. Nothing in the scoring pipeline requires a connection.

---

## What Requires Network

Two things are optional and require network access if you choose to use them:

**AI provider for screenshot OCR.** If you want to paste screenshots into ChatGPT, Claude, or another cloud provider to extract mission data, you need a connection. This is optional; you can enter mission data manually instead. See `docs/MANUAL_COPY_PASTE_WORKFLOW.md`.

**Telemetry submission.** `bundle_telemetry.py` packages your session outcome data into a zip file. Nothing is sent automatically. If you choose to submit the bundle, that step contacts a remote endpoint. If you do not run the submission step, no data leaves your machine.

Neither of these is needed to use the scoring tools. Both are opt-in enhancements.

---

## Workflow Without AI or Network

1. Note your mission offers in-game (reward, pickup, delivery, issuer).
2. Write them into a JSON file following the format in `docs/DETERMINISTIC_MODE_GUIDE.md`.
3. Run `ingest_mission_batch.py` with your input file.
4. Read the score and recommendation.
5. Accept or override based on the score and your live conditions.
6. After your run, update your session data manually and run `session_state_manager.py` to persist it.

That is the full offline loop. No AI, no network, no external dependencies beyond Python itself.

---

## Privacy

No data leaves your machine unless you take a deliberate action to send it.

The scoring tools write output to local JSON files you specify. Session state is stored locally. Your mission data, route history, and scoring results are files on your disk that you control.

If you run `bundle_telemetry.py` and then choose to submit the bundle, that data is sent. The bundle contains session outcomes, not API keys, not personal identifiers beyond what you put in your mission data. You can inspect the bundle file before submitting.

If you never run the submission step, nothing is transmitted.

---

## API Keys

No API key is required to run the scoring pipeline. API keys are only needed if you choose to use a cloud AI provider for screenshot OCR.

If you do use an AI provider, supply the key via environment variable only:

```bash
export OPENAI_API_KEY=your-key-here
```

Do not put API keys in JSON input files, config files, or command-line arguments. Environment variables are the safe method. See `CLAUDE.md` (LOG-01) for the full rationale.

---

## Offline AI Option

If you want screenshot OCR without sending data to a cloud provider, local AI models via Ollama or LM Studio can provide vision OCR without cloud access. Model availability and names change with software updates, so check the current Ollama or LM Studio documentation for which models support image input.

The rest of the pipeline (normalizer → batch scorer) is unaffected by which OCR source you use. The only difference is whether the AI call goes to a cloud endpoint or a local one.

Using a local model means your screenshots never leave your machine and there is no per-call cost. The tradeoff is that local models may be slower or less accurate depending on your hardware.

---

## File Storage

All tool outputs are local JSON files. You choose the output path when you run each tool.

Suggested layout for a session:

```
output/
  sessions/
    YYYY-MM-DD/
      batch_scored.json
      session_state.json
exports/
  telemetry_bundle_<epoch>.zip   (only if you run bundle_telemetry)
```

The scoring tools will write to any path you specify within the allowed write roots (`output/`, `exports/`, `telemetry/`). Paths outside those directories are rejected by the path validation layer in the tools.

You own all the output files. Back them up, delete them, or share them as you see fit. There is no database, no remote storage, and no account system.
