# Local Production Manifest — HF-Cache-First

Probed 2026-10-30 on Xevioso-6: Apple Silicon, 96 GB unified memory, macOS 27.0.1,
ffmpeg 9.0.2, `rapid-mlx` 0.14.3, **146 GiB free**, HF cache **581 GB**.

Two hard rules:

1. **Local production only.** No cloud model is on the critical path.
2. **Every weight lives in `~/.cache/huggingface/hub`.** Download with
   `rapid-mlx pull <alias>` or `hf download <repo>`. No second model store. rapid-mlx,
   the MLX tools and Unsloth all read base models from this cache; ollama's separate blob
   store and ComfyUI's copied model directories are exceptions, not the default. ComfyUI
   gets symlink views into the cache.

`rapid-mlx` is the default runtime because it reads the HF cache directly and serves
text, image, video, audio and speech through one OpenAI-compatible surface. It wraps the
same MLX kernels that `mlx-lm`, `mlx-video`, `mlx-audio` and `mflux` use, with batching,
model profiles and MTP/speculative decode.

---

## Pull script

`scripts/pull_models.py` downloads this manifest into the HF cache. It is idempotent:
present models are skipped, partial downloads resume, nothing is deleted. It checks free
space against the selected footprint plus a reserve, logs every attempt, and can pull by
tier or by name.

```bash
S=~/src/ml/skills/skill-bundle/skills/film-production/scripts/pull_models.py

python3 "$S" --list                       # tiers, sizes, repos
python3 "$S" --tier core --check         # what is present / missing
python3 "$S" --tier core --dry-run       # show the plan and commands
python3 "$S" --tier core --yes           # pull the core set
python3 "$S" --tier core,quality --yes   # core plus two quality models
python3 "$S" --model ltx-2.3-mlx-q4 --yes
python3 "$S" --tier tools --yes          # MuseTalk, LatentSync, ACE-Step, MusicGen
```

Defaults: `--via hf` (`hf download` with `--cache-dir`), `--reserve-gb 15`, `--retries 2`.
Use `--via rapid-mlx` to pull aliases through `rapid-mlx pull`; models without an alias fall
back to `hf`. `--force` re-downloads even when a repo is present. `--allow-tight` bypasses
the disk check (it still warns). The log defaults to
`~/.cache/huggingface/pull-film-models.log`.

Tier totals: core ~91 GB (66 GB missing on this machine), quality ~69 GB, optional ~114 GB,
tools ~22 GB. Do not run `--all` on 146 GB of free disk; it will refuse.

---

## Tier 0 — already on disk, no download

| Role | Alias / repo | Quant | Size | Runtime | Note |
|---|---|---|---:|---|---|
| LLM, fast default | `qwen3.6-35b-ud` | MLX 4-bit (UD) | 20.2 GB | rapid-mlx :8001 | cached; MoE, ~60 tok/s class |
| Image, fast default | `flux2-klein-4b` | mflux 4-bit | 4.3 GB | rapid-mlx :8002 | cached; keyframes, boards |
| STT, draft | `openai/whisper-large-v3-turbo` | fp16 | 1.5 GB | native / HF | cached; captions |
| Legacy video | LTX 0.9.8 distilled | fp8 (ComfyUI) | 4.2 GB | ComfyUI | outside HF cache; replace with LTX-2.3 below |
| Legacy video | Wan 2.2 T2V-A14B Q4_K_M, TI2V-5B Q8 | GGUF | 18 + 5 GB | ComfyUI | outside HF cache; migrate or keep as fallback |

---

## Tier 1 — core pulls (~71 GB)

Install these first. All are HF-cache models served by rapid-mlx.

