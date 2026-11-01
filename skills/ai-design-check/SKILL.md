---
name: ai-design-check
description: Run the machine floor-gate for AI-built interfaces before any UI work is called done — 49 rules checked automatically (of 74; the rest need eyes), reporting rule id + file:line, exit 1 on errors; plus inventory (distinct button/heading "looks" census), narrow (320px render to catch overflow), baseline mode and reasoned inline ignores for mid-project adoption. Use on "run the design gate", "is this UI slop-check clean?", before shipping any React/Next/Vue/Svelte/Svelte/HTML/Blade/SwiftUI/Compose screen, or whenever impeccable/ux-excellence/web-artifact-and-app-building finished a screen. Prose craft skills judge what the checker cannot; this proves the floor.
---

# ai-design-check

The checker half of the UI craft pair (upstream: [enmerasoftware/ai-design-check](https://github.com/enmerasoftware/ai-design-check), MIT — vendored here whole; `RULES.md` documents all 74 rules with reasons; `RESEARCH.md` the validation against 16 high-rated Dribbble/Behance dashboards). Our `impeccable`, `ux-excellence` and `design-system` skills decide taste; **this skill proves the floor** — the mechanically true rules a human review repeatedly lets slip late in a build.

## Run it

```
node <skill>/bin/ai-design-check.js <files-or-dirs>       # floor gate: findings + exit 1 on any error
node <skill>/bin/ai-design-check.js inventory <dir>       # census of distinct "looks" — design-system drift
node <skill>/ai-design-check-config --init                # per-project config (also: .design-rules.json)
node <skill>/bin/ai-design-check.js --write-baseline <dir>  # adopt on an existing screen without big-bang fixes
```

Reads `.tsx/.jsx/.vue/.svelte/.html/Blade/CSS/i18n JSON/.swift/.kt`. Zero dependencies, Node 20+, no LLM, no API key. Per-rule severity and `allow` globs live in the config; class rules parse class strings (`class`, `className`, `cn()`, `clsx()`, `cva()`, `twMerge()`) only.

## The two-dimension grading model (adopt this everywhere)

- **Severity**: `error` (must fix) > `warning` > `note`.
- **Enforcement**: `checked` (the CLI proves it) vs `review` (a person/agent judges it).
Every rule our UI skills state should declare where it sits on both axes. A "review" rule with a concrete threshold (≤80 chars, 4.5:1) can be promoted to `checked` when its jurisdiction is a generator we own — see the Lessons on gate scoping.

## Known false-positive surfaces (verified here, 2026-11-01)

The class-string claim ("comments and copy don't trigger them") holds for **HTML comments**; it leaks on:
1. **JSX comments** — `className="…"` inside `{/* … */}` fires class rules. A comment is not an attribute; but the gate can't tell. Baseline it or reword the comment.
2. **Built bundles / inline scripts** — JS comments ("…seamless tile…") and array literals (`[x]`, `[X]` in math) fire `no-buzzwords` and `no-placeholder-data`. **Scope the gate to source, never the built page**; the examples' dist outputs are out of jurisdiction.
3. Mitigation when running wide: config `allow` globs, per-rule severity, or a committed baseline reviewed like code.

## Excluded rules in this bundle

Per owner decision: **`locale-aware-case`** (Turkish i/İ case-mapping) — ignored. The other locale rules stand, generalized: `locale-number-format` (all numbers through `Intl` formatters with explicit locale — KES/M-Pesa-aware), `no-naive-plural` (real plural forms), `no-concatenated-translation` (sentences are one key with placeholders).

## Wire it into the craft loop

- After `impeccable` or `ux-excellence` finishes a screen: run the gate on the touched source; findings above baseline are part of the review loop's material — the model then judges the "review" rules and the taste the rules cannot reach.
- Continuous enforcement during builds: a Claude Code `PostToolUse` hook running the checker per edited file, exit 2 → agent keeps working. Configure via the `update-config` skill; scope the hook's glob to the project's source directories.
- `narrow` renders at phone width through your Chrome to catch overflow and cutoff — run it on every responsive deliverable, in addition to the ink engine's phone shot recipe.
- `story` renders a before/after fix video (DevTools + ffmpeg) — the artifact of record for remediation claims.

## Provenance (this bundle's canaries)

- Planted 14 violations across 12 rule families on a `.tsx` canary: all 14 reported, exit 1. ✓
- Comments-in-JSX and built-bundle false positives reproduced. Recorded above. ✓
- Exit code is 1 on errors, 0 on warnings-only — do not read only the printout; check `$?`.