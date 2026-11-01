---
name: cinematic-pipeline
description: Generate a 5-min vertical (9:16) cinematic MP4 with narration, music, and burnt captions from one topic prompt, running fully offline on this Mac. Default shot engine is LTX-Video 0.9.8 distilled fp8 (renders at 512×768, lanczos-upscales to 1080×1920 in assembly); Wan 2.2 T2V and MiniMax-H3 REF2VA are also wired. F5-TTS for narration, MusicGen for score, ffmpeg for assembly. Resumable — Ctrl-C safe. Use when the user says "make a 5-min video about X", "create a TikTok-style cinematic on X", "generate a vertical short film about X", or any request for a multi-shot narrated video piece. Expect ~1h 40min wall clock on M2 Max with the default engine (60+ shots × ~100 s each); Wan 2.2 or MiniMax push that to 6-8 hours. For provider-agnostic multi-pipeline video production (explain, documentary, talking head, clips, dub) with cloud+local providers and approval gates, see open-montage. For a narrative film or series from a rough outline, with story, character design, storyboards and delivery, see film-production.
compatibility: macOS 14+ on Apple Silicon; ComfyUI running at localhost:8188; Ollama serving qwen3.6:35b-mlx; ~40 GB free disk for outputs.
---

# Cinematic Pipeline

> **Routing:** For editing an existing video by conversation (cuts, grade, subtitles, overlays), use **video-use**.

Turns a topic prompt into a finished vertical cinematic video, running entirely on the local Mac against local models.

## Prerequisites checklist

Before running, confirm all of these once per session:

```bash
# 1. Ollama is serving the LLM
curl -sf http://localhost:11434/api/tags | jq -r '.models[].name' | grep -q '^qwen3.6:35b-mlx$' || echo "MISSING: ollama pull qwen3.6:35b-mlx"

# 2. ComfyUI is up
curl -sf http://127.0.0.1:8188/system_stats > /dev/null || echo "MISSING: cd ~/src/ComfyUI && ./venv/bin/python main.py &"

# 3. The default workflow JSON exists (others only needed for --engine overrides)
[ -f ~/src/CinematicPipeline/workflows/ltxv_t2v_api.json ] || echo "MISSING: workflows/ltxv_t2v_api.json — see ~/src/CinematicPipeline/README.md"
# Optional non-default engines:
for f in wan22_t2v_api.json minimax_h3_ref2va_api.json flux_t2i_api.json; do
  [ -f ~/src/CinematicPipeline/workflows/$f ] || echo "note: workflows/$f absent (only needed for --engine ${f%_api.json})"
done
```

If any check reports MISSING, resolve it before proceeding. Do not proceed with a partial setup.

## Run

The orchestrator is a Python script. You just wrap it and stream progress back to the user.

```bash
cd ~/src/CinematicPipeline
~/src/ComfyUI/venv/bin/python pipeline.py "<topic>" --resume 2>&1 | tee -a logs/run_$(date +%Y%m%d_%H%M%S).log
```

Options you can pass through:
- `--shots N` — override the default 75 (each LTX shot is ~4 sec, so N × 4 = total seconds).
- `--engine ltxv_t2v` (default, fast) · `--engine wan2.2_t2v` (14B MoE, higher quality, 4× slower) · `--engine minimax_h3_ref2va` (33B + audio-aware, needs a Flux hero image for character consistency, slowest).
- `--skip storyboard hero shots voiceover score assemble` — space-separated list of stages to skip.
- `--resume` — always include this; skips stages whose outputs already exist. Ctrl-C is safe.

## Reporting to the user

Progress lines look like `[HH:MM:SS] stage N: <what>`. Relay them as they come. The user cares about which stage is running and how many shots are done, not the raw ffmpeg output.

At the end, tell the user:
- Where the final MP4 lives: `~/src/CinematicPipeline/output/final.mp4`
- Wall clock the run took
- Any stage that failed (from state.json — the last successful stage is the last key)

## Failure modes to know about

- **ComfyUI stalls on a shot**: check `~/src/ComfyUI` for the process, `curl http://127.0.0.1:8188/queue` to see the queue. If stuck, kill+restart ComfyUI, then re-run with `--resume` — completed shots are cached in `output/shots/`.
- **`FileNotFoundError: workflow template missing`**: user hasn't exported an API-format workflow JSON. Direct them to `~/src/CinematicPipeline/README.md` "One-time setup" — 4 clicks in the ComfyUI UI.
- **Out of memory**: LTX-Video at 512×768 fits comfortably. If they picked `--engine minimax_h3_ref2va` or `--engine wan2.2_t2v`, close any ComfyUI tabs with other models loaded before the shot loop starts — a 14B/33B MoE + Flux + F5-TTS + MusicGen can exceed 96 GB unified memory.
- **Shots look soft**: LTX renders at 512×768 and assembly upscales via lanczos to 1080×1920. This is by design (4× faster than native vertical). If the user wants sharper native output, switch to `--engine wan2.2_t2v` or edit `RENDER_W`/`RENDER_H` in `config.py` to 704×1280 — expect ~7 h wall clock for a 5-min piece.
- **F5-TTS install missing**: `~/src/ComfyUI/venv/bin/pip install f5-tts` (should already be present).

## Educational variant

If the topic is a math / physics / CS concept, ask the user whether they want:
- A cinematic narrative (current pipeline — a story about the concept)
- A formal Manim animation (deterministic, equation-heavy, better for STEM)

If they pick Manim, use `~/src/CinematicPipeline/manim_scenes/pythagoras.py` as the shape reference and generate a new `.py` file with a `Scene` subclass. Render with:

```bash
~/src/ComfyUI/venv/bin/manim -qm --resolution 720,1280 --format mp4 <scene_file>.py <SceneClassName>
```

Narration for a Manim scene is a separate F5-TTS pass; mux with ffmpeg. Do NOT try to do a Manim scene inside the cinematic pipeline — they're different workflows.

## What NOT to do

- Do NOT try to generate the whole shot list serially in a single `pi -p` call. The pipeline handles the orchestration; you're just launching it.
- Do NOT modify `config.py` unless the user explicitly asks — it's the one source of truth.
- Do NOT run the pipeline without `--resume` if `output/state.json` exists from a prior run; it wastes hours of shot generation.
- Do NOT try to convert Manim to cinematic or vice versa on the same content — pick one register and commit.
