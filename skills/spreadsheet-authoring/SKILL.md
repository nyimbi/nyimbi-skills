---
name: spreadsheet-authoring
description: >-
  Use this skill whenever a spreadsheet file is the primary input or output.
  Triggers include "fix these formulas", "chart this range", "add a column of
  growth rates", "clean up this CSV", "build a three-statement model", "preserve
  the formatting when you edit it", "why is this cell #REF!", "recalculate the
  workbook", "convert these tabs into one sheet", and any reference to an .xlsx,
  .xlsm, .xltx, .csv, or .tsv file by name or path — even casually, like "the xlsx
  in my downloads". It owns the spreadsheet format and its tooling: openpyxl for
  formulas, styles, and structure; pandas for bulk data in and out; markitdown for a
  quick look; and the mandatory LibreOffice recalculation pass that turns formula
  strings into real cached values with a zero-error report. It also covers cleaning
  malformed tabular data into a proper workbook. Do not use for prose or a report
  deliverable (see writing-and-internal-communications), for Word or PowerPoint files
  (see word-document-authoring, presentation-authoring), or for a coded dashboard
  (see web-artifact-and-app-building).
---

# Spreadsheet Authoring

A spreadsheet is a program the user will keep running after you hand it over, so the
bar is not "the numbers look right now" — it is "the numbers stay right when an input
changes". Three failure modes account for nearly every bad workbook: a value computed
in Python and hardcoded where a formula belonged, a formula that LibreOffice cannot
evaluate and that ships as `#NAME?`, and a recalculation pass skipped, leaving every
formula cell empty to anything that reads cached values. The workflow below closes
all three.

## When to use

- Creating a workbook from scratch or from other data sources
- Editing an existing `.xlsx`/`.xlsm`: adding columns, data, formulas, formatting
- Building or repairing a financial model, forecast, or scenario table
- Fixing formula errors — `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`, `#N/A`
- Charting, pivoting, or summarising a range into a readable sheet
- Cleaning or restructuring messy tabular data (malformed rows, misplaced headers)
- Converting between tabular formats (`.csv` ↔ `.tsv` ↔ `.xlsx`)
- Reading a workbook's contents or extracting a sheet for use elsewhere

**Do not use for** — `writing-and-internal-communications` when the ask is the
narrative or the exec summary of the numbers rather than the workbook;
`web-artifact-and-app-building` when the deliverable is a coded dashboard or web app
instead of a spreadsheet file; `file-media-and-engagement-tools` when the job is a
bulk format conversion with no formulas, formatting, or structure to preserve;
`word-document-authoring` / `presentation-authoring` when the target file is a
`.docx` or `.pptx`, even if the source data is a table.

## Workflow

1. **Choose the tool by task.**

   | Task | Tool |
   |---|---|
   | Formulas, styles, workbook structure, editing an existing file | `openpyxl` |
   | Bulk data in or out, analysis, reshaping | `pandas` (`read_excel`, `to_excel`) |
   | Quick look at a sheet's contents | `markitdown file.xlsx` — `## SheetName` per sheet; no cell coordinates, so never plan edits from it |
   | Read a model (formulas *and* values) | two `load_workbook` passes — see step 2 |

   `openpyxl`, `pandas`, and `markitdown` are preinstalled — import directly and only
   `pip install` if an import or the `markitdown` command actually fails.

2. **Inspect before you write.** For an existing file, find its conventions first:
   tab names, column headers, number formats, and the designated input cells (a
   distinct font colour, fill, or shading marks them). Read formulas and values with
   two loads — `load_workbook(f)` for formula strings, `load_workbook(f,
   data_only=True)` for cached results. One pass cannot give you both, and saving a
   `data_only=True` workbook permanently replaces every formula with a literal.

3. **Write formulas, never Python-computed results.** The sheet must recalculate when
   its inputs change:

   ```python
   sheet['B10'] = '=SUM(B2:B9)'        # not the computed total
   sheet['C5']  = '=(C4-C2)/C2'        # not the growth rate you calculated
   ```

   Pick functions the recalculation engine can actually evaluate:
   - Prefer Excel-2007-era functions — `SUMIFS`, `INDEX`, `MATCH`, `IFERROR`,
     `SUMPRODUCT` — which need no prefix.
   - Six post-2007 functions work only with an `_xlfn.` prefix: `_xlfn.TEXTJOIN`,
     `_xlfn.CONCAT`, `_xlfn.IFS`, `_xlfn.SWITCH`, `_xlfn.MAXIFS`, `_xlfn.MINIFS`.
     Written bare, each yields `#NAME?`.
   - **Never use `XLOOKUP`, `XMATCH`, `SORT`, `FILTER`, `UNIQUE`, or `SEQUENCE`.**
     The runtime's LibreOffice cannot evaluate them under any prefix, and even where
     it can, they are spilling arrays with no spill metadata in an openpyxl-written
     file — only the top-left cell gets a value and the error report says zero
     errors. Use `INDEX`/`MATCH` for lookups; sort, filter, and de-duplicate in
     Python before writing cells.
   - A formula the engine could not parse is written back **lowercased** — a quick
     tell beside a `#NAME?`.

