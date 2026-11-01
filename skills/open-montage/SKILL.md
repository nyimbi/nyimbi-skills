---
name: open-montage
description: OpenMontage (calesthio, AGPLv3) — the open-source agentic video production studio. Use when the user wants a full produced video through pipelines rather than one generated clip: animated explainers, documentary montages from real stock/archival footage, talking-head videos, clip factories (long video → batch of shorts), podcast repurposing, screen demos, cinematic trailers, localization/dubbing, avatar spokespersons, character animation. Runs the research → proposal → script → scene plan → assets → edit → compose flow with scored provider selection, human approval gates, budget caps, and post-render self-review. Zero API keys needed for the free path (Piper TTS, Remotion, HyperFrames, ffmpeg, Archive.org/NASA/Wikimedia footage). Installed on this machine at ~/Developer/openmontage. Do not use for editing existing footage conversationally (see video-use), for fully-local 9:16 cinematic shorts rendered by LTX-Video (see cinematic-pipeline), for a narrative film or series developed from a rough outline (see film-production), or for motion-graphics MP4 inside the OpenDesign app (see open-design).
---

# open-montage (OpenMontage)

OpenMontage turns the coding agent into a full video production team. There is
no code orchestrator — the agent reads a YAML pipeline manifest, follows the
per-stage "director skills", calls Python tools through a scored provider
selector, self-reviews against quality gates, and pauses for human approval
at creative decision points. Every provider choice and creative decision is
logged in an auditable decision trail.

## State on this machine

| What | Where |
|---|---|
| Runtime | `~/Developer/openmontage` (git clone, AGPLv3) |
| Setup | `make setup` (Python venv + `remotion-composer/` npm install + `piper-tts`) |
| Agent contract | `~/Developer/openmontage/AGENT_GUIDE.md` (720 lines — read before non-trivial work) |
| Skills (Layer 2) | `~/Developer/openmontage/skills/{core,creative,meta,pipelines}/` (157 files) |
| Pipeline manifests | `~/Developer/openmontage/pipeline_defs/` (YAML) |
| Live board | `python -m backlot open` — fills in as the production runs; approval gates show here |
| API keys | `~/Developer/openmontage/.env` — every key optional; more keys = more tools |

If the venv is missing or stale: `cd ~/Developer/openmontage && make setup`.
Probe capability before promising anything (verified 2026-09-28: 121 tools
registered, 51 available with zero keys — ffmpeg analysis, Piper TTS, stock
media, Remotion/HyperFrames composition):

```bash
cd ~/Developer/openmontage && source .venv/bin/activate
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.support_envelope(), indent=2))"
```

## Pipelines

| Pipeline | Produces |
|---|---|
| **explainer** | AI-generated animated explainer with live web research, narration, visuals, music |
| **documentary-montage** | Thematic montage cut from a CLIP-indexed corpus of free stock/archival footage (real motion, no paid generation) |
| **talking-head** | Footage-led speaker videos (user footage, captions, b-roll) |
| **clip-factory** | Batch of ranked short-form clips from one long source |
| **cinematic** | Trailers, teasers, mood-driven edits |
| **animation** | Motion graphics, kinetic typography |
| **avatar-spokesperson** | Avatar-driven presenter videos |
| **hybrid** | Source footage + AI-generated support visuals |
| **localization-dub** | Subtitle, dub, translate existing video |
| **podcast-repurpose** | Podcast highlights → video |
| **screen-demo** | Polished software screen recordings/walkthroughs |
| **character-animation** | SVG-rig cartoon acting via HyperFrames |

Every pipeline follows `research → proposal → script → scene_plan → assets →
edit → compose`. Web research is a first-class stage (15–25+ searches across
YouTube/Reddit/HN/news/academic before any script is written).

## Zero-key capability (what works with no .env at all)

Piper TTS narration · Archive.org + NASA + Wikimedia Commons footage ·
Pexels/Unsplash/Pixabay with free dev keys · Remotion (React) composition ·
HyperFrames (HTML/CSS/GSAP) composition · ffmpeg post (encode, subtitle burn,
audio mix, color grade) · built-in word-level subtitles. The renderer is
chosen at proposal (`render_runtime`: Remotion for data-driven explainers,
HyperFrames for motion-graphics-heavy briefs) and locked — silent swaps are a
governance violation.

With keys (add to `.env`): fal.ai (FLUX + Veo/Kling/MiniMax), ElevenLabs
(TTS/music/SFX — this machine already has an ElevenLabs key for video-use),
OpenAI TTS/GPT Image, Google TTS/Imagen, Suno music, Runway, Seedance, Kling
official, HeyGen gateway. Local GPU generation: WAN 2.1/2.2, Hunyuan,
CogVideo, LTX-Video (`make install-gpu` + `VIDEO_GEN_LOCAL_ENABLED=true`).

## Workflow

1. **Select the pipeline** for the brief (table above); read its manifest in
   `pipeline_defs/` and its stage director skills in
   `skills/pipelines/<pipeline>/`.
2. **Check the envelope** (probe above) so proposals only promise what the
   configured providers can deliver; the agent must state cost estimates
   before asset generation.
3. **Run the stages** with the human approval gates (proposal → script →
   scene plan → generated assets → publish). `python -m backlot open
   <project-id>` shows the live board.
4. **Budget governance is on by default** — estimate → reserve → reconcile,
   per-action approval above $0.50, $10 total cap (configurable).
5. **Post-render self-review is mandatory** — ffprobe validation, frame
   sampling (black frames, broken overlays), audio level analysis, delivery
   promise verification, subtitle checks. A failing review means the video
   is not presented.

## Boundaries

- **video-use** — conversational editing of footage the user already has
  (cuts, grades, overlays, captions). OpenMontage *produces* a video from a
  brief; video-use *edits* existing material. They can chain: produce here,
  polish in video-use.
- **cinematic-pipeline** — fully local 5-min 9:16 cinematic rendered by
  LTX-Video 0.9.8 (offline, ~1h40m). OpenMontage is provider-agnostic and
  pipeline-broader; it also supports LTX-Video as one of many providers.
- **open-design** — motion-graphics MP4 (HyperFrames) produced inside the
  OpenDesign app with a DESIGN.md brand loop.

## Reference map

| File | Contents |
|---|---|
| `references/skill-index.md` | OpenMontage's own skill index: 3-layer knowledge architecture, capability families, selector/provider pattern (upstream `skills/INDEX.md`) |
| `references/core/*.md` | Core compositor/editor skills verbatim: remotion, hyperframes, ffmpeg, whisperx, subtitle-sync, color-grading |

The full runtime knowledge (all 12 pipeline director skill sets, creative
techniques, reviewer/checkpoint protocol, 100+ tool docs) lives with the
runtime at `~/Developer/openmontage/skills/` — read it in place rather than
duplicating it here.

Upstream: https://github.com/calesthio/OpenMontage (AGPLv3).
