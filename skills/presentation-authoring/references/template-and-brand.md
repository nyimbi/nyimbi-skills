# Template, Brand, and File Mechanics

The file-level layer: templates, masters, placeholders, theme binding, brand assets,
export, accessibility, notes, and file size. Load this when the deck must sit on a
corporate template, survive a client's machine, or pass a brand or accessibility review.

Adapted from Oria's MIT-licensed `claude-pptx-skills` pack. See
[`sources/INDEX.md`](sources/INDEX.md).

## File types and geometry

| Type | Contains | Use |
|---|---|---|
| `.potx` | Master, layouts, theme, defaults | The brand template; new decks are created from it |
| `.thmx` | Colours, fonts, effects only | Re-theme a deck without restructuring it |
| `.pptx` | A presentation | The deliverable, not a template |

A "template" circulated as a `.pptx` for people to copy and strip is where brand drift
starts.

Set slide size once, before building. Two 16:9 presets exist and do not merge cleanly:

| Preset | Inches | Ratio |
|---|---|---|
| Widescreen | 13.333 × 7.5 | 16:9 |
| On-screen 16:9 | 10 × 5.625 | 16:9 |
| On-screen 4:3 | 10 × 7.5 | 4:3 |
| A4 paper | 10.833 × 7.5 | ~1.44:1 |

In `ppt/presentation.xml` this is
`<p:sldSz cx="12192000" cy="6858000"/>` for 13.333 × 7.5 in. Units are EMU: 914,400 per
inch, 360,000 per centimetre, 12,700 per point.

When changing ratio, prefer **Ensure Fit** for 4:3 → 16:9: nothing is lost. **Maximize**
fills the width and crops top and bottom; use it only on genuinely full-bleed decks.
Neither option reflows intelligently: re-crop images, re-check type sizes, turn off
autofit on affected placeholders, ungroup shapes before scaling, and re-anchor master
graphics.

## Theme

A PowerPoint theme has exactly twelve colour slots, stored in `ppt/theme/theme1.xml` as
`<a:clrScheme>`: `dk1`, `lt1`, `dk2`, `lt2`, `accent1`–`accent6`, `hlink`, `folHlink`.

- `dk1` / `lt1` are the primary text and background pair. Keep them near-black and
  near-white unless the brand is genuinely different.
- `accent1` is the primary brand colour; default shapes, charts and SmartArt pick it up
  first.
- Accent order is the chart series order. Fill all six in the order charts should use them.
- Set hyperlink and followed-hyperlink colours; default blue-purple links are the most
  common brand defect.
- Tints and shades generated from a slot move with it. Colours picked from the Standard
  Colors row or typed as hex do not.

Font scheme: `majorFont` (headings) and `minorFont` (body), each with Latin, East Asian and
complex-script faces. Fill the `ea` and `cs` faces or the substitution is silent.

## Master and layouts

Build 8–12 layouts, no more. Every extra layout is maintenance and a chance to pick wrong.
A working set: Title · Section Divider · Title and Content · Two Content · Comparison ·
Content with Caption · Full-bleed Image · Table · Chart · Quote · Closing.

Rules:

- Put only universal furniture on the master: background, standing logo, footer, date,
  slide number, title and body type styles.
- Placeholders are what make a layout a layout. A text box on a layout is decoration; only
  a real placeholder (`<p:ph type="…"/>`: `title`, `ctrTitle`, `subTitle`, `body`, `pic`,
  `chart`, `tbl`, `dt`, `ftr`, `sldNum`) passes formatting to slides.
- Body and content placeholders inherit by `idx`, not by position. A copied slide whose
  placeholder index does not match the layout silently loses the layout's formatting.
  Rebuild rather than nudge.
- Use **Hide Background Graphics** on full-bleed or dark-divider layouts; flip the colour
  map on a dark master rather than recolouring every text run.
- Set **Default Text Box**, **Default Shape** and **Default Line** to the brand body style,
  so newly inserted objects arrive on-brand.
- Add guides in master view at margins and columns; they save with the file.
- Delete unused stock layouts and second masters. PowerPoint normally drops unused masters
  unless **Preserve Master** pinned them (`preserve` attribute in the file).

## Layout mapping and placeholders

For each slide, name its job (open, divide, one idea, compare, one chart, full-bleed image,
close) and map it to the closest template layout. Change the layout first; move content
second.

Then migrate content into real placeholders:

