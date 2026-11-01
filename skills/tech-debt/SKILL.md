---
name: tech-debt
description: Identify, categorize, prioritize, audit, and remediate technical debt. Use when the user asks about tech debt, code health, what to refactor, or the maintenance backlog, or to remove/fix debt — cleaning code smells, eliminating TODOs and placeholders, enforcing type safety and error handling, or improving test coverage, security, or performance. Every run writes a persistent report under docs/audit/.
---


# Tech Debt

Find and reduce code-level technical debt pragmatically. Detection uses the catalog below; prioritization scores what to fix first; every run writes a persistent report under `docs/audit/`. The realistic goal is **not** to eliminate all debt — that is impossible and often economically irrational. The goal is to **eliminate all P0 and high-scoring P1 debt**, document everything else, and hand the user a clear, prioritized roadmap for the remainder.

## Debt Categories

| Type | Examples | Risk |
|------|----------|------|
| **Code debt** | Duplicated logic, poor abstractions, magic numbers | Bugs, slow development |
| **Architecture debt** | Monolith that should be split, wrong data store | Scaling limits |
| **Test debt** | Low coverage, flaky tests, missing integration tests | Regressions ship |
| **Dependency debt** | Outdated libraries, unmaintained dependencies | Security vulns |
| **Documentation debt** | Missing runbooks, outdated READMEs, tribal knowledge | Onboarding pain |
| **Infrastructure debt** | Manual deploys, no monitoring, no IaC | Incidents, slow recovery |

## Modes

- **Audit** (default): read-only. Detect, score, and write the report. Do not modify code.
- **Remediate**: fix findings in priority order, then update the report.

**Mode decision rule:** "find", "audit", "list", or "detect" → **Audit**. "fix", "remove", "remediate", or "refactor" → **Remediate**. Ambiguous ("handle tech debt") → ask.

## Workflow

1. **Determine scope** — whole repo, a module/package, or a targeted concern (types, tests, security, performance). If unsure, ask.
2. **Detect** — sweep the scope against the catalog. Prefer structural search (`rg`/grep/AST over files) and targeted reads; note `file:line` for every finding.
3. **Score & prioritize** — assign severity, impact, risk, effort (see framework), and decide fix-now vs defer.
4. **Write the report** — update `docs/audit/tech-debt.md` in the project root (see output contract).
5. **Remediate (if requested)** — fix in priority order. Run checks scaled to the change (see remediation standard).
6. **Close out** — mark resolved items `fixed`, note deferred items with a tracking reference, add a change-log entry, summarize.

## Output contract — `docs/audit/tech-debt.md`

Use a **single persistent master file**: `docs/audit/tech-debt.md` (project root = git worktree root, or cwd if not a repo; create the dir if missing).

- Each run **appends** a `## Audit Run YYYY-MM-DD` section; never overwrite the file.
- Findings fixed in a run are marked `fixed(<date>)`; findings that persist stay `open`; deferred items get a tracking reference.
- A run that finds nothing still writes a run section stating the scope was clean.

Finding fields:

| Field | Meaning |
|---|---|
| `severity` | `P0` (correctness/security/data-loss) · `P1` (high-risk maintainability) · `P2` (medium) · `P3` (cosmetic) |
| `category` | catalog section name |
| `location` | `file:line` or a precise module/component reference |
| `finding` | concrete description |
| `recommendation` | specific fix |
| `effort` | `S` (<2h) · `M` (3–8h) · `L` (>8h) |
| `status` | `open` · `fixed(<date>)` · `deferred(<ref>)` |
| `confidence` | `High` · `Medium` · `Low` — see legend below |
| `evidence` | `file:line` (static), `test:...` (tests), or `profile:...`/`lighthouse:...` (runtime) |

Confidence legend:

- **High** — statically verified in source (grep/AST) or captured from a deterministic test failure (e.g. a `pytest` run showing flakiness).
- **Medium** — captured from runtime analysis (Lighthouse, profiler, APM) that may vary by environment.
- **Low** — inferred heuristically (e.g. guessing a UI is inaccessible from missing `aria-*` attributes without screen-reader testing).

Also include:

- **`## Heatmap (Debt Density)`** — `| Module/Domain | Total | P0 | P1 | P2 | P3 | Density |`. If `cloc` is unavailable, approximate density as findings ÷ file count and label the column `Density (approx findings/file)`; skip density for repos under ~10k lines.
- **`## Remediation Plan`** — findings in priority order, split fix-now vs defer.
- **`## Change Log`** — one line per run: date, mode, summary, items fixed/deferred.
- **`## Manual Review Queue`** — items deferred with no tracking system, using `deferred(manual-<date>)`.

