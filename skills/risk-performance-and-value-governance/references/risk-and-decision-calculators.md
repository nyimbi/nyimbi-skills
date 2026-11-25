# Risk and Decision Calculators

## Risk scoring with velocity

```bash
python3 scripts/risk_matrix.py --config risks.json
```

Config: each risk's likelihood (1–5), impact (1–5), velocity (1–5), and current mitigation.
Velocity is how fast the risk could materialise: 1 years, 5 weeks.

Output: a score per risk and a monitoring cadence. Two risks with the same likelihood ×
impact need different cadences when one can hit in weeks and the other in years.

## Decision-tree expected value

```bash
python3 scripts/decision_tree_ev.py --config scenarios.json
```

Config: strategic options, each with scenarios (name, probability, payoff). Probabilities
within an option must sum to 1.0.

Output: expected value per option and the maximin choice when it differs from the best-EV
choice. A high EV with a catastrophic worst case is a different decision from a high EV with
a bounded downside.

## Value realization

The backward-looking check. For each benefit promised in the business case:

| Field | What to record |
|---|---|
| Promise | the original benefit, with its source |
| Baseline | the metric before the change |
| Realised | the metric after, same definition, same period |
| Bridge | price, volume, mix, productivity, one-off |
| Verdict | realised, partially realised, not realised |
| Cause | what differed from the case |
| Action | keep, fix, stop |

Do not let a new baseline quietly replace the old one. If the definition changed, restate the
old number under the new definition and show both.

## Decision rules

- A risk register without owners and review dates is a list.
- A risk with a velocity of 5 needs a trigger, not a quarterly review.
- A decision tree whose probabilities are invented is a scenario exercise; label it `[A]`.
- A value-realization review that only reports the aggregate hides which promise failed.
- A benefit that cannot be measured was not a benefit; it was a hope.

## Pitfalls

- Scoring impact without a dollar or time range.
- Treating mitigation as done because a plan exists.
- Comparing realised to the latest forecast rather than the approved case.
- Netting a miss in one driver against an overperformance in another without showing both.
