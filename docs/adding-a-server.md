# Adding an MCP server — mcp-server-hub

Add a server to the catalog by dropping **one JSON card** into `servers/`. No
code changes needed — `browse.py`, `install.py` and `manage.py` pick it up
automatically.

## The schema

Every card is a JSON object. Two required-ish sets:

**Required** (`validate_card()` fails without them):

```jsonc
{
  "name": "my-server",            // unique key (matches the filename)
  "description": "What it does for the agent, in one sentence.",
  "command": "npx -y @modelcontextprotocol/server-my-server",  // how to launch
  "categories": ["coding", "data"] // top-level filter buckets
}
```

**Optional** (drive richer output):

```jsonc
{
  "args": ["--db-path", "/path/to.db"],   // appended after `command`
  "env": ["MY_API_KEY"],                  // required env vars (warned on install)
  "source": "https://github.com/…",        // reference
  "tags": ["sql", "db"],                   // extra search tokens
  "notes": "guides around the card"
}
```

## Steps

1. **Name the card**

   ```bash
   cp servers/context7.json servers/my-server.json
   # or
   touch servers/my-server.json
   ```

2. **Fill it in** with the schema above. Use `env` for anything the server
   needs beyond the command `run` string, and `tags` for search synonyms.

3. **Validate locally (cheap, immediate):**

   ```bash
   python3 install.py --validate
   ```

   A broken card prints its problems and exits 1 — fix until clean.

4. **Browse to confirm it shows up:**

   ```bash
   python3 browse.py -q my-server
   ```

5. **Smoke-install it (dry-run):** `python3 install.py my-server --dry-run` —
   the printed command must be exactly what you'd paste into a client.

6. **Open a PR.** The catalog only merges schema-validated cards. Reviewer
   checks: noun-precise description, correct `command`, real `env` list.

## Guidelines

- **Description = one agent-facing sentence** of what it *does*, not why it's
  good. (`"Web search via Brave"`, not `"Great search server our team loves"`.)
- **Categories come from the known set** — avoid inventing new buckets unless
  you also add them to `CATEGORIES` in `hub_common.py`.
- **Commands stay launched by your client** — never a raw `curl`/`ssh` that
  runs on the hub's behalf; the hub only prints the command.
- **Prefer `npx -y`/`uvx` official runners** over bespoke installs, and point
  `source` at the upstream that documents the exact command.

## Testing your card in isolation

```bash
cd /tmp && $HOME/.cache/uv/... 2>/dev/null   # or just:
$(python3 -c "import json;print(json.load(open('servers/my-server.json'))['command'])") \
  2>&1 | head
```
(Substitute the server you trust.) The card is philosophy-pure when the command
it prints launches a real, working MCP server.

## When to add vs when to skip

- **Add**: an official, stable, schema-able server that lots of agents would
  want.
- **Skip**: a throwaway cron, a local-only script, a private API you'd install
  by hand. Hub cards commit the catalog to curating breadth *and* quality —
  quality wins.