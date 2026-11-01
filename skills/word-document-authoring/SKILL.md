---
name: word-document-authoring
description: >-
  Use this skill whenever the user wants to create, read, edit, or review a Word
  document. Triggers include "turn this outline into a report", "make it a .docx",
  "add tracked changes", "redline this contract", "accept the revisions", "add a
  comment on this clause", "insert a table of contents", "apply the heading styles",
  "what does this Word file say", and any mention of .docx, .dotx, "Word doc",
  "memo", "letter", "template", or "deliverable as a Word document". It owns the
  docx file format and its tooling: docx-js for authoring new files, raw OOXML for
  editing existing ones, pandoc for text extraction, tracked-changes and comment
  markup, style and numbering XML, and render-and-inspect verification. It also
  covers reading content out of a .docx even when the extracted text will be reused
  somewhere else. Do not use for producing PDFs (see pdf-processing), for deciding
  what the document should say (see writing-and-internal-communications), or for
  decks and spreadsheets (see presentation-authoring, spreadsheet-authoring).
---

# Word Document Authoring

A `.docx` is a ZIP archive of XML, and the XML is not where the prose lives — Word
splits one visible sentence across many `<w:r>` runs for revision ids, spell-check
markers, and formatting. Everything difficult about this format follows from that:
find-and-replace misses, tracked changes that render as stray empty bullets, tables
that collapse because a column width was written once instead of twice. Pick the
route by task, and verify by rendering, never by reading the XML you just wrote.

## When to use

- Creating a new report, memo, letter, contract, or template as a `.docx`/`.dotx`
- Editing an existing Word file: text, styles, headings, tables, headers, numbering
- Adding or reviewing tracked changes (redlining), then accepting or rejecting them
- Adding anchored comments, replies, and comment metadata
- Reading or extracting content from a `.docx`, including with revisions visible
- Converting legacy `.doc` to `.docx`, or fixing a document that Word refuses to open
- Building a table of contents, cross-references, page numbers, or section breaks
- Inserting images, hyperlinks, or footnotes with correct relationship entries

**Do not use for** — `pdf-processing` when the deliverable is a PDF or the job is to
merge/OCR/fill PDFs; `writing-and-internal-communications` when the question is what
to write rather than how to encode it as a Word file; `presentation-authoring` and
`spreadsheet-authoring` when the target format is `.pptx` or `.xlsx`.

## Workflow

1. **Choose the route before touching anything.** The tool differs per task; getting
   this wrong is the most common failure.

   | Task | Approach |
   |---|---|
   | **Read** content | `pandoc --track-changes=all file.docx -o out.md` |
   | **Create** a new document | Write a `docx` (npm) script — see step 3 |
   | **Edit** your own simple change | `unzip` → edit `word/document.xml` → `zip` |
   | **Edit** someone else's document | Redlining workflow (step 5) — the default |
   | **Legal / academic / government** document | Redlining workflow — required |
   | **Comments or complex structure** | Unpack, then `scripts/comment.py` or the Document library |

   Prerequisites: `pandoc`, `docx` (npm), LibreOffice (`soffice`), `pdftoppm`
   (Poppler), `defusedxml`, and `python-docx`. `docx` is preinstalled — only run
   `npm install docx` if `require('docx')` fails.

2. **Read and inspect first.** Convert to markdown to see structure and existing
   revisions; unpack only when you need comments, media, or raw formatting:

   ```bash
   pandoc --track-changes=all file.docx -o current.md
   unzip -q file.docx -d unpacked/
   find unpacked -type l -delete   # strip symlinks — external docx is untrusted
   ```

   Key parts: `word/document.xml` (body), `word/comments.xml` (comments),
   `word/media/` (images), `<w:ins>`/`<w:del>` (revisions).

