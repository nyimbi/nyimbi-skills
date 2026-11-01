# Growth Barriers Playbook

Finds the binding constraint blocking growth and separates root cause from symptom. Run
at **Full Case** depth (see [SKILL.md](../SKILL.md)); **Client Deliverable** when the
diagnosis goes to leadership.

## When to use

- Growth is underperforming and leadership is debating symptoms: stalled new logos,
  revenue plateau, funnel drop-off, retention decay, sales-productivity stalls
- "Why are we not growing?" / "Where is the funnel breaking?"
- Market-side questions (is the market shrinking?) route to
  `../../market-and-competitive-intelligence/SKILL.md` instead

## Approach

Treat growth as a system, not a list of initiatives. Build the growth driver tree — a
MECE decomposition of the growth equation — quantify where momentum breaks, and isolate
the one or two constraints that actually bind. The profit/revenue tree templates in
[diagram-templates.md](diagram-templates.md) and the Revenue Tree walkthrough in
`../../strategic-choices-and-economics/references/frameworks-financial.md` are the
mechanical backing.

## Workflow

1. **Define target, baseline, and gap.** Target vs current trajectory, sized in units,
   not adjectives.
2. **Build the driver tree.** Decompose the growth equation (e.g. new = traffic ×
   conversion × ACV; growth = acquisition + retention + expansion) into MECE branches
   down to drivers you can measure.
3. **Gather signals per branch** across acquisition, activation, conversion, retention,
   expansion, pricing, and capacity — each with evidence and a confidence label.
4. **Locate the break.** Compare branches against benchmark, trend, and plan to find
   where the math stops working.
5. **Separate symptom from root cause.** Ask "why?" down the tree until the cause is
   something the organization controls. Label the chain `[F]`/`[I]` explicitly.
6. **Name the binding constraint and act.** One or two constraints max; every recommended
   action must trace to a diagnosed constraint, with a kill condition stating what data
   would flip the diagnosis.

## Output format

```markdown
# Growth Barrier Diagnosis

## Growth Gap
[Target, current trajectory, size of gap.]

## Driver Tree
[MECE breakdown of growth drivers.]

## Barrier Assessment
| Driver | Evidence | Impact | Confidence | Root Cause |
|---|---|---|---|---|

## Binding Constraint
[The constraint most limiting growth.]

## Recommended Actions
1. [Action — traces to the constraint, owner, deadline]
2. [Action — traces to the constraint, owner, deadline]
3. [Action — traces to the constraint, owner, deadline]
```

## Quality bar

Playbook checks on top of the SKILL.md checklist:

- [ ] The diagnosis starts from the growth equation, not an initiative list
- [ ] Exactly one or two binding constraints are named; the rest are ranked context
- [ ] Every barrier row shows evidence that separates cause from symptom
- [ ] Every recommended action links back to the diagnosed constraint
- [ ] Kill conditions state which data point would relocate the constraint
