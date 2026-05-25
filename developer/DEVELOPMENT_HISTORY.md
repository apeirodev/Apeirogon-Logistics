# Apeirogon Logistics: Development History

This file records the phase-by-phase construction history of the platform. It is reference material only and does not describe the current operational state of the project.

For current capabilities see `README.md`. For the current changelog see `CHANGELOG_0_30_5.md`.

---

## Phase 1

Purpose: portable seed dataset for Hull-B Covalex hauling route optimisation.

Introduced canonical Stanton location records, source attribution, aliases, and initial derived operational scores. Intentionally separated sourced facts from derived hauling heuristics.

Key files: `data/locations.json`, `data/location_aliases.json`, `data/source_registry.json`, `schema/location.schema.json`

---

## Phase 2

Introduced topology-only route graph edges and adjacency representations.

Key files: `data/route_edges.json`, `data/adjacency_matrix.json`, `schema/route_edge.schema.json`

Note: QT time remains runtime-derived from quantum drive data and is not stored as a fixed edge value.

---

## Phase 3

Introduced derived operational hauling heuristics and classification models for Stanton logistics optimisation.

Key files: `data/hauling_penalties.json`, `schema/hauling_penalty.schema.json`, `docs/DERIVATION_RULES.md`, `docs/KNOWN_ISSUES.md`, `VERSION.json`

---

## Phase 4

Introduced hauling ship operational profiles and runtime traversal modelling foundations.

Key files: `data/ship_profiles.json`, `runtime/runtime_traversal_models.json`, `schema/ship_profile.schema.json`, `schema/runtime_traversal.schema.json`

---

## Phase 5

Introduced quantum drive operational profiles and dynamic traversal modelling foundations.

Key files: `data/quantum_drive_profiles.json`, `runtime/traversal_calculation_models.json`, `schema/quantum_drive.schema.json`, `schema/traversal_calculation.schema.json`

---

## Phase 6

Introduced mission ingestion structures, OCR normalisation rules, and screenshot extraction foundations.

Key files: `data/mission_batches.json`, `runtime/screenshot_ingestion_rules.json`, `runtime/OCR_normalization_rules.json`, `runtime/mission_extraction_pipeline.json`

---

## Phase 7

Introduced route optimisation, mission scoring, and hauling strategy engines.

Key files: `analytics/route_scoring_models.json`, `analytics/mission_chain_models.json`, `runtime/route_optimization_engine.json`, `analytics/mission_acceptance_rules.json`, `analytics/hauling_strategy_profiles.json`

---

## Phase 8

Introduced historical mission-learning and adaptive route prediction foundations.

Key files: `analytics/historical_mission_patterns.json`, `analytics/continuation_probability_models.json`, `analytics/adaptive_route_prediction_models.json`, `analytics/mission_density_heatmaps.json`, `analytics/hauling_behavior_learning_rules.json`

---

## Phase 9

Introduced persistent mission memory and cross-session adaptive analytics foundations.

Key files: `runtime/live_mission_ingestion_runtime.json`, `analytics/persistent_mission_memory.json`, `analytics/cross_session_analytics_models.json`, `analytics/adaptive_player_profile_models.json`, `schema/mission_history_log.schema.json`

---

## Phase 10

Introduced live execution state engines and probabilistic automated route simulation.

Key files: `runtime/live_route_execution_engine.json`, `runtime/mission_state_machine_models.json`, `runtime/automated_route_simulation_models.json`, `runtime/live_recommendation_adaptation_models.json`, `schema/execution_event_log.schema.json`

---

## Phase 11

Introduced distributed fleet coordination and cooperative hauling orchestration.

Key files: `analytics/fleet_coordination_models.json`, `analytics/multiplayer_hauling_orchestration.json`, `analytics/cooperative_route_distribution_models.json`, `analytics/convoy_risk_models.json`, `schema/fleet_event_log.schema.json`

---

## Phase 12

Introduced economic forecasting and inter-system logistics expansion.

Key files: `analytics/commodity_flow_models.json`, `analytics/economic_forecasting_models.json`, `analytics/intersystem_route_models.json`, `analytics/regional_supply_pressure_models.json`, `schema/commodity_event_log.schema.json`

---

## Phase 13

Introduced autonomous logistics delegation and distributed operational planning systems.

Key files: `analytics/autonomous_hauling_agent_models.json`, `analytics/logistics_delegation_models.json`, `analytics/distributed_operational_planning_models.json`, `analytics/adaptive_convoy_command_models.json`, `schema/autonomous_event_log.schema.json`

---

## Phase 14

Introduced alliance-scale strategic logistics governance and persistent economic campaign systems.

Key files: `analytics/strategic_logistics_governance_models.json`, `analytics/alliance_scale_coordination_models.json`, `analytics/persistent_economic_campaign_models.json`, `analytics/macro_supply_chain_resilience_models.json`, `schema/strategic_event_log.schema.json`

---

## Phase 15

Introduced galactic-scale logistics and geopolitical hauling simulation systems.

Key files: `analytics/galactic_logistics_simulation_models.json`, `analytics/sovereignty_influence_models.json`, `analytics/geopolitical_hauling_analysis_models.json`, `analytics/strategic_corridor_control_models.json`, `schema/geopolitical_event_log.schema.json`

---

## Phase 16

Introduced civilisation-scale logistics ecosystem simulation and autonomous faction equilibrium systems.

Key files: `analytics/civilization_scale_logistics_ecosystems.json`, `analytics/autonomous_faction_simulation_models.json`, `analytics/transregional_equilibrium_models.json`, `analytics/strategic_civilization_resilience_models.json`, `schema/civilization_event_log.schema.json`

---

## Phase 17

Introduced synthetic recovery systems and post-scarcity logistics modelling.

