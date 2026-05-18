# Ship Specialization Guide

_CANONICAL FILE — player copy is at `player/uploads/SHIP_SPECIALIZATION_GUIDE.md`. If you update this file, update the player copy too._

This guide explains how ship modifiers affect scoring, which ships suit which mission types, and how to tune ship settings in the config. All cargo capacity values are from community sources (Alpha 4.8.0) and should be verified in-game before mission planning.

---

## How Ship Modifiers Work

When you pass a ship to the scorer, it loads that ship's modifier block from `runtime/scoring_config.json` and applies multipliers to specific scoring factors before the final score is calculated.

A modifier greater than 1.0 amplifies a factor — meaning a bonus scores higher and a penalty scores worse. A modifier less than 1.0 dampens a factor.

For example: if `fragmentation` normally contributes -12 to your score and your ship has `fragmentation×1.10`, the effective contribution is -13.2. Ships that carry cargo in ways that make fragmented routes worse (harder loading, more stops, more exposure to partial deliveries) carry amplified penalties for those route shapes.

The modifiers stack on top of the base weights in `scoring_config.json`. They do not replace the weights — they scale them at calculation time.

---

## Quick Reference: All Supported Ships

Ships with 90+ SCU capacity. Values are community-sourced advisory — verify in-game.

| Ship | Manufacturer | SCU | Flyable | Best Use |
|---|---|---|---|---|
| RAFT | ARGO | 192 | Yes | Orbital station freight, Covalex Junior–Member |
| Freelancer MAX | MISC | 120 | Yes | Entry-level generalist, near-neutral modifiers |
| Constellation Taurus | RSI | 174 | Yes | Armed generalist, Covalex Rookie–Member |
| Starlancer MAX | MISC | 224 | Yes | Deep space generalist, Covalex Junior–Member |
| Asgard | Anvil | 180 | Yes | Vehicle carrier / secondary hauler, atmospheric |
| A2 Hercules | Crusader | 216 | Yes | Heavy bomber, incidental hauler only |
| Valkyrie | Anvil | 90 | Yes | Atmosphere-heavy routes, incidental hauler only |
| Hermes | RSI | 288 | Yes | Fast blockade runner, dead-leg recovery |
| Starfarer | MISC | 291 | Yes | Tanker, secondary hauler |
| Starfarer Gemini | MISC | 291 | Yes | Armed tanker, secondary hauler |
| Railen | Gatac | 640 | Yes | Xi'an freighter, Covalex Member–Experienced |
| Caterpillar | Drake | 576 | Yes | High-volume single-destination |
| C2 Hercules | Crusader | 696 | Yes | Best atmo lifter, Covalex Experienced |
| M2 Hercules | Crusader | 522 | Yes | Military transport, contested routes |
| Ironclad Assault | Drake | 1440 | Yes | Armored vehicle carrier |
| Hull-B | MISC | 512 | Yes | Covalex orbital chains, Member rank sweet spot |
| Starlancer TAC | MISC | TBC | Yes | Combat logistics hybrid, not recommended for hauling |
| Galaxy | RSI | 576 | No | Modular freighter (not yet flyable) |
| Ironclad | Drake | 2204 | Yes | Armored deep-space freight, single destination |
| Hull-C | MISC | 4608 | Yes | Bulk rate contracts, Covalex Senior+ |
| Merchantman | Banu | 2880 | No | Trading hub freighter (not yet flyable) |
| Hull-D | MISC | 6912 | No | Capital bulk logistics (not yet flyable) |
| Hull-E | MISC | TBC | No | Capital bulk logistics (not yet flyable) |

---

## Ship Modifier Table

All multipliers from `runtime/scoring_config.json`. A multiplier > 1.0 amplifies the factor; < 1.0 dampens it.

