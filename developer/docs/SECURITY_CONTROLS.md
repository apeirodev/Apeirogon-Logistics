# Security Controls and Governance Alignment

**Version:** 0.62.1
**Date:** 2026-05-25
**Scope:** Apeirogon Logistics Python tool suite (developer/tools/)

---

## Architecture Summary

Apeirogon Logistics is a Python-first, local-first, JSON-centric hauling advisor for Star Citizen.

**Trust boundaries:**

1. **User-supplied CLI input** -- file paths via --input/--output, batch JSON, OCR text
2. **AI provider output** -- structured JSON responses from Claude, ChatGPT, Gemini, Ollama, etc.
3. **OCR extraction output** -- structured text extracted from game screenshots (potentially adversarial)
4. **Telemetry input** -- player-submitted JSON records, unvalidated until ingested
5. **Internal deterministic tools** -- fully trusted Python code in developer/tools/

**What this system does:**
- Reads user-supplied JSON (route descriptions, mission batches, telemetry) from stdin or file
- Optionally passes sanitized fields to external AI providers for advisory analysis
- Runs a deterministic scoring engine on all inputs
- Writes scored JSON to stdout or a user-supplied output path
- Generates and verifies release checksums
- Has NO web server, NO database, NO user authentication, NO multi-user model

**Primary risk surface:**
- File path traversal via CLI --output/--input arguments (FILE-01)
- Hallucination amplification when AI-invented numeric values are passed downstream (AI-03, AI-04)
- Prompt injection via user-supplied contract data sent to AI providers (LLM01)
- Provenance loss if AI output is persisted without governance metadata (ASI02, ASI10)
- Supply chain attacks via unpinned Python dependencies (SC-01)

---

## Applicable Standards

| Standard | Version | Coverage |
|----------|---------|----------|
| CSA CCM | v4.0 | Cloud Controls Matrix (applicable domains only) |
| CSA AICM | draft 2025 | AI Controls Matrix (applicable domains only) |
| OWASP ASVS | v4.0 | Application Security Verification Standard |
| OWASP Top 10 | 2025 | Web application risks (limited applicability) |
| OWASP LLM Top 10 | v2.0 2025 | LLM application risks |
| OWASP Top 10 for Agentic Apps | 2026 draft | Agentic AI risks |
| MITRE ATLAS | current | Adversarial ML threats |
| NIST AI RMF | 1.0 | AI risk management |

---

## Scope Limitations

The following domains and controls are **not applicable** to this codebase and should not generate findings:

| Domain | Reason |
|--------|--------|
| CCM IAM (Identity and Access Management) | No user accounts, no authentication |
| CCM BCR (Business Continuity) | Local-first tool with no uptime requirements |
| CCM CEK (Cryptography and Key Management) | No encryption at rest, no user-managed keys |
| CCM CCC (Change Control and Configuration) | Managed by git, not a cloud control |
| CCM IVS (Infrastructure and Virtualization) | No cloud infrastructure |
| OWASP A07 Authentication Failures | No user authentication system |
| OWASP A01 Broken Access Control | No multi-user access model |
| OWASP A04 Cryptographic Failures (passwords) | No user accounts |
| OWASP A06 Insecure Design (web threat modeling) | No web server |
| CSA AICM AI-FED (Federated Learning) | Not applicable |
| CSA AICM AI-PRI (Privacy) | No PII collected or stored |

---

## Implemented Controls

