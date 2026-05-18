#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re
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

def main():
    parser = argparse.ArgumentParser(description="Validate manifest references")
    parser.add_argument("--root", default=".")
    parser.add_argument("--output", "-o", default="-")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    findings = []
    for m in sorted(root.rglob("*manifest*.json")):
        if ".git" in m.parts:
            continue
        try:
            data = json.loads(m.read_text(encoding="utf-8"))
            refs = sorted(set(candidate_paths(data)))
            missing = [r for r in refs if not (root / r).exists()]
            findings.append({"manifest": str(m.relative_to(root)), "valid": not missing, "reference_count": len(refs), "missing_references": missing[:100]})
        except Exception as e:
            findings.append({"manifest": str(m.relative_to(root)), "valid": False, "error": str(e)})
    dump_json({"valid": all(f["valid"] for f in findings), "manifest_count": len(findings), "findings": findings}, args.output)

if __name__ == "__main__":
    main()
