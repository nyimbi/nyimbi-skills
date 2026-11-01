# Analyzing Malicious URL With Urlscan

## API Reference

## Base URL
```
https://urlscan.io/api/v1
```

## Authentication
```
API-Key: YOUR_API_KEY
```

## Submit Scan
```
POST /scan/
```
```json
{"url": "https://example.com", "visibility": "private"}
```
| Field | Values | Description |
|-------|--------|-------------|
| `url` | URL string | URL to scan |
| `visibility` | public/unlisted/private | Scan visibility |

Response: `{"uuid": "...", "result": "https://urlscan.io/result/UUID/", "api": "..."}`

## Get Result
```
GET /result/{uuid}/
```
Returns 404 while scanning, 200 when complete.

## Search
```
GET /search/?q=domain:example.com&size=100
```
Query fields: `domain:`, `ip:`, `server:`, `country:`, `filename:`, `hash:`

## Result Structure
| Field | Description |
|-------|-------------|
| `page.url` | Final URL after redirects |
| `page.domain` | Domain name |
| `page.ip` | Resolved IP |
| `page.country` | Server country |
| `page.status` | HTTP status code |
| `page.title` | Page title |
| `page.server` | Server header |
| `page.tlsIssuer` | TLS certificate issuer |
| `verdicts.overall.malicious` | Boolean malicious verdict |
| `verdicts.overall.score` | Risk score (0-100) |
| `lists.ips` | List of contacted IPs |
| `lists.certificates` | TLS certificates observed |
| `stats.resourceStats` | Resource type statistics |

## Screenshot
```
GET /screenshots/{uuid}.png
```

## DOM Snapshot
```
GET /dom/{uuid}/
```

## Rate Limits
- Free: 100 scans/day, 1000 searches/day
- Paid: Higher limits per plan

---

## Standards and Controls

## MITRE ATT&CK References
- **T1566.002**: Phishing: Spearphishing Link
- **T1204.001**: User Execution: Malicious Link
- **T1608.005**: Stage Capabilities: Link Target
- **T1071.001**: Application Layer Protocol: Web Protocols
- **T1102**: Web Service (for C2 via web)

## URLScan.io API Reference
| Endpoint | Method | Description |
|---|---|---|
| `/api/v1/scan/` | POST | Submit URL for scanning |
| `/api/v1/result/{uuid}/` | GET | Get scan results |
| `/api/v1/search/?q=` | GET | Search scan database |
| `/api/v1/result/{uuid}/screenshot/` | GET | Get page screenshot |
| `/api/v1/result/{uuid}/dom/` | GET | Get rendered DOM |

### Search Query Syntax
- `domain:example.com` - Search by domain
- `ip:1.2.3.4` - Search by IP
- `server:nginx` - Search by web server
- `filename:login.php` - Search by filename
- `hash:abc123` - Search by resource hash
- `page.domain:example.com AND date:>now-7d` - Combined queries

## Industry Standards
- **NIST SP 800-83**: Guide to Malware Incident Prevention and Handling
- **NIST SP 800-86**: Guide to Integrating Forensic Techniques into Incident Response
- **RFC 3986**: Uniform Resource Identifier (URI) syntax

