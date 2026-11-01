# Ad-Library Mining (Competitive Ads Extractor)

A **collection method** for competitive intelligence: mine competitors' paid ads from
public ad libraries (Meta/Facebook Ad Library, LinkedIn Ads Library, Google Ads
Transparency Center, TikTok Creative Center) and turn them into evidence about
positioning, messaging, and target segments. It supplies inputs to
[competitive-intel.md](competitive-intel.md); it does not infer likely moves or build
response plans on its own.

## When to use

- Building or refreshing a competitor evidence base: "extract ads from [competitor]",
  "what is [competitor] messaging right now?"
- Positioning research: which pain points, use cases, and value props rivals emphasize
- Spotting segment targeting by ad variation, and creative/copy patterns that recur
- Tracking a rival's messaging shift between periods ("compare Q1 vs Q2 ads")

## Workflow

1. **Scope the set**: one competitor for depth, 3–5 for pattern comparison, a category
   list for benchmarking.
2. **Extract**: query each ad library by advertiser name; capture ad copy, headline,
   CTA, format, media, landing page, and first-seen/active dates. Save screenshots as
   an evidence archive (`competitor-ads/<name>/`), plus a CSV of copy, CTAs, and themes.
3. **Tag**: group ads by theme, audience, format, and pain point. Count occurrences —
   frequency across a rival's own spend is the closest public proxy for what they think
   is working.
4. **Analyze**: what problems they highlight, which use cases they target, how they
   position against alternatives, which audiences each variation addresses, and which
   copy/creative patterns repeat.
5. **Cross-check**: compare platforms (LinkedIn vs Meta messaging differs by audience),
   compare rivals for whitespace, and re-run monthly to see what changed.
6. **Feed the analysis**: recurring themes and segment signals go into the competitor
   map and response plan in [competitive-intel.md](competitive-intel.md); whitespace in
   competitor messaging goes to [market-mapping.md](market-mapping.md).

## Analysis output

```markdown
# <Competitor> Ad Analysis

## Overview
[Total active ads, primary themes with %, formats, CTA patterns.]

## Key Problems They Highlight
1. **[Problem]** (n ads) — representative copy — why it resonates
2. **[Problem]** (n ads) — representative copy — why it resonates

## Creative Patterns
[Pattern name] — what it shows — how many ads use it — when it is used.

## Audience Targeting Signals
[Segment → message angle, inferred from ad variations.]

## Copy That's Working
[Headlines and body patterns, with frequency.]

## Implications
[Whitespace to exploit, claims to rebut, pain points to address — each tied to a
recommended action.]
```

## Collection rules

- Use only public ad libraries and account for research; respect platform terms of service.
- Store copies as **evidence**, cite the library and date retrieved — an ad set is a
  snapshot, not a permanent fact.
- Do not plagiarize copy or designs: adapt patterns into original creative; the
  insight is the pattern, not the wording.
- Ad volume is not performance — libraries show what is running, not what converts.
  Treat "runs many variations of X" as `[I]` (inference), never as `[F]` for efficacy.
- Track over time: a single pull cannot show a messaging shift.

## Quality bar

- [ ] Every claim cites the ad library, advertiser, and retrieval date
- [ ] Theme counts back the "what's working" language; no vibes-based conclusions
- [ ] Competitor messaging facts (`[F]`) are separated from performance inferences (`[I]`)
- [ ] Findings land in the competitor map, response plan, or whitespace list — not a report nobody uses
- [ ] Original creative is derived from patterns, not copied
