#!/usr/bin/env python3
"""Example: build and validate a server card programmatically.

Showcases the hub's validation API on a freshly-constructed card.

Run:
    python examples/build_card.py            # valid example
    python examples/build_card.py --broken   # show a card that fails lint
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from hub_common import validate_card, REQUIRED_FIELDS, OPTIONAL_FIELDS  # noqa: E402


CARD = {
    "name": "example-server",
    "description": "Prove that the hub proves cards.",
    "command": "npx -y @modelcontextprotocol/server-example",
    "categories": ["utility"],
    "env": ["EXAMPLE_KEY"],
    "tags": ["demo"],
}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bad", action="store_true")
    args = ap.parse_args(argv)

    card = dict(CARD)
    if args.bad:
        card.pop("command")      # force a schema violation

    print("card to validate:")
    print(json.dumps(card, indent=2))
    print(f"\nschema requires: {', '.join(REQUIRED_FIELDS)}")
    print(f"optional fields: {', '.join(OPTIONAL_FIELDS)}")

    problems = validate_card(card)
    if problems:
        print("\n[FAIL] card is invalid:")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("\n[PASS] card is valid — installable.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())