# Identity and Drift

Identity drift is not a model bug to be re-rolled. It is a missing constraint. The fix is
a written contract, repeated verbatim, plus references that show the features the words
cannot carry.

## The identity string

Write once, 60–120 words, in this order:

1. **Age and build** — "late 30s, wiry, 175 cm".
2. **Skin and face** — tone, face shape, nose, jaw, eyes, brows.
3. **Hair** — color, texture, length, how worn. Name the texture: "tight auburn curls",
   not "curly hair".
4. **Wardrobe** — every garment, color, material, condition.
5. **Drift-prone features** — two or three, named as absolutes.
6. **Silhouette** — what reads at 20 metres.
7. **Era and class markers**.

Do not include emotion, backstory, or comparative references. Those belong to the shot
or the performance, and comparisons ("like a young X") import an entire face.

## Why drift happens

| Cause | Mechanism | Fix |
|---|---|---|
| Paraphrase | every paraphrase changes token weights; the model recasts | paste the block verbatim, never summarise |
| Reference order | positional reference tokens bind different roles | fix the array order: character, location, style, prop |
| Reference conflict | two refs show different hair or coat | curate the set; one canonical per feature |
| Model version change | weights and training data change the prior | freeze the version per project; a change is a project decision |
| Shot scale | a wide shot gives the model too few face pixels | generate a close-up or medium for identity-critical beats |
| Motion budget | too much action leaves no capacity for identity | one action, one camera move per clip |
| Extreme angle | profile and low angle expose features the refs do not show | add profile and low-angle refs |
| Lighting change | a different key recasts skin tone | carry the light direction in the prompt and the ref |
| Wardrobe state | a costume change is read as a new character | name the state and show a state ref |
| Compression | low bitrate destroys fine features | use a higher-quality master for reference, not a proxy |

## LoRA and reference thresholds

| Screen time | Strategy |
|---|---|
| 1–5 shots | identity block + hero frame + 3-view sheet |
| 6–20 shots | add expression sheet, detail refs, and a fixed seed family |
| 20+ shots, or a series lead | train a character LoRA, or maintain a 10–20 image reference set |
| Recurring across episodes | LoRA plus a locked hero frame per episode, re-audited at boundaries |

Training is cheaper than re-rolling when a lead appears in dozens of shots. Budget it at
design lock, not after the third failed episode.

## Inline reminders

The lock block is necessary but not sufficient. Add the specific clause where the failure
happens:

- Hands in frame: "bare hands, fingers uncovered, five fingers".
- Headwear: "hat stays on in every shot".
- Coat: "grey wool coat, never black".
- Hair: "tight curls, not wavy, not straightened".
- Age: "late 30s, no younger".
- Injury: "left hand bandaged, visible in every shot until E05".

## Drift audit

Run at three points: after keyframes, after every 10 approved shots, and at each episode
boundary.

1. Pull one frame per approved shot.
2. Compare against the hero frame on: face geometry, hairline, eyes, scar, wardrobe,
   silhouette, palette.
3. Score pass/fail per feature.
4. A feature failing twice gets a stronger clause or a dedicated crop.
5. A feature failing three times is a design change, not a prompt change: version it and
   re-audit.

Record results in `04_gen/continuity-failures.md` and update the ledger.

## Cheap continuity glue

- One ambience bed under a sequence hides small visual drift.
- Keep faces relatively large; identity survives at medium and close, not at wide.
- Cut away before a character has to do something the model cannot render.
- Use the same lens and light direction across a scene; a change reads as a different
  world.
- Prefer silhouettes, backviews, and inserts when the story allows them. They are not a
  compromise; they are coverage.

*Methods in this file are adapted from Khaled Al Refay's painterly short-film skill
(IDENTITY LOCK, character sheets, drift prevention), CC BY 4.0. See
`references/NOTICE-refay.md`.*
