# Operational Handoff Guide

## Start Here
For daily use, begin with:
- final_operational_playbook.md
- final_reusable_prompt_library.md
- lightweight_operational_package_manifest.json

## Core Workflow
1. Provide mission screenshots.
2. Extract missions with unresolved values preserved.
3. Group by pickup.
4. Group by destination overlap.
5. Select ship and issuer context.
6. Score route burden.
7. Recommend accept, reject, or defer.
8. Log telemetry after execution.
9. Recalibrate heuristics only from verified telemetry.

## Non-Negotiable Rules
- Do not invent mission details.
- Do not infer unreadable OCR.
- Do not overwrite sourced facts with telemetry.
- Treat route scoring as heuristic.
- Treat runtime values as runtime-dependent.
