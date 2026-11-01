# Meeting Insights Analyzer

Purpose: turn a folder of meeting transcripts into behavior patterns with
timestamped evidence and one improvement at a time. This is the
communication/behavior track of `research-and-insight-analysis`.

## When this track applies

The user has transcripts and wants to know how they (or a person they coach)
actually behave: "when do I avoid conflict", "what's my speaking ratio", "how
has my facilitation changed since Q1", "prepare concrete examples for my
performance review".

## Evidence sources

Transcript files (`.txt`, `.md`, `.vtt`, `.srt`, `.docx`) from Granola, Zoom
cloud recording, Google Meet, Fireflies, Otter, or any pasted notes. Before
analyzing, establish: which files are in scope, the date range, whether files
carry speaker labels and timestamps, and how the subject is identified in the
text. Naming files `YYYY-MM-DD - Meeting Name.txt` makes period comparison
possible at all.

Nothing goes in the brief that is not attributable to a quote, a timestamp, or a
counted number.

## Method

1. Inventory the folder: file count, formats, date range, speaker labels
   present, subject identified. Report what is missing before analyzing.
2. Confirm the behaviors in scope. If unspecified, ask — one behavior at a time
   produces far deeper analysis than ten at once.
3. Count and quote in parallel: quantitative rows (speaking share, interruptions
   given/received, question:statement ratio, filler words per minute, turn
   length) come from tallying; qualitative rows (hedging, indirect phrasing,
   subject changes under tension, paraphrasing, building on others' points)
   come from reading for the markers.
4. Attach 2-3 of the strongest examples per pattern: meeting, timestamp, exact
   quote, why it mattered, better approach.
5. Compare periods when more than one window is supplied — deltas, not vibes.
6. Synthesize: patterns ranked by impact, strengths worth keeping, and 3-5 next
   steps the subject can run in their next meeting.

## Analysis lenses

| Lens | Look for |
|---|---|
| Conflict avoidance | "maybe", "kind of", "I think"; indirect requests; subject changes when tension rises; agreement without commitment; obvious problems left unaddressed |
| Speaking ratio | % of meeting speaking, interruptions by/of the subject, average turn length, questions vs. statements |
| Filler | "um", "uh", "like", "you know", "actually" per minute or per turn; situations where frequency rises |
| Active listening | questions referencing a prior point, paraphrase, building on others' contributions, clarifying questions |
| Facilitation | directive vs. collaborative decisions, handling of disagreement, inclusion of quiet participants, agenda and time control, action-item clarity |

## Output template

```markdown
# Meeting Insights Summary
**Analysis period**: … | **Meetings**: N | **Total duration**: …

## Key patterns
### <Pattern>
- **Observed**: what, across how many meetings
- **Impact**: why it matters
- **Evidence**:
  1. **<Meeting>** — <timestamp>
     > "exact quote"
     **Why it matters**: …   **Better approach**: "…"
- **Recommendation**: one concrete change

## Communication strengths
1. Strength + the quote or number that proves it

## Speaking statistics
Speaking time % · questions/meeting · filler per minute · interruptions given/received

## Next steps
3-5 actions, each runnable in the next meeting.
```

## Quality gates for this track

- Every pattern carries at least one verbatim quote with a timestamp, or a
  stated count across a stated number of meetings
- Counts and quotes are separated: a count is not evidence of meaning, a quote
  is not evidence of frequency
- The subject's improvement areas are prioritized; the brief recommends one
  focus at a time
- Period comparisons use the same lenses on both windows
- Private transcript content stays local and is not reproduced beyond the
  quotes needed to make the point
- Strengths are evidenced the same way gaps are — no unbacked praise
