# Portfolio Review Playbook

Reviews a set of businesses, products, markets, initiatives, or bets and recommends
allocation moves — invest, hold, fix, harvest, exit. Run at **Full Case** depth (see
[../../strategy-diagnosis-and-framing/SKILL.md](../../strategy-diagnosis-and-framing/SKILL.md));
**Client Deliverable** for capital-allocation or annual-planning reviews.

## When to use

- Product, market, initiative, or customer portfolios; capital and resource allocation
- "Where should we invest?" / "What do we stop funding?" / "Which bets stay?"
- Portfolio *level* questions — single-option economics belong in
  [business-case-builder.md](business-case-builder.md)

## Approach

Compare portfolio elements on consistent criteria across two separate axes:
**attractiveness** (market growth, profit pools — inputs from
`../../market-and-competitive-intelligence/SKILL.md`) and **performance / right to win**
(internal). Scoring structures for the classic grids (growth-share, GE nine-box) are
in `../../market-and-competitive-intelligence/references/frameworks-strategy.md`.
Recommend allocation actions, not rankings — a ranked list with no moves is a report.

## Workflow

1. **Define the portfolio and decision question**: what is included, what is excluded,
   what resource is being allocated.
2. **Select evaluation criteria** — identical for every element, with weights stated.
3. **Score each element**, keeping attractiveness and internal strength separate.
4. **Classify** into invest, maintain, fix, harvest, and exit candidates.
5. **Assess reallocation implications**: what moves, what it costs, what capability or
   runway it consumes, and what concentration risk it creates.
6. **Recommend portfolio moves** and the decisions required to authorize them.

## Output format

```markdown
# Portfolio Review

## Portfolio Scope
[What is included and excluded.]

## Evaluation Matrix
| Item | Attractiveness | Performance | Fit | Right To Win | Recommendation |
|---|---|---|---|---|---|

## Allocation Moves
| Move | Rationale | Resource Implication |
|---|---|---|

## Decisions Required
1. [Decision]
2. [Decision]
3. [Decision]
```

## Quality bar

Playbook checks on top of the SKILL.md checklist:

- [ ] One criterion set, applied identically to every element
- [ ] Performance is scored separately from attractiveness
- [ ] Every element ends in an allocation action, not a score alone
- [ ] Trade-offs created by reallocating are named (what gets starved)
- [ ] Exit/fix calls state what would change the call
