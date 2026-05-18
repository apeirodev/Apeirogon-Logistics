#!/usr/bin/env python3
import argparse
from lib.common import dump_json, load_json
def main():
    parser = argparse.ArgumentParser(description="Analyze OCR confidence")
    parser.add_argument("--input", "-i", default="-")
    parser.add_argument("--output", "-o", default="-")
    args = parser.parse_args()
    data = load_json(args.input)
    unresolved = data.get("unresolved_fields", [])
    try:
        conf = float(data.get("ocr_confidence", 0))
    except Exception:
        conf = 0
    dump_json({
        "ocr_confidence": conf,
        "unresolved_count": len(unresolved),
        "usable_for_recommendation": conf >= 0.65 and len(unresolved) <= 2,
        "requires_human_review": conf < 0.80 or bool(unresolved)
    }, args.output)
if __name__ == "__main__":
    main()
