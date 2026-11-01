Layout turns product priority into reading order, grouping, rhythm, and usable space. Diagnose the structural problem before moving boxes.

---

## Visitor mode

- **Persuade + Experience:** composition may be asymmetric, fluid, or intentionally disruptive when the selected world earns it.
- **Operate + Read:** predictable structure, stable density, and navigable linearity are affordances.
- **Native:** follow [ios.md](ios.md) or [android.md](android.md) for navigation, insets, adaptation, and touch targets.

Preserve the established visual world. A layout command changes structure inside it; identity replacement belongs to [new-work.md](new-work.md).

## Two isolated assessments

When a sub-agent tool is available and permitted, run these independently; otherwise run them yourself in this order.

1. **Layout assessment:** inspect representative states and viewports. Answer every question below with rendered or source evidence:
   - **Reading order:** Apply the squint test. With detail blurred, can you still identify the primary element, the secondary element, and the major groups in order?
   - **Grouping:** Are related items close and distinct groups separated, or are containers compensating for weak proximity?
   - **Rhythm:** Do tight and generous intervals create a deliberate cadence, or is one spacing value repeated until everything has equal weight?
   - **Structure:** Does the topology match the content and task? Are repeated cards, columns, or sections genuinely equivalent, or merely a framework default?
   - **Density:** Does the amount of information per region fit use frequency, decision complexity, and visitor mode?
   - **Adaptation:** At narrow, intermediate, wide, zoomed, and localized states, what reorders, collapses, wraps, scrolls, or remains fixed? Does DOM and focus order still agree with the visual order?
   - **Extremes:** Do long content, empty states, overlays, sticky elements, safe areas, and small touch targets expose structural failures?
2. **Mechanical scan:** run:

```bash
.claude/skills/impeccable/scripts/impeccable detect --json --scope layout [target files or dirs]
```

Also inspect arbitrary spacing, overflow, stacking, and container behavior the detector cannot resolve. Keep mechanical evidence out of the first assessment, then synthesize both passes before editing. A clean scan cannot prove hierarchy or rhythm.

### Frame measurements

The layout scope reads markup and returns nothing for the frame of the page. These are read off the render at 1440, 768, and 390 wide, answered with the number each produced. They are the failures a reader names first — "no clear title", "everything is shifted to one side", "big random blank spaces" — and they survive a clean scan.

- **Margins.** Measure from the content box to each viewport edge. The two match to a few pixels at every width; 16–32px is the working range and nothing goes under 16px, the phone included. A 20–30px drift reads as shifted. The navigation sits on the page's pair, not on its own inset, and a bleed starts from the margin rather than moving it.
- **Half-empty sections.** Count the sections whose text takes one side and leaves the other to plain ground. Text in one half is ordinary; the other half then holds the section's own picture, a second column, a list, or the large number. The middle counts too: a card at the left edge and an action at the right with the middle third empty is the same hole.
- **Blank stretches.** Walk the page top to bottom and measure every run taller than half a screen holding no text, picture, or control. More than one fails; one is a rest and only if something closes it — a picture across it, a step in ground tone, a field of colour. A hairline is not a closer. Section gaps run 120–240px on desktop and 72–112px on a phone, always larger than any gap inside a section.
- **The title.** One `h1` on the first screen, at display size (32px or more on desktop), two lines at most, saying what this is: the name with what it does, the product with what it is for. A bare name needs a line under it, 18px or more, carrying the plain words. Read it on the first paint, not after an entrance fires.
- **Section titles.** Every section that carries text opens with a heading, one or two lines, in the heading face at section size, starting on the same margin or anchor line as the rest. A section of thirty words or more with no heading is a hole in the structure.
- **Edge text.** Only deliberately bled display type sits within 16px of the screen edge, or 12px on a phone, where the margin is 16–20px. A display line that starts inside the margin and runs a few pixels off the opposite edge is a fit error, not a bleed: fit it by measurement.
- **What moves.** Count the elements that actually move, on load and on scroll, and name each. One authored moment carries the page; a scattered count with no lead is the page moving because it can.
- **Faces.** Read `document.fonts` for what loaded, not what the stylesheet declares. A declared face that never loads falls back silently, and the fallback is what the reader sees.

Two are readable from source alone — the heading per section and the `h1` count. The rest need a render.

## Set the spatial thesis

Before editing, name:

- the primary reading or task path;
- what belongs together and what must separate;
- which element leads and which supports;
- the intended density and spacing rhythm;
- how the structure changes across containers, viewports, input modes, and content extremes.

Choose the simplest structural model that expresses those relationships. Use layout primitives according to the relationships they control, and name reusable spacing and container roles semantically.

## Apply

- Group by meaning. Use proximity before adding containers or decoration.
- Create rhythm through deliberate contrast between tight and generous intervals.
- Use a documented spacing scale rather than one-off values. A 4-unit base usually provides the useful middle steps that an 8-only scale misses.
- Let hierarchy follow product priority, not framework defaults.
- Keep distinct content visually distinct without turning every group into an isolated component.
- Make responsive behavior structural: reorder, collapse, reflow, or reveal based on what remains important.
- Prefer container-aware components when the same component appears in different contexts.
- Use `gap` for sibling rhythm when it expresses the relationship more directly than child margins.
- Keep touch targets usable even when their visible marks are small.
- Use depth only when it clarifies state or hierarchy.
- Make optical corrections only after inspecting the rendered result.

Variation is not a goal by itself. Repetition should support recognition; break it only when content or priority changes.

## Verify

- The squint test still reveals the primary, secondary, and major groups in order.
- The reading and task path remains clear at every supported size.
- Related content groups naturally; unrelated content does not blur together.
- Tight and generous spacing create intentional rhythm instead of monotonous repetition.
- Density matches use frequency and content complexity.
- Long text, empty states, localization, zoom, and dynamic content do not break the structure.
- The frame measurements hold at 1440, 768, and 390: equal margins, no half-empty section, no blank stretch past half a screen, a titled first screen, a heading on every section that carries text, text inside the margin.
- Keyboard, touch, and assistive-technology order agree with the visual order.
- The final mechanical scan has no unexplained findings.

Answer each item with rendered or source evidence, then rerun the scan. Do not substitute a bare “yes” for verification.

When the structure holds, hand off to `/impeccable polish`.

## Live-mode signature params

Every variant declares a coarse `density` parameter and authors spacing against `var(--p-density, 1)`.

```json
{"id":"density","kind":"range","min":0.6,"max":1.4,"step":0.05,"default":1,"label":"Density"}
```

Add one structural parameter only when the topology genuinely branches. Follow [live.md](live.md)'s parameter contract.
