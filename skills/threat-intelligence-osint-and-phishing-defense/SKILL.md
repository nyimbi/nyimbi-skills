---
name: threat-intelligence-osint-and-phishing-defense
description: >-
  Produce external threat intelligence and adversary knowledge: run the
  intelligence lifecycle (direction, collection, processing, analysis,
  dissemination, feedback), collect and enrich OSINT, share indicators through
  MISP/STIX/TAXII, profile and attribute threat actors, track campaigns and
  adversary infrastructure, monitor the dark web, brand impersonation,
  typosquatting, certificate transparency and supply-chain packages, and defend
  against phishing — email gateway tuning, QR (quishing) phishing,
  adversary-in-the-middle kits, and anti-phishing simulation programs. Use when
  the user asks to "track this threat actor", "monitor for typosquatting or
  lookalike domains", "set up MISP or STIX/TAXII sharing", "triage and enrich
  these IOCs", "write a threat intelligence report", "analyze this phishing
  email", "detect AiTM or QR-code phishing", "monitor the dark web for leaked
  credentials", or "run a phishing simulation". Do not use for responding to an
  observed compromise (security-incident-response-and-soc), hypothesis-driven
  hunting or detection-rule engineering (threat-hunting-and-detection), or
  reverse engineering a sample (malware-analysis-and-reverse-engineering).
---

# Threat Intelligence, OSINT, and Phishing Defense

Threat intelligence is a question-answering service, not a feed subscription.
Everything in this skill hangs off the intelligence lifecycle — direction →
collection → processing → analysis → dissemination → feedback — and every
product must name the requirement it answers, the evidence behind it, and the
confidence level attached to each judgment. A link list with no requirement and
no confidence language is data, not intelligence; produce the link list only as
an appendix.

Phishing lives here because phishing is an intelligence problem as much as a SOC
problem: the lure reveals actor intent, the infrastructure reveals capability and
tradecraft, the targeting reveals who matters to the adversary and why. This
skill produces that knowledge and the standing defenses built from it. The
response to a user who already clicked — containment, eradication, forensics —
belongs to `security-incident-response-and-soc`.

## When to use

- Establishing or running a CTI program: writing PIRs, collection plans,
  audience/product mapping, feedback loops, program metrics
- Collecting OSINT on actors, infrastructure, domains, and leaked credentials
  (passive by default), and pivoting across WHOIS, passive DNS, CT, Shodan
- Triaging and enriching IOCs from feeds, alerts, or phishing submissions, and
  deciding block vs. monitor vs. whitelist
- Sharing or consuming intelligence: MISP events and feeds, STIX 2.1 objects,
  TAXII collections, OpenCTI graphs, ISAC exchange
- Profiling and attribution: who is behind this campaign, what they do, whom
  they target, how confident we are, and what would change our mind
- Standing monitoring: dark web forums/leak sites/paste sites, brand and
  typosquatting domains, certificate transparency, supply-chain packages
- Phishing: analyzing a sample or campaign, tuning gateways for spearphishing
  and BEC, defending against quishing and AiTM, building user-report workflows
- Designing anti-phishing simulation and awareness programs, and reading their
  results as collection input rather than as a scoreboard alone

**Do not use for** — `security-incident-response-and-soc` when a compromise has
been observed and the job is containment, eradication, or the IR timeline;
`threat-hunting-and-detection` when the job is proactive hypothesis-driven search
inside your environment or writing Sigma/EDR detection rules; and
`malware-analysis-and-reverse-engineering` when the job is deciding what a
sample *does* — its extracted IOCs and TTPs come back here for enrichment and
dissemination. Authorized reconnaissance during an engagement is
`offensive-security-and-red-teaming`, even when it uses the same OSINT tools.

## Workflow

1. **Direction — write the requirement before collecting.** Turn stakeholder
   questions into answerable requirements in the form "What is the capability
   and intent of [actor] to attack [asset] using [vector] this quarter?" Pick
   product level (strategic 6–24 months / operational 1–6 months / tactical
   hours–days), audience, TLP, and due date for each. Standing watches get
   standing requirements: lookalike domains, certificate issuance on owned
   zones, credential mentions, package names, sector campaigns. If available
   sources cannot answer a requirement, log it as a collection gap and say so —
   never fill the gap with a confident-sounding guess.
   *Output: numbered requirement list with owner, priority, source plan, due date.*

