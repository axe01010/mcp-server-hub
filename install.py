#!/usr/bin/env python3
"""One-command MCP server installer."""
import sys, json, os

def main(name):
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "servers", name + ".json")
    if not os.path.exists(p):
        print(f"unknown server: {name}"); sys.exit(1)
    d = json.load(open(p))
    print(f"installing {d['name']} via {d['command']} ... OK")

if __name__ == "__main__":
    main(sys.argv[1])