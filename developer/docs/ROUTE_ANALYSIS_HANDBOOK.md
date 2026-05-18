# Route Analysis Handbook

Complete reference for understanding Apeirogon Logistics scores, factors,
recommendations, and how to use them in practice.

---

## How the Score Works

Every route starts at **50 points** (neutral).

Points are added for positive factors (stacking opportunities, route efficiency)
and subtracted for negative factors (dead legs, fragmentation, risk).

The final score is clamped to 0 to 100.

```
Final score = 50 + (positive factors) - (negative factors) ± issuer/ship modifiers
```

---

## Score Bands and Recommendations

| Score Range | Recommendation | Practical Meaning |
|-------------|---------------|-------------------|
| 70 to 100 | **accept** | Worth doing, good structure, low risk |
| 45 to 69 | **defer** | Marginal, consider stacking with other missions |
| 0 to 44 | **reject** | Poor structure, skip unless no alternatives |

These thresholds are configurable in `runtime/scoring_config.json` under
`score_bands`. Adjust them if the defaults don't match your playstyle.

---

## Positive Factors

### same_pickup (+16 per point)
The most valuable factor. Triggers when multiple missions share a pickup location.

A mission with `same_pickup: 1` means one extra mission shares your pickup; you
load cargo for two missions at one location. This adds 16 points.

Three missions at Port Olisar = `same_pickup: 2` = +32 points.

**For Hull-B**: The same-pickup stacking bonus is the primary value driver.
Look for Port Olisar clusters when choosing missions.

### destination_overlap (+12 per point)
Multiple missions deliver to the same location. Each extra mission going to
the same delivery adds 12 points. Less impactful than same-pickup but still
significant.

### orbital_loop (+12 per point)
Station-to-station route that follows a logical orbital chain (e.g. L-point
to L-point in the same system). Rewards routes with natural continuity.

### issuer_alignment (+8 per point)
This factor is applied by the issuer modifier system. Covalex routes get a 10%
boost to this factor, rewarding Covalex mission clustering.

### ship_suitability (+10 per point)
How well-suited the ship is to this route type. Hull-B has a 5% ship_suitability
modifier, reflecting its strong fit for multi-stop orbital Covalex runs.

### route_continuity (+10 per point)
Route includes a repeated location (e.g. returning to a hub). Rewards orbital
loop structures where you pass through a hub multiple times.

### cargo_panel_clarity (+8 per point)
Predictable cargo load with clear SCU counts. Hull-B gets a 15% modifier here,
reflecting the importance of clear panel reads for external spindle management.

---

## Negative Factors

### dead_leg (-15 per point)
The most damaging penalty. A dead leg is an empty flight from one place to
another, burning time and fuel for nothing. Each dead-leg event costs 15 points.

**Avoid missions that require a separate pickup at a distant location** unless
the reward justifies the positioning cost.

### chain_collapse (-14 per point)
Triggers when a route has more than 6 stops. Long chains become hard to execute
and collapse under server instability. -14 points when stop count exceeds 6.

### fragmentation (-12 per point)
Multiple deliveries spread across different locations. Each extra unique destination
adds to fragmentation. Hull-B gets a 10% modifier here; fragmented routes are
especially costly for its external cargo handling.

### atmosphere (-12 per point)
Atmosphere-heavy deliveries require flight through planetary atmosphere while
loaded, which is demanding for the Hull-B and increases delivery complexity.

### stop_density (-6 per point)
Triggers for each stop beyond 3. A 5-stop route incurs -12 points for stop density
(2 excess stops × -6). Discourages excessive multi-stop complexity.

### fatigue (-7 per point)
Route complexity fatigue: accumulates on long routes. Hull-B is relatively
resilient here (0.95× modifier, i.e. 5% reduction), reflecting its
orbital-loop specialisation.

### congestion (-8 per point)
Delivery to high-traffic or contested locations. Penalises routes with
predictable bottlenecks.

### unloading_cognitive_load (-7 per point)
Complex unloading scenarios: multiple cargo types, fragmented holds, or
mixed delivery manifests.

---

## Issuer Modifiers

