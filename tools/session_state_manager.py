#!/usr/bin/env python3
import argparse
from lib.common import dump_json, load_json, stable_hash, collect_unresolved
def main():
    parser = argparse.ArgumentParser(description="Validate session state")
    parser.add_argument("--input", "-i", required=True)
    parser.add_argument("--output", "-o", default="-")
    args = parser.parse_args()
    state = load_json(args.input)
    missing = [x for x in ["session_id"] if x not in state]
    dump_json({"valid": not missing, "missing": missing, "session_hash": stable_hash(state), "unresolved_fields": collect_unresolved(state), "state": state}, args.output)
if __name__ == "__main__":
    main()
