# OpenDesign design-system packages

Source: `docs/design-systems.md` + `design-systems/README.md` in
[nexu-io/open-design](https://github.com/nexu-io/open-design) (Apache-2.0),
main 2026-09-27.

## Package contract

A design system is a **package**, not a standalone markdown file. Minimum
machine-readable shape (all three files present in the bundled catalog):

```text
design-systems/<slug>/
├── manifest.json   ← discovery metadata and declared package files
├── DESIGN.md       ← canonical design prose for agents
└── tokens.css      ← canonical compiled CSS custom properties
```

`DESIGN.md`-only folders still work (legacy / user-installed discovery
fallback), but new packages should ship all three.

## manifest.json (v1)

Fixed canonical file names; v1 schema:

```json
{
  "schemaVersion": "od-design-system-project/v1",
  "id": "acme",
  "name": "Acme",
  "category": "Productivity & SaaS",
  "description": "A concise English catalog summary.",
  "source": { "...": "provenance / origin of the package" }
}
```

## How the loop uses it

1. The user picks a package in the app (picker) or points the agent at a
   folder — "drop a folder in, the picker finds it".
2. Every render reads the active package's `DESIGN.md` as the **brand
   contract**: the agent applies the tokens, typography, color, and layout
   rules when generating the artifact.
3. `tokens.css` is the compiled form agents (and the preview iframe) can
   consume directly; MCP exposes it by name so the agent sees the live file,
   not a stale export.

## Catalog

151 design-system packages ship with the repo (`design-systems/`), e.g.
productivity & SaaS brands, editorial palettes, fintech Swiss grids. Browse
them in the app's Design System page; to add a brand, run the
`brand-extract` / `design-md` functional skill: give it a screenshot, URL,
or git repo + existing `DESIGN.md`, and it codifies a reusable package.

## Boundary

This is how OpenDesign *consumes* brands. Authoring, auditing, or documenting
a design system as a standalone spec (naming conventions, token hygiene,
component variant docs, a11y notes) belongs to the bundle's `design-system`
skill — the two skills can hand off: `design-system` produces the spec,
`open-design` renders against it.
