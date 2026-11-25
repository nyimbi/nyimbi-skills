---
name: product-strategy
description: >-
  Take a product or venture from an idea to a validated, positioned, launchable strategy:
  score the opportunity, design the business model, define the customer and JTBD, write the
  value proposition, position it, plan the 90-day go-to-market, prioritise the roadmap, design
  growth loops and monetization, and run the launch with behaviour signals and kill criteria.
  Use when the user says "validate this idea", "should I build this", "position this product",
  "business model", "value proposition", "go-to-market", "pricing and packaging", "growth
  loop", "launch plan", "product roadmap", "why is retention flat", or "turn this idea into a
  product strategy". Do not use for corporate strategy or a business unit decision (see
  strategy-core), for a full investor business plan (see business-plan-authoring), for market
  sizing alone (see market-and-competitive-intelligence), or for a single pricing model (see
  strategic-choices-and-economics).
---

# Product Strategy

The startup and product layer of the strategy core. It answers three questions in order:
is this worth building, what exactly is it, and how does it reach and keep customers.

> **Pipeline position.** Use after `strategy-core` has framed the decision, or directly when
> the ask is a product or venture. Route market sizing to
> `market-and-competitive-intelligence`, financial models to
> `strategic-choices-and-economics`, execution design to `operating-model-and-execution`, and
> the investor plan to `business-plan-authoring`.

## Intake

Establish, inferring where possible:

```yaml
stage: idea | validated idea | live product | growing product
product: what it is, in one sentence
customer: who has the problem
problem: what they do today instead
business_model: how it might make money
market: geography, segment, category
constraint: team size, capital, runway, regulatory exposure
goal: validate | position | launch | grow | raise
```

State the stage and the goal in one line. A live product with flat retention needs a
different engagement from a pre-idea. Where the intake leaves a field blank, use the
personal defaults in [`../strategy-core/references/personal-context.md`](../strategy-core/references/personal-context.md)
and say that you did.

## 1. Opportunity thesis

Do not start with features. Start with a change in the world that makes a new behaviour
possible or necessary.

- **Signal harvest.** Three independent sources: quantitative (search, app reviews, marketplace
  listings, support tickets), qualitative (interviews, community threads), and a structural
  shift (platform rule, payment rail, regulation, model capability, cost curve).
- **Thesis.** "Because <shift>, <customer> can now <job> in a way that was previously
  <expensive/impossible/unsafe>."
- **Score:** desirability, feasibility, timing, strategic fit, each 1–5. A high desirability
  score with low feasibility is a research project, not a product.
- **Brief:** user tension, evidence, why now, first wedge, unknowns.

Output `01-opportunity.md`.

## 2. Validation

Score the idea before building. Ten dimensions, 1–5, with a weight you state up front:

| Dimension | The question |
|---|---|
| Problem severity | Does the customer lose money, time, status or sleep? |
| Frequency | Does the job recur often enough to form a habit or a budget line? |
| Willingness to pay | Is there evidence of spend today, not just interest? |
| Market size | Can the wedge reach a market that matters? Cross-check top-down and bottom-up. |
| Competition | What do they use now, and why is it inadequate? |
| Moat | What compounds: data, workflow, distribution, switching cost, brand? |
| Founder/market fit | Why this team, why now? |
| Distribution | Is there a channel that reaches the customer without paid acquisition? |
| Execution feasibility | Can a small team ship the first version in 90 days? |
| Regulatory/trust | What licence, consent, audit or liability sits in the path? |

Weight the dimensions for the business model. A consumer social product weights frequency and
distribution; a payments product weights trust and regulation.

**Decision:** go, hold with a named test, or kill. A hold without a test and a date is a kill
that has not been admitted.

Output `02-validation.md` with the score table and the evidence under each score.

## 3. Business model

Complete the nine blocks, then test the economics:

1. Customer segments.
2. Value proposition.
3. Channels.
4. Customer relationships.
5. Revenue streams.
6. Key resources.
7. Key activities.
8. Key partners.
9. Cost structure.

Then run `strategic-choices-and-economics/scripts/unit_economics.py` on CAC, ARPU, gross
margin, churn and payback. A model without CAC payback is a story.

Output `03-business-model.md`.

## 4. Customer and JTBD

Segments are needs-based, not demographic. For each priority segment:

- **Job.** What progress are they trying to make, in their words?
- **Current alternative.** What do they do today, including "nothing" and a spreadsheet?
- **Pains and gains.** What is expensive, slow, risky, embarrassing or unreliable?
- **Buying process.** Who feels the pain, who approves the spend, who blocks it?
- **Trigger.** What event makes them look for a solution this week?
- **Proof.** What would convince them, and what would make them distrust you?

Write one page per priority segment. Do not average two segments into a persona.

