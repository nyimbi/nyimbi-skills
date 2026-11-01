---
name: visual-design-and-branding
description: >- For design artifacts rendered inside the OpenDesign app (DESIGN.md brand-bound, live preview, HTML/PDF/PPTX/MP4 export), see open-design.
  Decide how something looks, then produce it: poster and art composition, theme
  and colour-system selection, type scale and typography, brand palette and
  identity constraints, distinctive UI design direction, generative p5.js art,
  image upscaling and export. Use when the user says "design a poster", "make
  this look better", "pick a theme for this deck", "apply our brand colours",
  "give this a distinctive visual identity", "this looks generic or templated",
  "create generative art", or "upscale this screenshot". This skill owns the
  design-decision sequence — audience, aesthetic direction, type scale, colour
  system, layout, production — and keeps five distinct techniques: preset theme
  system, brand constraints, UI craft, static composition, image enhancement. Do
  not use for the words or the document structure
  (writing-and-internal-communications); for generating PowerPoint, Word, or
  Excel files (presentation-authoring, word-document-authoring,
  spreadsheet-authoring); or for scoping, building, and browser-testing
  interactive web artifacts (web-artifact-and-app-building), which defers to
  this skill only for visual direction.
license: Apache-2.0
---

# Visual Design and Branding

This skill owns **how it looks**. It does not own what the document says
(`writing-and-internal-communications`), the office container it ships in
(`presentation-authoring`, `word-document-authoring`), or the architecture and
verification of an interactive app (`web-artifact-and-app-building`).

Everything here runs through one sequence — **audience → aesthetic direction → type
scale → colour system → layout → production** — and five source techniques plug into
it at fixed points. They do different jobs and must not be flattened into one vague
"aesthetics" paragraph:

| Technique | Supplies | Use it for |
|---|---|---|
| **theme-factory** | the *system* | preset colour+type tokens for decks, docs, reports, landing pages; custom theme generation when no preset fits |
| **brand-guidelines** | *brand constraints* | the Anthropic palette and type — a constraint that overrides preference, not a style suggestion |
| **frontend-design** | *UI craft* | distinctive, brief-specific direction for a screen: type scale, motion restraint, interface copy |
| **canvas-design** | *static composition* | posters and art pieces: philosophy → composed `.png`/`.pdf` |
| **algorithmic-art** | *generative composition* | seeded p5.js pieces with an interactive viewer |
| **image-enhancer** | *production/retouch* | upscaling, sharpening, de-artifacting an existing raster before delivery |

## When to use

- Static visual pieces: "design a poster", "make me a cover", "create a piece of art",
  print-ready PNG or PDF
- Styling an artifact: "pick a theme for this deck/report/landing page", "generate a
  theme for this brand", "apply these colours and fonts consistently"
- Brand work: applying Anthropic's brand colours and typography, checking whether an
  artifact is on-brand, restating a palette with roles
- UI direction: "give this a distinctive visual identity", "this looks like every
  other AI-generated page", "critique this design direction", type scale and layout
  decisions for a screen
- Generative work: "create generative art", "build me a p5.js sketch with parameter
  controls", seed-based variation exploration
- Image production: "upscale this screenshot", "sharpen this image", "clean up
  compression artifacts", export sizing for a destination

**Do not use for** — `writing-and-internal-communications` when the problem is the
words, the structure, or the audience framing rather than the appearance;
`presentation-authoring`, `word-document-authoring`, or `spreadsheet-authoring` when
the ask is to generate or edit the actual Office file — this skill supplies the design
specification, those supply the file; `web-artifact-and-app-building` when the ask is
to scope, architect, bundle, or browser-test an interactive artifact — that skill owns
the build and the verification, and comes here only for the visual direction.

## Workflow

