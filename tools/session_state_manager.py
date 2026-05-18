#!/usr/bin/env python3
from __future__ import annotations
import argparse
import time
from lib.common import (
    add_common_args,
    collect_unresolved,
    dump_json,
    governance_metadata,
    load_json,
    normalize_patch,
    stable_hash,
)

REQUIRED_FIELDS = ["session_id"]
RECOMMENDED_FIELDS = ["ship", "issuer", "patch_version"]
OPTIONAL_FIELDS = [
    "session_start_epoch",
    "current_pickup",
    "completed_missions",
    "pending_missions",
    "notes",
    "home_location",
]

KNOWN_SHIPS = {
    "hull-b", "hull-c", "hull-a", "hull-d",
    "taurus", "caterpillar", "freelancer max", "cutlass black", "freelancer",
}

KNOWN_ISSUERS = {
    "covalex", "ling", "ling family", "red wind", "hurston dynamics", "crusader industries",
}


def _validate(state: dict) -> tuple[list[str], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    recommendations: list[str] = []

    for f in REQUIRED_FIELDS:
        if not state.get(f):
            errors.append(f"missing required field: {f}")

    for f in RECOMMENDED_FIELDS:
        if not state.get(f):
            warnings.append(f"recommended field absent: {f}")
            recommendations.append(f"Add {f} for more accurate scoring and session continuity.")

    ship = (state.get("ship") or "").lower().strip()
    if ship and ship not in KNOWN_SHIPS:
        warnings.append(f"unrecognised ship '{ship}' — not in known ship list")
        recommendations.append("Check spelling or add ship to runtime/scoring_config.json ship_modifiers.")

    issuer = (state.get("issuer") or "").lower().strip()
    if issuer and issuer not in KNOWN_ISSUERS:
        warnings.append(f"unrecognised issuer '{issuer}' — not in known issuer list")
        recommendations.append("Check spelling or add issuer to runtime/scoring_config.json issuer_modifiers.")

    patch = normalize_patch(state)
    if patch == "UNRESOLVED":
        warnings.append("patch_version unresolved — score accuracy may be reduced")
        recommendations.append("Add patch_version (e.g. 'Alpha 3.23') for patch-era tracking.")

    completed = state.get("completed_missions")
    if completed is not None and not isinstance(completed, list):
        errors.append("completed_missions must be a list")

    pending = state.get("pending_missions")
    if pending is not None and not isinstance(pending, list):
        errors.append("pending_missions must be a list")

    epoch = state.get("session_start_epoch")
    if epoch is not None:
        try:
            epoch_val = int(epoch)
            if epoch_val > int(time.time()) + 86400:
                warnings.append("session_start_epoch is in the future")
            if epoch_val < 1_000_000_000:
                warnings.append("session_start_epoch looks too small to be a Unix timestamp")
        except (TypeError, ValueError):
            errors.append("session_start_epoch must be a numeric Unix timestamp")

    return errors, warnings, recommendations


def validate_session(state: dict) -> dict:
    errors, warnings, recommendations = _validate(state)
    unresolved = collect_unresolved(state)
    valid = len(errors) == 0

    return {
        "valid": valid,
        "errors": errors,
        "warnings": warnings,
        "recommendations": recommendations,
        "missing_required": [f for f in REQUIRED_FIELDS if not state.get(f)],
        "missing_recommended": [f for f in RECOMMENDED_FIELDS if not state.get(f)],
        "session_hash": stable_hash(state),
        "unresolved_fields": unresolved,
        "state": state,
        "governance_metadata": governance_metadata(
            source_class="session_state_validation",
            patch_era=normalize_patch(state),
            unresolved=unresolved,
            provenance=[{"type": "session_hash", "sha256": stable_hash(state)}],
            derivation_type="deterministic",
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate and load hauling session state")
    add_common_args(parser)
    args = parser.parse_args()
    state = load_json(args.input)
    if args.patch_version:
        state["patch_version"] = args.patch_version
    dump_json(validate_session(state), args.output)


if __name__ == "__main__":
    main()
