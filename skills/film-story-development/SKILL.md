---
name: film-story-development
description: >-
  Develop a rough film or series idea into a production-ready screenplay: interrogate the
  premise, build the character spine, choose a structure, write the beat sheet and scene
  cards, draft in Fountain format, run a table read and cut for runtime, and produce the
  series bible for episodic work. Use when the user has an outline, premise, treatment, or
  "idea for a movie/series" and needs the story fleshed out before design or storyboarding:
  "turn this into a screenplay", "flesh out this outline", "write the story", "develop the
  characters and plot", "make a series bible", "why is this draft too long", "adapt this for
  AI production". Do not use for shot planning and blocking (see film-directing), for visual
  design (see film-design), or for the end-to-end production run (see film-production).
---

# Film Story Development

The writing room. It turns a rough idea into a script that is worth designing and cheap
to change, and it refuses to hand downstream a story that is still vague. A screenplay is
the cheapest place to solve a problem; a generated shot is the most expensive.

> **Pipeline position.** Stage 1 of `film-production`. Writes `01_story/`; hands the
> locked script and continuity seed to `film-design` and `film-directing`.

## Intake

Establish, inferring where possible:

```yaml
format: short | episode | feature | vertical | trailer
runtime: seconds or minutes
genre: drama | thriller | comedy | horror | sci-fi | action | romance | ...
tone: grounded | heightened | comic | tragic | mythic
audience: general | young adult | genre fans | family
rating: G | PG | PG-13 | R | unrated
language: dialogue language
constraints: cast size | locations | budget tier | deadline | AI-production limits
theme_seed: what the author wants to say, if stated
```

Do not interrogate. State assumptions in one or two lines and proceed. The one question
worth asking is the ending: a story whose destination is unknown cannot be structured.

## Step 1 — Premise and logline

Write a one-sentence logline with five parts:

```text
When <inciting situation>, <protagonist> must <goal> before <stakes>,
but <obstacle/antagonist> forces <hard choice>.
```

Then test it:

- **Specific** — a person, a goal, a clock. Not "a journey of self-discovery".
- **Ironic or pressured** — the goal should cost something, or the situation should
  contradict the goal.
- **Visual** — you can see the world of the film in the sentence.
- **Filmable at this budget** — no element that the pipeline cannot produce.

Write `01_story/logline.md` with the logline, the dramatic question, the theme as a
contestable claim ("loyalty is a debt that outlives the person you owe"), and the tone
contract (what the audience is promised: dread, warmth, awe, laughter).

## Step 2 — Character spine

For each principal (2–5 for a short, 4–8 for a feature, recurring cast for a series):

| Field | Question |
|---|---|
| Want | What do they pursue, concretely, in this story? |
| Need | What do they actually require to be whole? |
| Wound | What happened before page one that made the want a substitute for the need? |
| False belief | What do they believe that the story will test? |
| Arc | Positive (belief broken), negative (belief confirmed at a cost), flat (belief tested and held) |
| Voice | Sentence length, vocabulary, evasion, verbal tic, what they never say |
| Contradiction | The trait that makes them hard to predict |
| Relationships | Who has power, who owes, who loves, who lies |
| Secret | What the audience learns last, and what it changes |

The antagonist gets the same spine. A villain with only a plan is a plot device.

Write one page per principal in `01_story/characters/<slug>.md`. `film-design` will turn
these into visual bibles; it needs psychology, not just appearance.

## Step 3 — Structure

Choose one model and commit. Never mix two structural maps in one draft.

| Model | Best for | Shape |
|---|---|---|
| Three-act | features, shorts | setup → confrontation → resolution; two major turns |
| Eight-sequence | features | eight ~12-minute sequences, each with its own question and turn |
| Save the Cat 15 beats | commercial features | beat-labeled, audience-legible |
| Story circle | character-driven | comfort → want → go → adapt → get → pay → return → changed |
| Kishōtenketsu | twist-led shorts, non-Western drama | introduction → development → twist → reconciliation |
| Short-film shape | 5–15 min | one protagonist, one problem, one turn, one final image; 20/50/20 |
| Episode shape | series | cold open/hook → act breaks → button or cliffhanger |
| Vertical micro-drama | 60–180 s | hook in 3 s → escalation every 15–20 s → cliffhanger |

Write `01_story/beats.md` as 7–12 beats. A beat is a **change in the balance of
pressure**, not a camera move. Each beat states:

