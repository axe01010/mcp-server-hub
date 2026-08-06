#!/usr/bin/env python3
"""Browse the curated MCP server directory.

List every server card from ``servers/*.json``, optionally filtered by
category, free-text query, or tag. JSON output is available for scripting.

Backward compatible: ``browse.py <category>`` still works, e.g.::

    python3 browse.py data
    python3 browse.py --category coding --json
    python3 browse.py --query "database"
    python3 browse.py --tags db
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from hub_common import load_cards, state_summary, CATEGORIES


def matches(card: dict[str, Any], category: str | None = None,
            query: str | None = None, tag: str | None = None) -> bool:
    """True if a card matches the given filters (case-insensitive substring)."""
    if category and category not in (card.get("categories") or []):
        return False
    if tag and tag not in (card.get("tags") or []):
        return False
    if query:
        hay = " ".join(str(v) for v in [
            card.get("name", ""), card.get("description", ""),
            " ".join(card.get("categories") or [])])
        if query.lower() not in hay.lower():
            return False
    return True


def render_text(cards: list[dict[str, Any]], installed: set[str]) -> str:
    lines = [f"{'NAME':<22} {'CATEGORIES':<26} STATUS  DESCRIPTION"]
    for c in cards:
        cats = ",".join(c.get("categories") or [])[:24]
        status = "installed" if c["name"] in installed else "available"
        short = (c.get("description") or "")[:60]
        lines.append(f"{c['name']:<22} {cats:<26} {status:<8} {short}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="browse", description="Browse the MCP server catalog.")
    ap.add_argument("category", nargs="?", default=None,
                    help="filter by category (legacy positional)")
    ap.add_argument("--category", dest="cat_opt", default=None, help="filter by category")
    ap.add_argument("-q", "--query", default=None, help="free-text search in name/desc")
    ap.add_argument("--tag", "--tags", dest="tag", default=None,
                    help="filter by a tag (run with --list-tags to see them)")
    ap.add_argument("--list-tags", action="store_true",
                    help="print all category/tag tokens and exit")
    ap.add_argument("--json", action="store_true", help="emit raw JSON")
    args = ap.parse_args(argv)

    if args.list_tags:
        tokens = sorted({t for c in load_cards().values()
                         for t in ((c.get("categories") or []) + (c.get("tags") or []))})
        print("\n".join(tokens))
        return 0

    category = args.cat_opt or args.category
    cards = [c for c in load_cards().values()
             if matches(c, category, args.query, args.tag)]
    cards.sort(key=lambda c: c["name"])
    installed, _ = state_summary()

    if args.json:
        print(json.dumps(cards, indent=2))
    else:
        print(render_text(cards, set(installed)))
        print(f"\n{len(cards)} of {len(load_cards())} servers shown. "
              f"Use --category <cat> | -q <query> | --json | --list-tags")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())