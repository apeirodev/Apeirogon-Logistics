# Contributor Data Standards

## Required Fields Where Possible
- Star Citizen patch version
- ship used
- mission issuer
- pickup location
- delivery locations
- cargo amount
- mission outcome
- observed timing
- confidence level

## Uncertainty Handling
Use:
- `unknown`
- `unresolved`
- `unverified`
- `requires_validation`

Do not substitute likely values.

## Patch Era
All operational telemetry should be tagged to a patch era. Telemetry without patch context should not be used for high-confidence calibration.
