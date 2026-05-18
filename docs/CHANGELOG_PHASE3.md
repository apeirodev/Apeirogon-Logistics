# Phase 3 Changelog

Generated: 2026-05-16

## Completed
- Added operational hauling penalty model.
- Added operational classifications.
- Added derived operational metrics.
- Added schema for hauling penalty records.
- Added derivation rules and known issues tracking.
- Added VERSION.json.

## Records
- Penalty records created: 75

## Operational Metrics Added
- hauling_efficiency_score
- dead_leg_risk
- stop_complexity
- cargo_turnaround_complexity
- atmospheric_burden
- expected_rep_efficiency

## Explicit Separation Maintained
- sourced facts
- derived heuristics
- unresolved values
- runtime-dependent values

## Unresolved Operational Uncertainties
- freight elevator latency
- patch-specific hauling bugs
- live congestion
- actual route density
- station implementation changes
- runtime ship-specific handling

## Next Phase
Phase 4 should build ship operational profiles and runtime traversal models.
