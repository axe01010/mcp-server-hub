<p align="center">
  <img src="https://github.com/axe01010/mcp-server-hub/raw/main/assets/banner.png" alt="mcp-server-hub" width="100%" />
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/axe01010/mcp-server-hub?style=for-the-badge&color=2563EB&logo=github" />
  <img src="https://img.shields.io/github/forks/axe01010/mcp-server-hub?style=for-the-badge&color=F97316&logo=github" />
  <img src="https://img.shields.io/github/license/axe01010/mcp-server-hub?style=for-the-badge&color=2563EB" />
  <img src="https://img.shields.io/github/last-commit/axe01010/mcp-server-hub?style=for-the-badge&color=F97316" />
</p>

<div align="center">

# 🧩 mcp-server-hub

**A curated, validated catalog of Model Context Protocol (MCP) servers — browse, install and manage them in seconds.**

`python browse.py` · `python install.py` · `python manage.py`

[What is MCP?](#what-is-mcp) · [Quickstart](#quickstart) · [Tools](#tools) ·
[Adding a server](docs/adding-a-server.md) · [License](#license)

</div>

---

## What is MCP?

The **Model Context Protocol** is an open standard (by Anthropic) that lets LLM
apps talk to external tools through a single JSON-RPC transport. An *MCP
server* is a small process that exposes capabilities — querying a database,
browsing the web, talking to your filesystem, remembering things — that the
agent can call. This hub is your **curated shelf** of ready-to-run server
definitions, plus the tooling to search, validate and track them.

## Quickstart

```bash
pip install -r requirements.txt

# explore the catalog — all 12 servers
python3 browse.py
python3 browse.py --category coding --json     # structured view
python3 browse.py -q "database"                 # free-text search

# confirm the catalog is healthy before using it
python3 install.py --validate                   # "catalog healthy — 12 cards OK"

# install one and get the exact command it would run
python3 install.py memory --dry-run
python3 install.py github

# track what's active on this machine
python3 manage.py status
python3 manage.py export
```

Every `install` prints the real command it *would* execute (it never runs it
for you), warns about required-but-unset environment variables, and records the
choice in `.installed.json` so `manage.py` always reflects reality.

## Catalog (12 servers)

| Server | Categories | Command |
| ------ | ---------- | ------- |
| `github` | coding, git | `npx @modelcontextprotocol/server-github` |
| `postgres` | data, database | `npx @modelcontextprotocol/server-postgres` |
| `playwright` | browsing, automation | `npx @modelcontextprotocol/server-playwright` |
| `memory` | memory, knowledge | `npx @modelcontextprotocol/server-memory` |
| `filesystem` | file, storage | `npx @modelcontextprotocol/server-filesystem` |
| `docker` | devops, containers | `docker mcp-script` |
| `brave-search` | search, web | `npx @modelcontextprotocol/server-brave-search` |
| `context7` | docs, coding | `npx @upstash/context7-mcp` |
| `fetch` | web, content | `uvx mcp-server-fetch` |
| `sqlite` | data, database | `uvx mcp-server-sqlite` |
| `time` | utility | `uvx mcp-server-time` |
| `sequential-thinking` | reasoning | `npx @modelcontextprotocol/server-sequential-thinking` |

Every card is a small JSON file in `servers/` — review the schema in
[docs/adding-a-server.md](docs/adding-a-server.md).

## How the pieces fit

```
servers/*.json  ──(load)──>  hub_common.load_cards / validate_card
      │                          └── browse.py · install.py
      │                                     │
      └───────────────────>  manage.py  ·  .installed.json
```

- `browse.py` reads the catalog (filter/search/JSON).
- `install.py` validates a card + env, prints the command, records it.
- `manage.py` maintains the local `.installed.json` state.
- `hub_common.py` is the one place the layout, schema and state live.

See **[docs/architecture.md](docs/architecture.md)** for the full picture.

## Use cases

- **Pull a server into a Claude/Cursor/Continue config fast** — find the card,
  copy the command, wire the env vars.
- **CI hygiene** — `validate.py --validate` (pretty) / `install.py --validate --json`
  fail the build if a card drifts from the schema.
- **Team share** — new servers are proposed as one JSON card + reviewed in a PR.
- **Personal memory / search a stack** — add `context7` for up-to-date docs,
  `memory` for a knowledge graph, `brave-search` for web search.

## FAQ

**Do you run the servers for me?** No — deliberately. `install.py` prints each
command for you to paste into your MCP client (or run yourself), so you keep
supply-chain control and the hub never silently executes `npx`/`uvx`.

**What configuration does each server need?** The card's `env` field lists it —
e.g. `github` needs `GITHUB_TOKEN`, `brave-search` needs `BRAVE_API_KEY`.
`install.py` warns when one is unset.

**How many servers can the catalog hold?** Principle: curated > every plugin.
A handful of high-quality cards is the point; add one per PR, validated.

## Contributing

Add a server with one JSON file per
[docs/adding-a-server.md](docs/adding-a-server.md), then pass
`python browse.py` and `python install.py --validate`. Open a PR.

## License

MIT — see [LICENSE](LICENSE).