2. **Collection — gather against requirements, passive first.** Map each
   requirement to sources: OSINT (WHOIS, passive DNS, CT logs, Shodan,
   VirusTotal, URLScan), commercial and open-source feeds, MISP communities and
   ISAC exchange, dark web/paste/ransomware leak sites, package registries and
   SBOMs, and internal telemetry (phishing submission mailbox, user reports).
   Collection stays passive — no packets to target infrastructure — unless
   written authorization permits active recon. Record provenance (source,
   retrieval time, TLP) for every item and reject anything you cannot date.
   Watch for stale data: six-month-old passive DNS is history, not current
   truth.
   *Output: raw collection set with provenance and freshness stamps.*

3. **Processing — normalize, defang, dedupe, enrich, qualify.** Classify each
   observable by type; defang (`evil[.]com`) for any human-facing use; dedupe on
   value *and* type so one indicator echoed by five aggregators does not count
   as five sources; enrich from at least three independent sources; then assign
   confidence, disposition, and expiry. High-stakes blocking requires ≥3
   independent sources and excludes shared/CDN infrastructure.
   *Output: qualified indicator set — disposition table and TTL policy in
   [ioc-quality.md](references/ioc-quality.md).*

4. **Analysis — separate fact, inference, and assumption; kill the bias.**
   Structure the problem with the Diamond Model (adversary, capability,
   infrastructure, victim), map behaviour to MITRE ATT&CK, and where actor
   identity is at issue run Analysis of Competing Hypotheses rather than
   arguing from a hunch. Enforce these disciplines on every claim:

   | Discipline | Rule |
   |---|---|
   | Fact / inference / assumption | Label each claim; an assumption that would falsify the judgment must be stated with it |
   | Confidence language | "assess with high confidence" / "assess" / "suggests" — one explicit level per judgment, never implied by hedging |
   | Mirror-imaging | The adversary does not share your constraints, doctrine, or risk aversion — test every "they would obviously…" claim against their actual constraint set |
   | Cherry-picking | Score *all* collected evidence in the ACH, including the items that contradict your leading hypothesis |
   | Attribution | Requires multiple independent evidence categories to converge; infrastructure overlap alone is manufactured-able and does not name an actor |

   When evidence does not converge, publish "cluster of related activity,
   actor unidentified" with the alternatives on the record — that is an
   acceptable, useful product.
   *Output: findings with explicit confidence, alternative hypotheses, and the
   disconfirming evidence discussed — full tables in
   [confidence-language.md](references/confidence-language.md).*

5. **Actor and campaign products.** Build the dossier: identity and aliases
   (vendor names differ — APT29 = Cozy Bear = Midnight Blizzard), motivation,
   targeting, capability, campaign history, top techniques per tactic, and
   infrastructure patterns; compare the technique list against your detection
   coverage to expose gaps. Track infrastructure over time (passive DNS, CT,
   WHOIS history, ASN) and correlate incidents across time and organizations
   into campaigns using shared indicators and TTP overlap. Refresh profiles at
   least quarterly — IOC-centric profiles rot in weeks.
   *Output: actor dossier + campaign timeline + gap list.*

6. **Treat phishing as an intelligence problem.** From a reported or observed
   message, extract four things — then decide what they mean:
   - *Header and authentication*: Received chain (bottom-up), SPF/DKIM/DMARC
     alignment, From/Reply-To mismatch, lookalike registration date.
   - *Lure and intent*: credential harvest, BEC/wire fraud, malware delivery,
     MFA reset, or session-token theft — the lure tells you what the actor wants
     and whom they studied.
   - *Infrastructure*: registrant, hosting, certificate, redirectors, kit
     fingerprints — feed it to the campaign tracker in step 5.
   - *Variant*: quishing arrives as image-only mail whose QR decodes to a
     URL — run the decoded URL through the same pipeline as any other URL and
     remember the scan happens on an unmanaged phone; AiTM (Tycoon 2FA,
     EvilProxy, Evilginx, Sneaky 2FA) sits a reverse proxy in front of the real
     login and steals the session cookie — the tells are sign-in/session
     mismatch, non-native authentication infrastructure, and impossible
     travel, not a bad URL reputation score.
   Standing defenses come from the same picture: gateway impersonation/URL/
   attachment layers, DMARC enforcement, reporting button, and simulations.
   Simulation results and user reports are *collection sources* — they tell you
   which lures currently work.
   *Output: phishing analysis with header verdict, lure intent, infrastructure
   IOCs, and campaign linkage.*

