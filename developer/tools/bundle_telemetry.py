#!/usr/bin/env python3
"""
Bundle telemetry JSON files into a dated zip for optional submission.

Usage:
  python tools/bundle_telemetry.py --input-dir telemetry/ --output-dir exports/
  python tools/bundle_telemetry.py --input-dir telemetry/ --output telemetry_bundle_2024.zip
"""
from __future__ import annotations
import argparse
import json
import logging
import sys
import time
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import safe_write_path

logger = logging.getLogger(__name__)

_MAX_FILE_BYTES = 10 * 1024 * 1024  # 10 MB per file


def _is_telemetry_file(path: Path) -> bool:
    return path.suffix == ".json" and path.is_file()


def _safe_load_json(path: Path) -> tuple[dict | None, str | None]:
    if path.stat().st_size > _MAX_FILE_BYTES:
        return None, f"file too large ({path.stat().st_size} bytes)"
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except Exception as exc:
        # ERR-02: full detail goes to the log, only a generic reason to output
        logger.error("Could not load telemetry file %s: %s", path, exc, exc_info=True)
        return None, "unreadable or invalid JSON"


def _sanitize_record(record: dict) -> dict:
    """Remove fields that should not leave the local machine."""
    STRIP_KEYS = {"api_key", "token", "secret", "password", "credential", "key"}
    return {
        k: "[REDACTED]" if any(s in k.lower() for s in STRIP_KEYS) else v
        for k, v in record.items()
    }


def bundle(input_dir: str, output_path: str) -> dict:
    root = Path(input_dir)
    if not root.exists():
        return {"error": f"input directory does not exist: {input_dir}", "bundled": 0}

    files = sorted(p for p in root.rglob("*.json") if _is_telemetry_file(p))
    if not files:
        return {"error": f"no JSON files found in {input_dir}", "bundled": 0}

    bundled: list[str] = []
    skipped: list[dict] = []
    manifest_entries: list[dict] = []

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            record, err = _safe_load_json(f)
            if err:
                skipped.append({"file": str(f.relative_to(root)), "reason": err})
                continue

            sanitized = _sanitize_record(record)
            arcname = str(f.relative_to(root))
            zf.writestr(arcname, json.dumps(sanitized, indent=2, sort_keys=True))
            bundled.append(arcname)
            manifest_entries.append({
                "file": arcname,
                "ship": record.get("ship", "UNRESOLVED"),
                "issuer": record.get("issuer", "UNRESOLVED"),
                "patch_version": record.get("patch_version", "UNRESOLVED"),
            })

        # Write a bundle manifest inside the zip
        manifest = {
            "bundle_created_epoch": int(time.time()),
            "file_count": len(bundled),
            "entries": manifest_entries,
            "submission_note": (
                "This bundle was created by tools/bundle_telemetry.py. "
                "Submission is opt-in. Review contents before sharing."
            ),
        }
        zf.writestr("_BUNDLE_MANIFEST.json", json.dumps(manifest, indent=2, sort_keys=True))

    return {
        "output": str(out),
        "bundled": len(bundled),
        "skipped": skipped,
        "manifest_entries": manifest_entries,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Bundle telemetry JSON files into a zip for optional submission"
    )
    parser.add_argument(
        "--input-dir", "-i", default="telemetry",
        help="Directory containing telemetry JSON files (default: telemetry/)"
    )
    parser.add_argument(
        "--output", "-o", default=None,
        help="Output zip path. Defaults to exports/telemetry_bundle_<epoch>.zip"
    )
    args = parser.parse_args()

    output_path = args.output or f"exports/telemetry_bundle_{int(time.time())}.zip"
    # FILE-01: the CLI-supplied output path must stay inside the allowed roots
    try:
        validated_output = safe_write_path(output_path)
    except ValueError:
        print(f"Error: output path outside allowed write roots: {output_path}")
        sys.exit(1)
    result = bundle(args.input_dir, str(validated_output))

    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Bundled {result['bundled']} files → {result['output']}")
        if result["skipped"]:
            print(f"Skipped {len(result['skipped'])} files:")
            for s in result["skipped"]:
                print(f"  {s['file']}: {s['reason']}")
        print("Review the bundle before submitting. Submission is always opt-in.")


if __name__ == "__main__":
    main()
