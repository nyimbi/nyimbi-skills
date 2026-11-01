# File Organization

Purpose: the method for turning a messy directory into a proposed structure, an
approved plan, and a logged set of moves — plus duplicate handling and a
maintenance cadence. This is the filesystem track of
`file-media-and-engagement-tools`.

## Scope questions (ask before touching anything)

- Which directory: Downloads, Documents, one project, or the whole home folder?
- What's the actual complaint: can't find things, duplicates, no structure, or clutter?
- What is off limits: active projects, sensitive data, shared drives?
- How aggressive: conservative (sort new stuff only) vs. comprehensive (dedupe + archive + restructure)?

Aggressiveness determines whether you may delete at all. Default to **never
delete without explicit confirmation**, even for exact duplicates.

## Inspecting the target

```bash
ls -la <target>                                              # overview
find <target> -type f -exec file {} \; | head -20            # real types, not extensions
du -sh <target>/* | sort -rh | head -20                      # largest items
find <target> -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn   # type mix
find <target> -type f -printf '%TY-%Tm-%d %p\n' | sort | head/tail   # date range
```

Report before proposing: total files and folders, type breakdown, size
distribution, date ranges, and the specific structural problems observed.

## Grouping axes

| Axis | Use when |
|---|---|
| By type | Media or reference collections (PDF, images, video, archives, code, spreadsheets, decks) |
| By purpose | Mixed work — Work vs. Personal, active vs. archive, project vs. reference vs. scratch |
| By date | Volume is high and content is interchangeable (current month, current year, older → archive) |
| By project | Files exist only to serve a named deliverable |

Pick **one primary axis** and one secondary; three-way nesting without a reason
is how folders become unusable again.

## Duplicate detection

```bash
find <dir> -type f -exec md5 {} \; | sort | uniq -d   # exact content duplicates
find <dir> -type f -printf '%f\n' | sort | uniq -d     # same name
find <dir> -type f -printf '%s %p\n' | sort -n         # same size, likely pairs
```

For each duplicate set show all paths, sizes, and modification dates, then
recommend the keeper (usually newest or best-named). Deleting any of them
requires confirmation — record the decision so it can be undone.

## Plan format (present, then execute)

```markdown
# Organization Plan for <directory>

## Current State
X files across Y folders, [size], type breakdown, structural issues.

## Proposed Structure
<directory>/
├── Work/{Projects,Documents,Archive}/
├── Personal/{Photos,Documents,Media}/
└── Downloads/{To-Sort,Archive}/

## Changes I'll Make
1. Create: [folders]
2. Move: N PDFs → Work/Documents/; M images → Personal/Photos/
3. Rename: [pattern, e.g. "YYYY-MM-DD - Description.ext"]
4. Delete: [duplicates/trash — only with explicit approval]

## Files Needing Your Decision
- [ambiguous items listed individually]

Ready to proceed? (yes / no / modify)
```

## Execution rules

- `mkdir -p` the structure first, then move file by file, logging each move for undo
- Preserve original modification dates; handle name collisions explicitly instead of overwriting
- Rename consistently (`YYYY-MM-DD - Description.ext`), never renaming active-project files without asking
- Stop and ask on anything unexpected: symlinks, permission errors, files in use, size surprises

## Close-out

Summarize what changed (folders created, files moved, GB freed, items
archived), show the new tree, list files left undecided, and give a maintenance
cadence: weekly sort of new downloads, monthly review and archive, quarterly
duplicate check, yearly archive of the previous year.

## Quality gates for this track

- Scope, aggressiveness, and off-limits paths confirmed before any move
- A written plan existed and was approved before execution
- No deletion happened without explicit confirmation; every move is logged
- Modification dates preserved; collisions resolved deliberately
- The new structure uses one primary grouping axis, and the close-out states it
