# Architecture Selection — Single-File vs Multi-Component

Decision file for step 2 of the [SKILL.md](../SKILL.md) workflow. Choose before
scaffolding; switching later means rewriting the delivery path.

| Axis | Single-file HTML | React + Tailwind + shadcn/ui project |
|---|---|---|
| Best for | one screen, static content, light interactivity, a demo, a form with local state | state, routing, multiple views, component reuse, data fetching, complex forms |
| State | a few variables, URL, or `localStorage` | reducers, context, hooks, controlled inputs at scale |
| Structure | inline `<style>` and `<script>` | `src/` components, path alias `@/`, typed props |
| Dependencies | none, or one CDN script | 40+ shadcn/ui components, Radix primitives, Tailwind theming |
| Delivery | hand over the file | build → inline → hand over `bundle.html` |
| Iteration cost | edit and refresh | edit, HMR, then re-bundle |
| Failure mode | unmanageable past ~500 lines | scaffolding a full toolchain for a landing page |

## Choose single-file when all of these hold

- One page, no routing, no shared state between views
- No component library needed — the UI is a handful of elements
- The user wants to paste or open the result immediately
- Total code will stay comfortably under a few hundred lines

Write it directly: one `<!DOCTYPE html>` with inline CSS and JS, no build step, no
`node_modules`. It must open from `file://` with no server.

## Choose the React project when any of these hold

- More than one view, or URL-addressable state
- Real state: filters, wizards, editors, optimistic updates, polling
- Forms with validation, or anything that benefits from typed component composition
- The user asks for shadcn/ui components, Tailwind theming, or a component library

Then use `scripts/web-artifacts-builder/init-artifact.sh` — see
[react-setup-and-bundling.md](react-setup-and-bundling.md).

## Middle path

If a single-file page is growing but the interaction is still simple, extract state
first (a single `useState`-equivalent pattern or URL params) before reaching for a
framework. Do not migrate to React to avoid organising a 300-line file.

## Design note

Both branches are *building* decisions. Visual direction — palette, type scale,
whether the page looks generic — belongs to `visual-design-and-branding`; the only
design rule enforced here is the anti-slop floor in the SKILL.md quality bar.
