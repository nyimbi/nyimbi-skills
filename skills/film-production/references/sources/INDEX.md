# Source Index

All documents retrieved **2026-10-30** with `curl -L` and stored in this directory.
HTML files are raw captures; `excerpts.md` holds the extracted claims this bundle
actually relies on. Re-verify model availability before a campaign — the two
retirements below happened within five weeks of this archive.

| File | Source | What it supports |
|---|---|---|
| `aifilmchallenge-pipeline-templates.html` | https://aifilmchallenge.com/resources/guides/pipeline-templates | the Develop → Design → Plan → Generate → Assemble → Sound → Finish → Deliver → Document backbone; consistency rules; format-specific time splits |
| `domer-script-to-storyboard.html` | https://domer.io/blog/ai-script-to-storyboard-preproduction-workflow-8706bc51 | the 12-step script-to-storyboard workflow; continuity-sheet fields; coverage and timing rules; "decisions before generation are cheap" |
| `mstudio-prompt-models.html` | https://mstudio.ai/blog/ai-filmmaking/how-to-prompt-ai-video-models | per-model prompt grammar and word budgets for Kling, Veo, Runway, Wan, Seedance; negative handling |
| `gemini-omni.html` | https://ai.google.dev/gemini-api/docs/omni | Gemini Omni Flash capabilities, inputs, references, extension limits, prompt rules |
| `runway-models.html` | https://docs.dev.runwayml.com/guides/models/ | current Runway model catalog: Kling 4.0, Seedance 2.5, WAN 3.0, MiniMax H3, Veo 3.1, Gen-4.5, Grok |
| `openai-sora-video.html` | https://developers.openai.com/api/docs/guides/video-generation | Sora 2 and the Videos API retired 2026-09-24; historical prompt guidance |
| `wan2.2-readme.md` | https://github.com/Wan-Video/Wan2.2 | Wan 2.2 variants, hardware, prompting, prompt extension |
| `refay-NOTICE.txt` | https://github.com/drkhaledalrefay-coder/refay-skills/blob/main/NOTICE | CC BY 4.0 attribution required for the identity-lock method |
| `smixs-NOTICE.txt` | https://github.com/smixs/visual-skills/blob/main/NOTICE | CC BY 4.0 attribution required for Visual Skills |
| `mlx-video-readme.md` | https://github.com/Blaizzy/mlx-video | native MLX video: LTX-2/2.3, Wan 2.1/2.2, LoRA, upscale |
| `mlx-video-with-audio-readme.md` | https://github.com/james-see/mlx-video-with-audio | LTX-2 T2V/I2V with synchronized audio on MLX |
| `latentsync-mlx-readme.md` | https://github.com/sb1992/latentsync-mlx | LatentSync lip-sync on Apple MLX |
| `hunyuanvideo-1.5-readme.md` | https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5 | 8.3B open video model |
| `musetalk-1.5-mlx.html` | https://huggingface.co/mlx-community/MuseTalk-1.5-fp16 | MuseTalk 1.5 MLX weights |
| `modelfit-local-video-mac.html` | https://modelfit.io/guides/local-video-generation-mac/ | Mac RAM tiers and model fit |
| `vcarl-apple-silicon-video.md` | https://github.com/vcarl/benchmark-local-llms/blob/main/local-video-generation-apple-silicon.md | indicative Apple Silicon video benchmarks |
| `text-flora.html` | https://flora.ai/guides/best-ai-image-model-for-readable-text-in-images | text-rendering comparison |
| `text-moda.html` | https://moda.app/resources/models/prompts/text-poster | 20-model poster/text test |
| `text-invideo.html` | https://invideo.io/blog/best-ai-model-text-in-images/ | typography compared by job |
| `text-toolcolumn.html` | https://www.toolcolumn.com/learn/best-ai-image-generator-for-text-in-images | text-in-image model survey |
| `text-kenerate.html` | https://kenerateai.com/blogs/best-ai-image-generator-for-text-2026 | eight-model comparison |

## Additional sources cited but not archived here

- Veo API status (preview retirement 2026-10-22): https://ai.google.dev/gemini-api/docs/video
- Fountain syntax: https://fountain.io/syntax
- ffmpeg filters: https://ffmpeg.org/ffmpeg-filters.html
- Suno MCP: https://suno.com/mcp
- DirectorSKILL (MIT): https://github.com/wuwangzhang1216/DirectorSKILL
- Visual Skills (CC BY 4.0): https://github.com/smixs/visual-skills

## Licence note

The Refay and Visual Skills material is CC BY 4.0 and requires attribution. Attribution
lives in `character-design/references/NOTICE-refay.md`, `film-directing/NOTICE`,
prompt-craft corpus NOTICE (in `film-directing/references/prompt-craft/`, adapted from Serge Shima visual-skills, CC BY 4.0), and `ai-image-art-direction/NOTICE`. DirectorSKILL is MIT;
its licence text is in `film-directing/LICENSE`.
