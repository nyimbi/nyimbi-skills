# Continuity and Artifact QA

Score every clip before it can become `approved.mp4`. A take that fails one hard check is
not a maybe; it is a retake or a redesign.

## Per-clip checklist

| # | Check | Pass condition | Hard? |
|---|---|---|---|
| 1 | Identity | face geometry, hair, wardrobe match the hero frame | yes |
| 2 | Screen direction | 180° line and eyeline match the previous shot | yes |
| 3 | Light | key direction and color temperature match the scene | yes |
| 4 | Palette | three colors + accent hold | no |
| 5 | Props | present, correct hand, correct state | yes |
| 6 | Motion | one primary action, one camera move, no speed ramp | no |
| 7 | Anatomy | hands, joints, teeth, ears | no |
| 8 | Artifacts | no flicker, warp, text, watermark, duplicated limbs | yes |
| 9 | Audio | dialogue intelligible, no drift, no invented speech | yes |
| 10 | Framing | matches the shot size and keeps safe area for captions | no |
| 11 | Duration | within ±10% of the plan; trims available | no |
| 12 | End state | the action finishes where the next shot expects | yes |

## Failure codes

| Code | Symptom | First fix |
|---|---|---|
| F1 | identity drift | re-anchor the reference; add the drift clause |
| F2 | pose, not action | write the action as start → motion → end |
| F3 | reference conflict | remove the conflicting ref; one canonical per feature |
| F4 | motion overload | one action + one camera move |
| F5 | missing end state | name where the action stops |
| F6 | camera logic | match the move to the space and the cut |
| F7 | continuity gap | build shot A's last frame and shot B's first together |
| F8 | hands / text | cut to an insert or a silhouette; design text in post |
| F9 | flicker / warp | shorter clip, simpler motion, higher-quality model |
| F10 | audio drift | record dialogue first; one speaker per clip |
| F11 | face too small | regenerate at medium/close for identity-critical beats |
| F12 | wardrobe state | add a state ref and the inline clause |

The full diagnosis manual with mechanisms and ranked causes is
`film-directing/references/failure-modes.md`. Use it when the first fix does not hold.

## Scoring

For each take:

```text
pass  = all hard checks pass
soft  = count of soft-check failures (0–4)
rank  = pass, then fewest soft failures, then best performance, then shortest retake cost
```

Approve the highest-ranked passing take. Do not keep "almost" takes as approved.

## Log format

`04_gen/continuity-failures.md`:

```markdown
## S01_SH010 v2
- Failed: F1 (hair) and F9 (flicker at 2.1s)
- Cause: reference sheet showed wavy hair; prompt said curls
- Fix: replace sheet crop with hero frame; add "tight curls, not wavy"
- Next: v3, one variable changed
```

`04_gen/generation-log.csv`:

```csv
shot,take,provider,model,version,dialect,seed,refs,duration_s,resolution,cost,gpu_min,verdict,reason
S01_SH010,v1,local,ltx-2.3,2026-10,ltx,12345,"mara/hero;harbour/est",4.0,512x768,0,1.7,reject,F1 hair
S01_SH010,v3,local,ltx-2.3,2026-10,ltx,12346,"mara/hero;harbour/est",4.0,512x768,0,1.7,approve,-
```

## Audio checks

- **Loudness** measured later in post, but flag clips that are clipped or silent now.
- **Dialogue** intelligible at normal playback; no invented words; no accent drift.
- **Native audio** may include music or ambience the plan did not ask for. Strip it in the
  mix rather than regenerate the picture for it.
- **Room tone** recorded or generated per location; it is the continuity glue.

## When to stop retaking

- Three failures on the same hard check → redesign the shot.
- A shot that fails identity at every scale is a design problem: the reference set is
  inconsistent.
- A shot that fails motion at every prompt is a motion-budget problem: split it into two
  shots.
- A shot that fails because the story needs something the model cannot do is a writing
  problem: change the shot, not the model.
