# Deck Craft

The narrative and exhibit layer above the `.pptx` file. Load this after the argument is
approved and before a slide is built. The investor-deck variant is
[`../../business-plan-authoring/references/deck-map.md`](../../business-plan-authoring/references/deck-map.md);
the board/IC narrative method is `executive-communication-and-alignment`.

Adapted from Oria's MIT-licensed `claude-powerpoint-skills` pack. See
[`sources/INDEX.md`](sources/INDEX.md).

## Order of work

1. **Ghost deck.** Agree the argument as titles only.
2. **Action titles.** Rewrite every title as a claim.
3. **Exhibits.** Choose the chart from the message, then finish it.
4. **Build.** Only now open the authoring route in `SKILL.md`.
5. **Partner review.** Review story first, craft second.

Designing before step 2 is the expensive mistake.

## Ghost deck

A ghost deck is one empty slide per evidence leaf, in presentation order, with the final
title and an exhibit sketch. It is deliberately ugly so reviewers critique the logic, not
the polish.

For each slide record:

| Field | Content |
|---|---|
| Action title | The final sentence the slide must prove |
| Exhibit sketch | "waterfall from current to target margin", "2×2 of segments by growth and profit" |
| Data needed | The exact table or source, and whether you have it |
| Confidence | solid / likely / speculative |

Rules:

- One slide per leaf, plus dividers and the executive summary.
- Write the titles now. The title chain is the deliverable under review.
- Do not style anything. No colour, icons, or alignment work.
- Present the titles alone first. Fix the argument before fixing the slides.
- Speculative slides are candidates to cut; say so before they consume build time.

Output: a numbered slide list, the total page count, and the data-gapped or speculative
slides called out.

## Action titles

A title is an action title when it states the conclusion, not the subject. The test: read
only the titles and you can reconstruct the argument.

| Fail | Pass |
|---|---|
| "Q3 Revenue" | "Revenue grew 12%, but all of it came from one account" |
| "Customer Segmentation" | "Two segments drive 80% of profit, so the growth plan should concentrate there" |
| "Pricing Analysis" | "We hold pricing power only in enterprise, which is where a price increase should be taken" |
| "Market Overview" | "Competitor entry has commoditised the segment, so we cannot win on price" |

Rules:

- Full sentence with a real verb: grew, fell, concentrated, lagged. Not "relates to".
- One claim. If the slide proves two things, it is two slides.
- Specific and falsifiable. "We are well positioned" says nothing.
- One line. Cut qualifiers that hedge rather than inform.
- The body must prove the title. A sharp title over a body that argues something else is
  worse than a label.
- Run the title-only read at the end. A jump means a missing slide; a repeat means a
  redundant one.

## Executive summary page

One page, self-contained, answer first.

