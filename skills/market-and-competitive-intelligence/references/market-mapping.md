# Market Mapping Playbook

Sizes and segments a market from two independent angles, then converts the map into
where-to-play options. **This playbook owns market sizing for the strategy group** —
[profit-pool-analysis.md](profit-pool-analysis.md) and
[competitive-intel.md](competitive-intel.md) consume its output rather than restating
it. Run at **Full Case** depth (see
[../../strategy-diagnosis-and-framing/SKILL.md](../../strategy-diagnosis-and-framing/SKILL.md)).

## When to use

- Market entry, expansion, category creation, investment screening
- "How big is this market?" / "Where is the white space?" / "Which space should we play in?"
- Anywhere a TAM figure is about to be quoted — size is an `[E]` estimate, never an
  asserted fact

## Approach

Define the boundary before sizing it, then build the number from at least two
directions and reconcile them. Segment MECE, mark contested and unmet spaces, and hand
the attractive spaces to where-to-play decisions — attractiveness of the *market* is
separate from the user's *right to win*, which belongs to
`../../strategic-choices-and-economics/SKILL.md`.

## Workflow

1. **Define the market boundary and decision question**: geography, customer type,
   product scope, time horizon, explicit exclusions.
2. **Top-down sizing**: category totals from industry sources, narrowed by share
   assumptions. Record source, year, and what the number actually includes.
3. **Bottom-up sizing**: customer count × penetration × annual spend (or units × price).
   Reconcile with top-down; a >2× gap means the boundary or an assumption is wrong.
4. **Segment the market** by needs, economics, channels, behavior, or use case — using
   the segment-quality rules in [customer-segmentation.md](customer-segmentation.md).
5. **Map attractiveness by segment**: size, growth, profitability, competitive
   intensity. Structural profit concentration is the separate read in
   [profit-pool-analysis.md](profit-pool-analysis.md).
6. **Identify white space** — unmet needs or weak competition — and state where-to-play
   options with what further analysis each requires.

The step-by-step TAM/SAM/SOM practitioner walkthrough (formulas, worked numbers,
common mistakes) lives in
`../../strategic-choices-and-economics/references/frameworks-financial.md`; this playbook
owns the boundary decision, the two-method cross-check, and the hand-off to where to
play. Industry-structure context (Five Forces, value chain) is in
[frameworks-strategy.md](frameworks-strategy.md).

## Output format

```markdown
# Market Map

## Market Definition
[Boundary, exclusions, geography, time horizon.]

## Size Estimate
| Method | Logic | Estimate | Confidence |
|---|---|---|---|

## Segment Map
| Segment | Size | Growth | Profitability | Competition | Attractiveness |
|---|---|---|---|---|---|

## White Space
[Where needs are unmet or competition is weak.]

## Where-To-Play Options
1. [Option]
2. [Option]
3. [Option]
```

## Quality bar

Playbook checks on top of the SKILL.md checklist:

- [ ] Boundary and exclusions are written before any number is produced
- [ ] At least two sizing approaches, reconciled, with the gap explained
- [ ] Every size figure is labeled `[E]` or `[F]` with source, year, and coverage
- [ ] Segments are MECE and decision-relevant
- [ ] Market attractiveness is never confused with right to win
- [ ] No fabricated market size — if data is missing, state what data is needed
