#!/usr/bin/env python3
"""Example: recommend an MCP stack for a goal, then dry-run the installs.

Demonstrates using browse + install as libraries.

Run:
    python examples/recommend.py "memory, documentation"
    python examples/recommend.py web
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from browse import matches, render_text     # noqa: E402
from hub_common import load_cards, load_state  # noqa: E402


GOAL_MAP = {
    "memory": ["memory"],
    "documentation": ["context7"],
    "docs": ["context7"],
    "web": ["brave-search", "fetch"],
    "search": ["brave-search"],
    "data": ["postgres", "sqlite"],
    "database": ["postgres", "sqlite"],
    "browser": ["playwright"],
    "automation": ["playwright"],
    "reasoning": ["sequential-thinking"],
    "code": ["github", "context7"],
    "coding": ["github", "context7"],
}


def main(argv: list[str] | None = None) -> int:
    goal = (argv or ["docs"])[0].lower()
    wanted = GOAL_MAP.get(goal)
    if not wanted:
        print(f"unknown goal {goal!r}; try: " + ", ".join(sorted(GOAL_MAP)))
        return 1

    state = load_state()
    installed = set(state)
    cards = [c for c in load_cards().values() if c["name"] in wanted]
    cards.sort(key=lambda c: c["name"])

    print(f"{'rated for goal: '}{goal} → {', '.join(wanted)}\n")
    if not cards:
        print("  (nothing matches)")
        return 0
    print(render_text(cards, installed))
    print("\nDry-run installs:")
    for c in cards:
        cmd = " ".join([c["command"]] + list(c.get("args") or []))
        status = "already installed" if c["name"] in installed else "recommended"
        print(f"  python install.py {c['name']}  # {status}: {cmd}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))