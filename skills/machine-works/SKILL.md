---
name: machine-works
description: Build how a machine or object works as one self-contained offline HTML page, using the engine the ask calls for — a hand-inked flat-colour isometric SVG figure (everyday objects: toaster, washing machine, vending machine, espresso, claw machine, lamp) with drag-to-turn, See-through, labels and buttons, or a mechanically faithful three.js 3D simulator (real machines: V8 engine, landing gear, walking linkage, pump, gearbox) with live panels driven by the same model that moves the parts, cutaway camera modes, an auto tour, and a record step that turns it into a 60 fps film with a synced procedural score. Use when someone asks how a machine works, wants a "visual explainer", a "simulator", a "cutaway", an "exploded view", an "interactive 3D lesson", a "Colorfigures" figure, a "what's inside X" figure, or a playable illustrated object. Dark glowing line-art → iso-glow instead.
---

# Machine Works

One subject, one page, two engines. Both share one doctrine (below); they differ in rendering physics and
output. Read the routing table, pick an engine, then work from that engine's own file — **`engines/ink/ENGINE.md`**
or **`engines/webgl/ENGINE.md`** — which holds the full workflow, traps and checklists for that engine. This file
is only routing and the rules the engines share.

`ENG` below is the engine folder: `<this skill>/engines/ink` or `<this skill>/engines/webgl`.

## Choose the engine

| Signals in the ask | Engine | Output | Capabilities unique to it |
|---|---|---|---|
| Illustrated, hand-inked, sketchy, flat colour, warm paper; everyday objects and appliances; "what's inside"; works on a phone | **ink** (SVG painter's-algorithm, no depth buffer) | One HTML page via `python3 "$ENG/scripts/build.py" figure.html OUT.html` | Full phone layout (numbered badge labels + list), real-object research with a 30–60 part see-through, painter's-sort discipline |
| Simulator, 3D, cutaway, exploded, engine/aircraft/linkage/pump/gearbox, "show it running", video, film, animation, sound | **webgl** (three.js/WebGL) | One offline HTML page via `node "$ENG/sims/build.mjs" <name>` (-live), plus `-film` variants | Deterministic `render(t)` frame capture to 60 fps mp4, review sheets, procedural score synced to the film timeline, auto tour with cursor and handoff, cutaway camera modes, GPU quality tiers |
| Style is unstated | Everyday object/appliance, no film mentioned → **ink**. A real large machine, a mechanism study, or film/video asked → **webgl** | | |
| Not renderable here | Dark glowing line art → **iso-glow** | | |

When both looks would serve, ask the owner once. Never blend the engines on one page.

## First run

- **ink**: nothing to install. `python3 build.py` is stdlib-only. Verify renders need headless Chrome.
- **webgl**: `cd "$ENG" && npm install && npx playwright install chromium`; video needs `ffmpeg` on PATH, sound
  needs Python 3 (stdlib only).

## Shared doctrine (both engines enforce this)

1. **Truth first.** Start from a reference — a photo, a manual cutaway, a clip of the real thing — never from
   imagination. Write how the object really works as ordered steps and where every material goes after each step
   (coin → chute → acceptor → cash box). Build against the reference and compare frame by frame.
2. **Real numbers, one source.** Get the real dimensions first. Every gauge, label, clearance and motion
   reads from the same constants that pose the parts; nothing on screen can disagree with the motion. Check one
   measurement by hand.
3. **One input drives everything.** One state (crank angle, stroke, wind, button press) drives every pose and
   readout through the real process. Nothing is keyframed by hand, so page, film and score never drift.
4. **The part doing the work opens up.** See-through / cutaway / isolate. A camera that goes inside is worth
   more than ten orbits. The normal closed view is the real object; the reveal is a switch, not the default.
5. **Every part is held by another, and every driver touches what it drives.** Nothing floats; cables run
   port to port; contact points worked out with numbers; moving paths clear every obstacle numerically.
6. **One accent, and it means something.** The accent marks the part working right now. Labels name parts that
   are drawn, sit anchored on their part, and never cover what they name.
7. **Verify by rendering, never by hoping.** You cannot watch a page run; you look at frames. Every engine has
   its own loop — ink: headless Chrome across 7 yaw/pitch angles, closed and see-through, press sequences,
   error-DOM check, phone shot. webgl: `--stills beats` review sheets, zoomed `--still T` passes, a final sheet
   from the encoded video. Read every tile. Stop when a full pass finds nothing.
8. **Neat over busy.** The subject fills 60–70% of the frame; nothing important within 60 px of an edge;
   repeated details read at normal size; every state holds long enough to read.

## Engine boundaries

- Film recording, procedural sound, the auto tour and the GPU/perf tiers exist only in webgl. Do not promise a
  video from an ink figure.
- Depth sorting, painter's-algorithm z-order and the phone badge-list label behaviour exist only in ink. Do not
  promise a phone label list from a webgl page.
- Engines live beside each other; take an example from the engine you are writing in (
  `engines/webgl/sims/` V8 / Cessna / Strandbeest, `engines/ink/assets/examples/` toaster / lamp / claw)
  and copy the closest one rather than starting from nothing.

## Credits

- **ink** engine: [April Zhu's colorfigures](https://april-zhu.com/colorfigures) — licence in `engines/ink/LICENSE`.
- **webgl** engine: [elvarofficial/teardown](https://github.com/elvarofficial/teardown) (MIT, derived from
  whaleyxbt/claude-motion, CC0 Freesound samples) — licence in `engines/webgl/LICENSE`.