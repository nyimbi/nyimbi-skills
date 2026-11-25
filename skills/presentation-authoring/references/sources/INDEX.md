# Source Index

Archived 2026-11-02 from two MIT-licensed packs published by Oria. They are the method
layer behind Oria's PowerPoint add-in; no add-in code, account, or proprietary asset was
inspected or copied.

| Archive | Source | Contents |
|---|---|---|
| `oria-deck-skills/` | https://github.com/andreworia/claude-powerpoint-skills | 12 deck-craft skills: ghost deck, SCQA narrative, action titles, executive summary, decision page, chart selection, waterfall, chart-to-message, colour encoding, data-ink, framework slides, partner review |
| `oria-pptx-skills/` | https://github.com/andreworia/claude-pptx-skills | 19 file and template skills: masters, layouts, placeholders, theme colour and fonts, grid, furniture, brand palette, logo, icons, imagery, native charts, font embedding, export, accessibility, notes, file size, reskin, brand audit, `.potx` construction |

Both packs: MIT, Copyright (c) 2026 Oria. Licence texts are in
[`../licenses/`](../licenses/).

## What was adapted

- [`../deck-craft.md`](../deck-craft.md): synthesis of the 12 deck skills, merged with the
  bundle's existing memo-first and investor-deck rules. It keeps the ghost-deck gate,
  action-title test, chart-selection tree, waterfall construction, one-accent colour rule,
  data-ink pass, framework archetypes, and partner-review order.
- [`../template-and-brand.md`](../template-and-brand.md): synthesis of the 19 file skills.
  It keeps the `.potx`/`.thmx` distinction, twelve colour slots, placeholder `idx`
  inheritance, theme binding, grid/safe zone, brand assets, font embedding and fallbacks,
  tagged PDF export, WCAG checks, notes/handout separation, and file-size method.

## What was not copied

- No Oria add-in code, service, prompt library, or account material.
- No marketing claims or product links beyond the source citation.
- No per-skill duplication: the 31 skills overlap heavily and are consolidated into two
  references under one owner, `presentation-authoring`.

Relative links inside the archived READMEs point at their upstream repositories and are
intentionally left unresolved.
