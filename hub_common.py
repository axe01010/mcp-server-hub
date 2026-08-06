"""Shared plumbing for the mcp-server-hub CLI family.

Holds the server-directory layout constants, catalog loading, schema
validation and the installed-state store so ``browse.py``, ``install.py`` and
``manage.py`` stay thin, consistent and DRY.
"""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
SERVERS_DIR = ROOT / "servers"
INSTALLED_FILE = ROOT / ".installed.json"

#: Keys every server card must have (plus optional: args, env, source, tags, notes).
REQUIRED_FIELDS = ("name", "description", "command", "categories")
#: Optional fields allowed in a card.
OPTIONAL_FIELDS = ("args", "env", "source", "tags", "notes", "installed")

#: Recognised category keys surfaced by `--categories`.
CATEGORIES = ("coding", "web", "search", "data", "database", "file", "storage",
              "memory", "knowledge", "devops", "containers", "automation",
              "browsing", "docs", "content", "reasoning", "utility")


def load_cards() -> dict[str, dict[str, Any]]:
    """Load every ``servers/*.json`` card keyed by name (sorted, de-duped)."""
    cards: dict[str, dict[str, Any]] = {}
    for path in sorted(SERVERS_DIR.glob("*.json")):
        try:
            card = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            print(f"[hub] warning: skipping {path.name}: {exc}")
            continue
        name = card.get("name") or path.stem
        card.setdefault("name", name)
        card.setdefault("installed", False)
        cards[name] = card
    return cards


def validate_card(card: dict[str, Any]) -> list[str]:
    """Return a list of schema problems (empty = valid)."""
    errors: list[str] = []
    for field in REQUIRED_FIELDS:
        if field not in card or card.get(field) in (None, ""):
            errors.append(f"missing required field '{field}'")
    if "categories" in card:
        bad = [c for c in card["categories"] if not isinstance(c, str)]
        if bad:
            errors.append("categories must be a list of strings")
    if "command" in card and not isinstance(card["command"], str):
        errors.append("command' must be a string")
    if "args" in card and not isinstance(card["args"], list):
        errors.append("args' must be a list")
    return errors


def find_card(name: str) -> dict[str, Any] | None:
    cards = load_cards()
    return cards.get(name)


# ---------------------------------------------------------------------------
# Installed-state registry (.installed.json)
# ---------------------------------------------------------------------------
def load_state() -> dict[str, dict[str, Any]]:
    """Read the installed-services state file (.installed.json)."""
    if not INSTALLED_FILE.exists():
        return {}
    try:
        data = json.loads(INSTALLED_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def mark_installed(name: str, detail: dict[str, Any] | None = None) -> None:
    state = load_state()
    state[name] = {"name": name, **(detail or {})}
    _write_state(state)


def mark_removed(name: str) -> bool:
    state = load_state()
    if name in state:
        del state[name]
        _write_state(state)
        return True
    return False


def _write_state(state: dict[str, dict[str, Any]]) -> None:
    INSTALLED_FILE.parent.mkdir(parents=True, exist_ok=True)
    INSTALLED_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def state_summary() -> tuple[list[str], list[str]]:
    """Return ``(available, installed)`` names from cards + state."""
    cards = load_cards()
    state = load_state()
    installed = [n for n in state]
    available = [n for n in cards if n not in installed]
    return installed, available