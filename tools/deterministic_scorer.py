#!/usr/bin/env python3
from __future__ import annotations
import argparse
from typing import Any, Dict, List
from lib.common import add_common_args, collect_unresolved, dump_json, governance_metadata, load_json, normalize_patch, stable_hash

DEFAULT_WEIGHTS = {
    "same_pickup": 16,
    "destination_overlap": 12,
    "orbital_loop": 12,
    "issuer_alignment": 8,
    "ship_suitability": 10,
    "route_continuity": 10,
    "cargo_panel_clarity": 8,
    "atmosphere": -12,
    "freight": -8,
    "dead_leg": -15,
    "fragmentation": -12,
    "stop_density": -6,
    "fatigue": -7,
    "congestion": -8,
    "unloading_cognitive_load": -7,
    "chain_collapse": -14
}

ISSUER_MODIFIERS = {
    "covalex": {"issuer_alignment": 1.10, "orbital_loop": 1.05, "route_continuity": 1.05},
    "ling": {"destination_overlap": 1.05, "same_pickup": 1.03},
    "ling family": {"destination_overlap": 1.05, "same_pickup": 1.03},
    "red wind": {"dead_leg": 1.10, "congestion": 1.05}
}

SHIP_MODIFIERS = {
    "hull-b": {"freight": 1.05, "fragmentation": 1.10, "cargo_panel_clarity": 1.15, "ship_suitability": 1.05},
    "hull-c": {"freight": 1.25, "stop_density": 1.20, "ship_suitability": 1.15},
    "taurus": {"ship_suitability": 1.05, "fatigue": 0.95},
    "caterpillar": {"freight": 1.10, "ship_suitability": 1.10},
    "freelancer max": {"ship_suitability": 1.02, "fatigue": 0.98}
}

def clamp(value: float, lo: int = 0, hi: int = 100) -> int:
    return int(max(lo, min(hi, round(value))))

def sequence(data: Dict[str, Any]) -> List[str]:
    return [str(x) for x in data.get("route_sequence") or data.get("stops") or []]

def factor(route: Dict[str, Any], key: str) -> float:
    if key in route:
        try:
            return float(route[key])
        except Exception:
            return 0.0
    missions = route.get("missions", [])
    seq = sequence(route)
    if key == "same_pickup" and missions:
        pickups = [m.get("pickup") for m in missions if isinstance(m, dict) and m.get("pickup")]
        return max(0, len(pickups) - len(set(pickups)))
    if key == "destination_overlap" and missions:
        dests = []
        for m in missions:
            if isinstance(m, dict):
                dest = m.get("destination") or m.get("delivery")
                if isinstance(dest, list):
                    dests.extend(str(x) for x in dest)
                elif dest:
                    dests.append(str(dest))
        return max(0, len(dests) - len(set(dests)))
    if key == "stop_density":
        return max(0, len(seq) - 3)
    if key == "route_continuity":
        return 1 if len(seq) >= 2 and len(set(seq)) < len(seq) else 0
    if key == "chain_collapse":
        return 1 if len(seq) > 6 else 0
    return 0.0

def score_route(route: Dict[str, Any], weights: Dict[str, float] | None = None) -> Dict[str, Any]:
    weights = weights or DEFAULT_WEIGHTS
    issuer = str(route.get("issuer", "")).lower()
    ship = str(route.get("ship", "")).lower()
    issuer_mod = ISSUER_MODIFIERS.get(issuer, {})
    ship_mod = SHIP_MODIFIERS.get(ship, {})
    total = 50.0
    trace = []
    warnings = []
    breakdown = {}

    for key, base_weight in weights.items():
        value = factor(route, key)
        if not value:
            continue
        modifier = issuer_mod.get(key, 1.0) * ship_mod.get(key, 1.0)
        weighted = value * base_weight * modifier
        total += weighted
        breakdown[key] = round(weighted, 3)
        trace.append({
            "factor": key,
            "input_value": value,
            "base_weight": base_weight,
            "modifier": round(modifier, 3),
            "weighted_effect": round(weighted, 3)
        })

    unresolved = collect_unresolved(route)
    if unresolved:
        warnings.append("Unresolved values present; confidence downgraded and human review recommended.")
        total -= min(12, len(unresolved) * 2)

    if factor(route, "fragmentation") >= 2:
        warnings.append("Cargo fragmentation exceeds recommended deterministic threshold.")
    if factor(route, "dead_leg") > 0:
        warnings.append("Dead-leg risk detected.")
    if factor(route, "stop_density") >= 3:
        warnings.append("High stop density may degrade practical execution.")
    if factor(route, "atmosphere") > 0:
        warnings.append("Atmosphere burden detected.")
    if factor(route, "chain_collapse") > 0:
        warnings.append("Route-chain collapse risk detected.")

    score = clamp(total)
    risk = "low" if score >= 75 else "medium" if score >= 50 else "high"
    recommendation = "accept" if score >= 70 else "defer" if score >= 45 else "reject"
    confidence = "medium" if unresolved or warnings else "high"

    output = {
        "recommendation": recommendation,
        "score": score,
        "operational_risk": risk,
        "confidence_level": confidence,
        "weighted_decision_trace": trace,
        "score_breakdown": breakdown,
        "warnings": warnings,
        "human_rationale": f"Deterministic score {score}/100 with {risk} operational risk. Recommendation: {recommendation}.",
        "machine_rationale": {
            "positive_factors": [t for t in trace if t["weighted_effect"] > 0],
            "negative_factors": [t for t in trace if t["weighted_effect"] < 0]
        },
        "unresolved_fields": unresolved,
        "governance_metadata": governance_metadata(
            source_class="deterministic_output",
            patch_era=normalize_patch(route),
            unresolved=unresolved,
            provenance=[{"type": "input_hash", "sha256": stable_hash(route)}],
            confidence_level=confidence,
            derivation_type="deterministic_heuristic"
        )
    }
    output["deterministic_hash"] = stable_hash(output)
    return output

def main() -> None:
    parser = argparse.ArgumentParser(description="Deterministic Apeirogon route scorer")
    add_common_args(parser)
    parser.add_argument("--weights", help="Optional weights JSON")
    args = parser.parse_args()
    route = load_json(args.input)
    if args.patch_version:
        route["patch_version"] = args.patch_version
    weights = load_json(args.weights) if args.weights else None
    dump_json(score_route(route, weights), args.output)

if __name__ == "__main__":
    main()
