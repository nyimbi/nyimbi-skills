# Finance and Deals

The calculators behind a business case, a pricing move, a portfolio decision, an acquisition
synergy case and a negotiation. All are dependency-free Python with JSON configs; read the
docstring at the top of each script for the full schema.

## Business case: NPV, IRR, payback

```bash
python3 scripts/npv_case.py --config case.json
```

Config: discount rate, initial investment (capex + working capital + one-time costs), and
per-year revenue, COGS %, opex. Output: annual cash flows, NPV, IRR, payback, and a revenue ×
discount-rate sensitivity grid.

Read the grid for the breakeven condition. "NPV of $3.3M at 10%" is not a case until you can
say where it turns negative.

## Unit economics

```bash
python3 scripts/unit_economics.py --config unit.json
```

Config: CAC, monthly revenue per customer, gross margin %, monthly churn by month, annual
discount rate. Output: contribution margin, cumulative discounted LTV, LTV:CAC, CAC payback,
month-by-month survival.

Use churn that decays over the first year; a flat churn rate overstates LTV.

## Pricing

```bash
python3 scripts/pricing_calculator.py --config pricing.json
```

Van Westendorp (too cheap, cheap, expensive, too expensive) plus price elasticity revenue and
margin. If you have no elasticity estimate, run a price test before trusting that section.

## Portfolio and capital reallocation

```bash
python3 scripts/portfolio_matrix.py --config portfolio.json
```

Weighted GE-McKinsey 9-box: attractiveness and competitive strength, per business unit, with
revenue and zone placement. The decision is not the score; it is the capital movement between
zones.

## Synergy case

```bash
python3 scripts/synergy_case.py --config synergies.json
```

Cost and revenue synergies with realistic ramp curves, a confidence haircut on revenue
synergies, one-time integration costs, and synergy NPV separate from the standalone deal.
Revenue synergies are less reliable than cost synergies; the haircut is not optional.

## Negotiation: BATNA and ZOPA

```bash
python3 scripts/batna_zopa.py --config negotiation.json
```

Role (buyer/seller), target, BATNA value, counterparty's estimated reservation and target.
Output: your reservation price, the ZOPA, a recommended anchor, and a flag when no ZOPA
exists. If there is no ZOPA, change the deal structure or walk; do not negotiate harder on
price.

## Rules

- Save the config beside the output. A number without inputs is not reproducible.
- State currency, period, units and discount rate in the memo.
- Print the sensitivity or scenario, not only the headline.
- One model per decision. A model reused for a different question is a new model.
- A calculator failure on a degenerate input (zero denominator, empty years) is a finding.

## Common failures

- Initial investment without working capital or one-time costs.
- Revenue as a single growth line rather than volume × price or customers × ARPU.
- Opex that silently scales with revenue, improving margin without evidence.
- A discount rate chosen to flatter the case.
- A synergy case that counts day-one run-rate as year-one cash.
- A negotiation plan with no documented BATNA.