Key files: `analytics/post_scarcity_logistics_models.json`, `analytics/synthetic_economy_simulation_models.json`, `analytics/galactic_equilibrium_recovery_models.json`, `analytics/strategic_repopulation_models.json`, `schema/synthetic_event_log.schema.json`

---

## Phase 17.1 Repair

Validated Phase 17 artefacts, regenerated only missing files, preserved version lineage, incremented package version to `0.17.1`.

---

## Phase 18

Introduced recursive self-healing logistics systems, galactic governance balancing, equilibrium preservation architectures, adaptive entropy suppression, and recursive stability feedback loops.

---

## Phase 19

Introduced operational packaging, validation hardening, export readiness, and practical Hull-B Covalex route-analysis guidance.

---

## Phase 20

Introduced live operational integration, screenshot workflow optimisation, continuous operational learning, and practical Hull-B hauling assistance.

---

## Phase 21

Introduced execution telemetry models, real session analytics, adaptive operational refinement, mission chain telemetry, and practical Hull-B telemetry logging.

---

## Phase 22

Introduced telemetry calibration systems, practical route-score tuning, observed Hull-B performance baselines, observed route-quality analysis, and telemetry calibration logging.

---

## Phase 23A

Introduced statistical calibration, telemetry variance modelling, comparative ship-efficiency analytics, patch-regression detection, operational anomaly detection, telemetry retention policy, and heuristic decay modelling.

---

## Phase 24B

Introduced generalised hauling intelligence, issuer profiles, multi-ship operational modelling, and hauling archetypes.

---

## Phase 25: Finalization

Platform finalised as a mature Star Citizen hauling intelligence platform.

Primary entry points at time of finalisation: `operational_handoff_guide.md`, `final_operational_playbook.md`, `final_reusable_prompt_library.md`, `canonical_future_maintenance_prompt.md`, `final_export_manifest.json`

---

## Public Enhancement Phase A

Extended for public open-source readiness.

Additions: operational doctrine rules, cargo panel assignment rules, patch lineage registry, telemetry submission workflows, contributor data standards, GitHub repository structure guidance, open-source governance guidance, route realism enrichment models.

---

## Phase 26: Provider-Neutral Local-First Architecture

Platform explicitly declared local-first, provider-neutral, and addon-ready.

Key rules established: users bring their own AI provider or run locally; manual mode supported; deterministic fallback supported; future addon support optional and unimplemented.

---

## Version 0.28.1: AI Provider Usability and Portable Persistence

Added provider-specific usage guides and portable persistence models.

Supported workflows: ChatGPT, Claude, Gemini, Microsoft Copilot, Perplexity, Ollama, LM Studio, OpenAI-compatible APIs, Anthropic-compatible APIs, manual copy/paste.

---

## Version 0.28.2: Licensing Update

License unified to CC BY-NC 4.0 for all project assets: code, tooling, adapters, runtimes, datasets, prompts, schemas, documentation, and operational intelligence.

---

## Version 0.29.1: Governance Alignment

Added architectural governance alignment materials for CSA CCM v4.1.0, CSA CAIQ v4.1.0, CSA AICM v1.0.3, and CSA AI CAIQ v1.0.2.

Added: provenance enforcement, telemetry trust tiers, AI output trust boundaries, contributor governance, threat models, shared responsibility models, governance metadata schema.

---

## Version 0.29.2: Operational Hardening

Governance correction, operational realism hardening, deterministic fallback execution, contributor usability improvements, CI validation, provider-neutral operation.

---

## Version 0.29.3: Operational Tooling Expansion

Expanded deterministic operational tooling, telemetry ingestion readiness, contributor onboarding, provider-neutral workflows, executable route-analysis tooling, CI/CD operational hardening.

---

## Version 0.30.1: MVP Operational Platform Transition

Transitioned from specification-heavy scaffolding to a minimally viable executable operational platform.

Added: executable CLI tooling, telemetry ingestion workflows, governance metadata validation, deterministic operational route analysis, operational regression fixtures, release integrity structures, portable local operational workflows.

---

## Version 0.30.2: Productionisation

Productionisation and placeholder elimination release.

---

## Version 0.30.5: Rebuild Release

Rebuilt the failed 0.30.4 scope from verified 0.30.3. Version 0.30.4 is recorded as `abandoned_failed_run`.

See `CHANGELOG_0_30_5.md` for full details.

---

## Version 0.36.2: Player Accessibility Release

Introduced the `player/` directory with AI-native workflow: per-platform setup guides (Claude, ChatGPT, Gemini, Other), session start prompt, and embedded scoring logic so players can get route recommendations from any AI assistant without installing Python. Reorganized repository so all technical and developer files live under `developer/`, leaving the root clean for non-technical users. Established Semantic Versioning (Major.Minor.Patch) as the project versioning standard.

---

## Version 0.36.2: Star Citizen Patch Update

Set Star Citizen patch version to Alpha 4.8.0 across all canonical files: VERSION.json, patch_lineage_registry.json, example sessions and outputs, test fixtures, and documentation examples. Previous placeholder values (UNRESOLVED_REQUIRES_VALIDATION, UNRESOLVED, 4.x, 4.1, Alpha 3.23) replaced with the confirmed current patch.

---

## Version 0.37.1: Player Uploads Folder

Added `player/uploads/` containing six files players upload to their AI project: scoring_config.json, OCR_normalization_rules.json, mission_schema.json, mission_issuer_profiles.json, hull_b_covalex_route_playbook.md (player-adapted), and GENERALIZED_HAULING_HANDBOOK.md (player-adapted). Four JSON files are exact copies; two markdown files have developer-specific sections replaced with the screenshot workflow. Cross-reference notes added to all canonical developer files. All four SETUP_*.md guides updated to reference player/uploads/.

---

## Version 0.57.1: Rank Mode Run Management

