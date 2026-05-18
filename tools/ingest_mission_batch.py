#!/usr/bin/env python3
"""
Ingest a batch of missions, score each one, and return ranked recommendations.

Accepts input from either:
  a) The output of OCR_result_normalizer.py (mode: ai_vision), or
  b) A raw batch object with top-level issuer/ship and a missions list.

Input structure (raw batch):
  {
    "issuer": "covalex",
    "ship": "hull-b",
    "missions": [
      {"pickup": "Port Olisar", "delivery": ["Baijini Point"], "cargo_scu": 24, "reward_usc": 12500},
      ...
    ]
  }

Output:
  - Ranked mission list with individual scores
  - Same-pickup stacking opportunities detected
  - A suggested combined route for accepted missions
  - Governance metadata for the batch
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from deterministic_scorer import score_route, DEFAULT_WEIGHTS
from route_chain_analyzer import analyze
from lib.common import (
    add_common_args, collect_unresolved, dump_json, governance_metadata,
    load_json, normalize_patch, stable_hash,
)


def _mission_to_route(mission: dict, issuer: str, ship: str) -> dict:
    """Build a route input dict from a single mission plus batch context."""
    pickup = mission.get("pickup", "UNRESOLVED")
    delivery = mission.get("delivery", ["UNRESOLVED"])
    if isinstance(delivery, str):
        delivery = [delivery]

    stops = [pickup] + [d for d in delivery if d not in ("UNRESOLVED", None, "")]
    route = {
        "issuer": mission.get("issuer") or issuer,
        "ship": ship,
        "stops": stops,
        "route_sequence": stops,
    }
    # Pass numeric fields from mission directly into route for factor() to pick up
    for field in ("cargo_scu", "reward_usc", "fee_usc", "atmosphere", "fragmentation",
                  "dead_leg", "congestion", "fatigue"):
        val = mission.get(field)
        if val not in (None, "UNRESOLVED", ""):
            route[field] = val

    # Preserve unresolved fields so scorer can penalise
    unresolved = list(mission.get("unresolved_fields", []))
    if unresolved:
        route["unresolved_fields"] = unresolved

    return route


def _detect_same_pickup(missions: list[dict]) -> dict[str, list[int]]:
    """Return {pickup_location: [mission_indices]} for pickups shared by 2+ missions."""
    from collections import defaultdict
    groups: dict[str, list[int]] = defaultdict(list)
    for idx, m in enumerate(missions):
        pickup = m.get("pickup", "UNRESOLVED")
        if pickup != "UNRESOLVED":
            groups[pickup].append(idx)
    return {k: v for k, v in groups.items() if len(v) >= 2}


def _build_combined_route(accepted_missions: list[dict], issuer: str, ship: str) -> dict | None:
    """Build a combined route from all accepted missions for chain analysis."""
    if not accepted_missions:
        return None
    stops = []
    seen_pickups: set[str] = set()
    # Group by pickup to stack same-pickup missions first
    for m in accepted_missions:
        pickup = m.get("pickup", "UNRESOLVED")
        if pickup != "UNRESOLVED" and pickup not in seen_pickups:
            stops.append(pickup)
            seen_pickups.add(pickup)
    # Then add all deliveries
    for m in accepted_missions:
        delivery = m.get("delivery", [])
        if isinstance(delivery, str):
            delivery = [delivery]
        for d in delivery:
            if d not in ("UNRESOLVED", None, "") and d not in stops:
                stops.append(d)

    return {
        "issuer": issuer,
        "ship": ship,
        "route_sequence": stops,
        "stops": stops,
        "same_pickup": sum(
            max(0, len([m for m in accepted_missions if m.get("pickup") == p]) - 1)
            for p in seen_pickups
        ),
    }


def ingest_batch(data: dict) -> dict:
    # Accept both raw batch and normaliser output (mode: ai_vision)
    if data.get("mode") == "ai_vision":
        missions = data.get("missions") or []
        issuer = data.get("issuer", "UNRESOLVED")
        ship = data.get("ship", "UNRESOLVED")
        patch = data.get("patch_version", "UNRESOLVED")
    else:
        missions = data.get("missions") or []
        issuer = str(data.get("issuer", "UNRESOLVED"))
        ship = str(data.get("ship", "UNRESOLVED"))
        patch = normalize_patch(data)

    scored: list[dict] = []
    for idx, mission in enumerate(missions):
        route = _mission_to_route(mission, issuer, ship)
        score_result = score_route(route)
        scored.append({
            "mission_index": idx,
            "issuer": mission.get("issuer") or issuer,
            "pickup": mission.get("pickup", "UNRESOLVED"),
            "delivery": mission.get("delivery", ["UNRESOLVED"]),
            "cargo_type": mission.get("cargo_type", "UNRESOLVED"),
            "cargo_scu": mission.get("cargo_scu", "UNRESOLVED"),
            "reward_usc": mission.get("reward_usc", "UNRESOLVED"),
            "score": score_result["score"],
            "recommendation": score_result["recommendation"],
            "operational_risk": score_result["operational_risk"],
            "unresolved_fields": mission.get("unresolved_fields", []),
            "score_breakdown": score_result["score_breakdown"],
            "warnings": score_result["warnings"],
        })

    ranked = sorted(scored, key=lambda x: x["score"], reverse=True)

    same_pickup_groups = _detect_same_pickup(missions)

    accepted = [s for s in ranked if s["recommendation"] == "accept"]
    deferred = [s for s in ranked if s["recommendation"] == "defer"]
    rejected = [s for s in ranked if s["recommendation"] == "reject"]

    # Build combined route from accepted + deferred (anything not outright rejected).
    # This is the primary value of the batch: showing stacking bonus even when
    # individual missions score too low to accept on their own.
    candidate_missions = [missions[s["mission_index"]] for s in ranked if s["recommendation"] != "reject"]
    if not candidate_missions:
        candidate_missions = [missions[s["mission_index"]] for s in ranked]  # fall back to all
    combined_route_input = _build_combined_route(candidate_missions, issuer, ship)
    combined_route = None
    if combined_route_input:
        combined_score = score_route(combined_route_input)
        combined_chain = analyze(combined_route_input)
        combined_route = {
            "stops": combined_route_input.get("route_sequence", []),
            "score": combined_score["score"],
            "recommendation": combined_score["recommendation"],
            "chain_analysis": combined_chain,
            "same_pickup_bonus": combined_route_input.get("same_pickup", 0),
        }

    unresolved = collect_unresolved(data)

    return {
        "batch_summary": {
            "mission_count": len(missions),
            "accepted": len(accepted),
            "deferred": len(deferred),
            "rejected": len(rejected),
            "issuer": issuer,
            "ship": ship,
            "patch_version": patch,
        },
        "ranked_missions": ranked,
        "same_pickup_stacking": same_pickup_groups,
        "suggested_combined_route": combined_route,
        "governance_metadata": governance_metadata(
            source_class="deterministic_output",
            patch_era=patch,
            unresolved=sorted(set(unresolved)),
            provenance=[{"type": "batch_input_hash", "sha256": stable_hash(data)}],
            confidence_level="low" if unresolved else "high",
            derivation_type="batch_deterministic_scoring",
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest a batch of missions and return ranked scores")
    add_common_args(parser)
    args = parser.parse_args()
    data = load_json(args.input)
    if args.patch_version:
        data["patch_version"] = args.patch_version
    dump_json(ingest_batch(data), args.output)


if __name__ == "__main__":
    main()
