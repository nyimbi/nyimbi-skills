---
name: film-production
description: >-
  Run a film or series end to end from a rough outline: develop the premise into a
  screenplay and series bible, lock characters, world and visual style, build the shot
  list, storyboards and animatic, generate shots on local or cloud models, edit, sound,
  finish, QC and deliver. Use when the user says "make a movie", "turn this idea into a
  film", "create a series", "produce this script end to end", "I have an outline, make
  the whole thing", or asks for the full production pipeline rather than one clip or one
  prompt. Routes the work to film-story-development, film-design, film-directing,
  film-generation and film-postproduction, and holds the project state, continuity ledger,
  approval gates, budget and resume logic across all of them. Do not use for editing
  footage the user already has (see video-use), for a single generated clip (see
  cinematic-pipeline or ai-video-directing), or for writing one prompt (see
  ai-video-directing).
---

# Film Production

The producer's desk for the `film-*` family: it decides what is being made, in what
order, at what quality, for how much, and whether the last stage is good enough to
unlock the next one. Every other film skill does one job; this one runs the job.

## What "whole film" means here

A **finished, watchable master** — picture, dialogue, sound, music, titles, captions,
delivery files — produced from a rough outline through a documented pipeline. It does
not mean one model renders ninety minutes in a single call. No current model does that.
The film is built from shots, the shots from keyframes, and the keyframes from a locked
design. This skill keeps those layers honest.

State the format and runtime before promising anything. A 10-minute short is an
overnight job on this machine; a 90-minute feature is a multi-day generation campaign
with a real budget. See `references/feasibility.md` for the arithmetic.

## The pipeline

Nine stages, five creative approvals. Stages are sequential; within a stage the work
can be parallel (batch by location or character). Each stage writes artifacts the next
stage reads.

| # | Stage | Skill | Writes | Gate to pass |
|---|---|---|---|---|
| 1 | Develop | `film-story-development` | logline, beats, scene cards, screenplay, series bible | premise + script lock |
| 2 | Design | `film-design` | style lock, character bibles, refs, world bible, voice casting | design lock |
| 3 | Plan | `film-directing` | shot list, blocking, storyboards, animatic, sound plan | shot-plan lock |
| 4 | Prepare | `film-generation` | provider choice, keyframes, compiled prompts, budget | keyframe approval |
| 5 | Generate | `film-generation` | approved takes, generation log, continuity failures | shot acceptance |
| 6 | Assemble | `film-postproduction` | rough cut, picture lock | picture lock |
| 7 | Sound | `film-postproduction` | dialogue, ambience, foley, score, mix | mix approval |
| 8 | Finish | `film-postproduction` | grade, titles, captions, masters | QC pass |
| 9 | Deliver | `film-postproduction` | delivery manifest, archive, process notes | delivery |

Stages may be re-entered. A failed shot returns to 4 or 5; a failed cut returns to 3.
Do not skip 2 or 3 to "save time": every unapproved design or shot decision becomes a
paid regeneration later.

### Key-art track (parallel)

Poster and key art are not a sequential stage. They run alongside production:

| Point | Work | Skill | Gate |
|---|---|---|---|
| Design lock | concept routes, art with type-safe negative space | `film-poster` | concept approved with the look |
| Picture lock | title treatment, credits, rating, release | `film-poster` | final art approved |
| Delivery | one-sheet, thumbnail, vertical, square, manifest | `film-poster` → `film-postproduction` | files checked in QC |

Start the concept at design lock so the poster uses the same style and hero frames as the
film. Finalize after picture lock, when the title and credits stop moving.

## Formats and tiers

| Format | Runtime | Shot budget at 4 s | Default tier |
|---|---:|---:|---|
| Vertical micro-drama episode | 60–180 s | 15–45 | local |
| Short film | 5–15 min | 75–225 | local, cloud for heroes |
| Series episode | 5–10 min | 75–150 | local + selective cloud |
| Feature | 80–120 min | 1,200–1,800 | hybrid: animatic, stock, 2D, selective generation |
| Trailer / teaser | 60–120 s | 15–30 | cloud or local |

**Tiers.** `local` = ComfyUI/MLX on this Mac (LTX-2.3, Wan 2.2, MiniMax H3, F5-TTS,
MusicGen). `standard` = paid cloud models for hero shots, local for coverage.
`premium` = cloud-first, highest-quality model per shot, budget-cap required.

## Intake

Infer what you can; ask at most two questions, and only where a wrong guess wastes hours:

