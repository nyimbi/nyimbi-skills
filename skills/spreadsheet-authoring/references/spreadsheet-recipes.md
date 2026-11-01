# Spreadsheet Recipes

Code patterns for reading, creating, and editing workbooks with pandas and openpyxl.
Open this when the SKILL.md workflow reaches "write the script" and you need the
exact API shape rather than the rule.

## Reading and analysing with pandas

```python
import pandas as pd

df = pd.read_excel('file.xlsx')                       # first sheet
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)   # dict of all sheets

df.head()                                             # preview
df.info()                                             # column types, nulls
df.describe()                                         # statistics

df.to_excel('output.xlsx', index=False)
```

Pandas options that prevent the common surprises:

```python
pd.read_excel('file.xlsx', dtype={'id': str})         # don't let ids become ints
pd.read_excel('file.xlsx', usecols=['A', 'C', 'E'])   # large files
pd.read_excel('file.xlsx', parse_dates=['date_column'])
df['flag'] = pd.notna(df['note'])                     # explicit null handling
```

## Creating a workbook with openpyxl

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
sheet = wb.active

sheet['A1'] = 'Hello'
sheet['B1'] = 'World'
sheet.append(['Row', 'of', 'data'])

sheet['B2'] = '=SUM(A1:A10)'                          # formula, not a computed total

sheet['A1'].font = Font(bold=True, color='FF0000')
sheet['A1'].fill = PatternFill('solid', start_color='FFFF00')
sheet['A1'].alignment = Alignment(horizontal='center')
sheet.column_dimensions['A'].width = 20

wb.save('output.xlsx')
```

## Editing an existing workbook

```python
from openpyxl import load_workbook

wb = load_workbook('existing.xlsx')                   # keeps formulas
sheet = wb.active                                      # or wb['SheetName']

for name in wb.sheetnames:
    print(f"Sheet: {name}", wb[name].max_row, wb[name].max_column)

sheet['A1'] = 'New Value'
sheet.insert_rows(2)
sheet.delete_cols(3)

new_sheet = wb.create_sheet('NewSheet')
new_sheet['A1'] = 'Data'

wb.save('modified.xlsx')
```

Load options:

```python
load_workbook('file.xlsx', data_only=True)   # cached values only — formulas gone
load_workbook('file.xlsx', keep_vba=True)    # required to preserve .xlsm macros
load_workbook('file.xlsx', read_only=True)   # large files, reading
```

## Merged cells, sheets, and references

```python
# Merged range: only the top-left anchor is writable
sheet.merge_cells('B2:D2')
sheet['B2'] = 'Merged title'          # correct
sheet['C2'] = 'nope'                  # MergedCell, read-only, raises

# Sheet name with a space must be quoted in a cross-sheet reference
sheet['B5'] = "='Assumptions Inputs'!$B$5"
```

## Formula patterns that survive recalculation

```python
sheet['B10'] = '=SUM(B2:B9)'                     # totals
sheet['C5']  = '=(C4-C2)/C2'                     # growth rate
sheet['D20'] = '=AVERAGE(D2:D19)'
sheet['E2']  = '=SUMIFS(D:D, A:A, "Q1", B:B, ">0")'
sheet['F2']  = '=INDEX(B:B, MATCH($A2, A:A, 0))' # lookup — not XLOOKUP
sheet['G2']  = '=IFERROR(F2/E2, 0)'
```

Post-2007 functions need the `_xlfn.` prefix because openpyxl writes the string
verbatim and Excel stores them prefixed: `_xlfn.TEXTJOIN`, `_xlfn.CONCAT`,
`_xlfn.IFS`, `_xlfn.SWITCH`, `_xlfn.MAXIFS`, `_xlfn.MINIFS`.

## recalc.py output shape

```json
{
  "status": "success",
  "total_errors": 0,
  "total_formulas": 42,
  "error_summary": {
    "#REF!": { "count": 2, "locations": ["Sheet1!B5", "Sheet1!C10"] }
  }
}
```

`status: "errors_found"` still exits 0 — read the JSON, not the exit code. A key
named `error` instead of `status` means nothing was recalculated at all.

## Off-by-one traps while scripting

Excel columns are letters and rows are 1-indexed: column 64 is `BL`, not `BK`, and
DataFrame row 5 lands on Excel row 6. Guard denominators before dividing, confirm every
referenced sheet name and range actually exists, and try the awkward inputs — zeros,
negatives, and very large values — before you call a formula finished.
