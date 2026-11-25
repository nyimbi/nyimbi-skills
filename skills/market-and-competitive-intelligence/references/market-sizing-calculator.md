# Market Sizing Calculator

Triangulates TAM/SAM/SOM from a top-down and a bottom-up estimate. A single market number is
a guess with a decimal point; two independent estimates that disagree by more than 30% are a
finding about the inputs.

## Method

1. **Define the market.** Customer, need, geography, and the alternative being replaced. A
   market defined by a product category is usually too narrow or too broad.
2. **Top-down.** Population × target share × annual spend. Name the population source and its
   date.
3. **Bottom-up.** Units or customers × annual revenue per customer. Use actual transaction or
   contract data where possible.
4. **Serviceable filters.** Geography, segment fit, regulatory eligibility. Apply each as a
   percentage with a source.
5. **SOM.** A realistic share of SAM over a stated number of years, bounded by distribution
   capacity, not ambition.
6. **Compare.** If top-down and bottom-up TAM differ by more than 30%, do not average them.
   Resolve which input is wrong.

## Calculator

`scripts/tam_sam_som.py`:

```json
{
  "top_down": {"total_population": 5000000, "target_share_pct": 12, "avg_annual_spend": 4800},
  "bottom_up": {"units_or_customers": 45000, "avg_annual_revenue_per_customer": 6200},
  "serviceable_filters": {"pct_geography": 70, "pct_segment_fit": 55, "pct_regulatory_eligible": 90},
  "obtainable": {"realistic_share_of_sam_pct": 8, "years_to_reach": 3}
}
```

```bash
python3 scripts/tam_sam_som.py --config market.json
```

## Pitfalls

- A TAM that requires a behaviour that does not exist yet.
- Using a national population for a product that needs a bank account, a smartphone or a
  licence.
- Counting the same customer in two segments.
- A SOM that assumes a share the distribution cannot reach.
- Averaging two estimates that disagree instead of fixing the wrong one.
- Mixing annual and monthly spend, or local currency and USD.

## Output

A table with top-down TAM, bottom-up TAM, variance, SAM, SOM, the filters and their sources.
One sentence on which estimate you trust and why.
