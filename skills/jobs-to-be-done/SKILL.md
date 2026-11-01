---
name: jobs-to-be-done
description: Build an exhaustive Jobs-To-Be-Done (JTBD) catalogue for a platform, then implement end-to-end workflow support so the platform has no gaping feature gaps or missing obvious capabilities. Use when the user asks for a JTBD audit, platform completeness review, capability/feature-gap analysis, workflow readiness, or to ensure the platform covers every job it should. Trigger with "JTBD", "jobs to be done", "feature gaps", "platform completeness", "capability audit", or "workflow readiness".
---

# Jobs To Be Done — Platform Completeness

Don't list screens or features. Identify every job users, admins, external actors, integrations, and system processes need to accomplish, map each to its workflow-system support, then close the gaps — no gaping feature gaps, no missing obvious capabilities.

> **Taxonomy note.** "JTBD" is used here as *platform-capability completeness* (the jobs the platform must support), not strict Christensen JTBD with its emotional/social progress and causal-mechanism analysis. Two layers are kept explicit: **User job** (the progress the user seeks) and **System capability** (the workflow/state-machine that enables it).

## Entry points

Pick one and say which:

- **Catalogue + implement** (default): run Phase 1, then Phase 2.
- **Audit only**: run Phase 1 and stop; do not touch code.
- **Implement only**: `docs/platform-jtbd-catalogue.md` already exists and is current — start at Phase 2.

## Capability disclaimer

Phase 2 assumes the agent can read, write, and execute code. If it cannot (no tool access, read-only repo, no test runner), deliver Phase 2 as a **detailed implementation plan a human can follow**, and say so explicitly.

## Cross-cutting invariants

- **Stable IDs** — `JTBD-XXX` never renumbers. Re-running appends IDs and updates status/evidence in place; never rewrite the whole catalogue.
- **State persistence** — `docs/jtbd-workflow-implementation-plan.md` and the catalogue are the source of truth. **Read them at the start of every turn/session; update them at each slice boundary.** Never rely on conversational history to know what is done or what is next.
- **Deterministic evidence** — a `Live`/`Partial` claim needs a verifiable signal, not prose impression. Two levels, clearly labelled:
  - **Runtime**: an executed test (`pytest`/`jest`/…) — cite `test path:test_name`.
  - **Structural**: a deterministic source signal — route registration, decorator, state-machine definition, migration — found via grep/AST.
  - Never claim live behavior without one of the above.
- **Repository discipline** — modify files and create migrations freely, but do **not** `git commit`/`push` unless explicitly asked.
- **Authority model** — each mutation names its permitted actors (role, ownership, scoped permission). Contextual access ("only the assigned adjuster") is modeled explicitly; admin/break-glass overrides leave an audit trail with a reason code.

---

## Phase 1 — Build the JTBD catalogue

Write the result to `docs/platform-jtbd-catalogue.md`.

### Step 0 — confirm scope and actors

Confirm (or state assumptions for): scope (whole platform vs a single domain), and the actor set — internal users, external users/portal participants, administrators, auditors, support operators, automated jobs, integrations. List domains once and reuse them as the `Domain` column.

### Step 1 — investigate iteratively (bounded context)

Do not try to hold the whole codebase in mind. Work in passes and **write findings to disk as you go**:

1. **Topology map** — generate a directory tree + dependency graph; identify domain boundaries. Record the domain list and actor list at the top of the catalogue.
2. **Process one domain at a time.** For each domain, in order: (a) **data layer** — models/migrations; (b) **API layer** — routes/controllers; (c) **logic layer** — state machines, workflows, gates, approvals. Write that domain's findings into the catalogue immediately, then move on — do not carry prior-domain detail in working memory.
3. **Cross-cutting pass** — RBAC/authorization, notifications, audit, background jobs, integrations, feature flags — inspected once across all domains.

### Step 2 — assign status (deterministic)

| Status | Verification requirement |
|---|---|
| `Live` | Test suite passes, or a deterministic structural signal (route registration, decorator, state-machine definition) confirms it — not prose reading alone. |
| `Partial` | Code exists but fails integration tests, or the structure reveals missing transitions/gates/escalation. |
| `Planned` | Documented in PRD/specs/tests; no implementation found via grep/AST. |
| `Implied` | Absent in code and docs; logically required for data integrity or domain coherence. |
| `Strategic` | Future ecosystem / long-term capability. |
| `Missing` | Absent; no logical requirement or documentation found. |

Decision tree when the matrix is ambiguous:

