# Hostile Review — Mandatory Red-Team Pass

Workflow step 7. This is the step that separates a plan that survives the room
from one that is polite. It is **mandatory**: a plan delivered without a
completed red-team pass is a draft, not a plan. The pass is written, not
mental — findings go into the Red-Team Findings artifact.

## 1. The frame

Adopt the strongest version of the skeptic, not a straw man. The working
assumptions of the hostile reader:

- the market is **half** the claimed size
- the competition is **stronger and faster** than described
- the unit economics are **worse** once scale hits
- the team is **less capable** than the bio suggests
- the traction is **survivorship** — the cherry-picked cohort
- the plan is **hiding its one real risk**

The goal is not to be nasty. It is to find, on paper, every point where the
plan would be destroyed in person — and fix, pre-empt, or acknowledge it
before the funder finds it.

## 2. The question battery

Run every question below against the draft. Answer in writing. A question with
no answer is itself a finding.

**Market**
1. Show me the math on the number you actually believe — not the TAM.
2. What is the bottom-up SAM, and why would you win it before [incumbent]?
3. Why now — what specifically changed in the last 24 months, with dates?
4. If the growth rate is a one-year number, where is the third year?

**Economics**
5. Derive CAC for me — sales comp, tooling, pipeline, cycle — not "about $x".
6. What is your CAC payback, and what happens at 2x CAC?
7. Gross margin: current, 24-month, and the cost lever between the two.
8. LTV/CAC — show the LTV build. Where does expansion come from, evidenced?

**Competition**
9. Why won't the incumbent ship this in six months, and what does that cost them?
10. What is your moat at the point you win — feature, workflow, data, network,
    regulation? Which of those survives a well-funded copy?
11. What is the strongest argument against us, stated by someone who believes
    it?

**Team and execution**
12. Why this team and not [famous alternative]? What have you done in this
    market, concretely?
13. What is the key-person risk, and what happens on a bad Tuesday?
14. What gap in the team is the plan actually betting on, and who fills it?

**Traction and financials**
15. Show the cohort table. Where is the churn, and why should I not read the
    traction as survivorship?
16. Change CAC by 20% — what breaks first? (must match the sensitivity table
    in `projections.md`)
17. Why this amount of money — show the burn bridge to the milestone.
18. What do you do if you hit the milestone at half the revenue?

**The risk the plan hides**
19. What is the single most likely failure, stated honestly?
20. What would make you kill this plan? (the kill condition must exist)

## 3. The pre-mortem

Written, separate from the battery: "It is [milestone date] and the round did
not happen. In three sentences, write what went wrong." Run it three times
with three different dominant causes (market, execution, external). Any cause
the pre-mortem surfaces that the plan does not address becomes a finding.
(Mechanics per `../../strategic-choices-and-economics/references/frameworks-decision.md`.)

## 4. Findings and triage

Every finding is logged and triaged:

| Verdict | Meaning | Required action |
|---|---|---|
| **Fatal** | The plan, as written, would be rejected on this point | Block delivery. Fix in the plan (better data, rebuilt model, re-stated claim) and re-run the affected questions |
| **Fixable** | Weak but repairable with a paragraph, a source, or a reframe | Fix before delivery; note the fix |
| **Acknowledged** | Real, cannot be fixed now | Must appear in section 11 (Risks) with mitigation and kill condition |

Rules:

- A finding cannot be closed by softening the claim — the claim must be
  re-evidenced, the model rebuilt, or the risk acknowledged. "We toned it
  down" is not a disposition.
- The **top-3 weakest points** — the findings the team most wishes did not
  exist — are named in the risk section explicitly. This is the single highest
  trust-building move in the whole plan: the funder who hears their own best
  objection from you first re-weights everything you said.
- After fixes, re-run only the questions whose underlying claim changed, plus
  questions 16 and 19 always.

## 5. Exit criteria

The pass is complete when:

- all 20 battery questions have written answers
- the three pre-mortems are on record
- every finding is triaged fatal / fixable / acknowledged
- **zero open fatal findings**
- the top-3 weakest points are named in section 11 with mitigation and kill
  condition
- the Investor Q&A prep doc (SKILL.md output artifact) is drafted from the ten
  hardest questions, each with the prepared answer and the evidence it leans
  on
