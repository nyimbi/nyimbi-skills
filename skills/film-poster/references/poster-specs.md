# Poster Specs and Delivery

Confirm the printer's and platform's current requirements before delivery; they change.

## Print one-sheet

| Property | Value |
|---|---|
| Trim | 27 × 40 in (686 × 1016 mm) |
| Bleed | 0.125 in (3 mm) each side |
| Resolution | 300 dpi |
| Pixel size at trim | 8100 × 12000 px |
| Color | CMYK for offset; sRGB only if the printer asks |
| Format | PDF/X-4 or TIFF, fonts embedded/outlined |
| Safe margin | type ≥ 0.375 in inside trim |
| Black | rich black for large areas; 100K for small text |

Some territories use 27×41 in or 24×36 in; confirm with the printer.

## Digital

| Deliverable | Pixels | Color | Format |
|---|---|---|---|
| Digital one-sheet | 2000×3000 | sRGB | PNG or high-quality JPEG |
| Teaser | 2000×3000 | sRGB | PNG |
| Streaming thumbnail | 1920×1080 | sRGB | JPEG, < 2 MB |
| Vertical social | 1080×1920 | sRGB | PNG/JPEG |
| Square social | 1080×1080 | sRGB | PNG/JPEG |
| Banner | 1920×1080 or 2560×1440 | sRGB | JPEG |
| Character poster | 2000×3000 | sRGB | PNG |

Keep a lossless master (PNG or TIFF) for every variant. Re-export platform files from the
master; do not re-compress a JPEG repeatedly.

## Naming

```text
poster_onesheet_27x40_300dpi.tif
poster_onesheet_2000x3000.png
poster_teaser_2000x3000.png
thumbnail_1920x1080.jpg
poster_9x16_1080x1920.png
poster_1x1_1080x1080.png
character_mara_2000x3000.png
poster.pdf
poster-manifest.md
```

## QC checklist

- [ ] Title, tagline, credits, rating and release are spelled correctly.
- [ ] Billing block matches the supplied contract; no invented names.
- [ ] Rating mark is the correct territory asset.
- [ ] Laurels are real selections only.
- [ ] Likeness and consent cleared for every real person.
- [ ] AI disclosure recorded where required.
- [ ] No spoiler in the image or tagline.
- [ ] Title readable at 200 px.
- [ ] Art matches the film's palette, grain and lens.
- [ ] Negative space is deliberate, not accidental.
- [ ] Every aspect is re-composited, not stretched.
- [ ] Print file has bleed, safe margins, CMYK and embedded fonts.
- [ ] Digital files are sRGB and within platform size limits.
- [ ] Manifest lists every file, size, credit source and approval.

## Manifest template

```markdown
# Poster Manifest — <title>

| File | Pixels | Color | Purpose | SHA-256 |
|---|---|---|---|---|
| poster_onesheet_27x40_300dpi.tif | 8100×12000 | CMYK | print | ... |
| poster_onesheet_2000x3000.png | 2000×3000 | sRGB | digital | ... |
| thumbnail_1920x1080.jpg | 1920×1080 | sRGB | streaming tile | ... |

**Credits source:** <contract / supplied block / studio>
**Likeness:** <cleared / not applicable>
**AI disclosure:** <text>
**Approved by:** <name, date>
```

## Legal notes

- **Billing block.** Union and contract rules govern order, size and wording. Use the
  supplied block verbatim. If none is supplied, use a placeholder and flag it as unapproved.
  Typeset it; do not ask an image model to render a dense credit block. Generated display
  type must be proofread glyph by glyph and vectorised for print where crispness matters.
- **Likeness.** A generated face that resembles a real person still needs consent. Do not
  use a real person's name or likeness without it.
- **Rating.** Use the board's official mark and descriptor; do not redraw it.
- **Laurels.** Only festivals actually won or selected. Do not invent.
- **AI disclosure.** Follow the platform, distributor and jurisdiction rules; record the
  disclosure text in the manifest.
- **Music and art.** A poster that reproduces a copyrighted artwork, still or logo needs a
  licence.
