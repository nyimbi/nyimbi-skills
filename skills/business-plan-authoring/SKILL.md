---
name: business-plan-authoring
description: >-
  Write a venture-grade business plan that survives a hostile, skeptical
  investor: every market claim sourced and dated, TAM cross-checked two ways,
  projections built from drivers not growth rates, and a mandatory red-team
  pass that finds the plan's three weakest points before the funder does.
  Includes a live web-research phase (market size, pricing, competitors,
   "why now") and a section-by-section defense template. It also compresses the
   finished plan into the investor deck narrative (one claim per slide) before
   handing the slide file off. Use when the user says "write a business plan",
   "I need a plan for our seed/Series A raise", "make this defensible before we
   meet the investors", "stress-test my plan", "build the financials for our
   fundraise", "turn this plan into a pitch deck", or asks for a plan they can
   put in front of a skeptical VC, PE firm, or lender. Do not use for a one-page
   business case or investment memo (see strategic-choices-and-economics), for
   producing the .pptx file itself (see presentation-authoring — this skill owns
   the deck narrative and hands off the slide file), for market research without
   a plan (see market-and-competitive-intelligence), or for the strategy behind
   the plan (see strategy-diagnosis-and-framing).
---

# Business Plan Authoring

A business plan is not a description of the business. It is a **claim that
someone should commit capital, with the evidence to survive someone trying to
destroy it.** This skill assumes the reader is hostile by default: they believe
the market is smaller than you claim, the competition stronger, the unit
economics worse, and the team less capable — until every one of those beliefs
is refuted with a dated source, a driver, or a track record.

Plans fail with investors for three reasons, in order of frequency: (1) a
number that does not survive the first "show me your math" — usually TAM or CAC
payback; (2) a projection that is a hockey stick with no drivers underneath;
(3) the plan hiding its own weakest point, which the investor finds and then
discredits everything else. The workflow below is engineered against exactly
these three.

## When to use

- "Write a business plan" / "business plan for my startup"
- "I have a seed / Series A / bridge meeting with VCs — I need the plan"
- "Make this plan defensible before [funder] sees it"
- "Stress-test my plan" / "what's going to get me killed in this one?"
- "Build the financials for our raise" / "use of funds"
- Preparing a plan for a bank, PE firm, strategic acquirer, or government grant

**Do not use for** — a single investment decision or one-off business case (see
`strategic-choices-and-economics` — its `business-case-builder.md` is used by
this skill, step 4); turning a finished plan into slides (see
`presentation-authoring`); market sizing or competitive analysis without a
fundraise attached (see `market-and-competitive-intelligence`); the strategic
logic of what to build (see `strategy-diagnosis-and-framing`).

## Workflow

1. **Intake and epistemic inventory.** Before any research, separate what the
   founder *knows* (signed customers, measured CAC, shipped product, founder
   domain evidence) from what is *assumed* and what is *unknown*. Write the
   funding decision explicitly: round, amount, use of funds, the milestone the
   money buys, and the threshold the plan must clear to be worth presenting.
   If the founder cannot state the threshold, the plan cannot be evaluated —
   get it stated. Everything the plan later claims as fact must be classed here
   as fact, assumption, or unknown; claims invented mid-draft are the classic
   failure mode.

2. **Research (live).** Execute `references/research-protocol.md`. Search the
   web for: market size and growth (two independent sizing methods), price
   points (at least two sources per price claim), the competitive set including
   "do nothing" and the incumbent, regulatory shape, and — most undervalued —
   **why now**: what changed in the last 24 months that makes this possible or
   valuable now. Every market claim gets `[Source: name, date]`. Claims that
   cannot be sourced get tagged `[Assumed]` and an entry in the assumption
   register with a kill condition (`../strategy-diagnosis-and-framing/references/assumption-audit.md`).

3. **Market and competitive section.** Run the market playbooks rather than
   re-inventing them: `../market-and-competitive-intelligence/references/market-mapping.md`
   (TAM/SAM/SOM, top-down AND bottom-up, with the gap between the two
   explained — an unexplained gap is an invitation to discount the whole
   section), `profit-pool-analysis.md`, `customer-segmentation.md`, and
   `competitive-intel.md` (model how the strongest competitor responds to a
   successful version of this company — hostile investors run exactly this
   model).

4. **Economics and scenarios.** Unit economics first (CAC, LTV, payback, gross
   margin with its cost drivers), pricing logic from
   `../strategic-choices-and-economics/references/frameworks-pricing.md`, then
   base / downside / upside cases via
   `../strategic-choices-and-economics/references/business-case-builder.md` —
   same structure, different assumptions, each scenario's drivers visible.
   No false precision: a two-significant-figure LTV with six-digit inputs is a
   red flag, not a virtue.

5. **Projections.** Build the 24–36 month model per `references/projections.md`:
   revenue from drivers (cohorts × logo economics × expansion; hires that
   produce output, not the reverse), use of funds bridging burn to named
   milestones. A projection is defensible only if an investor can change one
   driver and watch the output move sensibly. If they cannot, rebuild.

6. **Draft the plan.** Write section by section using
   `references/section-defense.md` — each section states its claim, the
   evidence, and its strongest counter-argument *inside the plan*. Write the
   executive summary last, answer-first: what, market, why now, traction, why
   we win, the ask. Narrative discipline follows
   `../executive-communication-and-alignment/SKILL.md` (Pyramid Principle, SCQA,
   hostile-question prep).

