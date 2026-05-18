#!/usr/bin/env python3
import argparse
from lib.common import dump_json, load_json, stable_hash
def main():
    parser = argparse.ArgumentParser(description="Load portable user profile")
    parser.add_argument("--input", "-i", required=True)
    parser.add_argument("--output", "-o", default="-")
    args = parser.parse_args()
    profile = load_json(args.input)
    missing = [x for x in ["user_profile_id"] if x not in profile]
    dump_json({"valid": not missing, "missing": missing, "profile_hash": stable_hash(profile), "profile": profile}, args.output)
if __name__ == "__main__":
    main()
