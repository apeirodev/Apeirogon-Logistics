#!/usr/bin/env python3
"""
Show how the route score changes as individual factor weights are scaled.

Usage:
  echo '{"issuer":"covalex","ship":"hull-b","same_pickup":2,"dead_leg":1}' \
    | python tools/weight_sensitivity_analyzer.py

  python tools/weight_sensitivity_analyzer.py -i route.json -o sensitivity.json
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import add_common_args, dump_json, governance_metadata, load_json, normalize_patch, stable_hash
from deterministic_scorer import DEFAULT_WEIGHTS, score_route


_SCALE_POINTS = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]
_SCALE_LABELS = ["×0.5", "×0.75", "×1.0 (baseline)", "×1.25", "×1.5", "×2.0"]


def _score_at_scale(route: dict, factor: str, scale: float) -> int:
    weights = dict(DEFAULT_WEIGHTS)
    weights[factor] = weights[factor] * scale
    return score_route(route, weights)["score"]


def analyze(route: dict) -> dict:
    baseline = score_route(route)
    baseline_score = baseline["score"]

    active_factors = [
        k for k in DEFAULT_WEIGHTS
        if route.get(k) not in (None, 0, "", "UNRESOLVED")
    ]

    sensitivity_table: list[dict] = []

    for factor in sorted(active_factors):
        row: dict = {
            "factor": factor,
            "baseline_score": baseline_score,
            "scales": {},
            "max_delta": 0,
        }
        max_delta = 0
        for scale, label in zip(_SCALE_POINTS, _SCALE_LABELS):
            s = _score_at_scale(route, factor, scale)
            delta = s - baseline_score
            row["scales"][label] = {"score": s, "delta": delta}
            if abs(delta) > abs(max_delta):
                max_delta = delta
        row["max_delta"] = max_delta
        sensitivity_table.append(row)

    sensitivity_table.sort(key=lambda r: abs(r["max_delta"]), reverse=True)

    most_sensitive = sensitivity_table[0]["factor"] if sensitivity_table else None

    unresolved = baseline.get("unresolved_fields", [])

    return {
        "baseline_score": baseline_score,
        "baseline_recommendation": baseline["recommendation"],
        "active_factors": active_factors,
        "most_sensitive_factor": most_sensitive,
        "sensitivity_table": sensitivity_table,
        "interpretation": (
            f"Score {baseline_score} is most affected by '{most_sensitive}'. "
            "A ×2.0 scale shows the upper bound of influence for each factor."
            if most_sensitive else
            "No active factors found -- route may have no factor inputs."
        ),
        "governance_metadata": governance_metadata(
            source_class="deterministic_output",
            patch_era=normalize_patch(route),
            unresolved=unresolved,
            provenance=[{"type": "input_hash", "sha256": stable_hash(route)}],
            derivation_type="sensitivity_analysis",
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze how route score changes as individual factor weights scale"
    )
    add_common_args(parser)
    args = parser.parse_args()
    route = load_json(args.input)
    if args.patch_version:
        route["patch_version"] = args.patch_version
    dump_json(analyze(route), args.output)


if __name__ == "__main__":
    main()
