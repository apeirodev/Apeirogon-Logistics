# Hull-B Covalex Route Playbook

> **CANONICAL FILE**: a player-adapted copy (with Python CLI sections replaced by the
> screenshot workflow) is at `player/uploads/hull_b_covalex_route_playbook.md`.
> If you update strategy or scoring content here, apply the same changes to the player copy.

Practical guide for Hull-B Covalex hauling. Not theory, but operational patterns
that score well and execute cleanly in practice.

---

## The Hull-B in One Paragraph

The Hull-B is MISC's mid-tier external spindle hauler. Its external cargo
configuration means you load at freight elevators, not internal bays. It handles
medium pads and is agile enough for orbital-loop Covalex routes. It does not do
well in atmosphere when loaded. Its sweet spot is station-to-station Covalex
chains in the same system, with the same pickup and multiple orbital deliveries.

Its cargo capacity is patch-dependent. **Always check your in-game loadout screen.
Do not trust AI estimates of Hull-B capacity; they are frequently wrong.**

---

## The Core Strategy

Maximise same-pickup stacking. Everything else is secondary.

The `same_pickup` factor is worth +16 per stacked mission. Three missions from
the same pickup location add +32 to your combined route score. That's the
difference between a 50-point (defer) individual mission and an 82-point
(accept) combined run.

**Look for Port Olisar clusters.** When three or more Covalex missions share
Port Olisar as their pickup, accept all of them and deliver in one run.

---

## Mission Selection: What to Accept

**Accept if:**
- Pickup matches your current location (no dead leg to get there)
- Two or more missions share the same pickup (stack them)
- Deliveries are in the same system, preferably same orbital band
- No atmosphere-heavy deliveries in the stack

**Accept with caution if:**
- Pickup requires one quantum jump to reach
- One delivery is slightly out of the orbital loop (adds a stop but worth it)
- Reward is high relative to complexity

**Reject or defer if:**
- Pickup requires flying to a different planet empty (dead leg)
- Delivery requires entering atmosphere loaded
- Route has 7 or more stops total
- The mission is isolated, with a different pickup and no nearby deliveries

---

## Identifying Same-Pickup Stacks

At the mission terminal, before accepting anything:

1. Note the pickup location of every available Covalex mission
2. Group them by pickup: "Port Olisar × 3", "Microtech × 1", etc.
3. Accept all missions from your largest pickup group first
4. Only add missions from other pickups if they don't create dead legs

If you have three Port Olisar missions and one ARC-L1 mission, accept the
three Port Olisar missions and skip ARC-L1. Flying empty from Covalex Hub Shopp-L4
to ARC-L1 to pick up costs more in time and positioning than the ARC-L1 mission earns.

---

## Route Sequencing

Once you've accepted missions, order deliveries like this:

1. **Pick up all cargo** at the first pickup (all same-pickup missions)
2. **Orbital deliveries** (L-point stations, asteroid belts): no atmospheric entry
3. **Moon deliveries** (if unavoidable): low atmosphere, manageable
4. **Return positioning**: end near your next pickup cluster

**Never end a run far from the next opportunity.** If your next run is likely
from Port Olisar, end near Port Olisar. The "where does this route leave me?"
question matters as much as the route itself.

---

## Hull-B Cargo Panel Assignment

The Hull-B has eight cargo panel quadrants. These are the only valid names:

- Left top front
- Left top back
- Left bottom front
- Left bottom back
- Right top front
- Right top back
- Right bottom front
- Right bottom back

Do not use any other names (not mid, not centre, not wide, not inner, not outer, not face). These eight names map directly to the CARGO PANEL TRACKING rules in the scoring instruction block, which require the AI to use this exact vocabulary.

**Operational practice**: assign each destination its own quadrant or set of quadrants before loading. When "Left top front" is always Baijini Point cargo and "Right top front" is always Shopp-L4 cargo, unloading at each stop is fast and clean -- you focus one quadrant, unload it, and leave. You are not sorting through mixed boxes to find what belongs at the stop.

This is why the `cargo_panel_clarity` modifier exists for Hull-B (x1.15). A mission set where each destination maps cleanly to its own quadrant scores better because it executes better. Fragmented routes where you pull cargo from multiple quadrants at each stop lose this advantage.

**Practical rule**: before loading, assign deliveries to quadrants and write it down or tell your AI. Prefer route sets where the number of destinations is no more than the number of usable quadrants. When stacking three same-pickup Covalex missions to three different orbital stations, you get clean quadrant separation with space to spare.

