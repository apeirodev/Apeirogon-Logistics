# Governance

How decisions are made in this project and how contributor data is governed.

---

## Maintainers

The project is maintained by ApeiroDev. Maintainers have write access to the repository and are the final arbiters of:

- Changes to `runtime/scoring_config.json` (weight changes affect all users)
- Changes to `docs/OPERATIONAL_DOCTRINE_HANDBOOK.md` (doctrine affects recommended practice)
- Changes to schema files (schema changes affect backward compatibility)
- Release tagging and checksum signing

---

## Decision Process

**Algorithmic changes** (weight adjustments, new scoring factors): require supporting telemetry data and a clear description of the systematic mismatch being corrected. Changes are made one weight at a time.

**Documentation changes**: open a pull request. No discussion required for corrections and clarifications. Doctrine changes require discussion first.

**New features**: open an issue describing the use case. Features that add AI dependency or cloud dependency are out of scope.

**Bug fixes**: open a pull request with a minimal reproduction and the corrected behaviour.

---

## Telemetry Governance

Telemetry submitted to this project is governed by `docs/TELEMETRY_PRIVACY_GUIDE.md`. Key principles:

- No personal identifiers in submitted data
- All submitted values must come from observed in-game screens
- Patch version is required on all telemetry; untagged data is held pending clarification
- Submitted telemetry is reviewed before use in calibration

---

## Data Ownership

Session state files and user profiles are owned by the user. The project tools process them locally; nothing is transmitted unless the user explicitly packages and submits a telemetry bundle.

---

## Conflict Resolution

Disputes about scoring weights, operational doctrine, or project direction are discussed in GitHub Issues. Maintainers make the final decision after community input. This is a small project — there is no formal voting process.
