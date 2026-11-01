---
name: web-artifact-and-app-building
description: >- For design artifacts rendered inside the OpenDesign app (DESIGN.md brand-bound, live preview, HTML/PDF/PPTX/MP4 export), see open-design.
  Build interactive web artifacts and small browser apps end to end: scope the
  artifact, choose between a single-file HTML build and a React + Tailwind +
  shadcn/ui multi-component project, scaffold it, develop it, bundle everything
  into one self-contained HTML file, then verify it in a real browser and
  iterate. Use when the user says "build me an artifact", "make an interactive
  dashboard / tool / landing page", "create a React artifact with shadcn",
  "bundle this into a single HTML file", "test this app in a browser", "why is
  my artifact blank", or asks to scope, prototype, ship, or debug a
  browser-based deliverable. Architecture, build, bundling, and Playwright
  browser verification are one workflow here — verification is not an optional
  extra step. Do not use for how it looks: visual direction, palette,
  typography, and branding belong to visual-design-and-branding; for slide
  decks, Word documents, or spreadsheets (presentation-authoring,
  word-document-authoring, spreadsheet-authoring); or for authoring agent
  skills, plugins, and MCP servers (skill-authoring-and-agent-tooling).
license: Apache-2.0
---

# Web Artifact and App Building

The spine is **scope → architecture → build → verify → iterate**. Two things are
non-negotiable about it: the architecture choice happens *before* scaffolding, and the
browser check is the second half of building, not a courtesy step afterwards. An
artifact that has never been rendered and clicked is a proposal.

This skill owns the build and its verification. Visual direction — palette, type,
whether the page reads as generic — is `visual-design-and-branding`, called at step 4
and nowhere else; do not drift into design advice here.

## When to use

- "Build me an artifact" — interactive tools, dashboards, explorers, calculators,
  wizards, landing pages, demos
- Multi-component work: "make it a React app", "use shadcn for this", state, routing,
  complex forms, component reuse
- Delivery: "bundle this into a single HTML file", producing one self-contained file
  that opens with no server
- Verification: "test this in a browser", "screenshot the app", "check the console for
  errors", "does this actually work"
- Debugging a broken artifact: blank page, unstyled UI, failed bundle, missing assets
- Scoping: deciding whether a request is one file or a project before any code is
  written

**Do not use for** — `visual-design-and-branding` when the question is the artifact's
appearance, palette, typography, or brand fit rather than its structure and behaviour;
`presentation-authoring`, `word-document-authoring`, or `spreadsheet-authoring` when
the deliverable is a deck, document, or workbook rather than a browser artifact;
`skill-authoring-and-agent-tooling` when what needs building is an agent skill, plugin,
or MCP server rather than a web interface.

- Deal-specific sales assets (landing pages, decks, one-pagers for a particular prospect) — use the **create-an-asset** skill; architecture/workflow/sequence diagrams — **archify**; slide decks — **presentation-authoring** or **open-slide**.

## Workflow

1. **Scope the artifact.** Write down: what the user does with it (the 2–4 primary
   interactions), whether there are multiple views or URL state, where state lives and
   how long it persists, whether data is fetched or embedded, where it will be
   consumed (chat artifact, pasted file, hosted page), and what "works" means for it.
   Anything out of scope gets named as out of scope now — that list is the acceptance
   criteria for step 6.

2. **Choose the architecture.** Decide from the scope, not from habit:

   | Scope signals | Architecture |
   |---|---|
   | One page, no routing, local state only, light interactivity | **Single-file HTML** — inline CSS/JS, no build step, opens from `file://` |
   | Multiple views, real state, forms with validation, component reuse, data fetching | **React 18 + TypeScript + Vite + Tailwind + shadcn/ui** project, bundled to one file |

   Full decision table, middle paths, and the failure mode of each branch:
   [architecture-selection.md](references/architecture-selection.md).