| Control ID | Standard | Description | Implementation | File/Location |
|------------|----------|-------------|----------------|---------------|
| FILE-01 | CLAUDE.md, OWASP A01 | File path traversal prevention | `safe_write_path()` validates all user-supplied output paths against allowed roots. `dump_json()` calls `safe_write_path()` on every non-stdout write. | `developer/tools/lib/common.py: safe_write_path(), dump_json()` |
| FILE-02 | CLAUDE.md, OWASP A08 | No pickle deserialization | All deserialization uses `json.loads()` / `json.load()`. `pickle` is not imported anywhere in the codebase. | All tools in `developer/tools/` |
| FILE-03 | CLAUDE.md, OWASP A05 | No shell interpolation | No `os.system()`, `subprocess` with `shell=True`, or `eval()` calls anywhere. Bandit SAST confirmed zero findings. | Bandit scan result, all tools |
| AI-01 | CLAUDE.md, NIST AI RMF | AI outputs are always advisory | `provider_output_validator.py` rejects any output where `advisory_only` is not `True`. `governance_metadata()` defaults `advisory_only=True`. | `developer/tools/provider_output_validator.py`, `developer/tools/lib/common.py` |
| AI-02 | CLAUDE.md, OWASP LLM02 | Sanitize provider outputs | `OCR_result_normalizer.py` flags injection-pattern text on both paths and sanitizes provider string fields in `_normalise_mission()` (control characters stripped, length bounded), ensuring that vision output is cleaned before downstream use. | `developer/tools/OCR_result_normalizer.py: normalize_ocr(), _normalise_vision(), _sanitize_provider_value()` |
| AI-03 | CLAUDE.md, OWASP LLM09 | Hallucination guardrails | `HALLUCINATION_RISK_FIELDS` defined; `_flag_hallucination_risk()` checks all numeric fields in provider output against user-supplied fields. | `developer/tools/provider_output_validator.py` |
| AI-04 | CLAUDE.md, OWASP LLM09 | Reject unsourced numeric fields | `validate()` sets `hallucination_flags` in output for all numeric fields not present in user-supplied input. | `developer/tools/provider_output_validator.py: validate()` |
| INT-01 | CLAUDE.md, OWASP A03 | Release artefact integrity | SHA-256 checksums generated by `generate_release_checksums.py`, verified by `verify_release_integrity.py`. All comparisons use `hmac.compare_digest`. | `developer/tools/generate_release_checksums.py`, `developer/tools/verify_release_integrity.py` |
| INT-02 | CLAUDE.md, SC-01 | Hash-pinned dependencies | `requirements-dev.txt` pins all packages to exact versions with SHA-256 hashes; `pip install --require-hashes` enforced in CI. | `requirements-dev.txt`, `.github/workflows/validation.yml` |
| ERR-01 | CLAUDE.md, OWASP A10 | Fail closed on validation error | `validate_governance_metadata()` wraps inner logic in try/except; any exception returns `(False, ["validation_error_fail_closed"])`. | `developer/tools/lib/common.py: validate_governance_metadata()` |
| ERR-02 | CLAUDE.md, OWASP A02 | No internal path/stack trace in output | `local_OCR_preprocessor.py` logs full exception to stderr via `logger.error()` and returns only `"invalid image path"` in JSON output. `schema_validator.py` returns `"validation error"` string in JSON. | `developer/tools/local_OCR_preprocessor.py`, `developer/tools/schema_validator.py` |
| LOG-01 | CLAUDE.md, OWASP A09 | No API keys in logs | `bundle_telemetry.py` redacts `STRIP_KEYS` containing `api_key`, `token`, `secret`, `password`, `credential`, `key` before bundling. | `developer/tools/bundle_telemetry.py: _sanitize_record()` |
| SRC-01 | CLAUDE.md, NIST AI RMF | Source separation | AI outputs are always stored in `ai_recommendation` or `governance_metadata` with `source_class="ai_output"` or `"ai_vision_extraction"`, never merged into `sourced_facts`. | `developer/tools/provider_output_validator.py`, `developer/tools/OCR_result_normalizer.py` |
| WARN-02 | CLAUDE.md | 10 MB input size cap | `load_json()` routes every named file path through `safe_load_json()`, which checks `st_size` before reading and raises `ValueError` for oversized files, ensuring that the cap applies at all tool entry points. `bundle_telemetry.py` enforces `_MAX_FILE_BYTES` per file. | `developer/tools/lib/common.py: load_json(), safe_load_json()`, `developer/tools/bundle_telemetry.py` |
| WARN-03 | CLAUDE.md | hmac.compare_digest for hashes | All hash comparisons use `hmac.compare_digest()`. See `replay_route_analysis.py`, `verify_release_integrity.py`, `verify_replay_integrity.py`. | Multiple tools |
| SC-05 | supply-chain-python.md | SHA-pinned GitHub Actions | Both workflow files pin all `uses:` references to full commit SHAs. | `.github/workflows/validation.yml`, `.github/workflows/regression.yml` |
| SC-06 | supply-chain-python.md | Minimal GITHUB_TOKEN permissions | Both workflows declare `permissions: contents: read` at top level. | `.github/workflows/validation.yml`, `.github/workflows/regression.yml` |
| LLM01 | owasp-llm.md | Prompt injection detection | `OCR_result_normalizer.py` checks for `ignore previous` and `system prompt` in OCR text and appends a warning. | `developer/tools/OCR_result_normalizer.py: normalize_ocr()` |
| ASI01 | owasp-agentic.md | Goal and instruction hijacking | Structural validation required before any agent step uses external data. `validate_governance_metadata()` validates all persisted output. | `developer/tools/lib/common.py`, `developer/tools/validate_governance_metadata.py` |
| ASI08 | owasp-agentic.md | Overreliance on AI output | `STRICT_AI_SESSION_PROMPT.md` instructs users to never allow AI to invent numeric values; `advisory_only=True` enforced on all AI outputs. | `player/uploads/STRICT_AI_SESSION_PROMPT.md`, `developer/tools/provider_output_validator.py` |
| SC-02 | supply-chain-python.md | pip-audit in CI | `validation.yml` runs `pip-audit` against `requirements-dev.txt` on every push and pull request. pip-audit itself is hash-pinned in the requirements file. | `.github/workflows/validation.yml` |

