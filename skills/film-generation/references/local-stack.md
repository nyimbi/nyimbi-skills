# Local Stack

Probed 2026-10-30 on Xevioso-6: Apple Silicon, 96 GB unified memory, macOS 27.0.1,
ffmpeg 9.0.2. Everything below is a probe result, not an assumption.

> **The install list is `film-production/references/local-production-manifest.md`.** It
> specifies the HF-cache-first rule, the exact aliases, the quantization to use, and the
> runtime per model. This file records what was probed and why; that file is the manifest.

## What exists

| Component | Path / endpoint | State |
|---|---|---|
| ComfyUI | `~/src/ComfyUI` | installed, **not running** at probe time |
| ComfyUI API | `http://127.0.0.1:8188` | start before generation |
| LTX models | `~/src/ComfyUI/models/checkpoints/ltxv/ltxv-2b-0.9.8-distilled-fp8.safetensors` | installed |
| MiniMax H3 | `~/src/ComfyUI/models/diffusion_models/MiniMax-H3-*.gguf` | installed (FL2VA, REF2VA) |
| Wan 2.2 VAE / UNet | `~/src/ComfyUI/models/vae/Wan2.2_VAE.safetensors`, `.../unet/wan2.2` | installed |
| FLUX | `~/src/ComfyUI/models/unet/flux1-dev-Q6_K.gguf` | installed for keyframes |
| SD 3.5 / SDXL Turbo | `~/src/ComfyUI/models/checkpoints/` | installed |
| F5-TTS | ComfyUI-F5-TTS custom node | installed |
| MusicGen | `facebook/musicgen-medium` | wired in `cinematic-pipeline` |
| Whisper | CLI installed | transcription for captions and timing |
| LTX-2.3 MLX | `~/.mlx-serve/models/dgrauet/ltx-2.3-mlx-q4` | model present; package appears partial — probe before use |
| LTX-2 code | `~/src/ml/Vision/LTX-2` | clone + venv; check its model instructions |
| CinematicPipeline | `~/src/CinematicPipeline` | 5-min vertical pipeline, LTX default |

Not installed or not configured at probe time: whisperx, piper, a local lip-sync node, and
any cloud provider key in OpenMontage's `.env` (all key fields empty).

## Start and probe

```bash
# ComfyUI
cd ~/src/ComfyUI && ./venv/bin/python main.py --listen 127.0.0.1 --port 8188

# probes
curl -sf http://127.0.0.1:8188/system_stats | head
curl -sf http://127.0.0.1:8188/queue
curl -sf http://localhost:11434/api/tags | jq -r '.models[].name'
```

If ComfyUI is already up, do not start a second copy. Check the queue before assuming it
is idle.

## Cinematic pipeline

`~/src/CinematicPipeline` is the fastest local path to a finished 5-minute vertical:

```bash
cd ~/src/CinematicPipeline
~/src/ComfyUI/venv/bin/python pipeline.py "<topic>" --resume
```

- Stages: storyboard → hero → shots → voiceover → score → assemble.
- LTX-0.9.8 distilled at 512×768, ~100 s per ~4 s shot; assembly upscales to 1080×1920.
- Wan 2.2 14B is ~4× slower; MiniMax H3 reference-to-video is slower still.
- Workflows present: `ltxv_t2v_api.json`, `api_wan2_7_t2v.json`,
  `wan22_ti2v_5b_template.json`.
- `config.py` is the single source of truth. Its default LLM name (`qwen3.6:35b-mlx`) and
  Wan workflow path may be stale; verify against the installed models before running.

For narrative work, use this pipeline only as a **shot engine**; the film pipeline owns
the story, design, shot list and edit.

## Practical limits

- LTX native vertical at 704×1280 is ~4× slower than 512×768. Budget accordingly.
- Wan 14B and MiniMax 33B plus FLUX plus TTS can exceed memory if models are left loaded.
  Close other ComfyUI workflows before a shot loop.
- A 10-minute short is ~150 shots: roughly 4 hours at LTX 100 s/shot, one pass. Three
  variants and retries make it 12–20 hours.
- Disk: 361 MB of skills is irrelevant to this, but video output is not. Estimate 20–200 MB
  per shot depending on resolution and codec, plus keyframes and masters.

## Local audio

- **Dialogue**: F5-TTS via ComfyUI, or `f5-tts` in the ComfyUI venv. One speaker per clip.
- **Score**: MusicGen medium, 25 s chunks with 1.5 s crossfades, or Suno MCP if the user
  connects it (see `film-postproduction/references/suno-mcp.md`).
- **Ambience/Foley**: generate beds locally from text prompts, or source licensed libraries.
- **Lip-sync**: no local node verified at probe time. Route to a model with native dialogue
  (Kling, Veo, Seedance) or install a lip-sync pass; do not claim it works until probed.

## Local keyframes

FLUX dev Q6 is the reliable local keyframe model. Generate at the project aspect, then use
the approved frame as first-frame conditioning for LTX/Wan. This is the cheapest
identity-control path on this machine.

## Recommended open-source local stack (surveyed 2026-10-30)

The installed set above is workable, not optimal. A focused follow-up survey found a
stronger Apple-Silicon path. Everything here is **reported**, not benchmarked on this
machine; verify locally before committing a production.

### Execution layers

