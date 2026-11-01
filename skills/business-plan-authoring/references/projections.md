# Projections — 24–36 Month Driver-Based Model

A projection is defensible when an investor can change one driver and watch the
output move sensibly. If the model is a number with a shape, it is a hockey
stick and the red-team pass will kill it. This is how the model in Workflow
step 5 is built.

## 1. Structure

- **Horizon:** 36 months preferred, 24 minimum for seed. Monthly detail for
  month 1–12, quarterly after (a month-18 monthly figure implies a precision
  no one has).
- **Three scenarios:** base / downside / upside — same structure, different
  driver values, each scenario's drivers visible side by side (scenario
  discipline per `../../strategic-choices-and-economics/references/business-case-builder.md`).
- **Units:** revenue, gross profit, opex by category, EBITDA, cash and runway.
  No line item that is not derived from a driver.

## 2. Revenue build — drivers, not growth rates

Revenue is never "last year × growth". It is:

```
Revenue(t) = Σ over cohorts c:
    customers(c, t) × logo_value(c) × (1 + expansion(c)) × (1 - churn(c))
```

Each driver is its own row with its own assumption:

| Driver | Basis | Tag |
|---|---|---|
| New customers per period | channel capacity × conversion, or pipeline ÷ cycle — stated | sourced or assumed |
| Logo value | price card × mix, or observed | sourced / internal data |
| Expansion | observed NRR if it exists; else stated assumption with a comparable | — |
| Churn | observed logo churn if it exists; else segment-typical with source | — |

Rules:

- Every driver carries a `[Sourced]` / `[Assumed]` tag and appears in the
  evidence ledger.
- A driver that has never been observed in the company's own data is an
  assumption — say so, and give the kill condition ("if 12-month cohort churn
  exceeds [x], the base case fails").
- Growth is an **output** of the hiring and channel plan, not an input. If the
  model grows 3x and the hiring plan only supports a 1.5x pipeline, one of
  them is wrong.

## 3. Cost model

- **COGS / gross margin:** name the cost drivers — infrastructure, delivery
  labor, payments, data, licensing — each with its own growth assumption.
  Margin is a derivation, never a flat input. State the current margin and the
  24-month target margin with the lever that closes the gap (scale, self-serve
  mix, re-pricing).
- **Opex by category:** product, go-to-market, ops, G&A. Every headcount line
  is a named role with a hire month and the output that role produces. A hire
  that produces no modeled output is a wish, not a plan — cut it or give it an
  output.
- **Salary bands:** sourced from the research phase (question 8). A 40% gap
  between assumed and market comp is a broken runway model.

## 4. Use of funds and the burn bridge

```
Starting cash + round − Σ burn(t) = cash at milestone date
```

- The bridge must land on the **named milestone** (the one the round is sold
  on) with a stated buffer. Buffer is explicit — 3–6 months typical — and the
  contingency it covers is named.
- Use-of-funds table matches the hiring plan line by line: every comp line in
  the table corresponds to a hire row in the model. A mismatch here is the
  single most common fatal finding in a fundraise model.
- At the end of the bridge, state the next decision point: next raise at
  [milestone/metric], break-even at [condition], or the kill/pivot trigger.

## 5. Sensitivities (required)

Before delivery, change the two most load-bearing drivers independently and by
combination:

| Sensitivity | Base | Downside | What breaks |
|---|---|---|---|
| CAC +20% | | | payback crosses [n] months at ... |
| Churn +3pts | | | LTV drops to ..., LTV/CAC to ... |
| Both | | | the milestone slips [n] quarters; buffer absorbs / does not absorb |

The plan presents this table. A model that survives CAC +20% and says what
breaks first is worth more than one that pretends the downside does not exist.

## 6. Anti-patterns (each one is a red-team finding)

- **Hockey stick with no drivers** — revenue grows at a constant rate for 36
  months. Fails step 2 by construction.
- **False precision** — a six-digit input feeding a two-significant-figure
  conclusion (business-case-builder rule). Round to what the evidence supports.
- **Flat margin** — gross margin as a constant line while the cost drivers
  move. Rebuild with named cost drivers.
- **Hiring before triggers** — comp lines that precede the revenue that funds
  them, with no bridge coverage.
- **"We'll optimize" as a line item** — a cost that only disappears by
  assertion. Name the mechanism or cut the line.
- **Round-sized to the model** — the amount chosen to make the bridge look
  clean rather than to buy the milestone. Size the round to the milestone,
  then show the bridge.
