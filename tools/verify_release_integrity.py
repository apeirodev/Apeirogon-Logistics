#!/usr/bin/env python3
"""
Verify release integrity by comparing a checksum manifest against actual files.

Accepts a manifest produced by generate_release_checksums.py:
  {"files": {"relative/path": "sha256hex", ...}}

Reports:
  - files whose on-disk hash does not match the manifest
  - files listed in the manifest that are missing on disk
  - files on disk (relative to --root) that are absent from the manifest
"""
import argparse
import hmac
from pathlib import Path
from lib.common import dump_json, file_sha256, load_json


def verify(manifest_data, root: Path):
    recorded = manifest_data.get("files")
    if not isinstance(recorded, dict):
        return {
            "valid": False,
            "error": "manifest missing 'files' dict",
            "file_count": 0,
            "mismatches": [],
            "missing_from_disk": [],
            "untracked_on_disk": [],
        }

    mismatches = []
    missing_from_disk = []

    for rel_path, expected_hash in sorted(recorded.items()):
        candidate = (root / rel_path).resolve()
        if not candidate.exists():
            missing_from_disk.append(rel_path)
            continue
        actual = file_sha256(candidate)
        if not hmac.compare_digest(actual, expected_hash):
            mismatches.append({
                "path": rel_path,
                "expected": expected_hash,
                "actual": actual,
            })

    # Find files on disk not in the manifest
    recorded_set = set(recorded.keys())
    untracked = []
    for p in sorted(root.rglob("*")):
        if p.is_file() and ".git" not in p.parts:
            rel = str(p.relative_to(root))
            if rel not in recorded_set:
                untracked.append(rel)

    valid = not mismatches and not missing_from_disk
    return {
        "valid": valid,
        "file_count": len(recorded),
        "mismatches": mismatches,
        "mismatch_count": len(mismatches),
        "missing_from_disk": missing_from_disk,
        "missing_count": len(missing_from_disk),
        "untracked_on_disk": untracked,
        "untracked_count": len(untracked),
    }


def main():
    parser = argparse.ArgumentParser(description="Verify release integrity manifest against disk")
    parser.add_argument("--input", "-i", default="-", help="Checksum manifest JSON (default: stdin)")
    parser.add_argument("--output", "-o", default="-", help="Verification report JSON (default: stdout)")
    parser.add_argument("--root", default=".", help="Root directory to resolve file paths against")
    args = parser.parse_args()
    manifest = load_json(args.input)
    root = Path(args.root).resolve()
    dump_json(verify(manifest, root), args.output)


if __name__ == "__main__":
    main()
