# QC and Delivery

## Technical QC

| Check | Command / method | Pass |
|---|---|---|
| Duration | `ffprobe` | within target ±1 s |
| Resolution | `ffprobe` | exact delivery size |
| Frame rate | `ffprobe` | constant, planned rate |
| Codec / profile | `ffprobe` | H.264 High / H.265 / ProRes as specified |
| Audio | `ffprobe` | 48 kHz, stereo or 5.1, AAC/PCM |
| Bitrate | `ffprobe` | platform minimum met |
| Black frames | `blackdetect` | none outside intended |
| Freeze | `freezedetect` | none unintended |
| A/V drift | spot-check first/middle/last | sync within 1 frame |
| Loudness | `loudnorm` | target ±1 LU |
| True peak | `loudnorm` | ≤ −1 dBTP |
| Captions | play first/middle/last cue | in sync, legible |
| Safe areas | overlay check | titles inside action/title safe |

## Continuity QC

- [ ] Character identity holds across scenes.
- [ ] Wardrobe and injury states follow the ledger.
- [ ] Props are present, in the correct hand, in the correct state.
- [ ] Screen direction and eyelines match across cuts.
- [ ] Light direction and time of day are consistent within a scene.
- [ ] Palette follows the color script.
- [ ] No unexplained location geography changes.

## Artifact QC

- [ ] Hands and fingers.
- [ ] Text, logos, watermarks.
- [ ] Warping, flicker, duplicated limbs.
- [ ] Teeth, ears, eyes.
- [ ] Background extras appearing or vanishing.
- [ ] Reflections and mirrors.

## Legal and disclosure

- [ ] Music licences for every track, including generated music's terms.
- [ ] Footage and stock licences.
- [ ] Consent for any real person depicted.
- [ ] AI disclosure per platform and jurisdiction.
- [ ] Rating and content warnings.
- [ ] Credits accurate.

## Delivery manifest

```markdown
# Delivery Manifest — <title>

| File | Spec | Duration | Size | SHA-256 |
|---|---|---|---|---|
| final_16x9_1080p.mp4 | H.264 High, 1920×1080, 24 fps, AAC 320k | 00:08:12 | 412 MB | ... |
| final_9x16_1080p.mp4 | H.264 High, 1080×1920, 24 fps, AAC 320k | 00:08:12 | 398 MB | ... |
| archive.mov | ProRes 422 HQ, 1920×1080, 24 fps, PCM 24-bit | 00:08:12 | 18.2 GB | ... |
| captions.srt | UTF-8, 42 cues | — | 4 KB | ... |
| poster.jpg | 1920×1080 | — | 820 KB | ... |

**Loudness:** −14.2 LUFS integrated, −1.1 dBTP true peak
**AI disclosure:** <text>
**Licences:** <list>
**Delivered:** YYYY-MM-DD
```

Checksums:

```bash
shasum -a 256 05_post/deliver/* > 05_post/deliver/SHA256SUMS
```

## Platform presets (starting points)

| Platform | Aspect | Resolution | Codec | Notes |
|---|---|---|---|---|
| YouTube | 16:9 | 1920×1080 / 3840×2160 | H.264 | −14 LUFS, faststart |
| YouTube Shorts | 9:16 | 1080×1920 | H.264 | native vertical, captions |
| TikTok / Reels | 9:16 | 1080×1920 | H.264 | safe areas, burned captions often preferred |
| Broadcast | 16:9 | 1920×1080 | ProRes / XDCAM | −23 LUFS, R128 |
| Archive | source | source | ProRes 422 HQ | stems + project files |

Confirm current platform specs at delivery; they change.

## Archive

Keep:

- Masters and stems.
- Project file / timeline / EDL or OTIO.
- `prompt.json` for every approved take.
- `generation-log.csv` and `continuity-failures.md`.
- Design locks and the final continuity ledger.
- Process notes.

The archive is what makes a sequel, a re-cut, or a dubbing pass possible without
regenerating the film.
