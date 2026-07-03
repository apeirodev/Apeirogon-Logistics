#!/usr/bin/env python3
"""
Normalize OCR/AI vision output into the standard mission extraction format.

Accepts two input modes:
  1. Raw OCR text  -- {"raw_text": "Covalex 24 SCU ..."}
  2. AI vision JSON -- {"source_class": "ai_vision_extraction", "missions": [...]}

In mode 2, each mission is normalized individually: issuer and location aliases
are resolved, UNRESOLVED values are preserved, and governance metadata is attached.
"""
import argparse
import json
import logging
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.common import (
    add_common_args, check_injection_risk, collect_unresolved, dump_json,
    governance_metadata, load_json, normalize_patch, normalize_text,
    parse_positive_number, stable_hash, structured_error,
)

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
            logger.warning("Could not load OCR_normalization_rules.json: %s -- using built-in defaults", exc)
    return {}


_RULES = _load_rules()
_ISSUER_ALIASES: dict = _RULES.get("issuer_aliases") or _FALLBACK_ISSUER_ALIASES
_LOCATION_ALIASES: dict = _RULES.get("location_aliases") or {}
_CONFIDENCE_THRESHOLD: float = (
    _RULES.get("ocr_ambiguity_handling", {}).get("minimum_confidence_threshold")
    or _FALLBACK_CONFIDENCE_THRESHOLD
)


def _resolve_issuer(text: str) -> str | None:
    lower = text.lower()
    for alias, canonical in _ISSUER_ALIASES.items():
        if alias in lower:
            return canonical
    return None


def _resolve_location(text: str) -> str:
    if not text or text == "UNRESOLVED":
        return text
    for alias, canonical in _LOCATION_ALIASES.items():
        if alias.lower() in text.lower():
            return canonical
    return text


# AI-02: provider string fields are sanitized (control characters stripped,
# length bounded) before any downstream use.
_MAX_PROVIDER_FIELD_LENGTH = 512
_MAX_RAW_TEXT_LENGTH = 4096
_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def _sanitize_provider_value(value):
    if isinstance(value, str):
        return _CONTROL_CHARS.sub("", value[:_MAX_PROVIDER_FIELD_LENGTH])
    if isinstance(value, list):
        return [_sanitize_provider_value(v) for v in value]
    return value


def _normalize_mission(mission: dict) -> dict:
    """Resolve aliases and collect unresolved fields for a single mission dict."""
    mission = {k: _sanitize_provider_value(v) for k, v in mission.items()}
    issuer_raw = mission.get("issuer", "UNRESOLVED")
    issuer = (
        _resolve_issuer(issuer_raw)
        if issuer_raw not in ("UNRESOLVED", None, "")
        else None
    ) or "UNRESOLVED"

    pickup_raw = mission.get("pickup", "UNRESOLVED")
    pickup = _resolve_location(pickup_raw) if pickup_raw not in ("UNRESOLVED", None, "") else "UNRESOLVED"

    delivery_raw = mission.get("delivery", "UNRESOLVED")
    if isinstance(delivery_raw, list):
        delivery = [_resolve_location(d) if d not in ("UNRESOLVED", None, "") else "UNRESOLVED"
                    for d in delivery_raw]
    elif delivery_raw not in ("UNRESOLVED", None, ""):
        delivery = [_resolve_location(delivery_raw)]
    else:
        delivery = ["UNRESOLVED"]

    unresolved = list(mission.get("unresolved_fields", []))
    if issuer == "UNRESOLVED":
        unresolved.append("issuer")
    if pickup == "UNRESOLVED":
        unresolved.append("pickup")
    if all(d == "UNRESOLVED" for d in delivery):
        unresolved.append("delivery")
    if mission.get("cargo_scu") in ("UNRESOLVED", None, ""):
        unresolved.append("cargo_scu")
    if mission.get("reward_usc") in ("UNRESOLVED", None, ""):
        unresolved.append("reward_usc")

    return {
        "issuer": issuer,
        "pickup": pickup,
        "delivery": delivery,
        "cargo_type": mission.get("cargo_type", "UNRESOLVED"),
        "cargo_scu": mission.get("cargo_scu", "UNRESOLVED"),
        "reward_usc": mission.get("reward_usc", "UNRESOLVED"),
        "fee_usc": mission.get("fee_usc", "UNRESOLVED"),
        "timer_minutes": mission.get("timer_minutes", "UNRESOLVED"),
        "contract_type": mission.get("contract_type", "UNRESOLVED"),
        "unresolved_fields": sorted(set(unresolved)),
        "notes": mission.get("notes", ""),
    }


