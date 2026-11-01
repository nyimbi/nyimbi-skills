# Canonical Shot Record

One shot, all facts, no dialect. The compiler turns it into each model's prompt.

## Schema

```json
{
  "id": "S01_SH010",
  "scene": "S01",
  "duration_s": 4.0,
  "function": "establish | relation | close | insert | reaction | transition | aftermath | pov | reveal",
  "shot_size": "extreme wide | wide | medium | medium close | close | extreme close | macro",
  "lens_mm": 24,
  "angle": "eye level | low | high | overhead | dutch",
  "subject": "who or what the shot is about",
  "action": "one primary action with a visible end state",
  "environment": "place, time, weather, atmosphere",
  "camera_move": "locked | pan | tilt | push | pull | track | handheld | crane",
  "lighting": "key direction, quality, ratio, practicals",
  "audio": "dialogue line, ambience, effect, or silence",
  "negative": "named instances only",
  "characters": ["@mara"],
  "refs": ["02_design/refs/mara/hero.png"],
  "dialect": "veo | kling_t2v | kling_i2v | runway | wan | seedance | omni | ltx | minimax",
  "control": "t2v | i2v | first_last | reference | multishot | v2v",
  "priority": "hero | coverage | insert",
  "risk": ["hands", "water", "text", "crowd"],
  "notes": "anything the compiler must not lose"
}
```

## Required fields by control surface

| Field | T2V | I2V | First/last | Reference | Multi-shot |
|---|---|---|---|---|---|
| subject | yes | from image | from images | yes | yes |
| action | yes | yes | bridge | yes | per segment |
| environment | yes | no (image) | no (images) | yes | overall block |
| camera_move | yes | yes | yes | yes | per segment |
| lighting | yes | no (image) | no (images) | yes | overall block |
| audio | if supported | if supported | if supported | if supported | per segment |
| negative | yes | yes | yes | yes | overall block |
| refs | optional | 1 | 2 | 1–N | 1–N |

## Compiler rules

1. **Never invent a field.** If a required field is missing, fail the shot and name it.
2. **Append the style block verbatim** from `02_design/style-lock.md`.
3. **Append the identity block verbatim** for every character in the shot, in the fixed
   reference order.
4. **Respect the word budget.** Trim environment before action, and action before camera.
5. **Convert negatives per model.** Field, inline, positive restatement, or unsupported.
6. **Write the compiled prompt and the parameters** beside the take; never only in chat.

## Example compilation

Canonical:

```json
{"subject":"Mara at the harbour rail","action":"she sets down a case and keeps her hand on the handle","environment":"grey water, rusted rail, cold dawn","camera_move":"slow push-in","lighting":"low sun camera-left, hard rim","audio":"gulls, water","negative":"no modern boats, no text","dialect":"veo","control":"t2v"}
```

Veo-shaped output:

```text
Mara, late 30s, tight auburn curls, grey wool coat torn at the left cuff, stands at a
rusted harbour rail. She sets down a worn leather case and keeps her hand on the handle.
Grey water, rusted pilings, cold dawn. Slow push-in from a medium-wide, camera at chest
height. Low sun from camera left, hard rim, deep shadow. [style block]. Audio: gulls,
water against pilings. No modern boats. No text.
```

Kling I2V-shaped output (motion only, 15–40 words):

```text
Slow push-in from the approved frame. She sets the case down and keeps her hand on the
handle. Gulls move off-screen. Wind lifts the coat hem once. Do not change her face,
hair, coat, or the light direction.
```

## File discipline

```text
04_gen/shots/S01_SH010/
  hero.png            approved keyframe
  v1.mp4  v2.mp4      takes
  prompt.json         compiled prompt, params, refs, seed, model version
  approved.mp4        the take that passed QA
```

Never overwrite an approved take. A new take is `v3.mp4`; a new shot is `S01_SH010A`.
