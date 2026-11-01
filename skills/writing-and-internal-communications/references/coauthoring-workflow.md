# Co-authoring Workflow — Context, Section Loop, Reader Test

Deep detail for steps 1, 3, and 7 of the [SKILL.md](../SKILL.md) workflow. This is the
*process* half of the skill; the format catalogue is the *content* half.

## Stage 1 — Context transfer

Goal: close the gap between what the user knows and what you know, so later guidance is
smart instead of generic.

**Meta questions first** (answer in shorthand is fine):

1. What type of document is this — spec, decision doc, proposal, RFC, update, post?
2. Who is the primary audience, and what do they already know?
3. What should happen after someone reads it? (decision, alignment, action, awareness)
4. Is there a template, house style, or prior example to follow?
5. What constraints matter — length, deadline, politics, what must NOT be said?

**Then invite an unstructured dump.** Background, rejected alternatives, team dynamics,
past incidents, timeline pressure, architecture, stakeholder worries. Tell them not to
organize it. Sources for the dump: pasted text, linked docs, threads, integrations
(Slack/Drive/SharePoint) if available — ask before searching anything.

**Then clarifying questions.** Generate 5–10 *numbered* questions aimed at real gaps,
not a re-ask of what was already answered. Tell the user they can answer "1: yes, 2: see
#channel, 3: no — backwards compat".

**Exit condition:** you can ask about edge cases and trade-offs without needing the
basics explained. If you can't, you are not done — but do not let gaps accumulate;
raise each one as it appears.

## Stage 2 — Structure and the section loop

1. **Agree the structure first.** Propose 3–5 sections for the doc type if the user
   doesn't know what they need. Start with the section carrying the most unknowns —
   the core decision for a decision doc, the technical approach for a spec. Leave the
   summary/executive overview until last.
2. **Scaffold with placeholders.** Create the file with all headers and
   `[To be written]` bodies before drafting anything. Both parties work from one
   scaffold; never brainstorm in a separate document.
3. **Per section:**
   - *Clarify* — 5–10 questions about what belongs in this section.
   - *Brainstorm* — 5–20 numbered candidate points, complexity-scaled. Surface context
     the user shared earlier but may have forgotten.
   - *Curate* — user replies "keep 1,4,7 / remove 3 (dupes 1) / combine 11 and 12".
     Freeform feedback ("looks good but…") is parsed the same way.
   - *Gap check* — anything important missing for this section?
   - *Draft* — replace the placeholder with real prose.
   - *Refine* — surgical edits only. Never reprint the whole document; ask the user to
     *say* what to change rather than editing directly, so preferences carry to later
     sections.
4. **Stop iterating a section** after three rounds with no substantial change. Then ask
   once: what can be removed without losing information?
5. **Coherence read at ~80%.** Re-read the whole document for flow, redundancy,
   contradictions, and filler — every sentence should carry weight.

## Stage 3 — Reader test

Purpose: catch blind spots that make sense to the author and to you (shared context
bleed) but not to a reader.

1. **Predict 5–10 questions** a real reader would ask to find or evaluate this document.
2. **Run them against a clean reader** — a sub-agent, a fresh conversation, or the user
   in an incognito chat — given only the document, no conversation history.
3. **Extra checks:** What is ambiguous? What knowledge does the doc assume? Any internal
   contradictions? What would a hostile reader exploit?
4. **Fix and re-run** only the questions that failed.

**Exit condition:** the clean reader answers correctly and surfaces no new gaps.

## Handling deviations

- User wants to skip a stage → offer freeform instead, don't force the process.
- User is frustrated → acknowledge, then offer the fast path (structure agreed → single
  full draft → one review pass).
- Missing context on something mentioned → ask immediately, don't bank a list of
  questions for later.