7. **Hostile red-team pass (mandatory, not skippable).** Execute
   `references/hostile-review.md`: the question battery per section, a written
   pre-mortem, and the explicit naming of the plan's three weakest points with
   mitigations and kill conditions. Findings are triaged fatal / fixable /
   acknowledged — fatal findings block delivery until fixed; acknowledged ones
   must appear in the risk section so the funder sees them stated honestly
   before they find them.

8. **Finalize.** Assemble the evidence ledger (every `[Source]` and `[Assumed]`
   tag, with confidence and kill conditions), the sources appendix, and — on
   request — a separate investor Q&A prep doc answering the 10 hardest
   questions out of the red-team pass. If a deck is wanted, run the
   compression pass in `references/deck-map.md` to produce the 12-slide
   outline (claims, appendix list, ledger cross-check), then hand the `.pptx`
   production to `presentation-authoring`
   (direct `.pptx`) or to `open-slide` (modern, browser-presentable deck with
   HTML/PDF/PPTX export) — offer the choice when the user has no format preference. Deliver the plan and the red-team
   findings together: a plan that has not been attacked and survived is a
   draft, not a plan.

## Quality bar

- [ ] Every quantitative claim is either `[Sourced]` (name + date + URL) or
      `[Assumed]` (with kill condition in the assumption register) — zero
      untagged numbers
- [ ] TAM sized two independent ways; the gap between top-down and bottom-up
      is explicitly explained
- [ ] Every price-point and growth-rate claim has two or more independent
      sources, or is tagged `[Assumed]`
- [ ] Projections are driver-based; an investor can change one driver and the
      output moves sensibly; no hockey-stick-without-drivers
- [ ] CAC, LTV, payback, and gross margin are each derived, not asserted —
      with the cost drivers of margin named
- [ ] "Why now", "why you", and "why we beat [incumbent]" are each answered in
      a paragraph with evidence, not adjectives
- [ ] The plan names its three weakest points in the risk section with
      mitigation and kill condition — before the funder names them
- [ ] The red-team pass was actually executed and its findings triaged (fatal /
      fixable / acknowledged); all fatal findings are resolved
- [ ] Use of funds matches the projection's hiring and milestone plan line by
      line; the burn bridge reaches the milestone the round is sold on
- [ ] Executive summary is answer-first and states the ask, the milestone the
      money buys, and the current traction
- [ ] The evidence ledger and sources appendix are complete and consistent with
      every tag in the body

## Reference map

| Situation | Open |
|---|---|
| Running the research phase (what to search, source hierarchy, citation rules, why-now) | [research-protocol](references/research-protocol.md) |
| Drafting any section — template, per-section claims, and the standard hostile attack it faces | [section-defense](references/section-defense.md) |
| Building the 24–36 month model and use of funds | [projections](references/projections.md) |
| Running the mandatory red-team pass — question battery, pre-mortem, weakest-point rule | [hostile-review](references/hostile-review.md) |
| Compressing the finished plan into the investor deck — 12-slide structure, one-claim rule, compression pass | [deck-map](references/deck-map.md) |
| TAM/SAM/SOM, profit pools, segmentation, competitor response modelling | [../market-and-competitive-intelligence/SKILL.md](../market-and-competitive-intelligence/SKILL.md) and its references |
| Base/downside/upside scenarios, decision thresholds, false-precision rules | [../strategic-choices-and-economics/references/business-case-builder.md](../strategic-choices-and-economics/references/business-case-builder.md) |
| Unit economics and financial mechanics | [../strategic-choices-and-economics/references/frameworks-financial.md](../strategic-choices-and-economics/references/frameworks-financial.md) |
| Pricing power and packaging claims | [../strategic-choices-and-economics/references/frameworks-pricing.md](../strategic-choices-and-economics/references/frameworks-pricing.md) |
| Assumption register and kill conditions | [../strategy-diagnosis-and-framing/references/assumption-audit.md](../strategy-diagnosis-and-framing/references/assumption-audit.md) |
| Evidence standards for what counts as proof | [../strategy-diagnosis-and-framing/references/evidence-standards.md](../strategy-diagnosis-and-framing/references/evidence-standards.md) |
| Executing-summary and narrative discipline, hostile-question prep | [../executive-communication-and-alignment/SKILL.md](../executive-communication-and-alignment/SKILL.md) |
| Producing the actual `.pptx` from the deck-map outline (format, layouts, OOXML) | [../presentation-authoring/SKILL.md](../presentation-authoring/SKILL.md) |
| Producing a modern, browser-presentable deck from the deck-map outline (React slides, HTML/PDF/PPTX export) | [../open-slide/SKILL.md](../open-slide/SKILL.md) |

## Output format

Deliver three artifacts, plus a fourth when a deck is wanted:

```markdown
# [Company] — Business Plan
<12 sections per references/section-defense.md, each section ending with
 "Strongest counter-argument and our answer">

## Evidence ledger
| Claim | Tag | Source / kill condition | Confidence |
|---|---|---|---|

## Appendix: Sources
[Numbered, dated, with URL — every [Sourced] tag resolves here]
```

```markdown
# Red-Team Findings — [Company]
| # | Section | Attack | Verdict (fatal/fixable/acknowledged) | Disposition |
|---|---|---|---|---|
+ named top-3 weakest points with mitigation and kill condition
```

```markdown
# Investor Q&A Prep — [Company]
<the 10 hardest questions from the red-team pass, each with the prepared
answer and the evidence it leans on>
```

```markdown
# Deck Outline — [Company]   (only when a deck is wanted; per references/deck-map.md)
<12 slides, each: claim, feeds-from section, one-line counter-argument,
 evidence-ledger entry for every number>
+ appendix list + handoff note to presentation-authoring
```
