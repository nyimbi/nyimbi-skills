# Customer Segmentation Playbook

Builds MECE customer segments on decision-relevant differences and ranks them by
attractiveness and right to win. Run at **Full Case** depth (see
[../../strategy-diagnosis-and-framing/SKILL.md](../../strategy-diagnosis-and-framing/SKILL.md)).

## When to use

- Targeting and ICP definition, go-to-market focus, account coverage
- Pricing or packaging segments, retention strategy, product roadmap prioritization
- "Which customers should we prioritize?" / "Who is this offer actually for?"
- The segment definition feeds pricing (see
  `../../strategic-choices-and-economics/references/pricing-strategy.md`) and market
  sizing (see [market-mapping.md](market-mapping.md))

## Approach

Segment by differences that change a decision — needs, economics, behavior, strategic
value. Demographic or firmographic labels are acceptable only when they predict those
differences; otherwise they are descriptions, not segments. Segments must be MECE
(enforced per
[../../strategy-diagnosis-and-framing/references/frameworks-problem-solving.md](../../strategy-diagnosis-and-framing/references/frameworks-problem-solving.md))
and observable or testable in real data.

## Workflow

1. **Define the decision the segmentation must support.** A segmentation built with no
   decision in mind cannot be evaluated.
2. **Gather customer data**: performance metrics, usage patterns, needs, constraints,
   contract and channel data.
3. **Identify candidate dimensions** (needs, value per customer, behavior, use case,
   acquisition channel, cost to serve).
4. **Build MECE segment options** — usually 2–3 competing cuts, not one forced answer.
5. **Score segments** on attractiveness (size, growth, profitability) and right to win
   (fit, capability, differentiated right to serve) — keep the two axes separate.
6. **Recommend priority segments** with explicit implications: targeting, offer,
   pricing, product, coverage, retention.

## Output format

```markdown
# Customer Segmentation

## Segmentation Objective
[Decision the segmentation supports.]

## Segment Definitions
| Segment | Defining Traits | Needs | Economics | Behavior |
|---|---|---|---|---|

## Segment Prioritization
| Segment | Size | Growth | Profitability | Fit | Priority |
|---|---|---|---|---|---|

## Strategic Implications
[Targeting, offer, pricing, product, coverage, or retention implications.]
```

## Quality bar

Playbook checks on top of the SKILL.md checklist:

- [ ] Segments are MECE enough to route a budget, not just to describe a population
- [ ] Each definition is observable or testable in available data
- [ ] Priorities follow stated criteria, not preference
- [ ] Attractiveness and right to win are scored separately
- [ ] Every priority segment states what changes because of it
