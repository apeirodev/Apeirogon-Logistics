# Contributing

How to contribute to Apeirogon Logistics. For the full contribution rules and review standards, see `docs/PUBLIC_CONTRIBUTOR_GUIDE.md`.

---

## Quick Rules

- **Preserve UNRESOLVED.** Never substitute a number you cannot confirm from your screen. Use `"UNRESOLVED"` for any field you did not read directly.
- **Include patch version.** All telemetry and calibration data must include the Star Citizen patch version it was collected on.
- **Separate data from interpretation.** Submit raw session data as telemetry. Submit analysis as a separate note or discussion.
- **No personal identifiers.** See `docs/TELEMETRY_PRIVACY_GUIDE.md`.

---

## What to Contribute

- Verified hauling telemetry (session outcomes from real runs)
- OCR correction examples (known AI extraction errors with correct values)
- Patch validation observations (what changed and how it affected scoring)
- Location alias additions (`runtime/OCR_normalization_rules.json`)
- Bug reports with minimal reproductions
- Documentation corrections and clarifications

Out of scope: other game types, cloud-based features, AI-driven scoring, real-money calculations.

---

## How to Submit

**Code changes, alias additions, documentation:**
Open a pull request. Use the pull request template. Include a clear description of what changed and why.

**Telemetry bundles:**
See `docs/TELEMETRY_SUBMISSION_WORKFLOW.md` for packaging and submission instructions.

**Bug reports:**
Open an issue using the `route_analysis_bug` template. Include the exact command, the input JSON, the actual output, and the expected output.

---

## Review Standards

All contributions are reviewed against the standards in `docs/PUBLIC_CONTRIBUTOR_GUIDE.md`. Numeric values require a source. Patch version is required on telemetry. Heuristic change proposals must be labelled as such and include supporting data.

See `CONTRIBUTOR_TRUST_MODEL.md` for how trust tiers affect what contributions can be accepted without additional review.
