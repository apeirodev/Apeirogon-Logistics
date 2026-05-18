#!/usr/bin/env python3
"""
Replay and verify a previously recorded route analysis.

Accepts either:
  - A raw route input with a replay_manifest (produced by route_analysis_runner)
  - A full analysis output containing a deterministic_hash

Re-runs the deterministic scorer on the original input and checks that the
output hash matches the recorded hash. Any divergence indicates the scoring
logic or input has changed since the original run.
"""
import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from deterministic_scorer import score_route
from route_chain_analyzer import analyze
from lib.common import add_common_args, dump_json, load_json, stable_hash
import hmac


def replay(data):
    manifest = data.get("replay_manifest", {})
    recorded_input_hash = manifest.get("input_hash")
    recorded_output_hash = manifest.get("output_hash") or data.get("deterministic_hash")

    # Determine what to score: if there's a nested score_result, the outer
    # object is the runner output and we need the original input separately.
    # Without the original input we can only re-hash the recorded output.
    score_result = data.get("score_result")
    chain_analysis = data.get("chain_analysis")

    if score_result is not None and chain_analysis is not None:
        # This is a runner output; we can re-hash to verify output integrity
        reconstructed = {
            "score_result": score_result,
            "chain_analysis": chain_analysis,
        }
        actual_output_hash = stable_hash(reconstructed)
        output_hash_match = (
            recorded_output_hash is None
            or hmac.compare_digest(actual_output_hash, recorded_output_hash)
        )
        return {
            "replay_mode": "output_integrity_check",
            "output_hash_match": output_hash_match,
            "actual_output_hash": actual_output_hash,
            "recorded_output_hash": recorded_output_hash,
            "valid": output_hash_match,
            "warnings": [] if output_hash_match else [
                "Output hash mismatch — scoring logic or stored result may have changed."
            ],
        }

    # Otherwise treat data as a raw route input and re-run analysis
    actual_input_hash = stable_hash(data)
    input_hash_match = (
        recorded_input_hash is None
        or hmac.compare_digest(actual_input_hash, recorded_input_hash)
    )

    fresh_score = score_route(data)
    fresh_chain = analyze(data)
    fresh_output = {
        "score_result": fresh_score,
        "chain_analysis": fresh_chain,
    }
    actual_output_hash = stable_hash(fresh_output)
    output_hash_match = (
        recorded_output_hash is None
        or hmac.compare_digest(actual_output_hash, recorded_output_hash)
    )

    warnings = []
    if not input_hash_match:
        warnings.append("Input hash mismatch — route data may have been modified since original run.")
    if not output_hash_match:
        warnings.append("Output hash mismatch — scoring logic may have changed since original run.")

    return {
        "replay_mode": "full_replay",
        "input_hash_match": input_hash_match,
        "output_hash_match": output_hash_match,
        "actual_input_hash": actual_input_hash,
        "recorded_input_hash": recorded_input_hash,
        "actual_output_hash": actual_output_hash,
        "recorded_output_hash": recorded_output_hash,
        "valid": input_hash_match and output_hash_match,
        "warnings": warnings,
        "replayed_result": fresh_output,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Replay and verify a recorded deterministic route analysis"
    )
    add_common_args(parser)
    args = parser.parse_args()
    data = load_json(args.input)
    if args.patch_version:
        data["patch_version"] = args.patch_version
    dump_json(replay(data), args.output)


if __name__ == "__main__":
    main()
