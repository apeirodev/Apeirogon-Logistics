# Public Contributor Guide

How to contribute to Apeirogon Logistics and what contributions are accepted.

---

## What This Project Accepts

Contributions that improve the tool's usefulness for Star Citizen haulers:

- **Verified hauling telemetry**: session outcome data from real runs with confirmed values
- **OCR correction examples**: known AI extraction errors with correct values, for improving alias coverage
- **Patch validation notes**: observations about what changed in a patch and how it affected scoring accuracy
- **Issuer behaviour observations**: patterns in mission availability, payout ranges, and route shapes for specific issuers
- **Ship operational observations**: real-world performance data for ships in the supported list
- **Location alias additions**: OCR variants and alternate spellings that need to be added to `OCR_normalization_rules.json`
- **Documentation improvements**: corrections, clarifications, additional examples
- **Bug reports**: specific tool failures with reproducible inputs

---

## Contribution Rules

These rules exist to keep the data quality high and the codebase trustworthy.

**Do not invent values.** Every numeric value in a telemetry submission or data contribution must come from an observed in-game screen. Do not estimate, extrapolate, or fill gaps from memory. Use UNRESOLVED for any field you cannot confirm.

**Mark unknowns as UNRESOLVED.** If you cannot read a value from your screenshot or did not record it at the time, the value is UNRESOLVED. Do not substitute a plausible number.

**Include patch version.** All telemetry and calibration data must include the patch version it was collected on. Data without a patch version cannot be used for calibration because values change across patches.

**Separate observed telemetry from interpretation.** Raw session data (what happened) and analysis of that data (what it means for scoring weights) are different things. Submit raw data as telemetry. Submit analysis as a separate note or discussion.

**Avoid personal or account-identifying information.** Screen names, RSI handles, and account details should not appear in submitted data. See `docs/TELEMETRY_PRIVACY_GUIDE.md`.

**Submit screenshots only when they support the specific claim.** Screenshots should be cropped to the relevant terminal or UI element and should not contain unrelated overlays or private information.

---

## Review Principles

Contributions are reviewed against these standards:

- **Sourced facts require a source.** A claim that a mission type pays X aUEC on patch Y needs a screenshot or session record backing it up, not memory or forum posts.
- **Telemetry requires patch tagging.** Untagged data cannot be placed in the patch timeline and will be rejected or held pending clarification.
- **Heuristic suggestions require clear classification.** Proposals to change scoring weights should be labelled as heuristic adjustment proposals and include the supporting data that prompted the suggestion.
- **Operational doctrine changes require discussion.** Changes to `docs/OPERATIONAL_DOCTRINE_HANDBOOK.md` affect every user's recommended practice. These require community discussion before merging, not just a pull request.

---

## How to Submit

**For code changes, alias additions, and documentation improvements:**
Open a pull request on the GitHub repository. Include a clear description of what changed and why.

**For telemetry bundles:**
See `docs/TELEMETRY_SUBMISSION_WORKFLOW.md` for how to package and submit session data.

**For bug reports:**
Open an issue on the GitHub repository. Include:
- The exact command you ran
- The input JSON you used (or a minimal reproduction)
- The output you received
- The output you expected
- Your Python version and operating system

---

## Scope

This project focuses on:
- Star Citizen hauling route scoring
- Hull-B and Covalex operations as the primary use case
- Deterministic, auditable scoring with no AI in the scoring loop
- Privacy-first, local-first tooling

Contributions outside this scope (other game types, cloud-based features, AI-driven scoring) are out of scope for the main project.
