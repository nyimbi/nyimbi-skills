---
name: pdf-processing
description: >-
  Use this skill whenever the user wants to manipulate PDF files. Triggers include
  "merge these PDFs", "split this PDF by page range", "rotate the pages", "fill this
  form", "OCR this scan so it is searchable", "extract the tables from this report",
  "password-protect this document", "add a watermark", "pull the images out", and
  "combine these scans into one file". It covers reading text, tables, and metadata;
  merging, splitting, rotating, cropping, and watermarking; creating new PDFs with
  reportlab; filling AcroForm fields and drawing text annotations onto non-fillable
  forms; encrypting and decrypting; OCR of scanned pages; and extracting embedded
  images. Use it even when a .pdf is only the input and the extracted content will be
  reused elsewhere. Do not use for deciding what the document should say (see
  writing-and-internal-communications), for authoring or editing Word, PowerPoint, or
  Excel files (see word-document-authoring, presentation-authoring,
  spreadsheet-authoring), or for generic file conversion and media handling that is
  not PDF-specific (see file-media-and-engagement-tools).
---

# PDF Processing

A PDF is a structured object stream, not a text file. Almost every botched PDF job
comes from the same four mistakes: writing a transform that drops the page tree,
extracting text from a scan and calling it done, filling a form with coordinates
measured in the wrong space, and delivering a file nobody has actually opened. This
skill exists so the output is a PDF that renders correctly on the first try.

## When to use

- Combining, splitting, extracting, reordering, or rotating pages in one or more PDFs
- Reading text, tables, metadata, or embedded images out of a PDF
- Filling AcroForm fields, or writing values into a form that has no fields
- Making a scanned or image-only PDF searchable through OCR
- Creating a new PDF — report, certificate, invoice, multi-page document
- Encrypting, decrypting, or password-protecting a PDF; adding a watermark or header stamp
- Repairing, optimizing, linearizing, or cropping a damaged or oversized PDF
- Turning a PDF into page images for inspection or verification

**Do not use for** — `writing-and-internal-communications` when the question is what
the document should say rather than how to package it as a PDF;
`word-document-authoring` when the deliverable is a `.docx` or the source is a Word
file that needs tracked changes; `file-media-and-engagement-tools` when the ask is a
generic format conversion (CSV→JSON, video, images) with no PDF in the pipeline;
`spreadsheet-authoring` when the real deliverable is a workbook of extracted tables
rather than the PDF itself.

## Workflow

1. **Confirm the job and the route.** Read the input(s): page count, whether the pages
   carry a text layer, whether they are encrypted, whether they contain AcroForm
   fields. Two probes answer almost everything:

   ```bash
   qpdf --show-encryption input.pdf            # encryption status, permissions
   pdffonts input.pdf                          # no fonts => image-only => OCR route
   ```

   Then pick the route — the rest of the workflow is that route:

   | Task | Tool | Entry point |
   |---|---|---|
   | Merge, split, extract, rotate, reorder | `pypdf` | `PdfWriter.add_page()` |
   | Same, from the shell, or decrypt | `qpdf` | `qpdf --empty --pages …` |
   | Extract text or tables | `pdfplumber` | `page.extract_text()` / `page.extract_tables()` |
   | OCR an image-only scan | `pytesseract` + `pdf2image` | render, then `image_to_string` |
   | Create a new PDF | `reportlab` | Canvas (positioned) or Platypus (flowing) |
   | Fill a form | `scripts/` + `references/forms.md` | see step 6 |
   | Advanced: pypdfium2, pdf-lib, batch, troubleshooting | — | `references/reference.md` |

2. **Read before you transform.** Never edit a PDF you have not inspected. Extract the
   metadata and the page inventory first so you can prove afterwards that nothing was
   lost:

   ```python
   from pypdf import PdfReader
   r = PdfReader("input.pdf")
   print(len(r.pages), r.metadata.title, r.metadata.author)
   ```

3. **Transform with `pypdf` (or `qpdf` for shell work).** Merge, split, rotate, and
   watermark all follow the same shape — build a `PdfWriter`, add pages, write once:

   ```python
   from pypdf import PdfReader, PdfWriter
   w = PdfWriter()
   for f in ["doc1.pdf", "doc2.pdf"]:
       for page in PdfReader(f).pages:
           w.add_page(page)
   with open("merged.pdf", "wb") as out:
       w.write(out)
   ```

   Rotate with `page.rotate(90)` before adding; watermark by merging one page onto
   every page with `page.merge_page(watermark)`. For page ranges, rotation, and
   decryption in one pass, prefer `qpdf input.pdf --pages . 1-5 -- out.pdf` and
   `qpdf --password=… --decrypt in.pdf out.pdf`.

