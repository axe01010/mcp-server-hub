#!/usr/bin/env python3
"""Manage installed MCP servers (record what's active on this machine).

Keeps DRY with the rest of the hub: reads/writes ``.installed.json`` and
knows nothing about the catalog internals beyond ``hub_common``.

Backward compatible:
    python manage.py list
    python manage.py add <name>          # record a server (any string)
    python manage.py remove <name>
    python manage.py status              # installed vs available
    python manage.py export              # print the state as JSON
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from hub_common import load_state, mark_installed, mark_removed, state_summary


def _print_state() -> int:
    state = load_state()
    if not state:
        print("(no servers recorded in .installed.json)")
        return 0
    for name, detail in sorted(state.items()):
        cmd = detail.get("command", "")
        print(f"  {name:<22} {cmd}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="manage", description="Manage installed MCP servers.")
    ap.add_argument("cmd", nargs="?", default="list",
                    choices=["list", "add", "remove", "status", "export", "help"])
    ap.add_argument("name", nargs="?", default=None, help="server name for add/remove")
    args = ap.parse_args(argv)

    if args.cmd == "list":
        return _print_state()

    if args.cmd == "add":
        if not args.name:
            ap.error("add requires a name")
        already = args.name in load_state()
        mark_installed(args.name, {"command": " ".join(sys.argv[2:])})
        print(f"{'already present; re-recorded' if already else 'added'} {args.name!r}")
        return 0

    if args.cmd == "remove":
        if not args.name:
            ap.error("remove requires a name")
        if mark_removed(args.name):
            print(f"removed {args.name}")
            return 0
        print(f"not installed: {args.name}")
        return 1

    if args.cmd == "status":
        installed, available = state_summary()
        print(f"installed ({len(installed)}): {', '.join(installed) or '—'}")
        print(f"available ({len(available)}): {', '.join(available) or '—'}")
        return 0

    if args.cmd == "export":
        print(json.dumps(load_state(), indent=2))
        return 0

    if args.cmd == "help":
        ap.print_help()
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())