| Ship key | Factor | Multiplier | Effect |
|---|---|---|---|
| hull-b | freight | ×1.05 | Freight penalty slightly amplified |
| hull-b | fragmentation | ×1.10 | Fragmented routes hurt more |
| hull-b | cargo_panel_clarity | ×1.15 | Clean mission sets score higher |
| hull-b | ship_suitability | ×1.05 | Slightly better baseline fit |
| hull-c | freight | ×1.25 | Strong reward for high-value freight |
| hull-c | stop_density | ×1.20 | High stop counts penalised hard |
| hull-c | ship_suitability | ×1.15 | Best match for mission size |
| taurus | ship_suitability | ×1.05 | Better baseline fit |
| taurus | fatigue | ×0.95 | Long chains accumulate less fatigue |
| caterpillar | freight | ×1.10 | Moderate freight bonus |
| caterpillar | ship_suitability | ×1.10 | Good mission fit score |
| freelancer max | ship_suitability | ×1.02 | Near-neutral |
| freelancer max | fatigue | ×0.98 | Marginal fatigue dampening |
| starlancer max | ship_suitability | ×1.05 | Good fit for deep-space missions |
| starlancer max | fatigue | ×0.95 | Long routes accumulate less fatigue |
| starlancer max | freight | ×1.03 | Small freight bonus |
| starlancer tac | ship_suitability | ×0.88 | Poor fit for hauling — combat ship |
| raft | ship_suitability | ×1.05 | Good fit for station freight |
| raft | freight | ×1.05 | Small freight bonus |
| raft | dead_leg | ×0.95 | Dead-leg penalty slightly dampened |
| valkyrie | ship_suitability | ×0.90 | Poor primary hauler fit |
| valkyrie | atmosphere | ×0.85 | Atmosphere penalty significantly reduced |
| valkyrie | fatigue | ×0.92 | Fatigue slightly dampened |
| asgard | ship_suitability | ×0.95 | Sub-optimal for pure hauling |
| asgard | atmosphere | ×0.85 | Atmosphere penalty significantly reduced |
| asgard | fatigue | ×0.95 | Fatigue slightly dampened |
| asgard | freight | ×1.03 | Small freight bonus |
| a2 hercules | ship_suitability | ×0.85 | Poor fit — bomber, not hauler |
| a2 hercules | atmosphere | ×0.90 | Atmosphere penalty slightly reduced |
| a2 hercules | freight | ×1.05 | Small freight bonus |
| m2 hercules | ship_suitability | ×1.05 | Good fit for contested routes |
| m2 hercules | atmosphere | ×0.90 | Atmosphere penalty slightly reduced |
| m2 hercules | freight | ×1.10 | Good freight bonus |
| m2 hercules | fragmentation | ×1.08 | Fragmented routes hurt somewhat more |
| c2 hercules | ship_suitability | ×1.08 | Strong fit for atmospheric hauls |
| c2 hercules | atmosphere | ×0.88 | Atmosphere penalty reduced — best in class |
| c2 hercules | freight | ×1.10 | Good freight bonus |
| c2 hercules | fragmentation | ×1.08 | Fragmented routes hurt somewhat more |
| starfarer | ship_suitability | ×0.88 | Poor fit — primary role is fueling |
| starfarer | freight | ×1.05 | Small freight bonus |
| starfarer | stop_density | ×1.10 | Multiple stops penalised more |
| starfarer gemini | ship_suitability | ×0.85 | Poor fit — military fueling ship |
| starfarer gemini | freight | ×1.05 | Small freight bonus |
| starfarer gemini | stop_density | ×1.10 | Multiple stops penalised more |
| ironclad | ship_suitability | ×1.10 | Excellent fit for armored deep-space cargo |
| ironclad | freight | ×1.15 | Strong freight bonus |
| ironclad | stop_density | ×1.25 | Multiple stops hurt severely — fly single-stop only |
| ironclad | fragmentation | ×1.15 | Fragmented routes hurt badly |
| ironclad assault | ship_suitability | ×0.90 | Sub-optimal — vehicle carrier, not hauler |
| ironclad assault | freight | ×1.10 | Moderate freight bonus |
| ironclad assault | stop_density | ×1.20 | Multiple stops penalised hard |
| hermes | ship_suitability | ×1.05 | Good fit for fast medium routes |
| hermes | dead_leg | ×0.90 | Dead-leg penalty dampened — good recovery ship |
| hermes | fatigue | ×0.92 | Fatigue dampened — suited to long sessions |
| galaxy | ship_suitability | ×1.05 | Good fit (speculative — not flyable) |
| galaxy | stop_density | ×1.05 | Small stop density amplification |
| galaxy | freight | ×1.05 | Small freight bonus |
| railen | ship_suitability | ×1.05 | Good fit for medium-heavy routes |
| railen | freight | ×1.08 | Moderate freight bonus |
| railen | atmosphere | ×0.90 | Atmosphere penalty slightly reduced |
| hull-d | ship_suitability | ×1.15 | Excellent fit (speculative — not flyable) |
| hull-d | freight | ×1.40 | Very strong freight bonus |
| hull-d | stop_density | ×1.35 | Multiple stops hurt severely |
| hull-d | fragmentation | ×1.25 | Fragmented routes very costly |
| hull-e | ship_suitability | ×1.20 | Best fit score (speculative — not flyable) |
| hull-e | freight | ×1.60 | Strongest freight bonus in the fleet |
| hull-e | stop_density | ×1.50 | Multiple stops hurt extremely badly |
| hull-e | fragmentation | ×1.40 | Fragmented routes catastrophically costly |
| merchantman | ship_suitability | ×1.20 | Excellent fit (speculative — not flyable) |
| merchantman | freight | ×1.20 | Strong freight bonus |
| merchantman | destination_overlap | ×1.10 | Destination overlap bonus amplified |