Modifiers are multipliers applied to specific factors when a matching issuer
is detected in the route.

| Issuer | Modified Factors | Effect |
|--------|-----------------|--------|
| Covalex | issuer_alignment ×1.10, orbital_loop ×1.05, route_continuity ×1.05 | Rewards Covalex orbital chain structure |
| Ling / Ling Family | destination_overlap ×1.05, same_pickup ×1.03 | Small bonus for destination stacking |
| Red Wind | dead_leg ×1.10, congestion ×1.05 | Red Wind routes penalised more for dead legs |

These are in `runtime/scoring_config.json` under `issuer_modifiers`. Edit them
to match your observed experience with each issuer.

---

## Ship Modifiers

| Ship | Modified Factors | Effect |
|------|-----------------|--------|
| Hull-B | freight ×1.05, fragmentation ×1.10, cargo_panel_clarity ×1.15, ship_suitability ×1.05 | Rewards clear-panel runs; penalises fragmentation more |
| Hull-C | freight ×1.25, stop_density ×1.20, ship_suitability ×1.15 | Strongly penalises high stop counts |
| Taurus | ship_suitability ×1.05, fatigue ×0.95 | Slightly more resilient to long chains |
| Caterpillar | freight ×1.10, ship_suitability ×1.10 | Moderate freight bonus |
| Freelancer MAX | ship_suitability ×1.02, fatigue ×0.98 | Near-neutral modifiers |

---

## Understanding Warnings

The output includes a `warnings` list. Common warnings and what to do:

| Warning | Meaning | Action |
|---------|---------|--------|
| "Unresolved values present" | Fields you didn't supply | Score is less accurate; supply more data |
| "Dead-leg risk detected" | A dead-leg factor is present | Reconsider the route unless reward justifies it |
| "Cargo fragmentation exceeds recommended threshold" | More than 2 fragmentation points | Consider accepting fewer missions |
| "High stop density may degrade practical execution" | 6+ stops | Trim the run; too many stops is hard to execute |
| "Route-chain collapse risk detected" | 7+ stops | Strongly reconsider; this run will probably break |
| "Atmosphere burden detected" | Atmosphere deliveries present | Factor in planetary flight time and risk |

---

## Unresolved Fields and Confidence

Every output includes `unresolved_fields`: a list of data you didn't provide.
For each unresolved field, the score is less precise.

The system applies a penalty of up to -12 points for unresolved fields
(2 points per field, capped at 6 fields). This is intentional; if you don't know
the reward or cargo quantity, the system is appropriately less confident.

`confidence_level` in `governance_metadata` will be:
- `high`: all key fields supplied
- `medium`: some fields unresolved

Supply more mission data (reward, SCU, exact locations) for more accurate scores.

---

## Batch Scoring vs Single Route Scoring

**Single route scoring** (`deterministic_scorer.py`): best for verifying a
specific route you've already planned. Pass the full route as one input.

**Batch scoring** (`ingest_mission_batch.py`): best for deciding which missions
to accept from a list. Scores each mission individually and then computes the
optimal combined route. Use this when you're looking at the mission terminal
and choosing what to take.

The combined route in batch output often scores higher than any individual mission
because the same-pickup bonus only activates when multiple missions are combined.

---

## The Score Is Advisory

The scoring system uses heuristics based on patterns in Star Citizen hauling.
It cannot know:
- Current server conditions
- Freight elevator wait times
- Whether specific stations have problems right now
- Actual travel times on your server
- Whether cargo is physically available at the pickup

Your in-game judgment overrides the score when real-time conditions contradict it.
A "reject" route might be worth running if the server is quiet and the payout is
exceptional. An "accept" route might be wrong if the station is currently broken.

Use the score as a starting point, not a final answer.

---

## Tuning the Scoring System

All weights are in `runtime/scoring_config.json`. Change values to match
your experience:

- If same_pickup stacking matters more to you → increase `same_pickup` weight
- If you tolerate dead legs more than average → reduce `dead_leg` weight (make it less negative)
- If your Hull-B handles fragmentation better than the default assumes → reduce `fragmentation` weight

Changes to the config file take effect immediately, with no code changes needed.
