---
name: open-slide
description: >- For design artifacts rendered inside the OpenDesign app (DESIGN.md brand-bound, live preview, HTML/PDF/PPTX/MP4 export), see open-design.
  Author presentation decks with the open-slide agent-native slide framework —
  the agent writes the slides as React components on a fixed 1920×1080 canvas,
  with themes, typed design tokens, stepped reveals, page transitions, morph
  transitions, built-in speaker notes and presenter mode, a click-to-comment
  in-browser inspector, and export to self-contained static HTML, print-ready
  PDF, and editable PPTX. Use when the user wants a modern, visually rich,
  presentable deck (pitch deck, product or executive presentation, keynote), a
  deck presented in a browser, "make a deck about X" where visual craft is the
  point, speaker notes or presenter mode, or "export this deck to PPTX/HTML"
  from a web source. Requires a scaffolded open-slide project (Node + network:
  npx @open-slide/cli init) — one project per deck. Do not use for direct .pptx
  authoring or editing an existing PowerPoint file, when PowerPoint is the only
  required format and no Node runtime is available (see
  presentation-authoring), for single-file HTML artifacts that are not decks
  (see web-artifact-and-app-building), or for architecture and process diagrams
  (see archify).
license: MIT
---

# Open Slide (agent-native slide framework)

Decks are authored as React: each slide is `slides/<id>/index.tsx` — a
non-empty array of zero-prop page components, each rendered into a fixed
**1920×1080** canvas that the framework scales. The agent writes the code; the
framework owns the runtime (navigation, hot reload, inspector, present mode,
export).

> **Runtime requirement.** Unlike the other skills in this bundle, this one
> needs a live project: Node 20+, network for the first `npx` fetch, and a
> dev server the user opens in a browser. Scaffold once per deck (or per set of
> related decks — a project holds many slides under `slides/`).

## When to use

- A deck where visual craft is the point — pitch decks, product launches,
  executive presentations, keynotes, conference talks
- A deck that will be **presented in a browser** (fullscreen play mode,
  presenter view with next-slide preview, speaker notes, timer)
- The user names open-slide, or asks for "speaker notes / presenter mode" on a
  deck, or "export the deck to PPTX / PDF / static site"
- Handoff from `business-plan-authoring`'s deck map when a modern presentable
  deck is wanted instead of a direct .pptx

## Prerequisites

```bash
npx @open-slide/cli init <deck-id>   # scaffold the project
cd <deck-id>
npm run dev                           # match the lockfile: npm / pnpm / bun
```

- Dev server at `http://localhost:5173/s/<id>`; home page lists all slides.
- `open-slide sync:skills` refreshes the framework's in-project skills.
- Only `react`, `@open-slide/core`, and standard web APIs are available inside
  slides — never `npm install` new dependencies.
- Do not touch `package.json`, `open-slide.config.ts`, or other slides.

## Workflow

### 1. Draft the deck — `references/create-slide/create-slide.md`

Theme picker (if `themes/` has themes), then **four mandatory scoping
questions** (aesthetic direction with 3 topic-tailored options, page count,
text density, motion), structure plan (one idea per page; cover / agenda /
divider / content / big-number / quote / comparison / closing), then write
`slides/<id>/index.tsx`.

### 2. Build pages — `references/slide-authoring/slide-authoring.md`

The technical reference for every page: file contract (`export default
Page[]`, `meta`, `design` const with `var(--osd-X)` tokens), canvas rules
(absolute px only), type scale, the **vertical budget math** (content must fit
1080px — compute `font × line-height × lines + gaps + 2×padding` per page
before writing; split the page rather than overflow), assets, webfonts,
speaker notes contract, and the self-review checklist. Its
`references/slide-authoring/references/<primitive>.md` files cover each
framework primitive (`design-system`, `assets`, `webfonts`, `page-numbers`,
`steps`, `transitions`, `morph`) — read the relevant one before using the
primitive.

### 3. Iterate with the user

- **Click-to-comment:** user clicks an element in the dev viewer, leaves a
  comment; it lands in source as an `@slide-comment` marker →
  `references/apply-comments/apply-comments.md` applies every pending edit and
  clears the markers.
- **"This page" / "this element":** deictic references →
  `references/current-slide/current-slide.md` re-reads
  `node_modules/.open-slide/current.json` fresh every turn (it is a live
  cursor; a prior read is stale) to resolve slide id, page, and selection.

### 4. Themes (optional) — `references/create-theme/create-theme.md`

Author a reusable visual identity as a `themes/<id>.md` + `themes/<id>.demo.tsx`
pair (palette, typography, paste-ready Title/Footer, motion) that `create-slide`
lists as a picker option and the dev UI previews.

### 5. Export

- **Static HTML / PDF / PPTX** — from the dev server's export UI. PPTX export
  runs entirely in the browser, turning each page into native PowerPoint text
  boxes, shapes, and images (editable).
- **Deployable static site** — `open-slide build` (outputs a plain static
  build for Vercel, Cloudflare Pages, Netlify, or any static host).

## Quality bar

- Vertical budget verified for **every page** before writing — no `overflow:
  auto/hidden` escape hatches; splitting a page is always the fix.
- One idea per page; bullets that wrap to a second line get shortened or their
  own page; body text never under 28px.
- One coherent visual direction across the whole deck (palette, type scale,
  layout padding, aesthetic commitment).
- New slides declare the `design` const so the user can live-tweak tokens from
  the Design panel.
- Visually repeated elements are explicit `<Component />` instances, never
  `array.map` (the inspector edits one source node at a time).
- Speaker notes live in `export const notes` (index-aligned with the page
  array) — never in a markdown file.
- The `slide-authoring.md` self-review checklist is run before handing off.

## Reference map

| Reference | Use when |
|---|---|
| [create-slide/create-slide.md](references/create-slide/create-slide.md) | Drafting a new deck end to end |
| [slide-authoring/slide-authoring.md](references/slide-authoring/slide-authoring.md) | Writing or editing any page (always consult before touching a slide) |
| [slide-authoring/references/](references/slide-authoring/references/) | Using a framework primitive: `design-system` · `assets` · `webfonts` · `page-numbers` · `steps` · `transitions` · `morph` |
| [apply-comments/apply-comments.md](references/apply-comments/apply-comments.md) | Processing `@slide-comment` markers from the inspector |
| [current-slide/current-slide.md](references/current-slide/current-slide.md) | Resolving "this page" / "this element" deictic references |
| [create-theme/create-theme.md](references/create-theme/create-theme.md) | Authoring a reusable theme bundle under `themes/` |

## Output format

On handoff, report:

1. Slide id and file path (`slides/<id>/index.tsx`)
2. Dev-server URL (`http://localhost:5173/s/<id>`) and that hot reload is live
3. Speaker-notes location (the `notes` export, visible in the presenter view) — if written
4. Export options (HTML / PDF / PPTX from the dev UI; `open-slide build` for deploy)

Do not start the dev server yourself unless asked.