---

## Per-Ship Notes

### Hull-B (512 SCU, MISC)

The Covalex orbital chain specialist. External spindle cargo rewards clean route stacking — each extra contract from the same pickup scores higher here than on any other ship. The `cargo_panel_clarity` bonus (×1.15) uniquely rewards having a readable, consistent mission set.

**Cargo panel assignment**: The Hull-B has eight external cargo panels (top, bottom, port, starboard, front, back — plus the forward/aft halves of the port and starboard sides). Assign each delivery destination its own panel or panel section before loading. When Panel A is "Baijini Point" and Panel B is "Shopp-L4", unloading is fast and clean. Fragmented routes that mix cargo from multiple destinations per panel lose this advantage entirely, which is why the fragmentation penalty hits harder here than on any other ship.

**Best for**: Covalex Member rank through Experienced. Same-pickup stacking at Everus Harbor. 10-mission runs, all orbital.

**Avoid**: Atmosphere deliveries when loaded. Fragmented multi-stop sets. The fragmentation multiplier (×1.10) amplifies an already heavy -12 base penalty.

**Covalex rank notes**: This is the sweet spot ship for Member rank. Hull-B becomes viable at Member (rank 4) and stays excellent through Experienced (rank 5).

---

### Hull-C (4608 SCU, MISC)

Required for Covalex Senior bulk rate contracts. Docking-only — cannot land while loaded. The stop density multiplier (×1.20) means every extra delivery stop costs significantly more than on any other ship. Only fly the Hull-C into routes with one or two delivery destinations and very large volumes per drop.

**Best for**: Covalex Senior and Master. Lagrange bulk rate hauls. Partial-submit strategies.

**Avoid**: Multi-stop missions. Any atmospheric destination. Routes with fragmented contract sets.

---

### Hermes (288 SCU, RSI)

Fast medium freighter / blockade runner (flyable since Alpha 4.6). The dead-leg multiplier (×0.90) makes it the best ship in the fleet for recovering from an empty fly-to. The fatigue dampener (×0.92) supports long sessions.

