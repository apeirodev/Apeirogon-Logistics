# Known Issues

Operational limitations and known gaps in the current scoring system.
These are not bugs; they are things the tool does not model yet, or game behaviours that change too frequently to hard-code.

---

## Route Modeling Gaps

**Freight elevator behaviour is not modeled.** Elevator availability, wait time, and reliability vary significantly across patches and servers. Routes with many elevator stops take longer than flight time suggests. Plan for this manually; the stop_density penalty is a rough proxy but not a precise model.

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

**Live mission distribution patterns are not learned.** The tool scores individual mission sets you provide. It does not have data on mission frequency, spawn rates, or typical availability at each location. Same-pickup stacking bonuses require you to have multiple missions from the same location; the tool cannot tell you how likely that is.

**Atmospheric flight burden varies by ship and pilot.** The atmosphere penalty (-12) is a fixed heuristic. Actual atmospheric difficulty depends on your ship's handling, your piloting, current weather effects, and server performance. Hull-B loaded in atmosphere is harder than other ships; the modifier amplifies this, but the actual time cost is not modeled precisely.

**Hangar assignment distance and efficiency are not modeled.** Which hangar you are assigned at a busy station affects your taxi time to the freight elevator. This varies by server and cannot be predicted.

**Congestion is a static estimate.** The congestion penalty reflects locations that tend to have high traffic, but actual server traffic is dynamic. A normally-congested station may be empty at 3am or during an event; the tool will still apply the penalty.

---

## OCR and AI Extraction

**OCR accuracy depends on in-game UI scale and screenshot quality.** If text is small or aliased, OCR confidence will be low. Increase your in-game UI scale before screenshotting for best results.

**AI providers may fail to acknowledge strict mode.** If your AI session does not respond with "STRICT MODE ACTIVE" after you paste `prompts/STRICT_AI_SESSION_PROMPT.md`, the hallucination guardrails are not active. Re-paste the prompt. Do not proceed without acknowledgement.

**Location alias coverage is incomplete.** `runtime/OCR_normalization_rules.json` contains known location aliases but does not cover every possible OCR variant. If a location is not resolving correctly, add it to the aliases file. See `docs/OCR_PROCESSING_GUIDE.md`.

---

## Unverified Game Mechanics

**Freight elevator container size sequence is player-reported and unverified.** The scoring instruction block uses the sequence [32, 16, 8, 4, 2, 1 SCU] for container breakdown calculations. This sequence was reported by a player during Alpha 4.8 testing. It has not been independently verified across all ship types, all station types, or all patch states. If the actual sequence differs, container breakdown calculations in rank mode will be wrong. The sequence may also vary by contract, by station, or by patch. When the player reports a different sequence at a specific elevator, use what the player observed for that session.

**Delivery crediting mechanism for same-commodity same-pickup contracts is not verified.** When two accepted contracts share the same pickup location and the same commodity type, the freight elevator presents an undifferentiated container pool. Whether Star Citizen credits containers to the source contract, to the commodity type, or to some other tracking mechanism is not documented in project knowledge files and has not been independently verified. The three safe strategies (monitor contract manager per interaction, load one full qualifying leg before the second, or load full-leg SCU for all conflicting contracts) are presented to the player without asserting how the game works.

**Same-pickup same-commodity disambiguation is not executable at the elevator.** In the shared-pool scenario above, minimum-load disambiguation -- loading exactly the container count for one contract before loading for the second -- cannot be confirmed to work correctly. The player may be loading containers from a shared pool that the game does not attribute per-contract. This is an open research question for the project. Players who discover the actual mechanism should report it so that the instruction block can be updated.

---

## Patch Sensitivity

**All payout and capacity values are patch-dependent.** The scoring tool does not store game values. When CIG changes mission payouts, cargo capacities, or station availability in a patch, you need to update your input data. The tool will score whatever you give it; wrong input produces wrong scores.

**Issuer and ship modifier calibration is manual.** The modifiers in `scoring_config.json` reflect patterns observed in testing. They may drift from actual game behaviour after patches. If scores feel wrong for your ship or issuer, adjust the relevant modifiers.

---

## Telemetry

**Telemetry submission is manual and opt-in.** `bundle_telemetry.py` packages local telemetry files into a zip. Nothing is submitted automatically. You need to manually initiate submission.

**Telemetry does not auto-calibrate the scorer.** Submitted telemetry is used for human review and future calibration. The tool does not update its own weights from telemetry automatically.