Eight live-session fixes (Issues 8-15):

8. Running capacity tracking added. After each accepted contract, outputs running total, ship capacity, and remaining capacity. Warns when remaining < 96 SCU. Hard blocks at capacity. Run cap enforcement stops acceptance at the declared cap and routes remaining VIABLE contracts to the DEFERRED list.

9. Run size target established at run start. "How many contracts do you want in this run?" asked before any contracts are evaluated. Used as a hard cap throughout.

10. Opportunistic same-location contracts: before recommending acceptance, recalculates total run SCU including the opportunistic contract's minimum load. Outputs updated running total first. Blocks recommendation if it would breach capacity.

11. COMBINED STOP detection added to RUN PLAN CONSTRUCTION. After finalising the contract list, scans all delivery destinations and all pickup locations for matches. Matched locations become single COMBINED STOP entries: deliver first, submit, then load. Never split into separate rows.

12. DEFERRED LIST section added. Tracks VIABLE contracts not included in the current run. Displayed at the start of every new run planning cycle. Persists until executed or explicitly abandoned by the player.

13. Run target destination declared at run start. "What is your target delivery destination for this run?" asked explicitly. DROP-OFF CONSOLIDATION CHECK now uses this declared target instead of inferring dominant destination from accepted contracts. Any contract not delivering to the declared target is an outlier before acceptance.

14. Route table column order fixed: Location | Action | Contract | Commodity | Containers. This order is mandatory for all route output.

15. Current location pickup check added to run start. "Are there any contracts available at your current location?" asked after target and size are confirmed. Qualifying contracts at current location flagged as ZERO DEAD LEG PICKUP and factored into capacity before evaluating other contracts.

Synced to all 7 SETUP files.

---

## Version 0.56.1: Rank Mode Run Plan Infrastructure

Seven live-session fixes, all in rank mode:

1. NOT VIABLE contracts now explicitly excluded from all downstream processing: run plan, capacity totals, container counts, stacking summary, drop-off consolidation check. Short-circuit is complete -- the contract does not appear again after the NOT VIABLE output.

2. Multi-commodity suppression now uses explicit "Do not load" output for every commodity not recommended. Single qualifying commodity: all others labelled "Do not load [commodity] -- not needed for rep threshold." Combined minimum: commodities at other destinations labelled "Do not load [commodity] -- delivers to [destination], not part of this run." Never outputs a combined SCU total.

3. Blocking fields extended: CONTRACT READING item 6 now lists all four blocking fields (pickup, delivery, cargo_scu, reward) with exact output format per field. In rank mode specifically, reward is not blocking -- it is marked UNRESOLVED and analysis continues. Pickup, delivery, and cargo_scu remain blocking in both modes.

4. Drop-off consolidation check added. Runs after all contracts are analyzed and before run plan construction. Identifies dominant destination, flags outlier contracts with exact output format and recommend-abandon instruction, blocks run plan until player confirms keep or abandon for each outlier.

5. Container math added throughout. Minimum qualifying SCU is now always converted to: container count = ceil(minimum/16), actual SCU = container count x 16. Per-commodity container counts for multi-commodity loads. Raw SCU minimum never shown without container count alongside it.

6. Duplicate contract detection added. Tracks all seen/abandoned contracts by pickup, commodity, total SCU, and leg structure. Detects duplicates immediately on paste and instructs "Abandon again" without re-analyzing.

7. Run plan construction section added. Defines structure for pickup stop listing, per-contract load lines, panel separation prompt for non-dominant destinations, panel naming gate before run plan output, and panel exclusion reminder in every subsequent pickup instruction.

Synced to all 7 SETUP files.

---

## Version 0.55.1: Rank Mode Viability Check, Multi-Commodity, and Reward Block

Three live-session fixes:

1. Pre-acceptance viability check (rank mode): viability is now the first output item for every contract. If no single leg reaches 26%, the AI outputs NOT VIABLE immediately with the highest leg percentage and abandon advice, then stops all further analysis for that contract. The full leg breakdown, minimum load, and payout tier are suppressed for NOT VIABLE contracts. The AI no longer waits for the player to ask.

2. Multi-commodity leg handling (rank mode): contracts with multiple commodities at the same pickup now evaluate each [commodity --> destination] pair independently. If one commodity alone qualifies (>= 26% of total), only that commodity is recommended and all others are suppressed from output. If no single commodity qualifies alone but combined delivery to one destination does, the minimum qualifying load is listed per-commodity, loaded highest-SCU first, with non-contributing commodities suppressed. The output format now requires per-commodity quantity breakdown whenever multiple commodities contribute to the minimum load.

3. Reward field blocking (normal scoring mode): if the reward field is UNRESOLVED for any contract, the AI outputs the readable fields, marks reward UNRESOLVED, and stops -- explicitly asking the player to type the reward before proceeding. A score or Accept/Defer/Reject recommendation is not output until the reward is supplied. The existing -2 UNRESOLVED penalty is not a substitute.

Synced to all 7 SETUP files.

---

## Version 0.54.3: Covalex Rank Mode Extended to All Ranks

Removed the Senior-to-Master restriction from rank mode. The partial submit
mechanic applies at every Covalex rank -- threshold and submission rules are
identical across all ranks. Only contract size and leg count vary.

Instruction block: trigger now also accepts "rank focus mode". Confirmation
message no longer says "master-rank". Added note that lower-rank contracts have
fewer legs and smaller total SCU, making the 26% threshold proportionally easier
to hit. Threshold logic and output format unchanged.

Handbook: retitled to "Rank Focus at Any Rank". CONTRACT PATTERN section replaced
with CONTRACT PATTERNS BY RANK covering lower ranks (Associate, Member) and higher
ranks (Senior, Master). Notes section updated with lower-rank guidance.

Synced to all 7 SETUP files.

