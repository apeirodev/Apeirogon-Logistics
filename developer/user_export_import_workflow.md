# User Export and Import Workflow

## Export at Session End
Ask the AI to output:
- updated portable_user_profile.json
- updated hauling_session_state.json
- any telemetry events
- unresolved fields

## Import at Session Start
Provide:
- current portable_user_profile.json
- latest hauling_session_state.json if continuing
- current patch version if known

## Storage Recommendation
Use a local folder structure:

```text
hauling-state/
├── user_profile.json
├── patches/
│   └── <patch-version>/
│       ├── sessions/
│       ├── telemetry/
│       └── OCR_corrections/
└── exports/
```
