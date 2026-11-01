# Formatting & layout contract

Applies to **every** course and every destination — a workspace directory, plain
files, or the site. Where the destination is nyimbi.com, Appendix A overrides
and extends the portable rules. Phase 5 lessons are written to this contract,
and the between-lessons style check runs its pre-flight list. Pedagogy is set
by SKILL.md and the phase prompts; this file is only about how the result
*looks and reads*. A lesson that violates it renders badly no matter how right
it is.

## 1. Source dialect

- GitHub-flavoured Markdown. ATX headings (`#`, `##`). Pipe tables only.
- **No grid or ASCII tables** — no `-----` rules, no column alignment by
  spaces. If a table cannot be a pipe table, it is a list or a diagram.
- Raw HTML is allowed for exactly four things: `<details>` (hint ladders),
  `<figure>`/`<svg>` (diagrams), `<dl>` (term lists), and nothing else.
- Blank lines around every block element. No tabs; two-space indent inside
  list items. No lines over ~120 characters except table rows and URLs.

## 2. Headings and navigation

The heading tree **is** the lesson's navigation. It must be real, regular and
shallow.

- Parts are `##`, subsections `###`, at most `####`. Never skip a level; never
  go below `####`.
- Section numbers live in the heading text, not a list: `## 4.2 The balance
  after n periods`. One H1 per document, only when the destination has no
  frontmatter title (Appendix A: the site supplies the title — no H1).
- **A line of bold text is not a heading.** If it introduces a section it is a
  heading; bold inside body text emphasises, it never structures.
- Heading text is a noun phrase with no trailing colon and no "Section" prefix.

## 3. Typography

A 10,000-word lesson is read in sittings. The furniture carries the reader
between them.

- Paragraphs hold one idea, at most ~90 words (hard stop 120). A paragraph
  that needs three sentences joined by semicolons is three paragraphs.
- List items that name a concept take a bold lead-in: `- **Debit.** An entry
  on the left side of an account.` Items stay under two lines; no blank lines
  between items of one list (blank lines re-open the spacing the renderer just
  closed).
- Any comparison of three or more options is a table (SKILL.md invariant 4).
  Header cells name the axes and carry units (`Debit ($)`, `h (hours)`).
  Alignment row marks numeric columns right (`--:`).
- No ALL-CAPS emphasis, no exclamation marks, no decorative rules (`---` only
  as frontmatter or table delimiter), no emoji.
- Citations take one shape everywhere: `[Author, Year · tier A/R]`. Readings
  live in a table (`Reading | Tier | Status | Why it is assigned`), not in a
  prose list.

## 4. Mathematics

Wherever the course has formulas, they are written for a KaTeX-grade
renderer. These rules are not negotiable; each is the fix for a real
rendering failure.

- Inline math `$...$`; display math `$$...$$` with the delimiters alone on
  their line. **Never** `\(...\)`, `\[...\]`, or bare `align`/`align*`
  (use `aligned`).
- Inside math, `%` is a comment character: write `\%` or the rest of the
  expression silently vanishes. Currency in prose is `\$100`, never bare `$`.
- Unicode math glyphs (∂, θ, ×, ≤, →) stay out of formulas; use the TeX
  command. Outside formulas, the Unicode character is fine.
- Every display equation earns its display: if it fits inline without hurting
  readability, it goes inline. Walls of one-line displays read as sludge.
- Formulas keep their limit cases (dimensional check, degenerate case, sanity
  inversion) per the lesson contract — those checks are prose plus arithmetic,
  not more display math.

## 5. Diagrams

Two drawn diagrams per lesson (SKILL.md), and "drawn" means composed for the
lesson's own objects — never a stock shape with a new caption.

**Hand-drawn SVG (the default).** Wrap every diagram in a figure:

```html
<figure>
<svg viewBox="0 0 720 340" role="img" aria-labelledby="fig-3-1-t">
<title id="fig-3-1-t">The ε–δ game: adversary picks ε, defender answers with δ</title>
…
</svg>
<figcaption>Fig 3.1 — The ε–δ game, played at ε = 0.3. The defender's window
must answer every adversary window, not just this one.</figcaption>
</figure>
```

- Size by `viewBox`, never a fixed `width`/`height` attribute — the diagram
  scales with the column.
- Axes are labelled with **quantities and units** (`t (s)`, `loss (nats)`),
  ticks carry real numbers from the lesson's own examples, and every curve,
  node or region a reader must name has a text label.
- Text inside an SVG stays short (≤ ~40 characters per element) or it
  overflows at mobile widths; anything longer belongs in the caption.
- One palette per course, used in every diagram. For the site the palette is
  set (Appendix A); elsewhere pick paper/ink/accent/soft-ink once in the
  outline and hold it.
