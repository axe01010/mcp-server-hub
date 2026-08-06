#!/usr/bin/env python3
"""Manage installed MCP servers."""
import sys, os, json

INSTALLED = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".installed.json")

def load():
    if not os.path.exists(INSTALLED): return []
    return json.load(open(INSTALLED))

def main(cmd):
    if cmd == "list":
        for s in load():
            print(s)
    elif cmd == "add":
        load().append(" ".join(sys.argv[2:]))
        print("added")
    else:
        print(f"usage: manage.py list|add <name>")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "list")