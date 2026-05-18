#!/usr/bin/env python3
import argparse
import logging
from lib.common import dump_json, load_json

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Analyze OCR confidence")
    parser.add_argument("--input", "-i", default="-")
    parser.add_argument("--output", "-o", default="-")
    args = parser.parse_args()
    data = load_json(args.input)
    unresolved = data.get("unresolved_fields", [])
    raw_conf = data.get("ocr_confidence", 0)
    try:
        conf = float(raw_conf)
    except (TypeError, ValueError) as exc:
        logger.warning("OCR confidence value %r is not numeric: %s — treating as 0", raw_conf, exc)
        conf = 0.0
    dump_json({
        "ocr_confidence": conf,
        "unresolved_count": len(unresolved),
        "usable_for_recommendation": conf >= 0.65 and len(unresolved) <= 2,
        "requires_human_review": conf < 0.80 or bool(unresolved)
    }, args.output)
if __name__ == "__main__":
    main()