- Flat design: no gradients, shadows or 3D. Strokes 1.5–2, corner radius 0–2.
  Effective type ≥ 11px at full width. Budget ≤ ~8KB of SVG per diagram.

**Mermaid — conventional flowcharts only** (process shapes, no quantities).
Strict syntax, because a malformed diagram blanks the whole page on some
renderers rather than failing loudly:

- One edge syntax per edge: `A -->|label| B` **or** `A -- text --> B`.
  Never mix them (`A -- text -->|+| A` is a parse error).
- Quote any label containing parentheses, colons or pipes:
  `-->|"text (+)"|`.
- Node labels sit in brackets (`A[Parse error]`); every `subgraph` is closed
  by its own `end`. One statement per line.
- If the diagram has axes, quantities or geometry, it is not a flowchart —
  draw it as SVG.

## 6. Callouts, checks and collapsibles

The lesson's interactive furniture uses exactly these shapes, so a reader
learns the shapes once:

- **Concept checks and design principles are block quotes**, opening with a
  bold tag: `> **Concept check.** …`, `> **Design principle.** …`. The answer
  or principle text follows inside the same quote.
- **Trap exercises** open with a bold marker — `**Trap.**` — and the marking
  key names the belief that fails, per the lesson contract.
- **Worked examples close with "The lesson:"** (SKILL.md invariant 4): one
  sentence, no bold.
- **Hint ladders are collapsible, one rung per `<details>`:**

  ```html
  <details><summary>Hint 1 — nudge</summary>Look at what happens to the term
  when θ is small.</details>
  <details><summary>Hint 2 — mechanism</summary>The denominator is the prior
  odds; the numerator is the likelihood ratio.</details>
  <details><summary>Hint 3 — step</summary>Divide both sides by P(H) before
  taking logs.</details>
  ```

  The summary names the rung and its kind — never "click here". The answer
  appears only in `S N.M`, never inside a hint. Content must read correctly
  with every `<details>` open (print, no-JS, screen reader).

## 7. Pre-flight checklist (run before accepting any lesson)

**Renders**
1. Every section opener is a real heading at the right level; no bold-line
   pseudo-headings.
2. Every table is a pipe table with header, delimiter row and named axes;
   numeric columns right-aligned; no ASCII tables anywhere.
3. `$$` balanced; `%` escaped inside math; only `aligned`; no `\[\]`/`\(\)`.
4. Each diagram is figure-wrapped SVG with `<title>` and caption, or a
   strictly-syntaxed mermaid flowchart.
5. No raw HTML outside the four allowed uses.

**Reads**
6. No paragraph over 120 words; no list item over two lines; no blank lines
   inside a list.
7. Every concept check / design principle / trap is tagged; every worked
   example closes with "The lesson:".
8. Hints are collapsed rungs; answers live in the solutions only.

**Measures**
9. Word count ≥ 10,000 including tables; ≥ 2 drawn diagrams; neither
   constraint met by padding.

---

## Appendix A — nyimbi.com site contract (the default destination)

The portable rules above all apply, plus:

- **Frontmatter**: `title: "Lesson N: …"` and `order: N`; add a one-line
  `summary:` (it is the SEO/description string). No H1 in the body — the
  layout renders the title. An optional first line in bold gives the slot:
  `**Weeks 3–4. Prerequisite: Lesson 2 and the prelude, §P.3.**`
- **Internal links** between lessons take the site form
  `/learning/<course-slug>/NN/` — root-relative, no `.md`.
- **Prompt artefact boxes**: a reusable prompt the lesson hands the learner is
  filed inline, in its own paragraph, as `[[prompt: You are a skeptical CFO…]]`
  — the site renders it as a stamped box with a copy button.
- **Margin notes**: an aside that would be a parenthetical in print goes in
  the margin instead — its own line, immediately after the block it annotates:
  `[[note: The textbook says Poisson. The queue says otherwise.]]`. Use
  `[[hand: …]]` for the variant in the handwriting face. Neither moves a fact
  the main text depends on; the article must read complete with margins
  collapsed.
- **Diagram palette** (hold it across the whole course): paper `#fffdf6`,
  ink `#1b2a52`, accent/rule `#bc3520`, soft ink `#5a5a52`, desk `#f3efe4`.
- **Math** is rendered at build time; a broken equation fails the deploy, and
  an unrendered lesson page fails it too. Before building, run
  `node tools/audit_math.mjs content/<slug>` (ground truth per expression);
  the smoke test is `pnpm build` in the site repo, which runs the gates.
- Deploys ship `dist/` only; nothing outside `content/`, `src/` and `public/`
  affects a lesson page.
