# Twitter/X Algorithm Optimisation

Purpose: explain and rewrite a draft tweet against how the recommendation
system actually ranks content, so the change is justified by a mechanism rather
than a vibe. This is the engagement-optimisation track of
`file-media-and-engagement-tools`.

> Licence note: the source skill declared `AGPL-3.0 (referencing Twitter's
> algorithm source)` in its frontmatter and ships no licence file. That
> declaration is preserved here verbatim and was not expanded or guessed.

## Ranking models

| Model | What it predicts / does | What it means for a draft |
|---|---|---|
| Real-graph | Likelihood users interact with you | Write something your existing followers will actually engage with |
| SimClusters | Community membership via sparse embeddings | Pick ONE community and speak its language |
| TwHIN | User and post embeddings (interest graph) | Stay in your lane, or clearly signal a topic shift |
| Tweepcred | Author reputation from past engagement | Reply to strong accounts; avoid engagement bait |

## Signals tracked

**Explicit (high weight):** likes · replies · reposts · quote tweets.
**Implicit (also weighted):** profile visits · link clicks · dwell time · bookmarks.
**Negative (penalised):** block/report · mute/unfollow · instant scroll-past.

Feed pipeline: candidate retrieval (search, UTEG, tweet-mixer) → ML ranking
("will *this* user engage with *this* tweet, how fast, and will it spread past
followers?") → filtering → delivery. A draft must survive retrieval *and* rank.

## Strategy map

| Lever | Do | Don't |
|---|---|---|
| Real-graph | questions, audience-specific hooks, post when followers are active | statements nobody can reply to |
| SimClusters | one clear topic, community vocabulary, niche value | mixed messages across unrelated topics |
| TwHIN | domain-specific terminology, continuity with prior posts ("3rd review in a row") | vague "I like lots of things" identity |
| Tweepcred | thoughtful replies to high-credibility accounts, consistent quality | "RETWEET IF…" bait, reply-guy volume |
| Replies | direct question, a debatable claim, an unfinished thought to complete | leaving the question unanswered yourself |
| Reposts | sharable utility, representational value, information advantage | asking for the repost |
| Bookmarks | how-tos, data to revisit, jokes to return to | throwaway one-liners |
| Negatives | nothing inflammatory, misleading, or off-brand | anything block/report-likely |

## Rewrite procedure

1. **Core message** — the one thing this tweet says, who should care, and the
   single engagement you want.
2. **Map to mechanism** — which follower segment (Real-graph), which community
   (SimClusters), does it fit the author's established identity (TwHIN), does it
   help or hurt Tweepcred.
3. **Optimise for signals** — does it earn a reply? is it worth reposting? will
   it be read rather than scrolled?
4. **Screen for negatives** — block/report risk, identity confusion, bait,
   inflammatory phrasing.

Deliver as a **before / after table**: original · rewritten · the mechanism each
change targets. Keep the author's voice; if a rewrite changes the meaning, say
so and offer both.

## Quality gates for this track

- Every suggested change names the ranking mechanism or signal it serves
- One community and one core message per draft — no multi-topic merging
- The author's voice survives; meaning is not silently altered
- Engagement bait and negative-signal risks are called out, not quietly left in
- Claims about the algorithm are attributed to the published open-source
  description, not presented as current private ranking facts
