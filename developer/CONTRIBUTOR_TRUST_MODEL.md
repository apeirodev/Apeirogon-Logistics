# Contributor Trust Model

Trust tiers control how much weight a contributor's data carries in the scoring pipeline.

---

## Tiers

| Tier | Label | Who | What they can contribute |
|------|-------|-----|--------------------------|
| T0 | System | Tools, CI, deterministic pipeline | All outputs; no human required |
| T1 | Maintainer | Project maintainers with repo access | All data types; first reviewer on telemetry |
| T2 | Verified contributor | Repeat contributors with accepted telemetry | Telemetry bundles, alias corrections, calibration notes |
| T3 | Community | First-time or occasional contributors | Bug reports, documentation improvements, unverified telemetry |
| T4 | Unvetted external | Anonymous or unreviewed sources | Flagged for human review before any pipeline use |

The tier is stored in `governance_metadata.contributor_trust_tier` on every pipeline output. It determines how `provider_output_validator` handles numeric field sourcing checks and how submitted data is categorized in the calibration log.

---

## Promotion

Promotion from T4 → T3 → T2 happens by track record: accepted pull requests and validated telemetry submissions. There is no formal application process; maintainers assign tiers when merging contributions.

T1 is reserved for maintainers with write access to the repository. T0 is non-human (pipeline-only) and is never assigned to a person.

---

## Demotion

A contributor may be demoted if submitted data is found to contain invented values or violates the `UNRESOLVED` sentinel rule. Demoted contributors revert to T4 until trust is re-established through reviewed submissions.

---

## In the Pipeline

When `provider_output_validator` processes AI output, it checks `contributor_trust_tier`. Output from T3 or T4 sources receives additional hallucination-risk flagging on all numeric fields. T0 and T1 output skips the external-contributor checks but is still subject to schema validation and `advisory_only: true` enforcement.

System-generated outputs (tools, CI) always emit T0. Manually constructed JSON submitted by a user is T3 unless the user is a known T1 or T2 contributor.