```text
Beat N — <name>
Function: what the audience now understands that they did not before
Action: what visibly happens
Turn: the value that flips (safe → endangered, together → alone, truth → lie)
Exit: the question that pulls us into the next beat
```

If a beat has no turn, it is a scene, not a beat. If two beats have the same turn, merge
them.

## Step 4 — Scene cards

Break the beats into 8–14 scenes (short) or 35–60 (feature). One row per scene:

| # | Location | Time | Cast | Goal | Conflict | Turn | Out | Purpose | Est. s |
|---|---|---|---|---|---|---|---|---|---|

Rules:

- Every scene has a **goal**, an **obstacle**, and an **outcome that changes the next
  scene's conditions**. A scene that only delivers information is a candidate for a line
  of dialogue or an insert.
- **Enter late, leave early.** Start after the greeting, end before the goodbye.
- Keep a **scene economy budget**: in a 10-minute short, 8–12 scenes; in a feature,
  roughly one scene per 90–150 seconds of screen time.
- Mark **AI-risk scenes** now: crowds, children, animals, hands, text, sustained
  dialogue, complex action, water, fire. See `references/ai-feasibility.md`.

Write `01_story/scene-cards.csv`.

## Step 5 — Screenplay

Draft in **Fountain**, plain text, because every downstream tool can parse it and every
agent can read it. Syntax: `references/fountain-format.md`.

Hard rules:

1. **Write only what can be seen or heard.** No interior states, no backstory the camera
   cannot show ("she remembers her mother"). Convert to behavior, object, or sound.
2. **Action is present tense, visual, and short.** One idea per paragraph. No camera
   directions unless the shot is the story.
3. **Dialogue is negotiation, not information.** Characters want something from each
   other in every exchange. If both characters agree, the scene is over.
4. **Subtext over text.** The line says one thing; the body, the pause, or the object
   says the other.
5. **Names must be speakable and distinct.** TTS and lip-sync degrade on similar
   phonemes; avoid two leads whose names rhyme.
6. **Keep the cast and locations small.** Every additional principal is another identity
   to lock, another voice to cast, another reference set to maintain.
7. **Write to the format.** Vertical frames faces and hands; widescreen frames space and
   isolation; a phone screen is a different grammar.

Write `01_story/screenplay.fountain`. Version it; never edit a locked draft in place.

## Step 6 — Table read, timing, cut

Read the script aloud, either with the user or with TTS voices from `film-design`'s
casting sheet. Time it. Then:

- **Runtime math.** One formatted page ≈ one minute. For AI production, also count shots:
  `runtime_s / average_shot_s`.
- **Cut 20–30%.** First drafts run long. Remove the weakest scene, the second explanation
  of any fact, and any scene whose only job is to move a character between locations.
- **Read for the ear.** Lines that are hard to say are hard to perform and harder to
  lip-sync. Cut or rewrite them.
- **Check the three-sentence test.** Can you describe the arc using only visible actions?
- **Check the ending.** The final image should answer the opening image, changed.

Write `01_story/table-read.md` with the timed read, cuts made, and unresolved performance
risks.

## Step 7 — AI-production pass

Before locking, walk every scene against the production constraints:

| Problem | Rewrite move |
|---|---|
| Crowd | isolate the protagonist; use sound and reaction shots |
| Complex hands | cut to the object, the face, or a silhouette |
| Legible text | design the insert in post, or avoid the shot |
| Sustained dialogue | split into one-speaker clips, reactions, and cutaways |
| Child or animal lead | reduce screen time; use POV, over-shoulder, or off-screen |
| Large action | stage it as cause → reaction → aftermath, not a continuous stunt |
| Many locations | consolidate; a location is a design asset and a continuity liability |
| Voice-over | use it for time jumps and interiority, not to explain the image |

Rewrite before the script locks. A scene that survives on the page but cannot be shot is
a debt paid in regeneration hours.

## Step 8 — Series bible

For episodic work, write `01_story/series-bible.md` before episode one. It contains:

- **Premise and promise** — the repeatable engine: what every episode delivers.
- **Season arc** — the question of the season, answered in the finale.
- **Character arcs** — state at episode 1 and at finale, with the turns between.
- **Episode grid** — one row per episode: promise, A-plot, B-plot, turn, cliffhanger.
- **World rules** — what is possible, what is forbidden, what it costs.
- **Continuity seed** — canonical identity blocks, relationships, knowledge states,
  injuries, props, and time-of-day logic. `film-design` extends this into the ledger.
