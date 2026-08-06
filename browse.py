#!/usr/bin/env python3
"""Browse the curated MCP server directory."""
import json, sys, glob, os

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "servers")

def main(cat=None):
    for f in sorted(glob.glob(os.path.join(DIR, "*.json"))):
        d = json.load(open(f))
        if cat and cat not in (d.get("categories") or []):
            continue
        print(f"{d['name']:24} {d.get('description','')}")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)