```
Code present?
├─ Yes → full end-to-end workflow coverage?
│   ├─ Yes → Live
│   └─ No  → Partial
└─ No → documented?
    ├─ Yes → Planned
    └─ No → logically required for correct output?
        ├─ Yes → Implied
        └─ No  → Missing
```

### Step 3 — assign priority and type

**Priority** (urgency) and **Type** (classification) are orthogonal — a strategic item can be P0.

- **P0** control/correctness: `Missing`/`Implied`/`Partial` whose absence causes wrong state, money loss, non-compliance, security exposure, or blocks core operations. **P1** operational completeness: can't complete the job end-to-end. **P2** efficiency/ergonomics: works but slow/manual/clunky.
- **Type** — `Core`, `Supporting`, `Enhancement`, `Strategic`, or `Research`.

| Condition | Priority |
|---|---|
| Missing/Implied + critical path | P0 |
| Partial + blocked workflow | P0 |
| Missing/Implied + high frequency | P1 |
| Partial + clunky but works | P2 |
| Strategic + low urgency | P2 (Type=Strategic) |

### Step 4 — write the JTBD table

| ID | Domain | Actor | User job (desired progress) | Trigger | Desired outcome | System capability (workflow) | Current status | Evidence | Gap | Type | Priority |
|---|---|---|---|---|---|---|---|---|---|---|---|

Rules:
- **Name the progress, not the screen.** `User job` = the progress the user seeks ("verify fraud and escalate with evidence"), never a feature name ("Orders page").
- `Trigger` starts the job; `Desired outcome` proves it done.
- `System capability` = the workflow/state-machine that enables the job; `Gap` = what's missing or broken. Fold external dependencies and failure/rollback concerns into `Gap`.
- `Evidence` = a `file:line`, route, module, test, or workflow name, labelled `runtime` or `structural`.

Domain-neutral example:

> `JTBD-017 | Orders | Support agent | Verify a flagged order for fraud and escalate it with evidence attached | Fraud score exceeds threshold | Order cleared, escalated with evidence, or cancelled with reason | Escalation workflow with evidence gates + task projection | Partial | routes/orders.py:45 (flagging); no escalation workflow | Escalation + evidence handling missing; no task projection | Core | P0`

### Step 5 — follow-on sections

- **`## Workflow Readiness Assessment`** — per major domain: existing vs missing — lifecycle states, transitions, gates, tasks/assignments, task projections, SLA/escalation, notifications, audit evidence, and error-path coverage.
- **`## First-Class Workflow Candidates`** — a **first-class workflow** is a job sequence with ≥3 distinct states, ≥2 actors, explicit gates/approvals, compliance/audit requirements, or high frequency/risk. Table: `| Candidate workflow | Source JTBD IDs | Subject | Why first-class | Initial states | Terminal states | Key gates | Type | Priority |`.
- Candidate sections for **Operational Task**, **Checklist / Evidence Gate**, **Admin Rule / Configuration**, **Notification / Escalation**, **Background Job**, and **External Portal Workflow**.
- **`## Gaps, Overlaps, And Duplications`** — docs-vs-code gaps; duplicate concepts; UI-without-backend; backend-without-UI; workflows without task projection; tasks without lifecycle state; notifications without action targets; audit events missing reason/evidence; domain statuses that should normalize into workflow states.
- **`## Recommended Workflow Expansion Roadmap`** — grouped `P0: Control and correctness`, `P1: Operational completeness`, `P2: Efficiency and ergonomics`, `Strategic: Ecosystem expansion`. Per item: JTBD IDs, why it matters, implementation shape, dependencies, acceptance criteria.
- **`## Definition Of Done For A Workflow-Backed JTBD`** — tiered (see Phase 2); include explicit **failure handling** (retry, dead-letter, rollback, user-visible error states) and **reversal/reopen** for terminal states where appropriate.

### Step 6 — discovery protocol

If deeper inspection contradicts an earlier status, or you hit a blocker: update the affected JTBD immediately; add a `## Discovery Notes` section; flag architectural blockers that would prevent a P0/P1 implementation; surface P0-critical blockers in the final response, not buried in the document.

### Step 7 — verify

Confirm the file exists with the expected sections and stable IDs; run markdown linting if present; record the main sources inspected; never claim live behavior without a runtime or structural signal.

### Phase 1 final response

File created; number of JTBD identified; highest-priority workflow candidates; caveats (runtime vs structural evidence, scope assumptions, any P0 blockers discovered).

