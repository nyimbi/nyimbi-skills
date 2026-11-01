# Quality Gate — Reflection Before Delivery

Deep detail for step 8 of the [SKILL.md](../SKILL.md) workflow. This gate runs *after*
the draft, the reader test, and the evidence check — it is the last thing before the
deliverable leaves the conversation.

## Why it exists

Confidently written, well-structured output gets taken at face value. For substantive
work the user will act on — spend money, brief a board, publish a claim, submit an
application — one moment of reflection catches a bad assumption before it matters. The
gate models three habits rather than lecturing about them:

- **Check facts** — which specific claims are worth verifying, and against what?
- **Question reasoning** — where did the logic take a step the user might want justified?
- **Notice missing context** — what did the answer have to assume because the user
  didn't say?

## When it applies

| Applies | Does not apply |
|---|---|
| Estimates, projections, numbers not grounded in the user's situation | Creative writing, brainstorming with no recommendation attached |
| Advice/recommendation in a consequential domain | Casual conversation, greetings, opinion swapping |
| Factual claims the user will act on or repeat | Code they will run — execution is the verification |
| Multi-step reasoning where one wrong assumption flips the conclusion | Simple lookups, unit conversions, definitions |
| Data or research interpreted on the user's behalf | Purely educational "how does X work" explanations |
| A substantive artifact drafted on their behalf (plan, pitch, proposal, email) | Material the user supplied — they are the judge of the transformation |

**The user already opted out** when they: asked you to double-check, cite, or flag
uncertainty (do the checking inline instead); asked for the quick version or said
they'll do their own research; asked you to review *their* work (your review *is* the
gate — raise open questions where they occur, not in a closing list); handed you the
material to summarize; or asked for your opinion ("what's your read?") — takes are
weighed, not fact-checked; hedge inline instead.

**Once per conversation.** If you already offered it on an earlier turn, stay silent.

## Writing the prompts

Two or three questions, never more. Each must reference something concrete you just
produced — a number, a named step, an assumption. Generic prompts defeat the purpose.

Each prompt does one of:

1. **Points at a fact or figure** — "How do these CPL estimates compare to benchmarks in
   my specific vertical?"
2. **Points at a reasoning step** — "Walk me through why you prioritized webinars over
   content — what assumptions does that rest on?"
3. **Points at missing context** — "I didn't mention my state — does the
   security-deposit rule change by jurisdiction?"

First person, conversational, question form, under ~120 characters each, so they read at
a glance.

## Output format

Answer the question completely first; the gate comes after and must be easy to skip.
Plain text, after a blank line:

```
A few things worth a second look:
- How do these CPL estimates compare to benchmarks in my specific vertical?
- Walk me through the reasoning behind the 70/30 split — what assumptions does it rest on?
```

Use that lead-in line exactly. Plain bullets, no heading, no blockquote, no emoji, no
HTML. Nothing after it — no "let me know if you'd like me to dig into these." The gate
is the closer.

## Suppression rule

Silence is the default; add prompts only when there is something concrete worth
reflecting *and* the user has not signalled that verification is covered. Repeating it
turns a light suggestion into nagging.