| Layer | Repo | Licence | Why |
|---|---|---|---|
| **rapid-mlx** | installed (0.14.3) | — | **default**: reads the HF cache; serves text, image, video, TTS and STT through one OpenAI-compatible API; MTP/spec decode; multimodal aliases |
| **Unsloth Studio** | installed (2026.10.10) | Apache-2.0 | full local runtime: LLM via llama.cpp/GGUF, image via bundled mflux, audio/TTS/ASR/music via audio.cpp, and video via MiniMax-H3 / Wan2.2-S2V / LiveAvatar; plus LoRA training | 
| ComfyUI | installed | GPL-3.0 | workflow runner; PyTorch/MPS; GGUF models and nodes rapid-mlx does not expose; use symlinks into the HF cache |
| `mlx-video` | [Blaizzy/mlx-video](https://github.com/Blaizzy/mlx-video) (321★) | MIT | native MLX fallback for LTX-2/2.3 and Wan 2.1/2.2; T2V, I2V, A2V; LoRA; 2× spatial upscale; use for scripting, not as the default server |
| `mlx-video-with-audio` | [james-see/mlx-video-with-audio](https://github.com/james-see/mlx-video-with-audio) (8★) | MIT | LTX-2 T2V/I2V with synchronized audio on MLX; new and small, treat as experimental |
| Draw Things | app, not open source | — | simplest Mac GUI for Wan 2.2 / LTX-2.3; use when a GUI is worth more than a pin |

ComfyUI MLX extensions were searched but no maintained, verifiable repo was found on
2026-10-30; do not assume one exists. Prefer the `mlx-video` CLI for the MLX path.

### Models by job

| Job | Model | State | Note |
|---|---|---|---|
| Fast draft, iteration | LTX-Video 0.9.8 distilled | **installed** | ~100 s per 4 s shot at 512×768 |
| Fast draft + native audio | LTX-2 / 2.3 | MLX package present, partial | mlx-video supports it; verify the package before promising audio |
| Practical quality / 5B | Wan 2.2 TI2V-5B Q8 | **installed** | fits 24 GB-class machines |
| Best open quality | Wan 2.2 A14B I2V/T2V | T2V A14B Q4 installed; **I2V-A14B missing** | add I2V-A14B for image-to-video; Lightning 4-step LoRA for speed |
| Reference/audio-driven | MiniMax H3 FL2VA/REF2VA | **installed** | slowest; use for hero reference shots |
| Quality alternative | HunyuanVideo 1.5 (8.3B) | not installed | reported ~60 min/clip on an M3 Max 128 GB; too slow for coverage here |
| Keyframes | FLUX dev Q6 | **installed** | the reliable local still model |
| Lip-sync, realtime | MuseTalk 1.5 (MLX weights) | not installed | reported ~34 faces/s at 256², ~7 GB peak; upstream 6.8k★ |
| Lip-sync, quality | LatentSync 1.5/1.6 (MLX port) | not installed | Apache-2.0 port; MLX ~2.3× faster than PyTorch MPS; preprocessing stays in PyTorch |
| Upscale / interpolation | ESRGAN, RIFE | node installed, **model dirs empty** | add models before claiming upscale or 60 fps |

### Suggested path for this machine

1. Use **rapid-mlx** as the default server for the LLM, LTX-2.3, Wan 5B/I2V, Flux2,
   Qwen-Image and TTS/STT. All weights come from the HF cache via `rapid-mlx pull`.
2. Keep ComfyUI for GGUF/MinMax/FLUX-dev workflows, upscale, interpolation and control nets;
   symlink its models from the HF cache instead of copying them.
3. Add Wan 2.2 I2V-A14B if image-to-video quality is the goal; use the Lightning 4-step LoRA
   for drafts.
4. Add MuseTalk MLX for dialogue coverage; keep LatentSync-MLX as the quality fallback.
5. Add ESRGAN and RIFE models so the finish stage can actually upscale and interpolate.
6. Benchmark before committing: same keyframe, same prompt, three shots, measure
   seconds/shot, identity retention, motion quality, and audio sync.

`omlx` is currently listening on `:8000`; run rapid-mlx on `8001+`. `ollama` keeps a
separate blob store (196 GB) and is not the film default. Unsloth Studio is a full local
runtime (`:8888` UI/API, audio.cpp `:8080`): it reads the HF cache for LLM/GGUF models, and
its audio.cpp media packages may use their own GGUF store. Its LoRA adapters and checkpoints
are project outputs.

### Caveats

- Apple Silicon is roughly 5–10× slower than an RTX 4090 and far slower than an H100 for
  this workload; the published per-clip numbers come from small or unvetted repos and vary
  with quantization, resolution, and frame count.
- MLX ports differ in maturity. Pin a commit, check the licence, and keep the PyTorch path
  as a fallback.
- Model licences differ: Wan and LTX are Apache-2.0; HunyuanVideo and MuseTalk carry custom
  terms; check before publishing a film made with them.
- A model that is installed is not a model that is measured. The pipeline's feasibility
  numbers remain estimates until a real bake-off replaces them.

Archived sources for this section: `film-production/references/sources/` —
`mlx-video-readme.md`, `mlx-video-with-audio-readme.md`, `latentsync-mlx-readme.md`,
`hunyuanvideo-1.5-readme.md`, `modelfit-local-video-mac.html`,
`vcarl-apple-silicon-video.md`, `musetalk-1.5-mlx.html`.

## Re-probe before every campaign

Model directories, ComfyUI nodes, and workflow JSONs change. Run `filmctl.py doctor` and
write the result into `state.json`. A capability you did not probe is a promise you cannot
keep.
