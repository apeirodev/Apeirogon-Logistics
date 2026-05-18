# Governance Metadata Guide

Every output from the Apeirogon Logistics pipeline carries a `governance_metadata` block. This guide explains each field, its allowed values, and what it means for how you should interpret the output.

---

## Why Governance Metadata Exists

The pipeline mixes data from different sources: AI extractions, OCR normalisations, user-typed values, and deterministic scoring. Without provenance tracking, a number in a scored output could be AI-hallucinated, OCR-garbled, user-entered, or algorithmically derived, and there would be no way to tell. Governance metadata makes provenance explicit and machine-readable.

---

## Required Fields

All 11 fields below are required on every pipeline output. Missing any of them causes `validate_governance_metadata()` to fail.

### `source_class`

What produced this output.

| Value | Meaning |
|-------|---------|
| `deterministic_output` | Produced by a deterministic tool (scorer, batch, chain analyzer) |
| `ai_vision_extraction` | Produced by an AI provider's vision OCR |
| `ai_output` | Generic AI provider output (non-vision) |
| `OCR_extraction` | Produced by local OCR normalisation |
| `telemetry_observational` | Session telemetry from a real run |
| `user_profile_validation` | User profile loader output |
| `session_state_validation` | Session state manager output |
| `manual_entry` | Typed directly by the user |

### `provenance_chain`

An ordered list of provenance entries tracing this output back to its inputs. Entries are objects with `type` and `sha256`. The chain is built automatically by the tools; you do not normally set it manually.

### `confidence_level`

How reliable the output is. Set automatically: `"high"` when no UNRESOLVED fields, `"medium"` when some fields are UNRESOLVED, `"low"` when many fields are UNRESOLVED.

| Value | Meaning |
|-------|---------|
| `high` | No UNRESOLVED fields; full data available |
| `medium` | Some UNRESOLVED fields; output usable with caution |
| `low` | Many UNRESOLVED fields; human review required |

### `verification_status`

Whether a human confirmed this output against source material.

| Value | Meaning |
|-------|---------|
| `not_human_verified` | Default for all tool outputs |
| `human_verified` | User confirmed values against their screen |
| `peer_reviewed` | Reviewed by a second contributor |

### `patch_era`

The Star Citizen patch version in effect when this output was produced. Set to `"UNRESOLVED"` if the patch is unknown. Calibration data without a patch era cannot be used for timeline analysis.

### `telemetry_support_level`

Whether real session telemetry backs the heuristic weights used in this output.

| Value | Meaning |
|-------|---------|
| `none` | No telemetry; weights are estimates |
| `partial` | Some weights have telemetry support |
| `observational` | Telemetry from a single session |
| `full` | Multi-session, multi-contributor telemetry |

### `operational_assurance_state`

The maturity of the scoring logic that produced this output.

| Value | Meaning |
|-------|---------|
| `designed` | Logic defined but not yet tested in operation |
| `implemented` | Logic coded and passing tests |
| `operational` | Logic in active use |
| `validated` | Logic validated against telemetry outcomes |
| `community_validated` | Logic validated across multiple contributor submissions |

### `unresolved_field_list`

A list of field names in this output that carry the `"UNRESOLVED"` sentinel. An empty list `[]` means the output has no missing values.

### `advisory_only`

Always `true`. Every output from this pipeline is advisory. No output from these tools should be treated as authoritative game data. Star Citizen values change with patches, and AI assistants can hallucinate.

### `contributor_trust_tier`

The trust tier of the source or contributor. See `CONTRIBUTOR_TRUST_MODEL.md`. System-generated outputs use `"T0"`. User-submitted data starts at `"T3"` unless the contributor is a known T1 or T2.

### `derivation_type`

A label for the specific algorithm or pipeline stage that produced this output. Examples: `deterministic_heuristic`, `batch_deterministic_scoring`, `ai_vision_normalisation`, `telemetry_ingestion`, `sensitivity_analysis`.

---

## Validation

To validate governance metadata on any output file:

```python
from tools.lib.common import validate_governance_metadata
ok, problems = validate_governance_metadata(output["governance_metadata"])
```

Or via the provider output validator for AI outputs:

```bash
python tools/provider_output_validator.py -i ai_output.json
```
