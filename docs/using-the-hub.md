# Using the hub — mcp-server-hub

A practical walkthrough of the daily commands.

## Setup

```bash
git clone https://github.com/axe01010/mcp-server-hub.git
cd mcp-server-hub
pip install -r requirements.txt        # requests
# optional:
pip install -e .                       # gives you mcp-browse / mcp-install / mcp-manage
```

## 1. Browse

Find what you need before installing anything.

```bash
# the whole catalog (12 today)
python3 browse.py

# filter by category
python3 browse.py --category coding
python3 browse.py --category data

# free-text search (name + description + categories)
python3 browse.py -q "web search"
python3 browse.py -q database

# tags (union of categories + tags)
python3 browse.py --list-tags
python3 browse.py --tag docs

# machine-readable for CI/scripts
python3 browse.py --json
python3 browse.py -q github --json | python3 -m json.tool
```

Legacy form still works: `python3 browse.py coding`

## 2. Validate

Before trusting a catalog (or after `git pull`), run the lint:

```bash
python3 install.py --validate
# catalog healthy — 12 cards OK.
# (exit 0)
```

A failing validation returns exit 1 and prints each broken card:

```bash
$ python3 install.py --validate --json
[{"name": "broken", "problem": "missing required field 'command'"}]
$ echo $?  # 1
```

Use it as a pre-commit / CI gate: `python3 install.py --validate` blocks
merges that would ship a malformed card.

## 3. Install

Install never auto-runs the server — it validates, prints the exact command,
and records the choice.

```bash
# dry run to see exactly what would be recorded, without side effects
python3 install.py memory --dry-run

# real install: validates + records
python3 install.py github

# it also tells you when an env var is needed
#   [warn] env var not set: GITHUB_TOKEN

# record even if already installed
python3 install.py github --force
```

The recorded command is a *plan*. Paste it into your MCP client (Claude
Desktop, Cursor, Continue) as the `command` for that server. Example:
`npx -y @modelcontextprotocol/server-github`.

## 4. Manage

Keep the local record of what's active:

```bash
python3 manage.py list
python3 manage.py status            # installed (2): github, memory ...
python3 manage.py export            # JSON of the installed-set
python3 manage.py remove github     # stop tracking one
python3 manage.py add context7      # track a bare name (free-form)
```

## Working example: a doc+search stack

Goal: give an agent up-to-date library docs, web search and a persistent
memory.

```bash
python3 install.py context7        # up-to-date docs (docs.python.org, MDN, Rust, …)
python3 install.py brave-search    # web search (set BRAVE_API_KEY)
python3 install.py memory          # knowledge-graph memory file

python3 manage.py status
# installed (3): brave-search, context7, memory

python3 manage.py export > stack.json
```

Now wire the three printed commands into your MCP client and restart it —
the agent gains `context7_*`, `web_search` and `memory_` tools.

## Next: adding your own server

See `docs/adding-a-server.md`.