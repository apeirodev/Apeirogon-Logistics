#!/usr/bin/env python3
import argparse
from pathlib import Path
from lib.common import dump_json, file_sha256

_EXCLUDED_PARTS = {".git", "__pycache__"}
_EXCLUDED_SUFFIXES = {".pyc", ".pyo"}

def main():
    parser = argparse.ArgumentParser(description="Generate release checksums")
    parser.add_argument("--root", default=".")
    parser.add_argument("--output", "-o", default="-")
    args = parser.parse_args()
    root = Path(args.root)
    files = {}
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        if any(part in _EXCLUDED_PARTS for part in p.parts):
            continue
        if p.suffix in _EXCLUDED_SUFFIXES:
            continue
        files[str(p.relative_to(root))] = file_sha256(p)
    dump_json({"files": files, "file_count": len(files)}, args.output)
if __name__ == "__main__":
    main()
