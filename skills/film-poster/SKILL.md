---
name: film-poster
description: >-
  Design and deliver a film's key art and poster package: concept routes, art prompts with
  type-safe negative space, title treatment, tagline, billing block and credits, rating and
  laurels, and platform variants (theatrical one-sheet, teaser, character posters, streaming
  thumbnail, vertical and square social). Use when the user says "make a movie poster", "key
  art", "one-sheet", "poster for the film", "thumbnail", "character poster", "title
  treatment", or when a film reaches design lock or delivery and needs marketing art. Do not
  use for general image prompting (see ai-image-art-direction), for the film's visual style
  lock (see film-design), or for editing the film (see film-postproduction).
---

# Film Poster and Key Art

A poster is a one-image argument for the film. It has to work at 200 pixels in a feed and at
27×40 inches on a wall, and it has to be legally accurate.

Text is no longer the blanket no it was. Top models — GPT Image 2.5, Ideogram 4.5, Nano
Banana Pro, Recraft V4.1 — set short display text with high fidelity, and Ideogram and
Recraft add layout boxes and vector output. What none of them can be trusted with is a
**dense legal billing block**: dozens of names, exact order, exact spelling, contractual
billing, and print-grade kerning. The working rule is therefore:

- **Display text** (title, tagline, one-line label): may be generated, ideally at the
  highest quality tier, then verified glyph by glyph. Re-set it as vectors for print unless
  the generated lettering *is* the artwork.
- **Contractual text** (billing block, credits, rating, laurels, release): composite from
  supplied assets. A model that invents a producer's name has broken the poster.

See `references/text-models.md` for the model-by-model capability table.

> **Pipeline position.** A parallel marketing track, not a sequential production stage.
> **Concept** begins at design lock, when the style, hero frames and logline exist.
> **Final** happens after picture lock, when the title, credits, rating and release date are
> fixed. `film-production` holds the gate; `film-postproduction` checks the files at delivery.

## Inputs

- Title, tagline, logline, genre, tone, audience, rating, release date.
- `02_design/style-lock.md` — palette, lens, grain, medium.
- Approved hero frames and location plates from `film-design` and `character-design`.
- Credits: cast, director, writers, producers, studio, distributor. **Human-supplied.**
- Likeness rights and consent for any real person depicted.
- Required deliverables: one-sheet, teaser, character posters, streaming thumbnail, social.

## Step 1 — The brief

Write one page before generating anything:

```markdown
# Key Art Brief — <title>

**Promise:** the one feeling or question the image must sell.
**Focal subject:** face, object, place, ensemble, or type.
**Genre signal:** what makes the genre legible in one glance.
**Title hierarchy:** title first, image first, or face first.
**Tagline:** optional; one line, not a synopsis.
**Audience and platform:** where the thumbnail will be seen first.
**Constraints:** rating, credits, likeness, franchise rules, spoiler limits.
**Deliverables:** <list>.
```

The **thumbnail test** is the acceptance criterion: shrink the concept to 200 px wide. If the
subject, genre and title do not read, the concept fails before generation.

## Step 2 — Concept routes

Choose two or three; do not generate ten variations of one idea.

| Route | Use when | Risk |
|---|---|---|
| Character close-up | a star or a face carries the film | likeness and identity drift |
| Icon / object | one prop or symbol is the story | the object must be instantly readable |
| Environment | place or scale is the promise | can read as a travel poster |
| Graphic / typographic | the title is the concept | type must be composited, not generated |
| Ensemble | cast is the draw | crowded, thumbnail-illegible |
| Negative-space teaser | restraint is the campaign | needs a strong single image |
| Before/after or split | a transformation is the hook | reads as an ad |

Write one sentence per concept: "the image argues that ___". If it cannot be stated, it is a
mood board.

## Step 3 — Generate the art

Use `ai-image-art-direction` for the prompt syntax. Rules:

- **Compose for type.** Leave deliberate negative space for the title, tagline and billing
  block. Say where: "upper third empty sky", "lower third dark water".
- **Text is a choice, not a default.** If the concept is a designed title, generate it with
  a text-strong model and quote the exact string; if the title will be typeset, keep the art
  text-free. Never let the model improvise signage, credits or logos.
- **Aspect masters.** Generate at the largest master aspect (usually 2:3 for a one-sheet);
  plan crops to 16:9, 9:16 and 1:1 rather than stretching.
- **Keep the style lock.** Same palette, lens, grain and medium as the film.
- **Face at scale.** For a character poster, use the approved hero frame as the identity
  reference; do not re-describe the face from scratch.
- **Three to five concepts**, each with a distinct argument, not three tints of one image.
- **Approve the art before type.** A rejected layout is cheap; a rejected photoshoot is not.

Save `06_marketing/poster/art/<concept>/master.png` and a `prompt.json` beside it.

## Step 4 — Type and layout

Choose the type route before laying out:

