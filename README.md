# Apeirogon Logistics

Provider-neutral, local-first hauling intelligence and operational analysis platform for Star Citizen.

Maintained by: ApeiroDev


# Star Citizen Hauling Dataset - Phase 1

Purpose: portable seed dataset for Hull-B Covalex hauling route optimisation.

This package contains canonical Stanton location records, source attribution, aliases, and initial derived operational scores. It is intentionally separated into sourced facts and derived hauling heuristics.

## Files

- `data/locations.json`: Canonical location records.
- `data/location_aliases.json`: Alias-to-location lookup table.
- `data/source_registry.json`: Source list and trust classification.
- `schema/location.schema.json`: JSON schema for location records.
- `docs/CHANGELOG.md`: Phase 1 changelog, assumptions, unresolved fields, and derived scores.

## Use

Import `locations.json` as the base node registry for later routing work. Do not treat derived operational fields as source facts. They are initial heuristics for Hull-B hauling optimization and should be validated during later phases.


## Phase 2 Additions

- `data/route_edges.json`: Topology-only route graph edges.
- `data/adjacency_matrix.json`: Expanded adjacency representation for traversal.
- `schema/route_edge.schema.json`: Route edge schema.
- `docs/CHANGELOG_PHASE2.md`: Phase 2 changelog.

QT time remains explicitly runtime-derived from quantum drive data and is not stored as a fixed edge value.


## Phase 3 Additions

- `data/hauling_penalties.json`
- `schema/hauling_penalty.schema.json`
- `docs/DERIVATION_RULES.md`
- `docs/KNOWN_ISSUES.md`
- `VERSION.json`

Phase 3 introduces derived operational hauling heuristics and classification models for Stanton logistics optimization.


## Phase 4 Additions

- `data/ship_profiles.json`
- `runtime/runtime_traversal_models.json`
- `schema/ship_profile.schema.json`
- `schema/runtime_traversal.schema.json`

Phase 4 introduces hauling ship operational profiles and runtime traversal modeling foundations.


## Phase 5 Additions

- `data/quantum_drive_profiles.json`
- `runtime/traversal_calculation_models.json`
- `schema/quantum_drive.schema.json`
- `schema/traversal_calculation.schema.json`

Phase 5 introduces quantum drive operational profiles and dynamic traversal modeling foundations.


## Phase 6 Additions

- `data/mission_batches.json`
- `runtime/screenshot_ingestion_rules.json`
- `runtime/OCR_normalization_rules.json`
- `runtime/mission_extraction_pipeline.json`

Phase 6 introduces mission ingestion structures, OCR normalization rules, and screenshot extraction foundations.


## Phase 7 Additions

- `analytics/route_scoring_models.json`
- `analytics/mission_chain_models.json`
- `runtime/route_optimization_engine.json`
- `analytics/mission_acceptance_rules.json`
- `analytics/hauling_strategy_profiles.json`

Phase 7 introduces route optimization, mission scoring, and hauling strategy engines.


## Phase 8 Additions

- `analytics/historical_mission_patterns.json`
- `analytics/continuation_probability_models.json`
- `analytics/adaptive_route_prediction_models.json`
- `analytics/mission_density_heatmaps.json`
- `analytics/hauling_behavior_learning_rules.json`

Phase 8 introduces historical mission-learning and adaptive route prediction foundations.


## Phase 9 Additions

- `runtime/live_mission_ingestion_runtime.json`
- `analytics/persistent_mission_memory.json`
- `analytics/cross_session_analytics_models.json`
- `analytics/adaptive_player_profile_models.json`
- `schema/mission_history_log.schema.json`

Phase 9 introduces persistent mission memory and cross-session adaptive analytics foundations.


## Phase 10 Additions

- `runtime/live_route_execution_engine.json`
- `runtime/mission_state_machine_models.json`
- `runtime/automated_route_simulation_models.json`
- `runtime/live_recommendation_adaptation_models.json`
- `schema/execution_event_log.schema.json`

Phase 10 introduces live execution state engines and probabilistic automated route simulation.


## Phase 11 Additions

- `analytics/fleet_coordination_models.json`
- `analytics/multiplayer_hauling_orchestration.json`
- `analytics/cooperative_route_distribution_models.json`
- `analytics/convoy_risk_models.json`
- `schema/fleet_event_log.schema.json`