| Role | Alias | Quantization | Size | Runtime / port | Why this quant |
|---|---|---|---:|---|---|
| LLM, quality | `qwen3.8-27b-4bit` | MLX 4-bit + MTP | 20.0 GB | rapid-mlx :8001 | 4-bit is the speed/quality sweet spot at 96 GB; rapid-mlx calls it 92% capability, ~41 tok/s |
| Video, default | `ltx-2.3-mlx-q4` | MLX q4, audio-capable | 21.2 GB | rapid-mlx :8003 | fastest realistic shot engine with native audio; 8-bit is 63 GB and not the default |
| Video, practical quality | `wan2.2-ti2v-5b-q8` | MLX q8 | 18.2 GB | rapid-mlx :8003 | 5B at q8 fits comfortably and is the quality step above LTX drafts |
| TTS, leads | `qwen3-tts-4bit` | MLX 4-bit | 2.2 GB | rapid-mlx :8004 | multilingual, custom voice; 4-bit is realtime-class |
| TTS, expressive | `chatterbox-4bit` | MLX 4-bit | 0.4 GB | rapid-mlx :8004 | fast emotion/voice-clone pass |
| TTS, scratch | `kokoro-4bit` | MLX 4-bit | 0.3 GB | rapid-mlx :8004 | table reads and scratch VO |
| STT, final | `whisper` (large-v3) | MLX | 2.9 GB | rapid-mlx :8005 | captions and timing; turbo 1.5 GB is already cached |
| Alignment | `qwen3-forced-aligner` | 8-bit | 1.2 GB | rapid-mlx :8005 | word-level timing for karaoke captions and cuts |

Total **70.7 GB**, leaving ~75 GiB for outputs and one Tier 2 model.

```bash
rapid-mlx pull qwen3.8-27b-4bit
rapid-mlx pull ltx-2.3-mlx-q4
rapid-mlx pull wan2.2-ti2v-5b-q8
rapid-mlx pull qwen3-tts-4bit
rapid-mlx pull chatterbox-4bit
rapid-mlx pull kokoro-4bit
rapid-mlx pull whisper
rapid-mlx pull qwen3-forced-aligner
rapid-mlx ls                      # confirm they are in the HF cache
```

---

## Tier 2 — quality pulls (choose at most two; ~29–40 GB each)

| Role | Alias | Quant | Size | Runtime | When |
|---|---|---|---:|---|---|
| Image with text | `qwen-image` | mflux q6 | 28.9 GB | rapid-mlx :8002 | posters, signage, key art with legible type |
| Image edit | `qwen-image-edit` | mflux q8 | 34.9 GB | rapid-mlx :8002 | object/wardrobe/light edits with preservation |
| Video I2V, hero | `wan2.2-i2v-a14b-q8` | MLX q8 | 39.7 GB | rapid-mlx :8003 | best open image-to-video; use Lightning 4-step LoRA for drafts |
| Video, hero + audio | `ltx-2.5-mlx-q8` | MLX q8 | 63.0 GB | rapid-mlx :8003 | highest local LTX quality; needs ~70 GB free and no other model resident |
| Image, quality | `hidream-o1-dev` | bf16 | 16.4 GB | rapid-mlx :8002 | alternative look; bf16 only when alone |

Disk arithmetic: Tier 1 + Qwen-Image ≈ 100 GB, leaving ~46 GiB. Tier 1 + Wan I2V ≈ 110 GB,
leaving ~36 GiB. Tier 1 + LTX-2.5 ≈ 134 GB, leaving ~12 GiB — **not enough for a film's
outputs**; move the cache or add an external drive before that pull.

---

## Tier 3 — specialist tools and small weights

| Job | Tool / weights | Size | Runtime | Note |
|---|---|---:|---|---|
| Lip-sync, realtime | MuseTalk 1.5 MLX (`mlx-community/MuseTalk-1.5-fp16`) | ~7 GB peak | native MLX | not a rapid-mlx alias; separate install |
| Lip-sync, quality | LatentSync-MLX (`sb1992/latentsync-mlx`) | ~5 GB | native MLX | preprocessing stays in PyTorch |
| Upscale | `4x-UltraSharp` / `RealESRGAN_x4plus` | ~64 MB | ComfyUI | symlink from HF cache |
| Interpolation | RIFE 4.6 | ~20 MB | ComfyUI | `ComfyUI-Frame-Interpolation` |
| Music / SFX | `facebook/musicgen-medium` | ~3 GB | native / ComfyUI | already wired in `cinematic-pipeline` |
| Music, songs | ACE-Step 3.5B (or Stable Audio Open) | ~5–7 GB | native / ComfyUI | optional; verify MLX/MPS support |
| Editing | ffmpeg, Blender, `video-use`, OpenMontage | — | native | no weights |

---

## Runtime assignment

