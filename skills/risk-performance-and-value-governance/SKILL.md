---
name: risk-performance-and-value-governance
description: >-
  Know whether execution is working and what could break it: design the KPI system
  (outcome, driver, and leading indicators with owners, thresholds, and review
  cadence), define the value ledger that turns promised benefits into tracked,
  proof-backed value, build a strategic risk register with likelihood, impact,
  mitigations, triggers, owners, and residual risk, and war-game the plan against
  competitor moves, market shifts, regulation, customer response, and execution
  failure. Use when the user asks "what should we measure?", "kill these vanity
  metrics", "build a KPI tree", "how do we make benefits stick?", "track the
  synergies", "what could go wrong?", "build a risk register", "war-game this
  strategy", or "what could break this plan?" — or for board risk reviews,
  transformation governance, post-launch benefits tracking, launch planning, and
  operating reviews. Do not use for designing decision rights and the governance forum
  itself (operating-model-and-execution), for market sizing and competitor
  intelligence (market-and-competitive-intelligence), or for the memo and alignment
  that win approval (executive-communication-and-alignment).
license: MIT
---

# Risk, Performance, and Value Governance

This skill owns the **instruments**: how you will know the strategy is working, what
value must show up, and what could break it before it does. It runs after a direction
is chosen and before or during delivery — the design of the machine is
[`operating-model-and-execution`](../operating-model-and-execution/SKILL.md), the
decision it supports is
[`executive-communication-and-alignment`](../executive-communication-and-alignment/SKILL.md).

Two pairs are frequently confused, and each concept is defined once here:

- **Value ledger vs KPI system** — the ledger says *what benefit counts and what
  proof* (baseline, target, owner, proof standard); the KPI system says *how it is
  watched day to day* (driver tree, leading indicators, thresholds, cadence). Ledgers
  feed thresholds; nothing is defined twice.
- **War game vs risk register** — the war game is the *generator* (scenarios,
  vulnerabilities, early-warning signals, response playbook); the register is the
  *system of record* (scored, owned, residual risk, go/no-go). Every vulnerability
  becomes a register row.

Run at the depth mode defined in
[`../strategy-diagnosis-and-framing/SKILL.md`](../strategy-diagnosis-and-framing/SKILL.md).

## When to use

- Metrics are noisy, backward-looking, too numerous, or disconnected from decisions: "what should we measure?"
- Designing or cleaning a KPI/OKR set, dashboards, operating reviews, performance management
- A strategy, transformation, acquisition, or initiative has approved benefits that must be tracked and captured: "how do we make benefits stick?"
- Synergy capture, post-launch benefits tracking, value-steam governance after commitment
- Board or investment-committee risk review: "what could go wrong?" before approval
- Launch, program, or transformation governance needing triggers, owners, and contingency moves
- Pressure-testing a plan before it meets reality: "war-game this strategy", "what could break it?"