---

## Partially Implemented Controls

| Control ID | Standard | Description | Gap | File/Location |
|------------|----------|-------------|-----|---------------|
| WARN-01 | CLAUDE.md | JSON schema validation before processing | Most tools call `load_json()` and immediately process without validating against a JSON schema. `schema_validator.py` exists but is not called inline by other tools. | All tools that call `load_json(args.input)` |
| WARN-02 (stdin) | CLAUDE.md | 10 MB cap on stdin | `safe_load_json()` enforces the cap for file inputs. No cap exists for stdin (`load_json()` with path=None). Practical impact is low since stdin is typically used with small inputs in a pipeline. | `developer/tools/lib/common.py: load_json()` |
| ASI10 | owasp-agentic.md | Audit trail for all written output | Tools write output with `governance_metadata` (which includes a `provenance_chain`). However, the `_audit` block with `session_id` and `written_at` described in ASI10 is not universally applied. | All tools writing JSON to disk |
| SC-03 | supply-chain-python.md | SBOM on release | No SBOM is generated on release. `generate_release_checksums.py` covers file hashes but not dependency inventory. | `developer/tools/generate_release_checksums.py` |

---

## Non-Applicable Controls

| Control | Standard | Rationale |
|---------|----------|-----------|
| CSA CCM IAM-01 through IAM-14 | CCM v4.0 | No user authentication or identity management |
| CSA CCM BCR-01 through BCR-11 | CCM v4.0 | Local-only tool; no availability requirements |
| CSA CCM CEK-01 through CEK-20 | CCM v4.0 | No encryption at rest or key management |
| OWASP A07 Authentication | OWASP 2025 | No authentication system |
| OWASP LLM08 Vector and Embedding Weaknesses | OWASP LLM 2025 | No vector store or RAG pipeline |
| OWASP ASI09 Multi-Agent Escalation | OWASP Agentic 2026 | Single-session architecture; no agent spawning |
| CSA AICM AI-FED | AICM draft 2025 | No federated learning |
| CSA AICM AI-PRI | AICM draft 2025 | No PII collected or stored |
| MITRE ATLAS AML.T0019 (White-Box Access) | ATLAS | Scoring weights are intentionally public |

---

## CSA CCM/AICM Applicable Domain Summary

### CCM: Applicable Domains

