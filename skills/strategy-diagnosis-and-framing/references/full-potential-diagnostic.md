# Full-Potential Diagnostic

Sizes the value at stake between current performance and a top-quartile benchmark. Use it
before a transformation, a turnaround, or a capital request, when the question is "how much
is on the table?" rather than "what is the strategy?"

## Method

1. **Choose the peer set.** Same business model, geography and scale. A payments processor is
   not benchmarked against a bank; a 20-person SaaS against a public one.
2. **Normalize.** Same fiscal year, currency, revenue definition, and one-off treatment.
3. **Build the metric tree.** Cover the P&L and working capital:
   - Gross margin, SG&A, EBITDA margin.
   - Revenue per customer, price realization, volume.
   - Inventory turns, DSO, DPO, cash conversion cycle.
   - Cost per transaction or per unit, where relevant.
4. **Compute the gap.** Current vs benchmark, in percentage points and in currency.
5. **Value at stake.** Sum the independent gaps at the revenue base. Remove double counting
   when two metrics move the same line.
6. **Split the gap.** Price, volume, mix, productivity, procurement. A gap with no mechanism
   is not a target.
7. **Test attainability.** Which moves close which gap, over what time, with what investment?
8. **Pick three moves.** A full-potential list is not a plan.

## Calculator

`scripts/full_potential_calc.py` takes a JSON config:

```json
{
  "revenue_base": 120000000,
  "metrics": [
    {"name": "Gross margin %", "current_value": 38, "benchmark_value": 46,
     "unit": "pct_of_revenue", "direction": "higher_is_better"},
    {"name": "SG&A as % of revenue", "current_value": 22, "benchmark_value": 16,
     "unit": "pct_of_revenue", "direction": "lower_is_better"}
  ]
}
```

It prints the value at stake per metric and the total. Run:

```bash
python3 scripts/full_potential_calc.py --config metrics.json
```

## Pitfalls

- A benchmark set chosen to flatter or frighten; state the peer list and why.
- Comparing a revenue mix with a different margin structure.
- Counting the same dollar twice across overlapping metrics.
- Treating a benchmark gap as a target without a mechanism.
- Ignoring working capital; the P&L gap can hide a cash problem.
- Quoting the total without the three moves that capture it.

## Output

A one-page table: metric, current, benchmark, gap, value at stake, mechanism, move, owner.
Then a sentence: "The value at stake is X; the three moves that capture Y% are ...".