## Prioritization framework

**Severity first:**

- **P0** — correctness bugs, security vulnerabilities, data loss, broken builds. Fix now.
- **P1** — untestable/brittle core logic, unsafe types on critical paths, missing error handling on money/auth paths.
- **P2** — duplicated logic, magic numbers, dead code, inconsistent naming, slow-but-tolerable spots.
- **P3** — cosmetic, stylistic, stable and harmless.

**Score** within a severity band: `Score = Impact × Risk` (1–25).

**Sort order:** (1) Severity (P0 → P3), (2) `Impact × Risk` descending, (3) Effort ascending (S before M before L).

Calibration:

| Rating | Impact (business/functional) | Risk (future maintenance cost) |
|---|---|---|
| 1 | Cosmetic, no user impact | Isolated, easily understood |
| 2 | Minor annoyance for power users | Localized to one module |
| 3 | Blocks a non-critical workflow | Affects 2–3 modules, moderate churn |
| 4 | Blocks a critical workflow, data corruption possible | Affects many modules, frequent changes |
| 5 | Data loss, security breach, or revenue loss | Core architecture, extremely brittle |

**Fix now vs defer:**

- **Audit mode** — all findings stay `open`; the remediation plan recommends running Remediate mode.
- **Remediate mode** — fix P0 and high-scoring P1. For the rest, use the repo's cost model (a P2 nobody touches can defer; a P2 on a hot path cannot). Never silently drop a finding — defer it with a reference.

**"Core logic" (for test-coverage debt)** — public APIs and entry points; business-critical computations (pricing, tax, eligibility); security-critical flows (auth, authorization, payment); error/exception paths that could cause data loss. Missing tests on core logic = P1; missing tests on trivial getters/setters = P3 or not debt.

## Remediation standard (practical)

**Regression safety over purity** — never change behavior while cleaning up. Scale verification to the change:

- **Trivial changes** (magic numbers, typos, naming, dead-code removal): lint + typecheck only.
- **Structural changes** (refactors, module replacement, behavior changes): full tests + lint + typecheck + build.

Note in the change log which checks ran and which were skipped.

- **Type safety** — eliminate `any`/untyped on critical paths; elsewhere convert what is cheap and safe. A truly unavoidable suppression gets a one-line reason and a `P2`/`P3` finding, never a silent cast.
- **Error handling** — replace swallowed/`console.log` paths with structured logging and explicit errors on user, API, and edge-case flows.
- **TODOs & placeholders** — resolve by implementing, or relocate to the project tracker and reference it. Deleting a TODO without implementing *and* tracking it is not allowed.
- **Dead code** — remove when confidently unreferenced; verify with grep first.
- **Tests** — cover critical paths and any code you change; target meaningful coverage of core logic, not a number.
- **Security** — fix OWASP-class issues immediately; add validation/encryption/access control where the flow demands it.
- **Performance** — optimize only with evidence (a profile, LCP/INP/CLS, a slow query); document before/after numbers.
- **Documentation** — keep existing docs accurate; add missing ones only where the user cares.

## Detection catalog

Some items need runtime tooling to **detect** (Lighthouse for LCP/CLS/INP, a profiler for memory leaks, a browser for UX/accessibility) even though their **fix** is code. Mark such findings `confidence: Medium`/`Low` and cite the tool. Static findings (grep/AST) are `confidence: High`.

**Runtime UX/Performance detection** — do **not** run Lighthouse/browser automation unless a `package.json` script exists (e.g. `npm run lighthouse`). If none exists, mark these findings `deferred(manual-ux-audit)` with `confidence: Low`. Static accessibility can still be detected via `eslint-plugin-jsx-a11y` or `@axe-core/cli` if installed — prefer those.

**Quick-win categories** (highest ROI, lowest effort): `as any` type assertions (P1/P2); magic numbers (P2/P3); commented-out code (P2/P3); hardcoded secrets (P0).

### Code Quality & Design

1. **Long Methods/Functions** — spans many lines, does multiple things.
2. **Large Classes/Components** — excessive properties, methods, responsibilities.
3. **Deep Nested Conditionals** — excessive `if/else`/`switch`, nested 3+ levels.
4. **Magic Numbers & Strings** — hard-coded values without named constants.
5. **Inconsistent Naming** — e.g. `fetchUser` vs `getUserData`.
6. **Excessive Comments** — comments explaining *what*, not *why*.
7. **Commented-Out Code** — dead code left "just in case."
8. **Code Duplication / DRY Violations** — copy-pasted logic repeated across files.
9. **High Cyclomatic Complexity** — many branching paths.
10. **Feature Envy** — a function more interested in another module's data.
11. **Shotgun Surgery** — one change touches many unrelated files.

