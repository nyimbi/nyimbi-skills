# House Style

## The decision memo

One page. Six sections, in this order:

1. **Bottom line.** The recommendation in one sentence, including the ask.
2. **Why now.** The trigger, the cost of waiting, and the deadline.
3. **The argument.** Three to five claims, each with its strongest evidence.
4. **Options considered.** Three real alternatives, including "do nothing", and why the
   recommendation beats them on the decision's own criteria.
5. **What would change my mind.** Kill conditions, thresholds, and the cheapest test.
6. **Next actions.** Owner, date, and the first milestone.

No executive summary before the bottom line. No slide titles that are labels rather than
claims.

## Evidence labels

| Label | Meaning | Required |
|---|---|---|
| `[F]` | Fact from a named source, with date | source and date |
| `[I]` | Inference from facts | the facts it rests on |
| `[A]` | Assumption | what would falsify it |
| `[E]` | Estimate | method and range |

A number without a label is treated as an assumption. A market size without a source is not
used.

## Modelling rules

- State currency, period, units, and discount rate before the first number.
- Decompose revenue into drivers (volume × price, or customers × ARPU × retention).
- Separate COGS from opex; state what scales and what does not.
- Include working capital and one-time costs in the investment.
- Print base, downside and upside, plus the sensitivity that matters.
- A single-point NPV is not a case. Show where it turns negative.
- Keep the config as JSON beside the output so the model can be rerun.

## Red team

Before recommending:

1. Name the three assumptions that carry the most weight.
2. For each, name the cheapest test and the cost of being wrong.
3. Ask what would have to be true for the opposite recommendation to be right.
4. Look for the second-order effect: what does this choice make harder later?
5. Check the denominator: is the comparison against the right baseline?

## Deck production

A deck is an artifact, not an argument. The argument is approved first, in the memo or
in `business-plan-authoring/references/deck-map.md`; the deck compresses it. Build the
ghost deck (titles and exhibit sketches) before any design work, using
`presentation-authoring/references/deck-craft.md`.

| Deliverable | Route |
|---|---|
| Direct `.pptx`, template fill, existing-deck edit, speaker notes | `presentation-authoring` |
| Default personal template | `presentation-authoring/assets/nyimbi-strategy.potx` |
| Browser-native React deck, presenter mode, HTML/PDF/PPTX export | `open-slide` |
| Visual identity, palette, typography for either | `visual-design-and-branding` |

Rules:

- One claim per slide, stated as the slide title. A label title is a failed slide.
- Every number traces to the memo or evidence ledger; proofs go in the appendix.
- 10–15 core slides. More means the memo was pasted into slides.
- The first paragraph of the story is written for the highest-power skeptic.
- Render every slide to an image and inspect it before delivery. A `.pptx` that
  opens is not a deck that reads.
- The handoff package is: per-slide claim, data references, appendix list, template or
  brand assets, and the decision the deck must win.

## Personal voice

- Answer first, then evidence. No throat-clearing.
- Concrete nouns and numbers. "Three payment rails" beats "the payments landscape".
- Short sentences. One idea per paragraph.
- Say "I don't know" and name the test that would settle it.
- No adjectives doing the work of a number.
