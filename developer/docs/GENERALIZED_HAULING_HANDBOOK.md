# Generalized Hauling Handbook

> **CANONICAL FILE**: a player-adapted copy (with developer tuning sections removed) is at
> `player/uploads/GENERALIZED_HAULING_HANDBOOK.md`. If you update strategic content here,
> apply the same changes to the player copy.

How to use Apeirogon Logistics for hauling scenarios beyond the Hull-B Covalex primary workflow.

---

## Primary vs. Generalized Use

The primary workflow this toolset was built for is Hull-B Covalex orbital chains in Stanton. The scoring config defaults, ship modifiers, and documentation are calibrated for that use case.

The generalized workflow extends the same tools to:
- Other ships (Hull-C, Taurus, Caterpillar, Freelancer MAX)
- Other issuers (Ling, Red Wind, others)
- Mixed-issuer batches
- Non-Stanton systems (less tested, no system-specific location data)
- Atmosphere-heavy routes that are planned rather than avoided

---

## Applying the Tool to Other Ships

Pass your ship via the `"ship"` field in your mission JSON. The scorer applies that ship's modifier block from `scoring_config.json`.

For ships not in the supported list, omit the ship field — the scorer uses base weights with no ship modifier. This is not ideal for calibrated scoring, but it produces a usable result for route shape analysis.

See `docs/SHIP_SPECIALIZATION_GUIDE.md` for the full ship modifier table and per-ship guidance.

---

## Mixed-Issuer Batches

The batch tool handles missions from multiple issuers. Each mission in the batch picks up its own issuer modifier. The combined route score uses the issuer of the dominant mission set (the one with the most missions).

When mixing issuers in a batch:
- Same-pickup stacking still applies to missions from the same pickup regardless of issuer
- Issuer modifiers apply per-mission, not per-batch
- A Covalex mission and a Ling mission at the same pickup can still stack

---

## Atmosphere-Heavy Routes

The atmosphere penalty (-12) is calibrated for Hull-B where atmospheric flight when fully loaded is a practical problem. For ships with better atmospheric handling (Taurus, Cutlass, smaller ships), this penalty may be too aggressive.

To tune: reduce the `atmosphere` weight in `scoring_config.json` for your ship, or add a ship-specific modifier to dampen the atmosphere penalty. Example:

```json
"ship_modifiers": {
  "taurus": {
    "ship_suitability": 1.05,
    "fatigue": 0.95,
    "atmosphere": 0.80
  }
}
```

This tells the scorer that atmosphere deliveries cost the Taurus 80% of what they cost the baseline ship, reflecting better atmospheric handling.

---

## Issuer-Specific Planning

**Ling / Ling Family:** Destination overlap and same-pickup bonuses reward stacking. The same batch analysis strategy as Covalex applies — identify same-pickup groups and stack them. Smaller ships work well for Ling missions given their typical cargo sizes.

**Red Wind:** Dead leg and congestion penalties are amplified. Only accept Red Wind missions when you are already positioned near the pickup and the delivery is orbital and on your route. Isolated Red Wind missions in congested areas are consistently poor performers.

**Unknown issuers:** If you encounter an issuer not in the config, add a `{}` entry for it in `issuer_modifiers`. The mission will score on base weights, which is better than no score.

---

## Non-Stanton Systems

The location alias file (`runtime/OCR_normalization_rules.json`) currently covers Stanton locations. If you are hauling in Pyro or other systems:

1. Add any new location names to `location_aliases` when you encounter them.
2. The scorer will still work — it just treats unfamiliar locations as non-orbital (unknown type) rather than orbital. This slightly understates scores for orbital stations in other systems.
3. Classify stops manually: if you know a stop is orbital, add it to the `_ORBITAL_KEYWORDS` list in `calculate_traversal.py` or add a comment noting its type in your notes field.

---

## Telemetry-Driven Refinement

The scoring heuristics are starting points. For any specialisation (a specific ship, issuer, or system), collect telemetry from your real sessions and compare scorer recommendations against outcomes. Where there are systematic mismatches, adjust the relevant weights.

The generalized workflow depends more on user calibration than the primary Hull-B Covalex workflow, because the default weights were tuned for Hull-B Covalex. The further your use case departs from that baseline, the more value you get from recording outcomes and adjusting weights.

See `docs/PATCH_MAINTENANCE_HANDBOOK.md` for the calibration process.
