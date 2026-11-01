---
name: ux-excellence
description: Rigorously audit and remediate the UI/UX of a platform to achieve expert-level design quality. Focus on systemic design coherence, exhaustive state-space coverage via type-system enforcement, physics-based motion with semantic intent, deterministic usability heuristics, human-centered research validation, content design, emotional design, and cross-platform input modality coverage. Use when the user asks to improve UX/UI, polish the platform, or ensure a world-class user experience. For accessibility-only (WCAG/a11y) checks, use the accessibility-review skill.
---

# UX Excellence — Systemic UI/UX Audit & Remediation

> **Routing:** For a one-off structured critique of a single mockup or screen, use **design-critique**; for auditing, documenting, or extending the design system (tokens, components), use **design-system**; for WCAG-only checks, use **accessibility-review**.

This skill transforms a functional UI into an expertly crafted experience. It does **not** rely on subjective "delight" scores. Instead, it audits **systemic design coherence** (spatial grids, typographic scales, semantic tokens, perceptual color science), **exhaustive state choreography** enforced via the type system, **physics‑based motion** mapped to semantic intent, **deterministic cognitive load** metrics, **performance‑conscious animation** (avoiding layout-thrashing properties), **human‑centered research validation** (telemetry, heuristics, cognitive walkthroughs), **content design & microcopy quality**, **emotional design & delight architecture**, and **cross‑platform input modality coverage**. Affective qualities are systematized with clear rules; human validation is required only for brand‑specific personality calibration.

## Modes

- **Audit** (default): read‑only. Detect structural debt, state‑space gaps, research gaps, content issues, and emotional design opportunities; write the report. Do not modify code.
- **Remediate**: implement fixes and improvements in priority order, after producing a **Tiered Rationale** (full rationale for P0/P1, micro‑rationale for P2/P3).

**Mode decision rule:** "audit", "review", "check" UX/UI → **Audit**. "fix", "improve", "polish", "enhance" → **Remediate**. Ambiguous → ask.

## Workflow

1. **Determine scope** — whole platform, a specific user journey, a component library, or a single screen. If unsure, ask.
2. **Gather research inputs** (Audit mode) — request or check for:
   - Heatmap data (Hotjar/Microsoft Clarity/Mouseflow)
   - Session recordings
   - Analytics funnel data and task completion rates
   - System Usability Scale (SUS) scores or CSAT/NPS data
   - If unavailable, mark as `deferred(research-required)` and proceed with code‑level audit.
3. **Detect** — perform a multi‑layer inspection using appropriate tools:
   - **Framework detection** (see below) to adapt AST/Regex rules.
   - **Human‑Centered Research Level** — cross‑reference telemetry with code findings (e.g., "Fitts's Law violation at checkout button correlates with 34% drop‑off at step 3").
   - **Heuristic Evaluation** — Nielsen's 10 heuristics + cognitive walkthrough protocol.
   - **Token & Syntax Level** (AST/Regex) — spatial grid violations, raw hex values, non‑modular typographic scale, missing semantic motion tokens, W3C token compliance.
   - **Type‑System Level** (AST/TypeScript) — missing state unions, unhandled promise branches, state transition validation.
   - **Content Design Level** — microcopy audit, error message quality, reading ease, jargon detection.
   - **Render‑Dependent Heuristics** (requires headless browser tooling: Playwright, Lighthouse, axe) — Fitts's Law, DOM node count, CLS, contrast ratios (WCAG 2.2 + APCA).
   - **Motion Performance** — detect layout‑thrashing animated properties.
   - **Emotional Design & Delight** — moment‑of‑truth mapping, personality consistency, signature interaction moments.
   - **Cross‑Platform & Input Modality** — touch target sizes, keyboard navigation, voice control, RTL, safe‑area insets.
4. **Score & prioritize** — use deterministic, empirically anchored proxies.
5. **Write the report** — update `docs/audit/ux-excellence.md` (see output contract). Generate three views: Executive Summary, Design Team Report, Engineering Ticket Specs.
6. **Remediate (if requested)** — for each change, produce a rationale scaled to severity. Then implement. Run relevant checks.
7. **Design QA Gate** — before closing, run the pre‑ship checklist.
8. **Close out** — mark resolved items `fixed`, note deferred items with a tracking reference, add a change‑log entry, summarise.