1. **Fix audience, medium, and job.** Establish who sees it, where it lands (print,
   screen, slide, social, in-product), what it must make them feel or do, and the
   format constraint (one A4 page, 16:9 slide, 1080×1080, mobile-first screen). Then
   pick the branch: **static piece**, **generative piece**, **interactive UI**,
   **themed artifact**, or **image fix**. If the destination is an Office file, this
   step also decides that you are producing a *specification* for
   `presentation-authoring`/`word-document-authoring`, not the file itself.

2. **Apply brand constraints before aesthetics.** Brand is a constraint, not a
   preference — resolve it first so the rest of the sequence operates inside it.

   | Role | Value |
   |---|---|
   | Dark (text / dark bg) | `#141413` |
   | Light (bg / text on dark) | `#faf9f5` |
   | Mid gray (secondary) | `#b0aea5` |
   | Light gray (subtle bg) | `#e8e6dc` |
   | Accent — primary | `#d97757` |
   | Accent — secondary | `#6a9bcc` |
   | Accent — tertiary | `#788c5d` |
   | Headings | Poppins (fallback Arial), 24pt+ |
   | Body | Lora (fallback Georgia) |

   Headings take Poppins at 24pt and above, body takes Lora, non-text shapes cycle the
   three accents, text colour is chosen from the background's luminance, hierarchy is
   preserved. Outside an Anthropic artifact, use the client's tokens by the same
   discipline — roles filled, not a loose swatch list. If no brand exists yet, generate
   the tokens in step 3.

3. **Choose the aesthetic direction.** One of three routes, chosen deliberately:

   - **Select a preset** — show `theme-showcase.pdf`, get an explicit choice, read the
     matching file from `themes/`. Ten presets, register-matched to the audience:
     [theme-system.md](references/theme-system.md).
   - **Generate a system** — no preset fits: produce a named custom theme (4–6 hex
     values with roles, exactly two typefaces with roles, one-sentence register) to the
     same completeness as a preset.
   - **Write a position** — for a poster or art piece, name the movement in 1–2 words
     and articulate it in 4–6 paragraphs before any pixels:
     [canvas-design.md](references/canvas-design.md); for a screen, write the compact
     token plan (colour / type / layout / principles) and review it against the brief
     for defaults: [ui-craft.md](references/ui-craft.md).

   Output of this step: a **named direction** plus its tokens. Nothing gets drawn until
   the direction exists on the page.

4. **Set the type scale.** One family or two clearly distinct; roles assigned
   (display, heading, body, data); explicit steps with intentional weights, widths, and
   spacing; body lines under ~80 characters; serif body gets slightly more leading than
   sans. When type is the headline, it is an active element, not a delivery vehicle.
   Avoid the three generated-page tells: single-word accenting in headlines, all-caps
   labels, ornamental labels above content.

5. **Set the colour system.** 4–6 named hex values for the base palette, then accents
   assigned to *roles* (primary action, secondary, rules/icons) rather than decoration.
   Check every text/background pair for AA contrast and fix luminance until body text
   passes. Spend boldness in one place — one accent, one moment — and keep everything
   else disciplined.

6. **Lay out.** Decide structure before rendering.
   - *Static piece*: composition, repetition, negative space, one anchor phrase, and
     hard containment — nothing overlaps or clips, everything sits inside the margins.
   - *Screen*: ASCII wireframe and alignment decision first; the hero opens with the
     most characteristic thing in the subject's world; structural devices (rules,
     numbering, eyebrows) encode information or they come out; exactly one orchestrated
     motion moment.
   - *Themed artifact*: one theme applied uniformly to every surface; icons and charts
     take the accent palette, body and background never do.

7. **Produce, then refine — do not decorate.** Render the artifact through its branch:
   composed `.png`/`.pdf` (canvas-design), single-file interactive viewer
   (algorithmic-art), or tokens handed to `presentation-authoring` /
   `word-document-authoring` for Office files, with
   [theme-system.md](references/theme-system.md) as the specification. Run
   [image-production.md](references/image-production.md) for any raster that needs
   upscaling or cleanup, always preserving the original. The second pass tightens what
   already exists — alignment, spacing, kerning, colour cohesion — and adds nothing: if
   the instinct is a new shape or a filter, ask instead how the existing composition
   becomes more of one piece of art.

