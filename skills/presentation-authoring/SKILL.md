---
name: presentation-authoring
description: >- For design artifacts rendered inside the OpenDesign app (DESIGN.md brand-bound, live preview, HTML/PDF/PPTX/MP4 export), see open-design.
  Use this skill whenever a PowerPoint file is involved as input, output, or both.
  Triggers include "build a deck from this outline", "turn these notes into slides",
  "fill in this template", "fix the layout", "add speaker notes", "duplicate that
  slide", "reorder the slides", "extract the text from this presentation", "make
  thumbnails of every slide", and any mention of .pptx, .potx, "deck", "slides", or
  "presentation" — even when the extracted content will be reused elsewhere, like in
  an email or summary. It owns the PowerPoint format and its tooling: pptxgenjs and
  html2pptx for authoring, raw OOXML unpack/edit/repack for existing decks,
  template-filling with slide rearrangement and text replacement, layouts, speaker
  notes, native charts, and the three-stage QA of content, file schema, and rendered
  slides. Do not use for deciding what the slides should say (see
  writing-and-internal-communications), for choosing the visual identity or palette
  (see visual-design-and-branding), or for HTML/web deliverables (see
  web-artifact-and-app-building); for agent-authored, web-native, presentable
  decks — React slides on a 1920×1080 canvas with browser present mode and
  HTML/PDF/PPTX export (see open-slide).
---

# Presentation Authoring

A `.pptx` is a ZIP archive of XML, and PowerPoint is far less forgiving than Word:
reorder two children of `<p:presentation>` and the deck becomes unopenable; use one
hex color with a `#` and the file corrupts. Two facts drive everything here. First,
PowerPoint renders the file, so the only honest check is a rendered image of the
slide. Second, pptxgenjs happily emits chart XML that python-pptx opens, LibreOffice
renders, and PowerPoint rejects — so schema validation is not optional.

## When to use

- Creating a new deck, pitch deck, or presentation from an outline or source material
- Filling an existing `.potx`/`.pptx` template with new content
- Editing, reordering, duplicating, or deleting slides in an existing deck
- Adding or editing layouts, placeholders, speaker notes, or slide comments
- Extracting text or structure from a `.pptx`, even if the text is used elsewhere
- Building native charts, tables, or SmartArt-style diagrams on slides
- Fixing a deck that PowerPoint reports as corrupt or refuses to open
- Generating visual thumbnails or slide images for review

**Do not use for** — `visual-design-and-branding` when the question is the palette,
typography system, or visual identity of the slides rather than how to encode it in
`.pptx`; `writing-and-internal-communications` when the question is what the deck
should argue; `web-artifact-and-app-building` when the deliverable is an HTML page or
app that merely resembles a slide; `open-slide` when the user wants a modern,
visually rich, browser-presented deck (or the deck is meant to be exported to
HTML/PDF) and a scaffolded open-slide project is acceptable — this skill remains
the route for direct `.pptx` authoring, existing-deck edits, and template fills.
`open-design` when the deck is meant to be produced inside the OpenDesign app (brand-bound render, live preview, template/theme picker) — that route owns the app loop; this skill owns direct `.pptx` authoring and edits.

## Workflow

1. **Choose the route.** Everything downstream depends on it.

   | Task | Approach |
   |---|---|
   | **Create** a new deck, no template | `html2pptx` (HTML slides → PPTX) or a `pptxgenjs` script |
   | **Create** from an existing template | inventory → outline → `scripts/rearrange.py` → `scripts/replace.py` |
   | **Edit** an existing deck | unpack → edit `ppt/slides/slideN.xml` → repack |
   | **Read** content | `markitdown deck.pptx`; visual grid: `scripts/skills-thumbnail.py` |

   Prerequisites: `pptxgenjs`, `markitdown[pptx]`, `Pillow`, `defusedxml`, `lxml`,
   `python-pptx`, LibreOffice (`soffice`), `pdftoppm`. `pptxgenjs` is preinstalled —
   write the script and `require('pptxgenjs')` directly; only install if that fails.

