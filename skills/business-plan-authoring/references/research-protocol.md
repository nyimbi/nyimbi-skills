# Research Protocol

How the research phase (Workflow step 2) is run. The output is not "information
gathering" — it is a **claim file**: every market statement the plan will later
make, with a source, a date, and a confidence tag. If a claim is not in the
claim file, it cannot appear in the plan.

## 1. Research questions (answer all before drafting)

| # | Question | Minimum bar to count as answered |
|---|---|---|
| 1 | How big is the market, and how fast is it growing? | Two independent sizing methods; growth over 3+ years or a credible cohort basis |
| 2 | What is the realistic addressable wedge (SAM/SOM)? | Bottom-up build from segments the team can actually reach |
| 3 | What do buyers actually pay? | Two or more independent price sources, or the plan's own pricing data |
| 4 | Who do buyers choose today, including "nothing"? | Named set incl. incumbent, adjacent, manual/Excel, and do-nothing with each one's strength |
| 5 | How does the strongest competitor respond if this succeeds? | At least one modeled response (price cut, feature match, bundling, acquisition) |
| 6 | What is the regulatory shape, and is it a barrier or a tailwind? | Named regulations; whether the team holds or needs approvals |
| 7 | **Why now?** What changed in the last 24 months? | Two or more concrete, dated changes (technology, cost curve, regulation, behavior) |
| 8 | What does it cost to hire/build in this area? | Salary bands for key roles; key input costs; anything that constrains the margin claim |

Question 7 is the one founders most often leave blank and investors ask first.
"We're early" is not an answer; "in [date], [change] made [capability] available
to [segment], which [metric] confirms" is.

## 2. Source hierarchy

Rank sources; when sources conflict, the higher rank wins **unless** the lower
source is materially newer — in that case state the conflict and date both.

1. **Primary** — company filings and earnings calls, regulator and statistics
   agency data (census, trade associations, central banks), patent filings,
   court records, the company's own customer/usage data
2. **Secondary** — established analyst firms, major business press with named
   reporters and primary sourcing, peer-reviewed work
3. **Tertiary** — vendor blogs, press releases, listicles, forum claims. Use
   only to generate leads to verify at higher tiers, never as the citation of
   record

**Never cite**: the plan's own claims, a round of funding as proof of market
size (circular), a competitor's marketing claim about the market (they sell
the market too), or a source whose business model depends on the market being
large.

## 3. Cross-check rules

- **TAM**: top-down (share of a larger measured market) and bottom-up
  (number of units × price) must both be built. If they differ by more than 2x,
  the plan must explain why — an unexplained gap is treated by hostile readers
  as a confession that one of the two was cooked.
- **Growth rates**: require three or more years of history, or a cohort/vintage
  basis. A one-year number with a trend line is a claim, not a fact — tag it.
- **Price points**: two independent sources. If the only evidence is the
  founder's own quotes, tag `[Assumed — internal data]` and say so.
- **Competitor claims**: every claim about a competitor's weakness must be
  checkable by that competitor's customer or a named source. "Their support is
  slow" is not evidence; "their public changelog shows feature X absent for 14
  months, and [source]" is.

## 4. Citation and the claim file

Every claim the plan will use is recorded as:

```
[Claim number] <the exact sentence the plan will make>
  Tag:      [Sourced] | [Assumed] | [Assumed — internal data]
  Source:   <name>, <date>, <URL>   (omit for internal data; state the sample size)
  Confidence: high | medium | low
  Kill condition: <what finding would falsify this, and where to check it>
```

Rules:

- The plan body uses the claim number or a short tag, e.g. "the market grows
  18% annually¹" with ¹ resolving in the evidence ledger.
- A claim may not be promoted from `[Assumed]` to `[Sourced]` without a
  source in the file.
- Dates matter: market data older than 24 months must be flagged as such, and
  anything older than 36 months needs a refresh attempt before it is used.
- If a search returns nothing for a claim, record "no public source found" —
  that is evidence too, and honest about the assumption's status.

## 5. Research effort calibration

Scale research to the decision: a pre-seed plan needs questions 1, 3, 4, 7
reasonably well and the rest flagged `[Assumed]` with kill conditions; a Series
A or debt plan needs all eight questions sourced. Spending research effort on a
question the funder will not probe is waste; skipping the question they will
probe first (why now, unit economics inputs) is how plans die in the room.
