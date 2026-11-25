# Validation

## The ten dimensions

Score 1–5. State the weight before scoring; weights follow the business model, not taste.

| # | Dimension | 1 | 3 | 5 |
|---|---|---|---|---|
| 1 | Problem severity | nice to have | costs time or money | costs money, safety, status or sleep |
| 2 | Frequency | once a year | monthly | daily or weekly |
| 3 | Willingness to pay | no spend evidence | some adjacent spend | budget line already exists |
| 4 | Market size | niche with no expansion | credible wedge | wedge into a large adjacent market |
| 5 | Competition | crowded commodity | clear incumbents with gaps | weak or misaligned alternatives |
| 6 | Moat | none | workflow or data advantage | compounding network or switching cost |
| 7 | Founder/market fit | generic | relevant experience | unfair insight or access |
| 8 | Distribution | paid only | one viable channel | organic or embedded channel |
| 9 | Execution feasibility | needs a large team | 6–12 months | shippable by a small team in 90 days |
| 10 | Trust and regulation | blocked | licence or audit needed | low regulatory surface |

## Weights

Suggested starting weights; change them and say why.

| Business | Heavy weights |
|---|---|
| Consumer social | frequency, distribution, moat |
| B2B SaaS | severity, willingness to pay, distribution |
| Payments / identity | trust and regulation, severity, moat |
| Marketplace | liquidity, frequency, trust |
| Local-first AI tool | severity, execution feasibility, distribution |

## Evidence per score

A score without evidence is an assumption. For each dimension, record:

- The claim.
- The evidence: source, date, sample, or interview quote.
- The label: `[F]/[I]/[A]/[E]`.
- The confidence: high, medium, low.
- The cheapest test that would raise confidence.

## Decision

| Composite | Decision | What happens next |
|---|---|---|
| ≥ 4.0 | go | build the wedge; name the first 90-day milestone |
| 3.0–3.9 | hold | run one named test with a date; do not build the full product |
| < 3.0 | kill | record why; keep the evidence for the next idea |

Never let a high average hide a 1 on trust or distribution. A single hard constraint can kill
a otherwise strong idea. Print the lowest dimension beside the composite.

## Business Model Canvas

| Block | The question |
|---|---|
| Customer segments | Who, precisely, and who is not served? |
| Value proposition | What job, what outcome, what proof? |
| Channels | How do they find, buy and receive it? |
| Customer relationships | Self-serve, assisted, community, contract? |
| Revenue streams | What is charged, on what metric, how often? |
| Key resources | What must you own or control? |
| Key activities | What must you be good at? |
| Key partners | Who supplies the rail, licence or distribution? |
| Cost structure | Fixed, variable, and what scales with volume? |

## Unit economics

Run the calculator:

```bash
python3 ../strategic-choices-and-economics/scripts/unit_economics.py --config unit.json
```

State:

- CAC by channel.
- ARPU or average order value.
- Gross margin after variable cost.
- Monthly churn and the implied lifetime.
- CAC payback months.
- LTV:CAC, with the churn-decay assumption printed.

A payback longer than the runway is a kill condition, not a growth problem.

## Common failures

- Scoring the idea on a blank page instead of against the current alternative.
- Counting interest as willingness to pay.
- A TAM that requires a market that does not exist yet.
- A moat that is really a feature.
- A distribution plan that assumes a channel the founder does not have.
- A "hold" with no test, owner or date.
