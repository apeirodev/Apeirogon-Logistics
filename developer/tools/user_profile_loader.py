#!/usr/bin/env python3
from __future__ import annotations
import argparse
from lib.common import (
    add_common_args,
    collect_unresolved,
    dump_json,
    governance_metadata,
    load_json,
    normalize_patch,
    stable_hash,
)

REQUIRED_FIELDS = ["user_profile_id"]
RECOMMENDED_FIELDS = ["preferred_ship", "preferred_issuer"]
OPTIONAL_FIELDS = [
    "home_location",
    "patch_version",
    "reputation",
    "notes",
    "created_epoch",
    "updated_epoch",
]

KNOWN_SHIPS = {
    "hull-b", "hull-c", "hull-a", "hull-d",
    "taurus", "caterpillar", "freelancer max", "cutlass black", "freelancer",
}

KNOWN_ISSUERS = {
    "covalex", "ling", "ling family", "red wind", "hurston dynamics", "crusader industries",
}


def _validate(profile: dict) -> tuple[list[str], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    recommendations: list[str] = []

    for f in REQUIRED_FIELDS:
        if not profile.get(f):
            errors.append(f"missing required field: {f}")

    for f in RECOMMENDED_FIELDS:
        if not profile.get(f):
            warnings.append(f"recommended field absent: {f}")
            recommendations.append(f"Add {f} to get ship- and issuer-specific scoring defaults.")

    ship = (profile.get("preferred_ship") or "").lower().strip()
    if ship and ship not in KNOWN_SHIPS:
        warnings.append(f"unrecognised preferred_ship '{ship}' — not in known ship list")
        recommendations.append("Check spelling or add the ship to runtime/scoring_config.json ship_modifiers.")

    issuer = (profile.get("preferred_issuer") or "").lower().strip()
    if issuer and issuer not in KNOWN_ISSUERS:
        warnings.append(f"unrecognised preferred_issuer '{issuer}' — not in known issuer list")
        recommendations.append("Check spelling or add the issuer to runtime/scoring_config.json issuer_modifiers.")

    reputation = profile.get("reputation")
    if reputation is not None:
        if not isinstance(reputation, dict):
            errors.append("reputation must be a dict mapping issuer names to values")
        else:
            for iss, val in reputation.items():
                try:
                    float(val)
                except (TypeError, ValueError):
                    errors.append(f"reputation['{iss}'] is not numeric")

    return errors, warnings, recommendations


def load_profile(profile: dict) -> dict:
    errors, warnings, recommendations = _validate(profile)
    unresolved = collect_unresolved(profile)
    valid = len(errors) == 0

    return {
        "valid": valid,
        "errors": errors,
        "warnings": warnings,
        "recommendations": recommendations,
        "missing_required": [f for f in REQUIRED_FIELDS if not profile.get(f)],
        "missing_recommended": [f for f in RECOMMENDED_FIELDS if not profile.get(f)],
        "profile_hash": stable_hash(profile),
        "unresolved_fields": unresolved,
        "profile": profile,
        "governance_metadata": governance_metadata(
            source_class="user_profile_validation",
            patch_era=normalize_patch(profile),
            unresolved=unresolved,
            provenance=[{"type": "profile_hash", "sha256": stable_hash(profile)}],
            derivation_type="deterministic",
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Load and validate portable user profile")
    add_common_args(parser)
    args = parser.parse_args()
    profile = load_json(args.input)
    if args.patch_version:
        profile["patch_version"] = args.patch_version
    dump_json(load_profile(profile), args.output)


if __name__ == "__main__":
    main()
