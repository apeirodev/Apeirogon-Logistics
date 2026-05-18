#!/usr/bin/env python3
import argparse
from lib.common import add_common_args, collect_unresolved, dump_json, load_json, validate_governance_metadata
def validate(data):
    problems = []
    gm = data.get("governance_metadata")
    if not isinstance(gm, dict):
        problems.append("missing governance_metadata")
    else:
        ok, issues = validate_governance_metadata(gm)
        if not ok:
            problems.extend(issues)
    if data.get("advisory_only") is not True and not (isinstance(gm, dict) and gm.get("advisory_only") is True):
        problems.append("provider outputs must remain advisory_only")
    return {"valid": not problems, "problems": problems, "unresolved_fields": collect_unresolved(data)}
def main():
    parser = argparse.ArgumentParser(description="Validate provider output")
    add_common_args(parser)
    args = parser.parse_args()
    dump_json(validate(load_json(args.input)), args.output)
if __name__ == "__main__":
    main()
