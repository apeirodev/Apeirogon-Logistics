#!/usr/bin/env python3
"""
Analyse a route's stop sequence for practical execution characteristics.

Identifies stop types, flags risks (chain collapse, atmospheric burden, dead legs),
and suggests an optimised ordering.

Usage:
  echo '{"stops":["Port Olisar","Covalex Hub Shopp-L4","Hurston","Baijini Point"]}' \
    | python tools/calculate_traversal.py

  python tools/calculate_traversal.py -i route.json
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import add_common_args, collect_unresolved, dump_json, governance_metadata, load_json, normalize_patch, stable_hash

# Locations known to require atmospheric entry
_ATMOSPHERE_LOCATIONS: set[str] = {
    "hurston", "microtech", "arccorp", "crusader",
    "lyria", "wala", "cellin", "daymar", "yela", "aberdeen", "magda",
    "ita", "euterpe", "calliope",
}

# Locations that are orbital (no atmosphere) — L-points, stations, asteroid belts
_ORBITAL_KEYWORDS = {
    "point", "station", "hub", "port", "arc-l", "cru-l", "hur-l", "mic-l",
    "mago", "olisar", "seraphim", "baijini", "shopp", "terra", "rest stop",
}

_CHAIN_COLLAPSE_THRESHOLD = 6
_STOP_DENSITY_THRESHOLD = 3


def _classify_stop(location: str) -> str:
    loc = location.lower().strip()
    for atm in _ATMOSPHERE_LOCATIONS:
        if atm in loc:
            return "atmosphere"
    for orb in _ORBITAL_KEYWORDS:
        if orb in loc:
            return "orbital"
    return "unknown"


def _detect_dead_legs(stops: list[str]) -> list[dict]:
    """Flag consecutive stops that suggest an empty repositioning leg.

    A dead leg is where the same location appears non-consecutively, implying
    a return trip — or where a pickup is not adjacent to the previous delivery.
    This is a structural heuristic only.
    """
    dead_legs = []
    seen: dict[str, int] = {}
    for i, stop in enumerate(stops):
        key = stop.lower().strip()
        if key in seen:
            gap = i - seen[key]
            if gap > 1:
                dead_legs.append({
                    "stop": stop,
                    "first_visit": seen[key],
                    "revisit_at": i,
                    "gap": gap,
                    "note": f"'{stop}' revisited after {gap} stops — possible repositioning leg",
                })
        seen[key] = i
    return dead_legs


def _suggest_ordering(stops: list[str], classified: list[dict]) -> list[str]:
    """Suggest reordering: pickup first, then orbital, then atmosphere."""
    if len(stops) <= 2:
        return stops

    # Keep first stop (presumed pickup/current location) fixed
    first = [classified[0]["stop"]]
    orbitals = [c["stop"] for c in classified[1:] if c["type"] == "orbital"]
    atmospherics = [c["stop"] for c in classified[1:] if c["type"] == "atmosphere"]
    unknowns = [c["stop"] for c in classified[1:] if c["type"] == "unknown"]

    return first + orbitals + unknowns + atmospherics


def analyze_traversal(data: dict) -> dict:
    raw_stops = data.get("stops") or data.get("route_sequence") or []
    stops = [str(s) for s in raw_stops]

    if not stops:
        return {
            "error": "No stops provided. Pass 'stops' or 'route_sequence' in input.",
            "stop_count": 0,
        }

    classified = [{"stop": s, "type": _classify_stop(s)} for s in stops]
    stop_count = len(stops)
    orbital_count = sum(1 for c in classified if c["type"] == "orbital")
    atmosphere_count = sum(1 for c in classified if c["type"] == "atmosphere")
    unknown_count = sum(1 for c in classified if c["type"] == "unknown")

    risks: list[str] = []
    warnings: list[str] = []

    if stop_count > _CHAIN_COLLAPSE_THRESHOLD:
        risks.append(
            f"chain_collapse: {stop_count} stops exceeds threshold of {_CHAIN_COLLAPSE_THRESHOLD}"
        )

    excess_stops = max(0, stop_count - _STOP_DENSITY_THRESHOLD)
    if excess_stops > 0:
        warnings.append(
            f"stop_density: {excess_stops} stops beyond recommended threshold of {_STOP_DENSITY_THRESHOLD}"
        )

    if atmosphere_count > 0:
        risks.append(
            f"atmosphere_burden: {atmosphere_count} stop(s) require atmospheric entry"
        )

    dead_legs = _detect_dead_legs(stops)
    if dead_legs:
        for dl in dead_legs:
            warnings.append(dl["note"])

    suggested = _suggest_ordering(stops, classified)
    order_changed = suggested != stops

    unresolved = collect_unresolved(data)

    return {
        "stop_count": stop_count,
        "orbital_stops": orbital_count,
        "atmosphere_stops": atmosphere_count,
        "unknown_stops": unknown_count,
        "classified_stops": classified,
        "risks": risks,
        "warnings": warnings,
        "dead_leg_candidates": dead_legs,
        "suggested_ordering": suggested,
        "ordering_changed": order_changed,
        "chain_collapse_risk": stop_count > _CHAIN_COLLAPSE_THRESHOLD,
        "atmosphere_burden": atmosphere_count > 0,
        "governance_metadata": governance_metadata(
            source_class="deterministic_output",
            patch_era=normalize_patch(data),
            unresolved=unresolved,
            provenance=[{"type": "input_hash", "sha256": stable_hash(data)}],
            derivation_type="traversal_analysis",
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyse route stop sequence for traversal risks and ordering"
    )
    add_common_args(parser)
    args = parser.parse_args()
    data = load_json(args.input)
    if args.patch_version:
        data["patch_version"] = args.patch_version
    dump_json(analyze_traversal(data), args.output)


if __name__ == "__main__":
    main()
