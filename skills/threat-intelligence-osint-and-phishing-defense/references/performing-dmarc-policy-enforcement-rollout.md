# Performing Dmarc Policy Enforcement Rollout

## API Reference

## Libraries Used
- **dnspython** (dns.resolver): DNS TXT record queries for DMARC, SPF, DKIM

## CLI Interface

```
python agent.py check --domain example.com
python agent.py audit --domains example.com example.org [--selectors default google k1]
```

## Core Functions

### `check_dmarc(domain)` — Query `_dmarc.<domain>` TXT
### `check_spf(domain)` — Query domain TXT for `v=spf1`
### `check_dkim(domain, selector)` — Query `<selector>._domainkey.<domain>`
### `audit_domains(domains, selectors)` — Full DMARC/SPF/DKIM audit with scoring

## DMARC Policy Levels
| Policy | Enforcement | Score |
|--------|------------|-------|
| `none` | No enforcement (monitoring only) | 0 |
| `quarantine` | Suspicious mail sent to spam | +20 |
| `reject` | Unauthorized mail rejected | +40 |

## Dependencies
```
pip install dnspython>=2.4
```

---

## Standards and Controls

## Core Protocol Standards
- **RFC 7489**: Domain-based Message Authentication, Reporting, and Conformance (DMARC)
- **RFC 7208**: Sender Policy Framework (SPF) for Authorizing Use of Domains in Email
- **RFC 6376**: DomainKeys Identified Mail (DKIM) Signatures
- **RFC 8616**: Email Authentication for Internationalized Mail
- **RFC 8601**: Message Header Field for Indicating Message Authentication Status

## Regulatory Requirements (2025)
- **Google Bulk Sender Requirements**: DMARC required for senders of 5,000+ messages/day to Gmail
- **Yahoo Sender Requirements**: DMARC authentication required for bulk senders
- **PCI DSS 4.0 Requirement 5.3**: Anti-phishing mechanisms including email authentication
- **NIST SP 800-177 Rev.1**: Trustworthy Email guidance

## DMARC Policy Progression
| Phase | Duration | Record | pct | Monitoring |
|---|---|---|---|---|
| Discovery | 2-4 weeks | p=none | N/A | Daily report review |
| Soft enforce | 4-6 weeks | p=quarantine | 10->100 | Twice-weekly review |
| Hard enforce | 4-6 weeks | p=reject | 10->100 | Weekly review |
| Maintenance | Ongoing | p=reject | 100 | Monthly review |

## SPF Lookup Limit
- Maximum 10 DNS lookups per SPF evaluation (RFC 7208 Section 4.6.4)
- Each `include:`, `a:`, `mx:`, `redirect=`, and `exists:` counts as one lookup
- Exceeding 10 lookups causes SPF permerror (treated as fail by some receivers)
- Use SPF flattening tools to stay within limit

## MITRE ATT&CK References
- **T1566.001**: Phishing: Spearphishing Attachment
- **T1566.002**: Phishing: Spearphishing Link
- **T1586.002**: Compromise Accounts: Email Accounts
- **T1656**: Impersonation

---

## Workflows

## Workflow 1: DMARC Phased Rollout

```
Week 1-2: Discovery
  |
  v
[Inventory all legitimate email sending sources]
  +-- Internal mail servers
  +-- Third-party SaaS (marketing, CRM, support)
  +-- Transactional email services
  +-- Application-generated email
  |
  v
Week 2-4: Foundation
  |
  v
[Configure SPF and DKIM for all sources]
  +-- Publish SPF record with all includes
  +-- Validate SPF under 10 lookup limit
  +-- Generate DKIM keys per sending source
  +-- Test outbound authentication
  |
  v
Week 4-6: Monitor
  |
  v
[Publish p=none DMARC record]
  +-- Collect aggregate reports for 2 weeks
  +-- Analyze: who is sending as your domain?
  +-- Fix alignment failures for legitimate sources
  +-- Identify unauthorized/spoofing sources
  |
  v
Week 6-12: Quarantine
  |
  v
[Move to p=quarantine with gradual pct increase]
  +-- pct=10 (2 weeks) -> check false positives
  +-- pct=25 (2 weeks) -> verify clean
  +-- pct=50 (1 week) -> validate stability
  +-- pct=100 (2 weeks) -> confirm all legitimate passes
  |
  v
Week 12-20: Reject
  |
  v
[Move to p=reject with gradual pct increase]
  +-- pct=10 (2 weeks) -> monitor rejections
  +-- pct=25 (2 weeks) -> verify no legitimate blocked
  +-- pct=50 (1 week) -> near full enforcement
  +-- pct=100 -> FULL ENFORCEMENT ACHIEVED
  |
  v
Ongoing: Maintenance
  +-- Monitor aggregate reports monthly
  +-- Update SPF/DKIM for new sending sources
  +-- Rotate DKIM keys annually
```

