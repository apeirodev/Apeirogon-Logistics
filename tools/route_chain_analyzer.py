#!/usr/bin/env python3
import argparse
from lib.common import add_common_args, dump_json, governance_metadata, load_json, normalize_patch, stable_hash

def analyze(data):
    sequence = [str(x) for x in data.get("route_sequence") or data.get("stops") or []]
    missions = data.get("missions", [])
    unique = len(set(sequence))
    count = len(sequence)
    continuity = "stable" if count and unique <= max(1, count - 1) else "fragile"
    collapse = "high" if count > 6 else "medium" if count > 3 else "low"
    return {
        "route_chain_continuity": continuity,
        "stop_count": count,
        "unique_stop_count": unique,
        "mission_count": len(missions),
        "chain_collapse_risk": collapse,
        "governance_metadata": governance_metadata(
            source_class="deterministic_output",
            patch_era=normalize_patch(data),
            provenance=[{"type": "route_chain_input_hash", "sha256": stable_hash(data)}],
            derivation_type="route_chain_analysis"
        )
    }

def main():
    parser = argparse.ArgumentParser(description="Analyze route-chain continuity")
    add_common_args(parser)
    args = parser.parse_args()
    dump_json(analyze(load_json(args.input)), args.output)

if __name__ == "__main__":
    main()
