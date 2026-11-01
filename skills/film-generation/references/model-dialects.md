# Model Dialects

Verified 2026-10-30 against vendor documentation and the Runway model catalog. Model
availability moves monthly; re-verify before a campaign and update this file with a date.

## The matrix

| Model family | Access | T2V | I2V | First/last | References | Native audio | Duration | Res |
|---|---|---|---|---|---|---|---|---|
| Gemini Omni Flash 1.1 | Gemini API | yes | yes | yes | up to 3 video refs, 3 s each; image refs | yes | extend 3–10 s to 40 s | 360p/720p/1080p/4k upscaled |
| Veo 3.1 | Runway / Vertex | yes | yes | — | up to 3 images (Vertex) | speech + audio | clip | 720p/1080p |
| Kling 4.0 | Runway / Kling | yes | yes | yes | image/video refs | — | 3–30 s | 720p/1080p |
| Kling 3.0 Pro / O3 | Runway | yes | yes | yes | image refs, source video | optional | 3–15 s | 1080p |
| Seedance 2.5 | Runway / ByteDance | yes | yes | yes | image/video/audio refs | audio control | up to 30 s | 480p/720p/1080p |
| WAN 3.0 | Runway / Alibaba | yes | yes | — | image/video/audio refs | built-in | 2–30 s | 480p/720p/1080p |
| MiniMax H3 / H3 Max | Runway / local | yes | yes | H3 Max | text/image/video/audio refs (H3) | audio refs / built-in | clip | 480p/768p |
| Gen-4.5 | Runway | yes | yes | — | image input | — | clip | 720p |
| Grok Imagine 1.5 | Runway / xAI | yes | yes | start frame | image/audio refs | built-in | clip | 480p–1080p |
| Wan 2.2 | local ComfyUI | yes | yes | — | single image | — | ~5 s | 480p/720p |
| LTX-2.3 | local ComfyUI/MLX | yes | yes | — | image conditioning | audio VAE present | ~4–8 s | 512×768 and up |
| Sora 2 | retired 2026-09-24 | — | — | — | — | — | — | — |
| Veo 3.1 Preview | retired 2026-10-22 | — | — | — | — | — | — | — |

Do not route to a retired model. If a user names one, say it is retired and offer the
current path (Gemini Omni Flash, Runway's Veo 3.1, or a local model).

## Per-model prompt rules

### Gemini Omni Flash (Interactions API)

- Natural language: scene, camera, light, mood. Over-description causes unintended changes.
- Negatives go **in the prompt**; there is no negative parameter.
- Timecodes work: `[0-3s]`, `[3-6s]`.
- For one unbroken scene: "continuous shot, no scene cuts".
- Editing: "keep everything else the same".
- Up to 3 video references, each up to 3 s; audio in references is ignored.
- Extension appends only, 3–10 s at a time, 40 s total.
- Uploaded-video editing/extension is unavailable in the EEA, Switzerland, and the UK.

### Kling (2.x / 3.0 / 4.0)

- Order: subject + movement + scene + camera + lighting + atmosphere.
- T2V: 60–100 words. I2V: 15–40 words, motion and camera only.
- Dedicated negative field on the native API.
- "Elements" image references; camera controls; multi-shot labels
  (`[Character A: ...]`).
- Native dialogue and lip-sync on 3.0+; one speaker per clip.
- Do not reuse a T2V prompt as I2V; it is the most common Kling mistake.

### Veo 3.x

- Order: subject → action → scene → camera → lens → style → audio → negative.
- No hard length cap; progressive detail is rewarded.
- Native audio; dialogue syntax differs between Vertex and Gemini API.
- Up to 3 reference images; negative field only on Vertex, inline otherwise.
- Timestamp syntax for multi-beat clips.

### Runway Gen-4.5

- Camera first: "[camera] shot of [subject] [action] in [environment]".
- Direct, declarative. One change per iteration.
- **No negative prompt field.** Restate constraints positively ("clear blue sky").
- `@tag` name references for recurring subjects.

### Wan (2.2 local / 3.0 hosted)

- Long narrative sentences; can carry multi-shot beats in one prompt.
- Positional reference tokens, 1-indexed: `[Image 1]` must anchor a noun phrase.
- `negative_prompt` field; the default negative may be Chinese.
- `prompt_extend` can invent details that contradict the storyboard. Disable it for
  locked shots, or review the expanded prompt.
- Wan 2.2 local: 480p/720p, ~5 s, single image reference.

### Seedance (2.0 / 2.5)

- Order: subject + motion + camera + environment + light + style.
- Explicit beat markers: "first / then / finally".
- Under ~250 words; beyond that later beats are dropped, not compressed.
- First-frame or first+last-frame conditioning; strong face retention.
- Multi-shot narration is native; audio controls available on 2.5.
- Reference kits bind roles; keep the order fixed.

### LTX-2.3 (local)

- Concise cinematic sentence; the model rewards clean subject + action + camera + light.
- Negative prompt field in ComfyUI.
- Image conditioning supported; first-frame conditioning is the reliable path.
- Audio VAE present in the MLX package; verify the workflow uses it before promising sound.

## Cross-model rules

1. **One canonical record, compiled per model.** Never hand-edit a dialect and call it the
   record.
2. **Negatives are structural**: field (Kling, Wan, LTX), inline (Gemini Omni, Seedance),
   Vertex-only (Veo), unsupported (Runway).
3. **Word budgets are real**: Kling I2V 15–40; Seedance <250; Wan long; Veo progressive.
4. **Reference order binds roles.** Record it.
5. **Freeze versions.** A version change is a re-audit, not a quiet upgrade.

## Sources

- Gemini Omni Flash: https://ai.google.dev/gemini-api/docs/omni (retrieved 2026-10-30)
- Runway model catalog: https://docs.dev.runwayml.com/guides/models/ (2026-10-30)
- Veo API status: https://ai.google.dev/gemini-api/docs/video (2026-10-30)
- Sora retirement: https://developers.openai.com/api/docs/guides/video-generation (2026-10-30)
- Wan 2.2: https://github.com/Wan-Video/Wan2.2 (2026-10-30)
- Prompt grammar comparison: https://mstudio.ai/blog/ai-filmmaking/how-to-prompt-ai-video-models (2026-10-30)

Archived copies and the full source index: `film-production/references/sources/`.
