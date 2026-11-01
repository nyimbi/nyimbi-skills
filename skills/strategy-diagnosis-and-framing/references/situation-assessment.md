# Situation Assessment Playbook

Establishes a defensible fact base for a business, market, product, or function before
any strategy is chosen. Run at **Full Case** depth (see
[SKILL.md](../SKILL.md)); use **Client Deliverable** when the read goes to a board or
leadership team.

## When to use

- Business reviews, turnaround diagnosis, market-position checks, operating-performance reviews
- Board or IC preparation where the audience will challenge the baseline
- Any strategy question that starts with "where are we really?"
- Precedes option generation — never recommend before the baseline exists

## Approach

Build the fact base before debating solutions. Look across financial performance, market
position, customer momentum, competitive posture, operating health, and organizational
constraints. Facts, interpretations, and open questions are labeled separately using the
`[F]/[I]/[A]/[E]` evidence codes from
[evidence-standards.md](evidence-standards.md).

## Workflow

1. **Frame the question.** Write the decision this assessment informs and who makes it
   (clarify step in SKILL.md). A baseline built for the wrong decision is waste.
2. **Collect the available facts.** Financials, KPIs, market data, customer signals,
   competitive context, recent changes. Record source and time period for every figure.
3. **Build a MECE current-state view** across performance, market, customers, operations,
   and organization — one level of branches, no overlaps, no gaps.
4. **Identify the few facts that matter** for the decision. Most of the fact base is
   context; 3–5 facts usually carry the read.
5. **Separate confirmed facts from hypotheses and unknowns.** Unknowns become the
   "Open Questions" list and, where they are load-bearing, feed
   [assumption-audit.md](assumption-audit.md).
6. **Write the read with implications.** State what each finding means for the decision;
   hand off to [growth-barriers.md](growth-barriers.md) when performance is the issue, or
   to `../../market-and-competitive-intelligence/SKILL.md` when the gap is external.

## Output format

```markdown
# Situation Assessment

## Executive Read
[One paragraph on where the business is and why it matters.]

## Fact Base
| Area | Evidence | Interpretation | Confidence |
|---|---|---|---|

## Momentum Signals
| Signal | Direction | Why It Matters |
|---|---|---|

## Strategic Issues
1. [Issue]
2. [Issue]
3. [Issue]

## Open Questions
[Questions that must be answered before committing to a strategy.]
```

## Quality bar

Playbook checks on top of the SKILL.md checklist:

- [ ] No recommendation appears before the baseline is stated
- [ ] Every fact carries source, unit, and time period; interpretations are labeled `[I]`
- [ ] Trend and momentum are shown, not only point-in-time values
- [ ] Every issue ends with an explicit "so what" for the decision at hand
- [ ] Open questions name how they would be answered, not just that they exist
