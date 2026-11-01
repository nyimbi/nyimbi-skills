---
name: journal-entry
description: Prepare journal entries with proper debits, credits, and supporting documentation for month-end close. Use when booking month-end accruals (AP, payroll, prepaid), recording depreciation or amortization, posting revenue recognition or deferred revenue adjustments, handling any manual journal entry, or documenting an entry for audit review.
argument-hint: "<entry type> [period]"
---

# Journal Entry Preparation

> If you see `~~connector` placeholders, that source is optional — skip the step when it is not available and ask the user for the data instead.

**Important**: This skill assists with journal entry workflows but does not provide financial advice. All entries should be reviewed by qualified financial professionals before posting.

Prepare journal entries with proper debits, credits, supporting detail, and review documentation.

## Entry Types

- `ap-accrual` — Accounts payable accruals for goods/services received but not yet invoiced
- `fixed-assets` — Depreciation and amortization entries for fixed assets and intangibles
- `prepaid` — Amortization of prepaid expenses (insurance, software, rent, etc.)
- `payroll` — Payroll accruals including salaries, benefits, taxes, and bonus accruals
- `revenue` — Revenue recognition entries including deferred revenue adjustments

Period is the accounting period (e.g., `2024-12`, `2024-Q4`, `2024`).

## Workflow

### 1. Gather Source Data

If ~~erp or ~~data warehouse is connected:
- Pull the trial balance for the specified period
- Pull subledger detail for the relevant accounts
- Pull prior period entries of the same type for reference
- Identify the current GL balances for affected accounts

If no data source is connected:
- Ask the user to provide trial balance or GL balances for affected accounts, subledger detail or supporting schedules, and (optionally) prior period entries for reference. The user can also paste trial balance data or upload a spreadsheet.

### 2. Calculate the Entry

**AP Accrual**
- Identify goods/services received but not invoiced by period end
- Calculate accrual amounts from PO receipts, contracts, or estimates
- Sources: open purchase orders with confirmed receipts; contracts with services rendered but unbilled; recurring vendor arrangements (utilities, subscriptions, professional services); employee expense reports submitted but not yet processed
- Debit: Expense accounts (or asset accounts for capitalizable items)
- Credit: Accrued liabilities
- Key considerations: reverse in the following period (auto-reversal recommended); use a consistent estimation methodology period over period; document the basis for estimates (PO amount, contract terms, historical run-rate); track actual vs accrual to refine future estimates

**Fixed Assets**
- Pull the fixed asset register or depreciation schedule
- Calculate period depreciation by asset class and method:
  - Straight-line: (Cost - Salvage) / Useful life — most common for financial reporting
  - Declining balance: fixed rate applied to net book value
  - Units of production: based on actual usage vs total expected
- Debit: Depreciation expense (by department/cost center)
- Credit: Accumulated depreciation
- Key considerations: verify new additions have correct useful life and method; check for disposals or impairments requiring write-off; keep book and tax depreciation tracking consistent

**Prepaid**
- Pull the prepaid amortization schedule
- Calculate the period amortization for each prepaid item (insurance, software licenses, prepaid rent, maintenance contracts, event deposits)
- Debit: Expense accounts (by type)
- Credit: Prepaid expense accounts
- Key considerations: maintain an amortization schedule with start/end dates and monthly amounts; review for items that should be fully expensed (immaterial amounts); check for cancelled contracts requiring accelerated amortization; add new prepaids to the schedule promptly

**Payroll**
- Calculate accrued salaries for days worked but not yet paid (working days in period vs pay period)
- Calculate accrued benefits (health, retirement contributions, PTO)
- Calculate employer payroll tax accruals (FICA, FUTA, health, 401k match)
- Calculate bonus accruals (plan terms: target amounts, performance metrics, payout timing)
- Debit: Salary expense, benefits expense, payroll tax expense (by department)
- Credit: Accrued payroll, accrued benefits, accrued payroll taxes, accrued bonus
- Key considerations: track PTO/vacation accrual liability if required by policy or jurisdiction