- The headline goes in the Title placeholder, body in Body/Content, pictures in Picture.
- Cut the text and paste as text into the placeholder; do not drag the old box on top.
- Clear direct formatting afterward so the placeholder style shows.
- Use Tab/Shift-Tab for outline levels, not manual indents.
- Delete the empty rogue boxes; keep genuine charts and diagrams.
- **Reset** the slide to restore a deleted placeholder.

## Brand palette

State the approved palette by role: primary, secondary, light neutral, dark neutral, and
one accent reserved for emphasis. Note any chart sequence.

- Find off-palette fills, lines and text; map each to the nearest approved slot by role,
  not by hue alone.
- **One accent per slide**, on the single thing the eye must land on. If two things are
  accented, demote one.
- Charts: brand primary for the focus series, neutral grey for context, or the defined
  sequence.
- Check contrast; fix it with the palette's light or dark end, not a new colour.
- Leave real third-party logos in their own colours.

## Type

- Use only the theme's major and minor fonts.
- Bind to `+Headings` / `+Body` slots, not literal font names, where possible.
- Normalise every size to the brand scale: title, subtitle, section header, body level one,
  body level two, caption, footer. Do not invent in-between sizes; cut content instead of
  shrinking below the scale.
- Use the brand weights; remove ad-hoc bold, italic, all-caps and letter-spacing.
- Apply one case rule to titles, and one line-spacing value.
- Clear direct formatting after font replacement, then re-apply only sanctioned emphasis.

## Grid and furniture

Recover canonical values from the template's placeholders:

- Left margin = title placeholder's left edge.
- Right margin = title or content placeholder's right edge.
- Title top = title placeholder's top.
- Content top = content placeholder's top.
- Safe zone = a small inset from trim; nothing structural crosses it.
- Column count and gutter for multi-element slides.

Snap placeholders back with **Reset**, align to guides, distribute evenly, and keep the
gap between stacked elements consistent. Check across slides in slide sorter; titles and
content should not jump.

Furniture belongs on the master:

- Titles share one position, size and case.
- Footer content is identical on every content slide; set it via Header & Footer, not
  per-slide boxes.
- Page numbers appear everywhere except deliberate exceptions (title, dividers), in one
  position and one convention (`n` or `n of N`).
- Dividers share one layout, background and numbering.
- Title and closing exceptions are deliberate, not accidental.

## Assets

**Logo**: use the approved variant per background (full colour on light, reversed on dark
or photo), the current high-resolution file, native aspect ratio, at or above minimum size,
with the defined clear space. Never recolour or stretch it. Partner logos keep their own
colours and are sized for optical balance.

**Icons**: one system — line or solid, one stroke weight, one corner radius, one colour
rule, one optical size. Replace off-system icons with the closest library equivalent; do
not hand-edit clip art. Bind colour to a theme slot. Align icons to text baselines and the
grid.

**Photography**: one treatment (full colour, duotone, or a defined filter and overlay), one
or two allowed aspect ratios, one crop convention (focal point on a third, faces whole), one
placement pattern (full-bleed, half-bleed, framed), one minimum resolution. Crop, never
stretch. Use one scrim or overlay for text on photos.

**Charts**: insert natively or paste with **Use Destination Theme and Embed Workbook**;
never paste as a picture. Keep the data embedded so the chart travels. Apply the deck theme,
then strip Excel defaults: title placeholder, legend, gridlines, unneeded axes. Verify you
can select one bar and edit it; if not, it is an image.

## Fonts

PowerPoint stores a font *name*, not the font. A missing face is substituted, advance
widths differ, and the slide reflows.

1. Inventory the theme major/minor fonts plus every direct run override. The override list
   is the one that surprises people.
2. Check the foundry's embedding permission: Non-embeddable, Preview/Print, Editable,
   Installable. A Preview/Print font embeds but recipients cannot edit that text.
3. Embed OpenType (`.otf`) or TrueType (`.ttf`), not Type 1. Choose **only characters used**
   for a read-only deck or **all characters** for anything a client will edit.
4. Verify: copy the file, rename to `.zip`, and look for `ppt/fonts/*.fntdata` plus
   `<p:embeddedFontLst>` in `ppt/presentation.xml`. No folder, no embedding.
5. Set a documented fallback in the theme for the cases embedding cannot cover (web,
   Google Slides, Keynote, older builds). Metric-compatible pairs reflow least:

| Brand font | Fallback |
|---|---|
| Calibri | Carlito |
| Cambria | Caladea |
| Arial / Helvetica | Liberation Sans |
| Times New Roman | Liberation Serif |
| Courier New | Liberation Mono |

6. Outline text only for a handful of display words or a wordmark. Outlined text is
   uneditable, unsearchable and invisible to screen readers.
