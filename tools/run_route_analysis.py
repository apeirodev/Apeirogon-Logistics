#!/usr/bin/env python3
import argparse
from deterministic_scorer import score_route
from route_chain_analyzer import analyze
from lib.common import add_common_args, dump_json, load_json, stable_hash

def main():
    parser = argparse.ArgumentParser(description="Run deterministic route analysis")
    add_common_args(parser)
    args = parser.parse_args()
    data = load_json(args.input)
    if args.patch_version:
        data["patch_version"] = args.patch_version
    result = {
        "score_result": score_route(data),
        "chain_analysis": analyze(data)
    }
    result["replay_manifest"] = {
        "input_hash": stable_hash(data),
        "output_hash": stable_hash(result),
        "tool": "route_analysis_runner"
    }
    dump_json(result, args.output)

if __name__ == "__main__":
    main()
