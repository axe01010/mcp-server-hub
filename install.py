#!/usr/bin/env python3
"""One-command MCP server installer with real validation.

Resolves a server key against the catalog, validates its schema, checks for
required environment variables, prints the exact install command and records
it in ``.installed.json``. Never executes the command itself — it emits the
command so a safe run (paste / CI plan / MCP client config) is fully under your
control.

Backward compatible:
    python install.py github          # install + record
    python install.py github --dry-run
    python install.py --validate --json        # validate all cards
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

from hub_common import (load_cards, find_card, validate_card, mark_installed,
                        mark_removed, state_summary, SERVERS_DIR)


def _full_command(card: dict[str, Any]) -> str:
    return " ".join([card["command"]] + list(card.get("args") or []))


def _missing_env(card: dict[str, Any]) -> list[str]:
    return [e for e in (card.get("env") or []) if not os.environ.get(e)]


def validate_all() -> list[dict[str, Any]]:
    """Return problems for every card (empty = catalog is healthy)."""
    problems = []
    for name, card in load_cards().items():
        for err in validate_card(card):
            problems.append({"name": name, "problem": err})
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="install", description="Install an MCP server from the catalog.")
    ap.add_argument("name", nargs="?", default=None, help="server key to install")
    ap.add_argument("--dry-run", action="store_true", help="print what would happen, don't record")
    ap.add_argument("--force", action="store_true", help="record even if already installed")
    ap.add_argument("--validate", action="store_true", help="validate all catalog cards, then exit")
    ap.add_argument("--json", action="store_true", help="emit JSON output")
    args = ap.parse_args(argv)

    if args.validate:
        problems = validate_all()
        if args.json:
            print(json.dumps(problems))
            return 0 if not problems else 1
        if problems:
            for p in problems:
                print(f"[invalid] {p['name']}: {p['problem']}")
            return 1
        print(f"catalog healthy — {len(load_cards())} cards OK.")
        return 0

    if not args.name:
        ap.error("provide a server name (see `python browse.py`) or use --validate")
    name = args.name

    card = find_card(name)
    if card is None:
        print(f"[error] unknown server '{name}'. Run `python browse.py` to list servers.")
        return 1

    errors = validate_card(card)
    if errors:
        for e in errors:
            print(f"[error] {name}: {e}")
        return 1

    missing = _missing_env(card)
    installed = name in state_summary()[0]

    cmd = _full_command(card)
    if args.json:
        print(json.dumps({"name": name, "command": cmd, "errors": errors,
                          "missing_env": missing, "installed": installed}, indent=2))
        return 0 if not errors else 1

    print(f"installing {name} via {cmd}")
    for env in missing:
        print(f"  [warn] env var not set: {env} (set it in your shell / MCP client)")
    if errors:
        print("  [error] card failed validation — aborted.")
        return 1

    if args.dry_run:
        print("  [dry-run] command NOT recorded.")
        return 0

    if installed and not args.force:
        print(f"  [info] {name} already recorded. Use --force to re-record.")
        return 0

    mark_installed(name, {"command": cmd, "categories": card.get("categories", [])})
    print(f"  [ok] recorded in .installed.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())