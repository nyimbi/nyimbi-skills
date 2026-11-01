---
name: writing-and-internal-communications
description: >-
  Draft, structure, and polish written communications people actually act on:
  internal status reports, leadership updates, 3P updates, company newsletters,
  FAQs, incident notes, project updates, documentation, proposals, specs,
  decision docs, research-backed articles with citations, changelogs and release
  notes from git history, and resumes tailored to a job description. Use when the
  user says "write a status report", "draft a leadership update", "put together a
  3P update", "write the company newsletter", "write this doc / proposal / spec /
  RFC", "add citations and strengthen the hook", "generate release notes from
  commits", "tailor my resume to this job", or asks for structure, editing,
  proofreading, or audience advice on a draft. This skill owns the process —
  context intake, audience and purpose, structure, draft, evidence and claims
  check, format-specific polish — plus the internal-comms format catalogue. Do
  not use for producing the office file itself: word-document-authoring for .docx,
  presentation-authoring for decks, spreadsheet-authoring for workbooks; not for
  the stakeholder narrative once a fact base exists
  (executive-communication-and-alignment), nor for gathering market, competitor,
  or user evidence (research-and-insight-analysis).
license: Apache-2.0
---

# Writing and Internal Communications

This skill owns **what to say and how to structure it**. It does not own how the
deliverable looks (`visual-design-and-branding`), which office container it ships in
(`word-document-authoring`, `presentation-authoring`), or how the underlying evidence
was gathered (`research-and-insight-analysis`).

Two things merge here and they are complementary, not competing:

- **The process** — a co-authoring workflow: context intake → audience + purpose →
  structure → draft → evidence/claims check → format-specific polish → quality gate.
- **The format catalogue** — what a 3P update, newsletter, FAQ, status report, incident
  note, changelog, or tailored resume is actually supposed to contain. The process picks
  up any format; the catalogue supplies the ones used every week.

The quality bar ends with a reflection gate: two or three specific follow-up questions
tied to something concrete in the draft, appended after the deliverable and easy to
skip. It is a check on *your* output, not homework for the user.

## When to use

- Internal comms: status reports, leadership updates, 3P (Progress/Plans/Problems)
  updates, company newsletters, FAQ responses, incident reports, project updates
- Structured documents: "write this doc", "draft a proposal", "create a spec", PRD,
  design doc, decision doc, RFC, write-up
- Research-backed writing: articles, thought leadership, tutorials, case studies that
  need citations, sources, and a hook that earns the first line
- Release communication: "generate release notes from commits", changelog entries,
  app-store update text, weekly product update summaries
- Applications: "tailor my resume to this job", resume versions per role, ATS
  optimisation, career-transition rewrites
- Editing and review: restructure a draft, tighten for an audience, cut filler, fix
  flow, improve an introduction

**Do not use for** — `word-document-authoring`, `presentation-authoring`, or
`spreadsheet-authoring` when the ask is to *produce or edit the office file* itself:
this skill gives you the content, structure, and wording, those skills give you the
`.docx`/`.pptx`/`.xlsx`. `executive-communication-and-alignment` when a fact base
already exists and the missing piece is stakeholder narrative, decision routing, or
getting alignment — not the drafting craft. `research-and-insight-analysis` when the
job is to go gather market, competitor, or user evidence rather than to write it up.

- Technical documentation (READMEs, API docs, architecture docs, runbooks, onboarding guides) — use the **documentation** skill; this skill serves people-facing communications.

## Workflow

1. **Intake context before writing a word.** Ask the meta questions — document type,
   primary audience and what they already know, desired impact after reading, template
   or house style, constraints (length, deadline, what must not be said) — then invite
   a free-form dump: background, rejected alternatives, team dynamics, timeline
   pressure, stakeholder worries. Pull from linked docs or threads only with
   permission. Follow with 5–10 numbered clarifying questions aimed at real gaps;
   shorthand answers are fine. Exit condition: you can probe edge cases without the
   basics being explained again. Detail:
   [coauthoring-workflow.md](references/coauthoring-workflow.md).

2. **Fix audience, purpose, and format.** Write one line each: *who reads this*, *what
   they should do or understand afterwards*, *which format carries it*. Then select the
   format from the catalogue below — if none fits, ask rather than inventing a
   structure. Format choice determines section order, length, tense, and how much
   context the reader is assumed to have.

