---
name: strategy-core
description: >-
  Run a strategy engagement end to end: frame the decision, choose the depth, route to
  diagnosis, market, economics, operating model, risk, communication, product or business
  plan, and hold the evidence and calculation gates. Use when the user says "help me decide",
  "build a strategy", "review this strategy", "size this market", "make a plan", "100-day
  plan", "prepare a negotiation", "fundraise", "should we enter / price / build / buy", or
  brings a broad business question rather than a single named framework. Personalized for a
  small, capital-constrained software team: decision memo first, three distinct options,
  reproducible numbers, kill conditions, local files. Do not use for explaining one framework
  (open the owning skill), for writing a full investor business plan (see
  business-plan-authoring), or for product/startup validation from an idea (see
  product-strategy).
---

# Strategy Core

The operating system for strategy work on this machine. It decides what kind of engagement
this is, how deep to go, which specialist skill owns each step, and whether the answer is
earned or merely well phrased.

The specialist skills still do the craft. This skill keeps the engagement honest.

## Personal context

- Principal: Nyimbi Odero, software engineer, Nairobi.
- Domains: payment rails, identity systems, local-first AI and developer tooling.
- Team: assume one to five people unless the user says otherwise. No staff functions.
- Capital: constrained. Prefer reversible pilots, capital-light moves and build-versus-buy
  before big commitments.
- Evidence: primary sources, dated numbers, reproducible models. No invented market data.
- Output: a decision memo first. A deck only when an external audience needs one.
- Default horizon: 100 days for execution, 18 months for strategy.

Edit `references/personal-context.md` when these defaults change. Do not put sensitive
personal or commercial data in that file.

## House rules

1. **One decision question.** If the ask contains three questions, split it or say which one
   is being answered.
2. **Three genuinely distinct options.** Variations on one idea are one option.
3. **Evidence labels.** Mark each claim `[F]` fact, `[I]` inference, `[A]` assumption, `[E]`
   estimate. A recommendation built on `[A]` is labelled as such.
4. **Reproducible numbers.** A model is a JSON config and a script output, not a paragraph.
   State units, period, currency and discount rate.
5. **Kill conditions.** Every recommendation names what would make it wrong and the
   threshold at which it should be stopped.
6. **Pre-mortem before approval.** Name the three most likely failure modes and the cheapest
   test for each.
7. **Memo before deck.** Write the one-page decision memo first. If it cannot fit on one
   page, the thinking is not finished.
8. **Owner and date.** Every next action has a named owner and a date. "The team" is not an
   owner.

## Engagement modes

| Mode | The ask | Default depth | Primary output |
|---|---|---|---|
| Decide | Choose between options, approve a case | Standard | Decision memo + model |
| Diagnose | Why is growth/performance stuck? | Standard | Issue tree + fact base + findings |
| Design | Design an operating model, org or service | Standard | Design + options + roadmap |
| Plan | Turn a choice into a 100-day or 18-month plan | Standard | Plan + OKRs + risk register |
| Review | Challenge a strategy, case or plan | Quick | Red-team memo + fixes |
| Present | Turn an approved argument into a board, IC or investor deck | Standard | Ghost deck, then `.pptx` or browser deck + speaker notes |
| Fundraise | Build the narrative, model and process | Full | Plan, model, deck, target list |
| Negotiate | Prepare a deal, contract or partnership | Quick | BATNA/ZOPA + trade plan |
| Product | Validate, position, launch or grow a product | Standard | Product strategy pack |
| 100-day | A new role, acquisition or turnaround | Standard | Day 1/30/100 plan |

## Depth ladder

| Depth | Time | What is produced | When |
|---|---|---|---|
| Quick structure | 30–60 min | One-page brief, three options, rough numbers, next test | Reversible or low-cost decision |
| Standard | Half a day | Evidence table, issue tree, model, decision memo | Most decisions |
| Full case | 1–3 days | Fact base, market model, financial model, risks, 100-day plan, board pack | Irreversible, external capital, board |

Say which depth you are using in the first response. Do not produce a board pack for a
reversible experiment.

## Pipeline

```
Frame → Diagnose → Choose → Value → Design/Deliver → Govern → Communicate
```

