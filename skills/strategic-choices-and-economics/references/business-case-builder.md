# Business Case Builder Playbook

Quantifies a strategic option: value drivers, costs, scenarios, sensitivities, and the
decision threshold. Run at **Full Case** depth (see
[../../strategy-diagnosis-and-framing/SKILL.md](../../strategy-diagnosis-and-framing/SKILL.md));
**Client Deliverable** for funding decisions and board cases.

## When to use

- Investment decisions: new products, market entry, transformation programs, pricing
  moves, M&A screening, major initiatives
- "Does this business case work?" / "What ROI and payback?" / "Is this worth funding?"
- The option set comes from [strategic-options.md](strategic-options.md) — this
  playbook quantifies options, it does not generate them

## Approach

Build around decision logic, not spreadsheet detail. Make assumptions visible, size
value and cost, run base/downside/upside, and state the threshold the case must clear.
Unit economics, profit trees, and bridge/waterfall mechanics:
[frameworks-financial.md](frameworks-financial.md). Every load-bearing assumption goes
into the register owned by
`../../strategy-diagnosis-and-framing/references/assumption-audit.md`, with its kill
condition flowing back into the recommendation.

## Workflow

1. **Define the decision and the option under review** — plus the threshold (hurdle
   rate, payback limit, budget cap) it must meet.
2. **Identify value drivers, cost drivers, timing, and risks.** Size market-side value
   inputs from
   `../../market-and-competitive-intelligence/references/market-mapping.md` rather than
   inventing them.
3. **Build base, downside, and upside cases** — same structure, different assumptions;
   show which assumption moves each scenario.
4. **Surface load-bearing assumptions**: high importance, weak evidence → register and
   test plan (assumption-audit playbook).
5. **Calculate decision-relevant metrics**: ROI, payback, NPV where cash timing
   matters, margin impact, cash impact. Precision follows evidence — a two-significant-
   figure NPV with six-digit inputs is false precision.
6. **Recommend** proceed, test, redesign, or stop — with the metrics that drove it and
   the sensitivity that would flip it.

## Output format

```markdown
# Business Case

## Decision
[Decision and option under review.]

## Economics Summary
| Metric | Downside | Base | Upside |
|---|---|---|---|

## Value Drivers
| Driver | Assumption | Evidence | Sensitivity |
|---|---|---|---|

## Cost and Investment
[Major cost categories and timing.]

## Risks
[Key risks and mitigations.]

## Recommendation
[Decision and rationale.]
```

## Quality bar

Playbook checks on top of the SKILL.md checklist:

- [ ] Assumptions carry evidence labels and confidence, and load-bearing ones are registered
- [ ] Downside and sensitivity are shown — base case alone is not a business case
- [ ] Metrics are tied to the actual decision threshold, not reported for show
- [ ] No false precision: rounding matches evidence quality
- [ ] The rejected option has survived the same scrutiny as the recommended one