2. **Authoring a new deck.** Read
   [`references/html2pptx.md`](references/html2pptx.md) in full first. The
   `pptxgenjs` footguns that cost the most time:

   - **Set `pres.layout` before adding slides.** Default `LAYOUT_16x9` is
     **10" × 5.625"**, not 13.3" wide; coordinates past the edge are written, not
     clamped. (`LAYOUT_WIDE` = 13.3" × 7.5".)
   - **Hex colors: never `#`, never 8 digits.** `color: "FF0000"`. Both `"#FF0000"`
     and baked-in alpha (`"00000020"`) corrupt the file. Use `transparency: 0-100`
     on fills/images and `opacity: 0.0-1.0` on shadows — each is ignored on the other.
   - **Option objects are mutated in place** (values become EMU on first use). Never
     share one `shadow`/options object across two `add*` calls.
   - **Shadow `offset` must be ≥ 0** — negative corrupts the file; cast upward with
     `angle: 270`.
   - **`letterSpacing` is ignored**; the real option is `charSpacing`.
   - **Lists:** `bullet: true` per item, never a literal `•`; `breakLine: true` on
     every array item except the last; space with `paraSpaceAfter`, not `lineSpacing`.
   - **One `new pptxgen()` per output file.**
   - **`rectRadius` only works on `ROUNDED_RECTANGLE`.**
   - **No gradient fills** — use a gradient image as the background.
   - **Text boxes have built-in padding** — `margin: 0` whenever text must align with
     a shape or icon at the same x.
   - **Speaker notes go in `slide.addNotes("...")`**, once per slide, never in a text
     box on the slide.
   - **Keep charts native** via `addChart()`; only chart types PowerPoint has no form
     for (Sankey, network, chord) go in as images. Default charts render bare — set
     `showTitle`, `showValue`, `chartColors`, and quiet the axis frame.
   - **Stacked bar/column labels must be `ctr`, `inEnd`, or `inBase`.** `outEnd`
     corrupts the file.
   - **A combo series using `secondaryValAxis`/`secondaryCatAxis` needs both `valAxes`
     and `catAxes`, two entries each.** Without them pptxgenjs declares axis ids it
     never defines and PowerPoint discards the chart.
   - **After `writeFile()`, run `scripts/office/validate.py`.** Fix in the generator,
     never by hand-editing packed XML.
   - **Never reorder the children of `<p:presentation>`.**
   - **Icons:** render `react-icons` to SVG, rasterize with `sharp` at ≥256px, insert
     as `data:image/png;base64,` — the prefix is required.

3. **Filling a template — inventory, then rearrange, then replace.** Read
   [`references/ooxml.md`](references/ooxml.md) first.

   ```bash
   python -m markitdown template.pptx > template-content.md
   python scripts/skills-thumbnail.py template.pptx template-thumbs   # always pass a per-deck prefix
   python scripts/rearrange.py template.pptx working.pptx 0,34,34,50,52   # 0-based; repeats duplicate
   python scripts/inventory.py working.pptx text-inventory.json
   # write replacement-text.json, then:
   python scripts/replace.py working.pptx replacement-text.json output.pptx
   ```

   - `thumbnail.py`'s prefix defaults to `thumbnails` and silently overwrites another
     deck's grids in the same directory. It only accepts `.pptx` — copy a `.potx` to a
     `.pptx` name first. Two implementations ship: `scripts/skills-thumbnail.py`
     (renders through LibreOffice) and `scripts/awesome-thumbnail.py` (python-pptx
     based, adds `--outline-placeholders`); either is fine, prefer the first for
     fidelity.
   - Write a `template-inventory.md` listing **every** slide index and its layout
     before choosing which to reuse. Match layout arity to content: two items never
     go into a three-column layout; count your content pieces first.
   - `replace.py` **clears every text shape not named in your JSON**. Carry over the
     paragraph properties from the inventory — `bold`, `alignment`, `bullet` +
     `level`, `font_size`, `color`/`theme_color` — not just the text. Never put a
     bullet glyph in the text when `"bullet": true`.

4. **Editing an existing deck.** Do all structural work first, then content:

   ```bash
   python scripts/unpack.py deck.pptx unpacked/        # pretty-prints XML, suggests an RSID
   python scripts/add_slide.py unpacked/ slide2.xml --after slide2.xml
   # reorder / delete = edit <p:sldIdLst> in ppt/presentation.xml
   python scripts/clean.py unpacked/                    # after sldIdLst is final
   # edit ppt/slides/slideN.xml
   python scripts/pack.py unpacked/ out.pptx
   python scripts/office/validate.py out.pptx --original deck.pptx
   ```

   - **Structural work before content edits.** `add_slide.py` copies a slide file
     verbatim, so duplicating after editing clones the edited content; `clean.py`
     deletes any slide missing from `<p:sldIdLst>`, including one you just wrote.
   - **Never copy a slide file by hand** — `add_slide.py` does every registration the
     package needs. Pass `-o` or it rewrites the input deck in place. A duplicated
     slide still *references* its source's chart/SmartArt parts rather than cloning
     them.
   - `python-pptx` cannot duplicate a slide, collapses formatting through
     `text_frame.text = "..."` (assign `run.text` instead), and cannot read the
     SVG/EMF most template art uses.
   - Legacy `.ppt` converts first via
     `python scripts/office/soffice.py --headless --convert-to pptx file.ppt`.
     `.potx` unpacks and packs identically — keep the extension.
   - Parse XML with `defusedxml.minidom`. Round-tripping through
     `xml.etree.ElementTree` rewrites namespace prefixes and corrupts the deck.
   - One `<a:p>` per list item; copy the sibling `<a:pPr>`; bold titles and inline
     labels via `b="1"` on `<a:rPr>`; let bullets inherit from the layout (never a
     literal `•`); text with leading/trailing spaces needs `xml:space="preserve"`.
   - Template slots ≠ source items: if the layout shows four team members and you have
     three, delete the fourth group entirely — image and text boxes, not just the text.

