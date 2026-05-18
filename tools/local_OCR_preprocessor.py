#!/usr/bin/env python3
import argparse
from pathlib import Path
from lib.common import dump_json


def main():
    parser = argparse.ArgumentParser(description="Generate local OCR preprocessing guidance")
    parser.add_argument("--image", required=True)
    parser.add_argument("--profile", default="star_citizen_contract_terminal")
    parser.add_argument("--output", "-o", default="-")
    args = parser.parse_args()
    image = Path(args.image)
    report = {
        "image": str(image),
        "exists": image.exists(),
        "profile": args.profile,
        "hard_dependency_on_ocr_engine": False,
        "recommended_steps": [
            "crop contract list region",
            "convert to grayscale",
            "increase contrast",
            "sharpen text edges",
            "run optional local OCR engine such as Tesseract",
            "preserve unreadable values as unresolved",
        ],
    }
    dump_json(report, args.output)


if __name__ == "__main__":
    main()
