#!/usr/bin/env python3
import argparse
import hmac
from lib.common import add_common_args, dump_json, load_json, stable_hash

_HASH_CARRIER_FIELDS = ("expected_hash", "deterministic_hash", "replay_manifest")


def main():
    parser = argparse.ArgumentParser(description="Verify replay integrity")
    add_common_args(parser)
    args = parser.parse_args()
    data = load_json(args.input)
    expected = data.get("expected_hash") or data.get("deterministic_hash") or data.get("replay_manifest", {}).get("output_hash")
    if "payload" in data:
        payload = data["payload"]
    else:
        # Exclude the hash-carrier fields themselves; they were not part of
        # the object when the recorded hash was originally computed.
        payload = {k: v for k, v in data.items() if k not in _HASH_CARRIER_FIELDS}
    actual = stable_hash(payload)
    if expected is None:
        # ERR-01: an integrity check with nothing to verify must fail closed,
        # ensuring that missing hashes are never reported as verified.
        result = {
            "valid": False,
            "status": "unverifiable_no_expected_hash",
            "actual_hash": actual,
            "expected_hash": None,
        }
    else:
        valid = hmac.compare_digest(str(actual), str(expected))
        result = {
            "valid": valid,
            "status": "verified" if valid else "hash_mismatch",
            "actual_hash": actual,
            "expected_hash": expected,
        }
    dump_json(result, args.output)


if __name__ == "__main__":
    main()