---

## Phase 2 — Implement from the catalogue

Use the catalogue as source of truth and extend backend + frontend so the workflow system fully supports the identified JTBD. **Not** a documentation-only task. Order: P0 → P1 → P2 → Strategic (where feasible).

### Targeted execution loop

Do not read the whole catalogue into context. Loop:

1. Read the tracker's progress summary + per-JTBD status; pick the next uncompleted P0/P1 slice.
2. Read **only** that JTBD's definition and its immediate domain context from the catalogue.
3. Execute the slice — backend → frontend → tests.
4. Run the slice's specific test suite (changed files + dependencies).
5. Update the tracker and the catalogue's status/evidence for that JTBD.
6. Repeat.

Create/update `docs/jtbd-workflow-implementation-plan.md` with a progress summary up top:

```
## Progress Summary
| Priority | Total | Done | In progress | Blocked | Not started |
|----------|-------|------|-------------|---------|-------------|
| P0 | … | … | … | … | … |
```

…followed by the per-JTBD tracker: JTBD ID, current support, backend changes, frontend changes, data-model/migration changes, workflow/task/notification/audit changes, tests required, status.

### Vertical slice scope

One slice = one complete user story (backend model → API → UI), sized for a single sitting (≤5 files changed or ≤3 new UI screens). Break larger JTBDs into `-a`, `-b` sub-slices tracked in the plan.

### Per-JTBD deliverable

- **Backend** — canonical subject/model; workflow definition or extension; legal transitions, terminal states, pause/resume, reason codes; checklist/evidence gates; server-side authority; operational task projection; SLA/breach/escalation/notification; audit events (actor, reason, subject, before/after, evidence links); API routes/services/views using existing patterns; background workers where async; migrations + seed/demo data.
  - **SLA** — per state: `sla_target`, `sla_unit`, `sla_start`, `sla_escalation_policy`, `pause_reasons`.
  - **Migrations** — `up`/`down` for safe reversal; a defined strategy for existing records (defaults, backfill, temporary state); tested against a representative sample.
- **Frontend** — workflow-aware UI (state, owner, blocker, deadline, next action, history); actions driven by backend capability/permission/gate checks; forms/dialogs for reasons, waivers, approvals, evidence; queue/task integration; notification deep links / quick actions; admin controls; empty/loading/error/unauthorized/blocked states.
- **Fixtures** — seed data exercising ≥1 happy path and ≥1 edge case per workflow, so QA works without production data.
- **Testing** — tiered: **P0** unit tests for all new business logic + 1 integration test per endpoint + 1 e2e per workflow; **P1** integration + happy-path e2e; **P2** unit tests for core changes. If the full suite is too large, run changed files + dependencies and record what was skipped.

### Safety, rollback & acceptance

- Reuse existing patterns/modules before adding abstractions; no new dependencies unless clearly necessary; no placeholder UI or stub routes presented as complete.
- **Rollback** — prefer feature-flag-driven changes; atomic `up`/`down` migrations; record a rollback plan (what to revert first, what data needs manual cleanup); test the rollback before deploy.
- Preserve existing behavior and tests unless intentionally superseded by a documented workflow change.
- A slice is "done" only when it meets its **DoD tier**; update the tracker/catalogue **after** each slice, never ahead of it.

### Definition of Done tiers

- **MVP DoD** (P0/P1 baseline) — model, states, API, basic UI, happy-path test, audit log.
- **Standard DoD** (default) — MVP + task projection, notifications, authority enforcement, migration (up/down).
- **Comprehensive DoD** (critical financial/compliance) — Standard + SLA/escalation/rollback, comprehensive tests, UI edge states.

Aim for Standard; P0 must reach Standard; critical financial/compliance workflows must reach Comprehensive.

### Implementation priority

Derive the P0/P1/P2 split from the catalogue roadmap. Shape reference (example — substitute your own domain):

- **P0**: normalize application-to-policy lifecycle; expand claim determination; reusable missing-information request workflow; first-class reinsurance concurrence; high-risk admin change workflow; finance exception workflow; ensure task projection, SLA, notifications, audit for each.
- **P1**: broker acceptance; specialist review; policy obligation lifecycle; migration exception; notification quick actions.
- **P2**: command-palette actions; AI provenance; story-mode audit per lifecycle.

### Phase 2 final response

Implemented JTBD IDs; changed backend files, frontend files, migrations, docs; tests run + results; remaining JTBD by priority and risk; known gaps / deferred strategic work.