## Quality bar

- [ ] Audience, medium, format, and the artifact's job are stated before design begins
- [ ] The direction is named and written down (tokens + register), not improvised
      mid-canvas
- [ ] Type scale is explicit: families, roles, steps, weights, line length
- [ ] Palette is 4–6 named hex values plus role-assigned accents; every text pair
      passes AA contrast; brand constraints applied where they apply — brand overrides
      theme preference
- [ ] No templated default unless the brief demands it: not the cream+serif+terracotta
      cluster, the acid-accent dark theme, the broadsheet layout, the identical-card
      kit, or the all-caps-eyebrow chrome
- [ ] Nothing overlaps, clips, or falls outside the canvas; margins and breathing room
      verified at the delivery size
- [ ] One memorable element carries the boldness; the rest is quiet
- [ ] Production matches the destination: format, resolution, colour space; image
      originals preserved beside enhanced versions
- [ ] The refinement pass refined rather than added; no filter or new element was used
      as a substitute for cohesion
- [ ] The composition is original — no existing artist's work reproduced

### Failure modes

- **Palette shopping** — colours chosen because they are nice, not because they encode
  a role
- **Philosophy essay instead of artwork** — a beautiful `.md` and no artifact
- **Theme without contrast checking** — preset applied verbatim, body text fails AA
- **Decoration as structure** — dividers, numbering, and eyebrows that encode nothing
- **Default drift** — the same five AI-tell clusters appearing regardless of subject
- **Filter as refinement** — adding effects when the composition itself needs work
- **Brand override in the wrong direction** — a client accent replacing the brand
  palette, or the brand palette applied to an artifact that is not on-brand
- **Upscaling a re-renderable source** — interpolating a raster that could have been
  exported again at the right size

## Reference map

| Situation | Open |
|---|---|
| Preset theme selection, application rules, custom theme generation | [references/theme-system.md](references/theme-system.md) |
| Static poster/art piece: philosophy → embedded reference → PNG/PDF | [references/canvas-design.md](references/canvas-design.md) |
| Generative p5.js art: philosophy → seeded algorithm → interactive viewer | [references/algorithmic-art.md](references/algorithmic-art.md) |
| UI craft: direction plan, anti-default tells, type scale, motion, interface copy | [references/ui-craft.md](references/ui-craft.md) |
| Image enhancement, upscaling, export sizing | [references/image-production.md](references/image-production.md) |

Carried assets: `theme-showcase.pdf` (all ten presets rendered — show, never edit),
`themes/<name>.md` (per-theme palette and font pairing), `canvas-fonts/` (licensed
families for canvas typography, each with its `*-OFL.txt`), `templates/viewer.html`
(fixed layout for the generative viewer) and `templates/generator_template.js` (p5.js
structure reference).

## Output format

Every design request delivers a **design brief plus the artifact** — never a mood
sentence alone:

```markdown
# <Project> — Design Brief
AUDIENCE:   [who sees it, what they already know]
MEDIUM:     [print / slide / social / screen / HTML artifact] · [size]
JOB:        [what it must make them feel or do]

DIRECTION:  [named theme or movement] — [one-sentence register]

TYPE:       display: [family, weights] · body: [family] · scale: [steps]
            line length: [~n chars] · rules: [what was avoided and why]

COLOUR:     base: [4–6 named hex] · accents: [hex → role] · contrast: [AA checked]

LAYOUT:     [ASCII wireframe or composition notes: grid, anchor, negative space]

PRODUCTION: [format, resolution, colour space, files delivered]

CHECKS:     [quality-bar items verified; anything skipped and why]
```

Then the artifact itself: `movement-name.md` + `artifact.png`/`.pdf` for static pieces;
`artifact.html` for the generative viewer; the brief alone as the specification when
an Office file or a developer will render it.
