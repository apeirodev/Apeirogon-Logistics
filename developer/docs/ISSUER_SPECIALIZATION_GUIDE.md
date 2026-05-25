# Issuer Specialization Guide

This guide explains how issuer modifiers affect scoring, which issuers favour which route shapes, and how to add new issuers as the game changes.

---

## How Issuer Modifiers Work

When the scorer sees an issuer field in your mission data, it loads that issuer's modifier block from `runtime/scoring_config.json` and applies multipliers to relevant scoring factors.

Issuer modifiers reflect the practical reality that different mission companies tend to produce different route shapes. Covalex missions cluster around orbital stations and reward chain efficiency. Ling missions often share pickups and destinations. Red Wind missions tend to appear in isolated or congested locations where dead legs are more likely.

The modifiers scale the base factor weights at calculation time. They do not change the accept/defer/reject thresholds (accept >= 70, defer 45 to 69, reject < 45).

If a mission has no issuer field or the issuer is not in the config, the scorer runs with unmodified base weights.

---

## Supported Issuers

| Issuer | Modifier | Value | Practical Meaning |
|---|---|---|---|
| covalex | issuer_alignment | ×1.10 | Strong bonus when mission type matches Covalex route profile |
| covalex | orbital_loop | ×1.05 | Orbital loop chains score better; Covalex rewards tight orbital work |
| covalex | route_continuity | ×1.05 | Bonus for missions that continue a clean route without dead legs |
| ling / ling family | destination_overlap | ×1.05 | Small bonus when destinations stack with other missions |
| ling / ling family | same_pickup | ×1.03 | Small bonus for same-pickup stacking |
| red wind | dead_leg | ×1.10 | Dead legs cost more with Red Wind missions; already -15 base, now worse |
| red wind | congestion | ×1.05 | Congested delivery points penalized more |

### Covalex

Covalex is the primary focus of this toolset. The issuer alignment, orbital loop, and route continuity multipliers all compound when you build a tight orbital chain, meaning Covalex missions score significantly better than their raw factor values when stacked correctly.

Best use: Build a mission set that stays in orbital space, chains pickups and deliveries without dead legs, and uses Hull-B if available. The combination of Hull-B ship modifiers and Covalex issuer modifiers is the highest-scoring configuration the tool supports.

### Ling / Ling Family

The destination overlap and same_pickup multipliers are small (×1.05 and ×1.03). Ling missions get a modest bonus for stacking but no strong route-shape incentive. They work well as fill missions when you already have a destination or pickup cluster; the small bonuses reward missions that fit your existing run rather than missions you'd build a run around.

Both `ling` and `ling family` map to the same modifier block in the config.

### Red Wind

The dead leg and congestion multipliers make Red Wind missions score lower in exactly the situations where they are most likely to appear. A -15 base dead leg penalty becomes effectively -16.5 with the ×1.10 multiplier.

Think carefully before accepting an isolated Red Wind mission. If you are already positioned near the pickup and the delivery is on your route, the modifier impact is low. If you are accepting it speculatively and will need to reposition, it will likely score below the accept threshold.

---

## Passing Issuer to the Scorer

**Per-mission field in JSON input:**

```json
{
  "issuer": "covalex",
  "ship": "hull-b",
  "missions": [
    {
      "pickup": "Port Olisar",
      "delivery": ["Covalex Hub Shopp-L4"],
      "cargo_scu": 24,
      "reward_usc": 12500
    }
  ]
}
```

**Valid issuer values:** `covalex`, `ling`, `ling family`, `red wind`

---

## Adding New Issuers

To add a new issuer to the config:

1. Open `runtime/scoring_config.json`.
2. Find the `issuer_modifiers` block.
3. Add a new entry with the issuer name as the key and a modifiers object as the value.

```json
"issuer_modifiers": {
  "new-issuer-name": {
    "dead_leg": 1.05,
    "orbital_loop": 1.03
  }
}
```

Any factor name that appears in the base weights block can be used as a modifier key. Changes take effect immediately.

If you are unsure what modifiers to assign to a new issuer, start with an empty block `{}`: the issuer will then score on base weights with no modification until you tune it.

---

## A Note on Payout Ranges

Issuer mission availability, payout ranges, and mission frequency all change with game patches. The modifiers in `scoring_config.json` reflect route-shape tendencies, not specific payout values. Never use AI-generated payout estimates for any issuer; those values are patch-dependent and will be wrong. Enter actual in-game values manually or via verified OCR.
