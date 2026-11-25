# Stakeholder Grid and Coalition Math

## The grid

For each stakeholder: power (1–5), interest (1–5), stance (champion, supportive, neutral,
skeptical, opposed), and what they need to say yes.

| Power / interest | Engagement |
|---|---|
| High power, high interest | manage closely; co-design the decision |
| High power, low interest | keep satisfied; short, decision-focused updates |
| Low power, high interest | keep informed; use as evidence and execution capacity |
| Low power, low interest | monitor; do not spend political capital |

## Coalition math

```bash
python3 scripts/power_interest_grid.py --config stakeholders.json
```

The calculator maps the grid and sums the power held by supporters against the power held by
opponents and skeptics. A grid full of green dots can still lose if the real power sits with
two skeptics.

If supporters do not outnumber opponents in power, the plan is not ready for the meeting.
Either convert a high-power skeptic, reduce the decision's scope, or change the decision.

## Decision memo audience

- The memo's first paragraph is written for the highest-power skeptic, not the friendliest
  supporter.
- Answer their strongest objection in the memo; do not leave it for the meeting.
- Give the approver a clear ask, a deadline and a default if they do nothing.
- Pre-wire the decision one-to-one before the group meeting. The meeting is for confirmation,
  not surprise.

## Pitfalls

- Mapping titles rather than actual influence.
- A supporter who is supportive but will not spend capital or reputation.
- An opponent who is not named because the relationship is uncomfortable.
- A coalition that is a majority in headcount and a minority in power.
- A memo that argues the case but never states the ask.
