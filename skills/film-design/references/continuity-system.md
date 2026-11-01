# Continuity System

Continuity is engineered, not remembered. The system has four parts: canonical blocks,
reference order, seeds/versions, and audits.

## Canonical blocks

Every recurring element has one block, stored once, pasted verbatim:

| Element | Block owner | Stored in |
|---|---|---|
| Character | `character-design` | `02_design/characters/<slug>.md` |
| Location | `film-design` | `02_design/world-bible.md` |
| Prop | `film-design` | `02_design/world-bible.md` |
| Style | `film-design` | `02_design/style-lock.md` |
| Voice | `character-design` | `02_design/voice-casting.md` |

Paraphrase is drift. If a block needs to change, version the file and re-audit.

## Reference order

Positional reference tokens bind roles. Fix one order and never vary it:

1. Character sheet / hero frame
2. Location establishing frame
3. Style frame
4. Prop reference
5. First / last frame for the shot

Record the order in `style-lock.md` and in every `prompt.json`. A model that uses
`[Image 1]`, `@tag`, or an array index will bind differently if the order changes.

## Seeds and model versions

- **Freeze model versions** per project in `state.json`: provider, model ID, version,
  resolution, duration. A provider update is a project decision with a re-audit.
- **Record seeds** for every approved take. A seed is reproducible only with the same
  model version, prompt, references, and parameters.
- **Keep the prompt** beside the take (`prompt.json`), not in a chat log.

## LoRA and reference thresholds

| Screen time | Strategy |
|---|---|
| 1–5 shots | identity block + hero frame |
| 6–20 shots | expression sheet, detail refs (hands, scar, props), fixed seed family |
| 20+ shots or series lead | character LoRA or 10–20 image reference set |
| Recurring across episodes | LoRA + per-episode hero frame + boundary audit |

## Drift audits

Run after keyframes, after every 10 approved shots, and at every episode boundary.

| Feature | Check |
|---|---|
| Face geometry | jaw, nose, eye spacing, brow |
| Hair | color, texture, length, hairline |
| Wardrobe | garment, color, condition, state |
| Body | injury, bandage, scar, age |
| Props | presence, hand, state |
| Screen direction | 180° line, eyeline |
| Light | key direction, color temperature |
| Palette | three colors + accent |
| Silhouette | reads at thumbnail |

A feature failing twice gets a stronger clause or a dedicated reference. Three fails is a
design change.

## Change protocol

```text
1. Name the canonical fact that changes.
2. Version the block: <file>_v2.md or a dated section.
3. Update continuity-ledger.md.
4. Re-audit affected keyframes and approved shots.
5. Record the change in decision-log.md with the reason and the cost.
```

Never silently edit an approved block. The next session will not know it changed.

## Ledger template

```markdown
# Continuity Ledger — <project>

## Canonical
- Style: 02_design/style-lock.md (vN)
- Characters: @mara, @dev, ...
- Locations: ...
- Model versions: ...

## @mara
- identity: <verbatim>
- refs: ...
- voice: ...
- wardrobe: E01 <state> → E0N <state>
- body: ...
- knows: ...
- relationships: ...

## Locations
- <name>: <canonical block>, key frames, state changes

## Props
- <name>: owner, state, location

## Timeline
- E01–E04: three days. E05: one month later.
```

Update it at design lock, after every episode, and after any retake that changes a
canonical fact.
