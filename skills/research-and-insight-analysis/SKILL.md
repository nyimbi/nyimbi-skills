---
name: research-and-insight-analysis
description: >- For scientific literature reviews and research databases (arXiv/PubMed/Semantic Scholar + 78 scientific DBs), see scientific-research.
  Run one research method across four kinds of question: qualify sales leads
  against an ideal customer profile with scores and outreach angles, mine
  meeting transcripts for behavioral and communication patterns with
  timestamped quotes, turn Claude Code history into a prioritized skill-gap
  report with curated learning, and brainstorm domain names with live
  availability checks. Frame the question, gather evidence with provenance,
  structure the findings, rank and qualify them, and deliver a brief someone
  can act on the same day. Use when the user says "find me leads that match our
  ICP", "research this company or person", "build a target list", "when do I
  avoid conflict in meetings", "what are my communication patterns", "analyze
  my coding history and tell me what to learn", "suggest domain names and check
  availability", "score and shortlist these options", or "turn these
  transcripts/notes into insights". Do not use for competitor, ad or positioning
  analysis (see market-and-competitive-intelligence), for drafting or polishing
  prose and documents (see writing-and-internal-communications), for diagnosing
  a business's strategic problem (see strategy-diagnosis-and-framing), or for
  questions about Claude's own skills, MCP servers and agents (see
  skill-authoring-and-agent-tooling).
---

# Research and Insight Analysis

Four different-looking jobs — a target list, a behavior report, a skill-gap
memo, a naming shortlist — turn out to be the same job. Each starts with a
question someone will act on, ends with a ranked, evidenced recommendation, and
fails in exactly the same way: a pile of interesting facts that never got
ranked against the question, or a confident claim with nothing behind it.

The method below is the shared spine. What differs per track is only *which
evidence is admissible*, *how ranking is defined*, and *what shape the brief
takes* — those live in the Track playbooks and their reference files.

## When to use

- Finding and qualifying companies or people to sell, partner, or pitch to
- Building a scored target list with outreach angles and decision-maker roles
- Reading a folder of meeting transcripts for conflict avoidance, speaking
  ratios, filler, listening, and facilitation patterns
- Comparing communication behavior across two time periods, or preparing
  evidence for a performance review
- Turning your own recent Claude Code history into prioritized skill gaps plus
  a reading list
- Brainstorming domain names and verifying which are actually registerable
- Ranking, shortlisting, or scoring any set of options against stated criteria
- Distilling a pile of notes, transcripts, or search results into a brief with a
  recommendation

**Do not use for** — `market-and-competitive-intelligence` when the subject is
competitors, their ads, or their positioning (it owns competitive ad extraction
and the landscape view); `writing-and-internal-communications` when the ask is
to write, edit, or polish the document itself rather than find out something;
`strategy-diagnosis-and-framing` when the problem is why a business is
underperforming and the deliverable is a strategic diagnosis; and
`skill-authoring-and-agent-tooling` when the thing being researched is Claude's
own skills, MCP servers, or agent behavior.

- Synthesizing user-research data (interviews, surveys, usability, NPS) into themes, segments, or personas — use the **research-synthesis** skill; planning or conducting a study — **user-research**. This skill serves the non-user-research questions above.

## Workflow

1. **Frame the question.** Write the question as the reader will judge it: who
   is this for, what decision does it inform, what would make the answer wrong,
   and what does "done" look like (a 10-lead shortlist? three patterns with
   quotes? a top pick?). Anything that does not serve that decision is out of
   scope. Output: a one-sentence question plus acceptance criteria.

2. **Choose the track and its admissible evidence.** Pick the playbook below.
   Declare up front what counts as evidence for this track — live lookups,
   transcript quotes, timestamped history entries — and what is merely
   inference. Inference is allowed; unlabelled inference is not. Output: a
   source plan naming where each part of the answer will come from.

3. **Gather with provenance.** Collect only what the source plan allows, and
   attach origin and observation date to every fact as you go: search result,
   quote plus timestamp, history line, availability lookup. Capture the quotes
   and numbers you will need later *during* gathering — you cannot reconstruct
   them afterwards. Output: an evidence set where every row can be traced.

4. **Structure the findings.** Group the raw evidence into themes, and give
   each finding a one-line statement, its supporting rows, and its confidence.
   Contradictions and single-source claims go in visibly rather than being
   smoothed over. Output: a findings table, evidence attached.

5. **Rank and qualify.** Apply the ranking rule for the track — fit rubric,
   pattern impact, gap severity, name quality — and score or order the set.
   Then drop what falls below the threshold: a shortlist nobody would act on is
   worse than a short one. Output: a ranked set with explicit criteria and
   confidence per item.

