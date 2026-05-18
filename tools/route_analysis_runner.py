#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from deterministic_scorer import score_route
from route_chain_analyzer import analyze
from lib.common import add_common_args, dump_json, load_json, stable_hash

def run_analysis(data: dict) -> dict:
    result = {
        "score_result": score_route(data),
        "chain_analysis": analyze(data),
    }
    result["replay_manifest"] = {
        "input_hash": stable_hash(data),
        "output_hash": stable_hash(result),
        "tool": "route_analysis_runner",
    }
    return result


def main():
    parser = argparse.ArgumentParser(description="Run deterministic route analysis")
    add_common_args(parser)
    args = parser.parse_args()
    data = load_json(args.input)
    if args.patch_version:
        data["patch_version"] = args.patch_version
    dump_json(run_analysis(data), args.output)

if __name__ == "__main__":
    main()