1. **Story** — the rough outline, or permission to develop one from a premise.
2. **Format and runtime** — short, episode, feature, vertical, trailer.
3. **Register** — live-action realism, painterly 2D/2.5D, animation, documentary.
4. **Hard constraints** — cast size, locations, language, rating, aspect, deadline, budget.
5. **Existing assets** — script, references, footage, voices, music.

If runtime is unspecified, default to a 5–8 minute short and say so. If the user asks for
a feature on a local-only budget, say what that costs in days and quality before starting.

## Project scaffold

Every project is one directory. `filmctl.py new` creates it; the layout is owned by
`references/project-layout.md`.

```text
<slug>/
  PRODUCTION.md          board: what is being made, stage, approvals, links
  state.json             machine state: stage status, approvals, model versions, budget
  decision-log.md        every irreversible choice with the reason
  continuity-ledger.md   characters, locations, props, wardrobe states, knowledge states
  01_story/              02_design/   03_plan/   04_gen/   05_post/
```

Rules:

- **Never overwrite an approved artifact.** Add `_v2`, or a dated copy, and record it.
- **Scene and shot numbers freeze at the shot-plan gate.** After generation starts, new
  shots append (`S03_SH120A`) and are never renumbered.
- **One directory per shot**, one `prompt.json` per take, one `approved.mp4` per shot.
- **State is on disk, not in chat.** A resumed session reads `state.json` and
  `PRODUCTION.md` first.

## Stage routing

Open the stage skill, hand it the artifacts it needs, and return with the gate artifact.

| You need | Load |
|---|---|
| premise, beats, screenplay, series bible | `film-story-development` |
| characters, world, style, voice, continuity assets | `film-design` |
| blocking, shot list, coverage, keyframes, animatic, edit plan | `film-directing` |
| model-specific prompt syntax (Seedance, Kling, Veo, Runway) | `ai-video-directing` |
| still-image prompt syntax (character sheets, plates, panels) | `ai-image-art-direction` |
| provider execution, variants, retakes, generation log | `film-generation` |
| cut, sound, grade, captions, masters, QC | `film-postproduction` |
| poster, key art, thumbnail, character posters, title treatment | `film-poster` |
| five-minute local vertical short from one topic | `cinematic-pipeline` |
| provider-agnostic studio with approval gates and budget | `open-montage` |
| edit existing footage conversationally | `video-use` |

## Approvals

Five creative gates and one delivery gate. Do not proceed past a gate without an explicit
yes. Record each approval in `state.json` and one line in `decision-log.md`. The delivery
gate (stage 9) checks the spec, not the creativity.

| Gate | Question the approver answers |
|---|---|
| Premise | Is this the film we want to make? |
| Script | Is this the story, at this length, with these characters? |
| Design | Is this how it looks, sounds, and who these people are? |
| Shot plan | Is this the cut we are going to shoot, at this budget? |
| Picture lock | Is this the film? |
| Delivery | Does it meet the spec and can it ship? |

For a solo user who says "just make it", the gates become self-checks: state the decision,
state the evidence, proceed, and log it. They never disappear.

## Series mode

A series is not a long film cut into pieces. It is a season of episodes that share a
bible, a continuity ledger, and an asset library. Run development and design once for the
season, then loop plan → generate → post per episode.

- Write the **season grid** before episode one: premise, arc per character, episode
  promises, midpoint, finale, cliffhangers.
- Lock **recurring assets** once: character sheets, location plates, props, voices, style.
- **Batch by asset, not by episode**, when practical: all shots in one location, all
  shots of one character, across adjacent episodes, to reduce drift.
- The **continuity ledger is updated after every episode**: who knows what, who is
  injured, what changed hands, what time of day it is.
- Produce a **pilot episode first**, pass every gate on it, run the blind quality comparison
  in `references/quality-ceiling.md`, then commit to the season. A pilot is the cheapest test
  of whether the pipeline can hold the look.

Details: `references/series-mode.md`.

## Feasibility arithmetic

Do this before the first generation, and put the numbers in `PRODUCTION.md`:

```text
shots        = runtime_s / average_shot_s
generations  = shots × variants_per_shot
gpu_hours    = generations × seconds_per_shot / 3600
cloud_cost   = generations × clip_seconds × provider_price_per_second
disk         = generations × clip_size + keyframes + audio + masters
```

On this machine (M2 Max, 96 GB), measured from `cinematic-pipeline`:

