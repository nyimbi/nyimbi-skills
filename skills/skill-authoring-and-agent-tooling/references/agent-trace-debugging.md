# Agent Trace Debugging with LangSmith Fetch

Purpose: command reference and diagnostic patterns for pulling execution traces
out of LangSmith Studio and turning them into a root cause. Read this when an
installed capability misbehaves at runtime.

## Setup

```bash
pip install langsmith-fetch
export LANGSMITH_API_KEY="..."
export LANGSMITH_PROJECT="..."
```

Verify with `echo $LANGSMITH_API_KEY` / `echo $LANGSMITH_PROJECT` before
troubleshooting anything else — most "no traces" reports are configuration.
`langsmith-fetch config show` prints the current config; `langsmith-fetch config
set project "<name>"` persists it. Put exports in `~/.bashrc` or `~/.zshrc` if
they do not survive new shells.

## Command patterns

| Situation | Command |
|---|---|
| What just happened | `langsmith-fetch traces --last-n-minutes 5 --limit 5 --format pretty` |
| Deep dive on one trace | `langsmith-fetch trace <trace-id> --format json` |
| Scan for failures | `langsmith-fetch traces --last-n-minutes 30 --limit 50 --format raw \| grep -i "error\|failed\|exception"` |
| Export a debug session | `langsmith-fetch traces ./session-<ts> --last-n-minutes 30 --limit 50 --include-metadata` |
| Export conversation threads | `langsmith-fetch threads ./session-<ts>/threads --limit 20` |
| After a timestamp | `langsmith-fetch traces --after "2025-12-24T13:00:00Z" --limit 20` |
| Speed up a large export | `langsmith-fetch traces ./out --limit 100 --concurrent 10` |

Formats: `pretty` for reading and showing a human, `json` for analysis, `raw`
for piping into `grep`/automation.

## Four diagnostic workflows

**1. Quick health check.** Pull the last few minutes, then report five things:
trace count, any errors, tools called, durations, token usage. If zero traces
come back, the cause is almost always one of: tracing disabled
(`LANGCHAIN_TRACING_V2=true`), wrong project name, bad API key, or the agent
never actually ran. Widen the window to `--last-n-minutes 1440` before
concluding anything.

**2. Root-cause a specific trace.** Load it as JSON and reconstruct, in order:
what the agent was trying to do → which tools ran → each tool's result → the
first failure → why it failed → the fix. Report the ordered execution flow, the
single failure point, the root cause in one sentence, 2-3 concrete fixes, and
the token/duration cost of the run.

**3. Error sweep.** Fetch a window as JSON, count failures against totals, then
group by error type with frequency, first/last occurrence, the agent and tool
involved, and the pattern (peak load? one misconfigured tool? a tool name that
does not exist?). Close with prioritized recommendations, not a log dump.

**4. Performance pass.** Export with `--include-metadata` and rank by execution
time, tool-call latency, token usage (context size), iteration count, and
slowest operations. Name the bottleneck explicitly.

## Symptom → check

| Report | First checks |
|---|---|
| "Agent isn't doing anything" | Traces exist? If no: tracing flag, project, key, did it run. If yes: errors, is it hanging, did tool calls complete? |
| "It called the wrong tool" | Load the trace, list tools available at execution time, read the reasoning step, then fix the tool description or the instructions — not the model |
| "It doesn't remember things" | Grep traces for memory operations: were they called, did recall return results, were writes persisted, are retrieved memories actually used in the reply? |
| "Too slow" | Per-trace duration, tool latencies, token/context size, iteration count — in that order |

## Reporting rules

- Lead with the finding and the fix; the trace dump is evidence, not the answer.
- Quote the exact error string and the tool it came from.
- When exporting a session for a team, keep the folder layout
  (`langsmith-debug/session-<timestamp>/{traces,threads}`) and note the file
  count and size so the recipient knows what they received.
- Save problematic traces under an `error-cases/` folder with a one-line README
  entry and the trace ID — that ID is what gets shared in an issue.
