---
name: course
description: Design and write a full-depth, research-grade curriculum with the user in command of pacing — seven phases (capability definition, outline, critique, rewrite, lesson creation, correction protocol, synthesis) run one prompt at a time, on a "next" pace, with self-sufficiency, evidence tiers, mathematical rigour and one style code enforced throughout. Default 20 lessons; the lesson count is user-specifiable. Every lesson is at least 10,000 words including tables, and carries relevant drawn SVG diagrams. Lessons are formatted to the layout contract in references/formatting.md (real headings, pipe tables, figure-wrapped SVGs, collapsible hint ladders, renderer-safe math) so the result reads beautifully in any destination. Use on "/course" or when the user asks for a course, a curriculum, a lecture series, a syllabus, or full lesson material of research-grade depth — not for a single lesson or a summary document (say so and route back).
---

# Course

A curriculum is built by phases, and each phase's output is the next phase's input. The method was
proven end to end on a 20-lesson research-grade Agentic Engineering course (the prompts in
`references/phase-prompts.md` are that run's prompts, generalized). The user controls the pacing;
the agent never skips, batches or improvises a phase.

## Invocation

`/course [<topic>] [<lesson-count>]` — lesson count defaults to **20**; any larger count is honoured
(never silently smaller). Also accept "more/less"/"N lessons" in prose. If the topic is missing, Phase 1
asks for it. Announce the seven phases and their names once, then start Phase 1. At the start, tell the
user the control surface once: *"One prompt at a time. You advance with 'next'. Corrections apply
mid-course without a restart."*

**Output destination**: settle in Phase 1, never assumed. The default of this workspace is the site
repo `/Users/nyimbiodero/src/pjs/websites/nyimbi.com`, `content/learning/<slug>/NN.md`,
frontmatter `title`+`order` — the agentic-engineering course set the convention. A workspace dir or
plain files are equally valid when the user names them.

## The seven phases

1. **Capability definition.** Start with what the learner should be able to *do*, never with topics.
   15–25 observable capabilities (each an artefact or decision someone else can assess), the 2–4 spine
   questions, 5 mastery criteria as rules, and a 4–6-cluster capability map with prerequisite/terminal
   capabilities. No "understand", no "be familiar with". See Prompt 1.
2. **Outline.** The full skeleton at the requested lesson count: architecture table (part | lessons |
   theme | primary outcome), per-lesson objectives/content/lab/readings with tiers, the mathematical
   prelude specification, capstone tracks (including a replication-and-negative-result track), assessment
   weights, open intellectual questions, the currency caveat, and — every 3–4 lessons — a **recitation
   plan**: 3–4 problems solved aloud in a group (or with the agent as tutor), in peer-instruction form
   (a board question, individual commitment, discussion, re-commitment), with a facilitator script that
   names the common wrong turns in advance. The retrieval schedule of the lesson contract is fixed here
   too, so it is a property of the outline, not a habit. See Prompt 2.
3. **Critique.** A rigorous review of the outline's own output: the spine's evidence base, the gaps, the
   weak sections, the sequencing, the depth, the assessment — every criticism carries a fix, every fix
   states impact, ending in a priority table. Apply the course's own standards to the course. See Prompt 3.
4. **Rewrite.** The v2 outline as a complete document (never a diff), critique incorporated, prelude
   specified, replacements made, every recommendation carrying a revision condition. See Prompt 4.
5. **Lesson creation.** One lesson per "next", each the full pedagogical content in the lesson structure
   (Prompt 5) — never a summary — formatted to the layout contract (`references/formatting.md`), which
   carries the renderer-safe math, table, diagram and callout rules. The prelude comes first.
6. **Correction protocol.** Mid-course: name the drift, state the correction as a applicable rule, apply
   forward only. Completed lessons are not rewritten unless asked. See Prompt 6.
7. **Synthesis.** The consolidated cheat sheet after the last lesson: one table per part
   (Concept | Rule or formula | Use), the mastery criteria and the spine questions at the end. If it
   exceeds ~6,000 words it is a summary, not a cheat sheet; compress. See Prompt 7.

## The invariants (state once per course, assume everywhere)

1. **Self-sufficiency.** Every document stands alone; prior results are restated in the form needed,
   not referenced by number alone.
2. **Evidence discipline.** Every citation carries a tier (A: peer-reviewed or arXiv-indexed; B: vendor
   publication or specification; C: secondary aggregator) and a status (R: independently reproduced;
   S: single-lab, inspectable; P: preprint, unreplicated; C: vendor claim). Vendor and preprint claims
   are hypotheses to test, never results to apply. The course applies this to its own citations.
3. **Rigour.** Definitions before claims; every formal object defined before use; every result proved,
   derived, or explicitly flagged as hypothesis; every formula used at least once in a worked example
   with the arithmetic shown.
4. **Style.** Possessive used sparingly (rewrite "the model's output" → "the output of the model"
   when the possessive earns nothing). Tables for any comparison of three or more. Block quotes for
   concept checks and design principles. "The lesson:" sentence after worked examples and exercises.
   "What good looks like" sections with five properties. Numbered sections, lettered parts. Bold for
   emphasis, not decoration. No credential-label framing — never "post-doctoral" or "post-graduate"
   in a course title or body; "research-grade" carries the claim and does not narrow the readership.
5. **Spine and mastery.** Each lesson traceable to at least one spine question; every claimed
   improvement carries uncertainty estimates and harness controls (adapt the wording to the domain once,
   in Phase 1, and hold it).

## Formatting and layout

A course is read, not just written. Every phase's output — and every lesson in
Phase 5 especially — follows the **layout contract in
`references/formatting.md`**: real headings at fixed levels (never bold-line
pseudo-headings), pipe tables with named axes, figure-wrapped SVG diagrams,
collapsible hint ladders, block-quote callouts, and renderer-safe math
(`$$`/`$` only, `%` escaped, `aligned` not `align*`). The contract is portable
— it holds for any destination, any subject — with a site appendix for
nyimbi.com (frontmatter, `[[prompt:]]` boxes, margin notes, the audit command).
Three moments enforce it: the outline (Phase 2) fixes the diagram palette and
citation shape; the pre-flight checklist in the contract runs on every finished
lesson before it is accepted as done; the smoke test (below) renders lesson 1
through the destination's own build before lesson 2 is written.

## The lesson contract

- **At least 10,000 words per lesson**, tables included in the count. Under 10,000 is a failure of the
  instruction, not a style choice.
- **At least 2 drawn SVG diagrams per lesson** — inline `<svg>` (or `<img src=data:...>`), hand-composed
  for that lesson: a mechanism, a control flow, a decision boundary, a timeline — with real quantities,
  labelled axes and a consistent palette shared across the course. Mermaid is acceptable only for
  conventional flowcharts; anything precise about the domain's own objects is drawn, not mermaid'd.
- **One demonstration per lesson, predict–observe–explain.** Open with the case that surprises: a live
  experiment (lab, simulation or numeric probe the learner runs), the learner states a prediction first,
  the result is then produced, and the discrepancy is explained. The demonstration earns its place only
  if a competent guesser in the domain would get it wrong.
- **Misconception engineering.** Each lesson names 2–4 target misconceptions (the wrong model a capable
  outsider actually holds) in the §N.0 map; each concept check tests a mechanism, and at least one
  exercise per lesson is a **trap** — it passes only if the misconception is gone, and its marking key
  names the belief that failed. A trap that cannot fail for anyone is decoration.
- **The guidance ladder.** Each lesson's body moves from full worked examples → completion problems
  (the learner fills the final step) → faded problems (structure cued, steps missing) → independent
  problems, in that order. Exercises are tiered the same way; hints are a ladder (nudge → mechanism →
  step), published as a collapsible sequence, never the answer with extra words.
- **Retrieval is spaced and cumulative.** Every lesson opens with a retrieval set: 5 questions sampled
  on a fixed schedule (the previous lesson, three lessons back, ten lessons back — or, when N≥15, the
  mid-course spine review). Each lesson exports a flashcard front/back table for a spaced-repetition
  deck. From lesson 4 on the exit test is cumulative — it may not test only the current lesson.
- **Drawing is retrieval too.** One exercise per lesson: reproduce the lesson's central diagram from
  memory, then check it against the SVG. The check verifies the diagram actually encoded.
- **A load-bearing mnemonic per lesson, tested forward.** The densest system in the lesson (a tuple, a
  decision sequence, a naming scheme) carries one structured mnemonic stated in the cheat sheet; the
  next lesson's retrieval set includes recalling the previous mnemonics by their letters or pegs. A
  mnemonic never tested again is decoration and is deleted.
- **Teach-back with calibration.** After the lab: explain the lesson's mechanism aloud to a novice in
  8+ sentences (the teach-back); the sentences that come out vague become the learner's study list.
  Before the exit test, the learner predicts their score; grading reports the prediction beside the
  result. Calibration is trained, not assumed.
- **Every formula carries its limit case.** At first use: a dimensional check, the degenerate case
  evaluated by hand (θ = 0, the ratio at its bound, the input at 0), and one sanity inversion (what
  would have to be true for this to fail?). A formula with no checked limit case is incomplete.
- **The lesson structure** (Prompt 5): header with prerequisites; §N.0 module map and 7–12 observable
  outcomes; 4–5 lettered parts (objects → results → worked example → comparison table → design-principle
  callout, inline cross-references); concept checks with answers naming the mechanism; the lab (task,
  conditions, controls, metrics table, pre-registered hypotheses, acceptance criteria, "What good looks
  like"); the cheat-sheet table; 6–9 numbered exercises with full worked solutions and "The lesson:"
  closers; the exit test (10–20 capabilities, verbatim "without notes").
- **First-lesson smoke test**: before writing the second lesson, render lesson 1 through the
  destination's own build (for the site: `astro build` in the repo — the math gate stops on a broken
  page) and read the rendered page once; fix the lesson conventions on lesson 1, never across 20.
- **Style check between lessons**: the possessive drift, the summary-instead-of-material failure, the
  forward reference, the claim without tier, the table whose axes are not named — scan each finished
  lesson before accepting it as done (Prompt 6's list, applied to yourself) — **plus the formatting
  contract's pre-flight checklist** (`references/formatting.md` §7): pseudo-headings, ASCII tables,
  unbalanced or renderer-unsafe math, unfigure-wrapped diagrams, untagged callouts.

## Anti-failures

- Summarising instead of writing the lesson. The lesson is the content.
- Teaching topics instead of capabilities. Every objective begins with a verb and names the artefact.
- The critique that finds faults without fixes, or the rewrite that is a diff.
- Batching phases because they "would flow". The user's pacing is the design.
- Numbers quoted without arithmetic; citations without tier and status; intellectual questions replaced
  by administrative ones.
- Pedagogical set-dressing: the exercise whose answer was just worked through in the body (near-transfer
  only counts); the trap that cannot fail; the mnemonic nobody retrieves again; the exit test that stops
  at the current lesson; the demonstration a domain expert could not get wrong. Each of these teaches
  fluency in the lesson's own wording and nothing about the domain — which is the illusion the course
  exists to prevent.
- Formatting that fights the renderer: the bold-line pseudo-heading, the ASCII or grid table, the
  `\[`/`\(` delimiter, the unescaped `%` inside math, the diagram pasted without a figure or title, the
  mermaid edge that mixes `-- text -->` with `-->|label|`. The layout contract
  (`references/formatting.md`) exists so none of these is a judgement call.