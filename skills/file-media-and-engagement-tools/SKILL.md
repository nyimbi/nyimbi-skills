---
name: file-media-and-engagement-tools
description: >-
  Six hands-on tools for files, media, and engagement: organize a messy folder
  into a stated structure with duplicate detection and an approved move plan,
  file invoices and receipts into a tax-ready tree with a summary CSV, download
  a video or just its audio at a chosen quality and format, pick raffle and
  giveaway winners with auditable randomness, rewrite a tweet against how the
  ranking system actually scores it, and build Slack-optimized GIFs and emoji
  animations that fit Slack's size limits. One workflow runs through all six:
  identify the track and its hard limit, inspect the inputs, state the plan,
  act, verify against that limit, then report what changed. Use when the user
  says "organize my downloads", "clean up these folders", "find duplicate
  files", "organize these invoices for taxes", "rename these receipts",
  "download this video", "get the audio only", "pick a raffle winner", "split
  this list into teams", "optimize my tweet", "why won't this tweet perform",
  or "make me a GIF for Slack". Do not use for extracting or merging PDF
  contents (see pdf-processing), for polishing prose and documents (see
  writing-and-internal-communications), or for designing branded visual assets
  (see visual-design-and-branding).
---

# File, Media and Engagement Tools

Six requests that look unrelated — tidy my Downloads, file these invoices,
grab this video, draw a winner, fix this tweet, make me a Slack GIF — are the
same job wearing different clothes. Each has **inputs**, a **hard limit** the
result must satisfy, and a **verifiable output**. The workflow below is the
shared spine; what differs per track is the limit and the artifact.

The failure mode is shared too: acting on an unseen input, or declaring success
without checking the constraint. Both are avoided by inspecting first and
verifying last.

## When to use

- Sorting, renaming, or restructuring files — Downloads, Documents, a project folder, an archive pass
- Finding duplicates and deciding which copy to keep
- Preparing invoices, receipts, or statements for tax season, with a summary CSV for the accountant
- Downloading a single video or extracting its audio at a stated quality and format
- Picking raffle, giveaway, or contest winners, runners-up, or random team assignments
- Rewriting or diagnosing a tweet or thread for reach and engagement
- Building an animated GIF or emoji that has to fit inside Slack's limits
- Any "make the artifact, then check it actually works" file or media task

**Do not use for** — `pdf-processing` when the deliverable is the PDF itself
(extracted text, merged or split documents, forms, OCR output as the artifact);
`writing-and-internal-communications` when the ask is to write or polish prose
and documents rather than reorganize or rank them; and
`visual-design-and-branding` when the deliverable is a designed visual asset,
layout, or brand system rather than a functional GIF inside a platform's limits.

## Workflow

1. **Identify the track and its hard limit.** Map the request to one of the six
   tracks below and write down the constraint the result must satisfy — file
   size, format, randomness auditability, a filename pattern, a ranking
   mechanism. Output: named track + one stated limit + the artifact that will
   prove success.

   | Track | Inputs | Hard limit | Deliverable |
   |---|---|---|---|
   | File organization | a directory | no deletion without approval; one grouping axis | approved plan + logged moves |
   | Invoice filing | PDFs/images folder | standard filename pattern; originals preserved | filed tree + summary CSV |
   | Video download | a URL | quality/format choice; one video, not a playlist | verified file on disk |
   | Random selection | list/CSV/sheet | cryptographically secure, no duplicate winners | draw result with timestamp |
   | Tweet optimisation | a draft | must serve a named ranking mechanism or signal | before/after rewrite |
   | Slack GIF | a described animation | Slack size and dimension limits for its use | validated GIF |

2. **Inspect the inputs before planning.** Inventory what is actually there:
   the directory's file mix and sizes, the invoice count and date range, the
   URL and available quality, the entry count after exclusions, the draft's
   current wording, the GIF's frame and colour budget. State what is ambiguous
   (unclear files, blocked URLs, ineligible entries) instead of assuming.
   Output: an inventory with counts, plus an explicit ambiguity list.

