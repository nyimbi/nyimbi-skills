---
name: strategy-diagnosis-and-framing
description: >-
  Diagnose what is true and why: build a defensible fact base, structure ambiguous
  business problems, and frame testable hypotheses before anyone picks a strategy.
  This skill owns the method layer for the whole strategy group — the three depth
  modes (Quick Structure, Full Case, Client Deliverable) every sibling strategy skill
  defers to, plus the clarify → structure → hypothesize → analyze → synthesize
  workflow, MECE issue trees, evidence labeling (fact, inference, assumption,
  estimate), Pyramid synthesis, devil's-advocate challenge, framework selection, and
  the delivery quality checklist. It also runs three deliverables: situation
  assessment, growth-barrier diagnosis, and assumption audit. Use when the user says
  "help me think through X", "structure this problem", "build an issue tree",
  "where are we really", "why are we not growing", "what has to be true", "audit these
  assumptions", "what are the key considerations", or asks for a recommendation, a
  strategy memo, or a board deck outline. Do not use for sizing markets, segments, or
  competitor moves (market-and-competitive-intelligence), for choosing or valuing
  options (strategic-choices-and-economics), or for org design, roadmaps, and delivery
  (operating-model-and-execution).
license: MIT
---

# Strategy Diagnosis and Framing

This skill answers two questions: **what is true, and why.** Everything else in the
strategy group builds on that — market skills read the external environment, choice
skills compare options, execution skills design the change. Nothing here picks a
strategy; the fact base, root cause, and hypothesis discipline come first.

It also owns the **depth mode** contract for the bundle. The three modes defined in
step 1 are the shared vocabulary for every strategy skill: siblings link back to this
file rather than restating them. When a sibling skill says "run at Full Case depth",
this is the definition.

## When to use

- Ambiguous, high-stakes business questions: "help me think through X", "structure this problem", "what are the key considerations?"
- Establishing a current-state baseline: business reviews, turnaround diagnosis, market-position checks, board preparation
- Growth is underperforming and leadership is arguing symptoms: "why are we not growing?", funnel, retention, sales-productivity stalls
- Pressure-testing a plan before commitment: "what has to be true?", assumption audits, investment cases, board prep
- Requests for a structured recommendation, issue tree, hypothesis tree, or decision memo
- Deliverables: strategy memo, board deck outline, executive brief with risks and kill conditions
- Choosing which consulting framework fits a problem — and when to use none

**Do not use for** — `market-and-competitive-intelligence` when the question is
external: market size, segments, white space, competitor moves, ad/messaging
intelligence; `strategic-choices-and-economics` when the question is which option to
take and what it is worth: option comparison, business cases, pricing, portfolio
allocation; `operating-model-and-execution` when the question is how the organization
will change: org design, initiative sequencing, transformation roadmaps. Once a fact
base exists and only the stakeholder narrative or decision routing is missing, that is
`executive-communication-and-alignment`.

## Workflow

1. **Detect the depth mode.** Full Case and Client Deliverable run steps 2–8; Quick
   Structure runs steps 2–3 only and returns structured thinking immediately.

   ### Depth modes (bundle-wide definition)

   | Mode | Trigger | Output | Gates applied |
   |---|---|---|---|
   | **Quick Structure** (default) | "help me think through", "what are the considerations", "I'm trying to figure out", or a vague prompt with missing context | Issue tree or framework, 1–2 paragraphs, no mandatory diagram | None — no context check, no output contract |
   | **Full Case** | "should we [decision]", "why is [metric] doing X", "[option A] vs [option B]", "is this worth it" | Full workflow: clarify → structure → hypothesize → analyze → synthesize | Context check, output contract, quality checklist |
   | **Client Deliverable** | "draft a memo", "build a deck", "write up", "put together a [board paper / IC memo / executive brief]" | Polished document structure: themes, diagrams, evidence coding | Everything, including diagram pipeline and devil's advocate |

   Rules: **if in doubt, default to Quick Structure** — useful structure now beats
   gating on missing information. When two modes plausibly fit, escalate one level only
   if the user has named both a specific decision *and* a stakeholder audience;
   otherwise stay light.

2. **Clarify before analysis** (Full Case and Client Deliverable). Establish
   **decision** (what is decided, by whom), **success metric**, **constraints** (time,
   budget, capability, politics), and **scope** (in, out). Context check:
   - [ ] Decision-maker identified (or assumed)
   - [ ] Success metric defined (or assumed)
   - [ ] Scope boundaries set (or assumed)

   If any are missing, state **provisional assumptions [A]** and proceed with the full
   analysis in the same response. Do not stop to ask and wait; never return questions
   without analysis. Example for a vague "we need to grow faster":
   > *Provisional assumptions [A]: B2B SaaS, $10–50M ARR, primarily US, growth slowed
   > from 40%+ to ≤20%. If wrong, tell me what's different and I'll restructure.*

