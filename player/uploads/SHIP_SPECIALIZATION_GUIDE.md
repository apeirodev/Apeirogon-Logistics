# Ship Specialization Guide

_PLAYER COPY — canonical version is at `developer/docs/SHIP_SPECIALIZATION_GUIDE.md`. This file is a player-adapted copy (developer tuning sections removed). Upload this file to your AI project._

This guide tells your AI which ships suit which missions and how ship modifiers affect scoring. All cargo capacity values are community-sourced (Alpha 4.8.0) — verify in-game before mission planning.

---

## How Ship Modifiers Work

When you tell your AI your ship, it uses that ship's modifier block to adjust scoring. A modifier greater than 1.0 amplifies a factor — a bonus scores higher and a penalty scores worse. A modifier less than 1.0 dampens a factor.

Example: if a fragmented route normally costs -12 points and your ship has `fragmentation×1.10`, the actual cost is -13.2. The Hull-B scores fragmented routes harsher than other ships because fragmented loads are operationally worse on that hull.

---

## Quick Reference — All Supported Ships

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

Multipliers from `scoring_config.json`. > 1.0 amplifies, < 1.0 dampens.

| Ship | Factor | Multiplier | What it means in plain terms |
|---|---|---|---|
| hull-b | freight | ×1.05 | Freight penalty slightly amplified |
| hull-b | fragmentation | ×1.10 | Fragmented routes (too many drop-off stops) hurt more |
| hull-b | cargo_panel_clarity | ×1.15 | Clean, readable mission sets score higher |
| hull-b | ship_suitability | ×1.05 | Better baseline fit for matched missions |
| hull-c | freight | ×1.25 | Strong reward for high-value freight runs |
| hull-c | stop_density | ×1.20 | Each extra delivery stop costs more than any other ship |
| hull-c | ship_suitability | ×1.15 | Best fit score when volume matches capacity |
| taurus | ship_suitability | ×1.05 | Good baseline fit |
| taurus | fatigue | ×0.95 | Long routes accumulate less fatigue penalty |
| caterpillar | freight | ×1.10 | Moderate freight bonus |
| caterpillar | ship_suitability | ×1.10 | Good mission fit score |
| freelancer max | ship_suitability | ×1.02 | Near-neutral |
| freelancer max | fatigue | ×0.98 | Marginal fatigue dampening |
| starlancer max | ship_suitability | ×1.05 | Good fit for deep-space missions |
| starlancer max | fatigue | ×0.95 | Long routes accumulate less fatigue |
| starlancer max | freight | ×1.03 | Small freight bonus |
| starlancer tac | ship_suitability | ×0.88 | Poor fit — combat ship, not a hauler |
| raft | ship_suitability | ×1.05 | Good fit for station freight |
| raft | freight | ×1.05 | Small freight bonus |
| raft | dead_leg | ×0.95 | Flying empty to pickup hurts slightly less |
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
| c2 hercules | atmosphere | ×0.88 | Atmosphere stops hurt least of any ship |
| c2 hercules | freight | ×1.10 | Good freight bonus |
| c2 hercules | fragmentation | ×1.08 | Fragmented routes hurt somewhat more |
| starfarer | ship_suitability | ×0.88 | Poor fit — primary role is fueling |
| starfarer | freight | ×1.05 | Small freight bonus |
| starfarer | stop_density | ×1.10 | Multiple delivery stops penalised more |
| starfarer gemini | ship_suitability | ×0.85 | Poor fit — military fueling ship |
| starfarer gemini | freight | ×1.05 | Small freight bonus |
| starfarer gemini | stop_density | ×1.10 | Multiple delivery stops penalised more |
| ironclad | ship_suitability | ×1.10 | Excellent fit for armored deep-space cargo |
| ironclad | freight | ×1.15 | Strong freight bonus |
| ironclad | stop_density | ×1.25 | Multiple stops hurt severely — only take single-destination runs |
| ironclad | fragmentation | ×1.15 | Fragmented routes hurt badly |
| ironclad assault | ship_suitability | ×0.90 | Sub-optimal — vehicle carrier, not hauler |
| ironclad assault | freight | ×1.10 | Moderate freight bonus |
| ironclad assault | stop_density | ×1.20 | Multiple stops penalised hard |
| hermes | ship_suitability | ×1.05 | Good fit for fast medium routes |
| hermes | dead_leg | ×0.90 | Flying empty to pickup hurts least of any ship |
| hermes | fatigue | ×0.92 | Fatigue dampened — suited to long sessions |
| galaxy | ship_suitability | ×1.05 | Good fit (speculative — not flyable yet) |
| galaxy | stop_density | ×1.05 | Small stop density amplification |
| galaxy | freight | ×1.05 | Small freight bonus |
| railen | ship_suitability | ×1.05 | Good fit for medium-heavy routes |
| railen | freight | ×1.08 | Moderate freight bonus |
| railen | atmosphere | ×0.90 | Atmosphere penalty slightly reduced |
| hull-d | ship_suitability | ×1.15 | Excellent fit (speculative — not flyable yet) |
| hull-d | freight | ×1.40 | Very strong freight bonus |
| hull-d | stop_density | ×1.35 | Multiple stops hurt severely |
| hull-d | fragmentation | ×1.25 | Fragmented routes very costly |
| hull-e | ship_suitability | ×1.20 | Best fit score (speculative — not flyable yet) |
| hull-e | freight | ×1.60 | Strongest freight bonus in the fleet |
| hull-e | stop_density | ×1.50 | Multiple stops extremely costly |
| hull-e | fragmentation | ×1.40 | Fragmented routes catastrophically costly |
| merchantman | ship_suitability | ×1.20 | Excellent fit (speculative — not flyable yet) |
| merchantman | freight | ×1.20 | Strong freight bonus |
| merchantman | destination_overlap | ×1.10 | Overlapping destinations score better |

