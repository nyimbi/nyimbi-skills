# skill-bundle

A single, deduplicated bundle of **143 skills**: **30 domain skills** consolidated
from **876 unique source skills** across five upstream collections, **55
skills adopted** from the user's live skill set (`~/.claude/skills`,
`~/.agents/skills`, `~/.pi/agent/skills`) after every internal duplicate was
merged, **51 skills adopted** from external projects, and **7 new film-production
syntheses** (`film-production`, `film-story-development`, `film-design`,
`character-design`, `film-generation`, `film-postproduction`, `film-poster`) plus
the earlier `business-plan-authoring`.

The external set: 3 platform wrappers (`open-slide` MIT, `open-design`
Apache-2.0, `open-montage` AGPLv3), 1 `open-code-review` (Apache-2.0), 4 official
Hugging Face skills, 1 Playwright webapp-testing skill, 1 curated
scientific-research subset (MIT), 1 Obsidian skill (MIT), 3 session-behavior
skills (`ponytail`, `caveman`, `i-have-adhd`, all MIT), 10 official Pydantic
skills (core, AI harness, 8 framework-migration guides), 23 official LangChain
skills (LangChain, LangGraph, Deep Agents, swarm, evals), and 3 adopted film
skills (`film-directing` MIT from DirectorSKILL, `ai-video-directing` and
`ai-image-art-direction` CC BY 4.0 from Visual Skills).