### Architecture & Structure

1. **Tight Coupling** — modules dependent on each other's internals.
2. **Circular Dependencies** — A imports B and B imports A.
3. **Weak/Leaky Abstractions** — exposing internals or forcing special cases.
4. **Premature Optimization** — complexity before a proven bottleneck.
5. **SOLID Violations** — especially SRP and Dependency Inversion.
6. **Inconsistent Architectural Patterns** — mixing state/data/design patterns.
7. **Spaghetti Code** — hard-to-follow control flow.
8. **Over-Engineering ("Speculative Generalization")** — abstractions "for the future."
9. **"Not Invented Here"** — custom builds where standard libraries suffice.

### Concurrency & Async

1. **Race Conditions & Data Races** — shared mutable state without synchronization.
2. **Unhandled Async Failures** — unhandled promise rejections, missing `.catch()`/`try/catch`.
3. **Deadlocks** — no timeout on lock/acquisition.
4. **Fire-and-Forget Correctness** — background jobs with no success/failure monitoring.

### Dependencies & Integration

1. **Brittle Integrations** — no fault tolerance, mocking, or graceful degradation.
2. **Outdated Dependencies** — deprecated versions with known issues.
3. **Vendor Lock-in Code** — intertwined with a specific SDK/API structure.
4. **Fragile Global State** — overuse of globals, singletons, ambient context.
5. **Missing Resilience Patterns** — no timeouts, retries/backoff, circuit breakers, idempotency.
6. **License & Provenance Debt** — OSS license non-compliance, no SBOM, unpinned transitive deps.

### API Design

1. **API Design Debt** — no versioning/deprecation policy, inconsistent error contracts, missing pagination/idempotency/rate limiting.

### Data & Persistence

1. **N+1 Queries / Missing Indexes** — query-performance debt.
2. **Schema/Migration Debt** — migration drift, non-reversible migrations, missing referential integrity. Non-reversible migrations → P0/high P1; missing indexes → P2 (P1 on a critical query); drift → P1.

### Data & Type Safety

1. **Inconsistent Data Models** — same concept (e.g. "User") with different shapes.
2. **Type Assertions (`as any`)** — bypassing the type system.
3. **Poor Error Handling** — silent failures or generic top-level `try/catch`.
4. **Time & Currency Handling** — timezone/DST bugs, float-for-money, unit ambiguity.

### Testing & Maintainability

1. **Untestable Code** — side effects, unclear I/O, direct dependency instantiation.
2. **Brittle Tests** — fail on unrelated changes (implementation, not behavior).
3. **Missing Tests for Core Logic** — unverified business-critical paths.
4. **"Test-Only" Code Paths** — logic/mocks existing only to make testing possible.

### AI/ML & Data Science Debt

1. **Hardcoded Prompts / Model Config** — prompts or model parameters hardcoded in source.
2. **Unversioned Feature/Pipeline Logic** — feature extraction unversioned.
3. **Manual Training/Evaluation Pipeline** — not automated.
4. **No Model Monitoring/Retraining** — no drift detection or retraining policy.
5. **Misaligned Evaluation Metrics** — eval metrics not aligned with business outcomes.

### Product & Quality — UX & Interface

1. **Inconsistent UI Patterns** — differing buttons/forms/feedback.
2. **Missing Loading States** — no skeletons/spinners.
3. **Missing Error States** — raw messages or blank screens.
4. **Poor Empty States** — blank areas with no guidance.
5. **Non-Responsive Design** — layout breaks on some sizes/devices.
6. **Inaccessible Components** — no keyboard nav, screen reader, ARIA.
7. **Janky Animations/Transitions** — non-smooth or performance-hitting.
8. **Unvalidated Forms** — invalid submissions or late error display.

### Product & Quality — Performance & Reliability

1. **Slow Page Loads (High LCP)** — main content appears too late.
2. **Layout Shifts (High CLS)** — elements move while loading.
3. **Poor Interaction Response (High INP)** — inputs/buttons feel slow.
4. **No Image Optimization** — no WebP/AVIF, no sizing.
5. **No Caching Strategy** — repeated API calls for static data.
6. **Memory Leaks** — degradation over time without refresh.
7. **No Frontend Error Monitoring** — no runtime error tracking/alerting.

