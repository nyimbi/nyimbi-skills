# Research, Citations, and Hooks

Deep detail for step 4 of the [SKILL.md](../SKILL.md) workflow. Use when a draft makes
claims that need backing, or when the opening line is doing no work.

## Outline before prose

```markdown
# Article Outline: [Title]

## Hook          — [opening line/story/statistic] · [why the reader should care]
## Introduction  — context, problem, what this covers
### Section 1: [Title]
- Key point A · Key point B · Example/evidence
- [Research needed: specific question]
### Section 2: [Title]
- Key point · data/citation needed
## Conclusion    — summary, call to action, final thought
## Research to-do
- [ ] find data on [topic]   - [ ] source citation for [claim]
```

Iterate the outline until the logic flows and every research gap is visible *before*
drafting. Keep research in a separate `research.md` so the draft stays prose.

## Extracting research

Search → identify credible sources → pull the specific fact, quote, or figure → attach
the citation immediately. Never carry a claim forward uncited; mark it `[needs source]`
instead so it cannot pass the evidence check unnoticed.

## Citation styles (pick one, use it consistently)

| Style | In text | At the end |
|---|---|---|
| Inline (author–year) | `Studies show 40% improvement (McKinsey, 2024).` | Reference list |
| Numbered | `Studies show 40% improvement [1].` | `[1] Author. (Year). "Title". Publication.` |
| Footnote | `…improvement^1` | `^1: Author. (Year). "Title". Publication.` |

Rules: verify the source before citing, prefer recent data, link to the original (not a
secondary write-up), and balance perspectives where the evidence is contested.

## Hooks

Analyse an existing opening on four axes — does it create curiosity, promise value,
stay specific, match the audience? Then offer three *named* alternatives rather than one
rewrite:

- **Bold claim** — a specific, defensible assertion
- **Personal scene** — a person, a moment, a consequence
- **Surprising data** — one number, with its source

Rewrite the user's hook; do not substitute a generic one. The hook must be supportable
by what follows — a hook that overpromises costs more than a flat opening.

## Section-by-section feedback

Return this shape while the user is still drafting, not after:

```markdown
# Feedback: [Section]
## What works
## Suggestions
- Clarity:  [issue] → [fix]
- Flow:     [transition] → [reordering]
- Evidence: [claim] → [add citation / make specific]
- Style:    [word choice] → [alternative]
## Line edits — original / suggested / why
## Questions to consider
```

## Voice preservation

Read existing samples before editing. Suggest rather than replace; offer options, not
directives. Enhance, don't override — if the user prefers their version, keep it. Check
in periodically: "Does this sound like you? Should this be more or less formal?"

## Final review

Assessment of structure and flow, content quality (argument, evidence, examples),
technical quality (grammar, consistency, citation completeness), readability (clarity,
sentence variety, paragraph length), then a pre-publish checklist:

- [ ] every claim sourced · [ ] citations formatted consistently · [ ] examples specific
- [ ] transitions smooth · [ ] call to action present · [ ] proofread