| Runtime | Runs | Why | Port |
|---|---|---|---|
| **rapid-mlx** | LLM, LTX/Wan/CogVideo, Flux/Qwen-Image, TTS/STT | Apache-2.0; reads HF cache; one OpenAI API; MTP and profiles; multimodal routes | 8001–8005 |
| **ComfyUI** | GGUF video, MiniMax H3, FLUX dev, F5-TTS, ESRGAN/RIFE, control nets, LoRA | GPL-3.0; node graphs and model support rapid-mlx does not expose | 8188 |
| **native MLX** (`mlx-lm`, `mlx-video`, `mlx-audio`, `mflux`) | scripts, batch, bench, custom pipelines | no server overhead; direct control | — |
| **omlx** | day-to-day LLM already on `:8000` | 22 registered HF-cache models, OpenAI API, memory guard | 8000 |
| **ollama** | quick LLM tests only | convenience and Anthropic-compatible surface; **separate blob store**, so not the film default | 11434 |
| **Unsloth Studio** | full local runtime: LLM (llama.cpp/GGUF), image (mflux), audio (audio.cpp: TTS, ASR, music), video (MiniMax-H3, Wan2.2-S2V, LiveAvatar, lip-sync, Foley), plus LoRA training | reads the HF cache for LLM/GGUF models; Studio API `:8888`; audio.cpp `:8080` on Metal; media packages may use its own GGUF store | 8888, 8080 |

`omlx` is currently listening on `:8000`. Do not start rapid-mlx on 8000; use 8001+.

### Endpoint map (rapid-mlx)

| Modality | Endpoint |
|---|---|
| Text | `POST /v1/chat/completions` |
| Image | `POST /v1/images/generations`, `POST /v1/images/edits` |
| Video | `POST /v1/videos`, `GET /v1/videos/capabilities` |
| TTS | `POST /v1/audio/speech`, `GET /v1/audio/voices` |
| STT / align | `POST /v1/audio/transcriptions` |

One model per process. Run stages sequentially; stop a server before loading a heavier one.

### Unsloth Studio

Unsloth is a full local runtime, not only a trainer:

| Surface | Command / endpoint | What it does |
|---|---|---|
| One-liner LLM server | `unsloth studio run --model <hf-repo> --gguf-variant UD-Q4_K_XL` | llama.cpp/GGUF server; reads the HF cache |
| Studio UI / API | `unsloth studio` → `:8888` | chat, training, image, audio and video pages |
| Audio engine | `~/.unsloth/audio.cpp/audiocpp_server` → `:8080` | TTS, voice clone, ASR, alignment, music, and media tasks |
| Image | mflux bundled in Studio | Flux/Qwen-Image generation and edits |
| Training | `unsloth train --model <hf-repo> --dataset <hf-repo> --output-dir <project>/training/<run>` | LLM LoRA; reads base model and dataset from the HF cache |
| Export | `unsloth export <ckpt> <dir> -f gguf -q q4_k_m` | GGUF adapter/merge for ComfyUI or llama.cpp |

The audio.cpp engine exposes `/v1/audio/speech`, `/v1/audio/transcriptions`,
`/v1/audio/alignments`, `/v1/tasks/*` and `/v1/recipes/*`. Its model specs include ACE-Step
music, Wan2.2-S2V speech-to-video, MiniMax-H3 video, LiveAvatar, lip-sync and
video-conditioned Foley. General cinematic T2V/I2V still goes to LTX/Wan through rapid-mlx;
Unsloth is strongest for performance, avatar, lip-sync and music.

**Cache caveat.** LLM/GGUF models and Studio's mflux models come from the HF cache. Some
audio.cpp media packages install into their own GGUF store (for example
`~/.cache/ace-step`). If the single-store rule is strict, point audio.cpp's model root at a
symlinked HF-cache tree or accept those packages as a documented exception.

---

## Licences

Runtimes: rapid-mlx **Apache-2.0**; ComfyUI **GPL-3.0**; mlx-lm, mlx-audio, mflux,
mlx-video **MIT**; Unsloth **Apache-2.0**; ffmpeg **LGPL/GPL** depending on build; Blender
**GPL**; OpenMontage **AGPL-3.0**; omlx and ollama are the desktop/server apps — check
their terms separately.

Model weights are a separate licence from the runtime. Known positions: Wan 2.2 and
LTX-Video **Apache-2.0**; Whisper **MIT**; Kokoro **Apache-2.0**; MusicGen code **MIT** but
the **weights are CC-BY-NC 4.0 (non-commercial)**; MiniMax H3, HunyuanVideo, MuseTalk and
some FLUX variants carry custom or non-commercial terms. Check the model card before a
commercial release; the runtime licence does not grant weight rights.

---

## Quantization rules

