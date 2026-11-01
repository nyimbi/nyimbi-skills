# Invoice and Receipt Organization

Purpose: read a messy folder of invoices and receipts, extract the fields that
matter, rename consistently, file them by a stated scheme, and hand the
accountant a CSV. This is the financial-documents track of
`file-media-and-engagement-tools`.

PDF parsing and field extraction on their own are owned by
`../pdf-processing/`; this track owns the organizing workflow around them.

## Scan

```bash
find . -type f \( -name "*.pdf" -o -name "*.jpg" -o -name "*.png" \) -print
```

Report: total files, formats (PDF invoices, scanned receipts, screenshots, email
attachments, bank statements), discernible date range, and current organization.
Confirm the folder and the grouping scheme before renaming anything.

## Extraction

**PDF invoices** — pull text, then match common markers:

| Field | Markers |
|---|---|
| Date | `Invoice Date:`, `Date:`, `Issued:` |
| Number | `Invoice #:`, `Invoice Number:` |
| Vendor | usually the topmost organisation name |
| Amount | `Amount Due:`, `Total:`, `Amount:` |
| Description | `Description:`, `Service:`, `Product:` |

**Image receipts** — read visible text: vendor (top), date (common formats),
total amount.

**Fallbacks** when a file is unclear: filename clues, then file creation or
modification date — and flag it for manual review rather than guessing a
critical field. Anything missing a date or vendor goes to a `Needs Review`
folder, not into the filed set.

## Grouping scheme (choose once, state it)

By vendor (Adobe/, Amazon/, Stripe/) · by expense category (Software/, Office/,
Travel/) · by period (2024/Q1/) · by tax category (Deductible/, Personal/) ·
custom. Default when unspecified: `Year/Category/Vendor`.

## Filename standard

```
YYYY-MM-DD Vendor - Invoice - Description.ext
2024-03-15 Adobe - Invoice - Creative Cloud.pdf
2024-01-10 Amazon - Receipt - Office Supplies.jpg
```

Rules: hyphens only (strip other special characters), vendor capitalised
properly, description concise but meaningful, `YYYY-MM-DD` so names sort
chronologically, original extension preserved.

## Filing

Show the plan (tree + 3-4 before/after examples) and get approval, then:

```bash
mkdir -p "Invoices/2024/Software/Adobe"
cp "invoice_adobe_march.pdf" "Invoices/2024/Software/Adobe/2024-03-15 Adobe - Invoice - Creative Cloud.pdf"
```

**Copy by default, move only if asked** — originals stay untouched unless the
user opts in.

## Summary CSV

```csv
Date,Vendor,Invoice Number,Description,Amount,Category,File Path
2024-03-15,Adobe,INV-12345,Creative Cloud,52.99,Software,Invoices/2024/Software/Adobe/2024-03-15 Adobe - Invoice - Creative Cloud.pdf
```

This is the artifact the accountant and the accounting import consume, so its
rows must match the files that were actually filed.

## Close-out

Processed count, date range, sum of amounts (when extracted), unique vendors,
the resulting tree with file counts, files created (folder, `invoice-summary.csv`,
`originals/`), the Needs Review list, and next steps (review the CSV, clear the
review folder, import to accounting, set up auto-filing for new receipts).

## Quality gates for this track

- Grouping scheme confirmed before the first rename
- Every filed file has a complete standard name; incomplete ones are in Needs Review, never guessed
- Originals preserved (copy, not move) unless the user asked otherwise
- CSV rows equal the files on disk — no row without a file, no filed file without a row
- Amounts, dates, and vendors come from the document, not the filename, unless explicitly used as a documented fallback
- Plan shown and approved before bulk changes
