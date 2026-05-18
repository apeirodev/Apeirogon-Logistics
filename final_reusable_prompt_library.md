# Final Reusable Prompt Library

## Mission Screenshot Analysis Prompt
Analyze the attached Star Citizen hauling mission screenshots using the hauling intelligence dataset. Preserve unreadable values as unresolved. Do not invent mission details. Output accepted missions, rejected missions, SCU totals, route sequence, route risks, and confidence notes.

## Hull-B Covalex Optimization Prompt
Analyze this mission batch for Hull-B Covalex reputation grinding. Prioritize same-pickup stacking, overlapping destinations, orbital loops, low unloading friction, and dead-leg avoidance. Treat QT timing as runtime-derived.

## Generalized Hauling Prompt
Analyze this hauling mission batch for the specified ship, issuer, and hauling style. Use generalized hauling profiles, mission issuer profiles, and ship operational models. Preserve unknowns explicitly.

## Telemetry Ingestion Prompt
Ingest this hauling session telemetry. Separate observed telemetry from sourced facts and derived heuristics. Use telemetry only for observational refinement.

## Patch Validation Prompt
Validate whether this patch appears to change hauling behaviour. Compare observed telemetry against prior patch-era baselines and identify heuristic invalidation candidates.