---

## Version 0.54.2: Covalex Rank Minimum Load Fix

Corrected the rank mode output to distinguish between the full leg SCU and the
minimum qualifying load required to reach the 26% threshold.

Key change: the AI now calculates minimum qualifying SCU = total contract SCU
multiplied by 0.26, rounded up. It reports the full leg, the minimum for rep,
and the space saved by loading only the minimum. Players should load the minimum
to preserve ship capacity for stacking additional contracts.

Ranking updated: contracts now rank by minimum qualifying SCU (not full leg SCU)
to reflect the actual capacity cost per contract in a stacking run.

Stacking summary added: after analyzing all contracts, the AI shows the combined
minimum qualifying SCU across all VIABLE contracts versus confirmed ship capacity.

Player workflow reminder updated to specify loading the minimum qualifying SCU at
the pickup location, not the full leg.

Player handbook (COVALEX_RANK_STRATEGY.md) updated with minimum-load explanation,
worked example, and stacking instructions updated to reference minimum loads.

Synced to all 7 SETUP files.

---

## Version 0.54.1: Covalex Rank Strategy Mode

New analysis mode for Covalex reputation grinding (Senior to Master rank).

Added COVALEX RANK STRATEGY MODE section to scoring_instruction_block.md:
- Trigger phrase: "covalex rank mode", "strategize covalex rank", or "senior to master mode"
- Separate mode that suspends standard scoring and cargo panel tracking
- Mechanic encoded: 25% game threshold, 26% working viability threshold with safety margin
- Partial submission credit payout tiers documented: ~15% credits at 25-50%, ~45% at 51-75%, ~76% at 76-99%
- For each contract: extracts all legs, calculates each leg's percentage of total SCU, identifies the highest-SCU single leg
- NOT VIABLE contracts flagged with advice to abandon at the kiosk (no rep penalty)
- Legs within 2 SCU of each other shown as tied options for player to choose
- Ranking output: all contracts ordered by recommended-leg SCU descending
- Player workflow reminder output once per mode entry: accept -> load one leg -> deliver -> submit manually
- Mode exit: "exit rank mode", "back to scoring", or new session start

Created player/uploads/COVALEX_RANK_STRATEGY.md:
- Player-facing guide explaining the mechanic, payout tiers, and workflow
- Two-contract stacking instructions
- AI rank mode usage instructions with trigger phrase and output format
- Workflow checklist
- Notes on credits vs. rep trade-off, abandon-is-free rule, manual submit requirement, and capacity check reminder

Synced to all 7 SETUP files.

---

## Version 0.53.1: Session Capability Gaps

Five gaps identified from a live hauling session and addressed in the scoring instruction block:

1. Panel state display suppression strengthened. Added explicit language that suppression is the default after the first contract. A one-line running SCU total is permitted per contract; the full state table is not. "Suppress means suppress" added to rule text.

2. Capacity tracking added. At session start the AI asks the player for their confirmed in-game cargo capacity. Tracks combined SCU (LOADED + PENDING PICKUP) against that figure. Flags at 80% of confirmed capacity. Flags at or above confirmed capacity and blocks further assignments without override. If no capacity confirmed, shows running SCU total numerically for player self-monitoring.

3. Mixed commodity, same destination rule made explicit. Multiple commodities may share a panel if and only if all deliver to the same destination. Each commodity listed as a separate row with its own SCU and mission reference.

4. Scoring suspension toggle added to SESSION STATE. ACTIVE/SUSPENDED states with explicit player-triggered transitions. SUSPENDED state processes contract intake (extraction, overlap, panel assignment) but omits score recommendation. Does not auto-resume on route or issuer change. Acknowledges suspension state at each contract intake.

5. Timer urgency flag added to HOW TO RESPOND. When timer is 90 minutes or less AND total delivery stop count across accepted contracts is 3 or more, adds a one-line flag after the recommendation. Does not estimate travel time. Does not assess achievability. Flags the combination for player assessment only.

Synced to all 7 SETUP files.

---

## Version 0.52.1: Cargo Tracking Overhaul and Edge Case Guards

Full review of all AI-relevant files. Updated scoring instruction block, hull_b_covalex_route_playbook.md, and WHATS_NEW.md.

Extrapolated failure modes identified and guarded against:

1. Number format normalization: "4,608" = 4608, "1.5M" = 1500000, "50 SCU x 4 containers" = 200 SCU total. AI must normalize and confirm with player.

2. Screenshot reading limited to text fields: AI may not infer values from UI icons, color coding, progress bars, or background imagery. Non-text indicators must be UNRESOLVED.

3. Terminal scrolling: added explicit rule that a screenshot does not show all available contracts. Evidence of a partial list must be noted.

4. Same commodity, same destination, multiple contracts: tracked as separate rows per contract (one row per contract), not merged. Per-contract traceability required for SCU integrity.

5. Player-reported SCU vs contract SCU conflict: discrepancy must be flagged immediately and player asked to confirm.

6. Panel reassignment mid-session: all table rows referencing the reassigned panel must be updated. Stale references prohibited.

7. Dropped contract with loaded cargo: panels become ORPHANED status. Player is asked what happened to the cargo before state tables are updated.

8. Session start clears panel state: added explicit rule that panel assignments expire on session start, not just contract data. Player must declare pre-existing loaded panels before tracking continues.

9. Ship switch mid-session: panel assignments cleared, player asked to re-declare panel names for new ship, new ship modifiers applied immediately.

10. Output hygiene: added rule that responses must match the scope of the question. No unprompted state dumps, tips, or commentary beyond the specified response format.

Playbook update: updated "Cargo ledger" paragraph in hull_b_covalex_route_playbook.md to describe the current LOADED/PENDING PICKUP dual-table format, source-derived SCU totals, and explicit confirmation requirement.

