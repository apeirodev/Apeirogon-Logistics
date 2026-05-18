# AI Telemetry Poisoning Threat Model

## Threat
Bad telemetry, malicious submissions, or hallucinated summaries contaminate calibration and route scoring.

## Mitigations
- telemetry trust tiers
- patch-era segmentation
- maintainer review for calibration promotion
- anomaly detection
- provenance retention
- no direct telemetry-to-heuristic mutation
