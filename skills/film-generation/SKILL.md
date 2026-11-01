---
name: film-generation
description: >-
  Execute a locked shot plan: probe local and cloud providers, generate and approve hero
  keyframes, compile one canonical shot record into each model's prompt dialect, batch
  variants, run continuity and artifact QA on every clip, handle dialogue and lip-sync, and
  keep a generation log with model versions, seeds, references and cost. Use when the user
  says "generate the shots", "render the film", "make the clips", "run the pipeline", "why
  does this clip drift", "regenerate this shot", or when a shot list and design are locked.
  Do not use for planning the shots (see film-directing), for prompt craft without execution
  (see ai-video-directing), or for cutting and finishing (see film-postproduction).
---

# Film Generation

The generation floor. It takes a locked shot list and a locked design and turns them into
approved takes, with the minimum number of paid or slow attempts.

> **Pipeline position.** Stages 4–5 of `film-production`. Consumes `03_plan/shots.json`,
> the design locks, and the continuity ledger. Writes `04_gen/`. Hands approved takes and
> the generation log to `film-postproduction`.

## Preflight — probe before promising

Never assume a provider, model, or workflow is available. Probe and write the result into
`state.json`:

```bash
python3 scripts/filmctl.py doctor <project>
```

The probe checks:

| Surface | Probe | If missing |
|---|---|---|
| ffmpeg / ffprobe | binary and version | install before any assembly |
| ComfyUI | `GET :8188/system_stats`, `GET :8188/queue` | start ComfyUI; record the URL |
| Local models | LTX-2.3, Wan 2.2, MiniMax H3 files | list what exists; do not promise the rest |
| MLX serve | model directory and any listening port | probe; do not infer |
| Cloud keys | presence only, never print values | route to local or ask for a key |
| Disk | free GB against estimated output | stop before filling the disk |
| Provider catalogs | model IDs and versions | freeze versions in `state.json` |

Model availability changes monthly. On 2026-10-30 the verified matrix is in
`references/model-dialects.md`; re-verify before a campaign and record the date.

## The canonical shot record

`03_plan/shots.json` is the single source of truth. Every dialect is compiled from it.
Schema: `references/canonical-shot.md`.

```json
{
  "id": "S01_SH010",
  "scene": "S01",
  "duration_s": 4.0,
  "function": "establish",
  "shot_size": "wide",
  "lens_mm": 24,
  "subject": "the harbour at dawn, Mara small at the rail",
  "action": "she sets down a case and does not let go of the handle",
  "environment": "grey water, rusted rail, cold blue light",
  "camera_move": "slow push-in, 1.5 m",
  "lighting": "low sun camera-left, hard rim, deep shadow",
  "audio": "gulls, water against pilings",
  "negative": "no modern boats, no text, no extra people",
  "characters": ["@mara"],
  "refs": ["02_design/refs/mara/hero.png", "02_design/refs/harbour/establishing.png"],
  "dialect": "veo",
  "priority": "hero",
  "risk": ["water", "hands"]
}
```

Rules:

- **One primary action** and **one camera move** per shot. More is a motion-budget
  overrun, not ambition.
- **Every action has an end state.** "She turns" is not a shot; "she turns until her
  profile is against the window and stops" is.
- **The style block is not in the record**; it is appended from `style-lock.md` verbatim.
- **The negative names instances**, never categories.
- **`priority`** drives the variant budget: `hero` 3–5, `coverage` 2, `insert` 1.

## Keyframes first

A video model mostly re-animates what the still already decided. Fix the still.

1. For each shot, generate 1–3 keyframe candidates with the character, location, and
   style references in the fixed order.
2. Approve one hero frame per shot. Record the prompt, seed, refs, and model version.
3. For transformations or designed transitions, generate a **last frame** as well and use
   the first/last-frame control surface.
4. Only then compile the motion prompt.

Gate: no video generation from an unapproved keyframe. This is the single highest-leverage
rule in the pipeline.

## Prompt compilation

Do not write a fresh prompt per model by hand. Compile the canonical record into the
target dialect. For the craft of the prompt itself, load `ai-video-directing`; for the
dialect table and word budgets, load `references/model-dialects.md`.

| Control surface | Shape | Typical models |
|---|---|---|
| Text-to-video | full description: subject, action, scene, camera, lens, light, style, audio | Veo, Kling T2V, Seedance T2V, Wan, LTX |
| Image-to-video | motion only: camera, action, end state, constraints | Kling I2V, Seedance I2V, Gen-4.5 |
| First + last frame | describe the bridge, not the stills | Kling, Seedance, MiniMax H3 Max |
| Reference-to-video | bind roles to reference slots; name the character verbatim | Seedance 2.5, Kling 4.0, MiniMax H3, WAN 3.0 |
| Multi-shot timestamped | overall continuity block + per-segment lines | Seedance 2.5, Kling 3.0+, Veo |
| Video-to-video | restyle/relight/repair an approved take | Aleph 2.0, Kling 4.0 editing |

