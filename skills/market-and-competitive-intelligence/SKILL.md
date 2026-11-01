---
name: market-and-competitive-intelligence
description: >-
  Read the external environment and decide where to play: define and size markets
  with top-down and bottom-up cross-checks, segment them MECE, map where profit pools
  actually sit, define priority customer segments, build a competitor evidence base
  (filings, pricing pages, job postings, review sites, and public ad libraries), and
  infer likely rival moves with pre-committed responses. This skill also owns the
  shared strategy-framework library the other strategy skills link to — Porter's Five
  Forces, Value Chain, Ansoff, BCG growth-share, GE nine-box, Blue Ocean, VRIO, 7S,
  Wardley mapping, and scenario planning. Use when the user asks "how big is this
  market", "where is the white space", "which customers should we prioritize", "where
  does the profit sit", "what will competitors do next", "map this category", "is this
  industry attractive", or "extract [competitor]'s ads and tell me what messaging is
  working". Do not use for the internal fact base or root-cause diagnosis
  (strategy-diagnosis-and-framing), for choosing or valuing options (strategic-choices
  and-economics), or for general research with no market or competitor question
  (research-and-insight-analysis); a full fundraise business plan that builds on
  this skill's market work is business-plan-authoring.
license: MIT
---

# Market and Competitive Intelligence

Market skills answer **where to play**: how big the field is, which parts of it are
worth entering, who the customers are, where profit concentrates, and what the other
players will do. They do not establish the internal fact base (that is
[../strategy-diagnosis-and-framing/SKILL.md](../strategy-diagnosis-and-framing/SKILL.md))
and they do not choose between options or value them (that is
`../strategic-choices-and-economics/SKILL.md`).

This skill also hosts the bundle's **shared strategy-framework library**
([references/frameworks-strategy.md](references/frameworks-strategy.md)) — the full
practitioner workflows for Porter, Ansoff, BCG, Blue Ocean, VRIO, 7S, Wardley, and
scenario planning. Other strategy skills link here rather than restating them.

## When to use

- Sizing a market: "how big is this market?", TAM/SAM/SOM, opportunity screening, expansion cases
- Structuring a category: market definition, segmentation, growth, white space, "where should we play?"
- Finding where money is made: profit pools, value-chain economics, margin concentration, pricing power by activity
- Prioritizing customers: "which customers should we prioritize?", ICP, segment attractiveness, GTM focus
- Competitive intelligence: "what will competitors do next?", rival response to a price move, launch, entry, or M&A
- Collection: mining public ad libraries — "extract [competitor]'s ads and tell me what messaging is working"
- Industry structure questions: competitive intensity, supplier/buyer power, substitutes, category maturity

**Do not use for** — `strategy-diagnosis-and-framing` when the question is what is
true *inside* the business: current-state fact base, growth root cause, assumption
audits, issue trees; `strategic-choices-and-economics` when the environment is mapped
and the question becomes which option to pick, what it is worth, how to price it, or
where to allocate capital; `research-and-insight-analysis` when the ask is open-ended
research, synthesis of sources, or insight reporting with no market, segment, or
competitor decision behind it; a full fundraise business plan that runs on top of
this skill's market work is `business-plan-authoring`.

For a deal-ready interactive HTML battlecard or a written competitive analysis brief (feature matrices, win/loss, battlecard sections) use the **competitive-brief** skill (its battlecard-artifact reference produces the HTML output). This skill owns the strategic reading of the external environment and the shared framework library.


## Workflow

Depth mode comes first: detect Quick Structure / Full Case / Client Deliverable using
the definitions in
[../strategy-diagnosis-and-framing/SKILL.md](../strategy-diagnosis-and-framing/SKILL.md).
Quick Structure answers one of the steps below with a map or table; Full Case and
Client Deliverable run all of them and apply the evidence, synthesis, and
devil's-advocate gates from that skill.

1. **Frame the where-to-play question.** Decision, decision-maker, success metric, and
   the market boundary: geography, customer type, product scope, time horizon,
   exclusions. A boundary stated after sizing is a rationalization.

2. **Size and segment the market.** Run the playbook in
   [references/market-mapping.md](references/market-mapping.md): top-down and bottom-up
   sizing reconciled, segments MECE and decision-relevant, white space marked. All
   sizes are `[E]` estimates with source, year, and coverage — never invented.

3. **Locate the profit.** Run
   [references/profit-pool-analysis.md](references/profit-pool-analysis.md) to separate
   revenue pools from profit pools and explain the structural reason profit
   concentrates. Attractiveness from steps 2–3 is market-side only; right to win is
   not assessed here.

