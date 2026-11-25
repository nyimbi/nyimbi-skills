# GTM, Growth and Monetization

## 90-day GTM

| Week | Question | Artifact |
|---|---|---|
| 1–2 | Who is the one segment, and where do they gather? | segment brief, channel list |
| 3–4 | What promise and proof? | landing page, demo, message test |
| 5–6 | What is the activation event? | onboarding path, instrumentation |
| 7–8 | What does the first cohort do? | cohort dashboard, interview notes |
| 9–10 | What blocks conversion? | friction list, fix list |
| 11–12 | What repeats? | retention read, channel verdict |

Kill criterion: if activation or week-4 retention is below the stated threshold, stop the
channel or the wedge. Do not add budget to a funnel that does not retain.

## Growth loop

A loop has four parts:

```text
Trigger → Action → Reward → Investment → (back to Trigger)
```

- **Trigger:** the moment the user is prompted.
- **Action:** the behaviour that creates value or content.
- **Reward:** the value the user receives.
- **Investment:** the artifact, data or invite that makes the next trigger more likely.

Measure conversion at every arrow, cycle time, and leakage. A loop that needs paid
acquisition at the top is a funnel with a subscription.

Pick one core loop and one accelerant. Do not run four loops before one works.

## Monetization

| Model | Value metric | Fits |
|---|---|---|
| Subscription | seat, workspace, tier | recurring workflow, teams |
| Usage | API call, transaction, storage | variable consumption, infrastructure |
| Outcome | per hire, per claim, per sale | measurable result |
| Marketplace | take rate | two-sided transaction |
| One-time | licence, hardware | durable asset |
| Hybrid | base + usage | platform with a floor and a ceiling |

Rules:

- The price metric should track the value the customer receives.
- Packaging should make the next step obvious, not punish the behaviour the loop depends on.
- Test willingness to pay with Van Westendorp; run
  `../strategic-choices-and-economics/scripts/pricing_calculator.py`.
- Price changes need a cohort read, not an opinion.

## Roadmap and RICE

- **Now:** the wedge that proves the promise.
- **Next:** the retention or expansion move.
- **Later:** the platform or second-segment bet.

Run `../operating-model-and-execution/scripts/rice_prioritizer.py`. Print the ranking and the
kill list. A roadmap with no kill list is a wish list.

## OKRs

One objective per horizon. Two to four key results, each with a baseline, a target and a
source. A key result that cannot fail is a task.

## Common failures

- Launching to everyone, then calling the lack of signal a marketing problem.
- A loop diagram with no measured conversion.
- Monetization that taxes the core action.
- A roadmap ordered by loudest customer rather than the wedge.
- A 90-day plan with no week where a decision is made.