| Engine | Render | Seconds per 4 s shot | 10-min short, one pass |
|---|---|---:|---:|
| LTX-Video 0.9.8 distilled | 512×768 | ~100 | ~4.2 h |
| Wan 2.2 14B | 720p | ~400+ | ~17 h |
| MiniMax H3 REF2VA | reference-driven | slowest | multi-day |
| LTX-2.3 MLX | probe first | unknown | probe first |

Three variants per shot multiplies all of it by three. Keyframes, retries, audio and
edit are additional. A feature is a campaign, not a render. Full table and cloud
considerations: `references/feasibility.md`.

## Quality ceiling and the pilot

The pipeline enables the workflow; it does not by itself guarantee reference-tier quality.
Local-only output is below the best photoreal AI series by default, especially for human
faces, sustained dialogue and lip-sync. The gap is closed by model tier, identity packs and
LoRAs, a dedicated lip-sync pass, voice performance, post, and iteration budget — or by a
hybrid that sends the face/dialogue shots to a cloud model.

Before a series commitment, run the 60–90 second pilot in
`references/quality-ceiling.md`: same script, keyframes and voices across LTX-2.3 q4,
Wan 2.2 I2V-A14B q8 and, only if permitted, one cloud model; score blind on identity,
lip-sync, realism, voice consistency and emotional read. Do not promise parity before that
test passes.

## Continuity ledger

One file, updated as facts become true. It is the only defense against a series drifting
apart across episodes.

```markdown
## @mara
- identity: <verbatim canonical block>
- refs: 02_design/refs/mara/
- voice: <provider + voice id + seed>
- wardrobe: S01 coat (grey wool, torn left cuff) → S03 jacket (same, repaired)
- state: S02 injured left hand, bandaged → S05 scar only
- knows: S03 learns the ledger is forged
```

Update it at design lock, after each episode, and whenever a retake changes a canonical
fact. `film-generation` reads it before every prompt.

## Failure handling

- **Three-strike rule.** If a shot fails identity twice, change the reference or the
  keyframe, not the prompt. If it fails a third time, redesign the shot: cutaway, insert,
  silhouette, off-screen, 2D insert, stock. A shot that cannot be generated is a writing
  problem, not a rendering problem.
- **One variable per retake.** Change the prompt, the seed, the reference, or the model —
  never two at once, or the log teaches nothing.
- **Log the failure.** `04_gen/continuity-failures.md`, with shot, code, cause, fix.
- **Never re-roll an approved shot** to "see if it gets better". Re-open the gate first.

## Output contract

A production is complete when all of these exist and the QC gate passes:

```text
05_post/deliver/final_<aspect>_<res>.mp4
05_post/deliver/captions.srt
05_post/deliver/qc-report.md
05_post/deliver/delivery-manifest.md
05_post/process-notes.md
06_marketing/poster/poster-manifest.md
state.json  (stage=delivered, approvals recorded)
continuity-ledger.md  (final state)
```

## filmctl.py

The scaffold and validator that makes the layout mechanical:

```bash
python3 scripts/filmctl.py new <slug> --format short --runtime 8 --aspect 16:9 --tier local
python3 scripts/filmctl.py status <slug>
python3 scripts/filmctl.py validate <slug>          # gate artifacts for the current stage
python3 scripts/filmctl.py doctor                   # probe ffmpeg, ComfyUI, MLX, cloud keys
python3 scripts/filmctl.py prompts <slug> --dialect veo
python3 scripts/filmctl.py assemble <slug>          # normalize approved takes + concat
```

It never generates and never spends money. It creates, checks, compiles prompts, and
assembles local files.

## Reference map

| File | Contents |
|---|---|
| `references/pipeline.md` | the nine stages in detail, with deliverables and exit criteria |
| `references/project-layout.md` | directory tree, naming, `state.json` schema |
| `references/feasibility.md` | shot arithmetic, local throughput, cloud tiers, honest limits |
| `references/series-mode.md` | season grid, episode loop, batching, continuity |
| `references/gates.md` | the creative-gate and delivery-gate checklists in full |
| `references/quality-ceiling.md` | honest local-vs-reference quality assessment, three routes, pilot protocol and pass thresholds |
| `references/local-production-manifest.md` | local-only install list: HF-cache aliases, quantizations, runtime per model, disk and memory plan |
| `scripts/pull_models.py` | idempotent HF-cache puller: tiers, disk check, resume, retries, log |
| `references/sources/INDEX.md` | archived sources for the pipeline's non-obvious claims |