### Product & Quality — Functionality & Completeness

1. **"Coming Soon" Placeholders** — advertised but non-functional.
2. **Partially Implemented Features** — flows that start but can't complete.
3. **Hardcoded Content/Configs** — text/pricing/flags needing a deploy to change.
4. **Lack of i18n** — can't translate UI or handle locales.
5. **No Offline Capability** — fails without network.
6. **Brittle User Flows** — critical paths break on unexpected data.

### Product & Quality — Security & Data

1. **Exposed Sensitive Data** — logs/keys/internal IDs in console or network.
2. **No Input Sanitization** — XSS or injection risk.
3. **Missing Data Validation** — front-end without matching back-end validation.
4. **Insecure Dependencies** — known-vulnerable packages.
5. **Broken Access Control** — IDOR, missing authorization checks, over-privileged roles.
6. **Hardcoded Secrets / Weak Key Management** — keys/tokens in code or config.

### Product & Quality — Analytics & Maintenance

1. **Missing Analytics Instrumentation** — no tracking of key actions/conversions.
2. **No Feature Flagging** — can't roll out/roll back without full deploy.
3. **Deprecated Features Still in Code** — hidden/disabled but not removed.
4. **Lack of User Journey Monitoring** — can't trace a user's path.
5. **Inconsistent Browser Support** — breaks in a major browser without reason.

### Development Process (code-remediable only)

1. **Slow Local Development** — starting app/tests/builds takes minutes.
2. **"It Works on My Machine"** — environment inconsistencies.
3. **Manual Configuration Needed** — undocumented manual setup steps.
4. **No Coding Standards** — inconsistent formatting, no linting/format config.
5. **Missing/Outdated Documentation** — no READMEs, ADRs, or API docs.
6. **Config/Secret Sprawl & Env Parity** — untyped/unvalidated config, secrets without rotation, drift between environments.

### Testing & Quality Assurance (code-remediable only)

1. **Test Suite Takes >10 Minutes** — developers avoid running it.
2. **Flaky Tests** — randomly fail without code changes.
3. **No Test Automation** — manual regression testing.
4. **No Performance Testing** — regressions only caught in production.

### CI/CD & Deployment (code-remediable only)

1. **Manual Deployment Steps** — deployment needs human intervention.
2. **Long CI/CD Pipeline (>30 min)** — slow PR feedback.
3. **No Rollback Strategy** — can't quickly revert a bad deployment.
4. **No Infrastructure as Code** — server configs maintained manually.

### Operations & Observability

1. **Unstructured Logging** — no correlation IDs, missing fields.
2. **Missing Metrics / SLOs** — no business metrics or SLO/SLI definitions.
3. **No Distributed Tracing** — no cross-service tracing.
4. **Noisy/Nonexistent Alerting** — no on-call rotation or alert hygiene.
5. **Neglected Dead-Letter Queues** — DLQ data never inspected or replayed.

## Default detection thresholds

Overridable baselines for structural detection:

| Category | Threshold | Method |
|---|---|---|
| Long function | > 40 lines (excl. blank/comments) | signature grep + line count |
| Deep nesting | > 4 indent levels | `rg '^(\t|\s{4}){5}'` |
| Large file | > 400 lines | `wc -l` |
| Many parameters | > 5 | signature grep |
| Cyclomatic complexity | > 10 | `radon` (Py) / `eslint` (JS) |
| Duplication | > 5 lines duplicated in ≥3 files | `jscpd` / `pmd-cpd` |

Tooling fallback: if a listed tool (`radon`, `eslint`, `jscpd`, `pmd-cpd`, `cloc`) isn't installed, use a heuristic approximation (e.g. count `if`/`case`/`&&`/`||` for complexity), mark the finding `confidence: Low`, or surface it as `deferred(manual-tooling)`.

## Guardrails

- **Regression safety** — run the scaled checks (trivial vs structural) before and after; revert anything that changes output or breaks a check.
- **Verify before deleting** — grep for usages before removing dead code, exports, or dependencies.
- **Small, reviewable changes** — batch fixes into logical, self-contained changes.
- **Repository discipline** — modify files freely. Do **not** `git commit`/push unless (a) the user says "commit" or "create a PR", or (b) the agent was invoked with an explicit `--auto-commit` flag. Otherwise leave the working tree dirty for the user to review and commit.
- **Scope discipline** — stay in the scope set; note out-of-scope findings as `deferred` rather than silently fixing or ignoring.
- **Document what you defer** — every deferred item gets `deferred(<ref>)` (or `deferred(manual-<date>)`), never a mental note.
