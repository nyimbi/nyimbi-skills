# Developer Growth Analysis

Purpose: read a window of your own Claude Code history and return an
evidence-based skill-gap report plus a curated reading list. This is the
self-assessment track of `research-and-insight-analysis`.

## When this track applies

The user wants structured feedback on their own recent work without waiting for
a code review: "analyze my developer growth from my recent chats", "what should
I learn from what I've been doing", "what did I struggle with this week".

## Evidence sources

Primary: `~/.claude/history.jsonl` — one JSON object per line with `display`
(the user's message), `project`, `timestamp` (Unix ms), and `pastedContents`.
Filter to the requested window (default the last 24-48 hours) against the
current timestamp before reading anything.

Secondary: the projects referenced in those entries (repo structure, the code
the complaints are about) when the user wants the observations tied to real
files.

Optional: a search source for learning material (HackerNews via an MCP tool, or
web search) used *after* the gaps are identified, and a delivery channel (Slack
DM, file, inline) used last.

## Method

1. Read and window the history; report how many entries fall in range before
   drawing conclusions from them.
2. Classify the work: projects and domains, technologies, problem types
   (performance, debugging, feature work, refactoring, setup), and approach
   patterns (methodical, exploratory, trial-and-error).
3. Mine for struggle signals: repeated questions on one topic, problems that
   took multiple attempts, explicit knowledge-gap phrasing, architecture
   decisions taken without conviction.
4. Convert signals into 3-5 improvement areas. Each must be **specific**
   ("advanced TypeScript: generics, utility types, discriminated unions — you
   iterated on union types for connection state"), **evidence-based** (point at
   the entry or project), **actionable**, and **prioritized** by impact.
5. Write the report (template below).
6. Curate 2-3 resources per area from real search results — title, date, link,
   one line on why it addresses *this* gap. Generic "learn TypeScript" links
   are a failure.
7. Deliver: inline first; to Slack only if a connection is available and the
   user asked for it.

## Output template

```markdown
# Developer Growth Report
**Period**: … | **Generated**: …

## Work summary
2-3 paragraphs: projects touched, technologies, overall focus.

## Improvement areas (prioritized)
### 1. <Area>
**Why this matters**: …
**What I observed**: specific evidence from the history
**Recommendation**: concrete step(s)
**Time to skill up**: estimate

## Strengths observed
2-3 bullets, each with the observation that supports it.

## Action items
Priority order, one per area, each runnable this week.

## Curated learning resources
### For: <Area>
1. **<Title>** — <date> — why it fits — <link>
```

## Quality gates for this track

- Every improvement area names the observation it came from; nothing survives
  on plausibility alone
- Areas are 3-5 and ranked; vague ones ("improve coding skills") are rewritten
  or cut
- Resource links come from a search performed in this session, never from memory
- Time estimates are given and plausible
- Strengths are evidenced the same way gaps are
- If the history window is empty or too thin to support conclusions, say so and
  widen the window instead of inventing findings
- Delivery step is skipped cleanly when the channel is not configured