**Cargo layout — quadrant assignment**: The Hermes has two long internal side grids. Place one or two 2-SCU personal storage boxes as a physical divider midway along each side to create four quadrants — forward port, aft port, forward starboard, aft starboard. Assign one destination per quadrant before loading. This gives you the same destination-separated unloading benefit that Hull-B gets from its eight named panels.

**Best for**: Routes with some contested space, missions where you might need to recover dead legs. General Covalex Junior through Member work. Up to four well-separated destinations.

**Avoid**: Very large volume runs where 288 SCU limits how many missions you can stack.

---

### Starlancer MAX (224 SCU, MISC)

Reliable deep-space generalist. Dual-bay design lets you mix cargo types. The fatigue modifier (×0.95) accumulates less penalty over multi-leg chains.

**Best for**: Covalex Junior through Member. Mixed mission types. Long hauling sessions.

---

### RAFT (192 SCU, ARGO)

Station-to-station freight specialist with external pods. The dead-leg dampener (×0.95) provides a small recovery benefit. Good at Covalex Junior through Member.

**Best for**: Orbital station runs. Routes that stay in space. Mission sets that fit the pod configuration.

**Avoid**: Atmosphere deliveries — the RAFT has limited atmospheric capability.

---

### Constellation Taurus (174 SCU, RSI)

Armed medium freighter. No unusual penalties. Good dead-leg recovery (9/10) due to speed and flexibility. Near-standard scoring behavior.

**Best for**: Covalex Rookie through Member. Players who want cargo capability with self-defense options.

---

### Caterpillar (576 SCU, Drake)

Five modular cargo bays. The freight (×1.10) and ship_suitability (×1.10) bonuses make high-value single-destination runs score well. Large and unwieldy — avoid atmosphere.

**Best for**: High-volume single-destination Covalex Member and above. Stations only.

**Avoid**: Fragmented routes, atmospheric landings.

---

### C2 Hercules Starlifter (696 SCU, Crusader Industries)

The best atmospheric hauler in the fleet. The atmosphere modifier (×0.88) gives the strongest atmosphere penalty reduction of any ship. Front ramp access makes loading straightforward. The fragmentation modifier (×1.08) means multi-stop runs cost a bit more.

**Best for**: Covalex Experienced rank. Surface delivery missions. Mixed orbital/atmosphere routes where most ships would score poorly.

**Avoid**: Fragmented multi-stop sets where 1.08× fragmentation penalty stacks up.

---

### M2 Hercules Starlifter (522 SCU, Crusader Industries)

Military variant with armored hull and turrets. Similar scoring to C2 but lower SCU due to military equipment. Good when route security matters.

**Best for**: Covalex Experienced, especially in contested or high-risk zones.

---

### A2 Hercules Starlifter (216 SCU, Crusader Industries)

Heavy bomber. 216 SCU when not carrying ordnance. The ship_suitability modifier (×0.85) reflects that this is not a hauling ship. Use only if it's what you own and nothing better is available.

---

### Railen (640 SCU, Gatac Manufacture)

Xi'an-designed medium-heavy freighter. First alien cargo ship built for the human market. The atmosphere dampener (×0.90) and freight bonus (×1.08) make it a good all-rounder.

**Best for**: Covalex Member through Experienced. Good for routes with some atmosphere stops.

**Note**: Xi'an grav-lev cargo handling may interact differently with human freight elevators. Verify in Alpha 4.8.0.

---

### Ironclad (2204 SCU, Drake Interplanetary)

Armored cargo juggernaut. Flyable since Alpha 4.8.0. The stop_density multiplier (×1.25) and fragmentation multiplier (×1.15) mean this ship only makes sense on single-destination runs with large volumes. The freight bonus (×1.15) rewards high-value cargo.

**Best for**: Single-destination bulk cargo, dangerous space routes, high-value freight.

