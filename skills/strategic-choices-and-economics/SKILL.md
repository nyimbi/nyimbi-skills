---
name: strategic-choices-and-economics
description: >-
  Decide which option to take and what it is worth: generate distinct strategic
  options, compare them against the decision's own criteria, build quantified business
  cases with base/downside/upside economics and sensitivities, review portfolios of
  bets for allocation moves, and diagnose pricing power and discount leakage. Carries
  the decision, financial, and pricing framework libraries the strategy group links to
  — RAPID, weighted decision matrices, pre-mortem, second-order thinking, inversion,
  profit and revenue trees, TAM/SAM/SOM, unit economics, waterfall bridges, value-based
  and competitive pricing, freemium. Use when the user asks "what are our options",
  "should we invest in this", "build the business case", "what is the ROI and payback",
  "where should we invest", "should we raise prices", "how should we package this", or
  "which path do we take". Do not use for the fact base or root-cause diagnosis
(strategy-diagnosis-and-framing), for sizing markets or reading competitors
(market-and-competitive-intelligence), for roadmaps, org design, and initiative
delivery (operating-model-and-execution), or for a fundraise-ready business plan with
projections and a red-team pass (business-plan-authoring).
license: MIT
---

# Strategic Choices and Economics

Market skills say where the value is; this skill says **which option to take and what
it is worth.** It owns the choice layer: option generation, comparison logic,
quantified business cases, portfolio allocation, and pricing moves. Diagnosis of what
is true internally stays in
[../strategy-diagnosis-and-framing/SKILL.md](../strategy-diagnosis-and-framing/SKILL.md);
market size, segments, and competitor reads come from
`../market-and-competitive-intelligence/SKILL.md`.

This skill also hosts three shared framework libraries used across the strategy group:
[references/frameworks-decision.md](references/frameworks-decision.md),
[references/frameworks-financial.md](references/frameworks-financial.md), and
[references/frameworks-pricing.md](references/frameworks-pricing.md).

## When to use

- Option generation and path selection: "what are our options?", build-buy-partner, growth paths, sequencing
- Investment decisions: "should we invest?", "does this business case work?", ROI, payback, NPV, funding requests
- Portfolio and capital allocation: "where should we invest?", product/market/initiative portfolios, harvest or exit calls
- Pricing: "should we raise prices?", discount leakage, packaging, willingness to pay, renewal and value-based pricing
- Decision mechanics: who decides (RAPID), weighted option scoring, pre-mortems, second-order consequences
- Quantifying a market-entry, product, or transformation choice with downside and sensitivity cases

**Do not use for** — `strategy-diagnosis-and-framing` when the fact base, root cause,
or assumption register does not yet exist — options built on an unstated baseline are
fiction; `market-and-competitive-intelligence` when the question is still external:
market size, segment attractiveness, profit pools, competitor response; when the choice
is made and the question becomes how the organization changes, that is
`operating-model-and-execution`; a fundraise-ready business plan with projections and a
hostile red-team pass is `business-plan-authoring`, which *uses* this skill's
`business-case-builder.md` for its scenarios.

## Workflow

Detect depth mode first — Quick Structure / Full Case / Client Deliverable as defined
in
[../strategy-diagnosis-and-framing/SKILL.md](../strategy-diagnosis-and-framing/SKILL.md).
Quick Structure compares options in a table; Full Case and Client Deliverable run the
full sequence with the evidence, synthesis, and devil's-advocate gates.

1. **Frame the decision.** What is decided, by whom (decision rights — RAPID in
   [references/frameworks-decision.md](references/frameworks-decision.md)), by when,
   the constraint set, and the threshold an option must clear (hurdle rate, payback
   limit, budget cap). State it before generating options.

2. **Generate distinct options.** Run
   [references/strategic-options.md](references/strategic-options.md): 2–4 options
   differing in mechanism, "do nothing" explicit, hybrids only when they change the
   mechanism. Define decision criteria and weights from this decision.

3. **Quantify each option.** Run
   [references/business-case-builder.md](references/business-case-builder.md): value
   and cost drivers, base/downside/upside, ROI, payback, NPV where cash timing
   matters, and sensitivity. Unit economics, profit/revenue trees, and bridges:
   [references/frameworks-financial.md](references/frameworks-financial.md). Every
   load-bearing assumption is registered in
   `../strategy-diagnosis-and-framing/references/assumption-audit.md`; market inputs
   come from `../market-and-competitive-intelligence/references/market-mapping.md`.

