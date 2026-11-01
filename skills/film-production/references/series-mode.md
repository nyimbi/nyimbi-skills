# Series Mode

A season is one design and many episodes. Develop and design once; loop production.

## Season grid

Write before episode one:

| # | Title | Promise | A-plot | B-plot | Turn | Cliffhanger | New canon |
|---|---|---|---|---|---|---|---|
| 1 | | | | | | | |
| 2 | | | | | | | |

- **Promise** is what the episode delivers on its own.
- **New canon** is what enters the continuity ledger. Empty means filler.
- The season question is answered in the finale; every episode tightens it.

## Production loop

```text
design lock (season)
  → for each episode:
      plan (shot list, boards, animatic)
      → generate
      → assemble
      → sound
      → finish
      → QC
      → update ledger
  → season QC and delivery
```

## Batch by asset, not by episode

When practical, generate across adjacent episodes:

- All shots in one location.
- All shots of one character.
- All shots that share a light setup.

This reduces drift and model reloads. It costs edit flexibility, so batch only after the
episode cuts are locked.

## Pilot first

Produce episode 1 fully, pass every gate, then commit. A pilot is the cheapest test of
whether the look, the cast, and the pipeline hold for a season. If the pilot fails
identity at shot 40, the season would have failed at every episode boundary.

Run the blind quality comparison in `quality-ceiling.md` on the pilot before committing:
same script, keyframes and voices across the local video engines, plus one cloud model only
if the user permits it. Score identity, lip-sync, realism, voice consistency and emotional
read against a reference clip. The scores, the cost per accepted shot and the decision
(local, hybrid, or a narrower format) go into `decision-log.md`.

## Continuity across episodes

Update `continuity-ledger.md` after each episode:

- Wardrobe and body state.
- Injuries and healing.
- Props and ownership.
- Knowledge states: who knows what, and when they learned it.
- Relationships and power balance.
- Time of day and elapsed time.
- Locations: damage, season, ownership.

At each episode boundary, run the drift audit on every recurring character.

## Asset reuse

- Character packs, location plates, prop refs, voices, and style lock are season assets.
- Reuse the **hero frame** per character per episode, re-approved against the sheet.
- Do not retrain a LoRA per episode; version it only if the character changes.
- Keep a season-level `assets/` index so a new episode does not rebuild what exists.

## Release shape

- Vertical micro-drama: batch 5–10 episodes, release on a cadence, cut each on a hook.
- Narrative series: pilot + season; deliver per-episode masters and a season trailer.
- Keep the season bible current; it is the contract for any later episode or re-cut.