**Cargo ledger**: when loading across multiple accepted contracts, tell your AI the quadrant, commodity, SCU, and destination for each quadrant you load. The AI will track required vs planned vs observed and flag any mismatch. If the numbers do not match your contracts, stop before loading more.

---

## Handling the Freight Elevator

Hull-B specific: loading and unloading is via freight elevator, not ramp.
This matters for timing:

- At busy stations, elevator availability varies by server
- Partial loads are sometimes necessary (come back for second load)
- Unloading order can affect how long you're docked

Plan for freight elevator interaction time; actual elapsed time per stop
is higher than quantum travel time alone. Routes with 4+ stops feel longer
than they look on paper.

---

## What the Tool Tells You About Hull-B Routes

When you pass `"ship": "hull-b"` to the scorer, these modifiers apply:

- `fragmentation` penalty is ×1.10 (10% worse than default)
- `cargo_panel_clarity` is ×1.15 (panel clarity is more valuable)
- `freight` modifier is ×1.05 (freight complexity slightly more costly)
- `ship_suitability` is ×1.05 (Hull-B is rewarded for well-suited routes)

In practice: **fragmented routes with many different delivery locations are
especially bad for Hull-B**. A single same-pickup run to two clean orbital
destinations scores much better than four runs to scattered locations.

---

## Using the Batch Tool for Mission Selection

At the mission terminal, use `ingest_mission_batch.py` to rank your options:

```bash
echo '{
  "issuer": "covalex",
  "ship": "hull-b",
  "missions": [
    {"pickup": "Port Olisar", "delivery": ["Covalex Hub Shopp-L4"], "cargo_scu": 24, "reward_usc": 12500},
    {"pickup": "Port Olisar", "delivery": ["Baijini Point"], "cargo_scu": 16, "reward_usc": 9000},
    {"pickup": "Microtech", "delivery": ["ARC-L1"], "cargo_scu": 32, "reward_usc": 8000}
  ]
}' | python tools/ingest_mission_batch.py
```

Look at:
1. `same_pickup_stacking`: which missions can be stacked
2. `suggested_combined_route.score`: what the stack scores together
3. `ranked_missions`: which missions are worth it individually

Missions that score "defer" individually often score "accept" when combined.
This is the tool's primary use case for Hull-B.

---

## Reputation vs Efficiency

Covalex reputation progression matters for contract availability and quality.
The scoring system doesn't directly model reputation, but the factors that
produce high scores (same-pickup stacking, low dead legs, orbital chains) are
also the patterns that build reputation efficiently; you're completing more
Covalex missions per hour than scattered routes would allow.

Prioritising reputation over one-off payout is usually correct in the medium term.
A route that pays slightly less but completes faster and positions you for the next
run is better than a high-payout isolated mission that leaves you out of position.

---

## AI Vision Workflow for Hull-B

Fastest workflow for live play:

1. At mission terminal: take a screenshot
2. Paste `STRICT_AI_SESSION_PROMPT.md` into ChatGPT/Claude → "STRICT MODE ACTIVE"
3. Tell the AI: *"I am flying a Hull-B."*
4. Paste `AI_VISION_EXTRACTION_PROMPT.md` + attach screenshot
5. Save the AI's JSON
6. Run: `python tools/OCR_result_normalizer.py -i raw.json | python tools/ingest_mission_batch.py`
7. Check `suggested_combined_route` and `same_pickup_stacking`
8. Accept missions accordingly

Takes about 90 seconds once you have the workflow memorised.

**Critical**: verify the AI's SCU and reward numbers against your screen before
running. If anything is fabricated, the batch score will be wrong. See
`docs/HALLUCINATION_GUARDRAILS.md`.

---

## Red Flags: Skip These Missions

| Pattern | Why |
|---------|-----|
| Pickup at planetary surface | Atmosphere entry loaded, very slow |
| Single mission, distant pickup | Dead leg, no stacking opportunity |
| 8+ stop chain | Chain collapse risk, hard to execute |
| Atmosphere delivery only | Hull-B handles atmosphere badly when loaded |
| Red Wind contracts in isolation | Higher dead-leg penalty, not worth it solo |

---

## Green Flags: Look for These

| Pattern | Why |
|---------|-----|
| 3× Port Olisar pickup | +32 stacking bonus, ideal |
| All deliveries at orbital stations | No atmosphere, fast runs |
| Covalex + Ling mix at same pickup | Both issuers have orbital deliveries |
| Deliveries cluster at 2 to 3 L-points | Clean route, low fragmentation |
| Route ends near next pickup | Good positioning for next run |
