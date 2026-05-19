#!/usr/bin/env python3
"""
Sync the canonical scoring instruction block across all player SETUP files.

Canonical template: developer/templates/scoring_instruction_block.md
SETUP files:        player/project_instructions/SETUP_*.md

Each SETUP file contains the instruction block between a bare triple-backtick
fence pair (``` with no language tag). This tool locates that fence pair and:

  --check  verify all SETUP files match the canonical template
           exits 1 if any file differs or has no fence
  --write  overwrite the block in all SETUP files from the canonical template
"""
import argparse
import re
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_TEMPLATE = _REPO / "developer" / "templates" / "scoring_instruction_block.md"
_SETUP_DIR = _REPO / "player" / "project_instructions"
_SETUP_GLOB = "SETUP_*.md"

_FENCE_RE = re.compile(r"(```\n)(.*?)(```)", re.DOTALL)


def _load_template() -> str:
    if not _TEMPLATE.exists():
        print(f"ERROR: canonical template not found: {_TEMPLATE}", file=sys.stderr)
        sys.exit(1)
    return _TEMPLATE.read_text(encoding="utf-8")


def _extract_block(content: str) -> str | None:
    m = _FENCE_RE.search(content)
    return m.group(2) if m else None


def _inject_block(content: str, canonical: str) -> str:
    def _replace(m):
        return m.group(1) + canonical + m.group(3)
    return _FENCE_RE.sub(_replace, content, count=1)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true",
                      help="Check all SETUP files match canonical template (exits 1 if any differ)")
    mode.add_argument("--write", action="store_true",
                      help="Overwrite block in all SETUP files from canonical template")
    args = parser.parse_args()

    canonical = _load_template()
    setup_files = sorted(_SETUP_DIR.glob(_SETUP_GLOB))

    if not setup_files:
        print(f"ERROR: no SETUP files found in {_SETUP_DIR}", file=sys.stderr)
        sys.exit(1)

    problems = []

    for path in setup_files:
        content = path.read_text(encoding="utf-8")
        current = _extract_block(content)

        if current is None:
            problems.append(f"{path.name}: no code fence found")
            continue

        if current == canonical:
            print(f"ok: {path.name}")
            continue

        if args.write:
            path.write_text(_inject_block(content, canonical), encoding="utf-8")
            print(f"updated: {path.name}")
        else:
            problems.append(f"{path.name}: block differs from canonical template")

    if problems:
        for msg in problems:
            print(f"FAIL: {msg}", file=sys.stderr)
        sys.exit(1)

    if args.check:
        print(f"all {len(setup_files)} SETUP files match canonical template")
    else:
        print(f"sync complete: {len(setup_files)} files processed")


if __name__ == "__main__":
    main()
