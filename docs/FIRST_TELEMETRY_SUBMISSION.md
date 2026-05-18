# First Telemetry Submission

How to prepare and submit your first session telemetry bundle.

---

## What Telemetry Is

Telemetry is a record of what actually happened during a hauling session: which routes you accepted, what the actual efficiency was, and whether the scorer's recommendations matched your outcome. Telemetry is used to calibrate scoring weights over time.

Telemetry is voluntary. The tool works fully without it.

---

## Required Fields

Every telemetry submission must include:

- **`patch_version`** — the Star Citizen patch you were playing on (e.g. `"Alpha 3.24"`). Without this, the submission cannot be placed in the calibration timeline.
- **`ship`** — the ship you were flying (e.g. `"hull-b"`).
- **`issuer`** — the primary mission issuer for the session (e.g. `"covalex"`).
- **`session_id`** — a unique identifier for this session. Can be a date string or UUID.
- **`export_timestamp`** — when the session state was exported.

---

## Filling in Values

Only record values you actually read from the in-game terminal or HUD. For any field you cannot confirm:

- Set it to `"UNRESOLVED"` — do not estimate or fill from memory.
- Add the field name to `unresolved_fields` in the mission object.

This is not a mark against your submission. UNRESOLVED values are expected and handled correctly by the calibration pipeline. Invented values corrupt the calibration baseline.

---

## Preparing Your Bundle

1. Complete your session and update your `session_state.json` (see `docs/USER_EXPORT_IMPORT_WORKFLOW.md`).
2. Validate the session file:
   ```bash
   python tools/session_state_manager.py -i session_state.json
   ```
3. Bundle the session and any telemetry events:
   ```bash
   python tools/bundle_telemetry.py \
     --input-dir hauling-state/patches/Alpha\ 3.24/sessions/ \
     --output telemetry_bundle.zip
   ```
4. Review the bundle manifest before submitting. The bundler strips any keys matching `api_key`, `token`, `secret`, or `password` — verify the manifest confirms this.

---

## Submitting

See `docs/TELEMETRY_SUBMISSION_WORKFLOW.md` for submission instructions.

Before submitting, verify:

- No screen names, RSI handles, or account identifiers appear in the data
- Patch version is present on all session and telemetry records
- All unconfirmed values are `"UNRESOLVED"`, not estimated numbers

---

## What Happens After Submission

Submitted bundles are reviewed by a T1 maintainer before any values are used for calibration. You will receive a response on the GitHub submission issue indicating whether the data was accepted, held pending clarification, or rejected and why.

Accepted telemetry is credited to your contributor trust tier over time.
