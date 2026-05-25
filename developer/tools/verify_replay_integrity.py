#!/usr/bin/env python3
import argparse
import hmac
from lib.common import add_common_args, dump_json, load_json, stable_hash
def main():
    parser = argparse.ArgumentParser(description="Verify replay integrity")
    add_common_args(parser)
    args = parser.parse_args()
    data = load_json(args.input)
    expected = data.get("expected_hash") or data.get("deterministic_hash") or data.get("replay_manifest", {}).get("output_hash")
    payload = data.get("payload", data)
    actual = stable_hash(payload)
    if expected is None:
        valid = True
    else:
        valid = hmac.compare_digest(str(actual), str(expected))
    dump_json({"valid": valid, "actual_hash": actual, "expected_hash": expected}, args.output)
if __name__ == "__main__":
    main()
