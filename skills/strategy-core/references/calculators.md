# Calculators

Every script is dependency-free Python, takes a JSON config with `--config`, and prints a
table plus a verdict. Read the docstring at the top of the script for the exact config shape.
Run from the skill directory:

```bash
python3 scripts/npv_case.py --config case.json
```

| Calculator | Owner skill | Use |
|---|---|---|
| `full_potential_calc.py` | `strategy-diagnosis-and-framing` | Gap to top-quartile on P&L and working-capital metrics; value at stake |
| `tam_sam_som.py` | `market-and-competitive-intelligence` | Top-down and bottom-up market size; flags >30% disagreement |
| `npv_case.py` | `strategic-choices-and-economics` | NPV, IRR, payback, revenue × discount-rate sensitivity |
| `unit_economics.py` | `strategic-choices-and-economics` | LTV:CAC, CAC payback, contribution margin, churn decay |
| `pricing_calculator.py` | `strategic-choices-and-economics` | Van Westendorp price points and elasticity revenue/margin |
| `portfolio_matrix.py` | `strategic-choices-and-economics` | Weighted GE-McKinsey 9-box and capital movement |
| `synergy_case.py` | `strategic-choices-and-economics` | Ramped cost/revenue synergies, confidence haircut, synergy NPV |
| `batna_zopa.py` | `strategic-choices-and-economics` | BATNA, reservation price, ZOPA, walk-away |
| `spans_layers.py` | `operating-model-and-execution` | Span of control by layer, management cost, delayering options |
| `rice_prioritizer.py` | `operating-model-and-execution` | RICE ranking and kill list |
| `risk_matrix.py` | `risk-performance-and-value-governance` | Likelihood × impact × velocity scoring |
| `decision_tree_ev.py` | `risk-performance-and-value-governance` | Expected value of strategic options under competitor response |
| `power_interest_grid.py` | `executive-communication-and-alignment` | Power/interest map and coalition arithmetic |

## Rules

- Save the config next to the output. A number without its inputs is not reproducible.
- State currency, period and discount rate in the memo.
- Print the sensitivity or scenario table, not only the headline.
- A calculator failing on a degenerate input (zero denominator, empty years) is a finding:
  fix the input or say the case is undefined.

## Attribution

The calculators are from `Natan-Mohart/24-strategy-skills-for-claude`, MIT. The licence sits
beside each script as `LICENSE-natan-mohart`.
