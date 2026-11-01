---
name: skill-authoring-and-agent-tooling
description: >-
  Build, test, wire, and debug Claude itself: author new skills and rewrite
  weak ones, run skill evals against a baseline with a review viewer, tune a
  skill description until it triggers, package and validate a skill, share it
  with the team on Slack, scaffold MCP servers with typed tool schemas,
  transports and evaluation harnesses, connect Claude to external apps such as
  Gmail, Slack, GitHub and Notion, and fetch LangSmith traces when an agent
  misbehaves at runtime. Use when the user says "create a skill for this",
  "improve this SKILL.md", "why doesn't my skill trigger", "run evals on this
  skill", "package this skill", "build an MCP server", "add a tool to my agent",
  "connect Claude to Gmail/Slack/GitHub", "share this skill with my team",
  "debug my agent", "why did it call the wrong tool", "fetch my LangSmith
  traces", or asks Claude API/SDK questions while wiring an agent. Do not use
  for business, market or user research briefs (see
  research-and-insight-analysis), prose or document content (see
  writing-and-internal-communications), or building web apps and artifacts (see
  web-artifact-and-app-building).
---

# Skill Authoring and Agent Tooling

Everything here sits on one spine: **author the capability → test it → wire it
into an agent → debug it at runtime.** The same discipline runs through all
four: a skill, an MCP server, a connected app, and a traced agent run are all
just capabilities that either do the job on a prompt the author never saw, or
do not.

Two failure modes cause almost every wasted iteration. The first is a skill
that only works on the examples it was written against — the author's own test
prompts pass, everything else fails. The second is a description that never
fires, so the perfectly good body is never read. Build against the first, and
measure the second.

## When to use

- Turning a workflow the user just demonstrated into a reusable skill
- Repairing an existing `SKILL.md`: bad description, bloated body, missing pointers
- Running evals — with-skill vs. baseline — and reading the results with the user
- Diagnosing triggering: the skill exists but Claude never loads it
- Building an MCP server, or adding/renaming tools on an existing one
- Connecting Claude to an external app so it takes real actions instead of drafting text
- Validating, packaging, and distributing a skill, or announcing it on Slack
- Debugging a running agent from its traces: wrong tool, silent failure, token blow-up
- Wiring agent code to the Claude API/SDK and needing the current binding shapes

**Do not use for** — `research-and-insight-analysis` when the deliverable is a
business, market, or behavioral brief about something outside Claude;
`writing-and-internal-communications` when the deliverable is the prose or the
document itself rather than the machinery that produces it;
`web-artifact-and-app-building` when the ask is a working web app, dashboard, or
front-end artifact; `file-media-and-engagement-tools` when the user just wants a
GIF, a video, a cleaned-up folder, or a rewritten tweet — those are end products,
not capabilities to install into an agent.

## Workflow

1. **Capture intent and fix the contract.** Extract what already exists in the
   conversation — the tools used, the step order, the corrections the user made,
   the observed input/output formats — then close the gaps with questions: what
   should the skill enable, when should it trigger (which phrasings), what does
   the output look like, and should it be tested? Test cases pay off when the
   output is objectively verifiable (file transforms, extraction, fixed
   workflows); subjective outputs (voice, design) are judged qualitatively.
   Output: a one-paragraph contract with trigger phrases and an output shape.

2. **Plan the bundled resources before writing prose.** Re-read each example and
   ask what would be reused on the tenth run: a script (same code rewritten
   every time), a reference doc (schemas, policies, API detail loaded on
   demand), or an asset (templates, fonts, boilerplate that ships in the
   output). Anything in `scripts/` must be runnable without loading into
   context; anything in `references/` must be pointed at from `SKILL.md` with a
   stated moment to open it. Output: an inventory of the three directories,
   including "none of them" if the skill is pure guidance.

3. **Scaffold and write the `SKILL.md`.** Run
   `python scripts/skill_creator/init_skill.py <skill-name> --path <dir>` and
   delete the example files you do not need. Frontmatter carries the routing:
   `name` equals the directory, and `description` says both *what* it does and
   *when* to use it — write it slightly pushy, because models under-trigger, and
   keep every "when to use" signal in the description rather than the body.
   Body: imperative instructions that explain *why*, not a stack of ALL-CAPS
   MUSTs; an explicit output template where a document is produced; under ~500
   lines with pointers to `references/` beyond that; and nothing that would
   surprise the user if the skill were described accurately — no malware, no
   exploit code, no deceptive instructions.

