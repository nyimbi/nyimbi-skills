# Project Layout

```text
<slug>/
  PRODUCTION.md
  state.json
  decision-log.md
  continuity-ledger.md

  01_story/
    logline.md
    premise.md
    characters/<slug>.md
    beats.md
    scene-cards.csv
    setup-payoff.csv
    screenplay.fountain
    table-read.md
    quality-report.md
    series-bible.md
    LOCK.md

  02_design/
    design-brief.md
    style-lock.md
    characters/<slug>.md
    refs/
      characters/<slug>/{sheet.png,expressions.png,hero.png,hands.png,voice.wav}
      locations/<slug>/{establishing.png,reverse.png,detail.png}
      props/<slug>/{front.png,detail.png,state.png}
    world-bible.md
    floorplans/<slug>.png
    voice-casting.md
    continuity-system.md
    LOCK.md

  03_plan/
    scene-breakdown.csv
    shots.json
    shot-list.csv
    storyboards/S01/S01_SH010.png
    animatic.mp4
    sound-plan.md
    production-plan.md
    budget.csv
    risk-register.md
    LOCK.md

  04_gen/
    prompts/<dialect>/S01_SH010.txt
    keyframes/S01_SH010/{v1.png,v2.png}
    shots/S01_SH010/{hero.png,v1.mp4,v2.mp4,prompt.json,approved.mp4}
    lipsync/S01_SH010.mp4
    normalized/S01_SH010.mp4
    generation-log.csv
    continuity-failures.md

  05_post/
    edit/timeline.otio
    rough-cut.mp4
    picture-lock.mp4
    sound/{dialogue,ambience,foley,score,mix}.wav
    sound/stems/
    deliver/
      final_16x9_1080p.mp4
      final_9x16_1080p.mp4
      archive.mov
      captions.srt
      poster.jpg
      qc-report.md
      delivery-manifest.md
      SHA256SUMS
    process-notes.md

  06_marketing/
    poster/
      brief.md
      art/<concept>/master.png
      art/<concept>/prompt.json
      poster_onesheet_27x40_300dpi.tif
      poster_onesheet_2000x3000.png
      poster_teaser_2000x3000.png
      thumbnail_1920x1080.jpg
      poster_9x16_1080x1920.png
      poster_1x1_1080x1080.png
      character_<name>_2000x3000.png
      poster-manifest.md
```

## Naming

- Scene: `S01`, `S02`, …
- Shot: `S<scene>_SH<number>`, e.g. `S01_SH010`.
- Appended shot after lock: `S01_SH120A`.
- Take: `v1`, `v2`, …
- Approved: `approved.mp4`, exactly one per shot.
- Episode: prefix `E01_` before the scene when a series shares one tree:
  `E01_S01_SH010`.

## `state.json`

```json
{
  "project": "the-long-way-down",
  "format": "short",
  "runtime_s": 480,
  "aspect": "16:9",
  "fps": 24,
  "tier": "local",
  "stage": "generation",
  "stages": {
    "development": "approved",
    "design": "approved",
    "preproduction": "approved",
    "prepare": "in_progress",
    "generation": "pending",
    "assemble": "pending",
    "sound": "pending",
    "finish": "pending",
    "deliver": "pending"
  },
  "approvals": {
    "premise": "2026-10-30",
    "script": "2026-10-30",
    "design": "2026-10-30",
    "shot_plan": "2026-10-31",
    "picture_lock": null,
    "delivery": null
  },
  "models": {
    "keyframe": "flux-dev-Q6_K",
    "video": "ltx-2.3",
    "tts": "f5-tts",
    "score": "musicgen-medium"
  },
  "capabilities": {
    "probed": "2026-10-30",
    "comfyui": false,
    "cloud_keys": []
  },
  "budget": {
    "cap_usd": 0,
    "reserved_usd": 0,
    "spent_usd": 0,
    "gpu_minutes": 0
  }
}
```

Stage values: `pending`, `in_progress`, `gate_pending`, `approved`, `failed`.

## `PRODUCTION.md`

A human board, one screen:

```markdown
# <Title>

**Format:** short · **Runtime:** 8:00 · **Aspect:** 16:9 · **Tier:** local
**Stage:** generation · **Next gate:** shot acceptance

## Logline
...

## Approvals
| Gate | Date | Decision |
|---|---|---|

## Open risks
| Risk | Owner | Mitigation |
|---|---|---|

## Links
- Script: 01_story/screenplay.fountain
- Style: 02_design/style-lock.md
- Shot list: 03_plan/shot-list.csv
- Gen log: 04_gen/generation-log.csv
- Cut: 05_post/rough-cut.mp4
```

## Rules

- `state.json` is machine state; `PRODUCTION.md` is human state. Keep them consistent.
- Never store a prompt only in chat. `prompt.json` beside the take.
- Never overwrite an approved file.
- The ledger is canonical; a chat message is not.
