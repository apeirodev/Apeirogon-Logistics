# Ship Specialization Guide

This guide explains how ship modifiers affect scoring, which ships suit which mission types, and how to tune ship settings in your config.

---

## How Ship Modifiers Work

When you pass a ship to the scorer, it loads that ship's modifier block from `runtime/scoring_config.json` and applies multipliers to specific scoring factors before the final score is calculated.

A modifier greater than 1.0 amplifies a factor — meaning a bonus scores higher and a penalty scores worse. A modifier less than 1.0 dampens a factor.

For example: if `fragmentation` normally contributes -12 to your score and your ship has `fragmentation×1.10`, the effective contribution is -13.2. Ships that carry cargo in ways that make fragmented routes worse (harder loading, more stops, more exposure to partial deliveries) carry amplified penalties for those route shapes.

The modifiers stack on top of the base weights in `scoring_config.json`. They do not replace the weights — they scale them at calculation time.

---

## Supported Ships

| Ship | Modifier | Value | Practical Meaning |
|---|---|---|---|
| hull-b | freight | ×1.05 | Small bonus for high-freight-value runs |
| hull-b | fragmentation | ×1.10 | Fragmented routes hurt more — avoid multi-stop jumbled missions |
| hull-b | cargo_panel_clarity | ×1.15 | Score rewards clean, readable mission sets |
| hull-b | ship_suitability | ×1.05 | Slightly better baseline fit for missions flagged as Hull-B-appropriate |
| hull-c | freight | ×1.25 | Strong reward for high-value freight runs |
| hull-c | stop_density | ×1.20 | High stop counts are penalised hard — only take simple routes |
| hull-c | ship_suitability | ×1.15 | Best match score when mission size fits Hull-C capacity |
| taurus | ship_suitability | ×1.05 | Slightly better baseline fit |
| taurus | fatigue | ×0.95 | Long chains accumulate less fatigue penalty — suited to extended sessions |
| caterpillar | freight | ×1.10 | Moderate freight bonus, better than baseline |
| caterpillar | ship_suitability | ×1.10 | Good mission fit score |
| freelancer max | ship_suitability | ×1.02 | Near-neutral — minimal modification |
| freelancer max | fatigue | ×0.98 | Marginal fatigue dampening |

### Hull-B

Best use: Covalex orbital chains with a clean, consistent mission set. The Hull-B rewards cargo panel clarity and ship suitability, meaning your score improves when the mission list is readable and well-matched to the ship.

Avoid: Fragmented routes and atmosphere deliveries when fully loaded. The fragmentation multiplier amplifies what is already a -12 base penalty. Atmosphere as a first delivery when orbitals are available is a red line — see the Operational Doctrine Handbook.

### Hull-C

Best use: Simple, high-volume runs to a small number of destinations. The stop density multiplier at ×1.20 means every extra stop costs more than it would on any other ship. Accept only routes where you can do large volume to one or two destinations.

Avoid: Any mission set with more than two or three distinct delivery points. The stop density penalty will drag your score below the accept threshold even on otherwise good missions.

### Taurus

Best use: Long hauling sessions and chain routes. The fatigue dampener at ×0.95 means the Taurus resists the score degradation that builds up over multi-mission chains. It is the closest thing to an all-rounder in the supported set.

### Caterpillar

Best use: Freight-heavy runs where cargo value is high. The freight and ship suitability multipliers both amplify the upside of good missions. No unusual penalties.

### Freelancer Max

Best use: Getting started, mixed mission types, learning the scoring system. The modifiers are near-neutral, so the Freelancer Max behaves close to the unmodified base weights. What you see in the base scoring config is close to what you get.

---

## Passing Your Ship to the Scorer

**JSON input field:**

```json
{
  "ship": "hull-b",
  "missions": [...]
}
```

Valid values: `hull-b`, `hull-c`, `taurus`, `caterpillar`, `freelancer max`

If no ship is specified, the scorer runs with unmodified base weights.

---

## Tuning Ship Modifiers

All ship modifier blocks live in `runtime/scoring_config.json`. To change a modifier:

1. Open `runtime/scoring_config.json`.
2. Find the `ship_modifiers` block for your ship.
3. Edit the multiplier value.
4. Changes take effect immediately on the next scorer run — no restart needed.

If you fly a ship not in the list, you can add a new block following the same pattern. A ship with no modifiers defined scores the same as the base weights.

---

## A Note on Cargo Capacity

Cargo capacity numbers are patch-dependent. They change when CIG adjusts ship loadouts or SCU values. Do not rely on AI estimates of capacity for any ship — AI training data is always behind the current patch. Check the in-game ship panel for capacity before planning a load. The scorer does not hard-code capacity values for this reason.