Output `04-customer-jtbd.md`.

## 5. Value proposition and positioning

**Value proposition.** Three to five promise statements. Each has an outcome, a proof, and a
named customer. Test the promise against the current alternative, not against a blank page.

**Positioning (April Dunford):**

| Component | Question |
|---|---|
| Competitive alternatives | What would they use if you did not exist? |
| Unique attributes | What do you have that the alternatives lack? |
| Value | What does that attribute let the customer do? |
| Who cares | Which segment values that most? |
| Market category | What context makes the value obvious? |

**Switch test:** show the positioning statement and the current alternative to five target
users. If they cannot say what changed and why it matters, the positioning is not done.

Output `05-positioning.md` with the statement, messaging hierarchy and proof points.

## 6. Go-to-market

A 90-day plan, not a launch day.

- **Segment and wedge.** One segment, one problem, one promise.
- **Channel.** Choose the channel that reaches the segment without a sales team, or state the
  sales motion and its cost.
- **Funnel.** Reach → interest → activation → retention → referral, with a number and a source
  for each assumption.
- **Budget.** Cash and time, split by channel; state the cost per activation.
- **Milestones.** Week 2, 4, 8, 12: what is learned, not only what is shipped.
- **Kill criteria.** The activation or retention threshold below which the channel or the
  wedge is stopped.

Output `06-gtm.md`.

## 7. Roadmap and prioritisation

- **Now / next / later.** Now is the 90-day wedge; next is the retention or expansion move;
  later is the platform bet.
- **OKRs.** One objective per horizon, two to four key results, each with a baseline and a
  target.
- **RICE.** Run `operating-model-and-execution/scripts/rice_prioritizer.py` on competing
  features. Print the kill list.
- **Dependencies.** Name the platform, partner or regulatory approval that can block each
  item.

Output `07-roadmap.md`.

## 8. Growth loops and monetization

**Growth loop.** Trigger → action → reward → investment. A loop must have a measurable
conversion at each arrow and a reason the output feeds the next input. A funnel is not a loop.

Pick one core loop and one accelerant. State the loop's cycle time and its leakage point.

**Monetization.** Choose the value metric (seat, usage, transaction, outcome, storage, access),
the packaging, and the price ladder. Test willingness to pay with
`strategic-choices-and-economics/scripts/pricing_calculator.py`.

Guardrails: no pay-to-win, no dark patterns, no pricing that punishes the behaviour the loop
depends on.

Output `08-growth-monetization.md`.

## 9. Launch and learning

- **Experiment ladder.** Fake door or landing page → concierge → closed beta → open beta →
  public. Each stage has an entry criterion and an exit criterion.
- **Instrumentation.** The event that proves activation, the event that predicts retention, and
  the event that reveals friction.
- **Behaviour signals.** Pair every quantitative cut with a qualitative source. Write belief
  statements: tension + evidence + implication.
- **Launch cadence.** Daily signal review during the first two weeks, weekly after; a decision
  log for pivots.
- **Strategy to ops.** Convert the chosen moves into issues with an owner, a dependency and a
  due date.

Output `09-launch.md` and `10-ops.md`.

## Artifacts

```text
strategy/<slug>/product/
  01-opportunity.md
  02-validation.md
  03-business-model.md
  04-customer-jtbd.md
  05-positioning.md
  06-gtm.md
  07-roadmap.md
  08-growth-monetization.md
  09-launch.md
  10-ops.md
```

Use the `strategy-core` layout when the product work is one workstream of a larger strategy.

## Quality gate

- [ ] The opportunity thesis names a shift, a customer and a job.
- [ ] Every validation score cites evidence; the decision is go, hold-with-test, or kill.
- [ ] The business model has a CAC payback and a gross margin.
- [ ] The priority segment is needs-based; the current alternative is named.
- [ ] The positioning passes the switch test with target users.
- [ ] The GTM plan has one segment, one channel, one promise, and a kill criterion.
- [ ] The roadmap has owners, dependencies and a kill list.
- [ ] The core growth loop has cycle time and measured conversions.
- [ ] The monetization metric rewards the behaviour the product wants.
- [ ] The launch has an experiment ladder and instrumentation.
- [ ] Every next action has an owner and a date.

## Reference map

| File | Contents |
|---|---|
| `references/validation.md` | 10-dimension scoring, weights, evidence thresholds, go/hold/kill |
| `references/positioning.md` | JTBD persona, Dunford canvas, messaging hierarchy, switch test |
| `references/growth-and-monetization.md` | GTM, loops, pricing, packaging, RICE and OKRs |
| `references/launch-and-ops.md` | Experiment ladder, behaviour signals, instrumentation, strategy-to-ops |
| `references/ATTRIBUTION.md` | StratArts and Product Strategist sources and licences |
