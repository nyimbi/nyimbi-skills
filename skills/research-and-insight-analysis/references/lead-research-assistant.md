# Lead Research Assistant

Purpose: qualify a shortlist of companies or people against your offering and
turn each into an outreach angle. This is the sales/business-development track
of `research-and-insight-analysis`.

## When this track applies

The user has something to sell or partner on and wants named, ranked accounts —
"find 10 companies that would buy this", "build a target list for [region/
industry]", "who should I contact at these accounts".

## Evidence sources

| Layer | Sources |
|---|---|
| Your side (required) | Product/service description or the repo itself — code, README, pricing page — to derive the value proposition |
| Ideal customer profile | Stated by the user, or inferred: industry, company size, location, growth stage, tech stack, pain points the product removes |
| Candidate companies | Web search on industry/size/location filters; job postings (hiring for the problem you solve); tech-stack detectors and public stack traces; funding and expansion news; complementary-product customer lists |
| Signals of need | Recent news, layoffs/reorgs, tool migrations, compliance deadlines, "we're hiring for X" posts |
| Contact layer | Publicly listed decision-maker role and profile URL — role and title only unless the user supplies the rest |

Record where each fact came from and when it was observed. A fit claim with no
source is an inference, not a fact, and must be labelled as one.

## Method

1. Restate the value proposition in one sentence, then derive the ICP as
   explicit filter criteria (industry, size, geography, stack, trigger events).
2. Search against those criteria; keep a candidate pool roughly 3× the requested
   size so ranking has something to work with.
3. For each candidate, collect the evidence rows: what they do, size/stage,
   stack, the trigger signal, why the pain is real *for them*.
4. Score 1-10 against a rubric written down before scoring starts — ICP
   alignment, strength of the need signal, budget indicator, timing.
5. Rank, drop below-threshold candidates, and write the outreach angle for each
   survivor.

## Output template

```markdown
# Lead Research Results

## Summary
Total found: X | High priority (8-10): X | Medium (5-7): X | Average fit: X

## Lead N: <Company>
**Website**: URL   **Priority score**: N/10 (rubric: …)
**Industry / size / stage**: …
**Why they fit**: 2-3 specific reasons, each tied to observed evidence
**Evidence**: signal | source | observed date
**Target decision maker**: role/title   **Profile**: URL if public
**Value proposition for them**: the specific problem you remove
**Outreach strategy**: personalized approach referencing their signal
**Conversation starters**: 2 concrete hooks
```

Offer the CSV (one row per lead: company, score, tier, decision-maker role,
signal, next action) as the CRM-ready follow-up.

## Quality gates for this track

- Every "why they fit" line cites an observed signal, not a restatement of the ICP
- Scores were produced against a rubric written before any candidate was scored
- Decision-maker is a role/title; no personal contact data invented
- Companies below threshold were removed rather than padded into the count
- The outreach strategy references something true and recent about that company
- Stale signals carry their observation date so the reader can judge freshness