| Class | Fast / draft | Balanced | Final | Avoid |
|---|---|---|---|---|
| LLM | 4-bit MLX | 6-bit MLX | 8-bit MLX (alone) | 2-bit for writing; 8-bit while video is resident |
| Video | q4 MLX (LTX-2.3), Q4_K_M GGUF (A14B) | q8 MLX (Wan 5B/I2V) | bf16 only when the model is alone | fp16 A14B (64 GB); 8-bit + LLM co-resident |
| Image | 4-bit mflux (Flux2, Z-Image) | q6 mflux (Qwen-Image) | q8/bf16 (Qwen-Image-Edit, HiDream) | bf16 while video is loaded |
| Audio | 4-bit TTS/STT | 8-bit | bf16 for final lead lines | fp16 duplicates |

Fast means: an LLM at 4-bit, a video model at q4 or Q4_K_M, an image model at 4-bit, a TTS
model at 4-bit. Balanced means 6–8-bit when the shot or line is worth the memory. Final
means bf16 for a single model with nothing else resident. The numbers above are footprint
and reported speed class, not measured on this machine.

---

## Stage-by-stage memory plan

| Stage | Resident model | Approx memory | Stop before next |
|---|---|---|---|
| Story / screenplay | Qwen3.8-27B 4-bit | 20 GB | image or video |
| Design / keyframes | Flux2 4-bit or Qwen-Image q6 | 4–29 GB | video |
| Video | LTX-2.3 q4 or Wan 5B q8 | 18–21 GB | image/LLM |
| Hero video | Wan I2V q8 or LTX-2.5 q8 | 40–63 GB | everything else |
| Dialogue / score | Qwen3-TTS / Chatterbox / MusicGen | 0.4–3 GB | — |
| Edit / finish | ffmpeg, Blender, ComfyUI upscale | CPU/GPU light | — |

Do not co-load the LLM, the image model and a 14B video model. 96 GB is enough for one
heavy tenant plus a small audio process, not for a studio's worth at once.

---

## ComfyUI without a second model store

ComfyUI needs files under `ComfyUI/models/<type>/`. Keep the bytes in the HF cache and
symlink:

```bash
SNAP=$(ls -d ~/.cache/huggingface/hub/models--<org>--<repo>/snapshots/*/ | head -1)
ln -sf "$SNAP/<file>" ~/src/ComfyUI/models/<type>/<file>
```

For the few models rapid-mlx does not expose (MiniMax H3 GGUF, F5-TTS, ESRGAN, RIFE),
download the repo with `hf download <repo>` and symlink the file. Do not keep a second copy.

### Migrating the legacy ComfyUI copies

The existing LTX 0.9.8, Wan GGUF and FLUX files were downloaded outside the HF cache. To
bring them under the single-store rule:

```bash
# 1. Pull the canonical repo into the HF cache
hf download <org>/<repo> --include "<file>.gguf"

# 2. Symlink the snapshot file into ComfyUI
SNAP=$(ls -d ~/.cache/huggingface/hub/models--<org>--<repo>/snapshots/*/ | head -1)
ln -sf "$SNAP/<file>.gguf" ~/src/ComfyUI/models/<type>/<file>.gguf

# 3. Verify ComfyUI loads it, then remove the old copy only after a successful run
```

Do the same for `MiniMax-H3-*.gguf` and `FLUX.1-dev`. Keep no duplicate after migration.
The ollama store (196 GB) is convenience-only; do not add film models there.

---

## Verify

```bash
rapid-mlx ls                         # cached aliases and sizes
rapid-mlx recipe                     # smart/fast LLM for this Mac
rapid-mlx ps                         # running servers
curl -s localhost:8001/v1/models
curl -s localhost:8003/v1/videos/capabilities
curl -s localhost:8004/v1/audio/voices
python3 skills/film-production/scripts/filmctl.py doctor
```

## Do not install

- **DeepSeek V4 141 GB, MiniMax M2 120 GB, Qwen3.5-122B 60–122 GB** — do not fit with
  headroom and are far slower than the 27–35B class.
- **Wan 2.2 T2V-A14B bf16 (64 GB)** — use the Q4_K_M GGUF in ComfyUI or the MLX q8 I2V
  variant instead.
- **Ollama copies of film models** — a second store outside the HF cache; use rapid-mlx.
- **Cloud stubs** (`:cloud` models in ollama) — not local production.
- **2-bit LLMs for writing** — fast but visibly degraded for screenplay and dialogue.