4. **Choose and build the tool surface.** Reach for the lightest thing that
   works:

   | Need | Build | Detail |
   |---|---|---|
   | Deterministic/repetitive step | Bundled script in `scripts/` | Runs without loading context |
   | Agent needs typed operations on an API | MCP server | [mcp_best_practices.md](references/mcp_best_practices.md), [python_mcp_server.md](references/python_mcp_server.md), [node_mcp_server.md](references/node_mcp_server.md) |
   | Agent must act in Gmail/Slack/GitHub/Notion… | App connection (Composio Tool Router) | see below |

   For an MCP server: research the protocol and the target API first, then
   implement shared infrastructure (auth client, pagination, formatting, error
   helpers) before tools. Each tool gets a Zod/Pydantic input schema with
   constraints and examples, an `outputSchema` with `structuredContent` where the
   SDK supports it, an action-oriented name with a consistent prefix, annotations
   (`readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`), and
   error messages that tell the agent what to try next. Cap response size
   (~25,000 characters) and truncate with a message that says how to page. Test
   with `npx @modelcontextprotocol/inspector` or `python -m py_compile` — never
   by running a stdio server in the foreground, which hangs. Then write 10
   independent, read-only, complex, verifiable QA pairs in the XML format in
   [mcp_evaluation.md](references/mcp_evaluation.md) and run
   `scripts/mcp-builder/evaluation.py`. For an app connection: install the
   plugin, run setup with the API key, authorize once via OAuth, then be
   specific in requests ("Slack #general", not "send a message") — the Tool
   Router picks the action, OAuth is handled automatically, and the action
   executes. Output: a working tool surface plus its evaluation file.

5. **Run test cases with a baseline, in the same turn.** Save 2-3 realistic
   prompts — phrased the way a real user types them, file paths and typos and
   backstory included — to `evals/evals.json` (prompt only; assertions come
   next). Spawn every run at once: one subagent per case *with* the skill, and a
   baseline *without* it (or against a pre-edit snapshot when improving an
   existing skill), writing to
   `<skill>-workspace/iteration-<N>/eval-<name>/{with_skill,without_skill}/outputs/`.
   Capture `total_tokens` and `duration_ms` from each completion notification
   into `timing.json` immediately — that data exists nowhere else. While runs
   execute, draft objectively verifiable assertions with descriptive names and
   explain them to the user; leave subjective qualities to human review.
   Output: completed runs, `eval_metadata.json` per case, and assertions.

6. **Grade, aggregate, and get it in front of the human.** Grade each run —
   reading [references/agents/grader.md](references/agents/grader.md) — saving
   `grading.json` with exactly `text`, `passed`, `evidence` per expectation
   (the viewer depends on those field names); script anything checkable rather
   than eyeballing it. Aggregate with
   `python -m scripts.skill_creator.aggregate_benchmark <workspace>/iteration-N --skill-name <name>`,
   then do an analyst pass per [references/agents/analyzer.md](references/agents/analyzer.md)
   for non-discriminating assertions, flaky high-variance cases, and time/token
   tradeoffs. Launch the viewer with
   `python eval-viewer/generate_review.py <workspace>/iteration-N --skill-name <name> --benchmark <workspace>/iteration-N/benchmark.json`
   (add `--previous-workspace` from iteration 2; add `--static <path>` when there
   is no browser — feedback then downloads as `feedback.json`, which you copy
   back into the workspace). Generate this *before* judging outputs yourself.
   Output: a viewer the user reviews, then `feedback.json`.

7. **Iterate, package, share.** Read the feedback and generalize from it — a fix
   that only works on the three test prompts is a liability; prefer a different
   metaphor or working pattern over an overfitted rule, remove anything not
   pulling its weight, and explain the *why* behind every instruction. Look for
   repeated helper scripts across runs and bundle the winner into `scripts/`.
   Re-run the whole set into `iteration-<N+1>/` until feedback is empty or
   progress stops. Then validate and package with
   `python -m scripts.skill_creator.package_skill <path/to/skill>` (emits a
   `.skill` file; fix any validation errors before it will write). To announce
   it, post name, description, and link to the team's Slack channel using the
   Slack send/post-message tools. Output: a validated `.skill` file and a team
   announcement.

8. **Tune the description until it triggers.** Generate ~20 realistic query
   strings — 8-10 should-trigger (varied phrasings of one intent, including
   cases that never name the skill) and 8-10 should-not-trigger *near-misses*
   that share keywords but need a different skill. Obviously irrelevant
   negatives test nothing. Review them with the user through
   [assets/eval_review.html](assets/eval_review.html) (fill the three
   placeholders, open it, then read `~/Downloads/eval_set.json` after they click
   Export). Run `python -m scripts.skill_creator.run_loop --eval-set <json>
   --skill-path <path> --model <current-model-id> --max-iterations 5 --verbose`
   in the background; it splits 60/40 train/test, scores each query three times,
   and returns `best_description` chosen on the held-out test set. Apply it and
   show before/after with the scores. Note that trivial one-step prompts do not
   trigger skills regardless of description quality — the eval queries must be
   substantive enough to be worth consulting a skill for.

