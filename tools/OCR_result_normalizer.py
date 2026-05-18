#!/usr/bin/env python3
import argparse
import json
import logging
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import add_common_args, dump_json, governance_metadata, load_json, normalize_patch, normalize_text, parse_positive_number, stable_hash

logger = logging.getLogger(__name__)

_RULES_PATH = Path(__file__).parent.parent / "runtime" / "OCR_normalization_rules.json"

_FALLBACK_ISSUER_ALIASES = {
    "cov alex": "Covalex",
    "covalex": "Covalex",
    "ling family": "Ling Family",
    "ling": "Ling Family",
    "red wind": "Red Wind",
}

_FALLBACK_CONFIDENCE_THRESHOLD = 0.65


def _load_rules() -> dict:
    if _RULES_PATH.exists():
        try:
            return json.loads(_RULES_PATH.read_text(encoding="utf-8"))
        except Exception as exc:
            logger.warning("Could not load OCR_normalization_rules.json: %s — using built-in defaults", exc)
    return {}


_RULES = _load_rules()
_ISSUER_ALIASES: dict = _RULES.get("issuer_aliases") or _FALLBACK_ISSUER_ALIASES
_LOCATION_ALIASES: dict = _RULES.get("location_aliases") or {}
_CONFIDENCE_THRESHOLD: float = (
    _RULES.get("ocr_ambiguity_handling", {}).get("minimum_confidence_threshold")
    or _FALLBACK_CONFIDENCE_THRESHOLD
)


def resolve_location(text: str) -> str | None:
    if not text:
        return None
    for alias, canonical in _LOCATION_ALIASES.items():
        if alias.lower() in text.lower():
            return canonical
    return None


def normalize_ocr(data: dict) -> dict:
    raw = data.get("raw_text") or data.get("text") or ""
    text = normalize_text(raw)
    lower = text.lower()

    issuer = None
    for alias, canonical in _ISSUER_ALIASES.items():
        if alias in lower:
            issuer = canonical
            break

    scu_candidates = []
    for m in re.finditer(r"(\d+(?:\.\d+)?)\s*(?:SCU|scu)", text):
        val = parse_positive_number(m.group(1))
        if val is not None:
            scu_candidates.append(val)

    confidence = data.get("confidence", data.get("ocr_confidence"))
    try:
        confidence = float(confidence) if confidence is not None else None
    except Exception:
        confidence = None

    unresolved = list(data.get("unresolved_fields", []))
    warnings = []

    if not text:
        unresolved.append("raw_text")
        warnings.append("No OCR text provided.")
    if issuer is None:
        unresolved.append("issuer")
        warnings.append("Issuer unresolved.")
    if not scu_candidates:
        unresolved.append("SCU")
    if confidence is not None and confidence < _CONFIDENCE_THRESHOLD:
        warnings.append("Low OCR confidence.")
    if "ignore previous" in lower or "system prompt" in lower:
        warnings.append("Potential prompt-injection text detected; treat OCR strictly as data.")

    result = {
        "normalized_text": text,
        "issuer": issuer or "UNRESOLVED",
        "scu_candidates": scu_candidates,
        "ocr_confidence": confidence if confidence is not None else "UNRESOLVED",
        "ambiguity_level": "high" if len(set(unresolved)) >= 2 else "medium" if unresolved else "low",
        "warnings": sorted(set(warnings)),
        "unresolved_fields": sorted(set(unresolved)),
        "governance_metadata": governance_metadata(
            source_class="OCR_extraction",
            patch_era=normalize_patch(data),
            unresolved=sorted(set(unresolved)),
            provenance=[{"type": "ocr_input_hash", "sha256": stable_hash(data)}],
            confidence_level="low" if unresolved else "medium",
            derivation_type="OCR_normalization",
        ),
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize OCR text output — issuer/location resolution and SCU extraction")
    add_common_args(parser)
    args = parser.parse_args()
    data = load_json(args.input)
    if args.patch_version:
        data["patch_version"] = args.patch_version
    dump_json(normalize_ocr(data), args.output)


if __name__ == "__main__":
    main()
