#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from lib.common import add_common_args, dump_json, governance_metadata

_ALLOWED_IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif", ".webp"}


def _validate_image_path(raw: str) -> Path:
    p = Path(raw).resolve()
    if p.suffix.lower() not in _ALLOWED_IMAGE_SUFFIXES:
        raise ValueError(
            f"Image path has unexpected extension '{p.suffix}'. "
            f"Allowed: {sorted(_ALLOWED_IMAGE_SUFFIXES)}"
        )
    # Path traversal guard: require the resolved path to be absolute and non-root
    if p == p.root or str(p) in ("/", ""):
        raise ValueError(f"Image path resolves to filesystem root: {raw}")
    return p


def main():
    parser = argparse.ArgumentParser(description="Generate local OCR preprocessing guidance")
    add_common_args(parser)
    parser.add_argument("--image", required=True, help="Path to screenshot image file")
    parser.add_argument("--profile", default="star_citizen_contract_terminal")
    args = parser.parse_args()

    try:
        image = _validate_image_path(args.image)
    except ValueError as exc:
        dump_json({"error": str(exc)}, args.output)
        sys.exit(1)

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
        "governance_metadata": governance_metadata(
            source_class="deterministic_output",
            derivation_type="ocr_preprocessing_guidance",
        ),
    }
    dump_json(report, args.output)


if __name__ == "__main__":
    main()