3. **Structure the problem (MECE).** Decompose into an issue tree: problem statement →
   MECE branches → sub-branches → data needs at leaves. Every level must be mutually
   exclusive (no overlap) and collectively exhaustive (no gaps). Construction workflow,
   good-vs-bad examples, and failure modes:
   [frameworks-problem-solving.md](references/frameworks-problem-solving.md) and
   [issue-tree-good-vs-bad.md](references/issue-tree-good-vs-bad.md). Diagram templates:
   [diagram-templates.md](references/diagram-templates.md).

   ### Framework selection

   | Problem type | Primary framework | Supporting |
   |---|---|---|
   | Market entry | Five Forces + TAM/SAM/SOM | Ansoff, competitive positioning |
   | Growth strategy | Ansoff + Revenue tree | 3 Horizons, Blue Ocean |
   | Pricing | Value-based pricing + Profit tree | Competitive analysis, willingness-to-pay |
   | Cost reduction | Profit tree + Value chain | Zero-based budgeting, 80/20 |
   | M&A / due diligence | Commercial DD checklist | Five Forces, 7S, VRIO |
   | Org effectiveness | 7S + Influence Model | ADKAR, Kotter |
   | Decision-making | RAPID + Decision matrix | Pre-mortem, second-order thinking |
   | Communication | Pyramid Principle + SCQA | Situation-Complication-Resolution |
   | Innovation | Blue Ocean + JTBD | Wardley Mapping, 3 Horizons |
   | Portfolio | Growth-Share Matrix / Nine-Box | Revenue mix, growth-profitability |

   When NOT to use a framework: **Five Forces** unless industry structure is the actual
   question; **revenue/profit tree** unless the dependent variable is quantified;
   **7S** only for organizational root cause; **Growth-Share** only for multi-product
   portfolios; **SWOT** almost never as a primary tool — it is a brainstorm format, not
   analysis; **Blue Ocean** only when creating new market space is a real option. If you
   reach for a framework before understanding the problem, stop — the problem dictates
   the framework. One-line index of every framework:
   [frameworks-index.md](references/frameworks-index.md).

4. **Hypothesize.** For each branch state the **hypothesis** (what must be true for
   this to matter), the **kill test** (the single data point that would disprove it),
   and its **priority** (the 80/20 branches that drive most of the answer). Lead with
   the hypothesis that, if true, most changes the recommendation.

5. **Analyze with evidence.** For each priority hypothesis separate **facts**
   (observed, sourced, verified), **inferences** (derived — labeled), and
   **assumptions** (judgment gaps, confidence 0–100%). Never present an assumption as a
   fact. Never cite a number without unit, time period, and source. Full labeling rules:
   [evidence-standards.md](references/evidence-standards.md).

6. **Synthesize answer-first** (Pyramid Principle). Lead with the bottom line, then at
   most three load-bearing arguments, then risks, kill conditions, next actions, and
   open questions — the full contract is in **Output format** below. A response that
   omits risks, kill conditions, or next actions is incomplete.

7. **Challenge your recommendation** (devil's advocate, mandatory for Full Case and
   Client Deliverable). Argue against your own answer: strongest reason it is wrong;
   the assumption whose failure reverses it; what a smart opponent would say. State the
   counter-argument explicitly, then either defend the recommendation against it or
   revise. If the rejected option has not survived the same stress test as the winner,
   the winner is a default, not a recommendation.

8. **Route to the deliverable.** Each playbook carries its own workflow and document
   template; all three inherit this skill's mode, MECE, and evidence discipline.

   | Situation | Playbook |
   |---|---|
   | Where are we really? Current-state fact base, baseline, board prep | [situation-assessment.md](references/situation-assessment.md) |
   | Growth is lagging; find the binding constraint, not the symptom | [growth-barriers.md](references/growth-barriers.md) |
   | What has to be true? Fragile plans, investment or board pressure tests | [assumption-audit.md](references/assumption-audit.md) |

## Quality bar

Verify before delivering:

- [ ] Depth mode was detected explicitly and the right gates were applied
- [ ] MECE check: every level of the issue tree is mutually exclusive and collectively exhaustive
- [ ] Evidence labeled: every claim tagged `[F]`, `[I]`, `[A]`, or `[E]`
- [ ] Numbers sourced: every figure has value, unit, time period, and source
- [ ] "So what" stated: every finding has an explicit implication for the decision
- [ ] Recommendation is specific: names who, what, by when
- [ ] At least 2 risks with mitigation paths
- [ ] At least 2 kill conditions — specific data points that would reverse the recommendation
- [ ] Next actions are owned: each has an owner and a deadline
- [ ] Devil's advocate applied: the strongest counter-argument is stated on the page
- [ ] Diagram delivered: self-contained SVG inlined, or a structured text description if no renderer is reachable (templates in [diagram-templates.md](references/diagram-templates.md))

### Epistemic rules

- Label every claim: fact (sourced), inference (derived), or assumption (judgment)
- State confidence as a probability — "70%", not "likely"
- Prefer disconfirming evidence over confirming anecdotes
- Pre-commit to what would change the recommendation
- If you don't know, say so — do not fill gaps with plausible-sounding fiction

### Failure modes