WHATS_NEW.md: added v0.52.1 entry covering all changes since v0.50.1 with player-facing explanations and re-paste instruction.

Synced instruction block to all 7 SETUP files.

---

## Version 0.51.3: Cargo Panel Rules Expanded

Full rewrite of the CARGO PANEL TRACKING section in the scoring instruction block based on a live test session error log. Eight issues identified by the player were addressed:

1. One destination per panel added as a hard rule. AI must never propose mixing delivery destinations on a single panel.

2. Drop-before-pickup added as a hard routing rule. Panel reuse within a run (deliver then reload) must sequence delivery first, pickup second. Enforced without player prompting. Dependency flagged in state table every time the panel appears.

3. Destination overlap check added as a required step before proposing panel assignment on each new contract. Three outcome cases: full match (no new panels needed), partial match (N new destinations), no match (all new destinations). If no free panels remain, the AI must flag this explicitly.

4. Contract swap comparison table added. When proposing to drop one contract for another, show pickup, commodity, SCU, reward, and panel impact for both.

5. LOADED and PENDING PICKUP state tables are now mandatory separate tables. They must never be merged. A panel moves from PENDING PICKUP to LOADED only on explicit player confirmation -- screenshots do not count.

6. SCU integrity rule added. All SCU totals must be derived from source contract data at every update -- never incremented from a prior running total. Discrepancies between source-derived and prior totals must be flagged immediately.

7. Response format for contract intake standardized: (1) contract extraction, (2) overlap check, (3) panel assignment for this contract only. Full state table shown only on player request, conflict, or first contract of session. Column structure must not change during a session.

8. Route sequencing rules: drop-before-pickup enforced in output, SHARED STOP labels required for stops that are both delivery and pickup, surface stop ordering deferred to player.

Also added RETURNING to session phase list (PRE-DEPARTURE / IN-TRANSIT / AT-DESTINATION / RETURNING). Updated dead leg recalculation step to explicitly require source-derived totals, not increments.

Synced instruction block to all 7 SETUP files.

---

## Version 0.51.2: Cargo State Tracking Fix

Three errors identified from live Claude.ai testing of a Hull-B multi-pickup session:

1. Premature state advancement from screenshot evidence. AI treated a screenshot showing cargo visible on panels as confirmation that session contracts had been loaded. Added explicit rule: screenshots do not advance cargo state -- only player verbal confirmation does.

2. Missing pickup location in cargo ledger. The planned panel state table showed destination but not where a panel loads. Panels that load mid-route (picking up at an intermediate stop, not the departure point) were indistinguishable from panels loaded at departure. Changed planned panel state format from "[quadrant] | [commodity] | [SCU] | [destination]" to "[quadrant] | [commodity] | [SCU] | [loads at] | [delivers to]". Added rule that panels not loaded at departure are marked "loads mid-route at [location]".

3. Missing session phase tracking. AI lost track of whether the session was pre-departure, in-transit, or at a destination across a long context. Added explicit PRE-DEPARTURE / IN-TRANSIT / AT-DESTINATION phase field to SESSION STATE. Rule: do not reference events from a phase that has not been confirmed by the player.

Synced instruction block to all 7 SETUP files.

---

## Version 0.51.1: Hallucination Guard Expansion

Comprehensive review of all player-facing files and AI instruction content. Identified and fixed six categories of hallucination risk:

1. Atmosphere weight override invitation removed from GENERALIZED_HAULING_HANDBOOK.md. The handbook previously told players to ask their AI to "reduce the atmosphere penalty" -- an explicit invitation to invent scoring weights. Replaced with a note that ship atmosphere modifiers are already built in and the AI should not be asked to override them.

2. Scoring instruction block SHIP ADJUSTMENTS expanded from 4 ships to 19. Players on Hermes, Starlancer MAX, RAFT, Ironclad, Railen, C2/M2/A2 Hercules, Starfarer variants, Valkyrie, and Asgard previously got no ship-specific guidance. Added all tuned modifiers from scoring_config.json. Added "for unlisted ships, apply base weights and say so."

3. Non-flyable ship guard added to RULES section. Hull-D, Hull-E, Banu Merchantman, and Galaxy have full data profiles but are not yet in the game. New rule instructs the AI to refuse scoring for these ships and tell the player they are speculative placeholders.

4. Placeholder issuer guard added to RULES section and ISSUER ADJUSTMENTS. Hurston Dynamics, microTech, and ArcCorp are recognized by the OCR system but have no calibrated scoring modifiers. New rule instructs the AI to score these on base weights only and state this to the player. Also added to GENERALIZED_HAULING_HANDBOOK.md player copy.

5. Unrecognized location classification rule added to RULES section. If a delivery location cannot be identified as an orbital station or a surface location, the AI must ask the player rather than guessing. Addresses cases where planet surface landing zones (not in OCR aliases) might be misclassified.

6. Non-Hull-B cargo bay naming rule strengthened in CARGO PANEL TRACKING. Now explicitly requires the player to name each bay before tracking begins for any ship other than Hull-B. Prohibits constructing labels like "bay 1", "port bay", or "mid section" without player-supplied terms.

Also updated GENERALIZED_HAULING_HANDBOOK.md ship table to include all 19 flyable ships with tuned modifiers.

Synced scoring instruction block to all 7 SETUP files.

---

## Version 0.50.2: Atmosphere Rule Correction

Corrected the atmosphere location rule added in v0.50.1. The original rule was too broad ("never infer atmosphere status from training knowledge"). Replaced with an accurate rule: all stations are in space (orbital stations, Lagrange point stations, asteroid stations, space platforms) -- atmosphere landings only occur when delivering to a planet surface or moon surface. If all deliveries are to stations, the route is fully orbital. Ask the player only when the destination type is genuinely ambiguous.

