# Confidence Language, Source Grading, and Analytic Rigor

Reference tables for writing claims you can defend: how to word confidence, grade a
source, run Analysis of Competing Hypotheses (ACH), and interrogate your own bias.

## Fact / inference / assumption — sentence patterns

| Label | Test | Example |
|---|---|---|
| Fact | Sourced, observable, someone could verify it independently | "The domain `login-m365[.]top` was registered 2026-03-02 via Namecheap (WHOIS, retrieved 2026-03-05)." |
| Inference | A conclusion drawn from one or more facts; state the logic | "The registration date two days before the first lure suggests deliberate campaign staging." |
| Assumption | Unverified premise the judgment depends on; state what would falsify it | "We assume the targeted subsidiary shares the parent's M365 tenancy — if it does not, the lure is misdirected." |

Never let an assumption wear a fact's clothing. If the judgment collapses when the
assumption fails, say so in the same paragraph.

## Confidence and likelihood wording (analytic standards)

Confidence describes the *quality of the underlying evidence*; likelihood describes
*probability of an event*. Do not mix them.

| Confidence | Wording | Meaning |
|---|---|---|
| High | "assess with high confidence" | Multiple independent evidence types converge; few assumptions; alternatives weak |
| Moderate | "assess" | Credible sources, some gaps or assumptions required |
| Low | "suggests" / "likely reflects" | Limited or single-source evidence; serious alternatives remain |

| Likelihood | Wording |
|---|---|
| Almost certain | "we expect" (≥90%) |
| Probable | "likely" (≈60–90%) |
| Roughly even chance | "about even" (≈40–60%) |
| Unlikely | "we doubt" (≈10–40%) |
| Very unlikely | "we consider it improbable" (<10%) |

Rules:
- One confidence level per judgment, stated explicitly — not implied by hedging.
- Confidence belongs to the judgment, not to each individual fact inside it.
- Low confidence is a legitimate finding. Publishing "we cannot distinguish APT28
  from APT29 on this evidence" beats inventing a name.

## Source grading (Admiralty credibility × reliability)

Grade every source once, at collection time, and carry the grade into the report.

| Reliability of source | Credibility of information |
|---|---|
| **A** Completely reliable | **1** Confirmed by other sources |
| **B** Usually reliable | **2** Probably true |
| **C** Sometimes reliable | **3** Possibly true |
| **D** Not usually reliable | **4** Doubtful |
| **E** Unreliable | **5** Improbable |
| **F** Reliability cannot be judged | **6** Truth cannot be judged |

- Vendor reports from vendors with commercial motive on their own attribution →
  grade the source, do not discard it.
- A single **F6** observation cannot carry a high-confidence judgment no matter
  how plausible it reads.

## ACH worksheet

Rows = evidence items (facts only). Columns = competing hypotheses. Score each cell,
then rank hypotheses by *least inconsistent* evidence, not most consistent.

| Evidence \ Hypothesis | Actor A | Actor B | Actor C (false flag) | Unattributed cluster |
|---|---|---|---|---|
| Shared C2 certificate | ++ | − | − | N |
| TTP overlap with known tooling | ++ | ++ | + | N |
| Working-hours pattern (UTC+3) | ++ | ++ | − | N |
| Language artifacts in payload | ++ | − | − | N |

| Score | Meaning |
|---|---|
| ++ | Strongly consistent (+2) |
| + | Consistent (+1) |
| N | Neutral / not relevant (0) |
| − | Inconsistent (−1) |
| -- | Strongly inconsistent (−2) |

Procedure:
1. List at least three hypotheses, including "actor unknown / unrelated opportunists".
2. Score evidence as consistent/inconsistent/neutral — inconsistency is what
   eliminates, consistency is what corroborates.
3. Hunt for evidence that would *break* the leading hypothesis before accepting it.
4. Report the runner-up and what evidence would flip the ranking.

## Bias catalog — prompts to run before publication

| Bias | Symptom | Antidote prompt |
|---|---|---|
| Mirror-imaging | "They would obviously…" — assuming the adversary shares your doctrine, constraints, budget, or risk aversion | What does their actual constraint set (tooling, language, operating hours, geopolitical window) predict instead? |
| Cherry-picking | Citing the three indicators that fit and omitting the four that do not | List every collected item, including the inconsistent ones, and score them all in the ACH. |
| Confirmation bias | Collecting only after the hypothesis forms | Define what evidence would disprove the hypothesis *before* the next collection tasking. |
| Anchoring | First actor named stays the named actor | Re-run the ACH from scratch with the first hypothesis removed; does the ranking hold? |
| Availability | overweighting the campaign that made the news | Weight evidence by independence, not by how memorable the incident is. |
| Temporal | Treating 6-month-old passive DNS as current | Date every infrastructure claim; re-resolve or mark as historical. |
| False-flag blindness | Shared tooling or leaked keys read as attribution | Ask explicitly: is this evidence *manufacturable* by a third party? |

## Pre-publication analytic checklist

- [ ] Every judgment carries an explicit confidence level using the wording table
- [ ] Every claim is labeled fact, inference, or assumption
- [ ] At least one alternative hypothesis is on the record with its evidence
- [ ] The strongest *disconfirming* evidence is discussed, not just the confirming set
- [ ] Sources are graded; no judgment rests solely on an ungraded source
- [ ] Mirror-imaging tested against the adversary's real constraint set
- [ ] Collection gaps stated instead of papered over with low-confidence prose
