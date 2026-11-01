# Strategic Options Playbook

Generates a small set of genuinely distinct options, compares them against the
decision's own criteria, and recommends a path with trade-offs visible. Run at **Full
Case** depth (see
[../../strategy-diagnosis-and-framing/SKILL.md](../../strategy-diagnosis-and-framing/SKILL.md));
**Client Deliverable** for board or IC audiences.

## When to use

- Before committing to a strategy: path selection, growth choices, market-entry modes,
  build-buy-partner, sequencing questions
- "What are our options?" / "Is this a false binary?" / "Which way should we go?"
- The options themselves are not yet written — once they are, quantification belongs
  in [business-case-builder.md](business-case-builder.md)

## Approach

Develop 2–4 options that are *meaningfully* different — different mechanisms, not
different dose. Compare them against criteria that reflect this decision (economics,
feasibility, risk, strategic fit), not generic attractiveness. Weighting, ownership,
and challenge techniques come from
[frameworks-decision.md](frameworks-decision.md): decision matrix for scoring, RAPID
for who decides, pre-mortem and inversion for stress-testing.

## Workflow

1. **Clarify the decision and constraints**: what is being decided, by whom, when, and
   what is off the table.
2. **Generate mutually distinct options** — include "do nothing / maintain course" as
   an explicit option, plus hybrids or sequencing only when they change the mechanism.
3. **Define decision criteria** and their weights from the decision, not from a
   generic scorecard; state the threshold an option must clear.
4. **Assess each option** on attractiveness, feasibility, risk, economics, and
   strategic fit — economics are directional here and rigorous in
   [business-case-builder.md](business-case-builder.md).
5. **Stress-test**: apply devil's advocate and pre-mortem to the frontrunner *and* the
   runner-up — an option that only survives because it was never examined is a
   default, not a recommendation.
6. **Recommend** a path with trade-offs visible, state what must be true for it to
   hold, and list the evidence (next tests) needed before committing.

## Output format

```markdown
# Strategic Options

## Decision
[Decision being made.]

## Options
| Option | Description | Upside | Trade-Off | What Must Be True |
|---|---|---|---|---|

## Evaluation
| Criteria | Option A | Option B | Option C |
|---|---|---|---|

## Recommendation
[Preferred option and rationale.]

## Next Tests
[Evidence needed before committing.]
```

## Quality bar

Playbook checks on top of the SKILL.md checklist:

- [ ] Options differ in mechanism, not just in magnitude or timeline
- [ ] "Do nothing" is present and evaluated with the same rigor
- [ ] Criteria and weights come from this decision and are shown
- [ ] Trade-offs are stated for the recommended option, not only for rejected ones
- [ ] "What must be true" and next tests are specific enough to run
