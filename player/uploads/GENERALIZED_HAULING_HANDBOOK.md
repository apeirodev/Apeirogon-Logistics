# Generalized Hauling Handbook

> **PLAYER COPY** — adapted from `developer/docs/GENERALIZED_HAULING_HANDBOOK.md` for the
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

Tell your AI which ship you are flying at the start of each session. The scoring system applies that ship's modifier block automatically. Supported ships and their scoring adjustments:

| Ship | Key adjustments |
|---|---|
| Hull-B | Fragmentation ×1.10, freight ×1.05, suitability ×1.05 |
| Hull-C | Stop density ×1.20, freight ×1.25, suitability ×1.15 |
| Taurus | Fatigue ×0.95 (slightly easier multi-stop runs) |
| Caterpillar | Freight ×1.10, suitability ×1.10 |
| Freelancer MAX | Suitability ×1.02, fatigue ×0.98 |

For ships not in this list, tell your AI what ship you are flying anyway. It will score on base weights, which is still useful for comparing routes against each other.

---

## Mixed-Issuer Batches

The scoring system handles missions from multiple issuers in a single session. Each mission uses its own issuer's modifier. When you have contracts from multiple issuers at the terminal:

- Same-pickup stacking still applies regardless of issuer — a Covalex mission and a Ling mission at the same pickup can be stacked
- Issuer modifiers apply per-mission, not per-batch
- Mixed batches score the combined route shape — overlapping deliveries and shared pickups are rewarded across issuer lines

---

## Issuer-Specific Planning

**Covalex:** Best for same-pickup orbital chains. The system gives Covalex missions a bonus for orbital loops and route continuity. Prioritize same-pickup clusters and stay in orbital space when possible.

**Ling / Ling Family:** Destination overlap and same-pickup bonuses reward stacking. The same cluster analysis strategy as Covalex applies. Smaller ships work well for Ling missions given their typical cargo sizes.

**Red Wind:** Dead leg and congestion penalties are amplified for Red Wind. Only accept Red Wind missions when you are already positioned near the pickup and the delivery is orbital and on your route. Isolated Red Wind missions in congested areas are consistently poor performers.

**Unknown issuers:** If you encounter an issuer not listed above, tell your AI anyway. It will score the route on base weights, which still gives you useful Accept / Defer / Reject guidance.

---

## Atmosphere-Heavy Routes

The atmosphere penalty is calibrated for Hull-B where atmospheric flight when fully loaded is a practical problem. Ships with better atmospheric handling (Taurus, Cutlass, smaller ships) handle atmosphere more comfortably.

If your AI is penalizing atmosphere stops too aggressively for your ship, tell it: *"I am flying a [ship] which handles atmosphere well — reduce the atmosphere penalty."* The AI can adjust its weighting for your session.

---

## Non-Stanton Systems

The location lookup file (`OCR_normalization_rules.json`) currently covers Stanton locations. If you are hauling in Pyro or another system:

- The scoring system still works — it treats unfamiliar locations as unknown type rather than orbital, which slightly understates scores for orbital stations in other systems
- If you know a stop is orbital, tell your AI: *"[Location name] is an orbital station"* — it will score it correctly
- As you encounter new locations, you can report them for addition to future updates

---

## What to Tell Your AI Each Session

For the most accurate scoring on any ship or issuer:

1. **Your ship** — exact model, e.g. "Hull-B", "Taurus", "Caterpillar"
2. **Your current location** — so the AI can identify dead legs
3. **The issuer(s)** on screen — if more than one, say so
4. **Any values you cannot read** — paste them as text; do not let the AI guess

The more context you give, the more accurate the recommendations.