4. **Apply the format conventions.** Unless the user or the existing file says
   otherwise:

   - **Font:** Arial or Times New Roman throughout.
   - **Colour:** blue text (`0,0,255`) for hardcoded inputs and scenario levers;
     black for formulas; green (`0,128,0`) for links to another sheet; red
     (`255,0,0`) for links to another file; yellow fill (`255,255,0`) for key
     assumptions and cells the user must fill in.
   - **Numbers:** currency `$#,##0` with the unit in the header (`Revenue ($mm)`);
     zeros render as `-`, including in percentages (`$#,##0;($#,##0);-`);
     negatives in parentheses; percentages `0.0%` **stored as fractions** (`0.15` →
     `15.0%`; storing `15` renders `1500.0%`); multiples `0.0x`; years as text
     (`"2024"`, never `2,024`).
   - **Structure:** every assumption in its own labelled cell, referenced by the
     formulas that use it (`=B5*(1+$B$6)`, never `=B5*1.05`); formulas identical
     across every projection period — a lone edited cell mid-row is the commonest
     silent error; zero-guarded denominators.
   - **Document every assumption and hardcoded number** where the reader will see it
     (cell comment, or a cell at the table's end), citing a real source when one
     exists (`Source: Company 10-K, FY2024, Page 45, Revenue Note, [SEC EDGAR URL]`)
     and saying plainly when the number came from the user.
   - A workbook **you create for someone to fill in** gets a short legend naming which
     cells to edit plus one example row of realistic values. Never add an example row
     to a file you were asked to edit.
   - **Editing an existing file: its conventions override every guideline here.**
     Write only in the designated input cells; leave every existing formula untouched.

5. **Recalculate — mandatory whenever the file contains formulas.** openpyxl writes
   formulas as strings with no cached values, so until you recalculate, every formula
   cell reads back as `None` to pandas, `data_only=True`, and most previewers:

   ```bash
   python scripts/skills-recalc.py output.xlsx [timeout_seconds]   # default 30
   ```

   LibreOffice computes every formula, the file is **rewritten in place**, and you get
   JSON: `status` (`success` | `errors_found`), `total_formulas`, `total_errors`, and
   an `error_summary` naming up to 100 cells per error type (`locations_truncated`
   says how many it withheld — trust `total_errors`, not the list length). Fix what it
   names and run it again. A JSON with an `error` key instead of `status` means
   nothing was recalculated; only that case exits non-zero, so a clean exit is **not**
   proof of a clean workbook.

   Two implementations ship: `scripts/skills-recalc.py` (detects external workbook
   links, caps reported locations, uses the shared `office` runtime) and
   `scripts/awesome-recalc.py` (configures the LibreOffice macro itself, no external
   link handling). Prefer the first; use the second only if it fails to start.

   **A green recalc proves the formulas evaluate, not that they are right.** An
   off-by-one range or a wrong-row reference yields an error-free file with wrong
   numbers — write 2–3 formulas first and check they pull the values you expect
   before building the grid.

   **External links are destroyed by a re-save.** A formula like
   `='[1]Returns Analysis'!$B$2` points at a separate file on disk; openpyxl strips
   the cached value, LibreOffice then fails to resolve it, writes `#NAME?`, and every
   link is gone. `recalc.py` refuses to run in that state — copy those cells' values
   out of the original first (`--force` overrides and accepts the loss).

6. **Verify and fix before delivering.** See the quality bar. Iterate until
   `scripts/skills-recalc.py` reports `status: success` with `total_errors: 0` **and**
   the spot checks in the quality bar pass.

## Quality bar

- [ ] Zero formula errors: `scripts/skills-recalc.py` reports `status: success` and
      `total_errors: 0`, and the run actually recalculated (a `status` key, not an
      `error` key)
- [ ] Every calculated cell holds a formula string, not a Python-computed literal —
      spot-check a total and a rate by changing an input and confirming it moves
- [ ] The first 2–3 formulas were validated against expected values before the grid
      was built; sample references, column mapping (col 64 = `BL`), and row offsets
      (DataFrame row 5 = Excel row 6) were checked
- [ ] No `XLOOKUP`/`XMATCH`/`SORT`/`FILTER`/`UNIQUE`/`SEQUENCE`; post-2007 functions
      carry the `_xlfn.` prefix; no formula was written back lowercased
- [ ] The user's spec is followed literally: exact tab names, exact column headers,
      the formula they spelled out
- [ ] Every hardcoded number and assumption is documented where it is visible, with a
      real source citation where one exists
- [ ] Professional font throughout; financial-model colour, number, and structure
      conventions applied, or the existing file's own conventions matched exactly
- [ ] Editing an existing file: input-cell conventions respected, existing formulas
      untouched, `.xlsm` macros preserved (`keep_vba=True`), merged cells written
      only at their anchor
- [ ] No workbook was saved from a `data_only=True` load, and no external-link
      workbook was re-saved without first capturing the cached values

## Reference map

| Situation | Open |
|---|---|
| Exact API: pandas read/analyse/write, openpyxl create/edit, merged cells, formula patterns, recalc output shape | [spreadsheet-recipes.md](references/spreadsheet-recipes.md) |

Executable helpers: `scripts/skills-recalc.py` (preferred),
`scripts/awesome-recalc.py` (fallback), `scripts/office/soffice.py` (LibreOffice
wrapper used by the recalculation runtime).

## Output format

Deliver the workbook plus:

```markdown
# <Workbook> — spreadsheet delivery note

## File
Path, format, sheet list, row × column count per sheet.

## What changed
Table: Sheet | Range | Change | Formula or value

## Formulas
The formulas written, one line each, with the range they fill — so the user can
audit consistency across periods.

## Assumptions and sources
Every hardcoded number, its cell, and its source citation.

## Verification
recalc.py JSON: status, total_formulas, total_errors; the spot checks performed
and their expected vs actual values.

## Residual issues
Anything not fixed: inherited errors proven to predate the edit (show the
original's cached value), external links at risk, ranges the engine approximates.
```

For a model handoff, add a short "how to drive it" section naming the input cells
and levers the user is expected to change.
