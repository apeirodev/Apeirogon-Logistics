#!/usr/bin/env python3
import argparse
from lib.common import dump_json, load_json, stable_hash
def main():
    parser = argparse.ArgumentParser(description="Export OCR debug metadata")
    parser.add_argument("--input", "-i", default="-")
    parser.add_argument("--output", "-o", default="-")
    args = parser.parse_args()
    data = load_json(args.input)
    dump_json({"debug_hash": stable_hash(data), "input_keys": sorted(data.keys()), "record": data}, args.output)
if __name__ == "__main__":
    main()
