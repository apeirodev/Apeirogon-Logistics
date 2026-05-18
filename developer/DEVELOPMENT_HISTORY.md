# Apeirogon Logistics — Development History

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

## Phase 25 — Finalization

Platform finalised as a mature Star Citizen hauling intelligence platform.

Primary entry points at time of finalisation: `operational_handoff_guide.md`, `final_operational_playbook.md`, `final_reusable_prompt_library.md`, `canonical_future_maintenance_prompt.md`, `final_export_manifest.json`

---

## Public Enhancement Phase A

Extended for public open-source readiness.

Additions: operational doctrine rules, cargo panel assignment rules, patch lineage registry, telemetry submission workflows, contributor data standards, GitHub repository structure guidance, open-source governance guidance, route realism enrichment models.

---

## Phase 26 — Provider-Neutral Local-First Architecture

Platform explicitly declared local-first, provider-neutral, and addon-ready.

Key rules established: users bring their own AI provider or run locally; manual mode supported; deterministic fallback supported; future addon support optional and unimplemented.

---

## Version 0.28.1 — AI Provider Usability and Portable Persistence

Added provider-specific usage guides and portable persistence models.

Supported workflows: ChatGPT, Claude, Gemini, Microsoft Copilot, Perplexity, Ollama, LM Studio, OpenAI-compatible APIs, Anthropic-compatible APIs, manual copy/paste.

---

## Version 0.28.2 — Licensing Update

License unified to CC BY-NC 4.0 for all project assets: code, tooling, adapters, runtimes, datasets, prompts, schemas, documentation, and operational intelligence.

---

## Version 0.29.1 — Governance Alignment

Added architectural governance alignment materials for CSA CCM v4.1.0, CSA CAIQ v4.1.0, CSA AICM v1.0.3, and CSA AI CAIQ v1.0.2.

Added: provenance enforcement, telemetry trust tiers, AI output trust boundaries, contributor governance, threat models, shared responsibility models, governance metadata schema.

---

## Version 0.29.2 — Operational Hardening

Governance correction, operational realism hardening, deterministic fallback execution, contributor usability improvements, CI validation, provider-neutral operation.

---

## Version 0.29.3 — Operational Tooling Expansion

Expanded deterministic operational tooling, telemetry ingestion readiness, contributor onboarding, provider-neutral workflows, executable route-analysis tooling, CI/CD operational hardening.

---

## Version 0.30.1 — MVP Operational Platform Transition

Transitioned from specification-heavy scaffolding to a minimally viable executable operational platform.

Added: executable CLI tooling, telemetry ingestion workflows, governance metadata validation, deterministic operational route analysis, operational regression fixtures, release integrity structures, portable local operational workflows.

---

## Version 0.30.2 — Productionisation

Productionisation and placeholder elimination release.

---

## Version 0.30.5 — Rebuild Release

Rebuilt the failed 0.30.4 scope from verified 0.30.3. Version 0.30.4 is recorded as `abandoned_failed_run`.

See `CHANGELOG_0_30_5.md` for full details.

---

## Version 0.36.2 — Player Accessibility Release

Introduced the `player/` directory with AI-native workflow: per-platform setup guides (Claude, ChatGPT, Gemini, Other), session start prompt, and embedded scoring logic so players can get route recommendations from any AI assistant without installing Python. Reorganized repository so all technical and developer files live under `developer/`, leaving the root clean for non-technical users. Established Semantic Versioning (Major.Minor.Patch) as the project versioning standard.

---

## Version 0.36.2 — Star Citizen Patch Update

Set Star Citizen patch version to Alpha 4.8.0 across all canonical files: VERSION.json, patch_lineage_registry.json, example sessions and outputs, test fixtures, and documentation examples. Previous placeholder values (UNRESOLVED_REQUIRES_VALIDATION, UNRESOLVED, 4.x, 4.1, Alpha 3.23) replaced with the confirmed current patch.

---

## Version 0.37.1 — Player Uploads Folder

Added `player/uploads/` containing six files players upload to their AI project: scoring_config.json, OCR_normalization_rules.json, mission_schema.json, mission_issuer_profiles.json, hull_b_covalex_route_playbook.md (player-adapted), and GENERALIZED_HAULING_HANDBOOK.md (player-adapted). Four JSON files are exact copies; two markdown files have developer-specific sections replaced with the screenshot workflow. Cross-reference notes added to all canonical developer files. All four SETUP_*.md guides updated to reference player/uploads/.

---

## Version 0.38.1 — Ship Expansion and Covalex Reputation Ranks

Expanded ship coverage from 5 to 23 ships (all 90+ SCU haulers in Alpha 4.8.0): added Hull-D, Hull-E, Hermes, Starlancer MAX, Starlancer TAC, Starfarer, Starfarer Gemini, ARGO RAFT, Valkyrie, Asgard, M2 Hercules, A2 Hercules, Ironclad, Ironclad Assault, Railen, Banu Merchantman, RSI Galaxy. Added 19 new ship modifier blocks to scoring_config.json. Added full Covalex reputation ranks (7 tiers: Trainee through Master) to mission_issuer_profiles.json, with recommended ships, strategies, and Master-rank unlock list. Added 3 new issuer placeholders: Hurston Dynamics, microTech, ArcCorp. Created SHIP_SPECIALIZATION_GUIDE.md (developer and player copies). Added ship_profiles.json to player/uploads/. Updated all SETUP_*.md guides to list 8 upload files.
