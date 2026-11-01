# Deck Map — Plan to Pitch Deck

How the finished plan becomes the investor deck. The deck is **a compression of
the plan, not a summary of it**: every slide makes one claim, the deck stands
alone (the investor may never open the plan), and anything that does not earn
its place in the room gets cut, not shrunk. The actual `.pptx` is built by
`../../presentation-authoring/SKILL.md`; design direction by
`../../visual-design-and-branding/SKILL.md`. This file owns the narrative.

## 1. Rules that beat the structure

1. **One claim per slide.** If a slide needs an "and", it is two slides.
2. **10–12 core slides plus appendix.** More than 15 total means a plan was
   pasted into slides — cut back to claims.
3. **Numbers follow the plan's tags.** A slide number that is not in the
   evidence ledger does not go on the slide — it goes in the appendix, or it
   gets cut. `[Assumed]` numbers are spoken, not slid, unless the assumption
   is the point of the slide (then say "assumption — kill condition in
   appendix").
4. **Counter-arguments travel twice.** The section-level
   "strongest counter-argument and our answer" becomes (a) one line on the
   relevant slide where it disarms in place ("vs [incumbent]: their strength is
   X; our position is Y because Z"), and (b) the risk slide. The **top-3
   weakest points** from the red-team pass go on the risk slide and are the
   first thing the founder volunteers verbally — the deck proving it first is
   the trust move.
5. **The deck and the plan must not diverge.** After the deck is built, any
   number changed in one is changed in the other and the evidence ledger is
   re-checked. A deck number the plan cannot support is the most discrediting
   artifact a founder can produce.

## 2. The 12-slide structure

| # | Slide | Claim it must make | Feeds from (section-defense.md) | Cut from the plan |
|---|---|---|---|---|
| 1 | Title | What the company is, in one line the investor can repeat | §1 (one-liner only) | everything else |
| 2 | Problem | The pain, who has it, what it costs — evidenced | §2 | workaround detail beyond one example |
| 3 | Why now | The two dated changes that make this possible now | §4 (why-now research) | full market history |
| 4 | Solution | What it is and the mechanism of value | §3 | feature list beyond three |
| 5 | Product | What is shipped today vs planned | §3 | roadmap past 12 months |
| 6 | Market | Bottom-up SAM as the number of record; TAM as context | §4 | the gap explanation (speak it, don't slide it) |
| 7 | Business model & unit economics | How money is made; CAC/LTV/payback derived | §5 | cost-driver detail (appendix) |
| 8 | Traction | The cohort story: revenue, retention/churn, trend shape | §9 | full cohort table (one chart) |
| 9 | Go-to-market | The channel, the evidence it works, pipeline | §7 | channel experiments that failed (Q&A) |
| 10 | Competition | The honest matrix incl. incumbent's strengths | §6 | the full modeled-response analysis (Q&A) |
| 11 | Team | Why this team wins here; the one acknowledged gap | §8 | bios beyond two lines each |
| 12 | Ask & milestones | Amount, instrument, the milestone it buys, the decision point after | §10 + §12 | full use-of-funds table (one bar + 3 numbers) |

**Appendix slides (on request):** evidence ledger / sources, assumption
register with kill conditions, full cohort table, full model sensitivity
table, the top-3 weaknesses with mitigations, team detail, pricing detail.
The appendix is where the plan's rigor shows without bloating the core deck —
and a hostile investor who asks for the appendix slide gets one that exists.

## 3. What does NOT make the cut

- The full 20-question red-team battery — that is the Q&A prep doc, not the
  deck
- All three scenario cases — base on the slide, sensitivity in the appendix
- The pre-mortems — internal; their findings are already dispositioned
- Any claim the plan tags `[Assumed]` with low confidence — spoken with
  "we're testing this; here's the kill condition", or cut
- Design flourishes that replace a claim — a deck is claims with visuals, not
  a magazine

## 4. The compression pass (run before handing to presentation-authoring)

1. Lay the 12 slides against the plan section by section; mark every slide
   number with its claim-file entry.
2. Read each slide as the hostile reader: if the slide's claim is not
   supported on the slide or one click away in the appendix, fix or cut.
3. Check the deck against the three killer findings from
   `hostile-review.md` — market math, projection drivers, hidden risk. If any
   is not disarmed on-slide or in the appendix, the deck is not ready.
4. Read the deck aloud in order, one minute per slide. If the story stumbles,
   the order or a claim is wrong — fix the deck, not the speech.

## 5. Handoff

Deliver to `../../presentation-authoring/SKILL.md` as: the 12-slide outline
with per-slide claim text, the appendix list, and the note that slide
numbers must match the plan's evidence ledger exactly. It produces the `.pptx`;
this map owns what the deck says.