| Stage | Question | Owner skill | Gate |
|---|---|---|---|
| Frame | What decision, by whom, by when, at what stake? | strategy-core | decision question and depth agreed |
| Diagnose | What is true, and what would change the answer? | strategy-diagnosis-and-framing | fact base with evidence labels |
| Choose | Which options exist, and against which criteria? | strategic-choices-and-economics | three distinct options and a criterion set |
| Value | What is it worth, under which conditions? | strategic-choices-and-economics | model runs; sensitivities; kill conditions |
| Design | How will it work in practice? | operating-model-and-execution | capabilities, decision rights, sequence |
| Govern | How will we know it is working? | risk-performance-and-value-governance | KPIs, risk register, value ledger |
| Communicate | What is the ask, and who must agree? | executive-communication-and-alignment | one-page memo, stakeholder map |

Market work sits inside Diagnose and Choose; product/venture work routes to
`product-strategy`; a fundable plan routes to `business-plan-authoring`.

## Routing

| Need | Load |
|---|---|
| Frame a fuzzy question, issue tree, hypothesis, fact base, evidence | `strategy-diagnosis-and-framing` |
| Market size, segmentation, profit pools, competitor response | `market-and-competitive-intelligence` |
| Options, business case, unit economics, pricing, portfolio, synergy, negotiation | `strategic-choices-and-economics` |
| Operating model, org design, spans and layers, 100-day plan, initiative prioritisation | `operating-model-and-execution` |
| KPIs, value ledger, risk register, war games, behaviour signals | `risk-performance-and-value-governance` |
| Decision memo, narrative, stakeholder alignment, investor story | `executive-communication-and-alignment` |
| Startup/product validation, positioning, GTM, growth loops, monetization, launch | `product-strategy` |
| Full investor-grade business plan | `business-plan-authoring` |
| Finished `.pptx` deck — board, IC, investor, template fill, existing-deck edit | `presentation-authoring` |
| Browser-native deck — React slides, presenter mode, HTML/PDF/PPTX export | `open-slide` |
| Slide visual identity, palette, typography | `visual-design-and-branding` |
| A single calculator | `references/calculators.md` |

The narrative is approved before the artifact is built. A deck request without an
approved memo or deck-map gets the memo first; the deck is a compression of the
argument, not a substitute for it.

## Artifact layout

One directory per engagement:

```text
strategy/<slug>/
  00-brief.md            decision question, owner, deadline, stakes, depth
  01-issue-tree.md       MECE branches and initial hypotheses
  02-evidence.csv        claim, label, source, date, confidence
  03-options.md          three distinct options and criteria
  04-model/              JSON config + calculator output
  05-decision-memo.md    one page, answer first
  06-100-day-plan.md     owner, date, milestone, kill condition
  07-review.md           realised vs promised, after the fact
```

The exact files can shrink for a Quick structure, but the brief and the memo do not
disappear.

## First response

Keep it to five lines:

1. Restate the decision question.
2. Name the mode and depth.
3. State the two or three assumptions you are making.
4. Name the first artifact and the specialist skill you will use.
5. Ask at most one question, and only if a wrong guess would waste the work.

Then start. Do not ask the user to choose a framework.

## Quality gate

- [ ] One decision question, owner and deadline are written down.
- [ ] Three genuinely distinct options, or a stated reason there are fewer.
- [ ] Every material claim carries `[F]/[I]/[A]/[E]`.
- [ ] The financial model runs from a saved config; inputs, units and period are stated.
- [ ] Sensitivities or scenarios are printed, not implied.
- [ ] Kill conditions and the cheapest test are named.
- [ ] The recommendation survives the pre-mortem, or the exception is stated.
- [ ] The memo fits on one page and ends with the ask.
- [ ] If a deck is produced, every slide makes one claim, carries a source, and traces
      to the memo or evidence ledger; the file has been rendered and inspected.
- [ ] Every next action has an owner and a date.

## Reference map

| File | Contents |
|---|---|
| `references/personal-context.md` | editable defaults: domains, team size, capital, horizon, output style |
| `references/house-style.md` | decision memo shape, evidence labels, modelling rules, red-team protocol |
| `references/engagement-templates.md` | per-mode intake questions, artifacts and gates |
| `references/calculators.md` | every bundled calculator, its owner skill and config shape |
| `references/ATTRIBUTION.md` | sources and licences for adopted methods and calculators |
| `references/sources/INDEX.md` | archived upstream READMEs and licences |