**Revenue**
- Review contracts and performance obligations
- Calculate revenue to recognize based on delivery/performance; adjust deferred revenue balances
- Recognize previously deferred revenue (Dr deferred revenue / Cr revenue); recognize with new receivable (Dr AR / Cr revenue); defer revenue received in advance (Dr cash/AR / Cr deferred revenue)
- Key considerations: follow the ASC 606 five-step framework; identify distinct performance obligations; determine transaction price including variable consideration; allocate price to performance obligations; recognize as/when obligations are satisfied; maintain contract-level detail for audit support

### 3. Generate the Journal Entry

Present the entry in standard format:

```
Journal Entry: [Type] — [Period]
Prepared by: [User]
Date: [Period end date]

| Line | Account Code | Account Name | Debit | Credit | Department | Memo |
|------|-------------|--------------|-------|--------|------------|------|
| 1    | XXXX        | [Name]       | X,XXX |        | [Dept]     | [Detail] |
| 2    | XXXX        | [Name]       |       | X,XXX  | [Dept]     | [Detail] |
|      |             | **Total**    | X,XXX | X,XXX  |            |      |

Supporting Detail:
- [Calculation basis and assumptions]
- [Reference to supporting schedule or documentation]

Reversal: [Yes/No — if yes, specify reversal date]
```

### 4. Documentation Requirements

Every journal entry should have:

1. **Entry description/memo** — clear, specific description of what the entry records and why
2. **Calculation support** — how amounts were derived (formula, schedule, source data reference)
3. **Source documents** — reference to underlying transactions or events (PO numbers, invoice numbers, contract references, payroll register)
4. **Period** — the accounting period the entry applies to
5. **Preparer identification** — who prepared the entry and when
6. **Approval** — evidence of review and approval per the authorization matrix
7. **Reversal indicator** — whether the entry auto-reverses and the reversal date

### 5. Approval Matrix

| Entry Type | Amount Threshold | Approver |
|-----------|-----------------|----------|
| Standard recurring | Any amount | Accounting manager |
| Non-recurring / manual | < $50K | Accounting manager |
| Non-recurring / manual | $50K - $250K | Controller |
| Non-recurring / manual | > $250K | CFO / VP Finance |
| Top-side / consolidation | Any amount | Controller or above |
| Out-of-period adjustments | Any amount | Controller or above |

*Thresholds should be set based on the organization's materiality and risk tolerance.*

### 6. Review Checklist

Before finalizing, verify:

- [ ] Debits equal credits (entry is balanced)
- [ ] Correct accounting period (not posting to a closed period)
- [ ] Account codes exist and are appropriate for the transaction
- [ ] Amounts are mathematically accurate with supporting detail
- [ ] Memo/description is clear and specific enough for audit
- [ ] Department/cost center/project coding is correct
- [ ] Entry is consistent with prior period treatment and accounting policies
- [ ] Reversal flag is set appropriately (accruals should auto-reverse)
- [ ] Supporting documentation is complete and referenced
- [ ] Entry is within the preparer's approval authority
- [ ] No duplicate of an existing entry
- [ ] No unusual or out-of-pattern amounts that need investigation

### 7. Common Errors to Check For

1. **Unbalanced entries** — debits do not equal credits (check manual entries)
2. **Wrong period** — posted to an incorrect or already-closed period
3. **Wrong sign** — debit entered as credit or vice versa
4. **Duplicate entries** — same transaction recorded twice (check before posting)
5. **Wrong account** — posted to an incorrect GL account (especially similar codes)
6. **Missing reversal** — accrual not set to auto-reverse, causing double-counting
7. **Stale accruals** — recurring accruals not updated for changed circumstances
8. **Round-number estimates** — suspiciously round amounts that may not reflect actual calculations
9. **Incorrect FX rates** — wrong exchange rate or date on foreign currency entries
10. **Missing intercompany elimination** — intercompany entries without corresponding elimination
11. **Capitalization errors** — expenses that should be capitalized, or vice versa
12. **Cut-off errors** — transactions recorded in the wrong period based on delivery/service date

## Output

Provide:
1. The formatted journal entry
2. Supporting calculations
3. Comparison to prior period entry of the same type (if available)
4. Any items flagged for review or follow-up
5. Instructions for posting (manual entry or upload format for the user's ERP)
