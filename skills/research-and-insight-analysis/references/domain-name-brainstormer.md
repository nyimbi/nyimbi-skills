# Domain Name Brainstormer

Purpose: generate candidate domain names for a project and verify which are
actually registerable, then rank the survivors. This is the naming/shortlist
track of `research-and-insight-analysis`.

## When this track applies

The user is naming something and wants both creativity and a reality check:
"brainstorm domains for my project management tool", "find available
alternatives to <taken name>", "short names with .ai or .io for an AI writing
assistant".

## Evidence sources

| Layer | Source |
|---|---|
| Project context | User's description of what is being built, for whom, and any fixed keywords |
| Name candidates | Generation against explicit criteria (length, pronounceability, hyphen-free, meaning) |
| Availability | A live RDAP/WHOIS or registrar lookup per candidate × TLD — never an assumption |
| Conflict checks | Trademark register lookup and social handle availability, only when the user asks |
| Pricing | Current registrar pricing for the TLD in question; premium/parked status from the lookup |

Availability must be checked, not guessed — an unverified "available" is the one
error that wastes the user's money and trust.

## Method

1. Extract the constraints: audience, meaning to convey, fixed keywords,
   preferred TLDs, forbidden words, language.
2. Generate 10-15 candidates across naming patterns (descriptive compound,
   invented word, verb+noun, keyword+category, phrase) plus TLD variants of the
   best few.
3. Filter against the naming bar before spending a lookup: under ~15 characters,
   spellable aloud, no hyphens or numbers, no collision with a well-known mark.
4. Look up every survivor across the requested TLDs; record status
   (available / taken / premium / parked) and price.
5. Rank the available set with a stated rationale, name a top pick and a
   runner-up, and list the taken-but-worth-it options with their price context.
6. Close with next steps: register now, check handles, or iterate on a
   direction the user liked.

## TLD guide

| TLD | Signals |
|---|---|
| `.com` | Universal, trusted, best default for a business |
| `.io` `.ai` | Tech startups, developer tools, AI/ML products |
| `.dev` `.app` | Developer-focused products, web/mobile apps |
| `.co` | Alternative to `.com` |
| `.xyz` `.design` `.tech` `.eco` | Modern/creative, sector-specific |

Price context: standard domains ~$10-15/yr; `.io`/`.ai` ~$30-50/yr; taken
domains only at whatever the owner asks; premium names run hundreds to
thousands.

## Output template

```markdown
# Domain Suggestions — <project>

**Audience**: … | **Key concepts**: … | **Checked**: <date>

## Available
1. ✓ **name.tld** — why it works (length, meaning, audience fit) — price
…

## Taken / premium
- name.tld — taken, <price or "premium listing">

## Recommendation
🏆 Top pick: name.tld — the one reason it wins
🥈 Runner-up: name.tld — the trade-off

## Next steps
Register the pick and its defensive variants; check @handle availability;
iterate on <direction> if none of these land.
```

## Quality gates for this track

- Every "available" was verified by a lookup in this session, with the date shown
- Candidates pass the naming bar (short, pronounceable, no hyphens/numbers)
- TLD choice is justified against the audience, not listed for variety
- Taken names are reported honestly, with price context where premium
- The recommendation names one winner and one alternative, each with a reason
- Social-handle and trademark checks are performed only on request, and are
  labelled as a separate check from domain availability
