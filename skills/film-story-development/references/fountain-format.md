# Fountain Format

Fountain is plain text that reads like a screenplay and parses into one. It is the
default because every downstream step — table read, TTS, shot breakdown — can read it
without a proprietary tool.

## Title page

```fountain
Title: The Long Way Down
Credit: Written by
Author: A. Writer
Draft date: 2026-10-30
Contact: writer@example.com
```

## Scene headings

A line beginning with `INT.`, `EXT.`, `EST.`, `INT./EXT.`, or `I/E` is a scene heading.

```fountain
INT. KITCHEN - NIGHT
EXT. HARBOUR - DAWN - CONTINUOUS
INT. CAR - LATER
```

Use a consistent time vocabulary: `DAY`, `NIGHT`, `DAWN`, `DUSK`, `CONTINUOUS`,
`LATER`, `MOMENTS LATER`.

## Action

Anything that is not another element is action. Present tense. One thought per
paragraph. Keep paragraphs under four lines.

```fountain
Rain hammers the window. MARA (40s) stands at the sink, sleeves rolled,
hands still. The tap runs. She does not look at it.
```

## Character and dialogue

A character cue is an uppercase line followed by dialogue.

```fountain
MARA
You said you'd call.

DEV
I did call.

MARA
You called the house. I wasn't the house.
```

- Parentheticals are for delivery that cannot be inferred, and are used sparingly:

```fountain
MARA
(quiet)
Don't.
```

- **Dual dialogue** uses `^` after the second character cue:

```fountain
MARA
Don't.

DEV ^
I have to.
```

## Transitions

Use only when the transition carries meaning: `CUT TO:`, `SMASH CUT TO:`,
`MATCH CUT TO:`, `DISSOLVE TO:`, `FADE OUT.` A transition on every scene is noise.

## Montage

```fountain
MONTAGE - MORNING ROUTINE

- Hands open a curtain.
- Kettle clicks on.
- A toothbrush, unused, in a cup.

END MONTAGE
```

## Notes, synopses, sections

```fountain
[[A production note the reader should see.]]

= Act One

# Sequence 2: The Harbour

## Scene 14 — the argument
```

`[[ ]]` is a note. `=` is a section, `#` a sequence, `##` a scene synopsis. Use them to
make the breakdown legible to `film-directing`.

## Forced elements

- `@` before a character cue forces it to be a character even if lowercase.
- `!` after a scene heading forces it to be a scene heading.
- `>` at the start of a line forces a transition.
- `~` forces a lyric line.
- `>` at the end of a line forces a page break before it.

## AI-production conventions

- Put the **canonical character name** in the cue exactly as it appears in the design
  bible. `MARA`, not `WOMAN` then `MARA`.
- Keep dialogue turns **one speaker per beat**, so each line can become one TTS clip and
  one lip-sync shot.
- Mark unfilmable or expensive action in a note rather than smuggling it into action:

```fountain
[[PRODUCTION: crowd of 40 — rewrite as isolated reaction or move to stock.]]
```

- Number scenes once and never renumber after the shot-plan lock. New scenes append
  letters: `14A`, `14B`.
