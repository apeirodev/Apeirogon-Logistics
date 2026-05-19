#!/usr/bin/env python3
"""
Validate that numeric values in the scoring instruction template match
the corresponding weights and modifiers in scoring_config.json.

Checks base weights, score thresholds, modifier multipliers, and
computed effective values (e.g. Covalex issuer alignment = base * 1.10).

Reports any mismatch between the template text and the config so that
updating scoring_config.json without updating the template fails CI.

Usage:
  python tools/validate_scoring_numbers.py
  python tools/validate_scoring_numbers.py | python -c "import json,sys; d=json.load(sys.stdin); assert d['valid'], d"
"""
import json
import re
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_CONFIG = _REPO / "developer" / "runtime" / "scoring_config.json"
_TEMPLATE = _REPO / "developer" / "templates" / "scoring_instruction_block.md"

# Unicode minus sign used in the template for negative values.
_MINUS = "−"
# Regex fragment matching either Unicode minus or ASCII hyphen-minus.
_M = rf"[{_MINUS}\-]"
# Regex fragment matching either Unicode multiplication sign or ASCII x.
_X = r"[x×]"


def _get(config, path):
    """Retrieve a nested value using a dot-separated path string."""
    node = config
    for key in path.split("."):
        node = node[key]
    return node


# Each check is a tuple of:
#   (label, template_regex, expected_value_fn, value_type)
# label:            human-readable name for the check
# template_regex:   pattern with one capture group for the number in the template
# expected_value_fn: callable(config) -> int or float
# value_type:       "int" or "float"
_CHECKS = [
    # Score structure
    ("base_score",
     r"Start at (\d+) points",
     lambda c: c["base_score"], "int"),

    ("accept_threshold",
     r"(\d+) or above = Accept",
     lambda c: c["score_bands"]["accept_threshold"], "int"),

    ("defer_threshold",
     r"(\d+) to \d+ = Defer",
     lambda c: c["score_bands"]["defer_threshold"], "int"),

    # Good factors — base weights
    ("same_pickup",
     r"same pickup[^+]+\+(\d+)",
     lambda c: c["default_weights"]["same_pickup"], "int"),

    ("destination_overlap",
     r"overlap between contracts[^+]+\+(\d+)",
     lambda c: c["default_weights"]["destination_overlap"], "int"),

    ("orbital_loop_base",
     r"orbital space[^+]+\+(\d+)",
     lambda c: c["default_weights"]["orbital_loop"], "int"),

    ("orbital_loop_covalex_mult",
     rf"orbital space.*?{_X}([\d.]+) for Covalex",
     lambda c: c["issuer_modifiers"]["covalex"]["orbital_loop"], "float"),

    ("ship_suitability",
     r"cargo type well[^+]+\+(\d+)",
     lambda c: c["default_weights"]["ship_suitability"], "int"),

    ("route_continuity",
     r"chain well[^+]+\+(\d+)",
     lambda c: c["default_weights"]["route_continuity"], "int"),

    ("cargo_panel_clarity_base",
     r"assign cleanly[^+]+\+(\d+)",
     lambda c: c["default_weights"]["cargo_panel_clarity"], "int"),

    ("cargo_panel_clarity_hull_b_mult",
     rf"assign cleanly.*?{_X}([\d.]+) for Hull-B",
     lambda c: c["ship_modifiers"]["hull-b"]["cargo_panel_clarity"], "float"),

    # Covalex issuer alignment: effective value = base * covalex modifier
    ("covalex_issuer_alignment_effective",
     r"Covalex issuer alignment[^+]+\+(\d+)",
     lambda c: round(
         c["default_weights"]["issuer_alignment"]
         * c["issuer_modifiers"]["covalex"]["issuer_alignment"]
     ), "int"),

    # Bad factors — base weights (template shows absolute values)
    ("dead_leg_base",
     rf"fly empty[^{_MINUS}\-]+{_M}(\d+)",
     lambda c: abs(c["default_weights"]["dead_leg"]), "int"),

    ("dead_leg_red_wind_mult",
     rf"fly empty[^x×]+{_X}([\d.]+) for Red Wind",
     lambda c: c["issuer_modifiers"]["red wind"]["dead_leg"], "float"),

    ("chain_collapse",
     rf"fragile dependencies[^{_MINUS}\-]+{_M}(\d+)",
     lambda c: abs(c["default_weights"]["chain_collapse"]), "int"),

    ("fragmentation_hull_b",
     rf"stop beyond the first[^{_MINUS}\-]+{_M}(\d+) \(Hull",
     lambda c: round(
         abs(c["default_weights"]["fragmentation"])
         * c["ship_modifiers"]["hull-b"]["fragmentation"]
     ), "int"),

    ("fragmentation_base",
     rf"stop beyond the first.*?or {_M}(\d+) \(other",
     lambda c: abs(c["default_weights"]["fragmentation"]), "int"),

    ("atmosphere",
     rf"atmospheric landing[^{_MINUS}\-]+{_M}(\d+)",
     lambda c: abs(c["default_weights"]["atmosphere"]), "int"),

    ("congestion",
     rf"Congested stations[^{_MINUS}\-]+{_M}(\d+)",
     lambda c: abs(c["default_weights"]["congestion"]), "int"),

    ("freight",
     rf"freight handling[^{_MINUS}\-]+{_M}(\d+)",
     lambda c: abs(c["default_weights"]["freight"]), "int"),

    ("unloading_cognitive_load",
     rf"unloading sequence[^{_MINUS}\-]+{_M}(\d+)",
     lambda c: abs(c["default_weights"]["unloading_cognitive_load"]), "int"),

    ("stop_density",
     rf"stop beyond 2[^{_MINUS}\-]+{_M}(\d+)",
     lambda c: abs(c["default_weights"]["stop_density"]), "int"),

    ("fatigue",
     rf"multi-leg route[^{_MINUS}\-]+{_M}(\d+)",
     lambda c: abs(c["default_weights"]["fatigue"]), "int"),
]


def _parse_number(raw: str, value_type: str):
    return float(raw) if value_type == "float" else int(raw)


def validate(config: dict, template: str) -> dict:
    mismatches = []
    not_found = []

    for label, pattern, expected_fn, vtype in _CHECKS:
        try:
            expected = expected_fn(config)
        except (KeyError, TypeError) as e:
            mismatches.append({
                "check": label,
                "error": f"config lookup failed: {e}",
            })
            continue

        m = re.search(pattern, template)
        if m is None:
            not_found.append({"check": label, "pattern": pattern})
            continue

        found = _parse_number(m.group(1), vtype)

        if vtype == "float":
            ok = abs(found - expected) < 0.001
        else:
            ok = found == expected

        if not ok:
            mismatches.append({
                "check": label,
                "expected": expected,
                "found_in_template": found,
            })

    valid = not mismatches and not not_found
    return {
        "valid": valid,
        "check_count": len(_CHECKS),
        "mismatch_count": len(mismatches),
        "not_found_count": len(not_found),
        "mismatches": mismatches,
        "not_found": not_found,
    }


def main():
    if not _CONFIG.exists():
        print(json.dumps({"valid": False, "error": f"config not found: {_CONFIG}"}))
        sys.exit(1)
    if not _TEMPLATE.exists():
        print(json.dumps({"valid": False, "error": f"template not found: {_TEMPLATE}"}))
        sys.exit(1)

    config = json.loads(_CONFIG.read_text(encoding="utf-8"))
    template = _TEMPLATE.read_text(encoding="utf-8")

    result = validate(config, template)
    print(json.dumps(result, indent=2))

    if not result["valid"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
