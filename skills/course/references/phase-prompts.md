# The seven phase prompts, generalized

Adapted from the Agentic Engineering course build (20 lessons at 10–12k words, live on nyimbi.com).
Replace bracketed fields; keep the operative structure. The `[DOMAIN]` phrasing in Prompt 1 becomes
the course topic at `/course` invocation.

## Prompt 1 — Capability definition

> **Role.** Help design a research-grade curriculum in [DOMAIN]. The learner starts at
> [PREREQUISITES], and should end [TERMINAL LEVEL] — able to do research-grade work, not just apply
> techniques.
>
> **Deliverables.**
> 1. **The end state.** 15–25 observable capabilities, each starting with a verb (derive, design,
>    compute, diagnose, produce, evaluate, critique). Each corresponds to an artefact or decision
>    someone else can assess. No topic labels, no familiarity claims.
> 2. **The spine.** 2–4 questions that, if answerable for any problem in the domain, prove mastery.
>    The course's every module traces to at least one.
> 3. **The mastery criteria.** 5 rules any claimed improvement must satisfy, stated as rules ("every
>    claimed improvement carries uncertainty estimates and controls"), not aspirations.
> 4. **The capability map.** 4–6 clusters; each names prerequisite and terminal capabilities. Clusters
>    become the parts; terminal capabilities become lesson objectives.
>
> **Constraints.** Testable, cumulative, research-grade. No "understand".
>
> **Output.** End state, spine, mastery criteria, capability map (Markdown).

## Prompt 2 — Outline (for the requested lesson count, default 20)

> **Deliverables.**
> 1. **Architecture table**: *Part | Lessons | Theme | Primary outcome* — parts from the clusters.
> 2. **Lessons** (the exact requested count): number+title, weeks/slot, objectives (3–6, as
>    capabilities), content (key results, techniques, debates), a runnable **lab** with acceptance
>    criteria, **core readings** each tiered A/B/C and statused R/S/P/C — flag single-lab and
>    over-relied-on readings.
> 3. **The prelude** spec: the derivations, results and formal objects the course assumes, fully
>    self-sufficient, closing with an annotated cheat sheet (*Term | Statement | Where used*).
> 4. **The capstone**: 3–4 tracks with weights, including a **replication-and-negative-result track**
>    (pre-registered replication, publishable either way).
> 5. **Assessment weights**, **mastery criteria restated**, **open intellectual questions** (4–6, each
>    with evidence on both sides, no administrative ones), **currency caveat**.
> 5a. **Recitation plans** every 3–4 lessons: 3–4 problems in peer-instruction form (board question,
>    individual commitment, discussion, re-commitment), a facilitator script naming the common wrong
>    turns in advance, and the retrieval schedule each future lesson opens with, stated here once.
>
> **Constraints.** Sequenced prerequisites, runnable labs, classified readings, self-sufficient document.
>
> **Formatting.** Fix here, once, what every later lesson reuses: the diagram palette (paper, ink,
> accent, soft ink — named hex values), the citation shape (`[Author, Year · tier A/R]`), and the
> heading scheme (parts as H2 numbered N.M, subsections H3). See references/formatting.md.
>
> **Output.** Architecture, lessons with all fields, prelude spec, capstone, assessment, criteria,
>    questions, caveat.

## Prompt 3 — Critique

> **Task.** Critique the outline, then propose fixes. Every criticism carries a fix; every fix states
> impact.
>
> **Cover**: the spine (is the evidence base thin — tier-P or single-lab load-bearing citations?); the
> gaps (objectives named but untaught; literature present but outline absent; assumed-but-unestablished
> prerequisites); the weaknesses (unsupported claims, tier-C sourcing, numbers asserted without
> arithmetic); the sequencing (concrete before abstract; violated dependencies; prelude placement); the
> depth (where a formal derivation, worked example, measurement protocol or forcing table is missing);
> the assessment (labs test objectives; acceptance criteria observable; a negative-result path exists).
> Apply the course's own standards to the course.
>
> **Output.** Executive verdict, section-by-section analysis, expansions/extensions/deepenings,
> revised sequencing, priority table (*Priority | Change | Effort | Impact*).

## Prompt 4 — Rewrite

> **Task.** Produce the v2 outline as a complete document (never a diff): structure that survived kept;
> everything the critique identified fixed; the prelude spec at the top, self-sufficient, closing with
> the annotated cheat sheet; the weak sections replaced by the critic's fixes; evidence discipline
> applied to the course's own claims (a tier-P dependency is stated as such); every recommendation
> carrying a revision condition (what observation would change it). Style rules enforced.

## Prompt 5 — Lesson creation (pacing: one lesson per "next")

> **Task.** Write the **full pedagogical content** for lesson N — never a summary, never an outline.
> Fully self-sufficient.
>
> **The lesson structure.**
> 1. **Header**: number, title, weeks/slot, prerequisite lessons and prelude sections, note that prior
>    results are restated in the form needed.
> 1a. **Retrieval open (from lesson 2)**: 5 questions on the fixed schedule — the previous lesson, three
>    lessons back, ten lessons back — plus recall of the previous lesson's mnemonics by their letters or
>    pegs, with answers at the same depth as concept checks.
> 1b. **Demonstration (predict–observe–explain)**: the surprising case stated, the learner's prediction
>    requested explicitly, the result produced (a lab clip, a simulation run, or a numeric probe with its
>    code shown once), the discrepancy explained.
> 2. **§N.0 — Module map and objectives**: the *Part | Content | Lab* table; a paragraph, then 7–12
>    observable outcomes (verbs, artefacts); the 2–4 **target misconceptions** named; the closing
>    "Everything is self-contained..." sentence.
> 3. **Parts A–E** (or as many as truthful): every section in order — objects, results (proof sketch or
>    flag), a **worked example with arithmetic and interpretation**, a **table** where three or more
>    options compare, a design-principle callout where a transferable heuristic emerges, inline
>    cross-references. The guidance ladder runs across the section's exercises: full worked example →
>    completion problem → faded problem → independent problem. Every formula carries its limit case:
>    dimensional check, degenerate case by hand, one sanity inversion. **At least 2 inline SVG
>    diagrams**, drawn for this lesson's own objects with real quantities and labelled axes, consistent
>    with the course's diagram palette. **At least 10,000 words** including tables.
> 4. **Concept checks** after each major section: block-quoted question + full answer naming the
>    mechanism, not the definition. Answerable from the section alone.
> 5. **Evidence discipline**: every citation tiered and statused; vendor/preprint claims marked as
>    hypotheses; every number either reproduced in the module's own arithmetic or flagged unreproduced.
> 6. **The lab**: task, conditions, held-fixed controls, metrics table, pre-registered hypotheses
>    H1–H5, acceptance-criteria table, "What good looks like" with five properties; then the
>    **teach-back** (explain the mechanism to a novice in 8+ sentences; vague sentences become the study
>    list) and **calibration** (predict the exit-test score; the report shows prediction beside result).
> 7. **The cheat sheet**: one table — *Term | Statement | Role in this lesson and in the course* —
>    covering every term introduced and every term used from earlier, including the lesson's
>    **mnemonic** and its pegs, and the flashcard front/back table for the spaced-repetition deck.
> 8. **Exercises and solutions**: 8–10 in the three tiers (guided / faded / independent, the last two at
>    least half the set), `E N.M` / `S N.M`, numerical or diagnostic (never recall), arithmetic shown,
>    each closing with "The lesson:". At least one is a **trap** keyed to a named misconception; one is
>    **redraw the diagram from memory** against the lesson's SVG; hint ladders (nudge → mechanism →
>    step) publish under each, never the answer restated.
> 9. **Exit test (cumulative from lesson 4)**: "You are ready for lesson N+1 when you can, without
>    notes:" — 10–20 capabilities, at least a third drawn from earlier lessons.
>
> **Style.** No code in the body (pseudocode only where precision demands); every formula used in a
> worked example; no forward references; no claim without tier. Possessive sparingly; tables for
> comparisons; block quotes for concept checks and design principles.
>
> **Formatting.** The lesson follows references/formatting.md end to end: real headings (parts H2
> numbered `N.M`, subsections H3, nothing deeper than H4, no bold-line pseudo-headings); pipe tables
> with named axes; every diagram figure-wrapped SVG with `<title>` and caption, or a
> strictly-syntaxed mermaid flowchart; math as `$…$`/`$$…$$` only (`%` escaped, `aligned` not
> `align*`); hint ladders as one `<details>` rung per hint. Before the lesson is accepted as done,
> run the contract's pre-flight checklist (§7) against it.