7. **Dissemination — match product to audience, TLP to sensitivity, and treat
   each platform family as one topic.** Executives get decisions, SOC gets
   defanged indicators and detections, partners get what their TLP permits.
   Four families in this skill each merge several reference files; use them as
   single coherent topics, not competing instructions:

   | One topic | What it covers | Reference files |
   |---|---|---|
   | STIX / TAXII sharing | Model objects (indicator, campaign, relationship with confidence + TLP markings), consume collections with `added_after` pagination and `spec_version` checks, publish back to shared collections, and host a TAXII server (OpenTAXII) only when you are the provider | [implementing-stix-taxii-feed-integration](references/implementing-stix-taxii-feed-integration.md) · [processing-stix-taxii-feeds](references/processing-stix-taxii-feeds.md) · [implementing-taxii-server-with-opentaxii](references/implementing-taxii-server-with-opentaxii.md) |
   | MISP sharing | Author events with PyMISP (attributes, galaxies, ATT&CK tags, TLP, distribution levels), curate and sync feeds at the instance level, and push validated indicators onward to SIEM/Sigma | [performing-threat-intelligence-sharing-with-misp](references/performing-threat-intelligence-sharing-with-misp.md) · [collecting-threat-intelligence-with-misp](references/collecting-threat-intelligence-with-misp.md) · [building-threat-feed-aggregation-with-misp](references/building-threat-feed-aggregation-with-misp.md) |
   | Dark-web monitoring | One program: scope sources (forums, marketplaces, paste sites, breach corpora, ransomware leak sites), set collection cadence, and maintain OPSEC — executed source-by-source (HIBP, paste scraping, Tor forums) rather than as two competing workflows | [performing-dark-web-monitoring-for-threats](references/performing-dark-web-monitoring-for-threats.md) · [monitoring-darkweb-sources](references/monitoring-darkweb-sources.md) |
   | Package typosquatting | One detection problem — misspelled/brandjacked npm and PyPI names — solved either by corpus-driven edit-distance and keyboard-proximity scanning or by registry-API heuristics (publish date, download disparity, author mismatch); pick one, or run both and merge scores. Domain lookalikes are a separate topic (`dnstwist`, step 2) | [detecting-typosquatting-packages](references/detecting-typosquatting-packages.md) · [detecting-typosquatting-packages-in-npm-pypi](references/detecting-typosquatting-packages-in-npm-pypi.md) |

   *Output: shareable package — report for humans, defanged indicator table,
   machine-readable STIX bundle or MISP event for platforms.*

8. **Feedback — close the loop or the program decays.** Within a week of
   dissemination, ask each consumer: did the product answer the requirement,
   what was missing, what was too late? Track PIR coverage, IOC true-positive
   rate, time-to-disseminate, report rate from users and simulations, and
   false-positive volume on shared indicators. Retire expired indicators,
   re-task collection against unanswered requirements, and retire requirements
   nobody consumes.
   *Output: feedback log + revised requirement list feeding step 1.*

## Quality bar

- [ ] Every product names the requirement (PIR/IR) it answers and the audience
      it was built for; unconsumed requirements are visible as gaps
- [ ] Every judgment carries one explicit confidence level, and every claim is
      labeled fact, inference, or assumption
- [ ] At least one alternative hypothesis is on the record for any attribution
      claim, with the strongest disconfirming evidence discussed; mirror-imaging
      and cherry-picking checks are done, not assumed
- [ ] Every indicator is defanged in documents, has source, retrieval date,
      confidence, disposition, and an expiry
- [ ] Blocking recommendations rest on ≥3 independent sources and exclude
      shared/CDN/SaaS infrastructure
- [ ] TLP is applied per product, matches source sensitivity, and no source
      identification leaks into TLP:AMBER/RED items