Compile with:

```bash
python3 scripts/filmctl.py prompts <project> --dialect veo
```

The compiler writes `04_gen/prompts/<dialect>/<shot>.txt` and refuses a shot missing a
required field.

Dialect rules that bite:

- **Kling I2V** gets 15–40 words of motion only. Scene description in an I2V prompt
  creates conflicting signals.
- **Runway** has no negative field. Restate constraints positively: "clear blue sky",
  not "no clouds".
- **Veo / Gemini Omni** take negatives inline on the Gemini API and order the prompt
  subject → action → scene → camera → lens → style → audio.
- **Wan** uses positional reference tokens (`[Image 1]`) and a long narrative; do not let
  `prompt_extend` invent details that contradict the board.
- **Seedance** drops beats beyond roughly 250 words instead of compressing them.
- **LTX** is concise; the local stack rewards a clean cinematic sentence, not a novel.

## Variants and retakes

- Generate the budgeted variants in one batch per shot, same prompt and references, seed
  varied deliberately.
- Score each take against the shot's function first, then continuity, then artifacts.
- **One variable per retake**: prompt, seed, reference, or model. Never two.
- **Three-strike rule**: two identity failures → change the reference or keyframe; a third
  → redesign the shot (cutaway, insert, silhouette, stock, 2D).
- Keep every take until the shot is accepted; delete only after the shot is approved and
  logged.

## Continuity and artifact QA

Score every clip before approval:

| Check | Pass condition |
|---|---|
| Identity | face, hair, wardrobe match the hero frame |
| Screen direction | 180° line and eyeline match the previous shot |
| Light | key direction and color temperature match the scene |
| Palette | three colors + accent hold |
| Props | present, correct hand, correct state |
| Motion | one action, one camera move, no speed ramps |
| Anatomy | hands, joints, teeth, ears |
| Artifacts | no flicker, warp, text, watermark, duplicated limbs |
| Audio (if native) | dialogue intelligible, no drift, no invented speech |

Failures are logged with a code and the cheapest fix. The full diagnosis manual belongs to
`film-directing` (`references/failure-modes.md`); this skill records the result.

## Dialogue and lip-sync

1. Record or synthesize the voice **before** the performance shot. One speaker per clip.
2. Match the take to the line length; a line that cannot fit is a writing problem.
3. Use native dialogue/lip-sync where the model supports it (Kling, Veo, Seedance), or a
   dedicated lip-sync pass.
4. Keep faces at medium or close for lip-sync; wide shots hide the mouth and waste the
   attempt.
5. Check phoneme alignment at the first and last word, not the middle.

## Cost and time

Before a batch, estimate and reserve:

```text
generations = shots × variants
gpu_hours   = generations × seconds_per_shot / 3600
cloud_cost  = generations × clip_seconds × price_per_second
```

- Freeze a **budget cap** in `state.json`; stop and ask before exceeding it.
- Log every generation's cost, even local ones (as GPU-minutes), so the next estimate is
  measured, not guessed.
- Local throughput and cloud tier guidance: `references/cost-and-throughput.md`.

## Logging

`04_gen/generation-log.csv`, one row per generation:

```csv
shot,take,provider,model,version,dialect,seed,refs,duration_s,resolution,cost,gpu_min,verdict,reason
```

`prompt.json` beside each take repeats the compiled prompt, the parameters, and the
reference order. A take without its prompt is not reproducible and should not be approved.

## Quality gate

- [ ] Preflight recorded; providers and model versions frozen.
- [ ] Every shot has a canonical record with all required fields.
- [ ] Hero frame approved for every shot before animation.
- [ ] Prompt compiled per dialect, not copy-pasted across models.
- [ ] Variant budget met for hero shots; one variable per retake.
- [ ] Continuity and artifact QA recorded for every approved take.
- [ ] Dialogue recorded before performance; lip-sync checked at first and last word.
- [ ] Generation log complete; cost within cap.
- [ ] Unusable shots redesigned, not re-rolled indefinitely.

## Reference map

| File | Contents |
|---|---|
| `references/canonical-shot.md` | shot schema, required fields, compiler behavior |
| `references/model-dialects.md` | verified model matrix and per-model prompt rules (2026-10-30) |
| `references/local-stack.md` | ComfyUI, LTX, Wan, MiniMax, F5-TTS, MusicGen on this machine |
| `references/continuity-qa.md` | per-clip checklist, failure codes, log format |
| `references/cost-and-throughput.md` | local throughput, cloud tiers, budget arithmetic |
