# Deterministic Fallback Handbook

Fallback mode must work without OCR, without AI, without internet, and without telemetry.

## Required Inputs
- ship
- issuer
- pickup
- delivery stops
- SCU
- unresolved fields

## Scoring
Use rule-based scoring only:
- same-pickup bonus
- destination overlap
- dead-leg penalty
- atmosphere burden
- freight burden
- cargo fragmentation