6. **Run the quality bar.** Check the gates below before drafting. The two that
   kill briefs are a claim with no source and a ranking whose criteria were
   written after seeing the results. Output: a pass/fail per gate, with gaps
   recorded as gaps.

7. **Write the actionable brief.** Recommendation first, evidence second,
   next actions last — each with an owner or a clear "you" and a verb. State the
   period covered, the sample size, and what was not checked. Offer the
   machine-readable follow-up where the track defines one (lead CSV, invoice
   summary). Output: the brief, in the track's template.

## Quality bar

- [ ] Every factual claim traces to a source with an observation date; inferences are labelled as inferences
- [ ] The ranking criteria were written before the items were scored, and are stated in the brief
- [ ] Quotes are verbatim with a timestamp or file reference; numbers come with the sample they were counted over
- [ ] High-impact claims resting on a single source are flagged as such rather than asserted
- [ ] Anything verified live (availability, search results, resource links) was checked in this session and is dated
- [ ] Nothing was invented: no names, URLs, titles, quotes, or statistics from memory
- [ ] Gaps, contradictions, and out-of-scope items are reported, not omitted
- [ ] The recommendation is specific enough to act on today, with an owner and a next step
- [ ] The brief states its period, sample size, and what would change the conclusion

## Track playbooks

### Lead research → scored target list

Question: *who will buy this, and how do I open the conversation?* Evidence is
company facts plus trigger signals (job postings, stack changes, funding, news)
measured against an ICP written down before scoring. Ranking is a 1-10 fit
rubric; the output is a prioritized lead list where each entry carries its
evidence, a target decision-maker role, a value proposition, and an outreach
strategy that references something true and recent about that company. Full
source table, rubric guidance, and template:
[references/lead-research-assistant.md](references/lead-research-assistant.md).

### Meeting insights → behavior report with timestamps

Question: *how do I actually behave in meetings, and what do I change first?*
Evidence is transcript quotes and counted tallies — nothing else. Ranking is by
impact on the reader's goal (leading, being heard, closing decisions). The
output pairs each pattern with 2-3 verbatim quotes at timestamps, the stats that
show frequency, and 3-5 next steps runnable in the next meeting. Lenses,
extraction markers, and template:
[references/meeting-insights-analyzer.md](references/meeting-insights-analyzer.md).

### Developer growth → skill-gap report with reading list

Question: *what should I learn next, given what I have actually been doing?*
Evidence is a windowed `~/.claude/history.jsonl` — projects, technologies,
struggle signals — with learning resources added only after the gaps are known,
from searches run now. Ranking is impact on development velocity. The output is
3-5 specific, evidenced improvement areas, strengths, prioritized action items,
and 2-3 genuinely relevant resources per area. Method and template:
[references/developer-growth-analysis.md](references/developer-growth-analysis.md).

### Domain naming → available shortlist with a winner

Question: *what can we actually register, and which should we take?* Evidence is
generation against explicit constraints plus a **live** availability lookup per
candidate × TLD — an unverified "available" is the one error that costs money
and trust. Ranking weighs meaning, length, pronounceability, and TLD fit for the
audience. The output separates available from taken/premium, names a top pick
and a runner-up with reasons, and closes with register-now next steps. TLD
guide, naming bar, and template:
[references/domain-name-brainstormer.md](references/domain-name-brainstormer.md).

## Reference map

| Situation | Open |
|---|---|
| Scoring leads, ICP filters, outreach angles, lead CSV | [lead-research-assistant.md](references/lead-research-assistant.md) |
| Transcript lenses, counting markers, period comparison | [meeting-insights-analyzer.md](references/meeting-insights-analyzer.md) |
| History windowing, struggle signals, resource curation | [developer-growth-analysis.md](references/developer-growth-analysis.md) |
| Naming constraints, TLD selection, availability checks | [domain-name-brainstormer.md](references/domain-name-brainstormer.md) |
| Competitor landscapes, ad and positioning extraction | [../market-and-competitive-intelligence/SKILL.md](../market-and-competitive-intelligence/SKILL.md) |

## Output format

All four tracks deliver the same skeleton; only the middle block changes.

```markdown
# <Subject> — Research Brief

## Recommendation
One paragraph: what to do, and why it wins against the question in step 1.

## Question and scope
The question, the decision it informs, period covered, sample size,
what was deliberately not checked.

## Ranked findings
| # | Item | Score / rank | Key evidence | Confidence | Next step |
|---|---|---|---|---|---|

## Evidence detail
Per top item: the source rows, verbatim quotes with timestamps, or the
lookup result that backs it — enough that a skeptic can re-check it.

## Gaps and caveats
Single-source claims, contradictions, stale data, out-of-scope items.

## Next actions
Numbered, each with an owner and a verb. Offer the machine-readable
follow-up (lead CSV, summary sheet) where the track defines one.
```
