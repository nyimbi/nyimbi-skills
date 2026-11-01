# AI-Feasibility Pass

The script is cheap. The shot is expensive. Rewrite anything that current models do
badly **before** the script locks.

## What is hard, and the rewrite

| Hard element | Why it fails | Rewrite |
|---|---|---|
| Crowds | identity, continuity, and motion budget collapse | isolate the lead; use sound, reaction, and shallow depth; cut to aftermath |
| Hands manipulating objects | finger geometry and object permanence | cut to the object, the face, or a silhouette; use an insert plate |
| Legible text | models invent or deform glyphs | design the insert in post; avoid the shot; use a close crop that excludes text |
| Sustained dialogue | one-speaker-per-clip rule; lip-sync drift | split into singles, reactions, and cutaways; use off-screen lines |
| Children and animals | performance and identity drift | reduce screen time; POV, over-shoulder, or off-screen |
| Complex action | motion budget: one action, one camera move | cause → reaction → aftermath; use cuts, not a continuous stunt |
| Water, fire, smoke | temporal coherence | short shots, silhouettes, sound-led coverage |
| Mirrors and reflections | identity duplication | avoid, or make the reflection the story point |
| Vehicles in motion | geometry and continuity | process shots, interior singles, exteriors from stock |
| Many locations | each is a design asset and a continuity liability | consolidate; reuse angles; imply off-screen space |
| Night exteriors | noise and light continuity | motivated practicals, closer shots, grade in post |
| Accents and dialects | TTS and lip-sync degrade | cast voices that match, or write around the accent |

## Shot arithmetic

```text
shots       = runtime_s / average_shot_s
variants    = 3 (hero shots), 2 (coverage), 1 (inserts)
generations = sum(shots × variants)
gpu_hours   = generations × seconds_per_shot / 3600
```

Example: a 10-minute short at 4 s per shot is 150 shots. At three variants each, 450
generations. At ~100 s per LTX shot on an M2 Max, that is ~12.5 GPU-hours before
keyframes, retries, audio, and edit.

A 90-minute feature at 4 s per shot is 1,350 shots — roughly 37.5 hours for one pass
locally, and several days with variants and retries. Write the feature as a hybrid:
animatic, stock, 2D inserts, and selective generation.

## Cast and location budget

| Tier | Principals | Recurring locations | Notes |
|---|---:|---:|---|
| Local short | 1–2 | 1–3 | every extra identity is a reference set and a drift risk |
| Local episode | 2–3 | 2–4 | reuse sets; batch by location |
| Cloud premium | 3–6 | 4–8 | references and LoRAs can hold more |
| Feature hybrid | any | any | generated heroes, practical/stock/2D coverage |

## Dialogue design

- One speaker per clip. Write reactions and silences as shots.
- Keep lines under ~12 words where lip-sync is visible.
- Avoid lines that depend on precise mouth shapes (`f`, `v`, `th` clusters) in close-up.
- Put exposition off-screen or in voice-over when the face does not need to carry it.
- Name characters with distinct phonemes; similar names confuse TTS casting and the
  viewer.

## The three-sentence test

Can you describe the film's arc in three sentences using only visible actions? If not,
the story still depends on interior states that the camera cannot shoot. Convert them
into behavior, objects, or sound before design begins.

## Cost of a late change

| Change after | Cost |
|---|---|
| Script lock | rewrite + re-breakdown |
| Design lock | new character sheets, references, voice, continuity |
| Shot-plan lock | re-board, re-time animatic, re-budget |
| Generation | regenerate every affected shot |
| Picture lock | re-edit, re-mix, re-grade, re-QC |

Solve story problems at the earliest row.