3. **Scaffold or write directly.**
   - *Single-file branch:* write the `<!DOCTYPE html>` yourself — one file, no
     dependencies beyond at most one CDN script.
   - *React branch:* `bash scripts/web-artifacts-builder/init-artifact.sh <name>` then
     `cd <name> && pnpm dev`. You get Tailwind 3.4.1 with the shadcn token set, the
     `@/` path alias, 40+ pre-installed shadcn/ui components, all Radix dependencies,
     `components.json`, and Node-version-aware Vite pinning. Import components as
     `@/components/ui/<name>`. Node 18+ required.
     Detail and troubleshooting:
     [react-setup-and-bundling.md](references/react-setup-and-bundling.md).

4. **Build against the anti-slop floor.** Implement the scoped interactions and make
   the components the scope actually needs. Minimum bar while coding: no excessive
   centered layouts, no purple gradients, no uniform rounded corners, no default Inter
   everywhere — a brief-level refusal of templated output. Deeper direction (palette,
   type scale, hero treatment) is requested from `visual-design-and-branding` for the
   design brief, then implemented here. Keep CSS selector specificity from cancelling
   itself out, especially padding/margin between type-based and element-based
   selectors.

5. **Bundle to one HTML file.** React branch only:
   `bash scripts/web-artifacts-builder/bundle-artifact.sh` → `bundle.html`, with all
   JS, CSS, and assets inlined by Parcel + `html-inline`. Preconditions: run from the
   project root, root `index.html` present. Single-file branch skips this step — the
   file already is the bundle. Steps, preconditions, and failure table:
   [react-setup-and-bundling.md](references/react-setup-and-bundling.md).

6. **Verify in a browser.** Mandatory unless the user explicitly says to skip it, and
   the only step that can fail silently if skipped.

   | Artifact | Serve how | Test how |
   |---|---|---|
   | Single-file HTML | none — `file://` | Playwright against the file path |
   | React dev server | `with_server.py --server "pnpm dev" --port 5173` | Playwright against `http://localhost:5173` |
   | Delivered `bundle.html` | none — `file://` | Playwright against the file: this is the artifact the user receives |

   Script pattern: `sync_playwright()`, headless Chromium, `goto` →
   `wait_for_load_state('networkidle')` → reconnaissance-then-action (screenshot, read
   the DOM, discover selectors, *then* interact) → exercise each scoped interaction →
   screenshot → capture console output → `browser.close()`. Run the scripts in
   `scripts/webapp-testing/` as black boxes (`--help` first; never read their source to
   decide how to call them). Full protocol, server helper usage, and the runnable
   examples: [browser-verification.md](references/browser-verification.md).

7. **Verify in depth (the triad).** Browser verification is mandatory unless the user explicitly says
   to skip it — but it is only one of three independent checks, ordered by cost:
   1. **Machine gates** — `ai-design-check` on the generated source, `diagram-design`'s verifiers on
      any shipped SVG figure, the build's own math/type gate. A gate that has never been observed
      failing doesn't count as a gate: plant one violation and watch it fire, once per project.
   2. **Rendered frames** — the browser run from the table below, then read its screenshots as
      images: seven views minimum for figures, interaction run-throughs from `?press=`-style URL
      params, phone and dark where claimed, plus the exact embed geometry the host will use.
   3. **The deployed smoke** — the only check the visitor meets. If the artifact ships to a vhost
      (or any host with a CSP), the deliverable is the deployed URL and **every** check's final
      answer is measured there: asset 200s + content types, cold-cache headless render, video
      `readyState`, zero pageerrors on one interaction.
   Full protocol: [verify-loop.md](references/verify-loop.md) and
   [deploy-contract.md](references/deploy-contract.md).

8. **Iterate, re-verify, deliver.** Fix what the run surfaced — console errors,
   selectors that never appeared, clipping at mobile width, a flow that needs two
   clicks where the scope said one — then re-run *only* the checks that failed plus a
   final render from the **deployed** URL when one exists. Hand over the deliverable with a short
   note: what it does, how to open it, what was verified at which layer, what was not — the honest
   residue by name, never hidden.

## Quality bar

- [ ] Scope written down before coding: primary interactions, state, delivery target,
      and an explicit out-of-scope list