Phase 11 introduces distributed fleet coordination and cooperative hauling orchestration.


## Phase 12 Additions

- `analytics/commodity_flow_models.json`
- `analytics/economic_forecasting_models.json`
- `analytics/intersystem_route_models.json`
- `analytics/regional_supply_pressure_models.json`
- `schema/commodity_event_log.schema.json`

Phase 12 introduces economic forecasting and inter-system logistics expansion.


## Phase 13 Additions

- `analytics/autonomous_hauling_agent_models.json`
- `analytics/logistics_delegation_models.json`
- `analytics/distributed_operational_planning_models.json`
- `analytics/adaptive_convoy_command_models.json`
- `schema/autonomous_event_log.schema.json`

Phase 13 introduces autonomous logistics delegation and distributed operational planning systems.


## Phase 14 Additions

- `analytics/strategic_logistics_governance_models.json`
- `analytics/alliance_scale_coordination_models.json`
- `analytics/persistent_economic_campaign_models.json`
- `analytics/macro_supply_chain_resilience_models.json`
- `schema/strategic_event_log.schema.json`

Phase 14 introduces alliance-scale strategic logistics governance and persistent economic campaign systems.


## Phase 15 Additions

- `analytics/galactic_logistics_simulation_models.json`
- `analytics/sovereignty_influence_models.json`
- `analytics/geopolitical_hauling_analysis_models.json`
- `analytics/strategic_corridor_control_models.json`
- `schema/geopolitical_event_log.schema.json`

Phase 15 introduces galactic-scale logistics and geopolitical hauling simulation systems.


## Phase 16 Additions

- `analytics/civilization_scale_logistics_ecosystems.json`
- `analytics/autonomous_faction_simulation_models.json`
- `analytics/transregional_equilibrium_models.json`
- `analytics/strategic_civilization_resilience_models.json`
- `schema/civilization_event_log.schema.json`

Phase 16 introduces civilization-scale logistics ecosystem simulation and autonomous faction equilibrium systems.


## Phase 17 Additions

- `analytics/post_scarcity_logistics_models.json`
- `analytics/synthetic_economy_simulation_models.json`
- `analytics/galactic_equilibrium_recovery_models.json`
- `analytics/strategic_repopulation_models.json`
- `schema/synthetic_event_log.schema.json`

Phase 17 introduces synthetic recovery systems and post-scarcity logistics modeling.


## Phase 17 Repair 0.17.1

Validated Phase 17 artefacts, regenerated only missing files, preserved version lineage, and incremented package version to `0.17.1`.


## Phase 18 Additions

- recursive self-healing logistics systems
- galactic governance balancing
- equilibrium preservation architectures
- adaptive entropy suppression
- recursive stability feedback loops


## Phase 19 Additions

- operational packaging
- validation hardening
- export readiness
- practical Hull-B Covalex route-analysis guidance


## Phase 20 Additions

- live operational integration
- screenshot workflow optimization
- continuous operational learning
- practical Hull-B hauling assistance


## Phase 21 Additions

- execution telemetry models
- real session analytics
- adaptive operational refinement
- mission chain telemetry
- practical Hull-B telemetry logging


## Phase 22 Additions

- telemetry calibration systems
- practical route-score tuning
- observed Hull-B performance baselines
- observed route-quality analysis
- telemetry calibration logging


## Phase 23A Additions

- statistical calibration
- telemetry variance modeling
- comparative ship-efficiency analytics
- patch-regression detection
- operational anomaly detection
- telemetry retention policy
- heuristic decay modeling


## Phase 24B Additions
- generalized hauling intelligence
- issuer profiles
- multi-ship operational modeling
- hauling archetypes


## Phase 25 Finalization

This package has been finalized as a mature Star Citizen hauling intelligence platform.

Primary entry points:
- `operational_handoff_guide.md`
- `final_operational_playbook.md`
- `final_reusable_prompt_library.md`
- `canonical_future_maintenance_prompt.md`
- `final_export_manifest.json`

Final operating rule:
Use this as an operational logistics-analysis platform, not as an authoritative source for volatile runtime gameplay values.


## Public Enhancement Phase A

This package has been extended for public open-source readiness.

