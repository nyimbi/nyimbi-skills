# Suno MCP — score and song generation

Suno exposes a hosted MCP endpoint. It is useful for a title song, an end-credit track, or
a melodic theme; it is not a replacement for a scored mix.

## Connect

```bash
claude mcp add --transport http suno https://api.suno.com/mcp
```

Then run `/mcp` in the session and sign in. Authentication is the user's Suno account; there
is no API key, and generations consume the plan's credits. Songs are saved to the user's
Suno library.

Other hosts: add `https://api.suno.com/mcp` as a custom connector or MCP server, then
authorize.

## Use in the film pipeline

1. Write the **music brief** from the story: function, tempo, instrumentation, reference
   feel, where it enters and exits, and the emotion it argues.
2. Generate 2–4 candidates. Do not iterate endlessly; pick the one that serves the cut.
3. Download the chosen track and place it in `05_post/sound/score/`.
4. Duck it under dialogue in the mix; deliver it as a separate stem.
5. Record the licence terms and the generation date in the delivery manifest.

## Rules

- **Score to picture, not to taste.** The cue's job is defined by the scene.
- **One theme, variations.** A film with five unrelated songs has no score.
- **Leave room for silence.** The absence of music is a cue.
- **Clear the licence.** Generated music's terms are the user's plan terms, not a blanket
  commercial licence; check before publishing.
- **Do not use a song with vocals under dialogue** unless the vocal is the point.

## Local fallback

MusicGen medium on the local stack (`facebook/musicgen-medium`, 25 s chunks with 1.5 s
crossfades) produces usable beds and motifs. It is slower to steer than Suno and weaker on
structure, but it needs no account and no network.

Source: https://suno.com/mcp (retrieved 2026-10-30).
