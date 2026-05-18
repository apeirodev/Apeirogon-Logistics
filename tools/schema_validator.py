#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from lib.common import dump_json, validate_governance_metadata

def find_refs(obj, refs):
    if isinstance(obj, dict):
        if "$ref" in obj:
            refs.append(str(obj["$ref"]))
        for v in obj.values():
            find_refs(v, refs)
    elif isinstance(obj, list):
        for item in obj:
            find_refs(item, refs)

def resolve_ref(root: Path, current: Path, ref: str) -> bool:
    if ref.startswith("#"):
        return True
    candidate = (current.parent / ref).resolve()
    if candidate.exists():
        return True
    candidate = (root / ref).resolve()
    return candidate.exists()

def validate_tree(root: Path):
    results = []
    for path in sorted(root.rglob("*.json")):
        if ".git" in path.parts:
            continue
        record = {"path": str(path.relative_to(root)), "valid_json": True, "refs": [], "missing_refs": []}
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            refs = []
            find_refs(data, refs)
            record["refs"] = refs
            record["missing_refs"] = [r for r in refs if not resolve_ref(root, path, r)]
            if isinstance(data, dict) and "governance_metadata" in data:
                ok, problems = validate_governance_metadata(data["governance_metadata"])
                record["governance_metadata_valid"] = ok
                record["governance_metadata_problems"] = problems
        except Exception as e:
            record["valid_json"] = False
            record["error"] = str(e)
        results.append(record)
    return {
        "valid": all(r.get("valid_json") and not r.get("missing_refs") for r in results),
        "file_count": len(results),
        "results": results
    }

def main():
    parser = argparse.ArgumentParser(description="Recursive JSON/schema validator")
    parser.add_argument("--root", default=".")
    parser.add_argument("--output", "-o", default="-")
    args = parser.parse_args()
    dump_json(validate_tree(Path(args.root).resolve()), args.output)

if __name__ == "__main__":
    main()
