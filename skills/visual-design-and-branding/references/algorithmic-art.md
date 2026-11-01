# Generative Art — p5.js, Seeded Randomness, Interactive Viewer

Technique file for the generative branch of the [SKILL.md](../SKILL.md) workflow.
algorithmic-art supplies **generative composition**: an algorithmic position, then a
self-contained interactive viewer. Files: `.md` (philosophy), `.html` + inline `.js`
(viewer).

## Step A — Write the algorithmic philosophy first

A computational aesthetic position, 4–6 paragraphs, output as `.md`. Name the movement
in 1–2 words ("Organic Turbulence", "Quantum Harmonics", "Emergent Stillness"), then
describe how it manifests through: computational processes and mathematical
relationships · noise functions and randomness patterns · particle behaviour and field
dynamics · temporal evolution and system states · parametric variation and emergent
complexity. Each aspect once. Beauty lives in the process, not the final frame.

Condensed starting positions: *Organic Turbulence* (layered-noise flow fields,
accumulating trails) · *Quantum Harmonics* (phase interference on a grid) · *Recursive
Whispers* (self-similar subdivision) · *Field Dynamics* (invisible forces shown only
by their traces) · *Stochastic Crystallization* (relaxation from random seeds).

Deduce the quiet conceptual thread from the request, as in
[canvas-design.md](canvas-design.md) — expressed through parameters and emergence
instead of form and colour.

## Step B — Start from the template

Read `../templates/viewer.html` **before writing any HTML** and use it as the literal
starting point, not inspiration. Its extensive comments mark what is fixed and what is
variable.

| Fixed (copy exactly) | Variable (build fresh each time) |
|---|---|
| Layout: header, sidebar, canvas area | The entire p5.js algorithm (`setup`, `draw`, classes) |
| Branding: UI colours, fonts, gradients | The `params` object and its members |
| Seed section: display, Prev/Next/Random, jump-to input | Parameters section: controls, names, min/max/step |
| Actions: Regenerate, Reset, Download PNG | Whether a Colours section exists at all |

Never invent custom chrome, dark themes, or system fonts, and never rebuild the
sidebar structure. `../templates/generator_template.js` is a reference for code
structure and seeded-randomness practice — not a menu of patterns to pick from.

## Step C — Implement with seeds and parameters

```javascript
let seed = 12345;            // or a hash of user input
randomSeed(seed);
noiseSeed(seed);
```

The same seed must always produce identical output. Define `params` from what the
*system* needs tunable — quantities, scales, probabilities, ratios, angles, thresholds
— not from imagined "pattern types". Let the philosophy dictate the algorithm: organic
emergence suggests accumulation and feedback loops; mathematical beauty suggests
geometric ratios and harmonics; controlled chaos suggests randomness inside strict
boundaries.

Craft floor: complexity without visual noise, palettes chosen rather than random RGB,
composition that keeps a hierarchy even under randomness, smooth real-time execution
where animated.

## Step D — Deliver one self-contained artifact

A single `.html` file: p5.js from CDN, all CSS and JS inline, no other imports, no
server. It must open directly in a browser and in a hosted artifact viewer.

- Parameter sliders update in real time; Reset restores defaults.
- Seed controls work: display, prev, next, random, jump.
- Regenerate and Download PNG work.
- Colour pickers only where the piece benefits from them; fixed palettes need no
  section at all.

For variation requests, use seed presets or a thumbnail gallery inside the same file —
the algorithm stays constant, each seed reveals a different facet.

## Quality additions

- Check for text/controls clipping at mobile widths before delivery.
- If the viewer must be verified in a real browser rather than trusted, use the
  Playwright flow in
  [browser-verification.md](../../web-artifact-and-app-building/references/browser-verification.md).
