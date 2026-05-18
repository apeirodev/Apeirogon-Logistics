# Known Issues

Operational limitations and known gaps in the current scoring system.
These are not bugs — they are things the tool does not model yet, or game behaviours that change too frequently to hard-code.

---

## Route Modeling Gaps

**Freight elevator behaviour is not modeled.** Elevator availability, wait time, and reliability vary significantly across patches and servers. Routes with many elevator stops take longer than flight time suggests. Plan for this manually — the stop_density penalty is a rough proxy but not a precise model.

**Quantum travel times are not modeled.** The tool counts stops and assesses route shape but does not calculate actual flight time between points. A five-stop route in a tight orbital cluster is faster than a three-stop route that crosses the system. Use your experience to estimate travel time.

**Exact QT distances are not included.** The route graph does not contain point-to-point distances. Stop count and orbital vs atmosphere classification are the current proxies for route length.

**Quantum interdictions are not modeled.** If your route passes through high-risk interdiction zones, the tool will not flag it. This is live game state that cannot be captured in a static scoring config.

---

## Location and Station Gaps

**Lagrange station implementations vary.** Some L-point stations have limited or inconsistent cargo handling across patches. The tool does not track per-station capability state. If a station appears in your route and you know it has cargo issues on the current patch, override the score manually.

**Surface outpost layouts are not individually modeled.** Surface deliveries are classified as "atmosphere" but the tool does not differentiate between a quick surface stop and a long outpost sequence.

**Station availability is server-dependent.** The tool assumes all stops in your route are accessible. If a station is offline, bugged, or inaccessible on your current server, the tool will not know.

---

## Scoring Model Limitations

**Live mission distribution patterns are not learned.** The tool scores individual mission sets you provide. It does not have data on mission frequency, spawn rates, or typical availability at each location. Same-pickup stacking bonuses require you to have multiple missions from the same location — the tool cannot tell you how likely that is.

**Atmospheric flight burden varies by ship and pilot.** The atmosphere penalty (-12) is a fixed heuristic. Actual atmospheric difficulty depends on your ship's handling, your piloting, current weather effects, and server performance. Hull-B loaded in atmosphere is harder than other ships; the modifier amplifies this, but the actual time cost is not modeled precisely.

**Hangar assignment distance and efficiency are not modeled.** Which hangar you are assigned at a busy station affects your taxi time to the freight elevator. This varies by server and cannot be predicted.

**Congestion is a static estimate.** The congestion penalty reflects locations that tend to have high traffic, but actual server traffic is dynamic. A normally-congested station may be empty at 3am or during an event; the tool will still apply the penalty.

---

## OCR and AI Extraction

**OCR accuracy depends on in-game UI scale and screenshot quality.** If text is small or aliased, OCR confidence will be low. Increase your in-game UI scale before screenshotting for best results.

**AI providers may fail to acknowledge strict mode.** If your AI session does not respond with "STRICT MODE ACTIVE" after you paste `prompts/STRICT_AI_SESSION_PROMPT.md`, the hallucination guardrails are not active. Re-paste the prompt. Do not proceed without acknowledgement.

**Location alias coverage is incomplete.** `runtime/OCR_normalization_rules.json` contains known location aliases but does not cover every possible OCR variant. If a location is not resolving correctly, add it to the aliases file. See `docs/OCR_PROCESSING_GUIDE.md`.

---

## Patch Sensitivity

**All payout and capacity values are patch-dependent.** The scoring tool does not store game values. When CIG changes mission payouts, cargo capacities, or station availability in a patch, you need to update your input data. The tool will score whatever you give it — wrong input produces wrong scores.

**Issuer and ship modifier calibration is manual.** The modifiers in `scoring_config.json` reflect patterns observed in testing. They may drift from actual game behaviour after patches. If scores feel wrong for your ship or issuer, adjust the relevant modifiers.

---

## Telemetry

**Telemetry submission is manual and opt-in.** `bundle_telemetry.py` packages local telemetry files into a zip. Nothing is submitted automatically. You need to manually initiate submission.

**Telemetry does not auto-calibrate the scorer.** Submitted telemetry is used for human review and future calibration. The tool does not update its own weights from telemetry automatically.
