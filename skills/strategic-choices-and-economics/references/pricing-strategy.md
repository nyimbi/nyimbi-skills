# Pricing Strategy Playbook

Diagnoses pricing power, willingness to pay, discount leakage, and packaging, then
recommends a tested pricing move. Run at **Full Case** depth (see
[../../strategy-diagnosis-and-framing/SKILL.md](../../strategy-diagnosis-and-framing/SKILL.md));
**Client Deliverable** for a pricing transformation or price-increase decision.

## When to use

- Improving monetization: price increases, discount control, packaging redesign,
  renewal pricing, value-based pricing, margin improvement
- "Where are we leaking price?" / "Should we raise prices?" / "How should we package this?"
- Method selection (value-based, cost-plus, competitive, dynamic, freemium):
  [frameworks-pricing.md](frameworks-pricing.md) — this playbook owns the diagnosis and
  rollout, not the framework walkthroughs

## Approach

Connect price to value, customer segments, competitive alternatives, and sales
behavior. Separate **list price, realized price, discounting, mix, and packaging** —
a pricing problem in one of them is invisible in the others. Segment logic comes from
`../../market-and-competitive-intelligence/references/customer-segmentation.md`; rival
price positions and likely reactions from
`../../market-and-competitive-intelligence/references/competitive-intel.md`; the margin
pool at stake from
`../../market-and-competitive-intelligence/references/profit-pool-analysis.md`.

## Workflow

1. **Define the pricing question and economic objective**: growth, margin, retention,
   adoption, or simplification — one primary objective.
2. **Gather the data**: price architecture, realized-vs-list waterfall, discount
   distribution, win-loss, churn, margin by SKU/segment, competitor price positions.
3. **Diagnose leakage** across list price, discounting, mix, packaging, and governance
   — quantify each so the biggest lever is visible.
4. **Assess willingness to pay** by segment or use case: value drivers, switching
   costs, competitive alternatives, observed WTP signals (win-loss, churn response,
   tests).
5. **Generate pricing moves** with their risks: customer perception, sales-execution
   risk, competitive reaction, channel conflict.
6. **Recommend an action plan with a test design**: pilot population, success metric,
   rollout sequence, rollback trigger.

## Output format

```markdown
# Pricing Strategy

## Pricing Objective
[Growth, margin, retention, adoption, or simplification.]

## Diagnosis
| Area | Evidence | Issue | Impact |
|---|---|---|---|

## Segment Price Logic
| Segment | Value Driver | WTP Signal | Pricing Move |
|---|---|---|---|

## Recommended Moves
1. [Move]
2. [Move]
3. [Move]

## Risks and Tests
[Risks, mitigations, and pilot design.]
```

## Quality bar

Playbook checks on top of the SKILL.md checklist:

- [ ] No price move without segment-level value logic behind it
- [ ] Realized price is analyzed separately from list price, with the discount waterfall shown
- [ ] WTP claims are backed by evidence, not asserted
- [ ] Customer risk and sales-execution risk are both covered
- [ ] Every move ships with a test or rollout sequence and a rollback trigger
