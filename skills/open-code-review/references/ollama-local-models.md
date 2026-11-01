# Open Code Review with local Ollama models

Recipe for running [open-code-review](https://github.com/alibaba/open-code-review)
against a local Ollama server (OpenAI-compatible endpoint).
Docs source: `pages/src/content/docs/en/configuration.md` + `faq.md` in the
repo (Apache-2.0), main 2026-09-28.

## Provider config (this machine, verified)

```bash
ocr config set provider                          ollama
ocr config set custom_providers.ollama.url       http://127.0.0.1:11434/v1
ocr config set custom_providers.ollama.protocol  openai
ocr config set custom_providers.ollama.model     qwen3.6-coding
ocr config set custom_providers.ollama.api_key   ollama          # required non-empty; Ollama ignores it
ocr config set custom_providers.ollama.timeout_sec 900           # local models are slow; default 300
```

`url` may be the API base or a full endpoint — OCR normalizes either way.
Verify with `ocr llm test` (prints source URL/model and a live reply).

## Hard requirement: native tool calling

OCR drives the entire review through tool calls (context tools +
`task_done` with findings). A model that narrates tool calls in text
(including inside thinking blocks) can never work — prompt tuning does not
help. `deepseek-r1` is the canonical failure.

Verify any candidate directly, without OCR in the loop:

```bash
curl http://127.0.0.1:11434/v1/chat/completions -H "Content-Type: application/json" -d '{
  "model": "MODEL",
  "messages": [{"role": "user", "content": "The code below has a bug, use the report_bug tool to report it.\n\nfunc add(a, b int) int {\n  return a - b\n}"}],
  "tools": [{"type": "function", "function": {"name": "report_bug", "description": "Report a bug in the code",
    "parameters": {"type": "object", "properties": {"line": {"type": "integer"}, "description": {"type": "string"}}, "required": ["description"]}}}]
}'
```

Pass = structured `tool_calls` array in the response. Fail = the "call"
appears as text inside `content`.

**Caveat learned the hard way:** passing this bare test is necessary but
not sufficient. OCR's real prompt is ~3k tokens of role/rule scaffolding,
and small models degrade under it. `qwen3.5:4b` passed the curl test but
failed the real review (see below). **Treat sub-~8b as unviable for OCR.**
Always confirm with an actual scratch-diff review (a few changed lines,
one planted bug, `ocr review --audience agent`).

## Model viability on this machine (96 GB RAM, 2026-09-28)

| Model | Size | Tool test | OCR end-to-end | Notes |
|---|---|---|---|---|
| `qwen3.6-coding` | 19 GB | pass (correct line + description) | **PASS** — found planted `a-b` bug, doc/impl mismatch, `panic`-in-library; suggested fixes | Default. Coding-specialized |
| `qwen3.5:4b` | 3.4 GB | pass | **FAIL** — round 1: "no actual code changes were provided in the `<review_files>` block" (hallucination); round 2: `task_done(state:FAILED)`; item failed | Too small for the prompt |
| `ornith-1.5:35b` | 22 GB | untested | untested | viable upgrade if quality needs it |
| `muse-glimmer:30b-mlx` | 21 GB | untested | untested | viable upgrade |
| `glm-4.7-flash` | 18 GB | untested | untested | viable upgrade |
| `gpt-oss` | 13 GB | untested | untested | MoE; decent tool support upstream |
| `granite4.2:8b` | 5.3 GB | untested | untested | borderline size |
| `deepseek-r1:14b` | 9 GB | n/a | known failure mode | narrates tools; skip |

`":cloud"` entries in `ollama list` are router aliases, not local models.

## Failure forensics

Review sessions land in `~/.opencodereview/sessions/<encoded-cwd>/<id>.jsonl`
(`ocr session list` in the repo directory). Each line is a typed event
(`session_start`, request/response pairs, `llm_response` with
`tool_calls` + `usage`, `review_item_failed`). Read it before re-running —
it distinguishes "model can't tool-call" from "prompt too long for the
model" from "timeout".

## Timeouts

- Per-provider: `custom_providers.<name>.timeout_sec` (set 900 here).
- Legacy: `llm.timeout_sec`.
- Env override: `OCR_LLM_TIMEOUT` (seconds).
- Symptom of too-small: "Comment filtering (1 request): calc.go: timed out
  -> failed" in the run summary — the main findings are still published;
  the post-filter pass just didn't run. `--no-filter` skips it entirely.

## Swapping models

```bash
ocr config set custom_providers.ollama.model <name>
ocr llm test
# then a scratch-diff review to confirm end-to-end
# or per-run: ocr review --model <name>
```
