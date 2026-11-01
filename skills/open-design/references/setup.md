# OpenDesign setup & this-machine wiring

Upstream: https://github.com/nexu-io/open-design (Apache-2.0).
Version verified on this machine: **0.24.1**.

## Install options (upstream, in order of preference)

1. **Desktop app** (recommended, zero config) — macOS (Apple Silicon + Intel)
   or Windows x64 from https://open-design.ai or GitHub Releases. No Node,
   no pnpm, no clone. Linux: no prebuilt artifact (issue #4368); run from
   source.
2. **Into the coding agent (no UI)** —
   `od mcp install <agent>` where `<agent>` = `claude | codex | reasonix |
   raven | cursor | copilot | openclaw | antigravity | pi | vibe | hermes |
   cline | kimi | kiro | trae | opencode`. Hosted equivalent:
   `curl -fsSL https://open-design.ai/install.sh | sh -s <agent>`.
3. **Docker** — `git clone …`, `cd deploy`, `cp .env.example .env`,
   `OD_API_TOKEN=$(openssl rand -hex 32) >> .env`, `docker compose up -d` →
   http://127.0.0.1:7456 (user `open-design`, password = the token).
4. **From source** — `corepack enable && pnpm install && pnpm tools-dev run
   web` (Node ~24, pnpm 10.33.x).

## The `od` PATH trap — and its fix on this machine

On macOS (and WSL2), `/usr/bin/od` is **Apple's octal-dump utility** and
normally shadows OpenDesign's `od` command. On this machine it is
**circumvented**: a wrapper script at `~/.local/bin/od` (which is earlier on
`$PATH` than `/usr/bin`) execs the app's bundled CLI directly:

```sh
#!/bin/sh
exec /opt/homebrew/bin/node "/Applications/Open Design.app/Contents/Resources/app/prebundled/daemon/daemon-cli.mjs" "$@"
```

So here `command -v od` → `~/.local/bin/od` = the real OpenDesign CLI
(verified: `od` prints the OD usage). If this wrapper ever disappears
(cleaned home dir, app update moving daemon-cli.mjs), re-create it — and
verify the target path against the app's **Settings → MCP server** snippet.

## This machine's wiring (verified 2026-09-28)

- App: `/Applications/Open Design.app` (v0.24.1).
- CLI wrapper: `~/.local/bin/od` → `node …/daemon-cli.mjs` (bypasses `/usr/bin/od`).
- opencode MCP entry in `~/.config/opencode/opencode.json`:

  ```json
  "open-design": {
    "type": "local",
    "command": [
      "/opt/homebrew/bin/node",
      "/Applications/Open Design.app/Contents/Resources/app/prebundled/daemon/daemon-cli.mjs",
      "mcp",
      "--daemon-url",
      "http://127.0.0.1:7456"
    ],
    "enabled": true
  }
  ```

- Project data: `~/.open-design/`.
- The daemon serves the app on `http://127.0.0.1:7456` when the app runs;
  MCP calls that fail with connection errors mean the daemon isn't up —
  open the app.

## MCP surface (agent side)

Through the MCP server or the `od` wrapper (both work; the CLI is the same
binary the MCP entry runs):

```
od project list --json          # projects
od files list <project-id> --json
od files read <project-id> <relative-path>
od plugin list --json
od skills list --json
```

MCP exposes the **live files** (tokens CSS, JSX components, entry HTML) as a
structured API queryable by name — no zip export/re-attach between
iterations.

## BYOK

Model-agnostic: any coding-agent CLI on PATH is the engine, or any
OpenAI-compatible endpoint via the BYOK proxy (SSRF-guarded at the daemon
edge). No OpenDesign subscription required for local use.
