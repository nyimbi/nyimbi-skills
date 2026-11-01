# Text-Capable Image Models

Verified 2026-10-30 from three independent 2026 comparisons (FLORA, Moda's 20-model
poster test, invideo's typography comparison) plus the bundled Visual Skills model notes.
Third-party tests disagree on rankings; treat the table as a starting point, not a verdict.

## What is solved, and what is not

**Solved:** short quoted strings (1–5 words), headlines, labels, menus and infographics up
to roughly 25–30 words, exact line breaks in some models, multilingual text, and — on
Ideogram and Recraft — layout boxes and vector output.

**Not solved:** dense legal body copy, a film billing block, exact kerning and hierarchy at
print size, long copy, consistent line wrapping across models, diacritics and non-Latin
scripts on some models, and editability unless the model outputs vectors.

## Model table

| Model | Text strength | Limits |
|---|---|---|
| **GPT Image 2.5** (Flare / Sunburst) | Exact wording and longer text: menus, infographics, UI labels. Preserved line breaks and pricing columns in FLORA's five-line test. Ranked #1 in Moda's poster test. Accepts up to 16 references; 1K–4K; five quality tiers. | Slower (~35 s); not vector; verify small type at `high`/`xhigh`. |
| **Ideogram 4.5 / v4** | Best layout control: JSON bounding boxes, hex color locking; strongest typographic/design aesthetic; matched line breaks in FLORA. | ~2× cost; weak diacritics/non-Latin; degrades past ~25–30 words; one poster test left most of the frame blank. |
| **Nano Banana 2.1 / Pro** | Fastest and cheapest; letter-perfect short text; bold clean type; 100+ languages in one frame; up to 14 references. | Weak line wrapping — broke menu lines across rows. |
| **Recraft V4.1 / V3** | Native SVG/vector output, editable in Figma/Illustrator; best for logos and wordmarks at 1–5 words. | Mixed poster results; not a general scene model. |
| **Qwen Image 3.0** | Budget pick; unmatched Chinese text. | Latin layout less controlled. |
| **Seedream 5.0 Pro** | Illustrated/anime posters with text. | Narrower style range. |
| **Grok Imagine Pro** | Fast, accurate short text. | Less tested for dense layouts. |
| **Flux 2 Flex** | Hex-code color binding; good prompt adherence. | Text length and layout less proven. |

## Prompt rules that survive the model

1. **Quote the exact string.** `"THE LONG WAY DOWN"`, not *the title*.
2. **One line per line.** Put each line on its own line and say where it sits.
3. **Put text early** in the prompt, then the scene.
4. **Name the type style, size, color and position.** Ideogram and Recraft can lock hex
   colors; Nano Banana can take a font name.
5. **Say how many times.** "Render the tagline exactly once."
6. **Ban the extras.** "No extra text, no duplicate text, no watermarks, no invented
   signage."
7. **Use the quality lever.** GPT Image 2.5 `high` or `xhigh` for small or print-bound type.
8. **Proofread every glyph.** Then fix with a targeted edit ("change the second A to an R"),
   not a re-roll.
9. **Do not ask for a billing block.** The model will invent names. Typeset it.

## Poster element decisions

| Element | Route | Model / tool |
|---|---|---|
| Title as designed lettering | generate, verify, re-set for print | GPT Image 2.5 xhigh, Ideogram 4.5 |
| Title as clean brand type | typeset | vector / HTML / layout tool |
| Tagline | generate or typeset | any text-strong model; verify |
| Billing block, credits | **typeset only** | supplied block, vector |
| Rating mark | **supplied asset** | board file |
| Laurels, release date | **typeset only** | facts |
| Logo / wordmark | generate or vectorise | Recraft V4.1 / V3 |
| Menu / sign / label in the art | generate | GPT Image 2.5 or Ideogram |

## Print caveat

A generated title is a raster image. At 27×40 in, 300 dpi, it will soften and may show
artifacts around edges. If the title must be crisp, either:

- generate it as a texture/reference and re-set the final lettering in vectors, or
- use Recraft's SVG output and clean the paths, or
- keep the generated lettering only for digital and social variants.

## Sources

- FLORA — best model for readable text: https://flora.ai/guides/best-ai-image-model-for-readable-text-in-images
- Moda — 20 models tested on posters: https://moda.app/resources/models/prompts/text-poster
- invideo — typography compared by job: https://invideo.io/blog/best-ai-model-text-in-images/
- ToolColumn — text-in-image models: https://www.toolcolumn.com/learn/best-ai-image-generator-for-text-in-images
- Kenerate — eight models compared: https://kenerateai.com/blogs/best-ai-image-generator-for-text-2026

Archived copies: `film-production/references/sources/text-*.html`.
