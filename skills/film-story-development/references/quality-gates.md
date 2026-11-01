# Story and Character Quality Gates

No pipeline guarantees "highest quality". Quality is comparative, audience-dependent and
finally a human judgement. What a pipeline can do is **raise the floor**: define what good
looks like, make defects visible with evidence, force independent readings, and refuse to
lock a draft that fails a hard check.

The rule: **the model drafts and diagnoses; a human decides.**

---

## 1. The rubric

Score each dimension 0–4. Target **average ≥ 3.0, no dimension ≤ 2** at script lock.

| # | Dimension | 0 | 2 | 4 |
|---|---|---|---|---|
| 1 | **Premise and dramatic question** | no question, no stakes | clear but familiar | specific, ironic, visual, unanswered until the end |
| 2 | **Causal structure** | episodic; things just happen | mostly causal, some coincidence | every major turn caused by a prior choice; "therefore / but", never "and then" |
| 3 | **Character** | types with labels | wants and obstacles, thin inner life | want, need, wound, false belief, contradiction, and a change visible in behavior |
| 4 | **Agency** | events happen to the lead | lead acts in the climax only | the protagonist's choices cause the major turns; the antagonist has a coherent, defensible want |
| 5 | **Scene craft** | scenes deliver information | goal and conflict, weak turns | every scene has goal, conflict, turn, and a changed exit condition; enter late, leave early |
| 6 | **Dialogue** | on-the-nose, interchangeable | functional, some subtext | negotiation with subtext; each principal identifiable blind; speakable; silence used |
| 7 | **Theme and emotional arc** | stated in dialogue | present but illustrated | tested by the plot; the ending answers the opening image; the emotion is earned by consequence |
| 8 | **Originality and feasibility** | derivative or unshootable | familiar shape, producible | a specific angle on a known form; producible with the cast, locations and generation limits |

Evidence, not vibes: every score below 3 must cite a scene or line, and every note must
propose a fix.

---

## 2. Hard checks (binary; any failure blocks lock)

- [ ] Logline names protagonist, goal, obstacle and stakes in one sentence.
- [ ] The dramatic question is answerable yes/no and the ending answers it.
- [ ] Every principal has want, need, wound, false belief and an arc.
- [ ] Every scene has a goal, conflict, turn and changed exit.
- [ ] Every setup has a payoff; every payoff has a setup.
- [ ] No two scenes turn on the same value.
- [ ] Runtime is within 10% of target.
- [ ] Every lead is identifiable from dialogue alone in a blind read.
- [ ] No unfilmable interior states in action lines ("she remembers", "he realizes").
- [ ] No major turn relies on coincidence or a character acting out of character.
- [ ] The final image answers the opening image, changed.
- [ ] AI-risk scenes are rewritten or accepted with a named fallback.
- [ ] A human has signed the premise, script and design gates.

---

## 3. Diagnostic questions

Ask these of the draft, and require scene/line citations. A single model answering "is it
good?" produces flattery; these questions produce evidence.

1. What does the protagonist want in the first five minutes, and what do they need? Cite
   the scenes that show each.
2. Name the choice that turns Act I. Why could they not make the opposite choice?
3. What is the midpoint reversal, and what does it change besides intensity?
4. Which scene could be deleted without changing the story? If one exists, cut or merge it.
5. Where is the theme stated aloud? Replace it with an action or an object.
6. Which line would each principal never say, and why? Where does the script make them say
   it anyway?
7. What does the antagonist want, and why is it reasonable to them?
8. Where does the story rely on coincidence? Replace it with a choice and a consequence.
9. What does the audience know at the end that they did not know at the start?
10. What is the final image, and how does it answer the opening image?
11. Which relationship changes the most, and which scene makes the change visible?
12. What is the story about when the plot is removed?

---

## 4. Three independent readers plus a hostile producer

Run these in **separate contexts**. Do not let the drafting model grade its own draft; it
prefers its own style and misses its own habits.