## Prompt 6 — Correction protocol (applied mid-course on drift)

> 1. Name the drift precisely ("the text is littered with possessives").
> 2. State the correction as a rule the agent applies ("prefer 'the output of the model' over 'the
>    model's output' when the possessive earns nothing").
> 3. Apply forward only; completed lessons are not rewritten unless asked.
> 4. Check the next lesson against the correction; repeat with an example only if it fails again.
>
> **Watch list**: the possessive drift; the summary-instead-of-material failure; a forward reference to
> an undefined term; a claim without its evidence tier; the comparison table whose axes are unnamed; the
> concept check whose answer restates the definition; the lab with unobservable acceptance criteria; the
> exercise that tests recall; **the formatting drifts** — the bold-line pseudo-heading, the ASCII or
> grid table, the `\[`/`\(` math delimiter, the unescaped `%` inside math, the diagram pasted without
> a figure or title, the mermaid edge that mixes `-- text -->` with `-->|label|` (see
> references/formatting.md §5–§7).

## Prompt 7 — Synthesis (after the last lesson)

> One consolidated cheat sheet, readable in one sitting: one table per part (*Concept | Rule or formula
> | Use*), no prose, no examples (the arithmetic stayed in the lessons), closing with the mastery
> criteria and the spine questions. Over ~6,000 words means it is a summary, not a cheat sheet; compress.