5. **QA — three passes, in this order.**

   **Content:**
   ```bash
   markitdown output.pptx
   markitdown output.pptx | grep -iE "\bx{3,}\b|lorem|ipsum|\bTODO|\[insert|this.*(page|slide).*layout"
   ```
   Any grep hit is leftover placeholder text — fix before declaring success.

   **File schema:**
   ```bash
   python scripts/office/validate.py output.pptx                       # from scratch
   python scripts/office/validate.py output.pptx --original src.pptx   # from a template
   ```
   Always pass `--original` for a template-derived deck: the template may itself
   contain parts the XSD rejects, and a real regression hides among those. Structural
   checks (relationships, content types, charts) ignore `--original` and report
   template-inherited problems either way.

   **Visual:**
   ```bash
   python scripts/office/soffice.py --headless --convert-to pdf output.pptx
   rm -f slide-*.jpg
   pdftoppm -jpeg -r 150 output.pdf slide
   ls -1 "$PWD"/slide-*.jpg
   ```
   Pass the printed absolute paths to the image view. `pdftoppm` zero-pads by page
   count (`slide-1.jpg` under 10 pages, `slide-01.jpg` for 10–99). After any fix,
   rerun all four commands — the PDF must be regenerated from the edited `.pptx`.
   Look at every slide fresh (a subagent works well) for, in priority order: text
   overflow or clipping, overlaps, citations/footers colliding with content, gaps
   under 0.3", margins under 0.5", misaligned columns, low-contrast text or icons,
   template decoration left positioned for the old text, leftover placeholders.

6. **Fonts are a QA hazard, not just a style choice.** The font name you write is
   rendered by the user's PowerPoint; your QA renders through LibreOffice, which
   substitutes. Safe fonts render true-to-width in QA *and* ship with Office: Arial,
   Calibri, Cambria, Times New Roman, Courier New, Bookman Old Style, Century
   Schoolbook. QA-unreliable (substitute has different widths, so overflow checks can
   be wrong): Georgia, Trebuchet MS, Impact, Arial Black, Garamond, Consolas,
   Palatino Linotype. Never default to Aptos — no metric-compatible substitute here
   and missing from older Office installs. For a user-requested font outside the safe
   list, use it where asked but leave ~10% slack and do not trust QA text-fit on it.

## Quality bar

- [ ] `markitdown` output contains every intended line, in order, and no placeholder
      text survived (`grep` above returns nothing)
- [ ] `scripts/office/validate.py` passes; `--original` used for anything built from
      a template
- [ ] Every rendered slide was inspected — no clipped text, no overlaps, no element
      within 0.5" of the slide edge, no orphaned template decoration
- [ ] Structural edits happened before content edits; no slide was hand-copied; the
      deck was repacked from inside the unpacked directory after `rm` of the old file
- [ ] Charts are native PPTX charts (not images), stacked-bar labels use
      `ctr`/`inEnd`/`inBase`, and secondary-axis combos declare both `valAxes` and
      `catAxes`
- [ ] Speaker notes live in `slide.addNotes()`, one per slide, not in slide text
- [ ] All colors are 6-digit hex without `#`; no shared/mutated option objects
- [ ] Fonts used for body text are on the QA-safe list, or their containers have
      documented slack
- [ ] Layout arity matches content arity — no empty placeholders, no content forced
      into a column it does not fit

## Reference map

| Situation | Open |
|---|---|
| Authoring slides — HTML slide syntax, html2pptx API, pptxgenjs charts/tables/shapes, icons and gradients | [html2pptx.md](references/html2pptx.md) |
| Editing OOXML — slide structure, text/list/shape/image/table patterns, slide operations, packing checklist | [ooxml.md](references/ooxml.md) |

Executable helpers: `scripts/rearrange.py`, `scripts/inventory.py`,
`scripts/replace.py`, `scripts/add_slide.py`, `scripts/clean.py`,
`scripts/unpack.py`, `scripts/pack.py`, `scripts/office/validate.py`,
`scripts/office/soffice.py`, `scripts/skills-thumbnail.py`,
`scripts/awesome-thumbnail.py`.

## Output format

Deliver the `.pptx` plus:

```markdown
# <Deck> — presentation delivery note

## File
Path, slide count, layout (16:9 / 4:3), template used (or "from scratch").

## Route
html2pptx / pptxgenjs / template-fill / OOXML edit — and why.

## Slide inventory
# | Layout or layout code | Purpose | Notes (speaker notes present?)

## Verification
Content check (markitdown), `validate.py` result including `--original`,
rendered slide count, list of visual defects found and fixed.

## Residual issues
Anything not fixed: font substitution risk, template parts that fail schema on
their own, placeholders left for the user to supply.
```

For a template fill, also attach the outline → template-slide-index mapping so the
user can see which source layout produced each output slide.
