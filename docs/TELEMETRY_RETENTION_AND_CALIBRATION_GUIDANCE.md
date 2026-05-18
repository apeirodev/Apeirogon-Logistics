# Telemetry Retention and Calibration Guidance

## Retention Periods
- Same patch telemetry: active calibration set.
- Previous patch telemetry: historical comparison only unless mechanics are unchanged.
- Pre-refactor telemetry: archive only, do not use for active route scoring.
- Unverified OCR telemetry: low-confidence cohort.
- User-verified telemetry: preferred calibration cohort.

## Minimum Samples
- Preliminary calibration: 10-20 sessions.
- Moderate confidence: 25-50 sessions.
- High confidence: 75+ sessions.
- Freight elevator calibration: 100+ unloading events.
- Dead-leg calibration: 100+ route chains.

## Decay Rules
- Decay confidence after every major patch.
- Decay confidence after major UI changes.
- Decay confidence after cargo mechanic changes.
- Do not delete old telemetry; archive by patch era.
