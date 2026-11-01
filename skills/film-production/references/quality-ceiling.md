# Quality Ceiling and the Pilot Test

**Question this answers:** TikTok shows fully AI series that look photorealistic, with
realistic lip-sync and distinct consistent voices. Does this pipeline fully enable equal
quality?

**Short answer:** it fully enables the **workflow**; it does not by default produce equal
**quality**. The ceiling is set by the model tier, the hardware, the iteration budget and
the craft. The pipeline's job is to make those constraints explicit and to test them before
a series commits.

---

## What the reference series are usually doing

- **Model tier:** cloud video models with native audio/lip-sync — Veo 3.x, Kling 4.0,
  Seedance 2.5, MiniMax H3 — or a high-end local GPU. Open local models are close for
  stylized work and behind for photoreal human faces in motion.
- **Shot design:** one or two characters, close-ups, simple blocking, 1–3 second cuts,
  limited hands, crowds and complex action. The format hides model weaknesses.
- **Consistency:** a locked hero image or short reference video per character, often a
  LoRA, fixed seeds and a frozen model version.
- **Voices:** cloned or trained voices, one voice ID per character, reused across episodes.
- **Lip-sync:** native model dialogue or a dedicated pass, then face restoration and
  upscaling.
- **Post:** grade, grain, sound design, music; many takes per shot, cherry-picked.
- **Hybrid reality:** some "fully AI" series use stock, real plates, or a real actor for a
  hero shot. The claim is not always literal.

---

## Where this pipeline stands

| Layer | Pipeline coverage | Local quality today |
|---|---|---|
| Story, characters, series bible | full, with rubric and review gates | not the bottleneck |
| Design, identity locks, continuity ledger | full | strong if the packs and LoRAs are built |
| Keyframes / key art | full | good (FLUX.2, Qwen-Image); not top-tier photoreal |
| Video | full | LTX-2.3 q4 and Wan 2.2 5B/I2V q8 are good, below Kling/Veo/Seedance for photoreal humans; LTX-2.5 q8 is better but 63 GB and slow |
| Lip-sync | step exists; tools not installed yet | MuseTalk/LatentSync can be good on close-ups; profiles, teeth, occlusion and fast speech still fail |
| Voices | full casting sheet and TTS path | Qwen3-TTS/Chatterbox/F5/VibeVoice give distinct, consistent voices; performance is flatter than ElevenLabs-class |
| Edit, sound, grade, delivery | full | depends on the mix, not the pipeline |
| Iteration | logged, variants, retries | throughput is the constraint: 5–10× slower than a 4090 |

---

## The honest gaps

1. **Photoreal human motion.** The best local generator for this is Wan 2.2 I2V-A14B q8,
   not the LTX q4 default. It is ~40 GB, slower, and still below the cloud leaders.
2. **Lip-sync on generated faces.** The step exists and the model options are known, but
   nothing is installed or tested. Native-dialogue models are better; local lip-sync needs
   a pilot to judge.
3. **Voice performance.** Consistency is solvable with voice IDs and reference audio.
   Emotional range and naturalness are the weak point; EQ, compression and room tone help,
   but do not equal a trained performer.
4. **Resolution and finish.** Local output is typically 512–1080p. Upscaling adds sharpness,
   not detail. The best social work is 1080p with a polished grade.
5. **Iteration budget.** Reference series are curated from many takes. A local 60-second
   pilot with 20 shots and 3–5 variants each is already hours; a 10-minute episode is a
   multi-day campaign.

---

## Three routes

| Route | What it buys | What it costs |
|---|---|---|
| **Local-only** | privacy, no per-shot fees, full ownership | lower photoreal ceiling; slower; needs LoRAs, lip-sync and post to close the gap |
| **Hybrid** | local for story, design, keyframes, coverage, animatic; cloud for the 10–20% face/dialogue shots | per-shot spend and a non-local dependency on the hero shots |
| **Craft-first local** | write for the format: two characters, one location, close-ups, no crowds or complex hands, singles for dialogue | narrower stories; still below cloud photoreal |

Do not promise TikTok parity on the local-only route before the pilot below.

---

## The pilot test

**Spec:** 60–90 seconds, two principals, one location, 15–20 shots, four to six dialogue
lines, one close-up per lead, one two-shot, one insert, one transition.

**Hold constant:** script, keyframes, character references, voice IDs, aspect, edit.

**Run three ways:**

1. LTX-2.3 q4 — speed baseline.
2. Wan 2.2 I2V-A14B q8 — local quality.
3. One cloud model, only if the user permits it for comparison — Veo/Kling/Seedance.

**Score blind**, 1–5, against one reference TikTok clip:

| Dimension | 1 | 3 | 5 |
|---|---|---|---|
| Identity | different person | recognisable, small drift | indistinguishable from the reference |
| Lip-sync | wrong or drifting | acceptable on close-ups | indistinguishable |
| Realism | plastic / uncanny | acceptable for social | photoreal |
| Voice consistency | changes between lines | stable, slightly flat | stable and performed |
| Emotional read | absent | legible | compelling |
| Artifacts | unusable | occasional | none |

**Pass for a parity claim:** identity ≥ 4, lip-sync ≥ 3.5, realism ≥ 3.5, voice consistency
≥ 4, emotional read ≥ 3, and no hard artifact. Anything below means: do not promise parity.

**Also record:** seconds per accepted shot, number of takes per accepted shot, GPU-hours,
cloud spend, and the failure codes from `film-generation`.

---

## Decision rule

- If the local pilot passes, commit to the local route and the format it proved.
- If it fails on identity or lip-sync, either adopt the hybrid for face/dialogue shots or
  restrict the format (fewer faces, more inserts, stylized medium, voice-over).
- If it fails on realism only, decide whether the audience accepts the look; do not spend
  weeks re-rolling a model that cannot reach it.
- Re-run the pilot after a model upgrade. The ceiling moves; the test is the same.

The pilot is the measurement. Model cards, demos and "fully AI" claims are not.