- [ ] Infrastructure and campaign claims are dated; anything stale is flagged or
      dropped
- [ ] Phishing analysis states header/authentication verdict, lure intent,
      infrastructure, and campaign linkage — never just "malicious"
- [ ] Near-duplicate platform families (STIX/TAXII, MISP, dark web, package
      typosquatting) are delivered as one coherent topic per family
- [ ] Feedback and metrics from the last cycle are recorded before the next
      collection plan is written

## Reference map

Per-technique detail lives in
[`references/technique-index.md`](references/technique-index.md) — one row per
technique (76 total) with a description and the tool-level API/workflow content.
Load the file for the technique you are executing rather than reading the index.

| Situation | Open |
|---|---|
| Confidence wording, source grading, ACH worksheet, bias checks | [confidence-language.md](references/confidence-language.md) |
| Enrichment source matrix, disposition tiers, TTLs, defanging, sharing mapping | [ioc-quality.md](references/ioc-quality.md) |
| Lifecycle setup: PIRs, collection management, feedback loops, metrics | [managing-intelligence-lifecycle](references/managing-intelligence-lifecycle.md) · [implementing-threat-intelligence-lifecycle-management](references/implementing-threat-intelligence-lifecycle-management.md) |
| Passive OSINT collection, pivots, SpiderFoot automation, AI-assisted correlation | [collecting-open-source-intelligence](references/collecting-open-source-intelligence.md) · [performing-osint-with-spiderfoot](references/performing-osint-with-spiderfoot.md) · [performing-ai-driven-osint-correlation](references/performing-ai-driven-osint-correlation.md) |
| IOC triage, enrichment, URL/hash/IP reputation, disposition decisions | [analyzing-indicators-of-compromise](references/analyzing-indicators-of-compromise.md) · [automating-ioc-enrichment](references/automating-ioc-enrichment.md) · [analyzing-malicious-url-with-urlscan](references/analyzing-malicious-url-with-urlscan.md) · [performing-malware-hash-enrichment-with-virustotal](references/performing-malware-hash-enrichment-with-virustotal.md) · [performing-ip-reputation-analysis-with-shodan](references/performing-ip-reputation-analysis-with-shodan.md) |
| Indicator lifecycle: extraction, dedupe, TTL, retirement | [performing-indicator-lifecycle-management](references/performing-indicator-lifecycle-management.md) |
| Feed evaluation, TIP selection, platform maturity | [analyzing-threat-intelligence-feeds](references/analyzing-threat-intelligence-feeds.md) · [evaluating-threat-intelligence-platforms](references/evaluating-threat-intelligence-platforms.md) · [building-threat-intelligence-platform](references/building-threat-intelligence-platform.md) |
| STIX/TAXII: model, consume, publish, host (one topic, four files) | [implementing-stix-taxii-feed-integration](references/implementing-stix-taxii-feed-integration.md) · [processing-stix-taxii-feeds](references/processing-stix-taxii-feeds.md) · [implementing-taxii-server-with-opentaxii](references/implementing-taxii-server-with-opentaxii.md) · [implementing-security-information-sharing-with-stix2](references/implementing-security-information-sharing-with-stix2.md) · [building-ioc-defanging-and-sharing-pipeline](references/building-ioc-defanging-and-sharing-pipeline.md) |
| MISP: author/share, collect, aggregate, operationalize into detections (one topic) | [performing-threat-intelligence-sharing-with-misp](references/performing-threat-intelligence-sharing-with-misp.md) · [collecting-threat-intelligence-with-misp](references/collecting-threat-intelligence-with-misp.md) · [building-threat-feed-aggregation-with-misp](references/building-threat-feed-aggregation-with-misp.md) · [operationalizing-misp-threat-feeds](references/operationalizing-misp-threat-feeds.md) |
| OpenCTI knowledge graph modelling and enrichment pipelines | [modeling-threats-with-opencti](references/modeling-threats-with-opencti.md) · [building-ioc-enrichment-pipeline-with-opencti](references/building-ioc-enrichment-pipeline-with-opencti.md) |
| Actor profiling, ATT&CK group TTPs, Navigator coverage layers | [profiling-threat-actor-groups](references/profiling-threat-actor-groups.md) · [building-threat-actor-profile-from-osint](references/building-threat-actor-profile-from-osint.md) · [analyzing-threat-actor-ttps-with-mitre-attack](references/analyzing-threat-actor-ttps-with-mitre-attack.md) · [analyzing-threat-actor-ttps-with-mitre-navigator](references/analyzing-threat-actor-ttps-with-mitre-navigator.md) · [analyzing-apt-group-with-mitre-navigator](references/analyzing-apt-group-with-mitre-navigator.md) |
| Attribution evidence, ACH, Diamond Model, campaign correlation, kill chain | [analyzing-campaign-attribution-evidence](references/analyzing-campaign-attribution-evidence.md) · [implementing-diamond-model-analysis](references/implementing-diamond-model-analysis.md) · [correlating-threat-campaigns](references/correlating-threat-campaigns.md) · [analyzing-cyber-kill-chain](references/analyzing-cyber-kill-chain.md) |
| Adversary infrastructure tracking (C2, passive DNS, WHOIS, certs) | [building-adversary-infrastructure-tracking-system](references/building-adversary-infrastructure-tracking-system.md) · [tracking-threat-actor-infrastructure](references/tracking-threat-actor-infrastructure.md) |
| Dark web, paste sites, breach corpora, ransomware leak sites (one monitoring topic) | [performing-dark-web-monitoring-for-threats](references/performing-dark-web-monitoring-for-threats.md) · [monitoring-darkweb-sources](references/monitoring-darkweb-sources.md) · [performing-paste-site-monitoring-for-credentials](references/performing-paste-site-monitoring-for-credentials.md) · [analyzing-ransomware-leak-site-intelligence](references/analyzing-ransomware-leak-site-intelligence.md) |
| Brand impersonation and lookalike domains | [performing-brand-monitoring-for-impersonation](references/performing-brand-monitoring-for-impersonation.md) · [analyzing-typosquatting-domains-with-dnstwist](references/analyzing-typosquatting-domains-with-dnstwist.md) |
| Certificate transparency: phishing discovery vs. owned-zone auditing | [analyzing-certificate-transparency-for-phishing](references/analyzing-certificate-transparency-for-phishing.md) · [auditing-tls-certificate-transparency-logs](references/auditing-tls-certificate-transparency-logs.md) |
| Package typosquatting and dependency confusion (one detection topic) | [detecting-typosquatting-packages](references/detecting-typosquatting-packages.md) · [detecting-typosquatting-packages-in-npm-pypi](references/detecting-typosquatting-packages-in-npm-pypi.md) · [detecting-dependency-confusion](references/detecting-dependency-confusion.md) · [detecting-malicious-npm-packages](references/detecting-malicious-npm-packages.md) |
| Supply-chain compromise intelligence: SBOMs, provenance, trojanized updates | [analyzing-sbom-for-supply-chain-vulnerabilities](references/analyzing-sbom-for-supply-chain-vulnerabilities.md) · [generating-and-analyzing-sboms](references/generating-and-analyzing-sboms.md) · [implementing-sigstore-for-software-signing](references/implementing-sigstore-for-software-signing.md) · [verifying-build-provenance-with-slsa-sigstore](references/verifying-build-provenance-with-slsa-sigstore.md) |
| Malware family context for intelligence (families, extraction, platforms) | [analyzing-malware-family-relationships-with-malpedia](references/analyzing-malware-family-relationships-with-malpedia.md) · [performing-malware-ioc-extraction](references/performing-malware-ioc-extraction.md) |
| Phishing email analysis, gateway layers, BEC, DMARC enforcement | [detecting-spearphishing-with-email-gateway](references/detecting-spearphishing-with-email-gateway.md) · [implementing-dmarc-dkim-spf-email-security](references/implementing-dmarc-dkim-spf-email-security.md) · [performing-dmarc-policy-enforcement-rollout](references/performing-dmarc-policy-enforcement-rollout.md) · [detecting-business-email-compromise](references/detecting-business-email-compromise.md) · [detecting-business-email-compromise-with-ai](references/detecting-business-email-compromise-with-ai.md) |
| Gateway product configuration and sandboxing | [implementing-proofpoint-email-security-gateway](references/implementing-proofpoint-email-security-gateway.md) · [implementing-mimecast-targeted-attack-protection](references/implementing-mimecast-targeted-attack-protection.md) · [implementing-google-workspace-phishing-protection](references/implementing-google-workspace-phishing-protection.md) · [implementing-email-sandboxing-with-proofpoint](references/implementing-email-sandboxing-with-proofpoint.md) |
| User-report button and triage workflow | [building-phishing-reporting-button-workflow](references/building-phishing-reporting-button-workflow.md) |
| QR-code phishing (quishing) detection | [detecting-qr-code-phishing-with-email-security](references/detecting-qr-code-phishing-with-email-security.md) |
| Adversary-in-the-middle phishing, MFA bypass, session theft | [performing-adversary-in-the-middle-phishing-detection](references/performing-adversary-in-the-middle-phishing-detection.md) |
| Vishing and deepfake audio in voice phishing | [detecting-deepfake-audio-in-vishing-attacks](references/detecting-deepfake-audio-in-vishing-attacks.md) |
| Phishing simulation campaigns and awareness programs | [performing-phishing-simulation-with-gophish](references/performing-phishing-simulation-with-gophish.md) · [implementing-anti-phishing-training-program](references/implementing-anti-phishing-training-program.md) |
| Finished intelligence: strategic/operational/tactical reports, flash notes | [generating-threat-intelligence-reports](references/generating-threat-intelligence-reports.md) |
| Sector threat landscape and MISP landscape analytics | [performing-threat-landscape-assessment-for-sector](references/performing-threat-landscape-assessment-for-sector.md) · [analyzing-threat-landscape-with-misp](references/analyzing-threat-landscape-with-misp.md) |
| Turning intel into ATT&CK coverage and attack-pattern libraries | [mapping-mitre-attack-techniques](references/mapping-mitre-attack-techniques.md) · [building-attack-pattern-library-from-cti-reports](references/building-attack-pattern-library-from-cti-reports.md) |
| Validating intel against the environment (coordinate with threat hunting) | [hunting-advanced-persistent-threats](references/hunting-advanced-persistent-threats.md) · [performing-threat-emulation-with-atomic-red-team](references/performing-threat-emulation-with-atomic-red-team.md) |

