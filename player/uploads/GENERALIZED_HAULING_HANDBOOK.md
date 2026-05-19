# Generalized Hauling Handbook

> **PLAYER COPY**: adapted from `developer/docs/GENERALIZED_HAULING_HANDBOOK.md` for the
> screenshot-paste workflow. Sections covering Python tool configuration and weight tuning
> are in the developer version and are not needed here.

How to use Apeirogon Logistics for hauling scenarios beyond the Hull-B Covalex primary workflow.

---

## Primary vs. Generalized Use

The primary workflow this toolset was built for is Hull-B Covalex orbital chains in Stanton. The scoring config defaults, ship modifiers, and documentation are calibrated for that use case.

The generalized workflow extends the same scoring system to:
- Other ships (Hull-C, Taurus, Caterpillar, Freelancer MAX)
- Other issuers (Ling, Red Wind, others)
- Mixed-issuer batches
- Non-Stanton systems (less tested, no system-specific location data)
- Atmosphere-heavy routes that are planned rather than avoided

---

## Applying the Scoring to Other Ships

Tell your AI which ship you are flying at the start of each session. The scoring system applies that ship's modifier block automatically. Supported ships and their key adjustments:

| Ship | Key adjustments |
|---|---|
| Hull-B | Fragmentation x1.10, freight x1.05, suitability x1.05 |
| Hull-C | Stop density x1.20, freight x1.25, suitability x1.15 |
| Taurus | Fatigue x0.95 (slightly easier multi-stop runs) |
| Caterpillar | Freight x1.10, suitability x1.10 |
| Freelancer MAX | No significant deviation from base weights |
| Starlancer MAX | Suitability x1.05, fatigue x0.95, freight x1.03 |
| Starlancer TAC | Suitability x0.88 (combat variant -- reduced hauling suitability) |
| RAFT | Suitability x1.05, freight x1.05, dead leg x0.95 |
| Valkyrie | Suitability x0.90, atmosphere x0.85 (reduced), fatigue x0.92 |
| Asgard | Suitability x0.95, atmosphere x0.85 (reduced), fatigue x0.95 |
| A2 Hercules Starlifter | Suitability x0.85 (bomber), atmosphere x0.90, freight x1.05 |
| M2 Hercules Starlifter | Suitability x1.05, atmosphere x0.90 (reduced), freight x1.10 |
| C2 Hercules Starlifter | Suitability x1.08, atmosphere x0.88 (reduced), freight x1.10 |
| Starfarer | Suitability x0.88 (tanker), freight x1.05, stop density x1.10 |
| Starfarer Gemini | Suitability x0.85, freight x1.05, stop density x1.10 |
| Ironclad | Suitability x1.10, freight x1.15, stop density x1.25, fragmentation x1.15 |
| Ironclad Assault | Suitability x0.90, freight x1.10, stop density x1.20 |
| Hermes | Suitability x1.05, dead leg x0.90 (reduced), fatigue x0.92 |
| Railen | Suitability x1.05, freight x1.08, atmosphere x0.90 (slightly reduced) |

For any ship not in this list, tell your AI the ship name anyway. It will score on base weights with no ship modifier -- still useful for comparing routes.

Hull-D, Hull-E, Banu Merchantman, and Galaxy are not yet flyable in Alpha 4.8. Do not attempt to score routes for these ships -- all published values for them are speculative placeholders.

---

## Mixed-Issuer Batches

The scoring system handles missions from multiple issuers in a single session. Each mission uses its own issuer's modifier. When you have contracts from multiple issuers at the terminal:

- Same-pickup stacking still applies regardless of issuer; a Covalex mission and a Ling mission at the same pickup can be stacked
- Issuer modifiers apply per-mission, not per-batch
- Mixed batches score the combined route shape; overlapping deliveries and shared pickups are rewarded across issuer lines

---

## Issuer-Specific Planning

**Covalex:** Best for same-pickup orbital chains. The system gives Covalex missions a bonus for orbital loops and route continuity. Prioritize same-pickup clusters and stay in orbital space when possible.

**Ling / Ling Family:** Destination overlap and same-pickup bonuses reward stacking. The same cluster analysis strategy as Covalex applies. Smaller ships work well for Ling missions given their typical cargo sizes.

**Red Wind:** Dead leg and congestion penalties are amplified for Red Wind. Only accept Red Wind missions when you are already positioned near the pickup and the delivery is orbital and on your route. Isolated Red Wind missions in congested areas are consistently poor performers.

**Hurston Dynamics, microTech, ArcCorp:** These issuers are recognized by the system but their scoring modifiers have not yet been calibrated. Your AI will score their missions on base weights and should tell you this. Do not expect issuer-specific bonuses or penalties for these three.

**Unknown issuers:** If you encounter an issuer not listed above, tell your AI anyway. It will score the route on base weights, which still gives you useful Accept / Defer / Reject guidance.

---

## Atmosphere-Heavy Routes

The atmosphere penalty is calibrated for Hull-B where atmospheric flight when fully loaded is a practical problem. Ships with better atmospheric handling are already accounted for through per-ship modifiers -- the C2 Hercules, Valkyrie, Asgard, M2 Hercules, and Railen all have reduced atmosphere penalties built into their scoring blocks. Telling your AI your ship at session start applies these automatically.

Do not ask your AI to adjust the atmosphere penalty weight mid-session. The AI has no valid basis for inventing a new weight, and will produce unreliable scores if asked to do so. If the penalty still feels wrong for your ship after using the correct ship name, report it so the modifier can be updated in the next release.

---

## Non-Stanton Systems

The location lookup file (`OCR_normalization_rules.json`) currently covers Stanton locations. If you are hauling in Pyro or another system:

- The scoring system still works; it treats unfamiliar locations as unknown type rather than orbital, which slightly understates scores for orbital stations in other systems
- If you know a stop is orbital, tell your AI: *"[Location name] is an orbital station"*; it will score it correctly
- As you encounter new locations, you can report them for addition to future updates

---

## What to Tell Your AI Each Session

For the most accurate scoring on any ship or issuer:

1. **Your ship**: exact model, e.g. "Hull-B", "Taurus", "Caterpillar"
2. **Your current location**: so the AI can identify dead legs
3. **The issuer(s)** on screen: if more than one, say so
4. **Any values you cannot read**: paste them as text; do not let the AI guess

The more context you give, the more accurate the recommendations.