3. **Structure before prose.** Propose the section list (3–5 sections if the reader
   hasn't specified one), start with the section carrying the most unknowns — the core
   decision for a decision doc, the technical approach for a spec — and leave the
   summary for last. Scaffold the file with headers and `[To be written]` placeholders.
   For each section: clarify → brainstorm 5–20 candidate points → let the user curate
   ("keep 1,4,7 / remove 3 / combine 11 and 12") → gap check → draft → surgical edits.
   Never reprint the whole document for an edit. After three rounds with no
   substantial change, ask what can be cut. Near completion, re-read the whole draft
   for flow, redundancy, and filler.

4. **Draft with evidence where the format demands it.**
   - *Claims-bearing writing* — outline first, mark `[needs source]` on every
     unsourced claim, extract research with citations attached at the moment of
     extraction, and strengthen the hook with three named alternatives. Style and
     templates: [research-citations-and-hooks.md](references/research-citations-and-hooks.md).
   - *Release notes* — establish the range, categorize commits, translate technical →
     user language, drop internal work. Commands and taxonomy:
     [release-notes-changelog.md](references/release-notes-changelog.md).
   - *Resume* — treat the job description as the spec, tier its requirements, map
     real experience to each, and build against ATS constraints:
     [tailored-resume.md](references/tailored-resume.md).
   - *Internal comms* — load the matching format file from the catalogue in step 2.

5. **Run the evidence and claims check.** Every figure carries value, unit, time
   period, and source. Facts, inferences, and assumptions are visibly separated;
   assumptions are labelled, never dressed as findings. Changelog bullets trace to a
   commit in the range. Resume bullets are substantiable in an interview. Citations are
   verified against the original, not a secondary mention. Anything unverifiable is
   marked as such or cut — plausible-sounding filler is the failure this step exists to
   prevent.

6. **Polish for the format, not in the abstract.** Apply the catalogue's length, tone,
   section, and tense rules; read the piece in the reader's shoes once; cut every
   sentence that does not carry weight; check the opening line does work; confirm
   links resolve and names are right. Voice preservation is a hard rule: suggest,
   don't replace — the user's version wins ties.

7. **Reader test.** Predict 5–10 questions a real reader would ask, then run them
   against a *clean* reader — sub-agent, fresh conversation, or the user in a new chat
   — given only the document. Ask what is ambiguous, what knowledge it wrongly assumes,
   and what contradicts. Fix what failed and re-run only those questions. Exit when the
   clean reader answers correctly and surfaces no new gaps. Protocol:
   [coauthoring-workflow.md](references/coauthoring-workflow.md).

8. **Quality gate, then deliver.** Walk the Quality bar below. Where the draft makes
   claims, estimates, or recommendations the user will act on, append two or three
   follow-up questions that each point at a specific figure, reasoning step, or
   assumption — after the deliverable, under the exact lead-in, and only once:
   [quality-gate.md](references/quality-gate.md). Skip it when the user already asked
   you to verify, supplied the material, asked for the quick version, or when the work
   is creative writing with nothing to check.

## Quality bar

- [ ] Audience, purpose, and format are stated explicitly before drafting begins
- [ ] Structure was agreed (or proposed and accepted) before prose was written
- [ ] Every number has value, unit, time period, and source — or is labelled an
      assumption
- [ ] Facts, inferences, and assumptions are distinguishable on the page
- [ ] Format spec met: length, section set, tense, and tone match the catalogue entry
- [ ] Voice preserved — the user's phrasing survives where they had a preference; no
      generic filler, no invented detail
- [ ] Claims trace to evidence: commit, citation, or the user's own supplied material
- [ ] Reader test run and failures fixed, or explicitly skipped with a stated reason
- [ ] Opening line earns attention and the last line says what happens next
- [ ] Where applicable, the two-or-three-question quality gate is appended in the exact
      format, and nothing follows it

### Failure modes

- **Process theatre** — running the section loop on a five-line status update
- **Template dump** — the format's skeleton delivered with no content decisions
- **Hedging everything** — "may, might, could" until the recommendation disappears;
  label the assumption instead of burying the verb
- **Citation theatre** — a reference list that does not support the claims beside it
- **Bulk reprinting** — pasting the whole document back instead of surgical edits
- **Resume embellishment** — a bullet the interview could not substantiate
- **Jargon leak** — commit subjects and internal component names in customer-facing
  release notes
- **Gate as nagging** — generic prompts, repeats across turns, or prompts after the
  user already asked for verification

## Reference map

| Situation | Open |
|---|---|
| Context intake, section loop, reader-testing protocol | [references/coauthoring-workflow.md](references/coauthoring-workflow.md) |
| Outline, research extraction, citation styles, hooks, section feedback | [references/research-citations-and-hooks.md](references/research-citations-and-hooks.md) |
| Final reflection gate: when it applies, prompt writing, exact format | [references/quality-gate.md](references/quality-gate.md) |
| Git history → user-facing release notes | [references/release-notes-changelog.md](references/release-notes-changelog.md) |
| Job description → tailored, ATS-safe resume | [references/tailored-resume.md](references/tailored-resume.md) |
| 3P (Progress/Plans/Problems) team update | [references/format-3p-updates.md](references/format-3p-updates.md) |
| Company-wide newsletter for Slack/email | [references/format-company-newsletter.md](references/format-company-newsletter.md) |
| Company FAQ collection and answers | [references/format-faq-answers.md](references/format-faq-answers.md) |
| Everything else internal: status reports, leadership updates, incident notes | [references/format-general-comms.md](references/format-general-comms.md) |

## Output format

Deliver the document itself — never a description of it. Around it, a short delivery
note:

```markdown
# <Title> — delivery note
AUDIENCE:   [who reads this and what they already know]
PURPOSE:    [what they should understand, decide, or do after reading]
FORMAT:     [catalogue entry or "custom — structure below"]
STRUCTURE:  [section list, one line each]
ASSUMPTIONS:[anything assumed because context was missing]
```

Then the draft, with citations inline in the chosen style. Format-specific shells:

| Format | Shell |
|---|---|
| 3P update | `Progress:` / `Plans:` / `Problems:` — 30–60 seconds' reading, team name confirmed |
| Newsletter | 20–25 bullets grouped into 3–4 clusters, `we` tense, links to primary sources |
| FAQ | `*Question*: …` / `*Answer*: 1–2 sentences`, sourced to official comms, uncertainty flagged |
| Status / leadership / incident | audience → headline → detail → blockers → asks, most important first |
| Changelog | `New / Improved / Fixed / Breaking`, one user-facing line per change |
| Resume | header → summary → skills → experience → education, plus the four analyses |
| Long-form doc | delivery note → executive summary → sections → risks/next actions → appendices |

If the format does not fit one of these rows, define the shell in the delivery note
before drafting so the user can correct the structure cheaply.
