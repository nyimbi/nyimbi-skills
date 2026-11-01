# Competitive Intel Playbook

Models likely competitor moves from incentives, capabilities, constraints, and market
position — then pre-commits responses. Run at **Full Case** depth (see
[../../strategy-diagnosis-and-framing/SKILL.md](../../strategy-diagnosis-and-framing/SKILL.md));
**Client Deliverable** when the response plan goes to leadership.

## When to use

- Before making a competitive move: market entry, pricing change, product launch,
  channel conflict, M&A threat, share defense
- "What will competitors do next?" / "How will they react to this move?"
- Upstream of `../../strategic-choices-and-economics/SKILL.md`, where options are compared
  — competitor response is an input to that comparison, not the comparison itself

## Approach

Do not stop at competitor facts. Infer behavior from what a rational rival would do
given its **goals, assets, constraints, and economics**, and pre-commit responses
before rivals move. Facts are collected first (evidence labels per
[../../strategy-diagnosis-and-framing/references/evidence-standards.md](../../strategy-diagnosis-and-framing/references/evidence-standards.md));
the inference from facts to likely moves is where the analysis lives.

## Workflow

1. **Define the strategic move or market question** the intel must inform.
2. **Identify competitors and substitutes** — direct, adjacent, and the "do nothing /
   customer does it themselves" alternative.
3. **Map each competitor**: position, incentives (what management is measured on,
   ownership, strategic mandates), capabilities and assets, constraints (balance sheet,
   regulation, channel, attention), and unit economics.
4. **Infer likely moves** under base, aggressive, and defensive scenarios. For each,
   state the trigger that would cause it and your confidence.
5. **Assess impact** on the user's strategy: revenue, share, price, channel, talent.
6. **Recommend pre-emptive or reactive moves** tied to the user's own economics and
   capabilities, with early-warning indicators and kill conditions.

**Collection methods.** Evidence base per competitor: filings and earnings calls,
pricing and packaging pages, product release notes, job postings (capability signals),
partner/channel announcements, review sites, and ad libraries — ad-library mining is a
dedicated method in
[competitive-ads-extractor.md](competitive-ads-extractor.md) and feeds this playbook's
competitor map rather than replacing it.

## Output format

```markdown
# Competitive Intel

## Competitor Map
| Competitor | Position | Incentives | Capabilities | Constraints |
|---|---|---|---|---|

## Likely Moves
| Competitor | Most Likely Move | Trigger | Impact | Confidence |
|---|---|---|---|---|

## Response Plan
| Scenario | Early Signal | Recommended Response |
|---|---|---|

## Strategic Implication
[What this means for the user's decision — one paragraph.]
```

## Quality bar

Playbook checks on top of the SKILL.md checklist:

- [ ] Every predicted move states *why* the competitor would act, not only *what* they may do
- [ ] Likely moves are separated from high-impact tail risks
- [ ] Each scenario has an observable early-warning indicator
- [ ] Responses are affordable for the user's economics and capabilities
- [ ] Competitor facts and inferred moves are labeled differently