**Do not use for** — `operating-model-and-execution` when the question is how the
organization will work: capabilities, decision rights, initiative sequencing, and the
governance *forum* itself (this skill supplies that forum's agenda);
`market-and-competitive-intelligence` when the question is external evidence — market
size, segments, competitor moves; war-gaming *simulates* competitor response but does
not *research* it, and the scenario-construction method lives there;
`strategic-choices-and-economics` when the question is pre-approval value — business
case, NPV, option comparison (this ledger starts at commitment);
`executive-communication-and-alignment` when the risks are known and the job is
writing the memo or winning the room.

## Workflow

1. **Clarify what is being governed and what decision it feeds.** Establish the
   initiative or strategy under review, the **decisions** the instruments must support
   (continue / re-scope / stop / escalate), the **success metric**, the horizon, and
   **scope**. Context check: decision-maker, success metric, and boundaries identified
   or explicitly assumed; if missing, state **provisional assumptions [A]** and
   proceed. Output: governance mandate plus assumption list.

2. **Define the value ledger — what counts as value.** Set the value ambition and
   timing, then split benefits into categories (revenue, cost, capital, risk avoided,
   capability) and, within each, **one-time vs recurring**. For every benefit: a
   **baseline** (measured, not remembered), a **target**, a **timing** profile, a
   single **owner**, and a **proof standard** — the evidence that will be accepted as
   captured (finance-verified P&L line, audited cost base, signed contract). Size the
   math with profit/unit trees and bridges where a benefit is calculated:
   [`../strategic-choices-and-economics/references/frameworks-financial.md`](../strategic-choices-and-economics/references/frameworks-financial.md).
   Output: value ledger.

3. **Build the KPI architecture the ledger is watched through.** Work backwards from
   the **decisions** leaders must make, then build the **value driver tree** connecting
   those decisions to outcomes. Separate **outcome** metrics (lagging, what you are
   accountable for), **driver** metrics (the levers), and **activity** metrics (output
   only — usually the first to cut). Remove vanity metrics: anything no decision would
   change on. For each survivor: the decision it supports, one **owner**, a
   **threshold** (drawn from the ledger baseline/target where it is a value metric),
   and a **leading** indicator where the outcome lags. End with the review cadence and
   escalation triggers. **Deduplication:** the ledger defined *what* the benefit is and
   what proof closes it; this step only defines how it is monitored — a metric appears
   in one definition and one watchlist, never two competing definitions.

4. **War-game the plan before reality does.** State the strategy under test, then the
   scenario dimensions: competitor response, customer reaction, market shift,
   regulatory change, operational failure, financial/capital constraint. Build at
   least a **base**, an **adverse**, and an **aggressive** scenario; assess each
   against the economics and the strategic logic, not just the narrative. Derive
   **early-warning signals** that are observable (a price move, a churn cohort, a
   regulatory filing) and pre-commit **defensive and offensive responses** with owners.
   Scenario construction, driving-force ranking, signposts, and strategy-scenario
   scoring are in
   [`../market-and-competitive-intelligence/references/frameworks-strategy.md`](../market-and-competitive-intelligence/references/frameworks-strategy.md)
   (Scenario Planning) — linked, not copied. Output: scenarios, vulnerabilities, and a
   response playbook.

5. **Convert findings into the strategic risk register.** Identify risks across
   categories — market, customer, competitor, financial, operational, regulatory,
   organizational — including every war-game vulnerability from step 4. Score
   **likelihood × impact**, then define for each: mitigation, an observable
   **trigger**, an **owner**, and the **residual risk** after mitigation. Only risks
   that could change the decision, economics, timing, or feasibility belong here.
   Close with a recommendation: **go, no-go, redesign, or gated approval**, plus the
   assumptions that most need testing. **Deduplication:** scenarios and signals are
   generated in step 4; scoring, ownership, residual risk, and the go/no-go live only
   here. Output: register plus contingency moves.

6. **Wire the governance rhythm.** Map each instrument to a meeting: cadence,
   participants, what is reviewed, what gets decided, and what triggers escalation.
   The forum's structure and decision rights belong to
   [`../operating-model-and-execution/SKILL.md`](../operating-model-and-execution/SKILL.md);
   what arrives on the agenda is owned here. Assign a named owner for every ledger
   line, KPI threshold, and register row — value has owners, not committees.

7. **Challenge the whole set (devil's advocate, mandatory).** Argue against it: which
   benefit is least likely to land and why; which KPI would look healthy while value
   erodes; the risk everyone scores Low that would end the program; the assumption
   that reverses the go decision. Pre-mortem, second-order thinking, and inversion
   are the fast tests:
   [`../strategic-choices-and-economics/references/frameworks-decision.md`](../strategic-choices-and-economics/references/frameworks-decision.md).
   State the strongest counter-argument on the page and update the register if it
   holds.

8. **Synthesize answer-first, then verify.** Lead with the bottom line — is this
   on track, what must change, what decision is required — then at most three
   load-bearing arguments with evidence labeled `[F]/[I]/[A]/[E]`, then the top risks
   with mitigations, kill conditions (the data points that reverse the
   recommendation), and next actions with owners and dates; full contract in
   [`../strategy-diagnosis-and-framing/SKILL.md`](../strategy-diagnosis-and-framing/SKILL.md).
   Run the quality bar below, then deliver the templates in Output format.

## Quality bar

Verify before delivering:

- [ ] Every KPI names the decision it supports; anything no decision would change on is cut
- [ ] Outcome, driver, and activity metrics are distinguished; at least one leading indicator per lagging outcome
- [ ] Every benefit has a measured baseline, a target, a timing profile, a single owner, and a stated proof standard
- [ ] One-time and recurring benefits are separated; no benefit appears with two competing definitions
- [ ] Every threshold traces to a ledger baseline/target or a stated operating tolerance
- [ ] War-game includes at least one painful scenario, and every early-warning signal is observable by a named owner
- [ ] Every risk has likelihood, impact, mitigation, trigger, owner, and residual risk — no generic "market risk" rows
- [ ] Risks that change the decision lead to an explicit go / no-go / redesign / gated-approval call
- [ ] Governance names cadence, escalation trigger, and participant per instrument
- [ ] Devil's advocate stated: the strongest reason these instruments are wrong, and the assumption that reverses the call
- [ ] Evidence labeled `[F]/[I]/[A]/[E]`; every number carries unit, period, and source

## Reference map

This skill ships no framework file of its own — scenario construction, financial
proof math, and challenge methods are owned by sibling skills and linked here rather
than copied.

| Situation | Open |
|---|---|
| Scenario construction, driving forces, signposts, strategy-vs-scenario stress test | [../market-and-competitive-intelligence/references/frameworks-strategy.md](../market-and-competitive-intelligence/references/frameworks-strategy.md) |
| Benefit math: profit tree, driver/KPI tree, unit economics, waterfall bridges | [../strategic-choices-and-economics/references/frameworks-financial.md](../strategic-choices-and-economics/references/frameworks-financial.md) |
| Challenging the register: pre-mortem, second-order thinking, inversion | [../strategic-choices-and-economics/references/frameworks-decision.md](../strategic-choices-and-economics/references/frameworks-decision.md) |
| Evidence rules for every claim: `[F]/[I]/[A]/[E]`, sourcing, confidence | [../strategy-diagnosis-and-framing/references/evidence-standards.md](../strategy-diagnosis-and-framing/references/evidence-standards.md) |
| Depth modes and the answer-first synthesis contract | [../strategy-diagnosis-and-framing/SKILL.md](../strategy-diagnosis-and-framing/SKILL.md) |
| Diagrams: risk matrix, profit tree, driver tree, waterfall | [../strategy-diagnosis-and-framing/references/diagram-templates.md](../strategy-diagnosis-and-framing/references/diagram-templates.md) |
| Governance forum structure, decision rights, initiative sequencing | [../operating-model-and-execution/SKILL.md](../operating-model-and-execution/SKILL.md) |

## Output format

Deliver the templates that match the ask; a full governance pack runs value ledger →
KPI architecture → risk register → war game in that order, prefixed with the
answer-first synthesis from step 8.

```markdown
# KPI Architecture

## Strategic Objective
[What the KPI system must manage, and the decisions it feeds.]

## Driver Tree
[Outcome → driver → activity; how each level connects to value.]

## KPI System
| KPI | Type (outcome / driver / activity) | Decision It Supports | Owner | Threshold | Cadence |
|---|---|---|---|---|---|

## Metrics To Remove
| Metric | Why It Fails (no decision, vanity, duplicate) |
|---|---|

## Review Cadence
[Meeting rhythm, escalation triggers, and owners.]
```

```markdown
# Value Realization Plan

## Value Ambition
[Target value, timing, and category split.]

## Value Ledger
| Benefit | Type (one-time / recurring) | Baseline | Target | Timing | Owner | Proof Standard |
|---|---|---|---|---|---|---|

## Governance
| Cadence | Participants | Decisions |
|---|---|---|

## Risks To Capture
[What could prevent value from being realized, with triggers.]
```

```markdown
# Strategic Risk Register

## Strategy Under Review
[Brief summary and the decision it feeds.]

## Risk Register
| Risk | Category | Likelihood | Impact | Mitigation | Residual | Owner | Trigger |
|---|---|---|---|---|---|---|---|

## Highest-Risk Assumptions
[Assumptions that need testing, with the test.]

## Recommendation
[Go / no-go / redesign / gated approval, with the gate conditions.]
```

```markdown
# Strategy War Game

## Strategy Under Test
[Summary and what would falsify its logic.]

## Scenarios
| Scenario | Trigger | Likelihood | Impact on Economics | Severity |
|---|---|---|---|---|

## Vulnerabilities
| Weak Point | Why It Matters | Register Ref | Mitigation |
|---|---|---|---|

## Response Playbook
| Signal | Response | Owner |
|---|---|---|
```
