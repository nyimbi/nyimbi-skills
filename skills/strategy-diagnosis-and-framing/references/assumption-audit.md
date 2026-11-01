# Assumption Audit Playbook

Surfaces the load-bearing assumptions behind a plan, grades their evidence, and converts
weak beliefs into tests. Run at **Full Case** depth (see
[SKILL.md](../SKILL.md)); **Client Deliverable** before board reviews, IC memos, or
major investment decisions.

## When to use

- A plan sounds plausible but rests on beliefs nobody has tested
- Pre-board, pre-investment, pre-launch, pre-acquisition, pre-expansion pressure tests
- "What has to be true?" / "How fragile is this case?"
- Any recommendation whose `[A]` labels cluster around the decisive numbers

## Approach

Find the beliefs that carry the weight of the strategy. Grade each by importance,
evidence strength, and testability; convert weak load-bearing assumptions into specific
validation work with an owner and a decision trigger. This is the operational form of
the epistemic rules in SKILL.md — it turns "state your assumptions" into a register with
a test plan.

## Workflow

1. **Name the strategy, decision, or plan under audit** and the decision it informs.
2. **Extract explicit and implicit assumptions.** Implicit ones (pricing holds, churn
   stays flat, the channel partner stays neutral) are where cases fail.
3. **Classify** by category: market, customer, economic, operational, competitive,
   organizational.
4. **Score each assumption** — importance (would failure change the decision?),
   evidence strength (`[F]`→`[A]` per evidence-standards), testability.
5. **Isolate load-bearing assumptions**: high importance, weak evidence. These are the
   ones worth naming in the recommendation's kill conditions.
6. **Convert weak load-bearing assumptions into tests**: test, data needed, owner,
   decision trigger. Anything that cannot be tested states what action follows if it
   fails.

## Output format

```markdown
# Assumption Audit

## Strategy Being Tested
[Brief description.]

## Assumption Register
| Assumption | Category | Importance | Evidence Strength | Risk |
|---|---|---|---|---|

## Load-Bearing Assumptions
1. [Assumption and why it matters]
2. [Assumption and why it matters]

## Test Plan
| Assumption | Test | Data Needed | Owner | Decision Trigger |
|---|---|---|---|---|

## Recommendation
[Proceed, pause, test first, or redesign.]
```

## Quality bar

Playbook checks on top of the SKILL.md checklist:

- [ ] Implicit assumptions are included, not only stated ones
- [ ] Load-bearing set is short and ranked — an audit that flags everything flags nothing
- [ ] Every test has evidence needed, owner, and a decision trigger
- [ ] Each failed assumption states what action follows
- [ ] The register is the source of the recommendation's kill conditions
