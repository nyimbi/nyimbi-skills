---
name: sox-testing
description: Plan, execute, and document SOX 404 control testing end to end. Use when planning quarterly or annual SOX 404 testing, scoping significant accounts and assertions, identifying controls to test, pulling a sample for a control (revenue, P2P, ITGC, close, payroll, treasury, fixed assets, inventory, entity-level, journal entries), determining sample sizes, generating sample selections, building testing workpaper templates, evaluating evidence, classifying control deficiencies (deficiency / significant deficiency / material weakness), aggregating deficiencies, or preparing for internal or external audits.
argument-hint: "<control area> [period]"
---

# SOX 404 Control Testing

> If you see `~~connector` placeholders, that tool is optional — skip the step if it is not connected.

**Important**: This skill assists with SOX compliance workflows but does not provide audit or legal advice. All testing workpapers and assessments should be reviewed by qualified financial professionals before use in audit documentation. While "significance" and "materiality" are context-specific concepts ultimately assessed by auditors, this skill assists professionals in creating and evaluating effective internal controls and audit documentation.

Generate control matrices, sample selections, testing workpapers, and deficiency assessments for SOX 404 internal control over financial reporting (ICFR).

## Usage

```
/sox <control-area> <period>
```

- `control-area` — `revenue-recognition` · `procure-to-pay`/`p2p` · `payroll` · `financial-close` · `treasury` · `fixed-assets` · `inventory` · `itgc` · `entity-level` · `journal-entries` · or a specific control ID/name
- `period` — testing period (e.g., `2024-Q4`, `2024`, `2024-H2`)

## Methodology overview

SOX 404 requires management to assess ICFR effectiveness:

1. **Scoping** — identify significant accounts and relevant assertions
2. **Risk assessment** — evaluate risk of material misstatement per significant account
3. **Control identification** — document controls addressing each risk
4. **Testing** — test design and operating effectiveness of key controls
5. **Evaluation** — assess whether deficiencies exist and their severity
6. **Reporting** — document the assessment and any material weaknesses

**Scoping significant accounts.** An account is significant if there is more than a remote likelihood it could contain a misstatement that is material (individually or in aggregate).

- *Quantitative*: balance exceeds the materiality threshold (typically 3–5% of a key benchmark); high transaction volume; subject to significant estimates or judgment.
- *Qualitative*: complex accounting (revenue, derivatives, pensions); fraud susceptibility (cash, revenue, related party); prior misstatements or audit adjustments; significant management judgment; new or significantly changed process.

**Assertions by account type:**

| Account type | Key assertions |
|---|---|
| Revenue | Occurrence, completeness, accuracy, cut-off |
| Accounts receivable | Existence, valuation (allowance), rights |
| Inventory | Existence, valuation, completeness |
| Fixed assets | Existence, valuation, completeness, rights |
| Accounts payable | Completeness, accuracy, existence |
| Accrued liabilities | Completeness, valuation, accuracy |
| Equity | Completeness, accuracy, presentation |
| Financial close/reporting | Presentation, accuracy, completeness |

**Assertions (CEAVOP)** — **C**ompleteness (all transactions recorded) · **E**xistence/Occurrence (they actually happened) · **A**ccuracy (amounts correct) · **V**aluation (properly valued) · **O**bligations/Rights · **P**resentation/Disclosure.

**Design vs operating effectiveness.** *Design*: is the control properly designed to prevent or detect a material misstatement in the relevant assertion? — evaluated via walkthroughs (trace a transaction end-to-end; confirm the control sits at the right point and addresses the identified risk), at least annually or when processes change. *Operating*: did it actually operate as designed throughout the period? — evaluated via testing (inspection, observation, re-performance, inquiry) over a sufficient sample covering the full period of reliance.

## Workflow

### 1. Identify controls to test

Present the control matrix:

| Control # | Control description | Type | Frequency | Key/Non-key | Risk | Assertion |
|-----------|---------------------|------|-----------|-------------|------|-----------|
| [ID] | [description] | Manual/Automated/IT-dependent | Daily…Annual | Key | High/Med/Low | [CEAVOP] |

Control types: **automated** (system-enforced, no manual intervention) · **manual** (performed by people with judgment) · **IT-dependent manual** (manual, relying on system-generated data — also test the IPE: completeness and accuracy of the underlying report).