---

## Version 0.50.1: Hallucination Guardrails Expanded

Added five new rule sections to the scoring instruction block (developer/templates/scoring_instruction_block.md), synced to all 7 SETUP files:

1. Atmosphere and congestion status: never infer from training knowledge; always player-reported or UNRESOLVED.
2. Ship cargo capacity: never state from training knowledge; player checks in-game loadout screen.
3. Travel time and profit-per-hour: explicitly prohibited as they are not scoring inputs.
4. CONTRACT READING section: AI must state how many complete contracts are visible before scoring, identify all fields (pickup, delivery, commodity, SCU, reward, fee), distinguish reward from fee for net profit calculation, and output UNRESOLVED for any unclear or cut-off field rather than gap-filling.
5. SESSION STATE section: session start message expires all prior contract data; contracts tracked as Available/Accepted/Delivered with player confirmation required for state transitions; dead legs and route order must be recalculated when the accepted set changes.

Updated player/WHATS_NEW.md with v0.50.1 entry explaining all five changes and instructing players to re-paste.

---

## Version 0.49.1: Cargo Panel Tracking Rules

Added CARGO PANEL TRACKING section to the scoring instruction block (developer/templates/scoring_instruction_block.md), synced to all 7 SETUP files. The section defines the Hull-B's 8 valid panel quadrant names (left/right x top/bottom x front/back), prohibits invented names with the same force as the no-invented-numbers rule, and requires a 4-state cargo ledger (required by contracts / planned panel state / observed loadout / variance) before every loading step. The response format for cargo tracking sessions is now standardised. Updated the Hull-B cargo panel section in both developer/hull_b_covalex_route_playbook.md and player/uploads/hull_b_covalex_route_playbook.md to replace vague panel terminology with the authoritative 8-quadrant vocabulary and added a cargo ledger explanation.

---

## Version 0.48.1: Inline Session Start Prompt in All SETUP Files

Added the session start prompt content inline to all seven SETUP files (SETUP_CHATGPT.md, SETUP_CLAUDE.md, SETUP_COPILOT.md, SETUP_GEMINI.md, SETUP_PERPLEXITY.md, SETUP_LMSTUDIO.md, SETUP_OTHER.md). Each file now has a "## Starting a session" section at the bottom containing the copy-pasteable session start block, the hallucination reset block, and tips -- players no longer need to open session_start_prompt.md separately. All references to session_start_prompt.md within the SETUP files were updated to point to the inline section.

---

## Version 0.47.1: Interactive Score Worksheet

Added developer/tools/score_worksheet.py. Interactive CLI tool that walks through scoring factors for a hauling route and produces a score, recommendation, and factor breakdown using the same deterministic scorer as the AI-assisted workflow. All prompts go to stderr so stdout is clean JSON when --json is used, making it safe to pipe. Fixed a display bug where the factor sign was printed twice (+{effect:+.1f} formatting). Added TestScoreWorksheet tests (test_json_output_accept, test_json_output_reject) to test_validators.py; total test count is now 191.

---

## Version 0.46.1: Player Changelog

Added player/WHATS_NEW.md. Plain-language release notes for players covering changes that affect their setup or scoring: 0.42.1 scoring completeness fix (two missing factors, UNRESOLVED cap), 0.41.x new platform guides and wording fixes, 0.38.1 ship expansion, and the original player folder introduction at 0.36.x. Distinct from DEVELOPMENT_HISTORY.md which is technical and developer-facing. Tells players specifically what to re-paste or reconfigure when they update.

---

## Version 0.45.1: Player Uploads Sync Tool

Added developer/tools/sync_player_uploads.py. Syncs the five player/uploads/ JSON files (scoring_config.json, OCR_normalization_rules.json, mission_issuer_profiles.json, mission_schema.json, ship_profiles.json) from their canonical developer sources. Each pair is compared ignoring the _copy_note field, which differs intentionally between canonical ("CANONICAL FILE") and player copy ("PLAYER COPY"). Running --check exits 1 if any copy differs from its canonical; --write updates all player copies while preserving their _copy_note. Added TestPlayerUploadsSync test and CI step in validation.yml.

---

## Version 0.44.1: Scoring Number Validator

Added developer/tools/validate_scoring_numbers.py. Reads scoring_config.json and the canonical scoring instruction template, then verifies that every numeric value in the template (base weights, score thresholds, modifier multipliers, and computed effective values like Covalex issuer alignment) matches the corresponding entry in the config. 23 checks covering all good factors, bad factors, score band thresholds, and key multipliers. Exits 1 on any mismatch or missing pattern. Added TestScoringNumbers test and a CI step in validation.yml. Any change to scoring_config.json weights that is not reflected in the template now fails the build immediately.

---

## Version 0.43.1: SETUP Sync Tool

Added developer/tools/sync_setup_scoring.py and developer/templates/scoring_instruction_block.md. The tool maintains a single canonical source for the scoring instruction block that appears identically in all seven player SETUP files. Running with --check verifies all files match the template (exits 1 if any differ); running with --write injects the canonical block into all files. Added a test (TestSetupSync.test_all_setup_files_match_template) and a CI step to validation.yml so any drift between the template and the SETUP files fails the build immediately. This directly prevents the class of bug that caused 0.42.1 (two scoring factors missing from all SETUP files because they were added to scoring_config.json but not propagated to the player docs).

---

## Version 0.42.3: README Maintainer Line Fix

Removed apeirogon.gg from the README.md footer maintainer line.

---

## Version 0.42.2: CI Requirements Hash Fix

Fixed requirements-dev.txt to include all transitive dependencies of pytest with their hashes. The file previously only specified a hash for pytest itself, which triggered pip's require-hashes mode. In that mode pip requires every package including transitive dependencies to have an explicit version pin and hash. The missing entries (iniconfig, pluggy, packaging, pygments) caused pip install to fail in any fresh environment (CI runner, new venv) with "In --require-hashes mode, all requirements must have their versions pinned with ==." This was the root cause of the validation workflow failing in CI on every push.

