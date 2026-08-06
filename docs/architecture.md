# Architecture — mcp-server-hub

How the hub is organised and why the pieces are split as they are.

## One schema, one shared module

Everything the CLI family does passes through `hub_common.py`. It owns:

- **Paths** — `SERVERS_DIR` (`servers/`), `INSTALLED_FILE` (`.installed.json`).
- **Loading** — `load_cards()` globs `servers/*.json` into a `name → card` dict,
  skipping malformed files with a warning.
- **Schema** — `REQUIRED_FIELDS` (`name`, `description`, `command`,
  `categories`) + `OPTIONAL_FIELDS` (`args`, `env`, `source`, `tags`, `notes`);
  `validate_card()` returns a list of problems (empty = valid).
- **Installed-state** — `load_state()`, `mark_installed()`, `mark_removed()`,
  `state_summary()` wrap the recorded-set on disk.

Keeping this in one module is what makes the three CLIs thin and consistent —
they never re-derive paths or reinvent validation.

```
             ┌───────────────────── hub_common.py ─────────────────────┐
             │  paths · load_cards · validate_card · state helpers     │
             └──────┬────────────┬─────────────┬────────────────────────┘
                    │ imports    │ imports     │ imports
                    ▼            ▼             ▼
               browse.py     install.py     manage.py
           (search/filter)  (validate+rec) (state CRUD)
```

## The two data stores

1. **`servers/*.json`** — the catalog: *everything available*, curated. Source
   of truth for the schema and the description.
2. **`.installed.json`** — the state: *what's active on this machine*,
   ephemeral, gitignored. `install.py` writes it; `manage.py` reads/writes it.

A server is `available` when it's a card but not in state, and `installed` once
recorded. That split is the whole point: the catalog is versioned and shared;
the installed-set is personal and local.

## Command flow

| You run | What happens |
| ------- | ------------ |
| `browse.py` | `load_cards()` → filter/search → render table or `--json`. |
| `browse.py --list-tags` | union of every `categories` + `tags` token. |
| `install.py <name>` | `find_card()` → `validate_card()` → warn on missing `env` → print command → `mark_installed()`. |
| `install.py --validate` | `validate_all()` over every card (whole-catalog lint). |
| `manage.py status` | `state_summary()` → available vs installed. |
| `manage.py export` | dump `.installed.json` (for CI / sharing). |

## Design principles

1. **Never execute third-party commands.** The hub prints the command; you run
   it. No hidden `npx`/`uvx` execution, no supply-chain surprise.
2. **Curated, not sprawling.** The catalog is a small set of high-value,
   schema-checked servers (12 today). Adding one requires a validated card.
3. **Validation everywhere.** `install.py --validate` / `install.py --json`
   provide a machine-readable exit code for CI gating.
4. **Backward compatible.** Legacy `browse.py <category>` and
   `manage.py add <name>` forms still work; `hub_common.py` sits underneath
   them without changing their CLI shape.

## Extending

New server → one JSON card in `servers/` (see `docs/adding-a-server.md`). New
CLI verbs → add branches in the relevant tool; keep I/O to `hub_common`.
New shared logic → lives in `hub_common.py`, not duplicated in a tool.