1. **Title** = the governing thought as a full sentence.
2. **Framing line** = period and lens, no argument ("Q2 results against the board-approved
   plan").
3. **Three to five proof points**, each one fact + one number + one so-what. Three is
   tight; five is the ceiling.
4. **The ask** in its own block: the decision and what approval commits. If it is a
   read-ahead, label it "For information".
5. **Source notes** for every number, traceable to a later page.
6. Reconcile every claim against the body. Nothing appears here that is not proven later.

If it does not fit on one page, the story is not sharp enough. Push detail down; do not
shrink the type.

## Decision and ask page

A board approves choices, not ideas.

1. **Decision question** phrased as the vote: "Approve the reallocation of capital across
   the initiative portfolio", not "Discuss our cost programme".
2. **Criteria first**: two to four, named before the options. Criteria stated after the
   recommendation read as rationalisation.
3. **Real options**, including the status quo. One option is not a decision page.
4. **Read each option against each criterion** as strong / adequate / weak. Do not invent
   precise scores.
5. **Recommendation and trade-off.** Name what you are accepting. A recommendation with no
   downside reads as naive.
6. **What approval commits**: money, mandate, timeline, and what changes the day after.
   Also state what it does not commit.
7. **Cost of delay**: one line.
8. **Two or three hard questions** with one-line answers.

## Chart selection

Start from the sentence the audience must remember, not from the data.

| Message type | Encoding |
|---|---|
| Comparison across categories | Horizontal bar, sorted by value; column only when categories are naturally ordered |
| Change over time | Line; column for few periods when level matters |
| Composition, one point in time | 100% stacked bar or labelled breakdown; pie only up to three slices |
| Composition, mix shift | 100% stacked column or stacked columns over time |
| Relationship between two measures | Scatter; bubble only if the third measure earns it |
| Distribution | Histogram or sorted dot plot |
| Bridge from start to end | Waterfall |

Disqualifiers:

- More than five lines: small multiples.
- More than seven stacked segments: regroup into "other" or show top items.
- Two numbers: a sentence or two large numbers beats a chart.
- One value against a target: a labelled bullet bar, not a gauge.
- The chart must restate the title within five seconds, or return to the message.

Prefer position and length; treat angle and area as last resorts.

## Chart to message

1. **Title = takeaway**, not "Revenue by region".
2. **One thing to see.** Decide the single bar, inflection, or gap; everything else is
   context.
3. **Colour as pointer.** Mute all marks; accent only the element that carries the message.
4. **Direct labels.** Label what matters; replace the legend with labels beside the series.
5. **Reference line.** Benchmark, target, or prior period, thin and labelled.
6. **One annotation** near the highlight, with a leader line. One, not five.
7. **Strip junk.** No 3D, shadows, heavy borders, background fills, or redundant axis
   titles. Gridlines or data labels, rarely both.
8. **Sort for meaning.** Bars by value unless time order is the point.
9. **Cover the title test.** If the chart no longer implies the title, the highlight or the
   data is wrong.

## Waterfall and bridge

A waterfall reconciles an opening value to a closing value through signed drivers.

1. List opening, each driver with sign and magnitude, and closing. They must sum exactly.
   If not, add an explicit "other / unexplained" bar; do not hide the gap.
2. Order deliberately: largest first, or a logical sequence (volume, price, mix, cost).
   Keep the order stable across periods.
3. Build floating bars from a stacked column: totals rest on zero; each delta floats on the
   running cumulative before it; the base series has no fill.
4. Colour by direction: one colour for increases, one for decreases, neutral for totals.
   Accent the single most important driver or the closing value.
5. Thin grey connectors from the top of one bar to the base of the next.
6. Label every bar with its signed value. The reader should be able to check the arithmetic.
7. Validate: opening + signed deltas = closing. State the reconciliation in one line.
8. Build native in PowerPoint so it stays editable.

## Colour encoding

- Start with one muted base colour. Add a second only to encode a real distinction.
- **Categorical**: distinct hues, similar saturation, five or six at most; same category =
  same hue across the deck.
- **Sequential**: one hue, light to dark; darker means more.
- **Diverging**: two hues meeting at a neutral midpoint; only when the midpoint is real.
- **Accent once per slide**, on the element the eye must land on.
- Bind chart colours to theme accents in order so a re-theme carries through.
- Check colour-vision deficiency and greyscale; pair colour with position or labels.
- Do not recolour a real logo to fit the palette.

## Data-ink

1. Inventory every mark: bars, lines, gridlines, borders, fills, shadows, legends, ticks.
2. Remove decoration first: shadows, 3D, gradients, heavy borders, background fills.
3. Remove redundant data ink: if the bar shows magnitude, the axis can be light and the
   label can replace gridlines. Gridlines or labels, not both.
4. Lighten what remains: faint gridlines, thin axes, few ticks, one muted palette plus one
   accent.
5. Cut decimal noise. "12%" beats "12.3847%".
6. Replace legends with direct labels.
7. Reduce, do not amputate. Keep the reference line, the annotation, and the labels that
   carry the message.
8. Compare before and after; if anything got harder to read, restore it.

## Framework slides

Pick the archetype from the relationship:

| Relationship | Archetype |
|---|---|
| Two crossing dimensions | 2×2 |
| Linear sequence | Process flow or value chain |
| Hierarchy | Pyramid or tree |
| Parallel components | Columns or wheel |
| Maturity over levels | Stairway |

Rules:

- Label axes with a clear low-to-high meaning; name all four quadrants.
- Each box carries one line of substance, not just a label.
- Establish one reading path: left to right for flows, bottom to top for pyramids, a marked
  starting quadrant for matrices.
- Highlight the conclusion (the quadrant you are in, the broken stage) with the accent; the
  rest stays neutral.
- Equal box sizes, even gaps, one corner style, everything on the grid.
- Arrows only for real flow or causation.
- If the framework is generic, add a callout that says what it implies here.

## Partner review

Review top-down: story before slides, message before format. Return Blockers, Majors,
Minors, each tied to a slide number. Lead with a one-line verdict.

1. **Story and answer**: one recommendation up front; the executive summary alone supports
   the decision.
2. **Title chain**: every title is a claim; the sequence argues without gaps.
3. **Logic**: groups are MECE; every section ladders up; no orphan slide.
4. **Exhibit fit**: right chart for the message; one insight highlighted; comparison anchor
   present; no chart implying a different conclusion than its title.
5. **Craft**: grid, spacing, type scale, palette, one accent, one icon family.
6. **Density**: one message per slide; split overloaded, merge thin, push detail to backup.
7. **Consistency**: same category, colour, label, footnote, rounding, and source style
   everywhere.
8. **Evidence**: every number traceable; no claim beyond the data; assumptions stated.
9. **Ask**: the deck ends with a clear decision or action.
10. **Prioritise**: Blockers (story or logic broken), Majors (title or exhibit wrong),
    Minors (alignment, colour). Fix Blockers first.

End with the three highest-impact fixes.

## Handoff to build

Give `presentation-authoring` the accepted ghost deck, the final action titles, the exhibit
specs (chart type, highlight, labels, reference line, annotation), the data sources, the
template if one exists, and the ask. The build route is in `SKILL.md`; the template and
brand mechanics are in [`template-and-brand.md`](template-and-brand.md).
