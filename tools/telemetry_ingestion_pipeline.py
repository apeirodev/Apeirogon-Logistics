#!/usr/bin/env python3
import argparse, time
from lib.common import add_common_args, collect_unresolved, dump_json, governance_metadata, load_json, normalize_patch, parse_positive_number, stable_hash

def trust_tier(data):
    if data.get("patch_baselined") and data.get("maintainer_validated"):
        return "T4"
    if data.get("maintainer_validated"):
        return "T3"
    if int(data.get("corroborating_submission_count", 0) or 0) >= 2:
        return "T2"
    if data.get("user_verified") or data.get("screenshot_supported"):
        return "T1"
    return "T0"

def validate(data):
    errors, warnings, remediation = [], [], []
    patch = normalize_patch(data)
    if patch == "UNRESOLVED":
        warnings.append("Patch version unresolved.")
        remediation.append("Add patch_version before attempting calibration or baseline promotion.")
    for field in ["ship", "issuer"]:
        if not data.get(field):
            errors.append(f"missing required field: {field}")
            remediation.append(f"Populate {field} or mark record incomplete.")
    duration = parse_positive_number(data.get("duration_minutes"))
    if duration is not None and duration > 600:
        errors.append("duration_minutes exceeds plausible single-session threshold.")
    cargo = parse_positive_number(data.get("cargo_scu"))
    if cargo is not None and cargo > 10000:
        errors.append("cargo_scu exceeds plausible operational threshold.")
    return errors, warnings, remediation

def ingest(data):
    errors, warnings, remediation = validate(data)
    unresolved = collect_unresolved(data)
    tier = trust_tier(data)
    accepted = len(errors) == 0
    result = {
        "accepted": accepted,
        "quarantined": not accepted,
        "errors": errors,
        "warnings": warnings,
        "remediation": remediation,
        "trust_tier": tier,
        "deduplication_hash": stable_hash(data),
        "patch_version": normalize_patch(data),
        "unresolved_fields": unresolved,
        "ingested_at_epoch": int(time.time()),
        "calibration_allowed": False,
        "calibration_reason": "Real telemetry review required; this tool does not calibrate heuristics.",
        "governance_metadata": governance_metadata(
            source_class="telemetry_observational",
            patch_era=normalize_patch(data),
            unresolved=unresolved,
            provenance=[{"type": "telemetry_input_hash", "sha256": stable_hash(data)}],
            contributor_trust_tier=tier,
            telemetry_support_level="observational",
            derivation_type="telemetry_ingestion"
        )
    }
    return result

def main():
    parser = argparse.ArgumentParser(description="Validate and ingest telemetry")
    add_common_args(parser)
    args = parser.parse_args()
    data = load_json(args.input)
    if args.patch_version:
        data["patch_version"] = args.patch_version
    dump_json(ingest(data), args.output)

if __name__ == "__main__":
    main()
