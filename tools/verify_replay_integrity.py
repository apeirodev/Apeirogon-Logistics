#!/usr/bin/env python3
import argparse
from lib.common import add_common_args, dump_json, load_json, stable_hash
def main():
    parser = argparse.ArgumentParser(description="Verify replay integrity")
    add_common_args(parser)
    args = parser.parse_args()
    data = load_json(args.input)
    expected = data.get("expected_hash") or data.get("deterministic_hash") or data.get("replay_manifest", {}).get("output_hash")
    payload = data.get("payload", data)
    actual = stable_hash(payload)
    dump_json({"valid": expected in (None, actual), "actual_hash": actual, "expected_hash": expected}, args.output)
if __name__ == "__main__":
    main()
