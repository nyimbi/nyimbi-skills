---
name: obsidian
description: Work with Obsidian vaults on this machine (vault: ~/src/pjs/work_docs) — reading/creating/searching notes, tasks, and properties via the Obsidian CLI; authoring Obsidian Flavored Markdown (wikilinks, embeds, callouts, properties); creating/editing JSON Canvas files (.canvas) and Obsidian Bases (.base) views. Adopted from kepano/obsidian-skills (MIT, the author is Obsidian's CEO). Use when the user mentions Obsidian, a vault, wikilinks, callouts, canvas files, bases, or work in ~/src/pjs/work_docs. Do not use for general documentation/runbook authoring outside a vault (see documentation) or for PDF/Word/Excel artifacts (see pdf-processing, word-document-authoring, spreadsheet-authoring).
---

# obsidian

Obsidian vault operations. Adopted from [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills)
(MIT) — each reference is an upstream skill adopted verbatim (`SKILL.md`
renamed to `<name>.md` so loaders don't pick it up nested).

## State on this machine

| What | Where |
|---|---|
| App | `/Applications/Obsidian.app` (+ Obsidian Web Clipper.app) |
| Vault | `~/src/pjs/work_docs` |
| CLI | `obsidian-cli` (see `references/obsidian-cli/obsidian-cli.md` for install/commands) |

## References

| File | What it does |
|---|---|
| `references/obsidian-cli/obsidian-cli.md` | Drive the vault from the shell: read, create, search, manage notes/tasks/properties; plugin/theme development commands |
| `references/obsidian-markdown/obsidian-markdown.md` | Obsidian Flavored Markdown: wikilinks, embeds, callouts, properties, syntax that plain-Markdown tools break |
| `references/json-canvas/json-canvas.md` | `.canvas` files: nodes, edges, groups — mind maps, flowcharts, visual boards |
| `references/obsidian-bases/obsidian-bases.md` | `.base` files: database-like views over notes with filters, formulas, summaries |

## Rules of thumb

- In the vault, write Obsidian Flavored Markdown, not generic Markdown —
  wikilinks (`[[Note]]`) and callouts are the native conventions.
- Prefer the CLI for bulk/programmatic work (search, property updates,
  batch create); use direct file edits for surgical single-note changes
  (the vault is plain files on disk).
- `.canvas`/`.base` files are JSON — edit as data, validate before saving.

## Boundaries

- **documentation / writing-and-internal-communications** — docs and
  communications that don't live in the vault.
- **humanizer** — prose polish for any Markdown, vault or not.

Upstream: https://github.com/kepano/obsidian-skills (MIT).