---

## Output contract — `docs/audit/ux-excellence.md`

Use a single persistent master file. Each run appends a `## Audit Run YYYY-MM-DD` section. For **small‑scope runs** (single component or isolated flow), the agent may output an **inline, condensed format** at the top of the run section. For platform‑wide audits, the full structure is required.

**Multi‑Audience Report Structure:** Generate three views from the same audit data.

### 1. Executive Summary (1 page)
- Business impact estimate (conversion lift, support ticket reduction)
- Risk severity matrix (P0 = revenue/legal risk)
- Top 3 recommendations with ROI
- Effort vs. Impact quadrant chart

### 2. Design Team Report (full structure below)

### 3. Engineering Ticket Specs (actionable)
- Per‑finding: file path, line number, exact code change, acceptance criteria
- Ready for Jira/Linear/GitHub Issues import

---

**Required sections (full audits — Design Team Report):**

### `## Framework Detection`
Note the design system used (Tailwind, CSS Modules, CSS‑in‑JS, etc.) and any relevant config files inspected. This informs subsequent token checks.

### `## Human‑Centered Research & Validation`
- **Telemetry Cross‑Reference:** Map heatmap/session data to code‑level findings. Example: "Rage clicks on save button (Clarity heatmap) correlate with missing loading state (code)."
- **Heuristic Evaluation (Nielsen's 10):** Score each heuristic 0–4 (0=no issue, 4=catastrophic). List violations.
- **Cognitive Walkthrough:** For each primary flow, answer the four questions:
  1. Will the user try to achieve the right effect?
  2. Will the user notice the correct action is available?
  3. Will the user associate the correct action with the effect?
  4. If the correct action is taken, will the user see progress?
- **Task Completion & SUS:** If data available, report scores and trends.

### `## Systemic Coherence Report`
- **Spatial Grid Compliance:** List margins/paddings not multiples of base unit (from config). Flag arbitrary values.
- **Typographic Scale:** Check modular scale compliance; flag arbitrary values. Verify line length (45–75 chars), line height (1.5–1.7 body), paragraph spacing (≥1em), letter‑spacing rules.
- **Design Token Topology (W3C Standard):**
  - Flag raw hex/rgb values outside token references.
  - Verify `$value` and `$type` syntax compliance.
  - Check token naming: `category/concept/variant/state`.
  - List missing tokens (elevation, z‑index, border, cursor).
- **Thematic Polymorphism:** Check dark‑mode variants use semantic tokens; flag hardcoded colors lacking dark‑mode mapping.
- **Fluid Topology:** Check for static `px` font sizes vs. `clamp()` or `rem`‑based responsive scales.
- **Color Science:**
  - Prefer OKLCH/LAB for token definitions.
  - Check hue consistency across lightness levels.
  - Dark mode: avoid pure black (`#000`), reduce saturation 10–20%, elevated surfaces lighter.
  - Check for halation in dark mode (APCA negative Lc limits).

### `## State‑Space Coverage (Code‑Level Mandate)`
Do not maintain a manual matrix. Verify programmatically:
- Ensure core data‑fetching components use a strict state union:
  ```ts
  type QueryState<T> = 
    | { status: 'idle' }
    | { status: 'loading' }
    | { status: 'error'; error: Error; retry: () => void }
    | { status: 'success'; data: T }
    | { status: 'empty'; guidance: string }
    | { status: 'refreshing'; data: T }
    | { status: 'offline'; queuedActions: Action[] }
    | { status: 'rateLimited'; retryAfter: number }
  ```
- **The State Quintet + Sub‑States:** Every data‑dependent component must handle:
  1. **Idle** — initial state, ready for input
  2. **Loading** — skeleton or spinner shown
  3. **Success** — data rendered, interactive
  4. **Empty** — no data, but not an error (guide user to create/add)
  5. **Error** — failure with recovery path (retry, fallback, contact support)
  6. **Partial Success** — stale‑while‑revalidate
  7. **Refreshing** — background re‑fetch
  8. **Rate‑Limited** — specific error with countdown
  9. **Offline** — queued actions, sync pending
- **State Transition Validation:** Verify no impossible transitions (e.g., `error → success` without `loading`). Every state must have an exit path. No dead‑end states.
- **Exhaustive Rendering:** The component's render function contains conditional branches for all states in the union.
- List components that lack the strict state union or have unhandled state branches.

### `## Content Design & Microcopy Audit`
- **Voice & Tone Consistency:**
  - Error messages: actionable? ("Enter a valid email" vs "Invalid input")
  - Empty states: guide forward?
  - Button labels: verb‑noun structure? ("Save Changes" not "Submit")
  - Success messages: confirm *what* happened?
- **Cognitive Load in Copy:**
  - Flesch Reading Ease target: >60 general, >80 universal
  - Sentence length: average <20 words
  - Jargon detection: flag without explanation
  - Progressive disclosure: complex info behind "Learn more" / tooltips
- **Error Message Quality Framework:** Every error must answer:
  1. What happened?
  2. Why?
  3. How to fix?
  4. Prevention?

### `## Motion & Choreography Ledger`
- **Semantic motion token usage:** Ensure transitions reference design tokens (`var(--motion-enter)`, `var(--motion-spring-fluid)`) rather than raw values.
- **Stagger delays:** Systematically applied (e.g., `calc(var(--index) * 50ms)`).
- **Layout animations (FLIP):** For elements changing position/size.
- **Performance‑conscious animation:** Flag any animated property triggering layout thrashing (`width`, `height`, `top`, `left`, `right`, `bottom`, `margin`, `padding`, `border`, `font-size`). Recommend `transform` and `opacity`.
- **Micro‑Interaction & Feedback Choreography:**
  - **Feedback Timing (Doherty Threshold):**
    - <100ms: instant feedback (button press, ripple)
    - 100ms–1s: subtle progress if destructive
    - 1s–3s: explicit loading indicator
    - 3s–10s: progress bar with %
    - >10s: detailed estimate + background execution + notify on completion
  - **Signature Interaction Moments:** Identify one signature micro‑interaction per core flow.
  - **Multi‑Modal Feedback Matrix:**
    | Interaction | Visual | Motion | Haptic | Sound |
    |---|---|---|---|---|
    | Success | Green check + toast | Spring bounce | Light tap | Subtle chime |
    | Error | Red inline + shake | Wobble | Double tap | Low tone |
    | Loading | Skeleton/progress | Pulse/glow | None | None |
    | Destructive | Warning modal | Scale‑down | Heavy tap | Alert tone |

### `## Emotional Design & Delight Architecture`
- **Moment‑of‑Truth Mapping:**
  - **Peak moments:** Celebrate success (onboarding complete, first purchase, streak)
  - **Pit moments:** Soften failure (empathy in errors, recovery paths)
  - **End moments:** Finish strong (confirmation screens, "what's next")
- **Personality Consistency:** Define dimensions (Friendly↔Serious, Playful↔Professional). Audit copy, motion, color, illustration against these. Flag inconsistencies.
- **Surprise & Delight Rules:**
  - Add unexpected but helpful details (e.g., witty loading messages, mascot reactions)
  - Never at cost of performance or accessibility
  - Must reinforce brand, not distract

### `## Journey Coherence & Task‑Flow Audit`
- **Interaction Depth Budget:** Core task ≤3 clicks/taps. Form fields ≤7 per screen. Navigation depth ≤3 levels.
- **State Continuity Across Screens:**
  - Data persists on back/forward navigation
  - Scroll position restored on back‑navigation
  - Filters/sorts persist across sessions
  - Flag "pogo‑sticking" (repeated jumps between two pages = information scent failure)
- **Entry Point Coverage:** Audit all entry points (direct URL, search, notifications, shared links). Each must land in a coherent state.

### `## Cognitive Load & Ergonomics` (Render‑Dependent)
- **Fitts's Law:** Interactive targets <44×44px (mobile) or <24×24px (desktop).
- **Hick's Law:** Decision points with >7 ungrouped options.
- **DOM Node Count:** >1000 nodes per page (Lighthouse).
- **Gestalt Proximity:** Related elements lacking spatial proximity or bounding containers.

### `## Accessibility Scorecard` (WCAG 2.2 + APCA)
- **WCAG 2.2 AA:**
  - Contrast: 4.5:1 normal text, 3:1 large text
  - Focus indicators: ≥2px thick, 3:1 contrast against adjacent colors
  - Focus Not Obscured (2.4.12)
  - Dragging Movements (2.5.7) — single‑pointer alternatives
  - Target Size (2.5.5): 44×44px minimum touch targets
  - Consistent Help (3.2.6)
- **APCA (WCAG 3.0 draft):**
  - Body text: Lc ~75
  - Small/thin text: Lc ~90
  - Large bold text: Lc ~60
  - Dark mode: check negative Lc values for halation/eye strain
- **Screen Reader & Assistive Tech:**
  - Heading hierarchy (no skipped levels)
  - Landmark regions (`<main>`, `<nav>`, `<aside>`)
  - Live regions for dynamic updates
  - Meaningful alt text
  - ARIA label consistency (icon‑only buttons must have accessible names)
  - Full keyboard navigation end‑to‑end

### `## Perceived Performance & Latency Budget`
- **RAIL Model:**
  - Response: <100ms for input feedback
  - Animation: <16ms per frame (60fps)
  - Idle: Max 50ms chunks for background work
  - Load: <1s above‑fold, <3s full page
- **Skeleton Screen Standards:**
  - Match final layout geometry (prevent CLS)
  - Use shimmer/pulse motion
  - Never "pop in" without skeleton
- **Optimistic UI Patterns:**
  - Optimistic updates (show success before API confirms)
  - Rollback UI on optimistic failure
  - Request deduplication (prevent double‑submit)

### `## Cross‑Platform & Input Modality Audit`
- **Touch:** 44×44px targets, gesture support, hover‑less design
- **Mouse:** Right‑click menus, hover states, 24×24px min targets
- **Keyboard:** Full tab navigation, shortcut keys, focus traps in modals
- **Voice:** Semantic HTML enables voice control; `aria-label` on icon buttons
- **Stylus/Pen:** Ink support where relevant
- **Responsive Architecture:**
  - Container queries (not just media queries)
  - `clamp()` fluid typography
  - Logical properties (`margin-inline-start`) for RTL
  - Safe‑area insets (notches, dynamic islands)
  - `color-scheme: light dark`, `prefers-contrast: more/less`, `prefers-reduced-motion`

### `## Competitive Benchmark & Best‑in‑Class Reference`
For each core flow, compare against 2–3 best‑in‑class competitors:
- Document patterns to emulate and anti‑patterns to avoid
- Benchmark onboarding (Notion, Figma, Duolingo), checkout (Apple, Amazon, Stripe), settings (Linear, Vercel, GitHub)

### `## Success Metrics & Validation Protocol`
- **Pre/Post Audit Metrics:**
  | Metric | Tool | Target |
  |---|---|---|
  | Task Completion Rate | Usability test / analytics | >85% |
  | Time on Task | Session recording | Reduce by 20% |
  | Error Rate | Analytics / heuristic eval | <5% |
  | SUS Score | Post‑test survey | >68 |
  | NPS / CSAT | In‑app survey | Track trend |
  | Conversion Rate | Analytics | Baseline + lift |
- **A/B Testing Protocol:** For P0/P1 enhancements, define hypothesis, primary metric, secondary metrics, guardrail metrics.

### `## Remediation Plan`
Findings in priority order, split fix‑now vs defer.

### `## Design QA Gate (Pre‑Ship Checklist)`
Mandatory checklist before any enhancement ships:

| # | Check | Method |
|---|---|---|
| 1 | All states render correctly (loading, error, empty, success, offline) | Visual inspection |
| 2 | No layout thrashing in animations | DevTools Performance panel |
| 3 | Color contrast passes WCAG 2.2 AA + APCA | axe / Polypane |
| 4 | Keyboard navigation works end‑to‑end | Manual tab‑through |
| 5 | Screen reader announces dynamic changes | NVDA/VoiceOver test |
| 6 | Touch targets ≥44px on mobile | DevTools device mode |
| 7 | Reduced motion respected | `prefers-reduced-motion` test |
| 8 | No visual regression in Storybook/Chromatic | Visual diff |
| 9 | Copy reviewed for tone, clarity, actionability | Content design review |
| 10 | Analytics events fire correctly | Network tab / debugger |
| 11 | State transitions validated (no impossible paths) | Code review / XState viz |
| 12 | Entry points land in coherent states | Manual navigation test |

### `## Change Log`
One line per run: date, mode, summary, items fixed/deferred.

---

## Finding fields

| Field | Meaning |
|-------|---------|
| `severity` | `P0` (blocker/correctness/legal) · `P1` (significant friction) · `P2` (polish) · `P3` (minor) |
| `type` | `Structural` (automatable) · `Affective` (systematized, human‑calibrate) · `Research` (requires telemetry) · `Content` (copy/microcopy) |
| `category` | e.g., "Spatial Grid", "State Quintet", "Motion", "APCA Contrast", "Content Design", "Emotional Design" |
| `location` | `file:line`, component name, or route |
| `finding` | concrete description |
| `recommendation` | specific fix |
| `effort` | `S` (<2h) · `M` (3–8h) · `L` (>8h) |
| `status` | `open` · `fixed(<date>)` · `deferred(<ref>)` |
| `confidence` | `High` (static AST/type‑check) · `Medium` (tool output) · `Low` (heuristic, requires verification) |
| `evidence` | static code reference, tool output, heuristic note, or telemetry correlation |

---

## Framework‑aware detection

Before running token/syntax inspections, detect the project's design framework:

- **Read `package.json`** and `tailwind.config.js` (if present), `theme.ts`, or equivalent configuration.
- **Tailwind:** Check the `spacing` and `fontSize` scales; use them to validate values. Flag values not in config (unless arbitrary values).
- **CSS‑in‑JS / CSS Modules:** Inspect theme provider files for design tokens; verify `var(--...)` references instead of raw hex values.
- **CSS Custom Properties:** Verify `var(--...)` tokens exist and are used correctly.
- **W3C Design Tokens:** If using a design token system, verify `$value` and `$type` syntax, token aliases, and cross‑platform export capability.

If no design system configuration is found, default to:
- Generic 4px/8px base unit
- Predefined modular scale (1.25 ratio)
- OKLCH color space recommendations
- `clamp()` fluid typography

---

## Detection catalog — by level of automation

### Human‑Centered Research Level (Requires telemetry / manual)
1. **Rage Click Correlation** — map heatmap rage clicks to missing feedback states.
2. **Drop‑Off Correlation** — map funnel drop‑offs to interaction depth or state gaps.
3. **Heuristic Severity** — score each Nielsen heuristic 0–4.
4. **Cognitive Walkthrough Failure** — any "no" answer to the four walkthrough questions.

### Token & Syntax Level (Automatable, framework‑aware)
0. **Machine floor gate** — `ai-design-check` (vendored bundle skill) proves 49 of the 74 upstream rules
   mechanically, class-string scoped to real attributes (JSX comments and built bundles are known
   false-positive surfaces; scope to source). Grade every finding this skill produces on the same two
   axes as that gate: severity (error/warning/note) × enforcement (checked/review) — a finding with a
   concrete threshold belongs at the checked end when its jurisdiction is code we generate.
1. **Spatial Grid Violation** — margins/paddings not matching project spacing scale.
2. **Non‑modular Typographic Scale** — font sizes not following defined scale.
3. **Raw Hex/RGB Values** — color literals not semantic tokens.
4. **Missing Design Tokens** — common tokens not defined (elevation, z‑index, border, cursor).
5. **Thematic Polymorphism Failure** — hardcoded colors lacking dark‑mode semantic mapping.
6. **Fluid Topology Violation** — static `px` font sizes instead of `clamp()` or `rem`.
7. **Color Science Violation** — using RGB/HSV instead of OKLCH/LAB; pure black in dark mode; hue shift across lightness.
8. **W3C Token Non‑Compliance** — missing `$value`/`$type` or inconsistent naming.

### Type‑System Level (Automatable via AST/TypeScript)
1. **Missing State Enums** — components lacking strict state union.
2. **Unhandled Async Branches** — async operations without explicit error/loading rendering.
3. **Exhaustive Rendering** — render functions not covering all union states.
4. **Impossible State Transitions** — transitions that violate the state machine.
5. **Dead‑End States** — states with no exit path.

### Content Design Level (Automatable + Manual)
1. **Error Message Incompleteness** — missing What/Why/Fix/Prevention.
2. **Reading Ease Violation** — Flesch score below threshold.
3. **Jargon Without Explanation** — industry terms unexplained.
4. **Button Label Ambiguity** — non‑verb‑noun structure.
5. **Empty State Dead‑End** — no forward guidance.

### Render‑Dependent Heuristics (Requires Tooling)
1. **Fitts's Law Violation** — interactive targets <44×44px (mobile) or <24×24px (desktop).
2. **DOM Node Count** — >1000 nodes per page (Lighthouse).
3. **Gestalt Proximity Violation** — related elements lacking spatial proximity.
4. **High CLS** — Cumulative Layout Shift >0.1 (Lighthouse).
5. **Insufficient Contrast (WCAG 2.2)** — below AA thresholds.
6. **Insufficient Contrast (APCA)** — Lc below thresholds for text size/weight.
7. **Focus Obscured** — focused elements hidden by sticky headers/footers.

### Motion Performance (Automatable via AST/Regex)
1. **Layout‑Thrashing Animations** — CSS/JS animations modifying `width`, `height`, `top`, `left`, `right`, `bottom`, `margin`, `padding`, `border`, `font-size`.
2. **Missing Reduced Motion Support** — animations not wrapped in `prefers-reduced-motion` checks.

### Emotional Design Level (Systematized + Human Calibrate)
1. **Missing Peak Moment Celebration** — success states are generic (just "Success!").
2. **Pit Moment Harshness** — error states lack empathy or recovery guidance.
3. **Personality Inconsistency** — playful visuals with clinical copy, or vice versa.
4. **Missing Signature Interaction** — no defining micro‑interaction for core flows.

### Cross‑Platform & Input Modality (Automatable + Manual)
1. **Touch Target Undersize** — <44×44px on touch devices.
2. **Keyboard Trap** — focus cannot escape modal/component.
3. **Missing Logical Properties** — hardcoded `margin-left` instead of `margin-inline-start`.
4. **Missing Safe‑Area Inset** — content obscured by notches/dynamic islands.
5. **Missing Single‑Pointer Alternative** — drag operations without click/tap alternative.

---

## Prioritization framework

**Severity (Structural / Content / Cross‑Platform):**
- **P0** — breaks core functionality, causes data loss, violates WCAG A, legal risk (APCA for gov/health), missing error recovery, impossible state transitions.
- **P1** — significant friction (missing state, confusing flow, cognitive overload, poor error messages, touch target violations, focus traps).
- **P2** — visual/design system inconsistencies, minor a11y issues (WCAG AA), motion performance, content tone inconsistencies.
- **P3** — micro‑details, cosmetic tweaks, delight opportunities.

**Severity (Affective / Emotional Design):**
- Tagged with `type: Affective` and severity based on user‑impact estimates.
- P1 if missing peak/pit moments in core flows; P2/P3 for polish.
- Always marked `confidence: Low` unless user explicitly requests implementation.

**Scoring for Structural items:** use deterministic proxies:
- **Interaction Depth:** number of clicks/taps to complete core task. >3 = high impact.
- **DOM Node Count:** >1000 per page → high impact.
- **State Coverage Gap:** missing states (no loading skeleton, no empty state, no offline) → high impact.
- **Cognitive Load proxy:** distinct visual groups per screen; >7 without grouping = high impact.
- **Telemetry Correlation:** if telemetry links a code issue to a drop‑off, severity +1.

**Sort order:** (1) Severity (P0 → P3), (2) Interaction Depth descending, (3) DOM Node Count descending, (4) Telemetry correlation strength, (5) Effort ascending (S before M before L).

**Fix now vs defer:**
- **Audit mode** — all findings stay `open`; remediation plan recommends Remediate mode.
- **Remediate mode** — fix P0 and P1 Structural/Content/Cross‑Platform items. Defer P2/P3 and unrequested Affective items with a reference.

---

## Remediation Rationale Gate

Before implementing any UI change (Remediate mode), generate a rationale scaled to severity:

### Tier 1: P0/P1 Structural Overhauls (Full Rationale Required)
- **Gestalt & Hierarchy:** How the change restructures perceptual grouping, improves visual hierarchy.
- **State Transition Map:** Exact before/after state machine logic (e.g., `loading → error → retry → success`).
- **Motion Choreography:** Semantic motion token applied and physical parameters. Ensure no layout‑thrashing properties.
- **Accessibility Fallback:** Degradation path for `prefers-reduced-motion` and screen‑reader users.
- **Content Impact:** How microcopy changes support the new state/flow.
- **Cross‑Platform Impact:** How touch, keyboard, and voice users are affected.

### Tier 2: P2/P3 Atomic Tweaks (Micro‑Rationale Required)
- **Rule Mapping:** Cite the specific systemic rule enforced (e.g., "Replaced `#FFF` with `var(--surface-primary)` per Token Topology Rule 1").
- **State Impact:** Confirm no state‑machine regression.
- **Content Impact:** Confirm copy changes are minimal and consistent.

Once the rationale is documented, implement the change.

---

## Remediation implementation guide

### Systemic fixes
- Replace raw hex values with semantic design tokens (OKLCH preferred).
- Normalise spacing to project's scale.
- Introduce modular typographic scale with reading‑science rules (line length, line height, paragraph spacing).
- Implement fluid typography via `clamp()`.
- Ensure dark‑mode tokens are mapped; avoid pure black; reduce saturation.
- Add missing tokens: elevation, z‑index, border, cursor.

### State‑space fixes
- Introduce strict state unions (TypeScript) for all data‑fetching components.
- Add loading skeletons for loading states.
- Add empty states with forward guidance.
- Add error states with recovery paths (What/Why/Fix/Prevention).
- Add offline, refreshing, rate‑limited, and partial‑success states.
- Validate state transitions with a state machine (XState or TS union exhaustiveness).

### Motion & Kinematics fixes
- Map transitions to semantic motion tokens.
- Use staggered entry for lists.
- Implement FLIP for layout changes.
- Replace layout‑thrashing animations with `transform`/`opacity`.
- Wrap all motion in `prefers-reduced-motion` checks.

### Content design fixes
- Rewrite error messages to answer What/Why/Fix/Prevention.
- Ensure button labels use verb‑noun structure.
- Add forward guidance to empty states.
- Reduce sentence length and jargon.
- Ensure success messages confirm the specific action.

### Cognitive load fixes
- Group options (categorized dropdowns).
- Enlarge touch targets to ≥44px (mobile), ≥24px (desktop).
- Add bounding containers for related elements.
- Reduce form fields per screen to ≤7.
- Ensure core tasks complete in ≤3 clicks.

### Emotional design fixes
- Add celebration to peak moments (success animations, confetti, mascot reactions).
- Soften pit moments (empathetic error copy, recovery paths, mascot consolation).
- Ensure end moments guide forward ("What's next?").
- Align copy, motion, color, and illustration to defined personality dimensions.

### Cross‑platform fixes
- Add logical properties for RTL.
- Add safe‑area insets.
- Ensure full keyboard navigation.
- Add single‑pointer alternatives for drag operations.
- Test touch targets on actual devices or DevTools.

---

## Verification & Testing

- After changes, run lint, typecheck, and unit tests for affected components.
- Run the **Design QA Gate** checklist.
- For visual changes, inspect representative pages and states.
- If render‑dependent heuristics are included, run Lighthouse/axe and include results.
- Validate state transitions with TypeScript exhaustiveness checking or XState visualizer.
- Mark runtime tests as confidence `Medium` and include results.

---

## Guardrails

- **Regression safety** — never change functionality unintentionally.
- **Repository discipline** — modify files freely; do **not** `git commit`/push unless explicitly asked.
- **Scope discipline** — stay in the scope set; note out‑of‑scope findings as `deferred`.
- **Document what you defer** — every deferred item gets `deferred(<ref>)`, never a mental note.
- **Accessibility first** — never implement a visual enhancement that degrades accessibility.
- **Performance budget** — never implement motion or imagery that violates RAIL or increases CLS.
- **Content is interface** — never treat copy as an afterthought; every state must have purposeful microcopy.

---

This skill elevates UI/UX from superficial polish to expert‑level systemic design. By rigorously auditing coherence, state choreography, semantic motion, cognitive ergonomics, human‑centered research, content design, emotional resonance, and cross‑platform accessibility, the agent creates the structural foundation upon which genuine user delight can flourish.