## Workflow 2: DMARC Report Analysis

```
Aggregate report received (daily XML)
  |
  v
[Parse report in DMARC analyzer]
  |
  v
[Categorize sending sources]
  +-- PASS: Legitimate, properly authenticated
  +-- FAIL (known): Legitimate source with auth issue -> FIX
  +-- FAIL (unknown): Unauthorized sender -> INVESTIGATE
  |
  v
[For each FAIL (known)]
  +-- Identify missing SPF include or DKIM config
  +-- Update DNS records
  +-- Wait for next report to confirm fix
  |
  v
[For each FAIL (unknown)]
  +-- Is it spoofing? -> Document for enforcement case
  +-- Is it shadow IT? -> Onboard or decommission
  +-- Is it forwarding? -> ARC chain may be needed
```

## Workflow 3: Emergency Rollback

```
Legitimate email being rejected (false positive detected)
  |
  v
[Immediate: Roll back pct or policy]
  +-- Reduce pct to previous stable level
  +-- OR roll back from reject to quarantine
  +-- OR roll back from quarantine to none
  |
  v
[Investigate root cause]
  +-- Check aggregate reports for failing source
  +-- Verify SPF/DKIM configuration for source
  +-- Check for forwarding or mailing list issues
  |
  v
[Fix and re-advance]
  +-- Correct authentication issue
  +-- Verify fix in next report cycle
  +-- Resume gradual pct advancement
```

---

## Working Template

## Sending Source Inventory
| Source | Type | SPF Included | DKIM Configured | Status |
|---|---|---|---|---|
| Exchange Online | Primary mail | include:spf.protection.outlook.com | selector1/selector2 | |
| SendGrid | Transactional | include:sendgrid.net | sg._domainkey | |
| Mailchimp | Marketing | include:servers.mcsv.net | k1._domainkey | |
| Salesforce | CRM | include:_spf.salesforce.com | salesforce._domainkey | |

## DMARC Rollout Schedule
| Week | Phase | Record Change | Monitoring |
|---|---|---|---|
| 1-2 | Discovery | (no DMARC yet) | Audit sending sources |
| 3-4 | SPF/DKIM | (configure auth) | Test outbound auth |
| 5-6 | Monitor | p=none; rua=... | Daily report review |
| 7-8 | Quarantine 10% | p=quarantine; pct=10 | Check false positives |
| 9-10 | Quarantine 50% | p=quarantine; pct=50 | Validate stability |
| 11-12 | Quarantine 100% | p=quarantine; pct=100 | Confirm all passing |
| 13-14 | Reject 10% | p=reject; pct=10 | Monitor rejections |
| 15-16 | Reject 50% | p=reject; pct=50 | Near full enforcement |
| 17-20 | Reject 100% | p=reject | FULL ENFORCEMENT |

## Emergency Rollback Procedure
- [ ] Reduce pct to previous stable value OR
- [ ] Revert policy to previous level (reject->quarantine or quarantine->none)
- [ ] Investigate failing source in DMARC reports
- [ ] Fix authentication issue
- [ ] Resume rollout after confirmation

## Sign-off
| Milestone | Approved By | Date |
|---|---|---|
| SPF/DKIM configured | | |
| p=none deployed | | |
| p=quarantine 100% | | |
| p=reject 100% | | |
