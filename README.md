# Apeirogon Logistics

Provider-neutral, local-first, deterministic operational intelligence platform for Star Citizen hauling gameplay.

**Maintainer:** ApeiroDev  
**Domain:** apeirogon.gg  
**Version:** 0.30.5  
**Status:** Stable pre-release — deterministic toolkit  

---

## What This Is

Apeirogon Logistics is a reproducible operational workflow framework and hauling-analysis toolkit for Star Citizen. It is built around the principle that operational intelligence should be explainable, auditable, and functional without any cloud service, AI provider, or external dependency.

The platform exists because:

- Star Citizen hauling gameplay is operationally complex
- Existing tools are fragmented or simplistic
- AI-assisted tooling is usually provider-locked
- Most solutions assume hosted SaaS architectures
- AI systems regularly hallucinate operational details
- Telemetry quality in community tools is ungoverned
- Players need reproducible, explainable route recommendations
- Offline and deterministic workflows are strategically important

This is not a calculator or a route optimizer. It is:

- a reproducible operational workflow framework
- a deterministic hauling-analysis toolkit
- a telemetry-ready intelligence platform
- a provider-neutral AI orchestration layer
- a governance-aware operational analysis system
- a future addon-compatible architecture layer
- a portable operational state framework

## What This Is Not

- a botting framework
- an automation platform
- an anti-cheat bypass tool
- a gameplay injection system
- a cloud service or SaaS product
- a tool that claims calibration it does not have

---

## Core Principles

### Deterministic-First

AI is optional. The platform is fully functional offline, without OCR, without telemetry, without cloud APIs, and without any AI provider. Deterministic tooling is the authoritative operational baseline. AI-assisted analysis is advisory only.

### Provider Neutrality

The project never depends on any specific AI provider. All provider support is abstracted. Users may bring their own API keys, use local inference, use manual copy/paste workflows, or run in fully deterministic mode.

Supported workflows: ChatGPT, Claude, Gemini, Microsoft Copilot, Perplexity, Ollama, LM Studio, OpenAI-compatible APIs, Anthropic-compatible APIs, manual copy/paste, and deterministic-only operation.

### Local-First Operation

All operational workflows function locally. Local telemetry storage, replay, validation, OCR preprocessing, schema validation, route analysis, and governance validation are all supported without cloud connectivity.

### Governance-Aware Architecture

The project is architecturally informed by CSA CCM v4.1.0, CSA CAIQ v4.1.0, CSA AICM v1.0.3, and CSA AI CAIQ v1.0.2.

This project does **not** claim certification, compliance, STAR submission, or audit attestation.

Governance exists to preserve operational trustworthiness, contain hallucinations, enforce provenance, separate heuristics from sourced facts, and improve reproducibility. It is not bureaucratic theatre.

---

## Current Capabilities (v0.30.5)

### Deterministic Route Analysis

- weighted route scoring
- burden modelling
- fragmentation modelling
- dead-leg analysis
- stop-density penalties
- unloading burden modelling
- issuer modifiers
- ship modifiers
- sustainability scoring
- chain continuity scoring

### Governance Metadata System

Every operational output includes:

- `source_class` — sourced fact, telemetry, heuristic, AI output, etc.
- `provenance_chain`
- `confidence_level`
- `verification_status`
- `patch_era`
- `telemetry_support_level`
- `unresolved_field_list`
- `contributor_trust_tier`
- `operational_assurance_state`
- `derivation_type`

### Replay and Auditability

- deterministic replay
- replay verification
- provenance reconstruction
- audit reconstruction
- replay manifests
- reproducibility hashing

### Schema and Validation System

- recursive schema validation
- manifest validation
- governance validation
- unresolved-field validation
- replay validation
- metadata propagation validation

### OCR Support

OCR providers are abstracted and optional. The platform supports text normalisation without a hard OCR engine dependency. Supported providers when available: Tesseract, PaddleOCR, EasyOCR, cloud OCR providers, AI vision providers, and manual text input.

