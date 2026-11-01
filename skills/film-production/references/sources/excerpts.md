# Extracted Claims

Short extracts from the archived sources, with the claim they support. These are
paraphrases unless quoted; the raw captures are the authority.

## Pipeline backbone — AI Film Challenge

> Develop → Design → Plan → Generate → Assemble → Sound → Finish → Deliver → Document

- Every format shares the backbone; the per-format templates differ in time split and
  deliverables.
- Narrative short time split: writing 15%, design/pre-production 20%, generation 35%,
  edit 15%, sound 10%, finish 5%.
- Consistency rules: full character sheet with a fixed description block; world bible with
  an establishing key frame per location and a floor plan for multi-angle scenes; mark the
  180° line; lock the animatic before expensive generation; generate a key frame for every
  shot; batch episodes for consistency.
- Frequent traps: identity drift, flipped screen direction, skipped animatic, sound treated
  as an afterthought.

Supports: `film-production/references/pipeline.md`, `film-design`, `film-directing`.

## Script to storyboard — Domer AI

- 12 steps: logline → beats → scenes → runtime cut → shot list → continuity sheet →
  reference stills → prompts → batches → rough cut → selective regeneration → sound pass.
- Continuity sheet fields: character (name, age range, hair, wardrobe, marks), location
  (architecture, materials, palette, weather, time), lighting (key direction, temperature,
  contrast, practicals), lens feel (focal range, depth, grain), palette (three colors +
  accent).
- Paste the character block verbatim; paraphrasing changes the image.
- Shot entries use five fields: framing, camera move, subject action, lighting, duration.
- A 90-second film at 5-second clips needs roughly 18 shots before overlap and trimming.
- "Decisions made before generation are cheap, and decisions made after generation are
  expensive."

Supports: `film-story-development`, `film-design`, `film-directing`, `film-generation`.

## Prompt dialects — M Studio

| Model | Ordering | Length | Negatives |
|---|---|---|---|
| Kling 2.x | subject + movement + scene + camera + lighting + atmosphere | T2V 60–100 words; I2V 15–40 | dedicated field |
| Runway Gen-4 | camera first | no cap | unsupported; restate positively |
| Veo 3.x | subject → action → scene → camera → lens → style → audio → negative | progressive detail | Vertex-only field |
| Wan 2.x | narrative sentences; positional `[Image N]` | up to ~5,000 chars | field; default may be Chinese |
| Seedance 2.0 | subject + motion + camera + environment + light + style; first/then/finally | under ~250 words | in-prompt |

Supports: `film-generation/references/model-dialects.md`.

## Gemini Omni Flash — Google

- Model `gemini-omni-1.1-flash`, Interactions API.
- Inputs: text, images (reference, first/last frames, subject), video (up to 3 clips, 3 s
  each; audio ignored), audio processing.
- Output: 16:9 default, 9:16; 360p/720p/1080p/4k (upscaled); extension 3–10 s per step to
  40 s total.
- Audio generated automatically; prompts can request or suppress it.
- Negatives go inline; no separate negative parameter.
- "Continuous shot, no scene cuts" for one unbroken scene; "keep everything else the same"
  for edits; timecodes `[0-3s]` supported.
- Uploaded-video editing is unavailable in the EEA, Switzerland, and the UK.

Supports: `film-generation/references/model-dialects.md`.

## Runway catalog — Runway

- 27 video models in the catalog, 4 Runway-built and 23 third-party.
- Kling 4.0: 3–30 s, 720p/1080p, text/frame/reference generation, source-video editing.
- Seedance 2.5: T2V/I2V/V2V, up to 30 s, 480p/720p/1080p, image/video/audio refs.
- WAN 3.0: 2–30 s, 480p–1080p, built-in audio.
- MiniMax H3 Max: first and last frames, 480p/768p.
- Veo 3.1: speech and audio.
- Gen-4.5: T2V/I2V.

Supports: `film-generation/references/model-dialects.md`.

## Sora retirement — OpenAI

- Sora 2 and the Videos API were retired **2026-09-24**. No direct replacement API.
- Historical capabilities: 16/20 s clips, image reference for first frame, reusable
  character uploads, extensions up to 120 s, edits, 480p/720p (1080p on Pro), generated
  audio.
- Content restrictions: no real people, human-face inputs rejected, no copyrighted
  characters or music.

Supports: do not route to Sora; `film-generation` deprecation checks.

## Wan 2.2 — Alibaba

- T2V-A14B, I2V-A14B, TI2V-5B, S2V-14B, Animate-14B.
- 480p/720p; TI2V-5B at 720p/24 fps and 24 GB VRAM; A14B examples use 80 GB.
- Prompt extension recommended for quality but can invent details; disable or review it
  for locked shots.
- No documented first/last-frame control and no multi-reference conditioning in 2.2.

Supports: `film-generation/references/local-stack.md`, `model-dialects.md`.
