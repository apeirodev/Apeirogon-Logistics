#!/usr/bin/env python3
import argparse
from lib.common import add_common_args, dump_json, load_json

def classify(data):
    if data.get("patch_baselined") and data.get("maintainer_validated"):
        return "T4"
    if data.get("maintainer_validated"):
        return "T3"
    if int(data.get("corroborating_submission_count", 0) or 0) >= 2:
        return "T2"
    if data.get("user_verified") or data.get("screenshot_supported"):
        return "T1"
    return "T0"

def main():
    parser = argparse.ArgumentParser(description="Classify telemetry trust tier")
    add_common_args(parser)
    args = parser.parse_args()
    data = load_json(args.input)
    tier = classify(data)
    dump_json({"trust_tier": tier, "patch_version": data.get("patch_version", "UNRESOLVED")}, args.output)

if __name__ == "__main__":
    main()