| | |
|---|---|
| Upstream source skills in scope | 890 |
| Upstream duplicate collapses | 14 (13 exact-name pairs + 1 near-duplicate pair) |
| Unique upstream sources merged | 876 |
| Personal skills adopted | 63 → **55** (8 duplicate overlaps merged away; 1 dangling link dropped) |
| External skills adopted | **52** (platforms, HF, testing, scientific, obsidian, behavior, Pydantic, LangChain, impeccable, film, design gate) |
| New film syntheses | **7** (production, story, design, character, generation, post, poster) |
| New engine syntheses | **1** (`machine-works` — two-engine routing skill: April Zhu's colorfigures SVG engine + elvarofficial/teardown three.js pipeline, each vendored intact as `engines/ink` / `engines/webgl` with a shared doctrine in SKILL.md) |
| New course syntheses | **1** (`course` — the seven-phase curriculum method proven on the Agentic Engineering course: capability → outline → critique → rewrite → paced lessons → corrections → synthesis; default 20 lessons at ≥10,000 words with tables and drawn SVG diagrams) |
| Bundle skills | **146** (30 consolidated + 55 personal + 52 external + 7 film + 1 engine synthesis + 1 course synthesis) |
| Upstream compression | ~30x (817 cyber skills → 13 domain skills) |
| Deliberately excluded | 832 `composio-skills` generated API automations |

Each bundle skill is a `SKILL.md` (the 30 consolidated ones run 155–298 lines —
the synthesized domain method, workflow and quality bar; adopted external
skills keep their original length, 54–585) plus `references/` for on-demand
depth and `scripts/` for executable helpers. An agent reads `SKILL.md` first
and pulls a reference file only when the situation warrants it.

---

## Skills

### Cybersecurity (13 skills, from 817)

| Skill | Merged from | Covers |
|---|---:|---|
| `security-incident-response-and-soc` | 102 | Alert triage, severity/SLA, containment, eradication, recovery, post-incident review, playbooks, SOC machinery |
| `threat-hunting-and-detection` | 71 | Hypothesis-driven proactive search, detection rule engineering, Sigma/SPL, deception, baselining |
| `digital-forensics-and-evidence` | 41 | Forensically sound acquisition, chain of custody, disk/memory/timeline/artifact analysis |
| `malware-analysis-and-reverse-engineering` | 39 | Safe handling, static/dynamic triage, unpacking, RE, behavior and IOC extraction |
| `offensive-security-and-red-teaming` | 59 | Authorized red team, adversary emulation, pentesting, AD attacks, C2, ROE gate |
| `cloud-container-and-devsecops-security` | 117 | Commit-to-runtime: CI secrets, SAST/SCA, IaC scan, image hardening, K8s admission, CSPM/CWP |
| `network-and-wireless-security` | 45 | Segmentation, IDS/IPS, traffic analysis, wireless assessment, WAF/NGFW |
| `identity-zero-trust-and-endpoint-security` | 75 | IAM, conditional access, PAM/JIT, MFA/FIDO2, zero-trust maturity, endpoint controls |
| `threat-intelligence-osint-and-phishing-defense` | 76 | TI lifecycle, OSINT, STIX/TAXII/MISP, actor profiling, phishing analysis and simulation |
| `application-api-mobile-and-ai-security` | 103 | Web/API/mobile/LLM testing methodology, OWASP, BOLA, prompt injection, guardrails |
| `vulnerability-management-and-compliance` | 38 | Discover → scan → prioritize (CVSS+KEV+EPSS+SSVC) → SLA → exceptions → framework mapping |
| `ot-ics-and-firmware-security` | 35 | Purdue/IEC 62443 zones, safe OT assessment, SCADA protocols, firmware extraction |
| `cryptography-and-key-management` | 16 | Encryption design, key hierarchy, HSM/PKCS#11, PKI/TLS, signatures, PQC migration |

### Strategy & consulting (7 skills, from 21 playbooks + 1 consulting method + 1 new)

| Skill | Merged from | Covers |
|---|---:|---|
| `strategy-diagnosis-and-framing` | 13 | **Owns the method layer**: depth modes, MECE, issue trees, hypothesis, evidence, synthesis, plus situation/growth/assumption diagnosis |
| `market-and-competitive-intelligence` | 7 | Market sizing, segmentation, profit pools, competitor response modelling, ad-library mining. Owns `frameworks-strategy.md` |
| `strategic-choices-and-economics` | 8 | Option generation, business cases, portfolio review, pricing. Owns decision/financial/pricing frameworks |
| `operating-model-and-execution` | 6 | Capabilities, decision rights, governance, initiative prioritisation, transformation roadmap |
| `risk-performance-and-value-governance` | 5 | KPI design, value ledger, risk register, war gaming |
| `executive-communication-and-alignment` | 4 | Decision memos, Pyramid/SCQA narratives, stakeholder pre-wiring |
| `business-plan-authoring` | — (new) | Venture-grade business plans that survive a hostile funder: live web research with citations, driver-based 24–36 month projections, per-section defense template, mandatory red-team pass, and a plan-to-deck compression map (hands the `.pptx` to `presentation-authoring`). Composes the five skills above |

### Personal operations & craft (58 skills, adopted from the live skill set)

Adopted from `~/.claude/skills`, `~/.agents/skills`, and `~/.pi/agent/skills` as the
single source of truth. Content preserved as-is (including command-style
`argument-hint` frontmatter and `~~connector` placeholders); only the `CONNECTORS.md`
pointer was rewritten to plain text, and five duplicate pairs were merged (marked M).

| Domain | Skills |
|---|---|
| **Sales & CRM (8)** | `account-research` · `call-prep` · `call-summary` · `create-an-asset` · `daily-briefing` · `draft-outreach` · `forecast` · `pipeline-review` |
| **Marketing & SEO (6)** | `brand-review` · `campaign-plan` · `content-creation` (M) · `email-sequence` · `performance-report` · `seo-audit` |
| **Finance & accounting (6)** | `close-management` · `financial-statements` · `journal-entry` (M) · `reconciliation` · `sox-testing` (M) · `variance-analysis` |
| **Product & research (7)** | `jobs-to-be-done` · `metrics-review` · `product-brainstorming` · `research-synthesis` (M) · `roadmap-update` · `user-research` · `write-spec` (incl. mattpocock grilling + domain-modeling) |
| **Competitive (1)** | `competitive-brief` (M — written analysis + interactive HTML battlecard artifact) |
| **Engineering & delivery (12)** | `architecture` · `code-review` · `debug` (incl. superpowers systematic-debugging method) · `deploy-checklist` · `documentation` · `incident-response` · `open-code-review` (external, Apache-2.0 — dedicated precision review CLI, `ocr`; on this machine wired to local Ollama `qwen3.6-coding`, verified end-to-end) · `security-review` · `sprint-planning` · `system-design` · `tech-debt` (M) · `testing-strategy` (incl. superpowers TDD red-green-refactor) |
| **Design & UX (7)** | `accessibility-review` · `archify` · `design-critique` · `design-handoff` · `design-system` · `ux-copy` · `ux-excellence` |
| **Design platforms & decks (3)** | `open-slide` (external, MIT — agent-authored React decks on a 1920×1080 canvas) · `open-design` (external, Apache-2.0 — the OpenDesign app: brand-bound prototypes, dashboards, decks, images, MP4 with live preview and HTML/PDF/PPTX/MP4 export; app + MCP already installed on this machine) · `impeccable` (external, Apache-2.0 — Paul Bakaus's design language for AI harnesses, v4.7.0: 1 skill, 24 commands, the anti-pattern detector over slop / quality / type / layout / a11y rule packs, live browser iteration, `--cdp` desktop-app scans; Rust engine 0.1.16 fetched and sha256-verified on demand into `~/.impeccable/bin/`, telemetry disabled in `~/.impeccable/config.json`. Three local additions to `reference/`: the frame measurements in `layout.md`, the competitor test in `new-work.md`, and open-collection sourcing in `visualize.md`) |
| **ML & science (5)** | `huggingface-llm-trainer` (TRL SFT/DPO/GRPO on HF Jobs + GGUF conversion) · `huggingface-community-evals` (inspect-ai/lighteval local evals) · `huggingface-trackio` (experiment tracking) · `huggingface-local-models` (llama.cpp/GGUF on Metal/CUDA/ROCm) · `scientific-research` (external, MIT — K-Dense subset: paper-lookup, literature review, publication figures, sklearn/PyTorch Lightning, 78 scientific databases) |
| **Film production (10)** | End-to-end narrative film and series: `film-production` (state machine, gates, budget, series) · `film-story-development` (premise → screenplay → series bible) · `film-design` (style lock, world bible, continuity) · `character-design` (sheet, identity lock, voice, drift audit) · `film-directing` (external, MIT — DirectorSKILL: previs, blocking, shot list, 20 lenses, F1–F19 failure manual) · `film-generation` (providers, prompt compilation, variants, QA, logs) · `film-postproduction` (edit, sound, finish, QC, delivery) · `film-poster` (key art, one-sheet, thumbnail, character posters, title treatment) · `ai-video-directing` (external, CC BY 4.0 — Visual Skills: dramaturgy + Seedance/Kling/Veo syntax) · `ai-image-art-direction` (external, CC BY 4.0 — character sheets, plates, storyboard panels) |
| **Video production (1)** | `open-montage` (external, AGPLv3 — 12 production pipelines, 121 tools / 51 available zero-key, approval gates + budget caps + post-render self-review; runtime at `~/Developer/openmontage`, verified) |
| **Testing (1)** | `webapp-testing` (external, Apache-2.0 — Anthropic's Playwright toolkit for local web apps) |
| **Note-taking (1)** | `obsidian` (external, MIT — kepano/obsidian-skills subset: CLI, Obsidian-flavored Markdown, JSON Canvas, Bases; vault `~/src/pjs/work_docs`) |
| **Session behavior (3)** | `ponytail` (lazy senior dev: YAGNI, stdlib first) · `caveman` (token-compressed output, 3 intensity levels) · `i-have-adhd` (ADHD-friendly output shaping; user-invoked) — all external, MIT; opt-in session styles, one-line cross-notes |
| **Media & video (2)** | `cinematic-pipeline` · `video-use` |
| **Writing & comms (3)** | `humanizer` · `stakeholder-update` · `standup` |
| **AI & agent tooling (13)** | `building-pydantic-ai-agents` (cross-checked against upstream, 2026-09-28) · `pydantic` (core data validation) · `pydantic-ai-harness` (Code Mode, filesystem/shell, sub-agents, planning, compaction) · 8× `migrating-*-to-pydantic-ai` (langchain, openai-agents-sdk, claude-agent-sdk, google-adk, mastra, agno, pi, vercel-ai-sdk+eve) · `codebase-memory` · `find-skills` · `zvec` |
| **Agent frameworks (23)** | `langchain-fundamentals` · `langchain-rag` · `langchain-middleware` · `langchain-dependencies` · `langchain-{python,typescript}-quickstart` · `langgraph-fundamentals` · `langgraph-persistence` · `langgraph-decision-models` · `langgraph-human-in-the-loop` · `langgraph-cli` · `deep-agents-{core,orchestration,memory}` · `deepagents-{python,typescript}-quickstart` · `swarm` · `managed-deep-agents` · `eval-engineering` · `langsmith-online-eval-engineering` · `ecosystem-primer` — all external, MIT, official langchain-ai skill set |

**Duplicates merged away (M and fold-ins):**
`journal-entry`+`journal-entry-prep` → `journal-entry`;
`research-synthesis`+`synthesize-research` → `research-synthesis`;
`tech-debt`+`remove-tech-debt` → `tech-debt`; `draft-content`+`content-creation` →
`content-creation`; `marketing-competitive-brief`+`product-management-competitive-brief`
→ `competitive-brief`; `audit-support`+`sox-testing` → `sox-testing`;
`competitive-intelligence` folded into `competitive-brief`
(HTML battlecard spec now `references/battlecard-artifact.md`); `frontend-design`
folded into `visual-design-and-branding` (unique material now in
`references/ui-craft.md`).

**Method merges into existing skills (external, adopted as references):**
`obra/superpowers` (MIT) `systematic-debugging` 4-phase process → `debug`;
`obra/superpowers` `test-driven-development` red-green-refactor →
`testing-strategy`; `mattpocock/skills` (MIT) `grilling` + `domain-modeling`
(grill-with-docs pattern: relentless frontier interview + `CONTEXT.md`
glossary + ADRs) → `write-spec`.

**Platform skills adopted as boundaries, not merges:** `open-slide` (the
framework's 5 agent skills + 7 primitive references, verbatim) and
`open-design` (a routing entry point into the OpenDesign app — its 163
functional skills are indexed in `open-design/references/skill-catalog.md`
but **not** merged, since they run inside the OD daemon and overlap both
each other and bundle skills). Both carry two-sided routing notes against
`presentation-authoring`, `design-system`, `visual-design-and-branding`,
`web-artifact-and-app-building`, and `create-an-asset`. `open-code-review`
(the project's own agent skill, adapted) is bounded two-sided against
`code-review` (in-session general PR review) and `security-review`; its
delegation-mode companion skill was dropped as redundant with
`code-review` (`ocr delegate` remains available directly).

**Overlap boundaries** — every remaining adjacency has two-sided routing notes
("Routing:" / "Do not use for") so a request has exactly one home:
("Routing:" / "Do not use for") so a request has exactly one home:
`incident-response` (SRE) ↔ `security-incident-response-and-soc` (breach/IR);
`security-review` (file/diff) ↔ `application-api-mobile-and-ai-security` (full
assessment) ↔ `code-review` (general PR review); `competitive-brief` (analysis +
battlecard) ↔ `market-and-competitive-intelligence` (strategic reading);
`user-research` (conduct) ↔ `research-synthesis` (process) ↔
`research-and-insight-analysis` (non-user-research questions);
`architecture` (ADR) ↔ `system-design` (design); `account-research` ↔ `call-prep`
↔ `draft-outreach`; `forecast` ↔ `pipeline-review`; `metrics-review` ↔
`performance-report` ↔ `variance-analysis`; `documentation` ↔
`writing-and-internal-communications`; `create-an-asset` ↔ `content-creation` ↔
`web-artifact-and-app-building` ↔ `archify` ↔ `open-design`; `presentation-authoring` ↔
`open-slide` ↔ `open-design`; `video-use` ↔ `cinematic-pipeline`; the design cluster
(`ux-excellence` ↔ `design-critique` ↔ `design-system` ↔ `accessibility-review` ↔ `open-design`);
`email-sequence` ↔ `content-creation`; `seo-audit` ↔ `content-creation`;
`brand-review` ↔ `content-creation`; `standup` ↔ `stakeholder-update` ↔
`daily-briefing`.

`strategy-diagnosis-and-framing/SKILL.md` defines the bundle-wide **depth modes**
(Quick Structure / Full Case / Client Deliverable); the other five link to it rather
than redefining it.

### Documents, writing & tooling (10 skills, from 52 + 19)

| Skill | Merged from | Covers |
|---|---:|---|
| `pdf-processing` | 2 | Merge/split/rotate/OCR/forms/encrypt — 2 revisions merged |
| `word-document-authoring` | 2 | .docx authoring, tracked changes, comments, OOXML tooling |
| `presentation-authoring` | 2 | .pptx decks, layouts, html2pptx, speaker notes |
| `spreadsheet-authoring` | 2 | .xlsx formulas, formatting, charts, recalculation |
| `writing-and-internal-communications` | 7 | Co-authoring workflow, internal comms formats, research-backed drafting, changelogs, resumes |
| `visual-design-and-branding` | 9 | Design-decision sequence, themes, brand system, canvas/algorithmic art, UI craft |
| `web-artifact-and-app-building` | 4 | Single-file vs React/Tailwind/shadcn artifacts + Playwright verification |
| `skill-authoring-and-agent-tooling` | 11 | Skill authoring/evals, MCP servers, Claude API reference, agent debugging |
| `research-and-insight-analysis` | 4 | One research method across lead, meeting, growth and naming questions |
| `file-media-and-engagement-tools` | 7 | File/invoice organisation, video download, Slack GIFs, fair raffle, tweet optimisation |

---

## How it is organised

```
skill-bundle/
├── README.md                     this file
├── sync-skills.py                mirrors skills/ into the agent skill roots
├── skills/<skill>/
│   ├── SKILL.md                  the only file an agent reads first
│   ├── LICENSE | LICENSE.txt     carried from sources (MIT / Apache-2.0 / Anthropic)
│   ├── references/
│   │   ├── technique-index.md    generated catalog (cyber skills) — complete coverage
│   │   ├── <technique>.md        per-technique deep detail, one file per source
│   │   └── <topic>.md            synthesized cross-cutting analysis
│   └── scripts/<technique>/      executable helpers, namespaced by origin
└── _build/                       build metadata — NOT a skill, no SKILL.md inside
    ├── SPEC.md                   the consolidation spec every skill follows
    ├── merge_cyber.py            regenerates the cyber reference/script layer
    ├── cyber-clusters.json       817 techniques → 13 clusters
    └── provenance/<skill>.json   what each skill was merged from (142 files)
```

### Two classes of reference file

- **Per-technique** (`references/<technique>.md`) — mechanically merged from each
  source skill's `api-reference.md` + `standards.md` + `workflows.md` +
  `template.md`. One file per source technique, deduplicated bundle-wide. 817 of
  these exist for cybersecurity.
- **Synthesized** (`references/<topic>.md`) — written during consolidation where
  cross-cutting analysis genuinely adds value (tool-selection matrices,
  prioritisation formulas, evidence-handling rules).

`SKILL.md` never restates what a reference file already says; `references/` never
restates `SKILL.md`.

---

## Deduplication report

### Exact duplicates collapsed (13 pairs)

Every one of these existed in both `skills/skills/` and `awesome-claude-skills/`.
Most were **differing revisions, not identical files** — both were diffed and the
richer content merged rather than one being discarded:

| Skill | Collapsed into |
|---|---|
| `pdf`, `docx`, `pptx`, `xlsx` | `pdf-processing`, `word-document-authoring`, `presentation-authoring`, `spreadsheet-authoring` |
| `internal-comms`, `brand-guidelines`, `theme-factory`, `canvas-design` | byte-identical — kept once |
| `webapp-testing` | `web-artifact-and-app-building` |
| `web-artifacts-builder` + `artifacts-builder` | `web-artifact-and-app-building` (same skill, two names) |
| `mcp-builder`, `skill-creator` | `skill-authoring-and-agent-tooling` |
| `slack-gif-creator` | `file-media-and-engagement-tools` |

Plus 1 near-duplicate collapse: `connect` + `connect-apps` → one topic in
`skill-authoring-and-agent-tooling`.

### Near-duplicate groups consolidated inside cybersecurity

Where the same technique was covered by several source skills, `SKILL.md` discusses
it once while the distinct source documents remain available. Full list per skill is
in `_build/provenance/<skill>.json` under `near_duplicate_groups`. Examples:

- 4 Trivy scanners → one image-scanning topic
- 3 Calico network-policy skills → one network-policy topic
- 2 post-quantum migration skills, 2 HSM skills, 2 memory-forensics skills
- 3 LOLBAS skills, 3 gophish skills, 2 fileless-malware skills
- 3 STIX/TAXII skills, 3 MISP skills, 2 dark-web skills
- 4 zero-trust NPA/BeyondCorp skills, 2 FIDO2 passwordless skills

### Dropped with reason

- **832 `composio-skills/*-automation`** — machine-generated third-party API catalog,
  excluded by decision. Repetitive boilerplate that would swamp the bundle.
- `template-skill` — a placeholder stub; its structure folded into authoring guidance.
- Generated boilerplate lines in cyber sources (e.g. *"When deploying or configuring
  \<name\> capabilities in your environment"*) — removed during synthesis.
- Superseded script revisions where two revisions of a helper differed only in
  comments or formatting; genuinely divergent implementations are kept side by side
  and named `scripts/skills-…` / `scripts/awesome-…` with the preferred one stated.

---

## Provenance & reproducibility

Every skill has `_build/provenance/<skill>.json` recording its source roots, the
exact count merged, duplicate collapses, drops with reasons, and the files it now
contains. The cybersecurity reference/script layer is regenerable:

```bash
python3 _build/merge_cyber.py     # rewrites references/, scripts/, LICENSE for the 13 cyber skills
```

`_build/` contains no `SKILL.md`, so skill loaders ignore it.

---

## Verification

The 30 consolidated skills are checked to the full spec; the 55 personal, 51
external and 6 film syntheses are checked for structural integrity (adopted skills
keep their original frontmatter and body style, so the consolidated
description/line-count bars do not apply to them).

Consolidated 30:

- [x] `name` frontmatter equals directory name — 30/30
- [x] description 120–220 words (actual range 127–188) with verbatim triggers and a
      `Do not use for` boundary — 30/30
- [x] body sections in spec order (`When to use` → `Workflow` → `Quality bar` →
      `Reference map` → `Output format`) — 30/30
- [x] SKILL.md within 150–450 lines (actual range 155–298) — 30/30
- [x] every `Reference map` link resolves — 0 broken
- [x] licence carried wherever a source shipped one — 28/30
      (`research-and-insight-analysis` and `business-plan-authoring` have none:
      the former because none of its 4 sources shipped a licence, the latter
      because it is a new synthesis of bundle content, not a merge of a
      licensed source file)

All 143 (re-verified 2026-10-30, after the film-family adoption):

- [x] `name` frontmatter equals directory name — 143/143
- [x] description present — 143/143
- [x] provenance JSON valid, complete, no orphans — 142/143
      (`impeccable` still has none; it was adopted after the provenance audit)
- [x] no broken authored relative links — 0 broken
- [x] no name collisions between consolidated, personal, external and film sets
- [x] every functional overlap resolved: 8 merges/fold-ins + two-sided routing
      notes on all remaining adjacencies
- [x] 817/817 cybersecurity techniques present in a technique index
- [x] film family: `filmctl.py` typechecks, scaffolds, validates, compiles prompts
      and assembles a two-shot rough cut end to end (2026-10-30)

### Known limitations

- Two links inside verbatim-copied reference material were source defects upstream
  (a bare `2000` that reads as a link, since removed; a doc-site absolute path,
  since neutralised). Authored files are clean.
- Per-technique reference files are merged source documents, not rewritten prose.
  They are lookup material; the synthesis lives in `SKILL.md`.
- The 809 `agent.py` / 282 `process.py` helpers were copied, not audited. They assume
  their original tooling is installed and authorized.

---

## Syncing to agents

`sync-skills.py` mirrors every skill in `skills/` into the skill roots of the
agents on this machine, as symlinks (edit the bundle, every agent sees it
live). Default roots: `claude` (`~/.claude/skills`), `opencode`
(`~/.config/opencode/skill`), `agents` (`~/.agents/skills`), `pi`
(`~/.pi/agent/skills`), `codex` (`~/.codex/skills`).

```bash
python3 sync-skills.py --dry-run          # preview
python3 sync-skills.py                     # sync all roots
python3 sync-skills.py --prune             # also remove links for skills
                                           # deleted from the bundle
python3 sync-skills.py --copy              # copies instead of symlinks
python3 sync-skills.py --root ~/other/skills   # extra root (repeatable)
python3 sync-skills.py --only claude pi     # restrict roots
python3 sync-skills.py --list               # list bundle skills
```

Safety: a per-root manifest (`.skill-bundle-manifest.json`) records what the
script owns. Existing entries that are real directories or foreign symlinks are
conflicts — they are reported and left untouched unless `--force` is passed
(which moves them aside as `<name>.conflict-<ts>`, never deletes). Pruning only
removes entries the manifest says are the script's. After adding/renaming/deleting
skills, re-run (with `--prune` for removals) and start a fresh agent session —
agents index skill names/descriptions at session start, but skill *bodies* are
read live from disk.

---

## Sources

| Repository | In scope |
|---|---|
| `Cybersecurity-Skills/` | 817 skills |
| `awesome-claude-skills/` | 32 hand-written (832 composio excluded) |
| `skills/skills/` | 19 Anthropic skills + 1 template |
| `strategy-skills-for-claude/` | 21 playbooks in 6 phases |
| `management-consulting/` | 1 skill + 11 framework references + 4 worked examples |
| Personal skill set (`~/.claude/skills`, `~/.agents/skills`, `~/.pi/agent/skills`) | 63 unique skills → 55 after merging 8 duplicate overlaps (originals removed from the agent roots; the bundle is now the single source of truth) |
| [open-slide](https://github.com/open-slide/open-slide) (MIT) | 5 agent skills (`create-slide`, `slide-authoring`, `create-theme`, `current-slide`, `apply-comments`) + 7 primitive references, adopted verbatim as reference docs of the `open-slide` skill |
| [open-design](https://github.com/nexu-io/open-design) (Apache-2.0) | Platform wrapper: 163-skill catalog index, design-system package contract, and setup/MCP docs (the app, plugins, templates, and 151 design systems are used in place from the installed app) |
| [open-code-review](https://github.com/alibaba/open-code-review) (Apache-2.0) | The project's own agent skill, adapted for this machine (brew CLI + local Ollama provider, verified model viability table) |
| [OpenMontage](https://github.com/calesthio/OpenMontage) (AGPLv3) | Platform wrapper: runtime at `~/Developer/openmontage` (verified: 121 tools, 51 available zero-key); skill-index + 6 core compositor skills as references |
| [Hugging Face](https://github.com/huggingface/skills) (Apache-2.0) | 4 official skills adopted verbatim: llm-trainer, community-evals, trackio, local-models |
| [anthropics/skills](https://github.com/anthropics/skills) (Apache-2.0) | `webapp-testing` (Playwright) adopted verbatim |
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) (MIT) | 6 of 166 skills as references of `scientific-research` (paper-lookup, literature-review, scientific-visualization, scikit-learn, pytorch-lightning, database-lookup) |
| [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) (MIT) | 4 of 6 skills as references of `obsidian` (obsidian-cli, obsidian-markdown, json-canvas, obsidian-bases) |
| [ponytail](https://github.com/DietrichGebert/ponytail) · [caveman](https://github.com/JuliusBrussee/caveman) · [i-have-adhd](https://github.com/ayghri/i-have-adhd) (MIT) | Session-behavior skills adopted (core behavior skill only, where repos are larger ecosystems) |
| [pydantic/skills](https://github.com/pydantic/skills) (MIT) | 10 official skills: `pydantic` core, `pydantic-ai-harness`, 8 framework-migration guides; `building-pydantic-ai-agents` (pre-existing) cross-checked identical to upstream. Logfire skills not adopted |
| [langchain-ai/langchain-skills](https://github.com/langchain-ai/langchain-skills) (MIT) | All 23 official skills adopted verbatim (LangChain, LangGraph, Deep Agents, swarm, evals, ecosystem primer) |
| [obra/superpowers](https://github.com/obra/superpowers) · [mattpocock/skills](https://github.com/mattpocock/skills) (MIT) | Method references merged into `debug`, `testing-strategy`, `write-spec` |

Licences are preserved per skill: Apache-2.0 (cybersecurity sources), MIT
(`management-consulting`), Anthropic `LICENSE.txt` (document/design/tooling skills).
See each skill directory.
