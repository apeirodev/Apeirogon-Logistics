# Recommended GitHub Repository Structure

```text
star-citizen-hauling-intelligence/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── data/
├── analytics/
├── runtime/
├── schema/
├── docs/
├── exports/
├── manifests/
├── public/
├── examples/
├── prompts/
└── tools/
```

## Branch Strategy
- `main`: stable releases
- `develop`: integration branch
- `patch/<sc-version>`: patch validation work
- `telemetry/<topic>`: telemetry ingestion batches
- `docs/<topic>`: documentation updates

## Suggested Issue Labels
- `telemetry`
- `ocr`
- `patch-validation`
- `ship-profile`
- `issuer-profile`
- `schema`
- `documentation`
- `bug`
- `needs-source`
- `unresolved`
