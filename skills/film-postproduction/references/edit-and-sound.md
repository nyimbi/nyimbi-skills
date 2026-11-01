# Edit and Sound

## Edit grammar

| Decision | Rule |
|---|---|
| Cut point | cut on the change, not after the line |
| Reaction | prefer the face hearing to the event |
| Establishing | enter a scene late; leave before the goodbye |
| J/L cut | sound leads or trails picture at scene changes |
| Montage | each shot must change the idea, not restate it |
| Match cut | build shot A's last frame and shot B's first together |
| Insert | under 2 seconds; one idea; no dialogue |
| Transition | cut by default; dissolve for time/memory; fade only at ends |
| Hold | after the turn, hold longer than feels comfortable |
| Music | cut on the musical accent only when the music is the point |

## Pacing

| Register | Average shot length |
|---|---:|
| Drama | 4–7 s |
| Thriller | 2–5 s |
| Action | 1.5–3 s |
| Comedy | 2–4 s (hold the button longer) |
| Vertical micro-drama | 1.5–3 s |
| Trailer | 1–3 s, with holds on the title |

Generated clips are usually 4–8 s. Trim them; do not let the generator's duration dictate
the film's rhythm.

## Sound layers

```text
DIA  dialogue
ADR  replaced dialogue
AMB  ambience / room tone
FOL  foley
SFX  spot effects
MUS  score
```

- **One ambience bed per sequence.** Crossfade at location changes.
- **Foley only where the ear expects it**: steps, cloth, a handled object, a door.
- **Spot effects are story events**, not decoration.
- **Score** enters when the scene needs an emotional argument the image cannot make alone.
- **Silence** before the turn; let the room carry it.

## Mix targets

| Deliverable | Integrated loudness | True peak |
|---|---:|---:|
| Streaming / web | −14 LUFS | ≤ −1 dBTP |
| Broadcast (EBU R128) | −23 LUFS | ≤ −1 dBTP |
| Cinema-style | −20 to −24 LUFS (dialogue-led) | ≤ −1 dBTP |

Measure with `loudnorm` or a meter. Do not normalize by ear.

## Dialogue rules

- One speaker per clip at generation; split overlaps in post.
- Dialogue sits in front of music; duck music under speech.
- Room tone under every dialogue edit, even a 100 ms fill.
- If a line cannot be understood on first listen, replace it or cut it.
- Keep a **dialogue stem** separate from music and effects.

## Stems

Deliver `dialogue.wav`, `music.wav`, `effects.wav`, and `mix.wav` at 48 kHz/24-bit. Stems are
what make re-versioning, dubbing, and re-mixing possible.

## Picture lock

Lock when:

- The story reads without sound.
- The sound adds meaning, not just coverage.
- Every cut has a reason that is not "the clip ended".
- The runtime is within the delivery target.

After lock, changes are versioned (`cut_v2`), re-mixed, and re-QC'd.
