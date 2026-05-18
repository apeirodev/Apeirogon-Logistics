#!/usr/bin/env python3
import argparse
from lib.common import add_common_args, dump_json, load_json
def collect_chains(data):
    chain = []
    if isinstance(data, dict):
        gm = data.get("governance_metadata")
        if isinstance(gm, dict):
            chain.extend(gm.get("provenance_chain", []))
        for v in data.values():
            chain.extend(collect_chains(v))
    elif isinstance(data, list):
        for item in data:
            chain.extend(collect_chains(item))
    return chain
def main():
    parser = argparse.ArgumentParser(description="Reconstruct audit chain")
    add_common_args(parser)
    args = parser.parse_args()
    data = load_json(args.input)
    chain = collect_chains(data)
    dump_json({"audit_chain": chain, "chain_length": len(chain)}, args.output)
if __name__ == "__main__":
    main()
