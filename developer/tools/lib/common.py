#!/usr/bin/env python3
from __future__ import annotations
import argparse
import hashlib
import json
import logging
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple

logger = logging.getLogger(__name__)

REQUIRED_GOVERNANCE_FIELDS = [
    "source_class",
    "provenance_chain",
    "confidence_level",
    "verification_status",
    "patch_era",
    "telemetry_support_level",
    "operational_assurance_state",
    "unresolved_field_list",
    "advisory_only",
    "contributor_trust_tier",
    "derivation_type",
]

TRUST_TIERS = ["T0", "T1", "T2", "T3", "T4"]
ASSURANCE_STATES = ["designed", "implemented", "operational", "validated", "community_validated"]

class ToolError(Exception):
    pass

_MAX_INPUT_BYTES = 10 * 1024 * 1024  # 10 MB -- WARN-02


def load_json(path: str | Path | None = None) -> Any:
    if path is None or str(path) == "-":
        return json.load(sys.stdin)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def safe_load_json(path: str | Path) -> Any:
    """Load JSON from a file, enforcing a 10 MB size cap (WARN-02).

    Raises ValueError if the file exceeds _MAX_INPUT_BYTES.
    Always reads from a named file path, never from stdin.
    """
    p = Path(path)
    size = p.stat().st_size
    if size > _MAX_INPUT_BYTES:
        raise ValueError(
            f"Input file too large: {size} bytes (limit {_MAX_INPUT_BYTES} bytes): {path}"
        )
    return json.loads(p.read_text(encoding="utf-8"))

def dump_json(data: Any, path: str | Path | None = None, skip_path_check: bool = False) -> None:
    """Serialize data as indented JSON and write to path or stdout.

    When path is an explicit file path (not None or "-"), this function
    enforces FILE-01 by calling safe_write_path() before writing. Pass
    skip_path_check=True only in internal tool contexts where the path is
    constructed from trusted, hard-coded sources (e.g. release tooling that
    writes to a fixed output directory under developer/).
    """
    text = json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if path is None or str(path) == "-":
        sys.stdout.write(text)
    else:
        if not skip_path_check:
            safe_write_path(str(path))
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

def stable_hash(data: Any) -> str:
    encoded = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()

def hash_payload(data: Any) -> str:
    return stable_hash(data)