| Element | Generate or composite? | Why |
|---|---|---|
| Title as artwork | generate, verify, re-set for print | GPT Image 2.5 xhigh, Ideogram 4.5, Recraft V4.1 for vector |
| Title as clean type | composite | exact kerning, brand consistency, print |
| Tagline | either; verify | short quoted text is reliable |
| Billing block / credits | **composite** | legal accuracy, dense type |
| Rating mark | **composite supplied asset** | must be the board's file |
| Laurels / release | **composite** | facts, not generation |

Composite in a vector or layout tool, or in HTML/CSS rendered headless. The template in
`assets/poster-template.html` is a working starting point. If you generate display type,
proofread every glyph and re-render at 100%; a single wrong letter fails the poster.

Layers, in hierarchy order:

1. **Art** — full bleed, graded to the style lock, darkened where type sits.
2. **Title** — the largest type; one treatment across the campaign.
3. **Tagline** — optional; smaller; never a synopsis.
4. **Billing block** — credits, small, condensed, legally accurate.
5. **Rating** — the correct board mark, not an invented one.
6. **Release** — date or "in cinemas", platform, or festival laurels.
7. **Studio / distributor marks** — supplied assets only.

Rules:

- **Title treatment is a brand asset.** Design it once; reuse it on every variant.
- **One focal point.** If the eye has three places to go, it has none.
- **Legibility at 200 px.** Test the final composite, not the art.
- **Contrast, not decoration.** Type over a busy image gets a scrim, not a drop shadow.
- **Safe areas.** Keep title and credits inside the trim; plan for platform crops.
- **Credits are contractual.** Do not invent, reorder, or abbreviate without the supplied
  block. If none is supplied, use a placeholder and flag it.

Layout patterns and safe areas: `references/poster-layouts.md`.

## Step 5 — Variants

| Variant | Aspect | Purpose |
|---|---|---|
| Theatrical one-sheet | 2:3 (27×40 in) | primary key art |
| Teaser | 2:3 or 16:9 | pre-release, less information |
| Character posters | 2:3 | one per lead, shared layout |
| Streaming thumbnail | 16:9 | platform tile; face and title legible at 200 px |
| Vertical social | 9:16 | stories, shorts, TikTok |
| Square social | 1:1 | feed |
| Banner | 16:9 or wider | site header, press kit |

Crop from the master with intent; do not auto-crop. Re-composite the type for each aspect,
or design a layout that survives the crop.

## Step 6 — Compliance and QC

- **Credits** — names, order, spelling, and billing block match the supplied contract.
- **Likeness** — consent and rights for every real person; no implied endorsement.
- **Rating** — the correct mark and descriptor for the territory.
- **Laurels** — only festivals actually won or selected; no invented awards.
- **AI disclosure** — follow platform and jurisdiction rules; record it in the manifest.
- **No spoilers** — the campaign image does not reveal the turn.
- **Text accuracy** — read every glyph; generators are not trusted with type.
- **Color** — sRGB for digital, CMYK conversion proofed for print.

Full checklist and specs: `references/poster-specs.md`.

## Step 7 — Deliver

| File | Spec |
|---|---|
| `poster_onesheet_27x40_300dpi.tif` | 8100×12000 px, CMYK or sRGB per printer |
| `poster_onesheet_2000x3000.png` | digital one-sheet, sRGB |
| `thumbnail_1920x1080.jpg` | streaming tile, sRGB, < 2 MB |
| `poster_9x16_1080x1920.png` | vertical social |
| `poster_1x1_1080x1080.png` | square social |
| `poster_teaser_2000x3000.png` | teaser variant |
| `character_<name>_2000x3000.png` | one per lead |
| `poster.pdf` | print-ready, fonts embedded |
| `poster-manifest.md` | files, sizes, credits source, AI disclosure, approvals |

Naming, color profiles and platform limits: `references/poster-specs.md`.

## Quality gate

- [ ] The brief states the promise and the focal subject.
- [ ] Two or three distinct concepts, each with a one-sentence argument.
- [ ] Art has deliberate negative space for type; any generated text is exact and verified
      glyph by glyph.
- [ ] Contractual text (billing block, rating, laurels, release) is composited, not generated.
- [ ] The approved art uses the film's style lock and hero-frame identity.
- [ ] Title treatment is designed once and reused.
- [ ] Billing block, rating, laurels and release are accurate and supplied.
- [ ] The final composite reads at 200 px.
- [ ] Every required aspect is re-composited, not stretched.
- [ ] Print and digital files meet the specs; manifest complete.
- [ ] Likeness, credits and AI disclosure are cleared.

## Reference map

| File | Contents |
|---|---|
| `references/poster-layouts.md` | layout archetypes, hierarchy, safe areas, thumbnail test, type rules |
| `references/poster-specs.md` | dimensions, formats, color, platform variants, QC, delivery manifest |
| `references/text-models.md` | which models render text well, at what length, and where they fail |
| `assets/poster-template.html` | a self-contained 2000×3000 HTML/CSS poster template |
