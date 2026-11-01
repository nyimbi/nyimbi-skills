# Feasibility

The arithmetic that decides whether a film is a weekend, a campaign, or a fantasy.

## Shot arithmetic

```text
average_shot_s = 4 (generated coverage), 2.5 (action), 6 (drama holds)
shots          = runtime_s / average_shot_s
variants       = 3–5 hero, 2 coverage, 1 insert
generations    = sum(shots × variants)
gpu_hours      = generations × seconds_per_shot / 3600
cloud_cost     = generations × clip_s × price_per_second
```

## Local throughput (measured, M2 Max 96 GB)

| Engine | Render | s per ~4 s shot | 10-min short, 1 pass | 90-min feature, 1 pass |
|---|---|---:|---:|---:|
| LTX 0.9.8 distilled | 512×768 | ~100 | ~4.2 h | ~37.5 h |
| Wan 2.2 14B | 720p | ~400+ | ~17 h | ~150 h |
| MiniMax H3 REF2VA | reference | slowest | multi-day | not practical |
| LTX-2.3 MLX | probe | unknown | probe | probe |

Add keyframes (~1 image per shot), retries (20–50%), audio, and edit. Plan 2–4× the
single-pass number for a finished short.

## What each format really costs

| Format | Shots | Local one pass | Realistic local schedule | Cloud shape |
|---|---:|---:|---|---|
| 60–180 s vertical | 15–45 | 0.5–1.5 h | an afternoon | small |
| 5–8 min short | 75–120 | 2–4 h | 1–2 days | tens to low hundreds |
| 10–15 min short | 150–225 | 4–7 h | 3–5 days | low hundreds |
| 5–10 min episode | 75–150 | 2–5 h | 2–4 days per episode | per-episode budget |
| 90-min feature | 1,350 | 37.5 h | weeks, hybrid required | thousands, hybrid required |

Prices are deliberately not printed. Query the provider; rates change monthly.

## The hybrid feature

A feature is feasible only if most of it is not generated:

- **Animatic / graphic novel** for sequences that carry voice-over.
- **Stock or archival** for establishing and montage.
- **2D / motion-graphic inserts** for text, screens, documents.
- **Generated heroes** for the 15–25% of shots the audience will remember.
- **Practical or licensed footage** where the story allows.

Decide the hybrid ratio at the shot-plan gate, not after the first failed sequence.

## Honest limits

- **Performance**: sustained dialogue, subtle emotion, and physical comedy are weak.
  Write around them.
- **Continuity**: identity holds at medium and close, not at wide, and not across a model
  version change.
- **Action**: one action, one camera move. Complex choreography needs cuts and inserts.
- **Hands, text, crowds**: avoid or design around.
- **Runtime**: length multiplies every risk. A 6-minute film with 12 great shots beats a
  90-minute film with 1,350 mediocre ones.
- **Sound**: native model audio is a convenience, not a mix. Plan the sound pass.

## Feasibility decision

Before stage 1 ends, answer:

1. Runtime and shot count?
2. Which shots are generated, and which are animatic, stock, or 2D?
3. Which model for each class of shot?
4. Local hours and cloud budget, with contingency?
5. What will be cut if the schedule slips?

If the answer to 5 is "nothing", the plan is not feasible.
