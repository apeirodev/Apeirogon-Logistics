#!/usr/bin/env python3
import argparse
import logging
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from lib.common import add_common_args, dump_json, load_json, governance_metadata, collect_unresolved

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Analyze OCR confidence")
    add_common_args(parser)
    args = parser.parse_args()
    data = load_json(args.input)
    unresolved = data.get("unresolved_fields", [])
    raw_conf = data.get("ocr_confidence", 0)
    try:
        conf = float(raw_conf)
    except (TypeError, ValueError) as exc:
        logger.warning("OCR confidence value %r is not numeric: %s -- treating as 0", raw_conf, exc)
        conf = 0.0
    result = {
        "ocr_confidence": conf,
        "unresolved_count": len(unresolved),
        "usable_for_recommendation": conf >= 0.65 and len(unresolved) <= 2,
        "requires_human_review": conf < 0.80 or bool(unresolved),
        "governance_metadata": governance_metadata(
            source_class="deterministic_output",
            unresolved=unresolved,
            derivation_type="ocr_confidence_analysis",
        ),
    }
    dump_json(result, args.output)

if __name__ == "__main__":
    main()
