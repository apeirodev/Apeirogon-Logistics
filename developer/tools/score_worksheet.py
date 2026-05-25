#!/usr/bin/env python3
"""
Interactive contract scoring worksheet.

Walks you through the scoring factors for a hauling route and produces
a score, recommendation, and factor breakdown. Uses the same deterministic
scorer as the AI-assisted workflow so results are identical.

Usage:
  python tools/score_worksheet.py
  python tools/score_worksheet.py --json      # output raw JSON instead of formatted
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from deterministic_scorer import score_route, DEFAULT_WEIGHTS, ISSUER_MODIFIERS, SHIP_MODIFIERS

_FACTOR_LABELS = {
    "same_pickup":            "Same-pickup bonus (extra contracts at this pickup)",
    "destination_overlap":    "Destination overlap between contracts",
    "orbital_loop":           "Full orbital route (no atmosphere landings)",
    "issuer_alignment":       "Issuer alignment bonus",
    "ship_suitability":       "Ship suits the cargo type",
    "route_continuity":       "Pickups chain well from one to the next",
    "cargo_panel_clarity":    "Cargo panels assign cleanly by destination",
    "dead_leg":               "Dead leg (flying empty to pickup)",
    "chain_collapse":         "Fragile dependencies that could collapse",
    "fragmentation":          "Extra delivery stops beyond the first",
    "atmosphere":             "Atmosphere landings",
    "congestion":             "Congested stations on the route",
    "freight":                "Difficult freight handling",
    "unloading_cognitive_load": "Complex unloading sequence",
    "stop_density":           "Stops beyond 2 total in the route",
    "fatigue":                "Tiring multi-leg route",
}

_DIVIDER = "-" * 54


def _ask(prompt: str, default: str = "") -> str:
    try:
        sys.stderr.write(f"  {prompt} ")
        sys.stderr.flush()
        raw = sys.stdin.readline()
        if not raw:
            raise EOFError
        raw = raw.strip()
    except (EOFError, KeyboardInterrupt):
        sys.stderr.write("\n")
        sys.exit(0)
    return raw if raw else default


def _yes(prompt: str) -> bool:
    raw = _ask(f"{prompt} [y/n]:", "n").lower()
    return raw.startswith("y")


def _int(prompt: str, default: int = 0) -> int:
    raw = _ask(f"{prompt} [{default}]:", str(default))
    try:
        return int(raw)
    except ValueError:
        return default


def _print_banner():
    print(file=sys.stderr)
    print("  Apeirogon Logistics -- Contract Score Worksheet", file=sys.stderr)
    print(f"  {_DIVIDER}", file=sys.stderr)


def _print_result(result: dict):
    score = result["score"]
    rec = result["recommendation"].upper()
    risk = result["operational_risk"]
    confidence = result["confidence_level"]
    trace = result.get("weighted_decision_trace", [])
    warnings = result.get("warnings", [])
    unresolved = result.get("unresolved_fields", [])

    rec_display = {"ACCEPT": "ACCEPT", "DEFER": "DEFER", "REJECT": "REJECT"}.get(rec, rec)

    print()
    print(f"  {_DIVIDER}")
    print(f"  SCORE: {score}/100  --  {rec_display}")
    print(f"  Risk: {risk}  |  Confidence: {confidence}")
    print(f"  {_DIVIDER}")

    if trace:
        print()
        print("  Factor breakdown:")
        for entry in trace:
            label = _FACTOR_LABELS.get(entry["factor"], entry["factor"])
            effect = entry["weighted_effect"]
            mod_note = f"  (modifier {entry['modifier']}x)" if entry["modifier"] != 1.0 else ""
            print(f"    {effect:+.1f}  {label}{mod_note}")

    if unresolved:
        penalty = -min(12, len(unresolved) * 2)
        print(f"    {penalty:+.0f}  UNRESOLVED fields: {', '.join(unresolved)}")

    if warnings:
        print()
        print("  Warnings:")
        for w in warnings:
            print(f"    - {w}")

    print()


def _collect_input() -> dict:
    _print_banner()

    print(file=sys.stderr)
    print("  Ship and issuer", file=sys.stderr)
    print(file=sys.stderr)

    known_ships = sorted(SHIP_MODIFIERS.keys())
    known_issuers = sorted(ISSUER_MODIFIERS.keys())

    ship_hint = ", ".join(known_ships[:6]) + "..."
    issuer_hint = ", ".join(known_issuers)

    ship = _ask(f"Ship ({ship_hint}):").lower()
    issuer = _ask(f"Issuer ({issuer_hint}, or leave blank):").lower()

    print(file=sys.stderr)
    print("  Route", file=sys.stderr)
    print(file=sys.stderr)

    extra_same_pickup = _int(
        "Extra contracts at the same pickup (0 if only one contract):", 0
    )
    dest_overlap = _int(
        "Destination overlaps between contracts (0 if none):", 0
    )
    orbital = _yes("Does the whole route stay in orbital space (no atmosphere landings)?")
    delivery_stops = _int("Number of delivery stops (1 = single drop-off):", 1)
    atmos_stops = 0 if orbital else _int(
        "How many of those stops require an atmosphere landing?", 0
    )
    dead_leg = _yes("Do you need to fly empty to reach the pickup (dead leg)?")

    print(file=sys.stderr)
    print("  Cargo and handling", file=sys.stderr)
    print(file=sys.stderr)

    ship_suitable = _yes("Does your ship suit this cargo type well?")
    route_chaining = _yes("Do pickup locations chain well from one to the next?")
    panel_clarity = _yes("Do cargo panels assign cleanly to each delivery destination?")
    hard_freight = _yes("Is freight handling difficult (awkward boxes, heavy cargo)?")
    complex_unload = _yes("Is there a complex unloading sequence at the destination?")

    print(file=sys.stderr)
    print("  Risk factors", file=sys.stderr)
    print(file=sys.stderr)

    congested = _yes("Are there congested stations on the route?")
    tiring = _yes("Is this a tiring multi-leg route?")
    fragile = _yes("Does the route have fragile dependencies that could collapse?")

    print(file=sys.stderr)
    unresolved_count = _int(
        "How many fields could you not read (UNRESOLVED)? [0]:", 0
    )
    unresolved = [f"field_{i+1}" for i in range(unresolved_count)]

    # Build stops list for stop_density auto-computation
    stops = ["pickup"] + [f"delivery_{i+1}" for i in range(delivery_stops)]

    route = {
        "ship": ship,
        "same_pickup": extra_same_pickup,
        "destination_overlap": dest_overlap,
        "orbital_loop": 1 if orbital else 0,
        "dead_leg": 1 if dead_leg else 0,
        "fragmentation": max(0, delivery_stops - 1),
        "atmosphere": atmos_stops,
        "ship_suitability": 1 if ship_suitable else 0,
        "route_continuity": 1 if route_chaining else 0,
        "cargo_panel_clarity": 1 if panel_clarity else 0,
        "freight": 1 if hard_freight else 0,
        "unloading_cognitive_load": 1 if complex_unload else 0,
        "congestion": 1 if congested else 0,
        "fatigue": 1 if tiring else 0,
        "chain_collapse": 1 if fragile else 0,
        "stops": stops,
    }

    if issuer:
        route["issuer"] = issuer
    if unresolved:
        route["unresolved_fields"] = unresolved

    return route


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--json", action="store_true", help="Output raw JSON result")
    args = parser.parse_args()

    route = _collect_input()
    result = score_route(route)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        _print_result(result)


if __name__ == "__main__":
    main()
