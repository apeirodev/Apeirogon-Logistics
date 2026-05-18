#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from lib.common import add_common_args, collect_unresolved, dump_json, load_json, validate_governance_metadata

# Fields that carry numeric operational values — if AI supplies these without
# the user having provided them, that is a hallucination risk.
NUMERIC_OPERATIONAL_FIELDS = {
    "reward_usc", "fee_usc", "profit_usc", "cargo_scu",
    "price_usc", "distance_km", "capacity_scu", "quantity_scu",
    "payout_usc", "penalty_usc", "net_usc",
}


def _flag_hallucination_risk(data: dict, user_supplied: set) -> list[str]:
    flags = []
    for field in NUMERIC_OPERATIONAL_FIELDS:
        val = data.get(field)
        if val is not None and isinstance(val, (int, float)) and field not in user_supplied:
            flags.append(
                f"hallucination_risk: '{field}'={val!r} is numeric but was not "
                f"in user-supplied fields — verify this value came from your data"
            )
    return flags


def validate(data: dict, user_supplied_fields: set | None = None) -> dict:
    problems = []
    hallucination_flags = []

    gm = data.get("governance_metadata")
    if not isinstance(gm, dict):
        problems.append("missing governance_metadata")
    else:
        ok, issues = validate_governance_metadata(gm)
        if not ok:
            problems.extend(issues)
        source_class = gm.get("source_class", "")
        if source_class not in ("ai_output", "ai_generated"):
            problems.append(
                f"provider output must have source_class 'ai_output', got {source_class!r}"
            )

    if data.get("advisory_only") is not True and not (
        isinstance(gm, dict) and gm.get("advisory_only") is True
    ):
        problems.append("provider outputs must remain advisory_only=true")

    if user_supplied_fields is not None:
        hallucination_flags = _flag_hallucination_risk(data, user_supplied_fields)

    return {
        "valid": not problems,
        "problems": problems,
        "hallucination_flags": hallucination_flags,
        "hallucination_flag_count": len(hallucination_flags),
        "unresolved_fields": collect_unresolved(data),
    }


def main():
    parser = argparse.ArgumentParser(description="Validate provider output")
    add_common_args(parser)
    parser.add_argument(
        "--user-supplied-fields",
        default="",
        help="Comma-separated list of field names the user explicitly provided "
             "(used to flag hallucination risk on numeric fields the AI invented)",
    )
    args = parser.parse_args()
    user_supplied = (
        {f.strip() for f in args.user_supplied_fields.split(",") if f.strip()}
        if args.user_supplied_fields
        else None
    )
    dump_json(validate(load_json(args.input), user_supplied), args.output)


if __name__ == "__main__":
    main()