4. **Set monetization where price is the lever.** Run
   [references/pricing-strategy.md](references/pricing-strategy.md) — diagnose realized
   vs list price, leakage, and willingness to pay — with method selection from
   [references/frameworks-pricing.md](references/frameworks-pricing.md).

5. **Review the portfolio context** when several bets compete for the same resources.
   Run [references/portfolio-review.md](references/portfolio-review.md); scoring grids
   (growth-share, GE nine-box) are in
   `../market-and-competitive-intelligence/references/frameworks-strategy.md`.

6. **Compare with equal rigor, then recommend.** Score options against the criteria,
   stress-test frontrunner *and* runner-up (pre-mortem and second-order thinking in
   [references/frameworks-decision.md](references/frameworks-decision.md)), state the
   trade-offs, what must be true, risks, kill conditions, and next actions — the
   recommendation contract in ../strategy-diagnosis-and-framing/SKILL.md. An option
   that wins because the alternative was never examined is a default, not a
   recommendation.

7. **Convert to execution hand-off.** Recommended moves, owners, and test designs
   become inputs to `operating-model-and-execution`; the stakeholder narrative becomes
   `executive-communication-and-alignment`.

## Quality bar

- [ ] Decision, decision-maker, and threshold are stated before options are generated
- [ ] Options differ in mechanism; "do nothing" is evaluated with equal rigor
- [ ] Criteria and weights derive from this decision, not a generic scorecard
- [ ] Base, downside, and upside are shown; the assumption moving each is named
- [ ] Every load-bearing assumption is registered with evidence, test, and kill condition
- [ ] Metrics are tied to the decision threshold; no false precision
- [ ] The runner-up survived the same stress test as the recommendation
- [ ] Pricing moves carry segment-level value logic and a test/rollback design
- [ ] Allocation recommendations name the trade-off they create elsewhere
- [ ] At least 2 risks, 2 kill conditions, and owned next actions accompany the recommendation

## Reference map

| Situation | Open |
|---|---|
| Option generation, criteria, recommendation logic | [references/strategic-options.md](references/strategic-options.md) |
| Business case: value/cost drivers, scenarios, ROI/NPV, sensitivity | [references/business-case-builder.md](references/business-case-builder.md) |
| Portfolio scoring and allocation moves | [references/portfolio-review.md](references/portfolio-review.md) |
| Pricing diagnosis, WTP, discount leakage, rollout tests | [references/pricing-strategy.md](references/pricing-strategy.md) |
| Decision frameworks: RAPID, decision matrix, pre-mortem, second-order thinking, inversion | [references/frameworks-decision.md](references/frameworks-decision.md) |
| Financial frameworks: profit tree, revenue tree, TAM/SAM/SOM, unit economics, waterfall | [references/frameworks-financial.md](references/frameworks-financial.md) |
| Pricing frameworks: value-based, cost-plus, competitive, dynamic, freemium | [references/frameworks-pricing.md](references/frameworks-pricing.md) |
| Depth modes, MECE/synthesis contract, assumption audit, evidence labels | [../strategy-diagnosis-and-framing/SKILL.md](../strategy-diagnosis-and-framing/SKILL.md) |
| Market size inputs, segment logic, competitor response, portfolio grids | [../market-and-competitive-intelligence/SKILL.md](../market-and-competitive-intelligence/SKILL.md) |

## Output format

Choice deliverables combine into one decision brief; playbooks supply their own exhibit
templates (options table, economics summary, portfolio matrix, pricing diagnosis):

```markdown
# Decision Brief — <decision>

## Recommendation
[Option chosen, threshold it clears, one sentence of rationale.]

## Decision
[What is decided, by whom, by when, and the constraint set.]

## Options considered
| Option | Upside | Trade-off | Economics (base) | What must be true |

## Economics summary
| Metric | Downside | Base | Upside |
|---|---|---|---|

## Assumptions that carry the case
| Assumption | Evidence | Confidence | Test | Kill condition |

## Risks / Kill conditions / Next actions
[Minimum 2 each, each action with owner and deadline — per the contract in
../strategy-diagnosis-and-framing/SKILL.md.]
```