- [ ] Architecture choice stated with its reason — and it matches the scope signals
- [ ] React branch: `init-artifact.sh` used as-is (no hand-rolled Tailwind/tsconfig),
      `@/` alias works, components imported from `@/components/ui/*`
- [ ] Bundle builds without errors and `bundle.html` loads standalone over `file://` —
      no dev server, no unbundled asset, no missing import
- [ ] Rendered at least once in a real browser — screenshot reviewed as an image —
      with every scoped interaction clicked through, not just the page load
- [ ] Console clean on the paths exercised — no uncaught errors or failed requests
- [ ] Mobile-width render checked for clipping and overflow; keyboard focus visible
- [ ] `ai-design-check` gate run over the source (never the built bundle): exit 0 or every finding
      above a committed baseline resolved; class-string false positives counted, not fixed silently
- [ ] Every check whose answer matters was measured at the **deployed** URL, cold cache — never
      `file://` (deploy-contract.md §§1–3): asset 200s + content-types, CSP verified with `curl -I`
      on both page classes, inlined `data:` assets against their policy
- [ ] Baked/live state precedence asserted in code and exercised with an empty live store (§4)
- [ ] Zero pageerror at default params and one interaction from the embed (§5) — a blank canvas is
      an import bug until proven otherwise
- [ ] Embedded pages measured at four widths × two heights; the pinned band + reason live in a
      host-page CSS comment (§6)
- [ ] Anti-slop floor met: no centered-layout/purple-gradient/uniform-radius/default-font
      cluster unless the brief asked for it
- [ ] Playwright runs used `networkidle` before inspection, launched headless, and
      closed the browser
- [ ] Delivery note states what was verified and what was skipped, with a reason

### Failure modes

- **Shipping the unrendered** — code read and assumed correct because it looks right
- **Testing nothing** — "optional step" treated as "skip the step"; verification is
  only skippable when the user says so
- **Selector guessing** — acting before reconnaissance on a dynamic app
- **Inspecting too early** — reading the DOM before `networkidle` and reporting a
  component as missing
- **Helper source ingestion** — reading `with_server.py` or the build scripts into
  context instead of running them
- **Server when none is needed** — standing up a dev server to check a `file://`
  artifact
- **Verify-the-wrong-thing** — testing `pnpm dev` and delivering `bundle.html`, the
  file that never ran
- **Scope creep in step 4** — building the interaction the brief implied instead of the
  one that was scoped
- **Design drift** — spending the turn on palette and type advice owned by
  `visual-design-and-branding`

## Reference map

| Situation | Open |
|---|---|
| Single-file vs React/shadcn decision, trade-offs, middle path | [references/architecture-selection.md](references/architecture-selection.md) |
| `init-artifact.sh` / `bundle-artifact.sh` usage, dev loop, troubleshooting | [references/react-setup-and-bundling.md](references/react-setup-and-bundling.md) |
| Playwright verification: server helper, recon-then-action, what to check, examples | [references/browser-verification.md](references/browser-verification.md) |

Carried helpers: `scripts/web-artifacts-builder/` (`init-artifact.sh`,
`bundle-artifact.sh`, `shadcn-components.tar.gz` — the component payload the scaffold
extracts) and `scripts/webapp-testing/` (`with_server.py` plus `examples/` with
`element_discovery.py`, `static_html_automation.py`, `console_logging.py`).

## Output format

```markdown
# <artifact name> — delivery note
WHAT IT DOES:  [2–3 lines: the interactions, in user terms]
ARCHITECTURE:  single-file | React + Tailwind + shadcn/ui — [reason]
FILES:         [bundle.html | index.html + src/ — the one thing to open]
OPEN IT:       double-click bundle.html | pnpm dev → <url>
VERIFIED:      [checks that passed — flows exercised, viewport, console, screenshot]
NOT VERIFIED:  [what was skipped and why]
KNOWN GAPS:    [out-of-scope items and anything unfinished]
```

Single-file artifacts may skip the note's VERIFIED block only when the user asked to
skip verification; everything else ships with it.
