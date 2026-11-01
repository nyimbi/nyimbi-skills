---
name: character-design
description: >-
  Design one character so they survive hundreds of generations: psychology into a canonical
  visual identity, a five-view reference sheet, expression and wardrobe variants, a hero frame,
  a verbatim identity-lock block, voice casting, and a drift audit. Use when the user says
  "design this character", "make a character sheet", "keep this character consistent", "cast a
  voice for her", "why does the face change between shots", or when film-design needs a lead's
  asset pack built. Do not use for the whole world or style lock (see film-design), for
  shot planning (see film-directing), or for writing the character's role in the story
  (see film-story-development).
---

# Character Design

A character is not a portrait. It is a **contract**: a fixed set of visual and vocal facts
that every downstream department repeats without paraphrase. This skill builds that
contract and the evidence that it holds.

> **Pipeline position.** A building block of `film-design`, used per principal. Consumes
> `01_story/characters/<slug>.md`; writes `02_design/characters/<slug>.md`,
> `02_design/refs/<slug>/`, and one block of `continuity-ledger.md`.

## Inputs

- The character's page from story development: want, need, wound, false belief, arc, voice,
  relationships.
- The locked style: medium, palette, lens, grain, aspect, era.
- Any user-supplied references or casting preferences.
- The shot count and whether the character is a lead (identity risk scales with screen time).

## Step 1 — Psychology into visible facts

Translate each psychological field into something a camera can see:

| Story field | Design consequence |
|---|---|
| Wound | a habit, a guarded body part, a object they never put down |
| False belief | a costume or grooming choice that expresses it |
| Want | the prop or garment they reach for under pressure |
| Need | the thing they avoid wearing or showing |
| Arc | a controlled change in wardrobe, hair, or posture across the story |
| Relationships | relative height, color proximity, who is framed above whom |
| Voice | pitch, pace, accent, vocabulary, verbal tic, silence pattern |

Write these into `02_design/characters/<slug>.md` under "Psychology → visible".

## Step 2 — Canonical visual identity

Write a **60–120 word block** that another person could use to draw the character without
seeing the references. It must include:

- Age range, build, height relative to the cast.
- Skin tone, face shape, nose, jaw, eyes, brows.
- Hair: color, texture, length, and how it is worn in this story.
- Wardrobe: every garment, color, material, condition, and what is carried.
- Two or three **drift-prone features** named explicitly (curl pattern, scar, hat, coat
  color, missing finger, glasses).
- One **silhouette fact** — what reads at a distance.
- Era and class markers.

Rules:

- No comparative references ("like a young Hepburn"). Describe the properties.
- No emotions in the identity block. Emotion belongs to the shot.
- No props that change state unless the state is named.
- Use concrete colors (hex or named pigment), not "warm".

This block is the **identity string**. It is repeated verbatim in every prompt. Paraphrase
is drift.

## Step 3 — Reference sheet

Generate a five-view sheet before any video:

```text
Character sheet, five views on a neutral background:
front, three-quarter left, profile, back, face close-up.
[Identity block verbatim]
[Style lock: medium, palette, lens, grain]
Neutral expression. Even light. No props unless canonical.
```

Then add:

- **Expression sheet** — neutral, joy, fear, anger, grief, thought. Same lighting.
- **Wardrobe variants** — only the states the story actually uses (before/after injury,
  act change, disguise).
- **Hero frame** — the character in the story's key light and location, at the aspect
  ratio. This is the reference that wins most identity checks.
- **Detail refs** — hands, jewelry, scar, shoes, the object they carry.

Approve each sheet by eye before it enters the reference set. A bad sheet poisons every
shot that uses it.

Prompt syntax for the image model lives in `ai-image-art-direction`; use that skill for
the actual prompt, then return here with the approved files.

## Step 4 — Identity lock

Write the lock block exactly as it will be pasted:

```text
IDENTITY LOCK — @mara: [identity string verbatim].
Do NOT change: tight auburn curls; scar through left eyebrow; grey wool coat, torn
left cuff; bare hands, no gloves.
100% matches reference.
```

Add **inline reminders** for the features that drift in specific shot types:

- Hands in frame → "bare hands, fingers uncovered".
- Headwear → "hat stays on" / "no head covering".
- Coat color → "grey wool coat, not black".
- Hair texture → "tight auburn curls, not wavy".

The lock block lives in `02_design/characters/<slug>.md` and is copied into the ledger.

## Step 5 — Voice casting

Voice is identity too. Cast before dialogue is generated.

| Field | Decision |
|---|---|
| Provider | local F5-TTS, ElevenLabs, Piper, other |
| Voice ID / reference audio | exact ID or file path |
| Seed / settings | reproducible parameters |
| Pitch and pace | relative to the cast |
| Accent and register | match the world and class |
| Verbal tic | the one habit the actor would use |
| Pronunciation guide | names, places, invented words |
| Performance notes | what this voice does under pressure |

Record a **reference line** per character (the same sentence for every character, so the
cast can be compared) and store it in `02_design/refs/<slug>/voice.wav`. Use the same
sentence for all: "I told you the truth, and you chose not to hear it."

## Step 6 — Drift audit

Before design lock, run the character through a consistency test:

1. Generate the same close-up from three different prompts (front, three-quarter, profile)
   using only the identity block and refs.
2. Compare: face geometry, hairline, scar, eye color, wardrobe, silhouette.
3. Score pass/fail per feature. A feature that fails twice gets a stronger explicit clause
   or a dedicated reference crop.
4. If the character appears in more than ~20 shots, plan a LoRA or a dedicated reference
   set; re-rolling is more expensive than training.

Record the audit in the character file. Do not lock a lead with an unresolved fail.

## Step 7 — Ledger entry

Add or update the character's block in `continuity-ledger.md`:

```markdown
## @mara
- identity: <verbatim block>
- refs: 02_design/refs/mara/{sheet.png,hero.png,hands.png,voice.wav}
- voice: <provider + id + seed>
- wardrobe: <state at E01> → <state change at E0N>
- body: <injuries, hair changes, age changes>
- knows: <knowledge state per episode>
- relationships: <who, what balance>
```

## Quality gate

- [ ] Identity block is 60–120 words, concrete, and free of comparative references.
- [ ] Five-view sheet, expression sheet, hero frame, and detail refs exist and are approved.
- [ ] Three drift-prone features are named, with inline reminders.
- [ ] Voice is cast, sampled, and reproducible.
- [ ] Drift audit passed; no unresolved feature failure for a lead.
- [ ] Ledger block is complete and matches the reference paths.

## Reference map

| File | Contents |
|---|---|
| `references/character-sheet-prompts.md` | sheet, expression, wardrobe, hero-frame prompt templates |
| `references/identity-and-drift.md` | the identity string recipe, drift causes, LoRA/reference strategy |
