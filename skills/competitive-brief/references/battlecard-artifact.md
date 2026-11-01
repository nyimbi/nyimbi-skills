# Deal Battlecard Artifact (interactive HTML output)

Use this when the user wants the competitive analysis as a **self-contained
interactive HTML battlecard** for use in deals — clickable competitor tabs, a
head-to-head comparison matrix, talk tracks, and landmine questions in one
file they can open in any browser, share, or host — rather than (or in
addition to) the written brief.

## Inputs

**Required:** the company (or detect from context) and the main competitors
(1–5). **Optional:** which competitor to focus on first, specific deals being
contested, pain points heard from customers about the competitors. Confirm
seller context once per engagement; skip when already established.

Connectors (all optional — web research works standalone): **CRM**
win/loss history and deal-level competitor tracking · **Docs** existing
battlecards and playbooks · **Chat** field intel from the team · **Transcripts**
competitor mentions and objections in customer calls.

## Research queries

Your company (always): `"[company] product"` · `"[company] pricing"` ·
`"[company] news"` (last 90 days) · `"[company] product updates OR changelog OR
releases"` · `"[company] vs [competitor]"`.

Per competitor: `"[competitor] product features"` · `"[competitor] pricing"` ·
`"[competitor] news"` · `"[competitor] product updates OR changelog OR releases"`
· `"[competitor] reviews G2 OR Capterra OR TrustRadius"` · `"[competitor] vs
[alternatives]"` · `"[competitor] customers"` · `"[competitor] careers"`
(hiring signals).

Then pull connected sources: closed-won/lost deals per competitor (CRM),
existing battlecard docs, 90-day chat mentions, call transcripts for
competitor mentions and customer quotes.

## Output specification

A single self-contained `.html` file, dark theme, professional styling, tabbed
navigation, expandable cards, responsive:

1. **Comparison matrix (landing tab)** — you vs all competitors at a glance:
   feature grid, pricing, market positioning, win-rate indicators (if CRM
   connected); color-coded winner indicators (green = you win, red = they win,
   amber = tie); sticky header row; expandable detail rows.
2. **One tab per competitor** — company profile (founded, funding, employees,
   target market, pricing model, market position); what they sell and how they
   position; recent releases (last 90 days) with impact; where they win / where
   you win (each with how-to-handle / proof point); pricing intelligence
   (model, entry, enterprise, hidden costs, talk track); scenario talk tracks
   (early mention / displacement / late addition to evaluation); objection
   handling; landmine questions.
3. **Your company card** — your releases (last 90 days), key differentiators,
   proof points and customer quotes.

### Skeleton

```html
<!DOCTYPE html>
<html>
<head>
  <title>Battlecard: [Your Company] vs Competitors</title>
  <style>/* dark theme, tabbed navigation, expandable cards, responsive */</style>
</head>
<body>
  <header><!-- [Your Company] Competitive Battlecard · Generated: [date] · Competitors: [list] --></header>
  <nav class="tabs"><!-- Comparison Matrix + one button per competitor --></nav>
  <section id="matrix" class="tab-content active">
    <h2>Head-to-Head Comparison</h2><!-- comparison table -->
    <h2>Quick Win/Loss Guide</h2><!-- per-competitor: when you win, when you lose -->
  </section>
  <section id="competitor-1" class="tab-content">
    <div class="battlecard">
      <div class="profile"></div><div class="differentiation"></div>
      <div class="talk-tracks"></div><div class="objections"></div>
      <div class="landmines"></div>
    </div>
  </section>
  <script>/* tab switching, expand/collapse */</script>
</body>
</html>
```

### Color system

```css
:root {
  --bg-primary: #0a0d14;  --bg-elevated: #0f131c;
  --bg-surface: #161b28;  --bg-hover: #1e2536;
  --text-primary: #ffffff;
  --text-secondary: rgba(255,255,255,.7);  --text-muted: rgba(255,255,255,.5);
  --accent: #3b82f6;      --accent-hover: #2563eb;   /* or your brand accent */
  --you-win: #10b981;     --they-win: #ef4444;       --tie: #f59e0b;
}
```

Cards: 12px radius, 1px low-opacity borders, hover elevation, 200ms transitions.

### Data structure per competitor

```yaml
competitor:
  name / website
  profile: { founded, funding, employees, target_market, pricing_model, market_position }
  what_they_sell: "[product summary]"
  their_positioning: "[how they describe themselves]"
  recent_releases: [{ date, release, impact }]
  where_they_win: [{ area, advantage, how_to_handle }]
  where_you_win:  [{ area, advantage, proof_point }]
  pricing: { model, entry_price, enterprise, hidden_costs, talk_track }
  talk_tracks: { early_mention, displacement, late_addition }
  objections:   [{ objection, response }]
  landmines:    ["[question that exposes their weakness]"]
  win_loss:     # when CRM connected
    { win_rate, common_win_factors, common_loss_factors }
```

Save as `[YourCompany]-battlecard-[date].html`.

## Delivery

```markdown
## ✓ Battlecard Created
[View your battlecard](file:///path/to/[YourCompany]-battlecard-[date].html)

**Summary** — Your company: [name] · Competitors: [list] · Sources: Web research [+ CRM / Docs / Transcripts]

**How to use** — Before a call: open the competitor tab, review talk tracks.
During a call: reference landmine questions. After win/loss: update with new intel.

**Sharing** — open locally in any browser; host on Netlify/Vercel/internal wiki; or send the file.

**Keep it fresh** — re-run monthly or before major deals.
```

## Refresh cadence

| Trigger | Action |
|---|---|
| Monthly | Quick refresh — new releases, news, pricing changes |
| Before a major deal | Deep refresh for that competitor |
| After a win/loss | Update patterns with new data |
| Competitor announcement | Immediate update on that competitor |

## Tips

- Be honest about their strengths — credibility comes from acknowledging them.
- Focus on outcomes, not features: "customers achieve Y" beats "they have X".
- The best intel comes from actual customer conversations, not just websites.
- Plant landmines, don't badmouth — expose weaknesses with questions.
- Track releases religiously — what they ship reveals their strategy and your opening.

## Related skills

- **account-research** — research a specific prospect before reaching out
- **call-prep** — prep for a call where a competitor is involved
- **create-an-asset** — build a custom comparison page for a specific deal
