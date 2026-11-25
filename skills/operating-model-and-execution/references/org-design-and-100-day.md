# Org Design and the First 100 Days

## Spans and layers

```bash
python3 scripts/spans_layers.py --config org.json
```

Config: benchmark span by layer type (executive, middle management, frontline), fully loaded
manager cost, and each layer's manager count and direct reports. Output: average span by
layer, layers that are too narrow against the benchmark, and the annual cost of the extra
management layers.

Read the result as a design question: a narrow span is not automatically wrong, but it must
be explained by the work (high-complexity expert teams, regulated functions) rather than by
history.

## RICE and the kill list

```bash
python3 scripts/rice_prioritizer.py --config initiatives.json
```

Reach × Impact × Confidence / Effort, plus cost of delay. Output: ranking and the initiatives
that should be killed or deferred. A prioritisation with no kill list is a wish list.

## 100-day plan

Use for a new executive, an acquisition integration, or a turnaround. Three blocks, one
outcome each.

### Day 1–30: listen and stabilize

- Meet every direct report and the three most important external stakeholders.
- Map the system: money in, money out, decisions, bottlenecks, risks.
- Identify what must not break, and who owns it.
- Find two quick wins that are reversible and visible.
- Do not announce a reorganisation in the first 30 days.

**Outcome:** a written diagnosis and a stakeholder map.

### Day 31–60: choose and align

- Pick three priorities with owners.
- Kill or defer the work that does not serve them.
- Set the operating cadence: weekly metrics, monthly review, decision log.
- Agree decision rights for the three priorities.
- Test the first change in one team or one market.

**Outcome:** a published 90-day plan with owners and kill criteria.

### Day 61–100: deliver and lock

- Ship the first milestone.
- Review the metric against baseline.
- Keep what works, stop what does not, document the decision.
- Publish the next 100 days.

**Outcome:** one delivered result, one measured delta, one written decision.

## Pitfalls

- A listening tour with no written diagnosis.
- A reorganisation before the diagnosis.
- Quick wins that are neither visible nor reversible.
- A plan with more than three priorities.
- A stakeholder map that lists names but not power or stance.
- A 100-day plan with no "do not touch" list.
