---
name: open-design
description: OpenDesign (nexu-io/open-design, Apache-2.0) — the local-first design engine that turns the coding agent into the renderer. Use when the user wants a design artifact produced through OpenDesign: prototypes (web/desktop/mobile), live dashboards, decks (15 templates / 36 themes), images, documents, or HyperFrames motion-graphics MP4 — bound to a DESIGN.md brand system, with sandboxed live preview and HTML/PDF/PPTX/MP4 export. Triggers: "open-design", "OpenDesign", "OD", "DESIGN.md", "design system package", "make a landing page in OpenDesign", "deck with the [brand] design system". Installed on this machine (v0.26.1, 2026-11-01) with the MCP server already wired into opencode. Read the installed app's own version when precision matters: `plutil -extract CFBundleShortVersionString raw "/Applications/Open Design.app/Contents/Info.plist"`. Do not use for direct .pptx authoring or editing existing decks (see presentation-authoring), React-canvas decks without the OD app (see open-slide), design-system documentation or audits (see design-system), or plain HTML artifacts with no preview/export/brand loop (see web-artifact-and-app-building).
---

# open-design (OpenDesign platform)

OpenDesign is an open-source "Claude Design" alternative: a local-first
desktop app whose **daemon** drives the coding agent already on the user's
machine. The agent writes real files (HTML/CSS, JSX, PPTX, MP4); the app
renders them in a sandboxed iframe, binds every render to the active
package's `DESIGN.md` brand contract, and exports to HTML / PDF / PPTX /
ZIP / Markdown / MP4.

Four planes, all portable directories: **plugins** (runnable workflows,
277 shipped) · **functional skills** (agent behavior, 163 shipped — catalog
in `references/skill-catalog.md`) · **design templates** (rendering
blueprints: 15 deck templates, 36 themes, HyperFrames) · **design systems**
(brand packages, 151 shipped).

## State on this machine

| What | Where |
|---|---|
| App (v0.24.1) | `/Applications/Open Design.app` |
| MCP server (opencode) | `~/.config/opencode/opencode.json` → `open-design` entry: `node …/daemon-cli.mjs mcp --daemon-url http://127.0.0.1:7456` (enabled) |
| Project data | `~/.open-design/` |
| `od` on `$PATH` | **Circumvented:** `~/.local/bin/od` wrapper (earlier on PATH than `/usr/bin`) execs the app's bundled `daemon-cli.mjs` — `command -v od` → `~/.local/bin/od` = the real OD CLI |

The daemon must be running for MCP to work (the desktop app starts it;
default port 7456). If MCP calls fail, ask the user to open the app (or
check that nothing else owns the port).

## When to use / when not to

**Use OpenDesign when:** the artifact should be *rendered, previewed, and
exported through the brand loop* — a landing page that must match a
`DESIGN.md`, a pitch deck in a specific template/theme, a dashboard with a
tweaks panel, a motion-graphics MP4, or an image through one of the media
providers. Also when the user explicitly names OpenDesign, a design system
package, or a `DESIGN.md`.

**Do not use OpenDesign when:**
- The deliverable is a `.pptx` produced or edited directly (no preview loop
  needed) → `presentation-authoring`.
- A modern React-canvas deck the user wants without the OD app →
  `open-slide`.
- Documenting, auditing, or extending a design system as a spec artifact →
  `design-system` (OD *consumes* `DESIGN.md`; it is not a spec-authoring
  tool).
- A brand direction, poster, or identity exploration before any rendering →
  `visual-design-and-branding`.
- A one-off HTML page/app with no brand system or export requirement →
  `web-artifact-and-app-building`.
- Sales assets generated from deal context → `create-an-asset`.

## Workflow

1. **Pick the entry point.** Check `references/skill-catalog.md` for a
   matching functional skill (or ask the user). Decks: `pptx`, `slides`,
   `ppt-keynote`, `deck-swiss-international`, `deck-guizang-editorial`,
   `deck-open-slide-canvas`, `frontend-slides`, `theme-factory`. Prototypes:
   `web-artifacts-builder`, `frontend-dev`, `frontend-slides`. Dashboards:
   `data-report`, `d3-visualization`, `frame-data-chart-nyt`. Brand:
   `design-md`, `brand-extract`, `brand-guidelines`, `brandkit`.
2. **Bind a design system.** The active package is a directory with
   `manifest.json` + `DESIGN.md` + `tokens.css` (see
   `references/design-systems.md`). If the user has a brand but no package,
   run the `brand-extract` / `design-md` flow: screenshot/URL in → `DESIGN.md`
   out.
3. **Generate.** The agent writes canonical project files; the app previews
   them live and the user iterates in conversation. Query project state via
   MCP: project list, files list/read, plugin list, skills list.
4. **Export.** HTML (single file, inlined), PDF (deck-aware print), PPTX
   (agent-driven — `pptx-html-fidelity-audit` verifies PPTX against the HTML
   source), ZIP, Markdown, MP4 (HyperFrames).
5. **Hand off.** The artifact is real HTML/CSS — drop it into any agent to
   continue as code; or deliver the exported file.

## Boundaries inside OD's own catalog

OD's 163 skills overlap its *own* templates and with each other (e.g. four
`pptx*` variants). Pick one per task: `pptx` (python-pptx, read/edit/generate)
vs `pptx-generator`/`slides` (PptxGenJS from scratch) vs `ppt-keynote`
(Keynote-style HTML, one card per screen). When two seem to fit, prefer the
one whose `category`/`od.mode` frontmatter matches the artifact type, and
tell the user which one you chose.

## Reference map

| File | Contents |
|---|---|
| `references/skill-catalog.md` | All 163 functional skills: name, category, one-line description (extracted from upstream frontmatter, main 2026-09-27) |
| `references/design-systems.md` | Design-system package contract (`manifest.json` / `DESIGN.md` / `tokens.css`), discovery, and adding a brand |
| `references/setup.md` | Install options (desktop app / `od mcp install` / Docker / from source), the `od` PATH-shadowing trap, and this machine's wiring |

Upstream: https://github.com/nexu-io/open-design (Apache-2.0, ~98k stars).
The app, its plugins, and its templates are used as-is; this skill is the
bundle's routing entry point into that platform.
