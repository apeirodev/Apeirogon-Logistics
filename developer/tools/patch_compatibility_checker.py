#!/usr/bin/env python3
import argparse
from lib.common import add_common_args, dump_json, load_json, normalize_patch
def main():
    parser = argparse.ArgumentParser(description="Check patch compatibility")
    add_common_args(parser)
    args = parser.parse_args()
    data = load_json(args.input)
    patch = normalize_patch(data)
    current = args.patch_version or patch
    dump_json({
        "patch_version": patch,
        "current_patch": current,
        "compatible": patch != "UNRESOLVED" and patch == current,
        "warning": None if patch != "UNRESOLVED" else "Patch unresolved; cannot patch-baseline output."
    }, args.output)
if __name__ == "__main__":
    main()