Executable helpers live in `scripts/<technique-name>/` (`agent.py`,
`process.py`) — read the reference file first to learn what the script expects,
then run it.

## Output format

Deliver finished intelligence in one shape; adapt depth to product level.

```markdown
# <Topic> — Intelligence Assessment

## Metadata
Report ID: CTI-YYYY-NNNN | Date: YYYY-MM-DD | Analyst:
Product level: strategic | operational | tactical
TLP: <RED | AMBER+STRICT | AMBER | GREEN | CLEAR>   Confidence: <high | moderate | low>
PIRs answered: <numbered requirements from step 1>

## Key judgments
1. <One-sentence, verb-led judgment with confidence qualifier. Max 5, numbered
   for citation in the body.>
2. ...

## Analysis
### Key judgment 1
- Fact: <sourced, observable, dated>
- Inference: <what the facts imply, and the logic>
- Assumption: <premise required, and what would falsify it>
- Confidence: <level + why the evidence supports it>
- Alternative considered: <runner-up hypothesis and what would flip the ranking>

## Adversary / campaign picture
Actor | aliases | motivation | targeting | ATT&CK techniques |
infrastructure patterns | campaign timeline | activity status

## Indicators
| Type | Value (defanged) | Context | Source | Retrieved | Confidence | Disposition | Expires |

## Recommendations
- Immediate (≤24h): <action — owner>
- Near-term (≤2 weeks): <action — owner>
- Structural: <program/control change — owner>

## Collection gaps
<Requirement we could not answer, why, and what collection would close it.>

## Sources
[1] <source — Admiralty grade — date — TLP> ...
```

For an IOC-only deliverable (tactical bulletin or feed push), the indicator table
above is the product: same columns, every value defanged, plus the machine-readable
mirror as a STIX 2.1 bundle or MISP event with `confidence` and `to_ids` mapped
from the disposition tiers in [ioc-quality.md](references/ioc-quality.md). No
narrative is required, but context and expiry are — an indicator without them is
not shareable intelligence.
