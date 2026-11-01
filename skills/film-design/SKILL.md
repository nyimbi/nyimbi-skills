---
name: film-design
description: >-
  Build the visual and aural world of a film or series so it survives production: one locked
  style, a world bible with a key frame and floor plan per location, props and set dressing,
  the continuity system, and the character asset packs (routed to character-design). Use when
  the user says "design the world", "set the look", "make a style bible", "design the
  locations", "keep the film visually consistent", or when a locked script needs to become
  reference assets before storyboarding. Do not use for writing the story (see
  film-story-development), for shot planning (see film-directing), or for generating the film
  (see film-generation).
---

# Film Design

Production design for an AI-made film. The job is to make the **same world** come back in
every shot, in every episode, without re-deciding what it looks like. Design is where a
film becomes cheap or expensive: a locked style and a reference set turn generation into
execution; an unlocked one turns it into a slot machine.

> **Pipeline position.** Stage 2 of `film-production`. Consumes the locked script and
> series bible; writes `02_design/`; hands `style-lock.md`, the character packs, the world
> bible, and `continuity-ledger.md` to `film-directing` and `film-generation`.
> Character asset packs are built with **character-design**, one per principal.

## Inputs

- `01_story/LOCK.md`, `screenplay.fountain`, and `series-bible.md`.
- The format, runtime, aspect, budget tier, and target models.
- Any user references: films, paintings, photographs, places, casting, existing art.
- The AI-risk list from story development (crowds, hands, text, action, water).

## Step 1 — Production design brief

Before choosing a look, write what the world must **express**:

| Story pressure | Design answer |
|---|---|
| The protagonist is trapped | spatial compression, low ceilings, corridors, frames within frames |
| The world is dying | material decay, desaturation, practical light failing |
| The family is wealthy but cold | scale, symmetry, hard surfaces, distance between bodies |
| The story is about performance | mirrors, stages, costume changes, visible audience |
| The era is contested | one anachronism that is the point, not an accident |

Write `02_design/design-brief.md` with the visual thesis in one testable sentence: "the
house gets larger and emptier as the family shrinks", not "wealth and loneliness".

## Step 2 — Style lock

One style target, no mixing. Write `02_design/style-lock.md`:

```markdown
# Style Lock — <project>

**Medium:** live action | painterly 2D | 2.5D cutout | 3D animation | stop motion | mixed
**Reference frames:** <3–6 images, each with what it contributes>
**Palette:** <three dominant colors + one accent, with hex or named pigment>
**Lens kit:** <range in mm; the two lenses the film actually uses>
**Depth and grain:** <deep/shallow; clean/grain; halation; bloom>
**Lighting grammar:** <key direction, ratio, practicals, color temperature>
**Camera grammar:** <locked / handheld / dolly; the allowed moves>
**Aspect / fps / resolution:** <e.g. 16:9 / 24 / 1920×1080>
**Era and place:** <period, region, class markers>
**Negative constraints:** <named instances only: no plastic, no modern logos, no text>
```

Rules:

- **Three colors plus one accent.** More is a mood board, not a palette.
- **Two lenses.** A film that uses every focal length has no visual grammar.
- **Named negatives.** "No modern objects" is unrenderable; "no plastic, no LED, no printed
  logos" is actionable.
- **One medium.** A painterly hero shot and a photoreal close-up cannot share a film.
- **Test the lock** on three subjects: a face, a location, and a prop. If the look does not
  survive all three, it is not locked.

## Step 3 — World bible

One entry per recurring location. Each entry must be usable by a stranger:

```markdown
## <Location name>

- **Story function:** what scenes happen here and what the space must do
- **Architecture and materials:** structure, surfaces, wear, era
- **Palette and light:** local colors, key direction, practicals, time of day
- **Geography:** entrances, exits, windows, sightlines, the 180° line for dialogue
- **Floor plan:** `02_design/floorplans/<slug>.png` — top-down, with camera positions
- **Establishing frame:** `02_design/refs/locations/<slug>/establishing.png`
- **Reverse angle:** `.../reverse.png`
- **Ambient sound:** room tone, HVAC, street, water, crowd off-screen
- **Props and set dressing:** the objects that carry story weight
- **Continuity facts:** what changes across the story (damage, season, time)
```