4. **Define priority customer segments.** Run
   [references/customer-segmentation.md](references/customer-segmentation.md) when the
   decision needs sharper customer groups: needs, economics, behavior, strategic
   value — with observable definitions. Segment quality rules apply even when step 2
   already produced a segment map.

5. **Build the competitor evidence base.** For each relevant rival and substitute:
   position, incentives (mandates, ownership, what management is measured on),
   capabilities, constraints, economics. Sources: filings and earnings calls, pricing
   and packaging pages, release notes, job postings, partner announcements, review
   sites — plus **ad-library mining** as a dedicated collection method in
   [references/competitive-ads-extractor.md](references/competitive-ads-extractor.md).

6. **Infer likely moves and pre-commit responses.** Run
   [references/competitive-intel.md](references/competitive-intel.md): base, aggressive,
   and defensive scenarios per competitor, each with a trigger, impact, confidence,
   and an observable early-warning signal.

7. **Select frameworks from the shared library.** Industry structure and value-chain
   questions open
   [references/frameworks-strategy.md](references/frameworks-strategy.md) — use its
   "which framework for which question" table rather than memorizing. The bundle-wide
   framework-selection guardrails (when *not* to reach for Five Forces) live in
   [../strategy-diagnosis-and-framing/SKILL.md](../strategy-diagnosis-and-framing/SKILL.md).

8. **Synthesize the where-to-play read.** Answer first, then market definition and
   size, segment and profit-pool maps, competitor read, and response plan — with risks,
   kill conditions, and next actions per the contract in
   ../strategy-diagnosis-and-framing/SKILL.md. Hand options and their economics to
   `../strategic-choices-and-economics/SKILL.md`.

## Quality bar

- [ ] Market boundary and exclusions are stated before any number
- [ ] Size reconciles two methods; the gap, or its absence, is explained
- [ ] No fabricated market size — missing data is named as missing data
- [ ] Segments are MECE, observable, and tied to a decision
- [ ] Revenue pools and profit pools are shown separately, with the structural driver of each concentration
- [ ] Every competitor prediction states the incentive behind it, with confidence and an early-warning signal
- [ ] Ad-library and other collection evidence is cited with source and date; inferences are labeled `[I]`
- [ ] Market attractiveness is never presented as right to win
- [ ] At least 2 risks and 2 kill conditions accompany any where-to-play recommendation

## Reference map

| Situation | Open |
|---|---|
| Sizing, segmentation, white space, where-to-play options | [references/market-mapping.md](references/market-mapping.md) |
| Profit concentration, value-capture, margin leakage | [references/profit-pool-analysis.md](references/profit-pool-analysis.md) |
| Customer segments, ICP, segment prioritization | [references/customer-segmentation.md](references/customer-segmentation.md) |
| Competitor mapping, likely moves, response plan | [references/competitive-intel.md](references/competitive-intel.md) |
| Mining Meta/LinkedIn/Google ad libraries for messaging intelligence | [references/competitive-ads-extractor.md](references/competitive-ads-extractor.md) |
| Strategy frameworks: Five Forces, Value Chain, 7S, VRIO, Ansoff, BCG, Nine-Box, Blue Ocean, Wardley, scenarios | [references/frameworks-strategy.md](references/frameworks-strategy.md) |
| Depth modes, MECE/issue trees, evidence labels, synthesis contract | [../strategy-diagnosis-and-framing/SKILL.md](../strategy-diagnosis-and-framing/SKILL.md) |
| Option comparison, business-case economics, pricing moves, portfolio allocation | [../strategic-choices-and-economics/SKILL.md](../strategic-choices-and-economics/SKILL.md) |

## Output format

Where-to-play reads combine into one brief; individual playbooks supply their own
exhibit templates:

```markdown
# Market and Competitive Read — <topic>

## Bottom line
[Where to play, or what changes — one sentence.]

## Market definition and size
[Boundary and exclusions; top-down vs bottom-up estimate, both labeled [E] with
source and confidence.]

## Segment map
| Segment | Size | Growth | Profitability | Competition | Attractiveness |

## Profit pools
| Pool | Revenue | Margin | Profit | Growth | Structural driver |

## Competitor read
| Competitor | Position | Incentives | Capabilities | Likely move | Confidence |

## Response plan
| Scenario | Early signal | Recommended response |

## Risks / Kill conditions / Next actions
[Per the contract in ../strategy-diagnosis-and-framing/SKILL.md — minimum 2 each.]
```
