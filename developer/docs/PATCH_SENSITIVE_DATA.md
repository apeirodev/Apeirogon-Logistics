# Patch-Sensitive Data Reference

This file documents which data in the repository is most likely to change when a new Star Citizen patch releases, and the process for re-verifying it.

For scoring weight tuning after a patch (modifier adjustment, issuer calibration, session state updates), see `PATCH_MAINTENANCE_HANDBOOK.md`. This file focuses on specific data values that need re-verification.

**Current patch version: Alpha 4.8.0**

When told that a new patch is out, work through the sections below in order. Start with the highest-risk data (ship SCU values), then proceed through scoring and issuer data, and finish with the version update.

---

## Process When a New Patch Is Out

1. User tells you: "New patch: Alpha X.Y.Z"
2. Update `VERSION.json` → `star_citizen_patch_version`
3. Work through each section below — note which fields are UNRESOLVED (not yet verified in-game)
4. Search for and replace the old patch reference string across all files (grep for the old version number)
5. Update all six version files (see CLAUDE.md versioning rule)
6. Commit with a message indicating the patch version update

---

## Highest Risk: Verify First

### Ship SCU Capacities (`developer/data/ship_profiles.json`)

CIG periodically rebalances ship cargo capacities. Any patch that includes ship rebalancing should trigger re-verification of all SCU values.

| Ship | Current SCU | Risk | Notes |
|---|---|---|---|
| Hull-B | 512 | Medium | Stable for several patches but subject to Hull series rebalance |
| Hull-C | 4608 | Medium | Same — Hull series rebalance risk |
| Hull-D | 6912 | High | Not flyable — estimate only. **Verify on release** |
| Hull-E | null | High | Not flyable — post-rebalance SCU not yet published |
| Hermes | 288 | Low | Recently released (Alpha 4.6), unlikely to change immediately |
| Starlancer MAX | 224 | Low | Stable |
| Starlancer TAC | null | High | SCU unconfirmed — verify in-game |
| Freelancer MAX | 120 | Low | Stable |
| Starfarer | 291 | Low | Stable |
| Starfarer Gemini | 291 | Low | Stable |
| Constellation Taurus | 174 | Low | Stable |
| Caterpillar | 576 | Low | Stable |
| C2 Hercules | 696 | Low | Stable |
| M2 Hercules | 522 | Medium | Military variant — may be adjusted |
| A2 Hercules | 216 | Medium | Bomb-bay configuration may change |
| ARGO RAFT | 192 | Low | Stable |
| Valkyrie | 90 | Low | Stable |
| Asgard | 180 | Medium | Newer ship — may be adjusted |
| Ironclad | 2204 | High | New in Alpha 4.8 — early release values often change |
| Ironclad Assault | 1440 | High | New in Alpha 4.8 — early release values often change |
| Railen | 640 | Medium | Xi'an ship — may see adjustments |
| Banu Merchantman | 2880 | High | Not flyable — estimate. **Verify on release** |
| Galaxy | 576 | High | Not flyable — estimate. **Verify on release** |

### Ship Flyability (`developer/data/ship_profiles.json`)

Ships flagged `"flyable": false` may become flyable in a new patch. Check each:
- Hull-D — check if flyable
- Hull-E — check if flyable
- Banu Merchantman — check if flyable
- Galaxy — check if flyable

When a ship becomes flyable, change `"flyable": true`, update SCU if the pre-release estimate was wrong, update notes to remove "NOT YET FLYABLE", and update scoring modifiers (speculative → live-tested values).

---

## Medium Risk: Verify After Ships

### Covalex Reputation Ranks (`developer/analytics/mission_issuer_profiles.json`)

The contracts available at each rank and the mission structure may be adjusted by CIG. If Covalex contracts change significantly, verify:
- What contract sizes are available at each rank
- Whether Everus Harbor stacking behavior still applies
- Whether the recommended ships at each rank still match available contract sizes

### Scoring Weights (`developer/runtime/scoring_config.json`)

The base scoring weights are internal heuristics, not game data — they don't change with patches. However:
- Ship modifier values for newly-flyable ships should be updated from speculative to live-tested
- Issuer modifier values may need adjustment if new patch changes issuer route structures

### OCR Normalization (`developer/runtime/OCR_normalization_rules.json`)

New locations may be added in patches. Check:
- New stations, outposts, or Lagrange points added
- Existing location names changed
- New mission issuers introduced

---

## Lower Risk: Verify If Available

### Quantum Drive Profiles (`developer/data/quantum_drive_profiles.json`)

Quantum drives are rebalanced less frequently but it does happen. If a patch notes mention quantum drive changes, re-check.

### Issuer Placeholders

When new issuer reputation data becomes available (Hurston Dynamics, microTech, ArcCorp), add reputation ranks following the same structure as Covalex.

---

## What NOT to Change Based on Patch Notes Alone

- Scoring weights (`default_weights` in scoring_config.json) — these are tuned heuristics, not game values. Only change based on observed scoring drift in live sessions.
- Source attribution fields — don't update unless the actual source changes.
- Schema files — patch updates don't require schema changes.

---

## Files That Reference the Patch Version

The following files contain explicit patch version references and must be updated:

- `VERSION.json` → `star_citizen_patch_version`
- `developer/data/ship_profiles.json` → `source_refs[].note` text mentions "Alpha 4.8.0"
- `developer/docs/SHIP_SPECIALIZATION_GUIDE.md` → intro paragraph and per-ship notes
- `player/uploads/SHIP_SPECIALIZATION_GUIDE.md` → intro paragraph
- `player/uploads/ship_profiles.json` → `source_refs[].note`
- `developer/analytics/mission_issuer_profiles.json` → check for per-rank notes
- `developer/data/patch_lineage_registry.json` → add new patch entry
- This file (`PATCH_SENSITIVE_DATA.md`) → "Current patch version" header above

When updating, search the repo for the old patch string: `grep -r "Alpha 4.8.0" .`