Rules:

- **One establishing frame per location**, approved before any shot uses it.
- **A floor plan for any location with more than one camera angle.** The model cannot infer
  where the last shot put the camera; the plan is how you encode it.
- **Design for the coverage you need**, not for a beauty shot: a room with one good angle
  is a room with one shot.
- **Ambient sound is part of the design.** A continuous bed is the cheapest continuity glue
  in the film.

Template: `references/world-bible-template.md`.

## Step 4 — Characters

For each principal and recurring supporting character, run **character-design**. It
produces the psychology-to-visual translation, the 60–120 word identity block, the five-view
sheet, expression and wardrobe variants, the hero frame, voice casting, and the drift audit.

Do not write a character's identity block here and a different one there. `character-design`
owns it; this skill only ensures the set is complete and consistent with the world.

## Step 5 — Props and set dressing

Props are continuity objects. For each story-bearing prop:

| Field | Answer |
|---|---|
| Function | what it does in the plot |
| Shape and material | what it is made of, how it wears |
| Scale | relative to hands and rooms |
| Color | palette position |
| States | new → worn → broken → repaired; who has it when |
| Reference | `02_design/refs/props/<slug>/{front,detail,state}.png` |
| Text/logo | whether it must be legible; if so, plan it as a post insert |

Small, handheld props are the hardest generation target. Design them to be shown in
inserts, not manipulated in wide shots.

## Step 6 — Continuity system

The design is only locked if the continuity system can enforce it. Write
`02_design/continuity-system.md` and seed `continuity-ledger.md`:

- **Canonical blocks** — identity strings, location blocks, prop blocks, style lock.
- **Reference array order** — the fixed order references are passed to each model
  (character first, then location, then style, then prop), because positional reference
  tokens matter.
- **Seeds and model versions** — the model version is frozen per project; a model update is
  a project decision, not a silent upgrade.
- **LoRA plan** — any character or location in more than ~20 shots gets a trained adapter or
  a dedicated reference set.
- **Drift audit schedule** — after keyframes, after every 10 approved shots, and at episode
  boundaries.
- **Change protocol** — a design change after lock is a versioned revision with a re-audit.

Details and the drift taxonomy: `references/continuity-system.md`.

## Step 7 — Design lock

Produce `02_design/LOCK.md`:

```text
Version: 1.0
Locked: YYYY-MM-DD
Style lock: 02_design/style-lock.md
Characters: N packs, N approved sheets, N hero frames, N voices
Locations: N, each with establishing frame + floor plan
Props: N, each with reference and state list
Continuity system: current, ledger seeded
Known risks: ...
Change policy: versioned revisions only; re-audit after any change.
```

Do not hand an unlocked design to shot planning. Every unresolved choice becomes a
regeneration.

At design lock, hand the style lock, hero frames and logline to `film-poster` so key art
starts from the same look. The poster's final type and credits wait for picture lock.

## Quality gate

- [ ] Visual thesis is one testable sentence.
- [ ] One style target; three colors + accent; two lenses; named negatives.
- [ ] Style test survives a face, a location, and a prop.
- [ ] Every principal has a character pack and a passed drift audit.
- [ ] Every recurring location has an establishing frame, reverse angle, and floor plan.
- [ ] Every story prop has references and a state list.
- [ ] Reference array order, seeds, and model versions are written down.
- [ ] Continuity ledger is seeded and matches the design files.
- [ ] `LOCK.md` exists and the user has approved the look.

## Reference map

| File | Contents |
|---|---|
| `references/style-lock.md` | style-lock fields, test protocol, palette and lens recipes |
| `references/world-bible-template.md` | location, floor-plan, prop, and ambient-sound templates |
| `references/continuity-system.md` | reference order, seeds, model freezing, LoRA thresholds, drift audit |
| `character-design` | per-character pack: sheet, identity lock, voice, drift audit |
