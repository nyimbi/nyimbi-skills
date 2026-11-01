# Cost and Throughput

Prices and model availability change monthly. This file gives arithmetic and **relative**
tiers; query the provider for the current price before reserving a budget.

## The arithmetic

```text
shots        = runtime_s / average_shot_s
generations  = sum(shots × variants)          # hero 3–5, coverage 2, insert 1
gpu_hours    = generations × seconds_per_shot / 3600
cloud_cost   = generations × clip_s × price_per_second
disk_gb      = generations × clip_size_mb / 1024 + keyframes + audio + masters
```

Put the result in `PRODUCTION.md` and freeze a cap in `state.json`.

## Measured local throughput

From `cinematic-pipeline` on this machine (M2 Max, 96 GB), one pass, ~4 s shots:

| Engine | Render | Seconds per shot | 10-min short (150 shots) | 90-min feature (1,350 shots) |
|---|---|---:|---:|---:|
| LTX-Video 0.9.8 distilled | 512×768 | ~100 | ~4.2 h | ~37.5 h |
| Wan 2.2 14B | 720p | ~400+ | ~17 h | ~150 h |
| MiniMax H3 REF2VA | reference | slowest | multi-day | not practical |
| LTX-2.3 MLX | probe | unknown | probe | probe |

Multiply by the variant count. Three variants on a 10-minute short at LTX is ~12.5 h;
with retries and keyframes, plan 16–24 h. A feature is a multi-day campaign even before
quality retries.

## Cloud tiers

Do not quote a price you have not queried. Use tiers:

| Tier | Use | Cost shape |
|---|---|---|
| Local | coverage, inserts, animatic, drafts | GPU-hours only |
| Standard cloud | hero shots, dialogue, complex motion | per second; a 10-min short is typically tens to low hundreds of dollars at current mid-tier rates |
| Premium cloud | key art, title sequence, hardest shots | per second; often several times standard |

The provider is chosen per shot, not per film. A hybrid that generates 20% of shots and
covers the rest with animatic, stock, or 2D is usually the only way a feature budget closes.

## Decision rules

- **Keyframe before video.** A rejected still costs one image; a rejected clip costs a
  video generation.
- **Local first for coverage.** Use cloud for the shots the audience will remember.
- **Do not generate what a cut can imply.** A reaction shot is cheaper than a stunt.
- **Batch by location and character.** It reduces drift and setup time.
- **Reserve 20% contingency.** Retakes are not optional; they are the process.

## Budget ledger

`state.json`:

```json
{
  "budget": {
    "cap_usd": 0,
    "reserved_usd": 0,
    "spent_usd": 0,
    "gpu_minutes": 0,
    "policy": "stop and ask before exceeding cap"
  }
}
```

`04_gen/generation-log.csv` carries per-take cost and GPU minutes. Reconcile after every
batch; a budget that is only estimated is a budget that is already exceeded.
