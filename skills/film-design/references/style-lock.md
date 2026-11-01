# Style Lock

A style lock is a one-page contract. If two people fill in shots from it and produce
incompatible work, it is not locked.

## Fields

| Field | Decision | Failure if vague |
|---|---|---|
| Medium | live action, painterly 2D, 2.5D, 3D, stop motion, mixed | the film looks like two films |
| Reference frames | 3–6 images, each with the one thing it contributes | a mood board instead of a target |
| Palette | 3 dominant colors + 1 accent | every shot invents its own grade |
| Lens kit | 2 focal lengths that carry the film | no visual grammar; faces distort unpredictably |
| Depth / grain | deep or shallow; clean, fine grain, halation | shots do not cut together |
| Lighting grammar | key direction, ratio, practicals, color temperature | day and night look the same |
| Camera grammar | locked, handheld, dolly; allowed moves | motion budget overruns |
| Aspect / fps / resolution | e.g. 16:9 / 24 / 1920×1080 | delivery re-renders |
| Era / place | period, region, class markers | anachronisms |
| Negatives | named instances only | category negatives are ignored |

## Palette recipes

- **Three plus one.** Pick a dominant, a support, and a ground, then one accent used
  sparingly. Example: amber-gold dominant, deep teal support, charcoal ground, blood red
  accent.
- **Color script.** Assign a palette shift per act: warm/safe → neutral/pressured →
  cold/isolated, or the reverse. Write it in the lock so the grade follows the story.
- **Skin is the constant.** Palettes that push skin off-natural read as stylization; decide
  that deliberately.

## Lens and camera recipes

| Register | Kit | Camera |
|---|---|---|
| Grounded drama | 35 mm and 50 mm | locked or slow push |
| Isolation / unease | 24 mm and 85 mm | locked wide, compressed close |
| Action | 28 mm and 50 mm | one move per shot, high shutter feel |
| Period / formal | 40 mm and 75 mm | symmetrical, locked |
| Vertical drama | 35 mm and 65 mm | close and medium, faces upper-middle |

Two lenses, one allowed move per scene. More is a decision the film has to earn.

## Style test

Before locking, generate three images with the same style block:

1. A face in the story's key light.
2. A location establishing frame.
3. A story prop in close-up.

If the three do not read as the same film, the lock is not finished. Adjust the medium,
palette, or light — not the individual prompts.

## The lock block

Write the reusable prompt fragment once:

```text
STYLE — [medium]. Palette: [3 colors + accent]. Lens: [two focal lengths].
Light: [key direction, ratio, practicals]. Grain: [fine/clean]. [Era, place].
Negative: [named instances].
```

This block is pasted verbatim into every keyframe and video prompt. `film-generation`
also records it in `generation-log.csv` so a look change is visible in the log.