| Role | Brief | Output |
|---|---|---|
| **Structural editor** | causality, turns, midpoint, pacing, setup/payoff | top 5 structural defects, each with scene citation and a proposed cut/merge/reorder |
| **Character auditor** | want/need/wound, agency, contradiction, voice, arc | per principal: what is legible, what is missing, the line that proves it |
| **Audience proxy** | genre promise, attention, confusion, emotional response | where attention drops, what is predicted, what is unclear, what is felt at the end |
| **Hostile producer** | "why should I fund this?" | the three weakest points, the comps, the commercial/creative risk |

Synthesis rule: fix the **top three structural issues**, not every note. A note that appears
in only one reader and is cosmetic is deferred. A hard-check failure is fixed regardless.

---

## 5. Blind read and table read

**Blind read.** Give the script to someone who has not seen the outline or the pitch. Ask
them to mark, page by page:

- where they were bored;
- where they were confused;
- what they expected to happen next;
- what they felt at the end;
- the one line they remember.

Do not explain the script first. Confusion in a blind read is a script problem, not a reader
problem.

**Table read.** Assign a distinct TTS voice per principal (`film-design` casting sheet),
read aloud, and time it. Then:

- Cut 20–30%. First drafts run long.
- Mark lines that are hard to say; rewrite them.
- Mark scenes where two voices sound the same; differentiate or merge.
- Mark every place the reader laughs at a line meant seriously, or is bored by a line meant
  to thrill.

---

## 6. Revision protocol

1. List defects by evidence: scene, line, dimension.
2. Fix structural causes before cosmetic symptoms. A weak scene is usually a missing
   choice, not a missing adjective.
3. Change one structural variable at a time (a turn, a relationship, an ending) and re-run
   the hard checks. Do not rewrite the whole draft from a pile of notes.
4. Keep a revision log: what changed, why, which diagnostic prompted it.
5. Compare drafts blind: read the old and new versions without labels; keep the better
   scene, not the newer one.
6. Re-run `storycheck.py` and the three readers after every structural revision.
7. Lock only when the rubric average is ≥ 3.0, no dimension ≤ 2, all hard checks pass, and a
   human signs.

---

## 7. Using local models without fooling yourself

- Draft with a strong local model at 4-bit (`qwen3.8-27b-4bit` or `qwen3.6-35b-ud`), but do
  not ask it to certify quality.
- Use **separate contexts** for drafting and critique. A model asked to grade its own draft
  in the same conversation grades its own style.
- Ask for **evidence** (scene/line citations), not adjectives.
- Run two or three critic passes with different briefs; aggregate only repeated or
  structural findings.
- Use the `humanizer` skill on prose passes, then read aloud. AI tells survive silent
  reading.
- Treat an LLM "8/10" as noise. Treat a cited structural defect as a signal.
- The final gate is human taste. The pipeline's job is to make the human's reading
  informed, not to replace it.

---

## 8. Red flags

| Red flag | What it usually means |
|---|---|
| Theme stated in dialogue | the plot does not test it |
| Protagonist reacts for two acts | no agency; rewrite the choices |
| Every scene ends where the next begins | no turns; scenes are transport |
| Two characters sound alike | one voice is the author's, not the character's |
| Coincidence resolves a turn | the story is not causal |
| The ending explains the meaning | the image is not doing the work |
| A scene exists to deliver information | convert to action, insert, or cut |
| The draft is long but nothing is cuttable | scenes are repeating a turn |
| Notes are all cosmetic | the structural problem has not been named |
| The model says it is excellent | it is agreeing with you |

---

## 9. Score sheet

```markdown
# Quality Report — <title>

Draft: vN   Date: YYYY-MM-DD   Reader(s): ...

| Dimension | Score (0–4) | Evidence (scene/line) | Fix |
|---|---:|---|---|
| Premise | | | |
| Structure | | | |
| Character | | | |
| Agency | | | |
| Scene craft | | | |
| Dialogue | | | |
| Theme / emotion | | | |
| Originality / feasibility | | | |
| **Average** | | | |

Hard checks: N/13 pass. Failures: ...

Top three structural fixes:
1.
2.
3.

Human sign-off: name, date, decision.
```
