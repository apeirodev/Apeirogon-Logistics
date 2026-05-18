# Hull-B Covalex Route Playbook

> **PLAYER COPY** — adapted from `developer/hull_b_covalex_route_playbook.md` for the
> screenshot-paste workflow. The developer version includes additional sections covering
> the Python CLI tools, which are not needed here.

Practical guide for Hull-B Covalex hauling. Not theory — operational patterns
that score well and execute cleanly in practice.

---

## The Hull-B in One Paragraph

The Hull-B is MISC's mid-tier external spindle hauler. Its external cargo
configuration means you load at freight elevators, not internal bays. It handles
medium pads and is agile enough for orbital-loop Covalex routes. It does not do
well in atmosphere when loaded. Its sweet spot is station-to-station Covalex
chains in the same system — same pickup, multiple orbital deliveries.

Its cargo capacity is patch-dependent. **Always check your in-game loadout screen.
Do not trust AI estimates of Hull-B capacity — they are frequently wrong.**

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

## Mission Selection — What to Accept

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
- The mission is isolated — different pickup, no nearby deliveries

---

## Identifying Same-Pickup Stacks

At the mission terminal, before accepting anything:

1. Note the pickup location of every available Covalex mission
2. Group them by pickup — "Port Olisar × 3", "Microtech × 1", etc.
3. Accept all missions from your largest pickup group first
4. Only add missions from other pickups if they don't create dead legs

If you have three Port Olisar missions and one ARC-L1 mission, accept the
three Port Olisar missions and skip ARC-L1. Flying empty from Covalex Hub Shopp-L4
to ARC-L1 to pick up costs more in time and positioning than the ARC-L1 mission earns.

---

## Route Sequencing

Once you've accepted missions, order deliveries like this:

1. **Pick up all cargo** at the first pickup (all same-pickup missions)
2. **Orbital deliveries** (L-point stations, asteroid belts) — no atmospheric entry
3. **Moon deliveries** (if unavoidable) — low atmosphere, manageable
4. **Return positioning** — end near your next pickup cluster

**Never end a run far from the next opportunity.** If your next run is likely
from Port Olisar, end near Port Olisar. The "where does this route leave me?"
question matters as much as the route itself.

---

## Hull-B Cargo Panel Assignment

The Hull-B has eight external cargo panels: top, bottom, port, starboard, front, and back — six named faces, but the spindle structure effectively gives you eight addressable panels when you count the forward and aft halves of the port and starboard sides.

**Operational practice**: assign each destination its own panel or set of panels. When you know Panel A is "Baijini Point" and Panel B is "Shopp-L4", unloading at each stop is fast and clean — you are not sorting through mixed cargo to find what belongs there.

This is why the `cargo_panel_clarity` modifier exists for Hull-B (×1.15). A mission set where each destination maps neatly to a panel section scores better because it executes better. Fragmented routes — where you'd be pulling cargo from multiple panels at each stop — lose this advantage.

**Practical rule**: before loading, assign deliveries to panels mentally or in your notes. Prefer route sets where the number of destinations is ≤ the number of usable panels. When stacking three same-pickup Covalex missions to three different orbital stations, you get clean panel separation with cargo to spare.

---

## Handling the Freight Elevator

Hull-B specific: loading and unloading is via freight elevator, not ramp.
This matters for timing:

- At busy stations, elevator availability varies by server
- Partial loads are sometimes necessary (come back for second load)
- Unloading order can affect how long you're docked

Plan for freight elevator interaction time — actual elapsed time per stop
is higher than quantum travel time alone. Routes with 4+ stops feel longer
than they look on paper.

---

## How the Scoring System Treats Hull-B

When you tell your AI you are flying a Hull-B, these modifiers apply:

- `fragmentation` penalty is ×1.10 (fragmented routes hurt more)
- `freight` modifier is ×1.05 (freight complexity slightly more costly)
- `ship_suitability` is ×1.05 (Hull-B rewarded for well-suited routes)

In practice: **fragmented routes with many different delivery locations are
especially bad for Hull-B**. A single same-pickup run to two clean orbital
destinations scores much better than four runs to scattered locations.

---

## Screenshot Workflow

Fastest workflow for live play:

1. At the mission terminal, take a screenshot of your available contracts
2. Open your AI project (Claude, ChatGPT, Gemini, or whichever you set up)
3. Paste `player/session_start_prompt.md` — fill in ship: Hull-B and your location
4. Paste the screenshot
5. Your AI scores each contract and tells you what to accept and in what order

If the AI cannot read a value from your screenshot, it will ask you to type
that one value. This is correct — do not skip it. An unresolved fee or reward
can change the recommendation.

---

## Red Flags — Skip These Missions

| Pattern | Why |
|---------|-----|
| Pickup at planetary surface | Atmosphere entry loaded, very slow |
| Single mission, distant pickup | Dead leg, no stacking opportunity |
| 8+ stop chain | Chain collapse risk, hard to execute |
| Atmosphere delivery only | Hull-B handles atmosphere badly when loaded |
| Red Wind contracts in isolation | Higher dead-leg penalty, not worth it solo |

---

## Green Flags — Look for These

| Pattern | Why |
|---------|-----|
| 3× Port Olisar pickup | +32 stacking bonus, ideal |
| All deliveries at orbital stations | No atmosphere, fast runs |
| Covalex + Ling mix at same pickup | Both issuers have orbital deliveries |
| Deliveries cluster at 2–3 L-points | Clean route, low fragmentation |
| Route ends near next pickup | Good positioning for next run |

---

## Reputation vs Efficiency

Covalex reputation progression matters for contract availability and quality.
The scoring system doesn't directly model reputation, but the factors that
produce high scores (same-pickup stacking, low dead legs, orbital chains) are
also the patterns that build reputation efficiently — you're completing more
Covalex missions per hour than scattered routes would allow.

Prioritising reputation over one-off payout is usually correct in the medium term.
A route that pays slightly less but completes faster and positions you for the next
run is better than a high-payout isolated mission that leaves you out of position.
