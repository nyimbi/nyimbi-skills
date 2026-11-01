# Theme System — Presets, Application, and Generation

Technique file for the colour/type-system step of the [SKILL.md](../SKILL.md)
workflow. theme-factory supplies the **system**: a named palette plus a font pairing
that can be applied to slides, docs, reports, or HTML landing pages, or generated fresh
when none of the presets fit.

## Choose a theme

Show `../theme-showcase.pdf` so the user sees all ten rendered — never modify that file.
Wait for an explicit selection before applying anything.

| Theme | Register |
|---|---|
| Ocean Depths | professional, calming, maritime |
| Sunset Boulevard | warm, vibrant, sunset |
| Forest Canopy | natural, grounded, earth tones |
| Modern Minimalist | clean, contemporary grayscale |
| Golden Hour | rich, warm, autumnal |
| Arctic Frost | cool, crisp, winter |
| Desert Rose | soft, sophisticated, dusty |
| Tech Innovation | bold, modern tech |
| Botanical Garden | fresh, organic |
| Midnight Galaxy | dramatic, cosmic, deep |

Selection rule: match the register to the **audience and occasion** in step 1, not to
personal taste — an exec review and a team retro are different themes. When a brand
constraint applies (step 2), the brand wins and the theme is only a starting point for
secondary elements.

## Apply a theme

1. Read the matching file in `../themes/<name>.md` — it carries the hex palette and the
   header/body font pairing with roles already assigned.
2. Apply colours to their roles (background, text, primary/secondary accent, rules) —
   never to decorative fills that carry no meaning.
3. Apply the font pairing to its role: header face to headings, body face to body copy.
   Do not introduce a third family.
4. Check contrast for every text/background pair before delivery; raise or lower
   luminance until body text passes AA.
5. Keep the identity consistent across every surface of the artifact — one theme per
   artifact, no per-slide improvisation.

## Generate a custom theme

When no preset fits, generate one to the same specification as the presets:

- Name it for what the combination *is* ("Slate Harbor", "Copper Meadow"), not for the
  client.
- Deliver 4–6 named hex values with roles: background, surface, text, and 2 accents.
- Deliver exactly two typefaces with a stated role each, plus a system fallback stack.
- State the register in one sentence and show the theme for review before applying it.

A generated theme must be as complete as a preset — a palette without roles and a font
pairing without assignments is not a theme.

## Guardrails

- Do not restyle a themed artifact mid-way; if the direction is wrong, change the
  theme once, deliberately, rather than accumulating one-off exceptions.
- Icons, charts, and rules take the accent palette; body and background never do.
- When the artifact is an office file (deck, doc, workbook), this file supplies the
  colour/type specification and `presentation-authoring` or `word-document-authoring`
  applies it to the actual file — this skill never generates those containers.
