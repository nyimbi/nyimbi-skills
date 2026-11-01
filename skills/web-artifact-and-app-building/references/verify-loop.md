# The verify loop — one artifact, three independent checks

You cannot watch what you wrote; you look at frames and read outputs. The triad below is ordered by
cost: machine gates first (cheap, fast fail), rendered frames second, deployed smoke last. Stop when a
full pass finds nothing — then stop.

## 0. Machine gates (before any visual pass)

- `ai-design-check` over the **source**, never the built bundle (class-string rules trip on JS
  comments and `[x]` array literals inside bundles; scope the gate to files you generate). Exit 0,
  or every finding above the committed baseline resolved.
- Per-type verifiers when the artifact embeds diagrammed/figure content: `diagram-design`'s
  `verify-geometry.py` / `verify-<type>.py` / `verify-contrast.py` on any SVG figure the page ships.
- A syntax/type pass on the tree (`tsc --noEmit`, `astro build`'s math gate) — but remember: both
  exit 0 on a file that renders nowhere. The gates bound the render, the next two steps prove it.
- The known-fail canary discipline: a gate must have been observed failing before its pass means
  anything. If a checker has never fired on this project, plant one violation and watch it report.

## 1. Rendered frames (read as images, never as code)

- Multi-view sheets: 7 angle/beat captures minimum for figures; every tile read at 2–3× crop, plus
  phone-width and dark-mode captures where the page claims either.
- Interaction run-throughs from URL params (`?press=`, `?xr=1`) at two time budgets, plus one
  out-of-order interaction proving the sensible-fallback path.
- One still of the exact embed geometry the host page uses (§6 of deploy-contract.md).
- The "second instance" trap: a state bug that lives in the second mount of a duplicated component
  is invisible to a test that renders one - render, change the identity prop, assert.

## 2. The deployed smoke (the only check the visitor meets)

- Every referenced asset: HTTP 200 + expected content-type + non-zero size, from the deployed host.
- Headless screenshot of the deployed page at desktop and phone widths, fresh profile (cold cache).
- Video: `readyState 4` + `poster` resolves.
- Error DOM check (`data-errors` empty) and zero console/pageerror at default + one interaction.
- Then, and only then, hand over the link.

## Standing rules

- One pass of edits per look: fix everything one look shows before looking again.
- Never report from a single view, a single width, or a single frame.
- Report what each pass found and what you fixed; end with the honest residue — what is still
  imperfect, plainly stated. A summary that hides a known blemish reads as its own kind of failure.