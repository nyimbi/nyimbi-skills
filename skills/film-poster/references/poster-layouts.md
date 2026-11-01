# Poster Layouts

## Hierarchy

One focal point, then one title, then everything else. A poster that gives equal weight to
face, object, title and credits has no hierarchy.

```text
1. Art          60–80% of the visual weight
2. Title        the largest type, readable at 200 px
3. Tagline      optional, one line
4. Billing      small, dense, legally accurate
5. Rating       small, correct mark
6. Release      small, unambiguous
7. Marks        supplied studio/distributor assets
```

## Archetypes

### 1. Face and negative space

A close-up or medium close-up, eyes at the upper third, title in the empty sky or wall.
Works when the cast is the draw. Keep the face large enough to survive a thumbnail.

### 2. Figure in environment

A small figure against a large place. Sells scale, isolation or genre. Title in the sky or
the foreground. Risk: reads as a landscape photograph without type.

### 3. Object macro

One prop or symbol, lit dramatically. Sells mystery and genre. The object must be readable
at 200 px; if it needs a caption, it fails.

### 4. Ensemble

Cast arranged by power or story geometry. Title centered or lower third. Risk: crowded and
illegible at thumbnail; limit to five faces and one clear leader.

### 5. Negative-space teaser

Almost empty frame with one element and the title. Sells restraint and confidence. Needs a
strong single image and a title treatment that carries the campaign.

### 6. Split / before-after

Two states divided by a hard line, a mirror, or a color break. Sells transformation. Risk:
reads as an advertisement; anchor it with the film's texture and palette.

### 7. Typographic

The title is the image, built from texture, environment or type. Sells a concept. Never let
the image model render the letters; composite the type over a generated texture.

### 8. Character series

One layout, one lead per poster, shared title block and credits. The set reads as a campaign
only if the grid, type and light are identical.

## Safe areas

### Print one-sheet (27×40 in)

```text
trim:            27 × 40 in
bleed:           0.125 in on all sides
safe margin:     keep type ≥ 0.375 in inside trim
title zone:      usually upper or lower third, never over the focal eyes
billing block:   bottom, ≥ 0.375 in above trim
rating:          bottom corner, supplied mark
```

### Digital

| Format | Size | Safe margin |
|---|---|---|
| Digital one-sheet | 2000×3000 | 5% |
| Streaming thumbnail | 1920×1080 | 5%; title inside centre 80% |
| Vertical social | 1080×1920 | 8% top/bottom for platform UI |
| Square | 1080×1080 | 5% |
| Banner | 1920×1080 or wider | 5%; keep focal point off the far edges |

Plan the crop before generating. A 2:3 master cropped to 16:9 loses the top and bottom; put
the face and title where both survive, or re-composite for each aspect.

## Thumbnail test

1. Export the final composite at 200 px wide.
2. View it at arm's length on a phone.
3. Ask: can I name the genre, the subject and the title?
4. If not, simplify: fewer elements, larger face, stronger contrast, shorter title line.

## Type rules

- **Title treatment** is a brand asset: one typeface, one weight, one tracking, one color
  system. Design it once.
- **Contrast over decoration.** Use a scrim or a darker grade behind type, not an outline or
  a drop shadow.
- **Title case vs uppercase.** Uppercase reads at distance; title case reads as prestige.
  Pick one and keep it.
- **Line breaks are composition.** Break the title where it balances the image, not where
  the words end.
- **Tagline** is one line, smaller than the title, never a synopsis.
- **Billing block** is condensed, centered, and legible at 100% but not at thumbnail. It is
  a legal object, not a design element.
- **Generate display type only when the lettering is the artwork.** Quote the exact string,
  use a text-strong model, and verify every glyph. Typeset the billing block and all
  contractual text. See `text-models.md`.

## Color and texture

- Grade the art to the film's style lock. The poster is part of the film, not a separate
  campaign.
- Keep one accent color for the title or a single element. More than one accent competes.
- Grain, halation and texture should match the film; a clean poster for a grainy film reads
  as a different project.
- Check contrast in grayscale. If the title disappears, it will disappear on a bad screen.

## Common failures

| Failure | Cause | Fix |
|---|---|---|
| Unreadable thumbnail | too many elements, small face | simplify; enlarge the focal point |
| Title lost in the image | no scrim, low contrast | darker grade behind type, or move the title |
| Looks like a different film | palette or grain not matched | apply the style lock |
| Invented credits | generator rendered text | composite the supplied billing block |
| Cropped face | 2:3 master cropped to 16:9 | re-composite; do not auto-crop |
| Busy billing block | too many names, no hierarchy | use the supplied block; do not add |
| Fake laurels | invented awards | only actual selections |
| Wrong rating | invented mark | use the supplied board asset |