**Avoid**: Any route with more than one delivery destination — the stop density penalty is severe.

---

### Ironclad Assault (1440 SCU, Drake Interplanetary)

Vehicle carrier variant. Lower SCU and a poor ship_suitability (×0.90) score. Use only if combat capability is the primary need.

---

### Valkyrie (90 SCU, Anvil Aerospace)

Troop dropship at the 90 SCU threshold. The atmosphere modifier (×0.85) is strong — this is the second-best atmosphere ship after the C2. Use only for atmosphere-heavy routes when a dedicated hauler is unavailable.

---

### Asgard (180 SCU, Anvil Aerospace)

Evolved from Valkyrie — carries tall ground vehicles or 180 SCU. The atmosphere modifier (×0.85) matches the Valkyrie. Not a primary hauler but flexible for mixed operations.

---

### Starfarer / Starfarer Gemini (291 SCU, MISC)

Primary role is fuel collection. Cargo is secondary. The ship_suitability modifier (×0.88 / ×0.85) reflects poor hauling fit. The stop_density modifier (×1.10) makes multi-stop routes more costly. Only use for cargo when the primary role is fueling.

---

### Galaxy (576 SCU, RSI): NOT YET FLYABLE

Modular: cargo (512 SCU), med-bay, or refinery module plus 64 SCU base hangar. Scoring modifiers are speculative placeholders. Update after live testing when it releases (expected IAE late 2026).

---

### Banu Merchantman (2880 SCU, Banu): NOT YET FLYABLE

Most anticipated community hauling ship. Internal market bays allow player vendor stalls. The destination_overlap bonus (×1.10) reflects that it is optimised for multi-buyer trade routes. Scoring modifiers are speculative placeholders pending live release.

---

### Hull-D (6912 SCU, MISC): NOT YET FLYABLE

Capital bulk hauler. Scoring modifiers are speculative. The stop_density (×1.35) and fragmentation (×1.25) multipliers will make this even more single-destination-focused than the Hull-C. Designed for Covalex Master interstellar bulk contracts.

---

### Hull-E (TBC SCU, MISC): NOT YET FLYABLE

Largest ship in the Hull series. Scoring modifiers are speculative placeholders. Original CIG SCU figures described as unrealistic for physicalized cargo — post-rebalance figures not yet published. Extreme stop_density (×1.50) and fragmentation (×1.40) modifiers reflect that only point-to-point bulk delivery makes sense at this scale.

---

## Passing Your Ship to the Scorer

**JSON input field:**

```json
{
  "ship": "hull-b",
  "missions": [...]
}
```

Valid ship key values match the keys in `scoring_config.json` → `ship_modifiers`. Use lower-case, hyphen-separated. Examples: `hull-b`, `hull-c`, `c2 hercules`, `railen`, `ironclad`, `starlancer max`.

If no ship is specified, the scorer runs with unmodified base weights.

---

## Tuning Ship Modifiers

All ship modifier blocks live in `runtime/scoring_config.json`. To change a modifier:

1. Open `runtime/scoring_config.json`.
2. Find the `ship_modifiers` block for your ship.
3. Edit the multiplier value.
4. Changes take effect immediately on the next scorer run — no restart needed.

If you fly a ship not in the list, add a new block following the same pattern. A ship with no modifiers defined scores the same as the base weights.

Ships marked NOT YET FLYABLE have speculative modifiers. Update them after live testing — especially stop_density and fragmentation, which tend to be the biggest surprises on new ships with complex cargo layouts.

---

## A Note on Cargo Capacity

Cargo capacity numbers are patch-dependent. They change when CIG adjusts ship loadouts or SCU values. Do not rely on AI estimates of capacity for any ship — AI training data is always behind the current patch. Check the in-game ship panel for capacity before planning a load. All SCU values in this guide are from community sources as of Alpha 4.8.0 and should be verified before mission planning.