## URL Classification Indicators
| Indicator | Risk Level | Description |
|---|---|---|
| Domain age < 7 days | Critical | Very recently registered |
| Domain age < 30 days | High | Recently registered |
| Free TLS cert (Let's Encrypt) with brand impersonation | High | Common phishing pattern |
| URL shortener | Medium | Obfuscates destination |
| Credential input form on non-brand domain | Critical | Credential harvesting |
| JavaScript obfuscation | High | Evasion technique |
| Multiple redirects | Medium | Chain obfuscation |
| Data URI scheme | High | Inline content, hard to trace |

---

## Workflows

## Workflow 1: URL Triage Pipeline

```
Suspicious URL received (from user report / email gateway / SIEM)
  |
  v
[Step 1: Defang and document URL]
  +-- Replace http with hxxp, . with [.]
  +-- Record original context (email subject, sender, timestamp)
  |
  v
[Step 2: Submit to URLScan (private visibility)]
  +-- POST to /api/v1/scan/
  +-- Wait for scan completion (poll /api/v1/result/{uuid}/)
  |
  v
[Step 3: Analyze results]
  +-- Review screenshot for brand impersonation
  +-- Check redirect chain (original URL vs final URL)
  +-- Examine DOM for login forms / credential inputs
  +-- Review network requests for suspicious endpoints
  +-- Check SSL certificate details
  |
  v
[Step 4: Classify]
  +-- Phishing (credential harvesting)
  +-- Malware delivery
  +-- Scam / fraud
  +-- Benign (false positive)
  |
  v
[Step 5: Action]
  +-- If malicious: Extract IOCs, block domain/IP, update filters
  +-- If benign: Document and close
  +-- If uncertain: Escalate for deeper analysis
```

## Workflow 2: Bulk URL Analysis

```
URL list from email gateway / threat feed
  |
  v
[Batch submit to URLScan API]
  +-- Rate limit: 2 submissions/second (free tier)
  +-- Use private visibility for sensitive URLs
  |
  v
[Collect all results]
  +-- Poll each scan UUID for completion
  +-- Download screenshots and DOM content
  |
  v
[Automated triage]
  +-- Flag: credential input forms detected
  +-- Flag: brand impersonation in screenshot
  +-- Flag: known phishing infrastructure (IP/ASN)
  +-- Flag: newly registered domains
  |
  v
[Generate report]
  +-- Categorized URL list (malicious / suspicious / clean)
  +-- IOC extract for blocking
  +-- Statistics summary
```

## Workflow 3: IOC Extraction and Enrichment

```
URLScan result available
  |
  v
[Extract from scan]
  +-- All domains contacted
  +-- All IPs contacted
  +-- SSL certificate fingerprints
  +-- JavaScript file hashes
  +-- Page resource hashes
  +-- Final redirect URL
  |
  v
[Cross-reference]
  +-- VirusTotal: domain/IP/hash reputation
  +-- PhishTank: known phishing URL database
  +-- WHOIS: domain registration details
  +-- AbuseIPDB: IP abuse reports
  +-- Google Safe Browsing: malware/phishing flags
  |
  v
[Compile IOC package]
  +-- STIX/TAXII format for TIP
  +-- CSV for firewall/proxy rules
  +-- JSON for SIEM enrichment
```

---

## Working Template

## Analysis Information
- **Analyst**: [Name]
- **Date**: [YYYY-MM-DD]
- **Case ID**: [CASE-XXXX]
- **Source**: [User report / Email gateway / SIEM alert]

## URL Details
| Field | Value |
|---|---|
| Original URL | |
| Defanged URL | hxxps://... |
| Final URL (after redirects) | |
| URLScan UUID | |
| Scan visibility | private/public |

## Page Analysis
| Field | Value |
|---|---|
| Page Title | |
| HTTP Status | |
| Server | |
| Domain | |
| IP Address | |
| ASN | |
| Country | |
| Login Form Detected | Yes/No |

## TLS Certificate
| Field | Value |
|---|---|
| Issuer | |
| Subject | |
| Valid From | |
| Valid To | |
| Certificate Age | |

## Redirect Chain
| # | URL | Status |
|---|---|---|
| 1 (original) | | |
| 2 | | |
| 3 (final) | | |

## Threat Intelligence Cross-Reference
| Source | Result | Score |
|---|---|---|
| URLScan Verdict | | |
| VirusTotal | /XX engines | |
| PhishTank | | |
| Google Safe Browsing | | |
| AbuseIPDB | | |

## IOCs Extracted
### Domains
| Domain | Role | Reputation |
|---|---|---|
| | | |

### IP Addresses
| IP | ASN | Country | Reputation |
|---|---|---|---|
| | | | |

### File Hashes
| Hash (SHA-256) | Type | Size |
|---|---|---|
| | | |

## Classification
- [ ] Phishing - Credential Harvesting
- [ ] Phishing - Malware Delivery
- [ ] Scam / Fraud
- [ ] Benign
- [ ] Inconclusive

## Recommended Actions
- [ ] Block domain at proxy/firewall
- [ ] Block IP at firewall
- [ ] Add to email gateway blocklist
- [ ] Submit to PhishTank / APWG
- [ ] Notify affected users
- [ ] Request domain takedown

## Notes
[Additional analysis observations]
