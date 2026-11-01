# World Bible Template

One entry per recurring location, one block per story prop, one ambient-sound plan. Keep it
usable by someone who has never seen the film.

## Location entry

```markdown
## <Location name>

**Story function:** <scenes, and what the space must do dramatically>

**Architecture:** <structure, era, condition>
**Materials:** <surfaces, wear, texture>
**Palette:** <local colors and their place in the film palette>
**Light:** <key direction, color temperature, practicals, time of day>
**Geography:** <entrances, exits, windows, sightlines, the 180° line>
**Scale:** <how many people fit; how the lead looks in it>

**Floor plan:** `02_design/floorplans/<slug>.png`
**Establishing frame:** `02_design/refs/locations/<slug>/establishing.png`
**Reverse angle:** `02_design/refs/locations/<slug>/reverse.png`
**Detail plates:** <door, table, window, texture>

**Ambient sound:** <room tone, HVAC, street, water, off-screen crowd>
**Set dressing:** <the objects that carry story weight>
**Continuity:** <what changes across the story: damage, season, time, ownership>
**Generation risks:** <reflections, windows, crowds, water, text>
```

Rules:

- A location used from more than one angle needs a floor plan before the shot list.
- Every location needs one approved establishing frame and one reverse.
- Design the angles the coverage needs; a beautiful single angle is a single shot.
- Write the ambient sound now; it is the cheapest continuity glue in the film.

## Prop entry

```markdown
## <Prop name>

**Function:** <what it does in the plot>
**Shape and material:** <what it is, how it wears>
**Scale:** <relative to hands and rooms>
**Color:** <palette position>
**States:** <new → worn → broken → repaired; who holds it when>
**Text/logo:** <legible? if yes, plan a post insert>
**References:** `02_design/refs/props/<slug>/{front,detail,state}.png`
**Generation risk:** <hands, reflection, fine detail>
```

## Ambient and sound plan

| Location | Room tone | Continuous bed | Spot effects | Music |
|---|---|---|---|---|

The continuous bed is the layer that survives cuts and hides visual drift. Plan it before
generation so the edit has something to cut against.

## World rules (for genre and series work)

| Rule | What is possible | What it costs | Who knows |
|---|---|---|---|

Only write rules the story tests. An unused rule is decoration.

## Design lock checklist

- [ ] Every recurring location has a full entry and both frames.
- [ ] Every multi-angle location has a floor plan.
- [ ] Every story prop has references and a state list.
- [ ] Ambient sound is planned per location.
- [ ] Continuity facts are copied into `continuity-ledger.md`.