Key public-facing additions:
- operational doctrine rules
- cargo panel assignment rules
- patch lineage registry
- telemetry submission workflows
- contributor data standards
- GitHub repository structure guidance
- open-source governance guidance
- route realism enrichment models

Public project rule:
Contributors must preserve sourced facts, telemetry, heuristics, OCR uncertainty, and runtime-dependent values as separate classes of information.


## Phase 26 Provider-Neutral Local-First Architecture

The platform is now explicitly local-first, provider-neutral, and addon-ready.

Key rules:
- Users bring their own AI provider or run locally.
- Manual mode remains supported.
- Deterministic fallback remains supported.
- Future addon support is optional and unimplemented until official capabilities exist.
- Telemetry contribution is opt-in.


## Version 0.28.1 AI Provider Usability and Portable Persistence

This release adds provider-specific usage guides and portable persistence models.

Supported workflows:
- ChatGPT
- Claude
- Gemini
- Microsoft Copilot
- Perplexity
- Ollama
- LM Studio
- OpenAI-compatible APIs
- Anthropic-compatible APIs
- manual copy/paste

Key rule:
User data must persist outside AI chat memory through portable JSON profile and session state files.


## Version 0.28.2 Licensing Update

Licensing is now split by asset type.

### CC BY-NC 4.0
Applies to:
- datasets
- prompts
- schemas
- documentation
- telemetry models
- operational doctrine
- analytical intelligence

### MIT
Applies to:
- tooling
- adapters
- runtimes
- utilities
- future addon/plugin code

Commercial use of the operational intelligence platform or dataset is prohibited without permission.


## Public Project Identity

- Project: Apeirogon Logistics
- GitHub Organization Recommendation: Apeirogon
- Maintainer Identity: ApeiroDev
- Domain: apeirogon.gg

## Project Positioning

Apeirogon Logistics is designed as:
- a local-first operational analysis platform
- a provider-neutral AI workflow system
- a telemetry-aware hauling intelligence framework
- a future addon-ready logistics platform

It is explicitly not:
- a botting framework
- an automation platform
- an anti-cheat bypass tool
- a gameplay injection system


## Version 0.29.1 Governance Alignment

Apeirogon Logistics now includes architectural governance alignment materials for:

- CSA CCM v4.1.0
- CSA CAIQ v4.1.0
- CSA AICM v1.0.3
- CSA AI CAIQ v1.0.2

This project does **not** claim certification or formal compliance.

The governance layer adds:
- provenance enforcement
- telemetry trust tiers
- AI output trust boundaries
- contributor governance
- threat models
- shared responsibility models
- continuous control monitoring readiness
- governance metadata schema


## 0.29.2 Operational Hardening

This release focuses on:
- governance correction
- operational realism
- deterministic fallback execution
- contributor usability
- CI validation
- provider-neutral operation

The platform is telemetry-ready, not yet telemetry-calibrated at scale.


## 0.29.3 Operational Tooling Expansion

This release expands:
- deterministic operational tooling
- telemetry ingestion readiness
- contributor onboarding
- provider-neutral workflows
- executable route-analysis tooling
- CI/CD operational hardening

The platform now includes executable deterministic fallback tooling and reproducible operational examples.


## 0.30.1 MVP Operational Platform Transition

This release transitions Apeirogon Logistics from specification-heavy scaffolding into a minimally viable executable operational platform.

Key additions:
- executable CLI tooling
- telemetry ingestion workflows
- governance metadata validation
- deterministic operational route analysis
- operational regression fixtures
- release integrity structures
- portable local operational workflows

The platform remains:
- provider-neutral
- offline-capable
- deterministic-fallback-capable
- telemetry-ready rather than telemetry-authoritative


## Version 0.30.2
Productionization and placeholder elimination release.

## 0.30.5 Rebuild Release

0.30.5 rebuilds the failed 0.30.4 scope from the verified 0.30.3 package.

0.30.4 is recorded as `abandoned_failed_run`.

This release provides functional deterministic local tooling for:
- route scoring
- route-chain analysis
- telemetry validation
- OCR text normalization
- provider-output validation
- governance metadata validation
- replay/audit reconstruction
- release checksum generation
- schema and manifest inspection

Remaining limitations:
- no real telemetry baselines
- no telemetry-calibrated scoring
- no hard OCR engine dependency
- no provider runtime adapters