- **Production shape** — recurring locations, cast per episode, asset reuse, batch order.

Template: `references/series-bible-template.md`.

## Step 9 — Quality review

A draft is not ready because it reads well to its author. Run the review before lock.

### 9.1 Mechanical diagnostics

```bash
python3 scripts/storycheck.py 01_story/screenplay.fountain \
  --cards 01_story/scene-cards.csv \
  --ledger 01_story/setup-payoff.csv \
  --out 01_story/quality-report.md
```

It reports runtime, scene lengths, dialogue share, voice similarity, agency proxy,
unfilmable action, on-the-nose dialogue, passive constructions, repeated phrases, card
completeness, and ledger matches. It is a defect finder, not a verdict: a clean run means
the flags below were not found, not that the script is good. Confirm every flag by reading
the scene.

### 9.2 The rubric

Score the eight dimensions in `references/quality-gates.md` 0–4. Target **average ≥ 3.0,
no dimension ≤ 2**. Every score below 3 cites a scene or line and proposes a fix.

### 9.3 Independent readers

Run these in **separate contexts**; never let the drafting model grade its own draft:

- **Structural editor** — causality, turns, midpoint, pacing, setup/payoff.
- **Character auditor** — want/need/wound, agency, contradiction, voice, arc.
- **Audience proxy** — genre promise, attention, confusion, emotional response.
- **Hostile producer** — "why should I fund this?", the three weakest points.

Fix the top three structural issues, not every note. A hard-check failure is fixed
regardless.

### 9.4 Blind read and table read

- **Blind read** by someone who has not seen the outline: mark boredom, confusion,
  predictions, the ending feeling, and the one remembered line. Do not explain first.
- **Table read** with a distinct TTS voice per principal (`film-design` casting sheet),
  timed. Cut 20–30%; rewrite lines that are hard to say.

### 9.5 Revision and re-test

Change one structural variable at a time (a turn, a relationship, an ending), keep a
revision log, compare drafts blind, and re-run `storycheck.py` and the readers after every
structural change.

## Step 10 — Lock

Produce `01_story/LOCK.md`:

```text
Version: 1.0
Locked: YYYY-MM-DD
Runtime target: N s
Scene count: N
Shot estimate: N (runtime / average shot length)
Principals: N
Locations: N
Known production risks: ...
Change policy: after lock, edits are numbered revisions; scene numbers never change.
```

## Quality gates

A script is ready for design only when all of these are true:

- [ ] Logline names a protagonist, goal, obstacle, and stakes in one sentence.
- [ ] Dramatic question is answerable yes/no and is answered by the ending.
- [ ] Every principal has want, need, wound, false belief, and arc.
- [ ] Every beat changes the pressure; no two beats share a turn.
- [ ] Every scene has goal, conflict, turn, and a changed exit condition.
- [ ] The draft reads aloud within 10% of target runtime.
- [ ] The final image answers the opening image.
- [ ] AI-risk scenes are rewritten or explicitly accepted with a fallback.
- [ ] Cast and location counts match the budget tier.
- [ ] For series: season grid, episode promises, and continuity seed exist.
- [ ] `01_story/quality-report.md` exists from `storycheck.py`; every flag was read and
      either fixed or accepted with a reason.
- [ ] Rubric average ≥ 3.0, no dimension ≤ 2, with scene/line evidence below 3.
- [ ] Structural editor, character auditor, audience proxy and hostile producer have each
      run in a separate context; the top three structural fixes are addressed.
- [ ] Blind read and timed table read are done; cuts and rewrites are logged.
- [ ] A human has signed the script gate and the decision is recorded.

## Reference map

| File | Contents |
|---|---|
| `references/structure-models.md` | the eight structural models with beat templates and when to use each |
| `references/fountain-format.md` | Fountain syntax and formatting rules |
| `references/ai-feasibility.md` | the AI-production rewrite table and shot arithmetic |
| `references/series-bible-template.md` | season grid, episode grid, continuity seed |
| `references/quality-gates.md` | 8-dimension rubric, hard checks, diagnostic questions, independent-review protocol, revision rules |
| `scripts/storycheck.py` | mechanical diagnostics: runtime, scene lengths, voice similarity, agency proxy, filmability, cards, ledger |
