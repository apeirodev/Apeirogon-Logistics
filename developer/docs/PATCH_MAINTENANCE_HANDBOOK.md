# Patch Maintenance Handbook

How to update the scoring config and alias files after a Star Citizen patch.

---

## What Changes With Patches

Star Citizen patches change game values that the scoring system depends on. When a patch drops, the following may be affected:

- Mission reward ranges (Covalex, Ling, Red Wind payouts)
- Cargo capacity for ships
- Landing and docking fees
- Station availability (new stations added, existing ones modified)
- Mission terminal UI (affects OCR extraction and alias matching)
- Freight elevator behaviour
- New mission issuers or retirement of existing ones

The scoring tools do not hard-code any of these values. You supply actual values from your screen on each run. But the **heuristic weights** and **modifiers** in `scoring_config.json` may need adjustment if a patch substantially changes which route shapes are profitable.

---

## After a Patch: Immediate Steps

**1. Check your location aliases.**

Open `runtime/OCR_normalization_rules.json` and check whether any station names have changed. If a station was renamed or a new station was added, add the appropriate aliases to the `location_aliases` block.

**2. Check ship modifiers.**

If a ship received a cargo capacity change, the fragmentation and freight modifiers may need adjustment. Run a few scored routes with your ship and compare the recommendations to your actual experience. If the tool is consistently under- or over-rating routes of a particular type, adjust the relevant modifier.

**3. Check issuer availability.**

If an issuer was added, modified, or removed, update `issuer_modifiers` in `scoring_config.json`. For a new issuer with no data, start with an empty modifier block `{}` and calibrate over time.

**4. Update patch_version in your session state.**

When you start your first session on the new patch, update `patch_version` in your `session_state.json` and `user_profile.json`. This ensures your telemetry is tagged correctly.

---

## Calibrating After a Patch

Calibration is the process of adjusting scoring weights to match actual observed outcomes. It is manual and iterative.

**Process:**

1. Run several scored sessions on the new patch.
2. Record outcomes in your telemetry files — which routes were accepted, what the actual efficiency was, whether the recommendations were correct.
3. Compare scorer recommendations against your observed outcomes.
4. Identify systematic mismatches: routes that the scorer rates highly but perform poorly, or routes it scores low that actually work well.
5. Adjust the relevant weights in `scoring_config.json`. Make one change at a time and test with known routes.

**Tools to help:**

```bash
# See how sensitive your score is to each factor
echo '{"issuer":"covalex","ship":"hull-b","same_pickup":2,"dead_leg":1}' \
  | python tools/weight_sensitivity_analyzer.py
```

This shows which factors most affect your current route score at different weight levels, helping you identify which weight to adjust first.

---

## Not Every Patch Requires Changes

Minor patches that do not affect cargo, missions, or station availability may not require any config updates. The scoring heuristics are designed to be stable across patch types that do not fundamentally change hauling economics.

Only update weights when you observe systematic scoring inaccuracy on the new patch. Premature calibration without observed data degrades accuracy rather than improving it.

---

## Tracking Patch History

Save dated snapshots of your `scoring_config.json` alongside your session state files when you make calibration changes. This lets you compare scoring behaviour across patches and roll back if a change makes scoring worse.

Example:

```
hauling-state/patches/Alpha 3.23/scoring_config_3.23.json
hauling-state/patches/Alpha 3.24/scoring_config_3.24.json
```

---

## Reporting Calibration Data

If you have collected telemetry and calibration notes that would benefit other players, consider submitting a bundle with your session outcomes and a note about any scoring adjustments you made and why. See `docs/TELEMETRY_SUBMISSION_WORKFLOW.md`.
