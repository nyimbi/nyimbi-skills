# The Nine Stages

The backbone is adapted from the AI Film Challenge pipeline (Develop → Design → Plan →
Generate → Assemble → Sound → Finish → Deliver → Document); the artifacts and gates here
are specific to this bundle.

## 1. Develop

**Question:** what film are we making?
**Do:** logline, premise, character spine, structure, beats, scene cards, screenplay,
table read, AI-feasibility pass, series bible.
**Write:** `01_story/logline.md`, `premise.md`, `characters/`, `beats.md`,
`scene-cards.csv`, `setup-payoff.csv`, `screenplay.fountain`, `table-read.md`,
`quality-report.md`, `series-bible.md`, `LOCK.md`.
**Exit:** premise and script approved; runtime within 10%; feasibility risks resolved or
accepted.

## 2. Design

**Question:** what does it look and sound like, and who are these people?
**Do:** design brief, style lock, world bible, locations and floor plans, props,
character packs (character-design), voice casting, continuity system.
**Write:** `02_design/design-brief.md`, `style-lock.md`, `world-bible.md`,
`characters/`, `refs/`, `floorplans/`, `voice-casting.md`, `continuity-system.md`,
`LOCK.md`.
**Exit:** design approved; every principal has a pack and a passed drift audit; every
location has an establishing frame, reverse, and floor plan.

## 3. Plan

**Question:** what exactly do we shoot, in what order, for how much?
**Do:** scene breakdown, blocking, shot list, coverage, keyframe strategy, storyboards,
animatic, sound plan, edit plan, risk register, budget.
**Write:** `03_plan/scene-breakdown.csv`, `shots.json`, `shot-list.csv`,
`storyboards/`, `animatic.mp4`, `sound-plan.md`, `production-plan.md`, `budget.csv`,
`risk-register.md`, `LOCK.md`.
**Exit:** shot-plan approved; every shot has the five production fields plus duration,
purpose, audio, model, and refs; runtime has 10% headroom; animatic timing locked.

## 4. Prepare

**Question:** can this be generated, by which model, at what cost?
**Do:** probe providers, freeze model versions, generate and approve hero keyframes,
compile prompts per dialect, reserve budget.
**Write:** `state.json` capability block, `04_gen/keyframes/`, `04_gen/prompts/`,
`04_gen/prompt.json` per shot.
**Exit:** every shot has an approved keyframe (or a documented reason it does not);
budget cap approved.

## 5. Generate

**Question:** does each take serve the shot?
**Do:** batch variants, score identity/continuity/artifacts, retake with one variable,
log everything.
**Write:** `04_gen/shots/<id>/{v*.mp4,prompt.json,approved.mp4}`,
`generation-log.csv`, `continuity-failures.md`.
**Exit:** every shot has an approved take; hard checks pass; cost within cap.

## 6. Assemble

**Question:** does the film cut together?
**Do:** conform, normalize, rough cut, J/L cuts, reactions, transitions, picture lock.
**Write:** `05_post/rough-cut.mp4`, `05_post/edit/`, `05_post/picture-lock.mp4`.
**Exit:** picture lock approved.

## 7. Sound

**Question:** does it sound like a place with people in it?
**Do:** dialogue, ADR, ambience, Foley, effects, score, mix, stems.
**Write:** `05_post/sound/{dialogue,ambience,foley,score,mix}.wav`, stems.
**Exit:** mix approved; loudness measured.

## 8. Finish

**Question:** does it meet the spec?
**Do:** grade, grain, upscale, titles, captions, AI disclosure.
**Write:** `05_post/deliver/`, `captions.srt`.
**Exit:** technical, continuity, artifact, and legal QC pass.

## 9. Deliver

**Question:** can it ship and can it be re-made?
**Do:** masters per aspect and resolution, cut-downs, manifest, checksums, archive,
process notes.
**Write:** `05_post/deliver/*`, `delivery-manifest.md`, `process-notes.md`.
**Exit:** every file plays; manifest complete; archive stored.

## Re-entry

| Failure | Return to |
|---|---|
| A shot cannot be generated at any quality | 3 (redesign the shot) |
| Identity drifts across a scene | 2 (reference set) or 4 (keyframes) |
| The cut does not work | 3 (shot plan) or 6 (edit) |
| The story does not work | 1 |
| Sound cannot save a scene | 3 or 1 |

## Parallel track — key art

Poster and key art do not sit in the nine-stage sequence. Concept begins at the design
gate; final type and credits begin at picture lock; files are checked at delivery.

| Point | Artifact | Owner |
|---|---|---|
| Design lock | `06_marketing/poster/brief.md`, concept art | `film-poster` |
| Picture lock | title treatment, credits, rating, release | `film-poster` |
| Delivery | one-sheet, thumbnail, social variants, manifest | `film-poster` → `film-postproduction` |