4. **Extract text and tables.** Use `pdfplumber` page by page; when the result is
   tabular, go straight to DataFrames so the structure survives:

   ```python
   import pandas as pd, pdfplumber
   frames = []
   with pdfplumber.open("report.pdf") as pdf:
       for page in pdf.pages:
           for table in page.extract_tables():
               if table:
                   frames.append(pd.DataFrame(table[1:], columns=table[0]))
   if frames:
       pd.concat(frames, ignore_index=True).to_excel("tables.xlsx", index=False)
   ```

   If `pdffonts` showed no fonts, skip extraction and go to OCR instead — text
   extracted from a scan without OCR is empty, not partial.

5. **OCR image-only pages.** Render each page to an image, then run Tesseract per page
   and keep the page boundaries in the output:

   ```python
   import pytesseract
   from pdf2image import convert_from_path
   text = ""
   for i, image in enumerate(convert_from_path("scanned.pdf"), 1):
       text += f"Page {i}:\n{pytesseract.image_to_string(image)}\n\n"
   ```

   To make the scan searchable rather than merely extracted, write the OCR text back
   as an invisible text layer over the original image pages — that is the difference
   between "I read it" and "the user can now search it".

6. **Fill forms by following `references/forms.md` exactly.** It is a step-ordered
   procedure with its own scripts, not a recipe to improvise:
   - `scripts/check_fillable_fields.py` decides the branch — AcroForm fields or
     annotations.
   - Fillable: `scripts/extract_form_field_info.py` → `field_values.json` →
     `scripts/fill_fillable_fields.py`.
   - Non-fillable: try `scripts/extract_form_structure.py` first (exact PDF
     coordinates), fall back to visual estimation from rendered PNGs, always run
     `scripts/check_bounding_boxes.py` before filling, then fill with annotations.
     Two implementations of that last step ship — prefer
     `scripts/skills-fill_pdf_form_with_annotations.py`, which auto-detects whether
     `fields.json` carries `pdf_width`/`pdf_height` structure coordinates or
     `image_width`/`image_height` pixel coordinates; `scripts/awesome-fill_pdf_form_with_annotations.py`
     handles image coordinates only.

7. **Create new PDFs with `reportlab`, not by hand-assembling objects.** Canvas for
   positioned output, Platypus when content should flow across pages. Two footguns
   that silently corrupt the render:
   - Never use Unicode subscript/superscript characters (`₀`, `²`) in reportlab —
     the built-in fonts lack the glyphs and they render as black boxes. Use
     `<sub>…</sub>` / `<super>…</super>` inside `Paragraph`, and on canvas-drawn text
     adjust the font size and y-offset manually.
   - One `Paragraph` per block; `\n` inside a run is not a line break.

8. **Verify by rendering the output, not by reading your own code.** Convert the
   result back to images and look at every changed page:

   ```bash
   python scripts/convert_pdf_to_images.py output.pdf verify_images/
   ```

   Check page count, text position, form values, and watermark placement against the
   input before you hand anything over.

## Quality bar

- [ ] Page count and page order of the output match the requested operation exactly;
      no page silently dropped during merge, split, or rotate
- [ ] Text extracted from a scanned PDF came from OCR — verified by `pdffonts` or an
      eyeballed page render, never assumed
- [ ] Encrypted inputs were decrypted only with the password the user supplied, and
      the output's encryption state is what was asked for (test-open it)
- [ ] Form fills were validated with `scripts/check_bounding_boxes.py` first and
      visually confirmed on a rendered page afterwards — no value in the wrong field,
      no text outside its box
- [ ] Coordinates in one `fields.json` are in one coordinate system
      (`pdf_width`/`pdf_height` **or** `image_width`/`image_height`), never mixed
- [ ] Generated PDFs contain no tofu glyphs: no Unicode sub/superscripts, no
      characters missing from the font in use
- [ ] Output opens in a real viewer without a repair prompt; `qpdf --check` is clean
- [ ] Metadata (title/author) is preserved on transforms unless the user asked to
      scrub it
- [ ] Extracted tables were spot-checked against the source page for header alignment
      and row count

## Reference map

| Situation | Open |
|---|---|
| Filling a PDF form — AcroForm fields, annotation fallback, coordinate systems, validation order | [forms.md](references/forms.md) |
| Advanced work — pypdfium2 rendering, pdf-lib/JS, poppler and qpdf power flags, batch runs, cropping, troubleshooting | [reference.md](references/reference.md) |

Executable helpers for the form workflow live in `scripts/` — read `forms.md` first
to learn which script runs in which order, then run it from the skill root.

## Output format

Deliver the transformed PDF plus a short report:

```markdown
# <Task> — PDF operation report

## Inputs
File | Pages | Encrypted | Text layer | Forms

## Operation
What was done, in order, with the tool used for each step.

## Output
Path, page count, and how it was verified (rendered page count, `qpdf --check`,
spot-checked fields).

## Findings
Anything the user should know: missing fonts, existing PDF errors, permissions
carried over, pages that needed OCR, form fields that could not be filled.

## Residual issues
What is not perfect and what would fix it.
```

For a form fill, add the field-by-field table (`field_id`, label, value applied,
verification status) so the user can audit every entry without opening a diff tool.