### 2. Determine sample size

| Control frequency | Expected population | Low risk | Moderate risk | High risk |
|-------------------|--------------------|----------|---------------|-----------|
| Annual | 1 | 1 | 1 | 1 |
| Quarterly | 4 | 2 | 2 | 3 |
| Monthly | 12 | 2 | 3 | 4 |
| Weekly | 52 | 5 | 8 | 15 |
| Daily | ~250 | 20 | 30 | 40 |
| Per-transaction (small pop.) | < 250 | 20 | 30 | 40 |
| Per-transaction (large pop.) | 250+ | 25 | 40 | 60 |

Increase for: higher inherent risk; sole control for a significant risk (no redundancy); prior-period deficiency; new control (not previously tested); external auditor reliance on management testing.

### 3. Generate the sample selection

**Random** (default for transaction-level controls, large populations): define the population, number items sequentially, select with a random number generator, no bias. Statistically valid and defensible, but may miss high-risk items.

**Systematic** (sequential populations, even period coverage): interval = population ÷ sample size; random start within the first interval; every Nth item. (Population 1,000, sample 25 → interval 40; random start 17 → items 17, 57, 97…) Periodic patterns in the population could bias results.

**Targeted/judgmental** (risk-based supplement; primary when the population is small or highly varied): items with risk characteristics — high dollar amount, unusual/non-standard, period-end (cut-off), related party, manual/override, new vendor/customer. Document the rationale for each. Not statistically representative.

**Haphazard** (only when random is impractical — no sequential listing — and the population is homogeneous): no pattern, spread across the full period, guard against unconscious bias. Not statistically valid.

Present the sample:

```
SAMPLE SELECTION
Control: [ID] — [description]        Period: [period]
Population: [N] items, $[total]      Sample size: [N]
Selection method: [Random/Systematic/Targeted]

| # | Date | Ref/ID | Amount | Basis |
```

### 4. Create the testing workpaper

```
SOX CONTROL TESTING WORKPAPER
==============================
Control #: [ID]
Control Description: [full description]
Control Owner: [role — tester to fill]
Control Type: [Manual/Automated/IT-Dependent Manual]
Frequency: [how often]                Key Control: [Y/N]
Relevant Assertion(s): [CEAVOP]       Testing Period: [period]

TEST OBJECTIVE:
To determine whether [control] operated effectively throughout the testing period.

TEST PROCEDURES:
1. [inspect/examine/re-perform step]
2. [evidence to obtain]
3. [comparison/verification]
4. [completeness of performance]
5. [timeliness of performance]

EXPECTED EVIDENCE:
- [document type 1]
- [document type 2]
- [document type 3]

TEST RESULTS:
| # | Ref | P1 | P2 | P3 | Result | Exception? | Notes |
|---|-----|----|----|----|--------|------------|-------|

EXCEPTIONS NOTED:
| # | Description | Root cause | Compensating control | Impact |

CONCLUSION:
[ ] Effective — no exceptions
[ ] Effective with exceptions — exceptions are isolated
[ ] Deficiency
[ ] Significant Deficiency
[ ] Material Weakness

Tested by: ________ Date: ____   Reviewed by: ________ Date: ____
```

Workpaper documentation must cover: **control identification** (ID, description, who/what/when, type, frequency, risk + assertion addressed) · **test design** (objective, procedures, expected evidence, selection methodology and rationale) · **test execution** (population description and size, selection details, per-item results with specific evidence examined, full exception descriptions) · **conclusion** (assessment, basis, impact of exceptions, compensating controls considered) · **sign-off** (tester and reviewer, names and dates).

**Pre-built test steps by area:**

*Revenue recognition* — sales order approval/authorization; delivery or performance evidence; recognition timing vs contract terms; pricing accuracy to contract/price list; credit memo approval and validity.

*Procure to pay* — PO approval and authorization limits; three-way match (PO, receipt, invoice); vendor master data change controls; payment approval and segregation of duties; duplicate payment prevention.

*Financial close* — reconciliation completeness and timeliness; journal entry approval and SoD; management review of financial statements; consolidation and elimination entries; disclosure checklist completion.

*ITGC* — user access provisioning/de-provisioning; privileged access reviews; change management approval and testing; batch job monitoring and exception handling; backup and recovery.