_INJECTION_CHECKED_FIELDS = ("pickup", "delivery", "cargo_type", "notes", "issuer")


def _normalize_vision(data: dict) -> dict:
    """Mode 2: normalize AI vision JSON that already contains structured missions."""
    raw_missions = data.get("missions") or []
    normalized_missions = [_normalize_mission(m) for m in raw_missions]

    all_unresolved = list(data.get("unresolved_fields") or [])
    for m in normalized_missions:
        all_unresolved.extend(m.get("unresolved_fields", []))

    confidence = data.get("extraction_confidence")
    try:
        confidence = float(confidence) if confidence not in (None, "UNRESOLVED", "") else None
    except (TypeError, ValueError):
        confidence = None

    # AI-02: check mission string fields for injection attempts (LLM01)
    injection_risk_detected = False
    for mission in raw_missions:
        for field in _INJECTION_CHECKED_FIELDS:
            value = mission.get(field)
            if isinstance(value, str) and check_injection_risk(value):
                injection_risk_detected = True
                logger.warning("Injection risk detected in AI vision field '%s'", field)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, str) and check_injection_risk(item):
                        injection_risk_detected = True
                        logger.warning("Injection risk detected in AI vision field '%s'", field)

    warnings = []
    if confidence is not None and confidence < _CONFIDENCE_THRESHOLD:
        warnings.append("Low extraction confidence -- human review recommended before scoring.")
    if not normalized_missions:
        warnings.append("No missions extracted from input.")
    if injection_risk_detected:
        warnings.append("Injection risk detected in one or more mission fields; treat AI output strictly as data.")

    return {
        "mode": "ai_vision",
        "missions": normalized_missions,
        "mission_count": len(normalized_missions),
        "extraction_confidence": confidence if confidence is not None else "UNRESOLVED",
        "ship": data.get("ship", "UNRESOLVED"),
        "patch_version": normalize_patch(data),
        "warnings": warnings,
        "unresolved_fields": sorted(set(all_unresolved)),
        "governance_metadata": governance_metadata(
            source_class="ai_vision_extraction",
            patch_era=normalize_patch(data),
            unresolved=sorted(set(all_unresolved)),
            provenance=[{"type": "vision_input_hash", "sha256": stable_hash(data)}],
            confidence_level="low" if all_unresolved else "medium",
            derivation_type="ai_vision_normalization",
        ),
        "injection_risk_detected": injection_risk_detected,
    }


def normalize_ocr(data: dict) -> dict:
    """Mode 1: normalize raw OCR text via regex extraction."""
    raw = data.get("raw_text") or data.get("text") or ""
    # AI-02: bound and strip control characters from OCR text before parsing
    raw = _CONTROL_CHARS.sub("", str(raw)[:_MAX_RAW_TEXT_LENGTH])
    text = normalize_text(raw)
    lower = text.lower()

    issuer = _resolve_issuer(lower) or None

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

    return {
        "mode": "raw_ocr",
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


def normalize(data: dict) -> dict:
    """Dispatch to vision or raw-OCR path based on source_class."""
    if data.get("source_class") == "ai_vision_extraction" or "missions" in data:
        return _normalize_vision(data)
    return normalize_ocr(data)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Normalize OCR text or AI vision extraction output into standard mission format"
    )
    add_common_args(parser)
    args = parser.parse_args()
    data = load_json(args.input)
    # WARN-01: validate input structure before processing
    if not isinstance(data, dict):
        dump_json(structured_error("input must be a JSON object"), args.output)
        sys.exit(1)
    if args.patch_version:
        data["patch_version"] = args.patch_version
    dump_json(normalize(data), args.output)


if __name__ == "__main__":
    main()
