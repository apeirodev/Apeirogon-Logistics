#!/usr/bin/env python3
import argparse, zipfile
from pathlib import Path
def main():
    parser = argparse.ArgumentParser(description="Build sorted deterministic zip")
    parser.add_argument("--root", default=".")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    root = Path(args.root)
    with zipfile.ZipFile(args.output, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(root.rglob("*")):
            if p.is_file() and ".git" not in p.parts:
                z.write(p, p.relative_to(root))
if __name__ == "__main__":
    main()