---

## Version 0.42.1: Scoring Completeness and Checksum Fix

Added two scoring factors missing from all seven player-facing SETUP files: cargo panel clarity (+8, with Hull-B modifier x1.15) and complex unloading sequence (-7). Added the UNRESOLVED field cap ("maximum -12 total") to the per-field penalty line, matching the actual scorer behaviour. Updated the Hull-B SHIP ADJUSTMENTS line to include the cargo panel clarity bonus explicitly. Fixed generate_release_checksums.py and verify_release_integrity.py to exclude __pycache__ directories and .pyc/.pyo files, making manifests portable across environments. Regenerated developer/releases/checksum_manifest.json with 27 clean entries; round-trip verification now reports valid: true with zero mismatches, missing, or untracked files.

---

## Version 0.41.8: Validation Workflow YAML Syntax Fix

Fixed a pre-existing YAML syntax error in validation.yml that caused "No jobs were run." Two run blocks used an unquoted inline python -c "..." construct with the Python code at column 1, which breaks YAML parsing. Collapsed each block to a single-line python -c call inside a pipe block scalar.

---

## Version 0.41.7: CI Workflow Working Directory Fix

Both GitHub Actions workflows (regression.yml and validation.yml) were failing because they ran python tools/ and pytest tests/ from the repo root, but all tooling lives under developer/. Added defaults: run: working-directory: developer to both jobs. Also updated the pip install step in validation.yml to reference ../requirements-dev.txt since that file sits at the repo root.

---

## Version 0.41.6: Scoring Instruction Accuracy Fixes

Fixed two misleading entries in the scoring instruction blocks across all seven SETUP files (Claude, ChatGPT, Gemini, Copilot, Perplexity, LM Studio, Other). Changed "Covalex issuer: +9 extra for alignment" to "Covalex issuer alignment: +9", removing "extra" which falsely implied a second additive bonus. Removed the "(x1.05 for Hull-B)" notation from the freight handling line since the effective value rounds to the same integer as the base, and the multiplier is already covered in the SHIP ADJUSTMENTS section. Findings from full project accuracy audit.

---

## Version 0.41.5: Remove Em and En Dashes Across All Docs

Removed all em dashes and en dashes from every markdown file in the repository (excluding third-party .claude/rules/ files). Replaced with commas, colons, periods, or rephrased sentences as appropriate. Fixed resulting sentence structure throughout.

---

## Version 0.41.4: README Wording Fix

Corrected "you open one panel" to "you focus one panel" in the Hull-B cargo placement example.

---

## Version 0.41.3: README What It Does Rewrite

Rewrote the "What it does" section in README.md to lead with concrete player outcome rather than scoring mechanics. New text explains cargo placement planning alongside contract selection, using the Hull-B panel assignment example (load by destination panel at the elevator, arrive at CRU-L1 and open one panel) to make the value immediately tangible to haulers.

---

## Version 0.41.2: ChatGPT No-Project Option Fix

Reframed SETUP_CHATGPT.md Option B from "Free account" to "No project / mobile app" to capture users on paid plans who don't use Projects and mobile app users where Projects may not be accessible. Added step to paste scoring_config.json content in Option B sessions to compensate for the absence of persistent file uploads.

---

## Version 0.41.1: New Player Setup Guides

Added dedicated setup guides for three additional AI platforms: `SETUP_COPILOT.md` (Microsoft Copilot: Notebook-based persistent instructions and free-tier paste workflow), `SETUP_PERPLEXITY.md` (Perplexity: paste-each-session with note on disabling search mode), and `SETUP_LMSTUDIO.md` (LM Studio and Ollama: local/offline AI with system prompt configuration, model recommendations, manual file paste workflow, and vision model notes). Updated `SETUP_OTHER.md` to reference the new dedicated guides. Updated README.md and player/README.md tables to list all seven AI options. Main README description updated to mention Copilot, Perplexity, LM Studio, and Ollama.

---

## Version 0.40.2: License Consolidation and Redundancy Cleanup

Removed four redundant files with no active references. License files consolidated: deleted `LICENSE_CODE.md` and `LICENSE_DATA.md`; their content is fully covered by `LICENSE` and `LICENSES.md`. Updated `LICENSE` to reference `LICENSES.md` instead of the deleted file. Removed two developer stub files (`developer/manual_copy_paste_workflow.md`, `developer/user_export_import_workflow.md`) whose content is superseded by comprehensive equivalents in `developer/docs/`. Removed three thin/redirect docs with no references (`OFFLINE_OPERATION_GUIDE.md`, `OFFLINE_OPERATIONAL_WORKFLOW.md`, `DETERMINISTIC_FALLBACK_HANDBOOK.md`). No functionality changed.

---

## Version 0.40.1: Lua Addon Framework (Functionality Stub)

Created `addon/` directory with a complete Lua 5.1 addon framework targeting CIG's future addon/plugin API. The architecture is fully designed and the deterministic scoring logic is implemented; all game API calls are clearly-marked placeholder stubs pending CIG's specification.

Added: `addon/ApeirogonLogistics.toc` (WoW-style manifest placeholder), `addon/lua/scoring_engine.lua` (complete: full deterministic scorer), `addon/lua/scoring_config.lua` (complete: Lua translation of `developer/runtime/scoring_config.json`), `addon/lua/utils.lua` (complete: shared helpers including minimal JSON encoder/decoder), `addon/lua/settings.lua` (stub: CIG_API placeholders), `addon/lua/contract_parser.lua` (stub: CIG_API placeholders), `addon/lua/ui_overlay.lua` (stub: SC_UI placeholders), `addon/lua/api_client.lua` (stub: Claude and OpenAI providers, non-blocking async pattern), `addon/lua/main.lua` (stub: event registration and /apl slash command). Added `addon/docs/ADDON_ARCHITECTURE.md` and `addon/docs/LUA_API_NOTES.md`. Updated main README and player README with future addon intent section.

