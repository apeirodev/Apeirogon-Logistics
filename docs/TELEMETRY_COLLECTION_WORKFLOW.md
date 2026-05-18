# Telemetry Collection Workflow

How to record session outcomes in a format that is useful for future calibration.

---

## What Telemetry Is For

Telemetry records what actually happened on a run — not what the scorer predicted, but what occurred in practice. Over time, telemetry from real sessions can be used to validate and calibrate the scoring heuristics.

Telemetry contribution is opt-in. Nothing is recorded or sent automatically. You decide what to record and whether to share it.

---

## What to Record

Record these during and after each run:

**Before accepting missions:**
- Screenshot of the mission terminal (keep locally)
- List of missions offered, including those you rejected
- Patch version

**After accepting:**
- Which missions you accepted
- Whether you followed the scorer's recommendation or overrode it
- Your starting location

**During the run:**
- Freight elevator wait time at each stop (Hull-B specific)
- Any stops you had to skip or reroute around
- Server issues that affected the run (lag, broken elevators, quantum interdictions)

**At completion:**
- Actual route sequence (which order you delivered)
- Total time from pickup to last delivery
- Whether each mission was completed successfully
- Profit after fees (actual vs. what you expected)
- Any UNRESOLVED fields you resolved during the run

---

## Format

Telemetry records are JSON files. There is no fixed schema, but the telemetry ingestion pipeline (`tools/telemetry_ingestion_pipeline.py`) validates and normalizes them before storage.

Minimum useful fields:

```json
{
  "patch_version": "Alpha 3.23",
  "ship": "hull-b",
  "issuer": "covalex",
  "session_start_epoch": 1700000000,
  "completed_missions": [
    {
      "pickup": "Port Olisar",
      "delivery": "Covalex Hub Shopp-L4",
      "reward_usc": 12500,
      "actual_delivery_time_minutes": 8,
      "ocr_verified": true
    }
  ],
  "dead_legs": 0,
  "elevator_waits_total_minutes": 4,
  "followed_scorer_recommendation": true,
  "notes": "Clean run, server stable"
}
```

All numeric fields should come from your actual in-game observations, not from estimates or the scorer's output.

---

## OCR Verification Field

The `ocr_verified` flag on each mission indicates whether you visually confirmed the OCR/AI extraction values against your screen during the session. Set it to:
- `true` — you checked the value against your screen
- `false` — you did not verify (values came from OCR only)
- omit — same as false

Records with `ocr_verified: true` are more useful for calibration because the input values are confirmed to be accurate.

---

## Where to Save Telemetry Files

Save telemetry files in the `telemetry/` directory. The bundle tool (`tools/bundle_telemetry.py`) scans this directory when packaging for submission.

Suggested naming: `telemetry/YYYY-MM-DD_session.json`

---

## Validating Before Bundling

Before bundling for submission, validate your telemetry file:

```bash
python tools/telemetry_ingestion_pipeline.py -i telemetry/my_session.json
```

The validator checks for required fields, plausible numeric ranges, and missing patch version. Fix any errors before bundling.

---

## Bundling for Submission

Once you have collected telemetry you want to share:

```bash
python tools/bundle_telemetry.py --input-dir telemetry/ --output exports/my_bundle.zip
```

Review the bundle before submitting. The bundle tool will redact any field with `api_key`, `token`, or similar sensitive names, but check the contents yourself before sharing.

Submission is always voluntary and opt-in.
