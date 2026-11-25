# Launch and Operations

## Experiment ladder

| Stage | Entry | Exit | Cost |
|---|---|---|---|
| Fake door | a promise and a landing page | click-through or waitlist above threshold | hours |
| Concierge | a handful of users | the job is done manually and repeated | days |
| Closed beta | working core, instrumentation | activation and week-4 retention | weeks |
| Open beta | support load is manageable | retention holds at higher volume | weeks |
| Public | unit economics and support are viable | growth without a proportional support spike | ongoing |

Each stage has a kill criterion and a named owner. Do not skip a stage because the demo looks
good.

## Instrumentation

Define before launch:

- **Activation event:** the first time the user gets the core value.
- **Retention event:** the behaviour that predicts return.
- **Friction event:** the step where users stop.
- **Value event:** the action that correlates with willingness to pay.
- **Guardrail event:** the abuse, error or support signal that should stop the launch.

If the event does not exist, the first task is instrumentation, not growth.

## Behaviour signals

For each belief, write:

> We believe <segment> will <behaviour> because <tension>. Evidence: <quant> and <qual>.
> Implication: <decision>. Test: <experiment>.

Pair every quantitative cut with a qualitative source: interview, support ticket, community
thread. A dashboard alone tells you what, not why.

## Launch cadence

- Daily signal review for the first two weeks: activation, retention, errors, support.
- Weekly after: cohort read, channel verdict, roadmap delta.
- A decision log: date, decision, evidence, owner.
- A rollback plan and a communications owner for each stage.

## Strategy to operations

Convert the chosen moves into issues:

```text
Issue: <one outcome>
Owner: <name>
Dependency: <platform, partner, approval>
Due: <date>
Done when: <measurable condition>
Kill if: <threshold>
```

If an issue cannot name a "done when" and a "kill if", it is a theme, not a task.

## Common failures

- Instrumentation added after launch, so the first cohort teaches nothing.
- A beta with no exit criterion, which becomes the product.
- A launch war room with no decision authority.
- A retro that lists what happened without changing the roadmap.
- Issues with no owner because "the team" owns everything.