---

## Per-Ship Notes

### Hull-B (512 SCU)

The Covalex orbital chain specialist. External spindle cargo rewards clean route stacking — each extra contract from the same pickup scores higher here than on any other ship. The `cargo_panel_clarity` bonus (×1.15) rewards having a readable, consistent mission set.

**Cargo panel assignment**: The Hull-B has eight external cargo panels (top, bottom, port, starboard, front, back — plus the forward/aft halves of the port and starboard sides). Assign each delivery destination its own panel or panel section before loading. When Panel A is "Baijini Point" and Panel B is "Shopp-L4", unloading is fast and clean. Fragmented routes that mix cargo from multiple destinations per panel lose this advantage entirely — this is why fragmentation hits harder on the Hull-B than any other ship.

**Best for**: Covalex Member rank through Experienced. Same-pickup stacking at Everus Harbor. All-orbital routes.

**Avoid**: Atmosphere deliveries when loaded. Fragmented multi-stop sets — the fragmentation multiplier makes them score worse than they would on any other ship.

**Covalex rank tip**: Hull-B is the sweet spot ship for Member rank (rank 4). Use it from Member through Experienced (rank 5).

---

### Hull-C (4608 SCU)

Required for Covalex Senior bulk rate contracts. Cannot land while loaded — station docking only. The stop density multiplier (×1.20) means every extra delivery destination costs more than on any other ship.

**Best for**: Covalex Senior and Master. Lagrange bulk rate hauls. Large volume to one or two destinations.

**Avoid**: Multi-stop missions. Atmospheric destinations. Anything fragmented.

---

### Hermes (288 SCU)

Fast medium freighter. The dead-leg modifier (×0.90) makes it the best ship in the fleet for routes where you might fly empty to the pickup. Long-session capable.

**Cargo layout — quadrant assignment**: The Hermes has two long internal side grids. Place one or two 2-SCU personal storage boxes as a physical divider midway along each side to create four quadrants — forward port, aft port, forward starboard, aft starboard. Assign one destination per quadrant before loading. This gives you clean, fast unloading at each stop without sorting through mixed cargo.

**Best for**: Routes with some contested space. Covalex Junior through Member. Sessions with likely dead-legs. Up to four well-separated destinations.

---

### Starlancer MAX (224 SCU)

