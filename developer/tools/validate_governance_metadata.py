#!/usr/bin/env python3
import argparse
from lib.common import add_common_args, dump_json, load_json, validate_governance_metadata
def main():
    parser = argparse.ArgumentParser(description="Validate governance metadata")
    add_common_args(parser)
    args = parser.parse_args()
    data = load_json(args.input)
    meta = data.get("governance_metadata", data)
    ok, problems = validate_governance_metadata(meta)
    dump_json({"valid": ok, "problems": problems}, args.output)
if __name__ == "__main__":
    main()
