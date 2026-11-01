# Profit Pool Analysis Playbook

Maps where profit is created, captured, and leaking across a market, value chain,
product set, or customer base. Run at **Full Case** depth (see
[../../strategy-diagnosis-and-framing/SKILL.md](../../strategy-diagnosis-and-framing/SKILL.md)).

## When to use

- Revenue size is misleading and the question is where attractive profit actually sits
- Market entry, product portfolio, channel, value-chain, and segment strategy questions
- "Where does the money go?" / "Why is a big market unprofitable?"
- Pricing power and margin-improvement scoping — the pricing moves themselves belong to
  `../../strategic-choices-and-economics/references/pricing-strategy.md`

## Approach

Follow the money across the system. Revenue pools and profit pools are different maps:
a large revenue pool at 3% margin is not an attractive pool. Show margin and profit,
name who captures value and why, and tie every finding to an allocation or positioning
decision. Market size and segment growth come from
[market-mapping.md](market-mapping.md) — this playbook does not size the market.

## Workflow

1. **Define the scope**: market, value chain, product set, customer base, or channel —
   with the boundary inherited from [market-mapping.md](market-mapping.md) where one exists.
2. **Map revenue and margin by activity, segment, product, channel, or customer group.**
   Revenue tree and profit tree mechanics:
   `../../strategic-choices-and-economics/references/frameworks-financial.md`; activity
   mapping via the Value Chain in [frameworks-strategy.md](frameworks-strategy.md).
3. **Identify concentration and leakage** — where profit pools are thick, where margin
   erodes between activities, and who sits on the toll booth.
4. **Assess structural drivers**: scale, pricing power, cost position, switching costs,
   competitive intensity. State the structural reason profit concentrates — an observed
   concentration with no mechanism is a coincidence, not an insight.
5. **Classify pools** as attractive, contested, or structurally unattractive.
6. **Recommend implications**: where to play, where to avoid, how to improve capture.

## Output format

```markdown
# Profit Pool Analysis

## Scope
[Market, products, customers, or value chain included.]

## Profit Pool Map
| Pool | Revenue | Margin | Profit | Growth | Attractiveness |
|---|---|---|---|---|---|

## Value Capture
| Player or activity | Value captured | Reason |
|---|---|---|

## Strategic Implications
1. [Where to play]
2. [Where to avoid]
3. [How to improve capture]
```

## Quality bar

Playbook checks on top of the SKILL.md checklist:

- [ ] Revenue size is never used as a proxy for attractiveness
- [ ] Margin and profit are shown alongside growth for every pool
- [ ] The structural driver behind each concentration is stated explicitly
- [ ] Findings convert to allocation or positioning decisions, not observations
- [ ] Margin estimates are labeled with their source and confidence