- **MECE theater** — exhaustive trees with no decision path
- **Framework salad** — five frameworks when one suffices; six frameworks × three models = eighteen analyses that share the same blind spot
- **Over-structuring** — not every yes/no question needs a three-level issue tree
- **Generic Porter analysis** — Five Forces as a reflex instead of an answer to an industry-structure question
- **Made-up market sizes** — never fabricate TAM; state what data would be needed
- **Framework confusion** — naming a framework is not analysis; applying it with specific data is
- **Unsupported numbers** — figures without source, period, or unit
- **Generic recommendations** — "improve customer experience" (how, by whom, by when?)
- **Skipped "so what"** — data without implications is incomplete
- **Winning by default** — the rejected option gets no scrutiny while the alternative wins by not being examined
- **Market description as analysis** — cataloguing an industry is research; analysis names the asset, price, cash flow, and why the customer needs it
- **Consensus without independence** — several models agreeing on the same incomplete context is not validation
- **Ignoring politics and implementation** — the right answer that cannot be implemented is the wrong answer
- **Unequal evidence weighting** — a CEO quote and a peer-reviewed study are not the same
- **Sector recommendations instead of deals** — "enter digital infrastructure" is not actionable; name the asset, the price, and the return

## Reference map

| Situation | Open |
|---|---|
| Situation assessment — fact base, baseline, current-state read | [references/situation-assessment.md](references/situation-assessment.md) |
| Growth-barrier diagnosis — driver tree, binding constraint | [references/growth-barriers.md](references/growth-barriers.md) |
| Assumption audit — load-bearing beliefs, test plan | [references/assumption-audit.md](references/assumption-audit.md) |
| MECE, issue trees, hypothesis trees, 7-step, Pyramid, SCQA | [references/frameworks-problem-solving.md](references/frameworks-problem-solving.md) |
| One-line framework index and where each group's practitioner file lives | [references/frameworks-index.md](references/frameworks-index.md) |
| Evidence rules: `[F]/[I]/[A]/[E]`, sourcing, confidence, triangulation | [references/evidence-standards.md](references/evidence-standards.md) |
| SVG templates: issue tree, 2×2, Five Forces, profit tree, waterfall | [references/diagram-templates.md](references/diagram-templates.md) |
| Worked example — Quick Structure end to end | [references/end-to-end-quick-structure.md](references/end-to-end-quick-structure.md) |
| Worked example — Full Case end to end | [references/end-to-end-full-case.md](references/end-to-end-full-case.md) |
| Worked example — issue tree good vs bad | [references/issue-tree-good-vs-bad.md](references/issue-tree-good-vs-bad.md) |
| Worked example — recommendation good vs bad | [references/recommendation-good-vs-bad.md](references/recommendation-good-vs-bad.md) |
| Strategy frameworks (Five Forces, Value Chain, 7S, VRIO, Ansoff, BCG, Blue Ocean, Wardley, scenarios) | [../market-and-competitive-intelligence/references/frameworks-strategy.md](../market-and-competitive-intelligence/references/frameworks-strategy.md) |
| Decision frameworks (RAPID, decision matrix, pre-mortem, second-order, inversion) | [../strategic-choices-and-economics/references/frameworks-decision.md](../strategic-choices-and-economics/references/frameworks-decision.md) |
| Financial/sizing frameworks (profit tree, revenue tree, TAM/SAM/SOM, unit economics, waterfall) | [../strategic-choices-and-economics/references/frameworks-financial.md](../strategic-choices-and-economics/references/frameworks-financial.md) |

## Output format

Quick Structure returns the issue tree or framework plus 1–2 paragraphs. Full Case and
Client Deliverable must include all six sections:

```markdown
BOTTOM LINE: [Answer/recommendation — one sentence]

SUPPORTING ARGUMENTS (max 3 — the load-bearing reasons)
1. [Argument] — [F/I/A/E] [evidence with source]
2. [Argument] — [F/I/A/E] [evidence with source]
3. [Argument] — [F/I/A/E] [evidence with source]

RISKS (minimum 2)
1. [Risk] — likelihood: [H/M/L], impact: [H/M/L], mitigation: [specific action]

KILL CONDITIONS (minimum 2 — what would reverse this)
1. [Data point or event] — if observed, [recommendation flips to X]

NEXT ACTIONS (minimum 2)
1. [Action] — owner: [who], deadline: [when], success metric: [how to verify]

OPEN QUESTIONS: [What we don't know and how we'll find out]
```

Evidence labels: `[F]` fact (observed, sourced) · `[I]` inference (derived from facts) ·
`[A]` assumption (judgment, state confidence) · `[E]` estimate (calculated from
assumptions + data, e.g. TAM = users × ARPU).

Client Deliverable adds the document shell around this contract — title, executive
summary, sectioned exhibits, and diagrams inlined as SVG — and every deliverable
playbook in the reference map supplies its own document template on top of it. For a
recommendation, also state the counter-argument you tested; see
[recommendation-good-vs-bad.md](references/recommendation-good-vs-bad.md).