Reliable deep-space generalist. Dual-bay design lets you mix cargo types. Long sessions accumulate less fatigue penalty.

**Best for**: Covalex Junior through Member. Mixed mission types. Extended sessions.

---

### RAFT (192 SCU)

Station-to-station freight specialist with external pods. Good fit for orbital routes. Slight dead-leg penalty reduction.

**Best for**: Covalex Junior through Member. Orbital station runs. Missions that stay in space.

**Avoid**: Atmosphere deliveries — limited atmospheric capability.

---

### Constellation Taurus (174 SCU)

Armed medium freighter. No unusual penalties. Good dead-leg recovery due to speed. Near-standard scoring behavior.

**Best for**: Covalex Rookie through Member. Players who want cargo plus self-defense.

---

### Caterpillar (576 SCU)

Five modular cargo bays. Good freight and suitability bonuses. Large and unwieldy in atmosphere.

**Best for**: High-volume single-destination runs. Covalex Member and above. Stations only.

**Avoid**: Fragmented routes, atmospheric landings.

---

### C2 Hercules Starlifter (696 SCU)

The best atmospheric hauler in the fleet. The atmosphere modifier (×0.88) gives the strongest atmosphere penalty reduction of any ship. The fragmentation modifier (×1.08) means multi-stop sets cost a bit more.

**Best for**: Covalex Experienced. Surface delivery missions. Mixed orbital/atmosphere routes.

---

### M2 Hercules Starlifter (522 SCU)

Military variant with armored hull and turrets. Similar scoring to C2 but less SCU. Use when route security matters.

**Best for**: Covalex Experienced, especially in contested or high-risk zones.

---

### A2 Hercules Starlifter (216 SCU)

Heavy bomber. Not a recommended hauler. Use only if it's what you have available.

---

### Railen (640 SCU)

Xi'an-designed freighter. Good all-rounder with moderate atmosphere benefit and freight bonus.

**Best for**: Covalex Member through Experienced. Routes with some atmosphere stops.

**Note**: Xi'an grav-lev cargo handling may interact differently with human freight elevators — verify behavior in Alpha 4.8.0.

---

### Ironclad (2204 SCU)

Armored cargo juggernaut (flyable since Alpha 4.8.0). Excellent for single-destination high-value cargo. The stop density (×1.25) and fragmentation (×1.15) modifiers make any multi-stop route score poorly.

**Best for**: Single-destination bulk cargo in dangerous space.

**Avoid**: Any route with more than one delivery destination — the stop density penalty is severe.

---

### Ironclad Assault (1440 SCU)

Vehicle carrier variant of the Ironclad. Use only if combat capability is the primary need.

---

### Valkyrie (90 SCU)

Troop dropship. At the 90 SCU threshold. Strong atmosphere modifier (×0.85). Use only for atmosphere-heavy routes when a dedicated hauler is unavailable.

---

### Asgard (180 SCU)

Evolved Valkyrie. Carries ground vehicles or 180 SCU. Strong atmosphere modifier (×0.85). Flexible for mixed operations but not a primary hauler.

---

### Starfarer / Starfarer Gemini (291 SCU)

Primary role is fuel collection. Use for cargo only when the primary role is fueling.

---

### Galaxy (576 SCU) — NOT YET FLYABLE

Modular: cargo (512 SCU), med-bay, or refinery. Scoring modifiers are speculative — update after live release.

---

### Banu Merchantman (2880 SCU) — NOT YET FLYABLE

Most anticipated community hauling ship. Internal market bays. Scoring modifiers are speculative — update after live release.

---

### Hull-D (6912 SCU) — NOT YET FLYABLE

Capital bulk hauler. Designed for Covalex Master interstellar bulk contracts. Scoring modifiers are speculative.

---

### Hull-E (TBC SCU) — NOT YET FLYABLE

Largest Hull series ship. SCU post-rebalance not yet published. Scoring modifiers are speculative.

---

## How to Tell Your AI Your Ship

At the start of every session, tell your AI your ship and current location:

> "I'm flying a Hull-B. I'm currently at Everus Harbor."

Your AI will use the correct ship modifiers for every contract it scores that session.
