# Consolidation Spec — skill-bundle

Every skill in this bundle is a **merge of many source skills**. Follow this spec exactly so
all 29 skills read as one coherent product, not 29 different authors.

## 1. Layout

```
skill-bundle/
  README.md                     <- index, provenance, dedup report (written last)
  skills/
    <skill-name>/
      SKILL.md                  <- required, the only file an agent reads first
      references/*.md           <- optional, deep detail loaded on demand
      scripts/*                 <- optional, copied helpers (namespaced, see §6)
      LICENSE.txt / LICENSE     <- required if any source had one (see §5)
```

`<skill-name>` is lowercase, hyphenated, no stop words. Never edit anything outside
`skills/<your-skill>/`.

## 2. SKILL.md frontmatter

```yaml
---
name: <skill-name>              # MUST equal the directory name
description: >-
  <120-220 words. Written as a trigger description, not a summary.
  Must contain: (a) what this skill does, (b) 4-8 concrete trigger phrases
  the user might say verbatim, (c) explicit "do not use for" boundary.
  The description is the ONLY thing the routing layer sees — it must
  disambiguate this skill from every sibling in the bundle.
license: <see §5>
---
```

Optional extra keys are allowed (`domain`, `merged_from_count`, `tags`) but keep them
consistent within a group. **No other frontmatter keys** — drop `mitre_attack`,
`d3fend_techniques`, `nist_csf`, `author`, `version` from sources unless the group
leader (below) says otherwise.

## 3. SKILL.md body — required section order

1. `# <Title Case Name>` (H1, no trailing period)
2. `## When to use` — 4-8 bullets of concrete triggers. Then a bold
   `**Do not use for**` line naming the 2-3 nearest sibling skills in this bundle that
   a router might confuse with this one. Use their real skill names.
3. `## Workflow` — numbered steps. This is the spine of the skill. Every step must be
   an action with an input and an output. 5-9 steps.
4. `## Quality bar` — 5-10 checkable criteria (`- [ ]` style or explicit "must").
   These are gates the agent verifies before delivering.
5. `## Reference map` — table of `| Situation | Open |` pointing at `references/<file>.md`
   relative paths. **Only list files you actually created.** Omit the section if there
   are no references.
6. `## Output format` — the shape of the deliverable (template or structure), only when
   the skill produces a document/artifact.

Rules:
- **Target 150-350 lines for SKILL.md.** Under 120 means you under-merged; over 450
  means you pasted instead of synthesizing — move detail into `references/`.
- Synthesize, do not concatenate. If five sources describe the same workflow step,
  write it once, taking the best version.
- Prefer tables for anything that is a taxonomy, matrix, or decision rule.
- Keep every command/tool invocation that is genuinely load-bearing; drop decorative
  examples and motivational prose from the sources.
- No `## Overview`, no `## Prerequisites` headings as standalone sections — fold
  prerequisites into step 1 of the Workflow.

## 4. references/

Two classes of reference file, both legitimate:

**(a) Per-technique lookup files** — `references/<source-skill-dir>.md`.
These already exist for cybersecurity skills; they are mechanically produced by
`_build/merge_cyber.py` (merges that technique's `api-reference.md`,
`standards.md`, `workflows.md`, `assets/template.md` into one file) and are
**not** to be rewritten. One file per source technique, deduplicated bundle-wide.

**(b) Synthesized topic files** — `references/<topic>.md`, written by you where
cross-cutting synthesis genuinely adds value (a tool-selection matrix, a
comparison table, a decision tree). Normal range 0-6 per skill; only create them
when they are not just a restatement of the SKILL.md.

Rules for both:
- Every reference file reachable from the `## Reference map` table, or — when there
  are many per-technique files — reachable via `references/technique-index.md`
  which is generated mechanically and must not be hand-edited.
- Synthesized files start with `# <Title>` and a one-line purpose sentence.
- **Never** duplicate SKILL.md content in a reference file.

## 5. Licensing

Sources carry mixed licences (Anthropic `LICENSE.txt`, Apache-2.0 per-skill `LICENSE`,
MIT on management-consulting). When merging:
- If **any** source skill had a licence file, copy it into the merged skill directory
  as `LICENSE.txt` (Anthropic) or `LICENSE` (Apache), preserving contents.
- If two different licences end up in one merged skill, keep both as
  `LICENSE.txt` and `LICENSE.apache-2.0` and add a line under the frontmatter:
  `> Licensed under the terms in LICENSE.txt and LICENSE.apache-2.0.`
- Do not invent licence text. Do not drop a licence that existed.

## 6. Scripts / executables

Some source skills ship `agent.py`, `process.py`, or `scripts/`. Rules:
- Copy only scripts a user would actually run to complete the workflow.
- Namespace on copy: `scripts/<original-skill-dir-name>.py` (or keep the original
  filename inside `scripts/<original-skill-dir-name>/` if there are several).
- Skip scripts that are pure boilerplate wrappers, empty stubs, or reference infra
  that is not in this bundle.
- Reference any copied script from SKILL.md or the relevant reference file with an
  explicit relative path.

## 7. Deduplication contract

- **Exact duplicates** (identical name across two source repos): merge into one;
  take the longer/better of the two bodies; record both in the provenance manifest.
- **Near duplicates** (same technique, different tool or angle): merge into one
  section with a tool-comparison row, not two sections.
- **No repeated content across skills in this bundle.** If two skills would both
  explain the same thing, one owns it and the other links to it:
  `See ../<owner-skill>/references/<file>.md` in the Reference map.
- Every skill's `## When to use` must include the `**Do not use for**` cross-boundary
  line so the router cannot confuse siblings.

## 8. Provenance manifest

Each skill writes `_build/provenance/<skill-name>.json`:

```json
{
  "skill": "<skill-name>",
  "merged_from_count": 42,
  "exact_duplicates_merged": ["pdf (awesome-claude-skills) + pdf (skills/skills)"],
  "near_duplicates_merged": ["scanning-docker-images-with-trivy + scanning-containers-with-trivy-in-cicd"],
  "dropped": [{"name": "...", "reason": "boilerplate / superseded / out of scope"}],
  "source_roots": ["Cybersecurity-Skills", "..."],
  "reference_files": ["..."],
  "scripts_copied": ["..."]
}
```

## 9. Definition of done

- [ ] frontmatter `name` == directory name
- [ ] description is 120-220 words, has triggers + do-not-use boundary
- [ ] body sections appear in the §3 order
- [ ] SKILL.md is 150-450 lines
- [ ] every `## Reference map` row points to a file that exists
- [ ] no reference file duplicates SKILL.md content
- [ ] licence files carried over
- [ ] provenance JSON written
- [ ] no content copied verbatim from a source without synthesis