def file_sha256(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

_ALLOWED_WRITE_ROOTS: list[Path] = [Path("output"), Path("exports"), Path("telemetry")]

def safe_write_path(raw_path: str, allowed_roots: list[Path] | None = None) -> Path:
    """Validate that raw_path resolves within one of the allowed write roots (FILE-01).

    Always pass the user-supplied --output path through this function before
    writing to it. Stdout (raw_path == "-") is unconditionally safe and is
    returned as the sentinel Path("-") without further validation.

    Raises ValueError for paths that escape the allowed roots.
    """
    if raw_path == "-":
        return Path("-")
    roots = allowed_roots if allowed_roots is not None else _ALLOWED_WRITE_ROOTS
    p = Path(raw_path).resolve()
    for root in roots:
        if p.is_relative_to(root.resolve()):
            return p
    raise ValueError(f"Output path outside allowed write roots: {raw_path}")

def collect_unresolved(data: Any) -> List[str]:
    fields: List[str] = []
    if isinstance(data, dict):
        for k, v in data.items():
            key = str(k)
            kl = key.lower()
            if "unresolved" in kl:
                if isinstance(v, list):
                    fields.extend(str(x) for x in v)
                elif v not in (None, "", []):
                    fields.append(str(v))
                else:
                    fields.append(key)
            elif v in (None, "", "UNRESOLVED", "unknown", "UNKNOWN"):
                fields.append(key)
            fields.extend(collect_unresolved(v))
    elif isinstance(data, list):
        for item in data:
            fields.extend(collect_unresolved(item))
    return sorted(set(x for x in fields if x))

def normalize_patch(data: Dict[str, Any], override: str | None = None) -> str:
    return override or data.get("patch_version") or data.get("patch_era") or "UNRESOLVED"

def governance_metadata(
    source_class: str,
    patch_era: str = "UNRESOLVED",
    unresolved: List[str] | None = None,
    provenance: List[Dict[str, Any]] | None = None,
    confidence_level: str | None = None,
    verification_status: str = "not_human_verified",
    telemetry_support_level: str = "none",
    contributor_trust_tier: str = "T0",
    derivation_type: str = "deterministic",
    advisory_only: bool = True,
    assurance_state: str = "implemented",
) -> Dict[str, Any]:
    unresolved = sorted(set(unresolved or []))
    if confidence_level is None:
        confidence_level = "medium" if unresolved else "high"
    return {
        "source_class": source_class,
        "provenance_chain": provenance or [],
        "confidence_level": confidence_level,
        "verification_status": verification_status,
        "patch_era": patch_era,
        "telemetry_support_level": telemetry_support_level,
        "operational_assurance_state": assurance_state,
        "unresolved_field_list": unresolved,
        "advisory_only": advisory_only,
        "contributor_trust_tier": contributor_trust_tier,
        "derivation_type": derivation_type,
    }

def ensure_metadata(data: Dict[str, Any], source_class: str = "deterministic_output") -> Dict[str, Any]:
    meta = data.get("governance_metadata")
    if not isinstance(meta, dict):
        meta = governance_metadata(
            source_class=source_class,
            patch_era=normalize_patch(data),
            unresolved=collect_unresolved(data),
            provenance=[{"type": "payload_hash", "sha256": stable_hash(data)}],
        )
        data["governance_metadata"] = meta
    return data

def validate_governance_metadata(meta: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate governance metadata fields.

    Fails closed on unexpected exceptions (ERR-01): any exception during
    validation returns (False, ["validation_error_fail_closed"]) rather than
    allowing untrusted data to pass.
    """
    try:
        return _validate_governance_metadata_inner(meta)
    except Exception as exc:
        logger.error("Governance validation error: %s", exc)
        return False, ["validation_error_fail_closed"]


def _validate_governance_metadata_inner(meta: Dict[str, Any]) -> Tuple[bool, List[str]]:
    problems = []
    missing = [field for field in REQUIRED_GOVERNANCE_FIELDS if field not in meta]
    if missing:
        problems.append("missing fields: " + ", ".join(missing))
    if meta.get("contributor_trust_tier") not in TRUST_TIERS:
        problems.append("invalid contributor_trust_tier")
    if meta.get("operational_assurance_state") not in ASSURANCE_STATES:
        problems.append("invalid operational_assurance_state")
    if meta.get("advisory_only") is not True:
        problems.append("advisory_only must be true")
    if not isinstance(meta.get("provenance_chain", []), list):
        problems.append("provenance_chain must be a list")
    if not isinstance(meta.get("unresolved_field_list", []), list):
        problems.append("unresolved_field_list must be a list")
    return len(problems) == 0, problems

def validate_metadata(meta: Dict[str, Any]) -> Tuple[bool, List[str]]:
    return validate_governance_metadata(meta)

def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--input", "-i", default="-", help="Input JSON path, default stdin")
    parser.add_argument("--output", "-o", default="-", help="Output JSON path, default stdout")
    parser.add_argument("--patch-version", default=None, help="Patch version override")
    parser.add_argument("--dry-run", action="store_true", help="Do not write side-effect files")

def parse_positive_number(value: Any) -> float | None:
    if value is None:
        return None
    match = re.search(r"[-+]?\d+(?:\.\d+)?", str(value).replace(",", ""))
    if not match:
        return None
    num = float(match.group(0))
    return num if num > 0 else None

def normalize_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()

def structured_error(message: str, remediation: str | None = None) -> Dict[str, Any]:
    return {"valid": False, "error": message, "remediation": remediation}

def timestamp() -> int:
    return int(time.time())


_INJECTION_PATTERNS = [
    r"ignore\s+(previous|above|all)\s+instructions",
    r"system\s*:",
    r"<\s*/?system\s*>",
    r"\bact\s+as\b",
    r"\byou\s+are\s+now\b",
]


def check_injection_risk(value: str) -> bool:
    """Return True if value contains a probable prompt injection attempt (LLM01)."""
    if not isinstance(value, str):
        return False
    lower = value.lower()
    return any(re.search(p, lower) for p in _INJECTION_PATTERNS)