9. **Debug the running agent from its traces.** When the installed capability
   misbehaves, stop guessing: fetch the evidence with `langsmith-fetch`
   (requires `pip install langsmith-fetch` plus `LANGSMITH_API_KEY` and
   `LANGSMITH_PROJECT`). Start with
   `langsmith-fetch traces --last-n-minutes 5 --limit 5 --format pretty`, report
   trace count, errors, tools called, duration, and tokens, then drill into the
   failing trace with `langsmith-fetch trace <id> --format json` to reconstruct
   the goal, the ordered tool calls, the exact failure point, the root cause,
   and a concrete fix. Full command reference, error-scanning patterns, and
   troubleshooting in [references/agent-trace-debugging.md](references/agent-trace-debugging.md).

## Quality bar

- [ ] Frontmatter `name` equals the directory name; `description` states both what and when, and contains the phrasings a user would actually type
- [ ] Every "when to use" signal lives in the description, not buried in the body
- [ ] SKILL.md stays under ~500 lines; anything longer is split into a `references/` file that is explicitly pointed to, with a stated moment to open it
- [ ] Instructions explain the reason behind each action; no unexplained ALL-CAPS MUSTs, and no rule that only holds for the author's examples
- [ ] Bundled scripts run from the skill directory without being loaded into context, and are referenced by explicit relative path
- [ ] MCP tools have typed input schemas with constraints/examples, a documented output schema, accurate annotations, size caps, and errors that name the next action
- [ ] Test runs include a baseline spawned in the same turn, timing captured from notifications, and assertions that are objectively checkable with descriptive names
- [ ] `grading.json` uses `text` / `passed` / `evidence`, and the review viewer was generated before any self-assessment of the outputs
- [ ] Description was measured against realistic hard negatives, not trivially irrelevant prompts
- [ ] Nothing in the skill would surprise the user if the skill were described accurately: no malware, no exploit code, no deceptive instructions
- [ ] Packaging validation passes before the `.skill` file is handed over

## Reference map

| Situation | Open |
|---|---|
| Full eval JSON schemas (`evals.json`, `grading.json`, `benchmark.json`) | [schemas.md](references/schemas.md) |
| Grading assertions against run outputs | [agents/grader.md](references/agents/grader.md) |
| Blind A/B comparison of two skill versions | [agents/comparator.md](references/agents/comparator.md) |
| Why one version beat another; non-discriminating assertions, flakiness | [agents/analyzer.md](references/agents/analyzer.md) |
| MCP server design: naming, response format, pagination, transport, security | [mcp_best_practices.md](references/mcp_best_practices.md) |
| Python/FastMCP server implementation and quality checklist | [python_mcp_server.md](references/python_mcp_server.md) |
| Node/TypeScript server implementation and quality checklist | [node_mcp_server.md](references/node_mcp_server.md) |
| Writing and running the 10-question MCP evaluation harness | [mcp_evaluation.md](references/mcp_evaluation.md) |
| Agent trace debugging: `langsmith-fetch` commands, error scans, troubleshooting | [agent-trace-debugging.md](references/agent-trace-debugging.md) |
| Claude API/SDK: language detection, current model/param shapes, per-language docs | [claude-api/README.md](references/claude-api/README.md) |
| Trigger-review page for a draft eval set | [assets/eval_review.html](assets/eval_review.html) |

Carried executables: `scripts/skill_creator/` (scaffold, validate, package,
benchmark, description optimizer), `scripts/mcp-builder/` (evaluation harness),
and `eval-viewer/generate_review.py` (human review page).

## Output format

Deliver the capability plus its evidence, in this order:

```markdown
# <Skill or server name>

## What it does and when it fires
One paragraph: the contract, plus the description field verbatim.

## Layout
skill-name/
├── SKILL.md
├── scripts/      # only what a user actually runs
├── references/   # pointed to from SKILL.md, each with an open-when trigger
└── assets/       # files that ship in the output

## Evidence
| Case | Prompt | With skill | Baseline | Assertions passed |
|---|---|---|---|---|

## Triggering
Should-trigger hit rate / should-not-trigger false-positive rate, before and
after, with the applied `best_description`.

## Known gaps
What the test set does not cover, and the next case to add.
```

For an MCP server, substitute the tool table (`name | purpose | input schema |
annotations`) and the evaluation result (questions passed / total) for the
evidence table.

## Finding official Claude learning material

When the ask is *how do I learn or teach* Claude rather than *build* something,
answer the question first, then offer at most one recommendation. Fetch
`https://academy.claude.com/assets/data/catalog.json` once per conversation and
recommend only from items it contains, copying item URLs verbatim under
`https://academy.claude.com/`. Strong match means intent, not topic: "how do
skills work?" qualifies; "help me finish this file" does not. If the catalog
cannot be fetched or its `staleAfter` has passed, name no items — link the
product hubs (claude, code, cowork, fluency, platform) or
`https://academy.claude.com/resources` instead, and stay silent about the
failure. Never invent a title, slug, or URL.
