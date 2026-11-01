---
name: film-postproduction
description: >-
  Finish a film from approved takes: conform and edit picture, build the sound track
  (dialogue, ambience, Foley, score, mix), grade, add titles and captions, run technical and
  continuity QC, and deliver masters and cut-downs. Use when the user says "cut the film",
  "edit this", "add sound and music", "grade it", "add subtitles", "make the final master",
  "deliver this", or when generation is complete. Do not use for planning the cut (see
  film-directing), for editing footage that already exists as the main task (see video-use),
  or for generating shots (see film-generation).
---

# Film Postproduction

Picture, sound, finish, delivery. A generated shot is raw material; the film is made here.
The edit exposes what the board got wrong, the sound bed hides what the model could not
hold, and the QC gate decides whether the film ships.

> **Pipeline position.** Stages 6–9 of `film-production`. Consumes approved takes,
> `03_plan/shot-list.csv`, the animatic, and the sound plan. Writes `05_post/` and the
> delivery package.

## Step 1 — Ingest and conform

1. Collect every `approved.mp4` into a single conform list in shot order.
2. Verify each file: duration, resolution, fps, audio presence, checksum.
3. Make **proxies** for editing if the masters are large; keep the masters untouched.
4. Compare the cut to the **animatic**. The animatic is the timing decision; the edit
   either honors it or records why it changed.
5. Normalize the working timeline: one resolution, one fps, one audio sample rate. Do not
   mix 24/25/30 fps in one sequence.

`filmctl.py assemble` normalizes and concatenates approved takes into a rough cut; the
creative cut happens in an editor or `video-use`.

## Step 2 — Edit picture

- **Cut for story, not coverage.** If a shot does not change what the audience knows or
  feels, remove it even if it is beautiful.
- **Rough cut immediately.** Do not wait for every shot to be perfect; the edit reveals
  which shots are missing.
- **J and L cuts.** Let sound lead or trail picture at scene changes; it is the cheapest
  way to make generated coverage feel continuous.
- **Reactions over action.** A face hearing news is usually stronger than the event.
- **One idea per cut.** Do not change location, time, and character in the same cut.
- **Protect the turn.** The scene's turn gets the cut, the hold, or the silence it needs.
- **Handles.** Keep 12–24 frames on each side of a trim for the mix and grade.
- **Transitions mean something.** Cut by default; dissolve for time or memory; fade only
  at the ends.

Picture lock is a gate. After it, changes are versioned and re-QC'd.

## Step 3 — Sound

Sound is a directing decision, not a cleanup. Build five layers:

| Layer | What it does | Source |
|---|---|---|
| Dialogue | story, performance, intelligibility | TTS/voice actor, native model audio, ADR |
| Room tone / ambience | continuity glue, place | generated beds, libraries |
| Foley | physical reality: steps, cloth, objects | recorded or generated |
| Spot effects | story events: door, gun, phone | libraries, design |
| Score | emotion and rhythm | Suno MCP, MusicGen, licensed track |

Rules:

- **Record dialogue first**, then picture, then score. Timing follows the voice.
- **One continuous ambience bed per sequence** hides small visual drift and glues cuts.
- **Silence is a layer.** Use it before the turn.
- **Music is not a carpet.** Score the story, not every second.
- **Loudness**: streaming masters around −14 LUFS integrated; broadcast around −23 LUFS;
  true peak ≤ −1 dBTP. Measure, do not guess.
- **Stems**: deliver dialogue, music, effects separately so the film can be re-mixed.

Details: `references/edit-and-sound.md`. Suno MCP setup: `references/suno-mcp.md`.

## Step 4 — Finish

- **Grade** to the locked palette and color script. One LUT or curve set per project; do
  not grade shot by shot into incoherence.
- **Grain, halation, bloom** to match the style lock and to bind generated and stock
  material.
- **Upscale** to delivery resolution; keep the native master.
- **Stabilize** only if the motion is not intentional.
- **Titles and credits**: legible, timed, and inside safe areas.
- **Captions**: SRT/VTT, checked against the mix, with speaker labels where needed.
- **AI disclosure**: follow platform and jurisdiction requirements; record it in the
  delivery manifest.

## Step 5 — QC

Run the technical and continuity checks before delivery:

```bash
ffprobe -v error -show_entries format=duration,size,bit_rate \
        -show_entries stream=codec_name,width,height,r_frame_rate,sample_rate,channels \
        -of json 05_post/deliver/final_16x9.mp4
```

Check:

- [ ] Correct duration, resolution, fps, codec, audio layout.
- [ ] No black frames, freezes, dropped frames, or A/V drift.
- [ ] Loudness and true peak measured; no clipping.
- [ ] Captions in sync at first, middle, and last cue.
- [ ] Titles and credits legible at delivery size.
- [ ] Continuity: no unexplained wardrobe, prop, injury, or screen-direction jumps.
- [ ] Artifacts: hands, text, warping, duplicated limbs, watermarks.
- [ ] Legal: music and footage licences, consent, AI disclosure, rating.
- [ ] Every deliverable in the manifest exists and plays.

Template: `references/qc-and-delivery.md`.

## Step 6 — Deliver

| Deliverable | Spec |
|---|---|
| Master 16:9 | 1920×1080 or 3840×2160, H.264/H.265, AAC/48 kHz |
| Master 9:16 | 1080×1920, natively framed, not cropped from 16:9 |
| Master 1:1 (optional) | 1080×1080 |
| Archive master | ProRes 422 HQ or equivalent, with stems |
| Captions | SRT and VTT, UTF-8 |
| Cut-downs | 6 s, 15 s, 30 s where the platform needs them |
| Thumbnail / poster | key art at delivery aspect; owned by `film-poster`, checked here |
| Manifest | files, specs, checksums, licences, AI disclosure |

Do not crop a widescreen film to vertical and call it native. If vertical matters, frame it
at the shot-plan stage.

## Step 7 — Document

Write `05_post/process-notes.md`:

- Premise and runtime.
- Pipeline stages, tools, model versions, and dates.
- Shot count, generation count, accepted/rejected, GPU-hours and cost.
- What failed and what fixed it.
- What was not attempted, and why.
- Credits and licences.

The process notes are how the next film gets cheaper.

## Quality gate

- [ ] Picture lock approved.
- [ ] Mix approved; loudness measured.
- [ ] Grade and titles match the style lock.
- [ ] Captions synced.
- [ ] Technical QC and continuity QC passed.
- [ ] Delivery manifest complete; every file plays.
- [ ] Process notes written; archive stored.

## Reference map

| File | Contents |
|---|---|
| `references/edit-and-sound.md` | edit grammar, sound layers, mix targets, stems |
| `references/ffmpeg-cookbook.md` | concat, normalize, mux, loudness, captions, delivery commands |
| `references/qc-and-delivery.md` | QC checklist, delivery specs, manifest template |
| `references/suno-mcp.md` | connecting Suno as the score provider |