3. **Create with `docx-js`.** Read [`references/docx-js.md`](references/docx-js.md)
   in full first, then write a script using `Document`/`Paragraph`/`TextRun` and
   export with `Packer.toBuffer()`. The footguns the model knows the API for:

   - **Page size defaults to A4.** US Letter: `page: { size: { width: 12240,
     height: 15840 } }` (DXA; 1440 = 1″).
   - **Landscape:** pass portrait dimensions plus
     `orientation: PageOrientation.LANDSCAPE` — docx-js swaps them internally.
   - **Tables need dual widths:** `columnWidths` on the table **and** `width` on
     every cell, both `WidthType.DXA` (`PERCENTAGE` breaks in Google Docs). Column
     widths must sum to the table width.
   - **Table shading:** `ShadingType.CLEAR`, never `SOLID` (renders black).
   - **Lists:** never type `•`; use a `numbering` config with `LevelFormat.BULLET`.
   - **`ImageRun` requires `type:`** (`"png"`, `"jpg"`, …).
   - **`PageBreak` must be inside a `Paragraph`.**
   - **Never use `\n`** — separate `Paragraph` elements.
   - **TOC:** headings must use built-in `HeadingLevel.*`; custom heading styles
     need `outlineLevel` set or they never appear.
   - **Don't fake a horizontal rule with a table** — use a paragraph bottom border.
   - **Dot leaders / right-aligned tab:** `PositionalTab`
     (`alignment: PositionalTabAlignment.RIGHT`, `leader: PositionalTabLeader.DOT`)
     inside a `TextRun`, not literal `.` padding.

4. **Edit an existing file through the ZIP.** Convert `.doc` first
   (`python scripts/office/soffice.py --headless --convert-to docx file.doc`), then:

   ```bash
   python scripts/merge_runs.py unpacked/     # coalesce fragmented runs
   # edit unpacked/word/document.xml in place — do NOT reformat or pretty-print
   (cd unpacked && rm -f ../out.docx && zip -Xr ../out.docx .)
   python scripts/office/validate.py out.docx --original file.docx
   ```

   `merge_runs.py` matters because a phrase you can see often does not exist as a
   contiguous string in the XML; it merges adjacent identically-formatted runs
   without changing content, and also accepts a `.docx` directly
   (`python scripts/merge_runs.py file.docx -o merged.docx`).

5. **Redline deliberately, in batches.** For any document you did not author, plan
   the tracked changes in markdown first, then implement them in 3–10 change batches,
   validating each batch before moving on.

   - **Mark only what changed.** Replace `30 days` → `60 days` by keeping the
     unchanged runs and wrapping just the changed token:

     ```python
     # BAD — replaces the whole sentence
     '<w:del><w:r><w:delText>The term is 30 days.</w:delText></w:r></w:del><w:ins><w:r><w:t>The term is 60 days.</w:t></w:r></w:ins>'
     # GOOD — unchanged text keeps its original <w:r> and RSID
     '<w:r w:rsidR="00AB12CD"><w:t>The term is </w:t></w:r><w:del><w:r><w:delText>30</w:delText></w:r></w:del><w:ins><w:r><w:t>60</w:t></w:r></w:ins><w:r w:rsidR="00AB12CD"><w:t> days.</w:t></w:r>'
     ```

   - Wrap runs in `<w:ins>`/`<w:del>` carrying `w:id`, `w:author`, `w:date`. Inside
     `<w:del>` the text element is `<w:delText>`, not `<w:t>`.
   - A deleted paragraph mark (`<w:pPr><w:rPr><w:del …/></w:rPr></w:pPr>`) means
     "join this paragraph into the next". Deleting a paragraph outright is that plus
     a `<w:del>` around every run. The `<w:del/>` must precede the `rPr`'s other
     children — the order is schema-enforced.
   - Find changes by section number, paragraph id, or a grep pattern with unique
     surrounding text — never by markdown line numbers.
   - `scripts/office/validate.py --original file.docx --author "<your redline name>"`
     reports any text you changed without a `<w:ins>`/`<w:del>` around it, which is
     invisible in the accepted view and easy to do by accident.

   To produce a clean copy: `python scripts/accept_changes.py in.docx out.docx`.
   Known asymmetry: a paragraph whose runs are all deleted should vanish when the
   mark is accepted. `pandoc --track-changes=accept` never joins the paragraphs;
   `accept_changes.py` joins them except when the deleted paragraph is followed by an
   empty spacer. An empty bullet in either view is an artifact of that view — check
   the paragraph deletion in the XML before "fixing" it.