### 5. Evaluate the evidence

**Sufficient:** screenshots of system-enforced controls; signed/initialed approvals; email approvals with identifiable approver and date; system audit logs (who/when); re-performed calculations that match; dated observation notes (location, observer).

**Insufficient:** verbal confirmation alone (corroborate); undated documents; no identifiable performer/approver; generic reports without date/time stamps; "per discussion with [name]" without documentation.

**Automated controls:** test the design (configuration enforces the control as intended); if configuration is unchanged, one test plus effective change-management ITGCs typically suffices for the period — re-test if the system changed.

### 6. Classify deficiencies

**Deficiency** — design or operation does not allow management or employees, in the normal course, to prevent or detect misstatements on a timely basis. Evaluate: likelihood of misstatement; magnitude of potential misstatement; compensating controls.

**Significant deficiency** — less severe than a material weakness yet important enough to merit attention by those charged with governance. Indicators: potential misstatement more than inconsequential but less than material; likelihood more than remote but less than reasonably possible; a key control not fully mitigated by compensating controls; individually minor deficiencies that together represent a significant concern.

**Material weakness** — reasonable possibility that a material misstatement will not be prevented or detected on a timely basis. Indicators: fraud by senior management (any magnitude); restatement of previously issued financials; auditor-identified material misstatement the controls missed; ineffective audit committee oversight; deficiency in a pervasive entity-level or ITGC control.

**Aggregation** — individually non-significant deficiencies can be significant in combination: identify deficiencies in the same process or assertion, evaluate the combined effect on material misstatement, consider whether compensating-control deficiencies exacerbate others, and document the analysis and conclusion.

**Remediation** (per deficiency): root cause analysis (design gap, execution failure, staffing, training, system) → remediation plan (redesign, training, system enhancement, added review) → timeline → owner → validation (how/when the remediated control will be re-tested).

## Reference: common control types

**ITGCs.** *Access*: provisioning approval; timely de-provisioning of terminations; privileged access restricted and monitored; periodic access recertification; password policy; SoD enforcement. *Change management*: documented approved change requests; non-production testing before promotion; dev/prod separation; documented emergency change procedure; post-implementation validation. *Operations*: batch job monitoring; tested backups and restores; availability/performance monitoring; incident escalation; DR planning and testing.

**Manual controls.** Management review of financials and key metrics; supervisory approval of JEs above threshold; three-way match verification; reconciliation preparation and review; physical inventory observation; vendor master change approval; customer credit approval. Test attributes: right person (authority)? timely? evidence of review (signature, initials, email, log)? sufficient information to review effectively? exceptions addressed?

**Automated controls.** System-enforced approval workflows; automated three-way match (payment blocked on mismatch); duplicate payment detection; credit limit enforcement; automated calculations (depreciation, amortization, interest, tax); system-enforced SoD; input validation (required fields, format, range); automated reconciliation matching.

**IT-dependent manual controls.** Management review of a system-generated exception report; aging-report review to assess reserves; reconciliation from a system trial balance; approval of system-workflow-identified transactions. Test the manual control **and** the IPE.

**Entity-level controls.** Tone at the top/code of conduct; risk assessment process; audit committee oversight; internal audit function; fraud risk assessment and anti-fraud program; whistleblower hotline; management monitoring; financial reporting competence; period-end close process (GAAP compliance reviews). They can mitigate but typically cannot replace process-level controls; ineffective entity-level controls (audit committee, tone at the top) are strong material-weakness indicators; effective ones may reduce process-level testing extent.

**Workpaper organization:**

```
SOX Testing/
└── [Year]/
    ├── Scoping and Risk Assessment/
    ├── Revenue Cycle/            (Control Matrix · Walkthroughs · Workpapers · Evidence)
    ├── Procure to Pay/
    ├── Payroll/
    ├── Financial Close/
    ├── Treasury/
    ├── Fixed Assets/
    ├── IT General Controls/
    ├── Entity Level Controls/
    └── Summary and Conclusions/  (Deficiency Evaluation · Management Assessment)
```

## Output

Provide:
1. Control matrix for the selected area
2. Sample selections with methodology documentation
3. Testing workpaper templates with pre-populated test steps
4. Results documentation template
5. Deficiency evaluation (if exceptions are identified)
6. Suggested remediation actions for any noted deficiencies
