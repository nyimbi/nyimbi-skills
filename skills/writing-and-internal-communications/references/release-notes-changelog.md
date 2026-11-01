# Changelog and Release Notes from Git History

Format reference for step 4 of the [SKILL.md](../SKILL.md) workflow. Turns commits into
release notes a user can read; the evidence check in step 5 treats the commit range as
the source of truth.

## Inputs to establish

- **Range**: since last tag (`v2.4.0..HEAD`), a date range, or a named version.
- **Audience**: customers (default), internal release docs, app-store reviewers.
- **Style**: `CHANGELOG_STYLE.md` or `CHANGELOG.md` conventions if the repo has them.
- **Branch/remote**: confirm the local repo is on the right branch and fetched.

## Gather

```bash
git log --oneline <tag>..HEAD              # or --since="2024-03-01"
git log --no-merges --pretty=format:'%h %s' <tag>..HEAD
git diff --stat <tag>..HEAD                # scope sense
git tag --sort=-creatordate | head         # find the previous release
```

For each commit worth keeping, open the diff if the subject line is ambiguous —
categorize from what changed, not from the commit message alone.

## Categorize and translate

| Category | Look for | Write as |
|---|---|---|
| New features | new user-facing capability | named capability + what it lets you do |
| Improvements | perf, UX, quality changes | measurable change where one exists |
| Fixes | bug resolutions | symptom the user saw, now resolved |
| Breaking changes | API/schema/behaviour changes | what changed, migration action required |
| Security | patches, hardening | what was protected — no exploit detail |
| Internal (drop) | refactors, tests, CI, deps, chores | excluded from user-facing output |

Translation rules: technical commit → customer language; one line per change unless a
breaking change needs a paragraph; strip jargon, ticket IDs, and internal component
names; group related commits into a single named bullet rather than one bullet per
commit.

## Shape

```markdown
# <Product> — <version or date range>

## ✨ New
- **Named Feature**: what it does for the user in one sentence.

## 🔧 Improved
- Faster X — now <measurable difference>.

## 🐛 Fixed
- Symptom the user would have reported.

## ⚠️ Breaking
- What changed → what to do about it.
```

## Rules

- Every claim must trace to a commit in the range — do not invent improvements.
- Skip the release entirely if nothing user-facing changed; say so.
- Review the generated notes before publishing; adjust wording to house voice.
- Output targets: `CHANGELOG.md`, GitHub release body, app-store description, in-app
  update notice — same content, different length.
