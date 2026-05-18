# Operational Doctrine Handbook

These are execution rules for live hauling. They exist because common mistakes cost real in-game time and burn contracts. Read this before your first serious run.

---

## Cargo Panel Management

Before you undock, open your cargo panel and read it. Every delivery destination should be visible. Group your understanding of the cargo by destination before you move.

Practical rules:
- Know how many distinct delivery points you have before you leave the pad.
- If you cannot read the panel clearly (OCR noise, overlapping items, UI glitch), flag the mission set as uncertain and re-run the normaliser with corrected data before committing.
- If any mission shows UNRESOLVED in the tool output, do not leave dock until you have verified it manually. See the UNRESOLVED section below.
- Check that your physical cargo matches what the panel says. Discrepancies before departure are recoverable. Discrepancies mid-route waste time.

---

## Delivery Ordering

The order in which you make deliveries affects your route efficiency and your score for future batches. The doctrine is:

1. Same-pickup missions first, before repositioning.
2. Orbital deliveries before atmosphere deliveries.
3. Nearest orbital cluster before distant ones.
4. Atmosphere deliveries last, as a dedicated segment of the run.

This ordering minimises dead legs and keeps your route shape clean for chain scoring. It also protects you from the atmosphere penalty (-12 base) compounding with a dead leg (-15 base) when you have orbitals still to complete.

If you have a single atmosphere delivery mixed into an otherwise orbital run, evaluate whether to complete it now or defer it to a dedicated atmosphere run. The scoring tool will flag this when it identifies orbital and atmosphere deliveries in the same batch.

---

## What UNRESOLVED Means in Practice

UNRESOLVED appears in tool output when a field — most often `reward_usc` — could not be read from OCR or was not supplied in your input.

An UNRESOLVED reward means the tool does not know whether this mission is profitable. It applies a 2-point penalty per unresolved field, capped at -12 across all fields, and drops the confidence rating to medium.

Do not fly a mission with an UNRESOLVED reward unless you have verified the actual value in-game. The tool cannot tell you whether the mission is worth your time if it does not know the reward. Accepting an UNRESOLVED mission is accepting an unknown — sometimes fine, sometimes a waste of a run.

To resolve it: look at the mission offer screen in-game, note the reward, add it to your JSON input manually, and re-run the scorer. This takes less than a minute and is worth doing for any mission you plan to accept.

---

## Freight Elevator Protocol (Hull-B)

The Hull-B loads and unloads via freight elevators. Plan for this.

Practical rules:
- Elevator wait time is real time. Account for it in your session planning. If you have six deliveries and each elevator takes two minutes, your run is twelve minutes longer than the flight time suggests.
- If a station elevator is broken or occupied, you may be unable to complete a delivery. Know your next delivery point before you discover a broken elevator, so you can reorder without confusion.
- Partial loads happen. If you cannot fit everything on one elevator run, note what you loaded and what remains. The cargo panel is your record.
- Come back for partial loads. Do not abandon remaining cargo at a station because it is inconvenient. Incomplete deliveries cancel the mission.

If you are running Hull-B on a fragmented route (multiple small deliveries to different stations), the fragmentation×1.10 modifier will hurt your score. This is by design — the Hull-B is not well-suited to fragmented routes and the tool reflects that.

---

## When to Override the Score

The score is advisory. There are legitimate reasons to accept a mission the tool scores below 70 or reject one it scores above 70.

Accept below threshold when:
- You have direct knowledge that a usually-penalised condition (congestion, dead leg) does not apply right now — for example, a normally-congested station that is empty on your current server.
- The payout is exceptionally high for the route length and you are willing to take a less efficient run for the income.
- You are positioning to a pickup cluster anyway and the dead leg cost is already paid.

Reject above threshold when:
- A station the route requires is known to be broken, bugged, or inaccessible on your current server.
- Server conditions are degrading and you do not want to commit to a long run.
- You have personal knowledge that the route conditions have changed since you entered the data.

When you override, note it. If you are submitting telemetry, the outcome data will be more useful if it reflects whether you followed or overrode the recommendation.

---

## Red Lines

These are actions the doctrine treats as unconditional stops. Do not do them.

**Never fly atmosphere-loaded with Hull-B as your first delivery when orbitals are available.**

The atmosphere penalty (-12 base, amplified by fragmentation on Hull-B) combined with the positioning cost of going to atmosphere before clearing orbitals will collapse your route efficiency. Orbitals first, always.

**Never accept a mission with UNRESOLVED reward without verifying the actual value first.** The tool does not know if the mission is worth your time. You are flying blind.

**Never accept a Red Wind mission that creates a dead leg into an isolated area unless the payout justifies it.** The dead_leg×1.10 modifier exists because this situation reliably produces poor runs. If you accept it anyway, you are making a deliberate choice, not an oversight.

---

## Positioning Discipline

Where you end your run determines how your next run starts. A run that ends at an isolated station with no nearby missions is a run that starts with a dead leg.

After each completed run:
- Check what missions are available from your current location.
- If the pickups are thin, plan your final delivery to put you near your next pickup cluster rather than at the most convenient delivery point.

This is not always possible — sometimes the best delivery comes last and that delivery is in the wrong place. But when you have a choice about which mission to complete last, choose the one that positions you best for the next run. Over a full session, positioning discipline compounds into meaningful time savings.