All OCR output includes: OCR provider, preprocessing profile, confidence score, unresolved fields, extraction timestamp, patch version, source image hash, and normalisation lineage.

### Portable User State

- portable user profiles
- hauling session states
- export/import workflows
- local JSON persistence

AI memory is convenience only and never required. Portable profiles are the authoritative user state.

### Executable CLI Tooling (v0.30.5)

- `tools/route_scorer.py` — deterministic route scoring
- `tools/route_chain_analyzer.py` — multi-stop chain analysis
- `tools/telemetry_validator.py` — telemetry ingestion and trust classification
- `tools/ocr_normalizer.py` — OCR text normalisation without hard OCR dependency
- `tools/provider_output_validator.py` — AI provider output validation
- `tools/governance_validator.py` — governance metadata validation
- `tools/replay_tool.py` — replay and audit reconstruction
- `tools/verify_release_integrity.py` — release checksum generation
- `tools/inspect_schema.py` — schema and manifest inspection

---

## Known Limitations

The platform is honest about what it does not yet have:

- no real telemetry baselines
- no telemetry-calibrated scoring
- no hard OCR engine dependency
- no provider runtime adapters
- no addon/API integration (future architecture only)
- no certification or compliance claim

The platform is **telemetry-ready**, not telemetry-calibrated.

---

## Star Citizen Operational Context

Current operational specialisation:

- Hull-B operational doctrine
- Covalex hauling optimisation
- multi-stop hauling
- fragmented cargo handling
- unloading burden analysis
- freight elevator burden modelling
- orbital-loop operational continuity

The platform also supports generalised hauling operations beyond Hull-B specialisation.

---

## Non-Negotiable Operational Rules

**Source separation** — sourced facts, OCR extractions, telemetry observations, user corrections, derived heuristics, runtime-derived values, AI-generated outputs, governance metadata, and contributor-submitted content are never silently merged.

**Unresolved values** — unreadable, uncertain, incomplete, or ambiguous values remain unresolved. The system never invents values, infers unreadable OCR fields, fabricates telemetry, or silently fills blanks. Unresolved data is operationally preferable to fabricated certainty.

**AI outputs** — always advisory, probabilistic, schema-validated, provenance-tagged, and confidence-tagged. AI outputs never overwrite sourced facts.

**Telemetry** — observational, probabilistic, trust-tiered, patch-version segmented, and provenance-tracked. Never treated as absolute truth.

---

## Trust Tier Model

| Tier | Meaning |
|------|---------|
| T0 | Raw unverified |
| T1 | User verified |
| T2 | Multi-user corroborated |
| T3 | Maintainer validated |
| T4 | Patch baselined |

---

## Getting Started

See `docs/GETTING_STARTED.md` for setup and first-run instructions.

See `docs/QUICK_START.md` for an abbreviated guide.

For Hull-B Covalex operations: `hull_b_covalex_route_playbook.md`

For AI provider integration: see the usage guides in `docs/` for your provider.

For offline/deterministic-only operation: `docs/OFFLINE_OPERATION_GUIDE.md`

---

## Licensing

**CC BY-NC 4.0** — all project contents: code, tooling, schemas, datasets, operational intelligence, heuristics, doctrine, prompts, and documentation.

Attribution required. Commercial use prohibited without explicit permission. See `LICENSE` and `LICENSES.md`.

---

## Development History

The phase-by-phase construction history of this project is recorded in `DEVELOPMENT_HISTORY.md`.

Release changelogs: `CHANGELOG_0_30_5.md`, `CHANGELOG_0_30_2.md`, `CHANGELOG_0_30_1.md`, `CHANGELOG_0_29_3.md`, `CHANGELOG_0_29_2.md`

---

## Contributing

See `CONTRIBUTING.md` and `docs/PUBLIC_CONTRIBUTOR_GUIDE.md`.

Contributors must preserve sourced facts, telemetry, heuristics, OCR uncertainty, and runtime-dependent values as separate classes of information. See `CONTRIBUTOR_TRUST_MODEL.md`.