| Domain | CCM Code | Assessment |
|--------|----------|------------|
| Application and Interface Security | AIS | Partially implemented -- FILE-01/02/03 controls present; JSON schema validation (WARN-01) partially met |
| Data Security and Information Lifecycle | DSI | Partially implemented -- source separation (SRC-01) enforced; no data encryption |
| Governance, Risk and Compliance | GRC | Partially implemented -- CLAUDE.md defines policy; no formal risk register |
| Security Incident Management | SEF | Not formally implemented -- no incident response process for a local-only tool |
| Supply Chain Management | STA | Partially implemented -- hash-pinned deps (SC-01), SHA-pinned Actions (SC-05); no SBOM (SC-03 gap) |
| Threat and Vulnerability Management | TVM | Partially implemented -- Bandit SAST and pip-audit run manually; not automated in CI |

### AICM: Applicable Domains

| Domain | AICM Code | Assessment |
|--------|-----------|------------|
| AI Governance | AI-GOV | Partially implemented -- CLAUDE.md formalizes advisory-only requirement; no formal model card |
| Data Risk and Security | AI-DRS | Partially implemented -- source class separation (SRC-01) enforced; input validation (WARN-01) partial |
| Model Integrity and Security | AI-MIS | Partially implemented -- scoring weights are integrity-checked via release checksums (INT-01); no model card |
| Operational Resilience and Safety | AI-ORS | Partially implemented -- hallucination guardrails (AI-03/04) and STRICT_AI_SESSION_PROMPT limit operational risk |
| Auditability and Explainability | AI-AUD | Partially implemented -- governance_metadata with provenance_chain on all output; no formal audit log |

---

## Identified Gaps and Residual Risks

| Risk | Severity | Current Mitigation | Recommended Action |
|------|----------|---------------------|-------------------|
| WARN-01: No inline JSON schema validation before processing user inputs | Medium | Tools handle missing fields gracefully with defaults | Add `schema_validator.validate_record()` call in each tool's main() before processing |
| SC-03: No SBOM generated on release | Low | Requirements file lists all direct deps with hashes | Add `cyclonedx-bom` to release generation step |
| ASI10 (partial): No universal `_audit` block on written output | Low | `governance_metadata.provenance_chain` provides partial traceability | Add `_audit` block with session_id and written_at to tools that write scored output files |
| WARN-02 (stdin): No size cap on stdin | Low | Stdin used only in pipeline contexts; impractical to cap | Document the limitation; add a stdin size warning if content exceeds a threshold |
| Stanton atmosphere locations may be incomplete | Info | `_ATMOSPHERE_LOCATIONS` covers primary planets and moons; new Alpha patches may add locations | Review `_ATMOSPHERE_LOCATIONS` set in `calculate_traversal.py` after each game patch |

---

## Recommended Future Hardening

Listed by priority (highest first):

1. **Add pip-audit to CI (SC-02)** -- Add `pip-audit -r ../requirements-dev.txt` as a step in `validation.yml`. Zero-cost, catches CVEs before deployment.

2. **Add inline JSON schema validation (WARN-01)** -- Call `schema_validator.validate_tree()` or a lightweight per-record check in tools that process user-supplied JSON. This ensures that malformed or adversarial input is rejected at the gate.

3. **Extend prompt injection check to AI vision mission fields (AI-02)** -- The `_normalise_vision()` path processes structured missions that may contain string fields supplied by an AI provider. Add `check_injection_risk()` (from `owasp-llm.md`) to free-text fields in each normalised mission.

4. **Generate SBOM on release (SC-03)** -- Add `cyclonedx-py environment` to `generate_release_checksums.py` or a separate release step. Include the SBOM hash in the release manifest.

5. **Universal `_audit` block on written output (ASI10)** -- Tools that write scored output to disk should append `{"_audit": {"written_at": ..., "tool": ..., "input_hash": ...}}` to provide full session traceability for replay and forensics.

6. **Add pip-audit to manual developer checklist** -- Until CI automation is in place, document the command in `developer/docs/GETTING_STARTED.md` and the versioning rule in `CLAUDE.md`.

7. **Review `_ATMOSPHERE_LOCATIONS` after each Alpha patch** -- Maintain the set in `calculate_traversal.py` as a living document. Current coverage: Hurston, microTech, ArcCorp, Crusader and all known moons as of Alpha 4.8.0.
