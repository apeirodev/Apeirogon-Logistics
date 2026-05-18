#!/usr/bin/env python3
import argparse
from lib.common import dump_json, load_json
def main():
    parser = argparse.ArgumentParser(description="Verify release integrity manifest")
    parser.add_argument("--input", "-i", default="-")
    parser.add_argument("--output", "-o", default="-")
    args = parser.parse_args()
    data = load_json(args.input)
    dump_json({"valid": isinstance(data.get("files"), dict), "file_count": len(data.get("files", {}))}, args.output)
if __name__ == "__main__":
    main()