---

## Version 0.39.1: Cargo Layout Specialization, Patch Tracking, and Addon Intent

Added Hull-B 8-panel cargo assignment doctrine (top/bottom/port/starboard/front/back) to both the route playbook and ship specialization guide. Added Hermes two-side-to-four-quadrant divider technique. Created PATCH_SENSITIVE_DATA.md: a structured checklist of data values that need re-verification on each new Star Citizen patch, including per-ship SCU risk levels, flyability flags, and files containing patch version references. Added future in-game addon intent to main README and player README, describing the planned real-time contract analyzer pending CIG addon/plugin support.

---

## Version 0.38.1: Ship Expansion and Covalex Reputation Ranks

Expanded ship coverage from 5 to 23 ships (all 90+ SCU haulers in Alpha 4.8.0): added Hull-D, Hull-E, Hermes, Starlancer MAX, Starlancer TAC, Starfarer, Starfarer Gemini, ARGO RAFT, Valkyrie, Asgard, M2 Hercules, A2 Hercules, Ironclad, Ironclad Assault, Railen, Banu Merchantman, RSI Galaxy. Added 19 new ship modifier blocks to scoring_config.json. Added full Covalex reputation ranks (7 tiers: Trainee through Master) to mission_issuer_profiles.json, with recommended ships, strategies, and Master-rank unlock list. Added 3 new issuer placeholders: Hurston Dynamics, microTech, ArcCorp. Created SHIP_SPECIALIZATION_GUIDE.md (developer and player copies). Added ship_profiles.json to player/uploads/. Updated all SETUP_*.md guides to list 8 upload files.

---

## Version 0.58.1: Audit Fixes and Player Content Update

Comprehensive content audit and player-facing documentation update.

**Instruction block changes:**
- Issue 9 fix: replaced fixed "how many contracts" run start question with dynamic capacity-based cap calculation. Run cap is now determined after viability analysis by summing minimum qualifying loads against confirmed capacity. Player confirms or reduces.
- EXAMPLE RESPONSE updated: replaced removed Port Olisar location with Hur-L2; em dashes replaced with double hyphens throughout.
- Covalex issuer alignment clarification added to ISSUER ADJUSTMENTS.
- All em dashes and en dashes replaced with double hyphens throughout.
- Synced to all 7 SETUP files.

**Player content updates:**
- `hull_b_covalex_route_playbook.md`: Port Olisar replaced with Hur-L2 throughout; COMBINED STOP handling section added; route table format documented; Covalex rank mode discovery note added.
- `session_start_prompt.md`: Port Olisar replaced with Hur-L2 in location example; rank mode trigger note added.
- `GENERALIZED_HAULING_HANDBOOK.md`: ship modifier table corrected -- added M2 fragmentation x1.08, C2 fragmentation x1.08, Asgard freight x1.03.
- `player/uploads/README.md`: COVALEX_RANK_STRATEGY.md added to uploads table.
- `player/WHATS_NEW.md`: player changelog updated with entries for v0.53.1 through v0.58.1.

**Developer housekeeping:**
- All 8 developer usage guides marked as legacy (old two-step JSON extraction workflow).
- Old validation reports (v0.30.5, v0.36.1) archived to `developer/validation/archive/`.

---

## Version 0.58.2: Grammar and Style Rules

Added grammar and style rules to CLAUDE.md and to the AI advisor's instruction block RULES section:

- "that" must always follow "ensure" and conjugations thereof.
- Oxford spelling with "ize" endings (organize, recognize, analyze, synchronize).
- No em dashes or en dashes -- double hyphens (--) for parenthetical breaks, plain hyphens (-) for ranges.

Synced to all 7 SETUP files.

---

## Version 0.59.1: Rep Grinding Ship Selection

Added ship selection logic to Covalex rank strategy mode based on operational constraints not captured by scoring modifiers.

Hard disqualifiers implemented (checked in order before run start):
1. Not flyable in Alpha 4.8: Hull-D, Hull-E, Galaxy, Banu Merchantman
2. Non-cargo primary role: A2 Hercules, Valkyrie, Starfarer, Starfarer Gemini, Starlancer TAC, Ironclad Assault
3. Station landing incompatibility when loaded: Hull-C
4. Ramp loading at freight elevators: C2/M2/A2 Hercules, Caterpillar, Starfarer, Starfarer Gemini, Valkyrie, Asgard, Ironclad Assault, Hermes, Starlancer MAX, Starlancer TAC, Freelancer MAX, Constellation Taurus

Ship verdicts: Hull-B (OPTIMAL), RAFT (NOT RECOMMENDED), Railen (UNCONFIRMED), Ironclad (UNCONFIRMED).

Verification prompt added for Railen and Ironclad: requires player to confirm freight elevator access, 16 SCU container compatibility, and pad availability at all 4 Covalex Senior destinations before approving for rep grinding.

Ship recommendation decision tree added: Hull-B first, Railen second (if verified), Ironclad third (if verified).

Scoring modifier suppression rule added: fragmentation penalty, stop density penalty, and cargo panel clarity bonus are not applied in rep grinding mode.

`loading_method` field added to all 23 ship records in `ship_profiles.json`: external_panel, external_pod, internal_ramp, external_panel_unconfirmed (Railen, Ironclad).

`COVALEX_RANK_STRATEGY.md` updated with ship selection section covering all disqualifiers, verdicts, and verification steps.

Synced to all 7 SETUP files.
