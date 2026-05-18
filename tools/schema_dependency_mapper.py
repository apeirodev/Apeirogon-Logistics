#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from lib.common import dump_json

def refs(obj):
    found = []
    if isinstance(obj, dict):
        if "$ref" in obj:
            found.append(obj["$ref"])
        for v in obj.values():
            found.extend(refs(v))
    elif isinstance(obj, list):
        for x in obj:
            found.extend(refs(x))
    return found

def main():
    parser = argparse.ArgumentParser(description="Map schema dependencies")
    parser.add_argument("--root", default="schema")
    parser.add_argument("--output", "-o", default="-")
    args = parser.parse_args()
    root = Path(args.root)
    mapping = {}
    for p in sorted(root.rglob("*.json")):
        try:
            mapping[str(p)] = refs(json.loads(p.read_text(encoding="utf-8")))
        except Exception as e:
            mapping[str(p)] = [f"INVALID_JSON:{e}"]
    dump_json({"schema_dependency_map": mapping}, args.output)

if __name__ == "__main__":
    main()