7. Test on a machine without the font, starting with the tightest titles and longest
   bullets.

## Export

- **PDF**: keep **Document structure tags for accessibility** on. Use PDF/A only when an
  archive or regulator requires it; re-inspect transparency, shadows and blends. Prefer
  fixing the font over rasterising text.
- **Images**: PNG for text and flat colour, JPEG for photographs. Export PDF and rasterise
  when you need a specific resolution.
- **Notes pages / handouts**: export separately from the slide PDF; one PDF cannot serve all
  three audiences.
- Open the export on a second device and check page count, fonts and order.

## Accessibility

State the standard: WCAG 2.0/2.1 AA, Section 508, or EN 301 549.

- **Unique slide title** on every slide; it is the screen-reader navigation handle. If the
  design has no visible title, use a hidden title placeholder rather than deleting it.
- **Alt text carries the finding**, not the appearance: "Revenue grew from £12m to £31m
  over four years, with the step change in FY23", not "bar chart". Mark decorative rules,
  textures and furniture as decorative.
- **Reading order**: the Reading Order Pane lists objects top-to-bottom in reading order;
  the Selection Pane lists the same objects in z-order, where the **bottom** item is read
  first. Fixing the Selection Pane top-down reverses the deck. Order: title, exhibit/body,
  source and footnotes. Re-check after layout changes.
- **Contrast**: 4.5:1 for normal text, 3:1 for large text (18 pt, or 14 pt bold) and for
  meaning-bearing non-text. Sample the actual pixels behind text over photos, gradients or
  translucent panels.
- **Never colour alone**: add a direct label, pattern or symbol; check greyscale.
- **Real tables**: use a table object with a header row; no merged cells, blank spacer rows
  or nested tables.
- **Media**: captions for video (WebVTT), transcript for audio, no autoplay, no more than
  three flashes per second, no information carried only by animation.
- **Links**: meaningful link text, not "click here" or a bare URL.
- Run **Check Accessibility** and fix Errors first; it is a floor, not a ceiling.

## Notes and handouts

Slides, notes pages and handouts have separate masters:

- `ppt/notesMasters/notesMaster1.xml`, one `ppt/notesSlides/notesSlideN.xml` per slide with
  notes, `ppt/handoutMasters/handoutMaster1.xml`.
- Set the notes body to the body font at 11–12 pt, left aligned, with real line spacing.
  Shrink the slide thumbnail if the notes matter more.
- Type notes into the Notes placeholder, not a text box dragged onto the notes page; only
  the placeholder exports and appears in Presenter View.
- Handout master controls header, footer, date, page number and orientation, not the
  thumbnail grid. Three per page is the working default because it leaves ruled note
  lines; two for a leave-behind; six or nine only as an index.
- Notes travel inside the `.pptx`. Before sending externally, Inspect Document and remove
  Presentation Notes, comments and document properties. Keep the master copy with notes.

## File size

Measure before cutting: copy the file, rename to `.zip`, inspect `ppt/media/`,
`ppt/embeddings/`, `ppt/slideMasters/`, `ppt/slideLayouts/`, `ppt/fonts/`.

1. **Delete cropped areas** (Picture Format → Compress Pictures). Cropping is a display
   instruction; the pixels remain. Destructive: work on a copy.
2. **Compress to needed resolution**: 330 ppi large-format print, 220 print, 150 screen and
   sharing, 96 email. A screen deck at 150 ppi is generous.
3. **Fix sources**: photographs as JPEG, UI/text as PNG, vector logos instead of 5000 px
   bitmaps, insert once and copy the shape so identical bytes deduplicate.
4. **Media**: compress video to 720p or link it; accept that a link breaks offline.
5. **Orphan masters/layouts**: unpin **Preserve Master**, then delete unused ones. Each
   carries its own background graphics.
6. **Editing data**: discard editing data, do not keep uncompressed images, and set the
   default image resolution in the template.
7. Remove unused custom shows, stale embedded workbooks, hidden slides and old comments.
8. Save As a new file, re-measure, and check the heaviest images at full-screen size.

## Brand audit

Audit structure, colour, type, logo, icons/images, furniture, then grade:

- **Blocker**: cannot ship — wrong logo, off-template layout, off-palette brand colour,
  unreadable text.
- **Major**: clearly off-brand but shippable — rogue font, inconsistent footer, rainbow
  chart.
- **Minor**: polish — a few points of misalignment, icon weight mismatch.

Fix Blockers first, then systemic Majors, then Minors. Point each finding at the slide
number and the fix.