3. **State the plan and get agreement.** For anything that changes existing
   files, show the plan first: the target tree, before/after rename examples,
   the duplicate keep-or-drop calls, files needing a decision. For
   parameter-driven work, confirm the parameters: quality and destination,
   winner count and exclusions, grouping scheme, target size. Output: an
   approved plan or parameter set — nothing is modified before this.

4. **Prepare the tool.** Install or point at what the track needs —
   `scripts/video-downloader.py` (drives `yt-dlp`, installs itself), `pip
   install -r scripts/slack-gif-creator/requirements.txt` with snippets run
   from `scripts/slack-gif-creator/`, the listing and hashing commands for the
   filesystem tracks. Output: a tool that runs, proven by a dry run or a
   single-item test before bulk work.

5. **Execute on one item, then the rest.** Do a single representative case
   first — one file moved, one invoice renamed, one short download, one GIF
   rendered, one draft rewritten — check it against the limit, then proceed in
   batch. Log every move and every rename as you go. Output: the transformed
   set, with the log that makes it reversible.

6. **Verify against the limit.** Re-check the constraint on the *result*, not
   the intent: files landed where the plan said, names sort correctly, the
   video exists and is non-zero, the GIF passes Slack validation, the winner
   count matches after exclusions, every rewrite names its mechanism. Fix and
   re-verify anything that fails — reducing colours and frames for an
   over-budget GIF, routing an unreadable invoice to Needs Review. Output:
   pass/fail per gate, with failures fixed or reported.

7. **Report and hand off.** State what changed in numbers (files organized,
   GB freed, invoices filed, size of the GIF, entries after exclusions), show
   the artifact (new tree, summary CSV, output path, draw result, before/after
   table), list what remains undecided, and offer the natural next action.
   Output: the change report in the Output format below.

## Quality bar

- [ ] Track and hard limit were named before any input was modified
- [ ] Inputs were inventoried with real counts; ambiguities are listed, not assumed away
- [ ] Plan or parameters were shown and agreed before bulk changes
- [ ] Nothing was deleted without explicit approval; every move and rename is logged
- [ ] A single representative item was executed and checked before batch work
- [ ] Verification ran on the result (path, size, count, mechanism), and failures were fixed or reported
- [ ] Output artifacts (tree, CSV, file path, draw record, before/after) are present and match reality
- [ ] Failures and skipped items are quoted verbatim — no partial result reported as success
- [ ] The report ends with a specific next action the user can take

## Reference map

| Situation | Open |
|---|---|
| Scope questions, grouping axes, duplicate hashing, move plan | [file-organization.md](references/file-organization.md) |
| Invoice field extraction, filename standard, filing scheme, summary CSV | [invoice-organization.md](references/invoice-organization.md) |
| Download options table, yt-dlp behaviour, output verification | [video-downloading.md](references/video-downloading.md) |
| Sources, exclusions, weighted draws, fairness record, announce format | [raffle-winner-selection.md](references/raffle-winner-selection.md) |
| Ranking models, signal weights, strategy map, rewrite procedure | [twitter-algorithm-optimization.md](references/twitter-algorithm-optimization.md) |
| Slack limits, validators, thirteen animation primitives, helper modules | [slack-gif-creation.md](references/slack-gif-creation.md) |
| Reading, splitting, or merging PDF documents as the deliverable | [../pdf-processing/SKILL.md](../pdf-processing/SKILL.md) |

## Output format

Every track closes with the same change report; the artifact block changes with
the track.

```markdown
# <Track> — Change Report

## What I did
2-3 sentences: inputs handled, the plan followed, the limit targeted.

## Inputs
Counts and scope: files in scope, invoices found, URL, entries after
exclusions, frames and colours budget, or draft reviewed.

## Result
- Track-specific numbers: files organized / GB freed / invoices filed and
  total amount / output path and file size / winner row and timestamp /
  GIF dimensions, frames, KB / rewrite changes applied
- The artifact: new folder tree, `invoice-summary.csv`, download path,
  draw record, before/after table, or validated GIF

## Verification
Pass/fail per gate from the track's quality bar, with the fix applied to
anything that failed.

## Decisions and leftovers
Items needing the user's call, skipped or unreadable files, anything out
of scope.

## Next steps
Numbered, specific, and runnable now (review the CSV, announce the
winner, post the rewrite, upload the GIF).
```
