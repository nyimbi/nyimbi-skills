# Raffle and Random Selection

Purpose: pick winners, runners-up, or random assignments from a list with
auditable fairness. This is the random-selection track of
`file-media-and-engagement-tools`.

## Inputs

Any of: CSV or Excel file, Google Sheet URL, or a pasted list of
`Name (email)` lines. Before drawing, confirm and state:

- Source and total entry count
- How many winners, and how many runners-up
- Any exclusions (previous winners, staff, ineligible entries)
- Whether selection is uniform or weighted (e.g. one row = one ticket)
- Eligibility rule the winner must satisfy

## Selection rules

- Use **cryptographically secure** randomness — never a hand-rolled `rand()`
- Duplicate prevention: one win per person, even if they appear in the source twice
- Exclusions are applied *before* the draw, and the post-exclusion count is reported
- Weighted draws use an explicit weights column and state the weights used
- Record timestamp (UTC) and method with the result; a seed can be published so a
  third party can replay the draw

## Output format

```
Total entries found: 247  (after exclusions: 231)
Selection method: cryptographically random   Seed: <if published>
Timestamp: 2024-03-15 14:32:18 UTC

WINNER — Row #142
Name: Sarah Johnson
Email: sarah@email.com
Entry date: 2024-03-10

Runners-up: #38, #177, #205
```

Follow with: pick another winner excluding those already drawn, export the
winner list, or pick more runners-up.

## Common shapes

| Shape | Handling |
|---|---|
| Giveaway | draw from exported entries, verify winner details, announce with timestamp |
| Event raffle | CSV of attendees → draw N → export → notify |
| Team assignment | split the list into K groups of equal size, show the rosters for review |
| Survey/test participants | draw the sample size the study calls for, honour exclusions |

## Fairness checklist

- Secure randomness, no visible pattern in the picks
- Every entry had equal (or explicitly weighted) probability
- The same person cannot win twice
- Timestamp and method published with the announcement
- Only the minimum personal data needed is shown in the announcement
- A runner-up exists in case the winner is ineligible

## Quality gates for this track

- Entry count, exclusions, and winner count confirmed *before* drawing
- Randomness is cryptographically secure, and the method is stated in the output
- Duplicates in the source are collapsed before the draw
- The result carries a UTC timestamp and, where fairness may be disputed, a seed
- Announcement shows winner details only — no dump of the full entry list
