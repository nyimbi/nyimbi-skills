# Indicator Qualification — Enrichment Sources, TTLs, and Sharing Rules

Reference tables for turning a raw observable into an indicator worth blocking,
sharing, or retiring.

## Enrichment source matrix

Query more than one source; each has a characteristic failure mode.

| Source | Best for | Query with | Characteristic failure |
|---|---|---|---|
| VirusTotal | Hash/URL/domain reputation, AV consensus, sandbox behaviour | `vt-py`, v3 API | 0 detections ≠ benign (custom tooling scores 0 for weeks); consensus can lag |
| AbuseIPDB | IP abuse reports, hosting context | v2 `check` | Community reports skew toward shared/CDN IPs |
| MalwareBazaar (abuse.ch) | Hash → family tag, YARA associations | POST `get_info` | Coverage limited to publicly shared samples |
| URLScan.io | Phishing page screenshots, DOM, redirect chains | POST `scan`, poll result | Scanning the URL notifies nobody but costs you stealth; also indexes benign pages |
| Shodan | Open ports, banners, certs, hosting provider for an IP | `api.shodan.io` | Shows today's tenant, not who owned it last month |
| Passive DNS / WHOIS history | Infrastructure pivots, registrant reuse, first-seen dates | SecurityTrails, RiskIQ | Privacy-redacted registrant; staleness — always record retrieval date |
| MISP / TIP | Campaign context, sightings, whether others already saw it | PyMISP `search` | A hit means "someone reported it", not "it is malicious" |
| Certificate transparency | Lookalike certs, subdomains, phishing staging hosts | crt.sh | Certs are issued for abandoned domains too; check validity window |

Hard rule for high-stakes blocking: **≥3 independent sources**, and at least one
that is not a reputation aggregate. A CDN, cloud, or SaaS IP that appears in one
feed is not a block candidate.

## Disposition tiers

| Tier | Confidence | Typical signal | Action |
|---|---|---|---|
| Block | ≥70% | ≥15 AV detections, AbuseIPDB ≥70, or matches a known campaign/family | Add to blocklist with expiry date |
| Monitor | 40–69% | 5–14 detections, moderate abuse, no campaign context | Alert on touch, do not block |
| Whitelist / investigate | <40% | ≤4 detections, no abuse, legitimate service | Confirm business use; document exclusion |
| False positive | — | Benign artifact incorrectly flagged | Record in the exclusion list so it stops recurring |

## TTL policy (indicator lifecycle)

| Indicator type | Default TTL | Why |
|---|---|---|
| IPv4/IPv6 address | 30 days | Hosting is repurposed; IPs are recycled fast |
| Domain / FQDN | 90 days | Longer-lived, but parked domains get resold |
| URL | 30 days | Paths churn; re-check before renewal |
| File hash (SHA-256) | Indefinite while sample still circulates | Content-addressed; does not age — but retire when superseded by a new family variant |
| Email sender / subject / artifact | 14–30 days | Lure themes rotate weekly |

An indicator with no expiry is a future false positive. Every indicator written to
a blocklist carries an owner and an expiry; renewal requires re-validation, not
habit.

## Defanging conventions

- Documents, tickets, chat, and email: `evil[.]com`, `hxxps://evil[.]com/path`,
  `198[.]51[.]100[.]7`, `user[at]evil[.]com`.
- Refang only in code that is deliberately contacting the indicator — never in a
  paste or report body.
- Anything pasted live into a wiki or ticket may be fetched by a link scanner;
  defanged text cannot.

## Confidence mapping when publishing

| Internal disposition | STIX `confidence` | MISP `to_ids` |
|---|---|---|
| Block | 70–100 | `True` (detect/exportable) |
| Monitor | 40–69 | `True` only if sighting-confirmed |
| Whitelist / investigate | 0–39 | `False` (context only) |
| False positive | 0 | `False`, tagged `FP` and excluded |

`to_ids=False` attributes are context, not detections — sending them to a
blocklist is how shared intelligence turns into an outage.

## Weak-signal pitfalls

- **Low AV count**: zero-day and APT tooling often scores 0/70 on first upload;
  check sandbox behaviour, passive DNS, and MISP before clearing.
- **Shared infrastructure**: blocking `104.21.x.x` (Cloudflare) because one path
  was malicious affects thousands of unrelated tenants.
- **Freshly benign**: an IP clean today may be the C2 tomorrow — reputation is a
  point-in-time observation, date it.
- **Duplicates across feeds**: deduplicate on value *and* type before counting
  sources, or one indicator echoed by five aggregators looks like five sources.
- **Sightings without context**: a MISP sighting tells you it was observed, not
  by whom or in what traffic — record the observing context or discount it.
