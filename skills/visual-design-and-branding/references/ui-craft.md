# UI Craft — Direction, Type, Motion, Copy

Technique file for the interactive-UI branch of the [SKILL.md](../SKILL.md) workflow.
frontend-design supplies **UI craft**: a distinctive, brief-specific point of view for
a screen — the opposite of a default theme. Theme-factory gives you a system; this file
tells you when the system is not enough.

## Ground the design in the subject

If the brief does not say what the product is, determine it and confirm: one concrete
subject, its audience, and the design's primary job. The subject's industry, materials,
and vernacular are where distinctive choices come from — a toy for 8–11 year-olds and a
financial-analyst dashboard share nothing. Build with the brief's real content
throughout.

## Two-pass process

**Pass 1 — plan.** Write a compact token system:

- **Colour** — 4–6 named hex values forming the base palette
- **Type** — the typefaces and their roles (display, body, data)
- **Layout** — one-sentence concept plus ASCII wireframes, with alignment decided
  (left / centre / justified)
- **Principles** — what makes *this* page unique

**Pass 2 — review the plan against the brief.** For each element, ask whether you would
arrive at the same choice for any similar page. If yes, it is a default, not a choice:
revise it and say what changed and why. Only then write code.

## Type

Typography carries the personality. One family, or two that are clearly distinct —
never a matching display/body pair by reflex. Set an explicit scale with intentional
weights, widths, and spacing (per *The Elements of Typographic Style*); when type is
the headline, treat the type treatment as an active design element. Body lines under
~80 characters; serif body gets slightly more line-height than sans.

Three commonest tells of a generated page — avoid unless the brief demands them:

1. Accenting a single word in a headline (italic, bold, or recoloured)
2. All-caps for labels
3. Unnecessary typographic labels above content

## Structure, motion, restraint

- The **hero opens with the most characteristic thing in the subject's world** — a
  headline, image, animation, live demo. "Big number + small label + supporting stats +
  gradient accent" is the default; use it only if it is genuinely best.
- Structural devices (outlines, numbering, eyebrows, dividers) must encode information.
  Numbered markers only when the content really is a sequence.
- **One orchestrated motion moment** beats scattered effects. Fade-and-slide-up on
  every section and hover transitions on every card are the generic default. Motion
  that answers a user action is welcome.
- Spend boldness in one place. One memorable element; everything else quiet and
  disciplined. Remove one accessory before leaving the house.

## The default-clusters to steer away from

1. Warm cream (~`#F4F1EA`) + high-contrast serif + terracotta accent (~`#D97757`)
2. Near-black ground with one acid-green or vermilion accent
3. Broadsheet layout: hairline rules, zero radius, dense newspaper columns
4. The SaaS-card kit: identical rounded cards, one radius everywhere, the same soft
   grey shadow, gradient washes as decoration
5. Template chrome: tracked-out ALL-CAPS eyebrows, `A · B · C` middle-dot meta strings,
   `WORD — fragment` em-dash labels, tinted near-black standing in for black, monospace
   for small labels, `→` appended to links

All five are legitimate for some brief. Where the brief pins a direction, follow it
exactly — the brief's own words win. Where it leaves an axis free, do not spend that
freedom on one of these.

## Writing in the interface

Words exist to make the product easier to understand and use — design content, not
decoration. Name things by what the user understands, not how the system is built ("manage
notifications", not "webhook config"). Active voice; a CTA states exactly what happens
("Save changes", not "Submit"); an action keeps one name through the flow, so "Publish"
produces "Published". Errors explain what went wrong and how to fix it in the
interface's voice — never vague, never apologetic. Empty states are invitations to act.
Plain verbs, sentence case, no filler, tone matched to brand and audience.

## Quality floor (build it, don't announce it)

Responsive down to mobile · visible keyboard focus · `prefers-reduced-motion`
respected · accessible contrast · no CSS selector specificity that cancels itself out
(especially padding/margin between type- and element-based selectors). Screenshot and
critique as you go; keep a running note of what you tried.


## The signature element

Spend your boldness in one place. The **signature** is the single unique element the
page will be remembered for — it embodies the brief in one appropriate gesture, and
everything around it stays quiet and disciplined. Cut any decoration that does not
serve the brief. Not taking a risk can itself be a risk. Before finishing, apply the
Chanel test: remove one more element and ship.

## Principles the condensed rules compress

- **The hero is a thesis.** Open with the most characteristic thing in the subject's
  world — a headline, an image, an animation, a live demo, an interactive moment. A big
  number with a small label, supporting stats, and a gradient accent is the template
  answer; use it only when it is truly the best option.
- **Structure is information.** Numbering, eyebrows, dividers, and labels should encode
  something true about the content, not decorate it. Sequential markers (01/02/03) are
  only right when the content genuinely is a sequence where order carries information.
  Question such choices before using them.
- **Motion, orchestrated.** One well-orchestrated moment (a load sequence, a
  scroll-triggered reveal, a hover micro-interaction) lands harder than scattered
  effects; extra animation reads as AI-generated. Match the amount of motion to the
  direction.
- **Complexity must match the vision.** Maximalist directions need elaborate execution;
  minimal directions need precision in spacing, type, and detail. Elegance is executing
  the chosen vision well.
- **The studio frame.** Work as the design lead of a small studio whose identity is
  that no client could be mistaken for another: deliberate, opinionated,
  subject-specific choices — palette, type, layout — and one real, justifiable
  aesthetic risk per project.
