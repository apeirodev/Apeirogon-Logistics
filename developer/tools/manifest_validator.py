#!/usr/bin/env python3
"""
Validate manifest files -- check that every file path referenced in a manifest
actually exists on disk.

--root      Directory to search for *manifest*.json files (default: .)
--base      Directory against which referenced file paths are resolved
            (default: same as --root)
--exclude   Comma-separated glob patterns to skip (e.g. "tests/*,fixtures/*")
--output    Output JSON path (default: stdout)
"""
from __future__ import annotations
import argparse
import fnmatch
import json
import re
import sys
from pathlib import Path
from lib.common import dump_json

PATH_RE = re.compile(r"[\w./-]+\.(?:json|md|py|txt|yml|yaml|zip)$")


def candidate_paths(obj):
    found = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            found.extend(candidate_paths(v))
    elif isinstance(obj, list):
        for item in obj:
            found.extend(candidate_paths(item))
    elif isinstance(obj, str):
        for m in PATH_RE.findall(obj):
            if not m.startswith("http") and not m.startswith("sandbox:"):
                found.append(m)
    return found


def is_excluded(path_rel: str, patterns: list[str]) -> bool:
    for pat in patterns:
        if fnmatch.fnmatch(path_rel, pat):
            return True
    return False


def main():
    parser = argparse.ArgumentParser(description="Validate manifest file references")
    parser.add_argument("--root", default=".", help="Directory to search for manifest files")
    parser.add_argument("--base", default=None,
                        help="Base directory to resolve referenced paths against (default: same as --root)")
    parser.add_argument("--exclude", default="",
                        help="Comma-separated glob patterns of manifest files to skip")
    parser.add_argument("--output", "-o", default="-")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    base = Path(args.base).resolve() if args.base else root
    exclude_patterns = [p.strip() for p in args.exclude.split(",") if p.strip()]

    findings = []
    for m in sorted(root.rglob("*manifest*.json")):
        if ".git" in m.parts:
            continue
        rel = str(m.relative_to(root))
        if is_excluded(rel, exclude_patterns):
            continue
        try:
            data = json.loads(m.read_text(encoding="utf-8"))
            refs = sorted(set(candidate_paths(data)))
            missing = [r for r in refs if not (base / r).exists()]
            findings.append({
                "manifest": rel,
                "valid": not missing,
                "reference_count": len(refs),
                "missing_references": missing[:100],
            })
        except Exception as e:
            print(f"manifest error: {e}", file=sys.stderr)
            findings.append({
                "manifest": rel,
                "valid": False,
                "error": "manifest read error",
            })

    dump_json({
        "valid": all(f["valid"] for f in findings),
        "manifest_count": len(findings),
        "findings": findings,
    }, args.output)


if __name__ == "__main__":
    main()
