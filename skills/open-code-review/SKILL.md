---
name: open-code-review
description: Run AI code review through the Open Code Review CLI (`ocr`, alibaba/open-code-review, Apache-2.0) — a dedicated review agent that reads Git diffs with a tool-use loop and emits structured, line-level findings (severity + category + suggested fix) at ~1/9 the tokens of a general-purpose agent, tuned for precision. Use when the user asks to "run ocr", "open code review", review a PR/commit/branch with the OCR CLI, review with SARIF/JSON output, or wire code review into CI. Configured on this machine against local Ollama (qwen3.6-coding). Do not use for in-session general PR review (see code-review), security-focused vulnerability review (see security-review), or reviewing code that isn't in a Git repo (see code-review).
---

# open-code-review (`ocr` CLI)

[Open Code Review](https://github.com/alibaba/open-code-review) reads Git
diffs, sends changed files to a configurable LLM through a tool-use agent
(can read files, search the codebase, inspect other changed files), and
produces structured review comments with line-level precision. Beyond diff
review, `ocr scan` reviews entire files for auditing unfamiliar codebases.
It favors precision over recall: engineering logic (template-engine rule
matching) keeps the model's attention focused, which is why it scores
higher precision/F1 than general-purpose agents on the same model at ~1/9
the tokens.

## State on this machine

| What | Value |
|---|---|
| CLI | `ocr` = open-code-review 1.12.9 (`brew install open-code-review`, `/opt/homebrew/bin/ocr`) |
| LLM provider | Ollama @ `http://127.0.0.1:11434/v1` (protocol `openai`, api_key placeholder `ollama`), timeout 900 s |
| Model | `qwen3.6-coding` (19 GB, local, verified tool-calling under OCR's prompts) |
| Config file | `~/.opencodereview/` (see `ocr config get` for keys) |
| `macocr` | the other `ocr` (macOCR screen/QR reader, brew `ocr`) is available as `~/.local/bin/macocr` — the `ocr` name was taken by Open Code Review via `brew link --overwrite` |

If `command -v ocr` no longer resolves to open-code-review, the macOCR
formula re-linked over it: `brew link --overwrite open-code-review`.

## Workflow

### 1. Gather business context

Analyze the review target (commits, branch, or changes) and extract concise
business context. Pass it via `--background` to improve review quality.

### 2. Run the review

Run directly (don't pre-probe for the CLI):

```bash
ocr review --audience agent --background "business context here" [user-args]
```

| User says | Command |
|---|---|
| "review my changes" / "review the working copy" | `ocr review --audience agent -b "context"` |
| "review this PR" / feature branch | `ocr review --audience agent -b "context" --from main --to <branch>` |
| "review commit abc123" | `ocr review --audience agent -b "context" --commit abc123` |
| "what would be reviewed?" (dry-run) | `ocr review --preview` |

Flags worth knowing:

- `--background "…"` / `--background-file <path>` — review context (file wins).
- `--output /tmp/ocr_out.txt` — write the full result to a file; **always
  prefer this over piping through `tail`/`head`** (large runs truncate and
  drop earlier comments).
- `--format text|json|sarif` — `sarif` for GitHub Code Scanning and CI
  integrations.
- `--exclude '**/generated/*,**/testdata/*'` — gitignore-style exclusions.
- `--concurrency <n>` — default 8 file workers; lower if rate-limited.
- `--provider <name>` / `--model <name>` — override the configured
  provider/model for this run only (`ocr llm providers` lists built-ins).
- `--timeout` — per-group seconds × review rounds (default 15; medium
  effort = 2 rounds → 30 min).
- `--max-tokens <n>` / `--max-tokens-budget <n>` — per-group prompt ceiling
  / total run budget (skipped files reported as `failed(budget)`).
- `--no-filter` — skip the LLM post-filtering pass (keeps all comments;
  also avoids the extra local-model timeout surface).
- `--resume <id>` — continue an interrupted range/commit review (id printed
  on failure; also `ocr session list`).

### 3. Report

OCR output carries `severity` (critical/high/medium/low) and `category`
(bug/security/performance/maintainability/test/style/documentation/other)
per comment. Present grouped by severity, discarding likely-false-positive
`low` items. Template:

```markdown
## Code Review Results

**Files reviewed**: N
**Issues found**: X critical, Y high, Z medium

### Critical
- **`path/to/file.go:42`** [bug] — description
  > Recommendation: fix
```

Mispositioned comments (`start_line`/`end_line` both 0): read the comment,
open the file, locate the section from context.

### 4. Fix

Only apply fixes when the user asked for "review and fix" (or grants
permission after a review-only run). Focus on critical/high/medium; apply
direct fixes when safe; describe manual ones; verify with the user before
committing.

## Custom review rules

Resolution order: `--rule <path>` → `<repo>/.opencodereview/rule.json` →
`~/.opencodereview/rule.json` → built-in defaults. `merge_system_rule: true`
on an entry keeps both the user and built-in rule:

```json
{ "rules": [
  { "path": "**/*.java", "rule": "All new methods must validate required parameters for null", "merge_system_rule": true },
  { "path": "**/*mapper*.xml", "rule": "Check SQL for injection risks" }
] }
```

Preview which rule applies: `ocr rules check <file>`.

## Local models (Ollama) — what works here

OCR drives the review entirely through **native tool calls**; a model that
narrates tool calls as text can never work, no matter the prompt
(`deepseek-r1` is the canonical failure).

- This machine: **`qwen3.6-coding`** — verified end-to-end (finds planted
  bugs, correct line ranges, structured `tool_calls`).
- **`qwen3.5:4b` fails** under OCR's ~3k-token review prompt even though it
  passes a bare tool-calling curl test: it hallucinates "no code provided"
  and then calls `task_done(state:FAILED)`. Treat sub-~8b models as
  unviable for OCR regardless of tool support.
- 96 GB RAM: `ornith-1.5:35b` (22 GB), `muse-glimmer:30b-mlx` (21 GB),
  `glm-4.7-flash` (18 GB) are viable upgrades — swap with
  `ocr config set custom_providers.ollama.model <name>` and re-test with
  `ocr llm test` + a scratch-diff review.
- Verification, troubleshooting, and the full provider config block:
  `references/ollama-local-models.md`.

## Gotchas

- **Working directory matters** — `ocr review` operates on the Git repo at
  the cwd; `--repo /path` to run from elsewhere.
- Bare `ocr review` includes staged, unstaged, **and untracked** changes.
- Files whose diff alone exceeds ~80% of `MAX_TOKENS` (default 200 000)
  are skipped before the LLM is called.
- Plan phase (extra risk-analysis round) triggers when a group's largest
  changed file hits 50 lines or 2+ files hit 100 combined changed lines —
  expect latency.
- Never `--audience human` — progress UI pollutes agent output.
- Comment language follows the `language` config (default English).
- Per-group failures are isolated: exit 0 if anything succeeded; check
  `warnings` (JSON mode) or stderr for which groups failed.
- On this machine the `ocr` binary name is shared with macOCR — if `ocr`
  suddenly prints "macOCR", re-run `brew link --overwrite open-code-review`
  (and `macocr` still works for the screen reader).

## Troubleshooting

- **`ocr: command not found`** — `brew install open-code-review` (or
  `npm i -g @alibaba-group/open-code-review`).
- **`ocr` prints macOCR usage** — name collision; `brew link --overwrite
  open-code-review`.
- **LLM connection error** — `ocr llm test`; check Ollama is running
  (`brew services info ollama`); re-apply the provider config block in
  `references/ollama-local-models.md`.
- **`No tool calls parsed … Max tool requests reached`** — model lacks
  native tool calling under this prompt; pick a bigger model (see above).
- **Comment filtering times out on local models** — expected on slow
  models; findings are still published. `--no-filter` skips the pass
  entirely; `custom_providers.ollama.timeout_sec` (set to 900 here) raises
  the ceiling.
- **Unknown flag `--output`** — CLI < v1.10.0; upgrade:
  `brew upgrade open-code-review`.

## References

| File | Contents |
|---|---|
| `references/ollama-local-models.md` | Full local-model recipe: provider config block, tool-calling verification, model viability table for this machine, timeout tuning |

Upstream: https://github.com/alibaba/open-code-review (Apache-2.0). Docs:
https://open-codereview.ai (configuration, CLI reference, review rules,
MCP, delegation mode). The workflow in this skill is adapted from the
project's own agent skill (`skills/open-code-review/SKILL.md` in the repo).