6. **Add comments with the helper, then place the anchors.** Comments require six
   cross-linked files; `scripts/comment.py` writes them all:

   ```bash
   python scripts/comment.py unpacked/ "Fees & expenses cap is too low"   # dir mode
   python scripts/comment.py unpacked/ "Agreed" --parent 0                # reply
   python scripts/comment.py contract.docx "This cap is too low" -o annotated.docx
   ```

   It prints the `<w:commentRangeStart>`/`<w:commentRangeEnd>`/`<w:commentReference>`
   snippet to paste into `word/document.xml`. Until those markers exist the comment
   is stored but not visible. For heavier structural work — tracked changes at scale,
   comment infrastructure, RSID handling — use the Document library described in
   [`references/ooxml.md`](references/ooxml.md) (`from scripts.document import
   Document` with `PYTHONPATH` set to this skill's root).

7. **Verify by rendering, then by re-reading.** Both halves are mandatory:

   ```bash
   python scripts/office/soffice.py --headless --convert-to pdf output.docx
   pdftoppm -jpeg -r 100 output.pdf page
   ls page-*.jpg    # Read the images
   pandoc --track-changes=all output.docx -o verify.md   # then grep for the edits
   ```

   `pdftoppm` zero-pads page numbers to the width of the page count
   (`page-01.jpg`…`page-12.jpg`).

## Quality bar

- [ ] The route chosen matches the task: never docx-js on an existing file (it
      cannot open one), never raw unzip for a first draft you could have generated
- [ ] `python scripts/office/validate.py out.docx --original src.docx` passes; for
      redlines, a run with `--author` reports no untracked edits
- [ ] Every revision carries `w:id`, `w:author`, and `w:date`; deletions use
      `<w:delText>`; deleted paragraph marks are present and correctly ordered
- [ ] Rendered pages were inspected: no overflow, no collapsed tables, TOC present
      and populated, list numbering continuous, images not stretched
- [ ] Comments are anchored — the range markers exist in `document.xml`, not just
      `comments.xml`
- [ ] Unchanged text kept its original runs and RSIDs; no wholesale
      delete-and-retype of a paragraph
- [ ] Styles are applied via `HeadingLevel`/style names, not by hand-bolding runs,
      so the navigation pane and TOC work
- [ ] `pandoc --track-changes=all` on the output shows exactly the intended
      revisions and nothing else

## Reference map

| Situation | Open |
|---|---|
| Writing a new document with `docx-js` — syntax, styles, lists, tables, images, page setup, common mistakes | [docx-js.md](references/docx-js.md) |
| Editing raw OOXML, the Document library, tracked-change patterns, comments, relationships, entity handling | [ooxml.md](references/ooxml.md) |

Executable helpers: `scripts/merge_runs.py`, `scripts/comment.py`,
`scripts/accept_changes.py`, `scripts/office/validate.py`,
`scripts/office/soffice.py`, `scripts/unpack.py`, `scripts/pack.py`.

## Output format

For any authoring or redlining request, deliver the file plus:

```markdown
# <Document> — Word delivery note

## File
Path, format (`.docx`/`.dotx`), page count.

## Route taken
Which approach from the workflow table, and why.

## Changes made
Table: Location | Change | Tracked? (w:ins/w:del/comment/none)

## Verification
`validate.py` result, rendered page count, `pandoc` spot-checks performed.

## Open items
Unresolved revisions, comments left for the user, anything Word may reflow
differently on their machine (fonts, field updates).
```

For a redline, list every change with its section anchor so the reviewer can walk
them in order without diffing the XML.
