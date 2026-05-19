#!/usr/bin/env python3
"""
Sync player/uploads/ JSON files from their canonical developer sources.

Each player upload JSON is an exact copy of a developer file, distinguished
only by a _copy_note field that identifies the canonical path and reminds
maintainers to keep both in sync. This tool reads each canonical file,
preserves the existing _copy_note in the player copy, and writes the result.

Canonical sources and their player copies:
  developer/runtime/scoring_config.json        -> player/uploads/scoring_config.json
  developer/runtime/OCR_normalization_rules.json -> player/uploads/OCR_normalization_rules.json
  developer/analytics/mission_issuer_profiles.json -> player/uploads/mission_issuer_profiles.json
  developer/schema/mission_schema.json          -> player/uploads/mission_schema.json
  developer/data/ship_profiles.json             -> player/uploads/ship_profiles.json

Usage:
  python tools/sync_player_uploads.py --check   # exits 1 if any copy differs from canonical
  python tools/sync_player_uploads.py --write   # update all player copies from canonical
"""
import argparse
import json
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent

# (canonical_path_relative_to_repo, player_copy_path_relative_to_repo)
_PAIRS = [
    ("developer/runtime/scoring_config.json",
     "player/uploads/scoring_config.json"),

    ("developer/runtime/OCR_normalization_rules.json",
     "player/uploads/OCR_normalization_rules.json"),

    ("developer/analytics/mission_issuer_profiles.json",
     "player/uploads/mission_issuer_profiles.json"),

    ("developer/schema/mission_schema.json",
     "player/uploads/mission_schema.json"),

    ("developer/data/ship_profiles.json",
     "player/uploads/ship_profiles.json"),
]


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _dump_json(data: dict, path: Path) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _canonical_matches_copy(canonical: dict, copy: dict) -> bool:
    """Return True if copy equals canonical when _copy_note is stripped from both."""
    canonical_data = {k: v for k, v in canonical.items() if k != "_copy_note"}
    copy_data = {k: v for k, v in copy.items() if k != "_copy_note"}
    return copy_data == canonical_data


def _build_synced(canonical: dict, existing_copy: dict) -> dict:
    """Return canonical data with _copy_note preserved from the existing copy."""
    result = dict(canonical)
    if "_copy_note" in existing_copy:
        result["_copy_note"] = existing_copy["_copy_note"]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true",
                      help="Check all player copies match canonical (exits 1 if any differ)")
    mode.add_argument("--write", action="store_true",
                      help="Update all player copies from canonical, preserving _copy_note")
    args = parser.parse_args()

    problems = []

    for canonical_rel, copy_rel in _PAIRS:
        canonical_path = _REPO / canonical_rel
        copy_path = _REPO / copy_rel
        name = copy_path.name

        if not canonical_path.exists():
            problems.append(f"{name}: canonical not found: {canonical_rel}")
            continue
        if not copy_path.exists():
            problems.append(f"{name}: player copy not found: {copy_rel}")
            continue

        canonical = _load_json(canonical_path)
        copy = _load_json(copy_path)

        if _canonical_matches_copy(canonical, copy):
            print(f"ok: {name}")
            continue

        if args.write:
            _dump_json(_build_synced(canonical, copy), copy_path)
            print(f"updated: {name}")
        else:
            problems.append(f"{name}: player copy differs from canonical ({canonical_rel})")

    if problems:
        for msg in problems:
            print(f"FAIL: {msg}", file=sys.stderr)
        sys.exit(1)

    if args.check:
        print(f"all {len(_PAIRS)} player upload files match canonical sources")
    else:
        print(f"sync complete: {len(_PAIRS)} files processed")


if __name__ == "__main__":
    main()
