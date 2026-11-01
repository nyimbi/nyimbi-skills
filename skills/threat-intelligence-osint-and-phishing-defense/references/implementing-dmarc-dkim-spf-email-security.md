# Implementing Dmarc Dkim Spf Email Security

## API Reference

## dnspython Lookups

```python
import dns.resolver
# SPF
answers = dns.resolver.resolve("example.com", "TXT")
# DMARC
answers = dns.resolver.resolve("_dmarc.example.com", "TXT")
# DKIM
answers = dns.resolver.resolve("selector._domainkey.example.com", "TXT")
```

## SPF Record Syntax

| Mechanism | Example | Meaning |
|-----------|---------|---------|
| `include:` | `include:_spf.google.com` | Authorize sender |
| `ip4:` | `ip4:203.0.113.0/24` | Allow IP range |
| `-all` | End of record | Hard fail others |
| `~all` | End of record | Soft fail (weak) |
| `+all` | End of record | Allow all (insecure) |

## DMARC Policy Levels

| Policy | Action | Severity if Missing |
|--------|--------|---------------------|
| `p=reject` | Reject failing mail | Recommended |
| `p=quarantine` | Send to spam | Acceptable |
| `p=none` | Monitor only | HIGH risk |

## Recommended DNS Records

```
# SPF
v=spf1 include:_spf.google.com -all

# DMARC
v=DMARC1; p=reject; pct=100; rua=mailto:dmarc@example.com; adkim=s; aspf=s

# DKIM (provider-specific key)
selector._domainkey.example.com TXT "v=DKIM1; k=rsa; p=MIIBIjAN..."
```

### References

- SPF RFC 7208: https://www.rfc-editor.org/rfc/rfc7208
- DMARC RFC 7489: https://www.rfc-editor.org/rfc/rfc7489
- DKIM RFC 6376: https://www.rfc-editor.org/rfc/rfc6376
- dnspython: https://dnspython.readthedocs.io/

---

## Standards and Controls

## RFC Standards
- **RFC 7208 (SPF)**: Sender Policy Framework - authorizing sending hosts via DNS
- **RFC 6376 (DKIM)**: DomainKeys Identified Mail Signatures
- **RFC 7489 (DMARC)**: Domain-based Message Authentication, Reporting and Conformance
- **RFC 8301**: Cryptographic Algorithm and Key Usage Update to DKIM (mandates RSA 2048-bit minimum)
- **RFC 8616**: Email Authentication for Internationalized Mail
- **RFC 8617 (ARC)**: Authenticated Received Chain - preserving authentication through forwarding
- **RFC 7960**: Interoperability Issues between DMARC and Indirect Email Flows
- **RFC 6591**: Authentication Failure Reporting Using ARF
- **RFC 8601**: Authentication-Results header field

## NIST Guidelines
- **NIST SP 800-177 Rev.1**: Trustworthy Email - comprehensive email security deployment guide
  - Section 4.3: Sender Policy Framework
  - Section 4.4: DKIM
  - Section 4.5: DMARC
- **NIST SP 800-45 Ver.2**: Guidelines on Electronic Mail Security

## Government Mandates
- **BOD 18-01 (CISA/DHS)**: Binding Operational Directive requiring all federal agencies to implement DMARC p=reject
- **UK NCSC Mail Check**: Mandates DMARC for government domains
- **Australian ASD Essential Eight**: DMARC listed as a mitigation strategy

## MITRE ATT&CK
- **T1566**: Phishing (all sub-techniques)
- **T1586.002**: Compromise Accounts: Email Accounts
- **T1585.002**: Establish Accounts: Email Accounts

## Industry Best Practices
- **M3AAWG DMARC Training Series**: Messaging Anti-Abuse Working Group deployment guide
- **DMARC.org Implementation Guide**: Step-by-step deployment methodology
- **Google Email Authentication Requirements (2024)**: Bulk senders must have SPF, DKIM, and DMARC

## SPF Syntax Reference

| Mechanism | Description | Example |
|---|---|---|
| `ip4:` | IPv4 address/range | `ip4:192.168.1.0/24` |
| `ip6:` | IPv6 address/range | `ip6:2001:db8::/32` |
| `include:` | Include domain SPF | `include:_spf.google.com` |
| `a` | Domain A record IPs | `a:mail.example.com` |
| `mx` | Domain MX record IPs | `mx` |
| `redirect=` | Use another domain's SPF | `redirect=_spf.example.com` |
| `-all` | Hard fail | Reject unauthorized |
| `~all` | Soft fail | Mark but deliver |
| `?all` | Neutral | No assertion |

## DMARC Tag Reference

| Tag | Required | Description | Values |
|---|---|---|---|
| `v` | Yes | Version | `DMARC1` |
| `p` | Yes | Policy | `none`, `quarantine`, `reject` |
| `rua` | No | Aggregate report URI | `mailto:reports@example.com` |
| `ruf` | No | Forensic report URI | `mailto:forensic@example.com` |
| `pct` | No | Percentage of messages | `0-100` (default 100) |
| `sp` | No | Subdomain policy | `none`, `quarantine`, `reject` |
| `adkim` | No | DKIM alignment | `r` (relaxed), `s` (strict) |
| `aspf` | No | SPF alignment | `r` (relaxed), `s` (strict) |
| `fo` | No | Failure reporting | `0`, `1`, `d`, `s` |

---

## Workflows

## Workflow 1: Phased DMARC Deployment

```
Phase 1: Discovery (Weeks 1-2)
  |
  +-- Inventory all email-sending services
  +-- Identify legitimate sources (marketing, transactional, internal)
  +-- Audit current SPF/DKIM/DMARC records
  |
Phase 2: SPF Setup (Weeks 2-4)
  |
  +-- Create SPF record with all authorized senders
  +-- Start with ~all (soft fail) for monitoring
  +-- Test with email validation tools
  |
Phase 3: DKIM Setup (Weeks 3-5)
  |
  +-- Generate 2048-bit RSA key pairs per sending service
  +-- Configure DKIM signing on MTA/email service
  +-- Publish public keys in DNS
  +-- Verify signatures with test emails
  |
Phase 4: DMARC Monitor (Weeks 5-8)
  |
  +-- Deploy DMARC with p=none
  +-- Set up aggregate report (rua) processing
  +-- Monitor for 4+ weeks
  +-- Identify and fix failing legitimate sources
  |
Phase 5: DMARC Quarantine (Weeks 9-12)
  |
  +-- Move to p=quarantine at pct=10
  +-- Gradually increase pct to 100
  +-- Monitor false positives
  |
Phase 6: DMARC Reject (Weeks 13+)
  |
  +-- Move to p=reject at pct=10
  +-- Gradually increase to pct=100
  +-- Ongoing monitoring and maintenance
```

## Workflow 2: SPF Record Construction

```
START: List all email sending sources
  |
  v
[Internal mail servers] --> ip4:x.x.x.x/y
  |
  v
[Cloud email (Google/M365)] --> include:_spf.google.com / include:spf.protection.outlook.com
  |
  v
[Marketing (Mailchimp, SendGrid)] --> include:servers.mcsv.net / include:sendgrid.net
  |
  v
[Transactional (SES, Postmark)] --> include:amazonses.com / include:spf.mtasv.net
  |
  v
[CRM (Salesforce, HubSpot)] --> include:_spf.salesforce.com / include:hubs.hubspot.com
  |
  v
[Combine all mechanisms, ensure < 10 DNS lookups]
  |
  v
[Add qualifier: ~all (monitor) or -all (enforce)]
  |
  v
[Publish TXT record at domain apex]
  |
  v
[Validate: mxtoolbox.com/spf.aspx]
```

## Workflow 3: DMARC Report Analysis

```
Daily DMARC aggregate reports (XML) received
  |
  v
[Parse XML reports with process.py]
  |
  v
[Categorize results]
  |
  +-- PASS (SPF + DKIM aligned) --> No action needed
  |
  +-- FAIL (unauthorized sender)
  |     |
  |     +-- Known service missing from SPF? --> Update SPF record
  |     +-- Known service missing DKIM? --> Configure DKIM signing
  |     +-- Unknown/suspicious sender --> Likely spoofing attempt
  |           |
  |           +-- Document source IPs
  |           +-- Add to threat intelligence
  |           +-- No SPF/DKIM changes needed (DMARC working correctly)
  |
  +-- PARTIAL PASS (SPF or DKIM only)
        |
        +-- Fix the failing mechanism
        +-- Check for forwarding/mailing list issues (consider ARC)
```

## Workflow 4: Ongoing Maintenance

```
Monthly:
  - Review DMARC aggregate reports for new unauthorized sources
  - Verify all third-party senders still authorized
  - Check SPF record is under 10 DNS lookup limit

Quarterly:
  - Rotate DKIM keys (update selector)
  - Review and update authorized sender inventory
  - Test authentication with external validation tools

Annually:
  - Full audit of email authentication configuration
  - Review DMARC policy strictness
  - Update documentation
```

---

## Working Template

## Domain Information
- **Domain**: [example.com]
- **DNS Provider**: [Cloudflare / Route53 / GoDaddy]
- **Email Platform**: [Google Workspace / Microsoft 365 / Postfix]
- **Implementation Date**: [YYYY-MM-DD]

## Current State Assessment
| Check | Status | Record |
|---|---|---|
| SPF | Present/Missing | |
| DKIM | Present/Missing | |
| DMARC | Present/Missing | |

## Authorized Email Senders Inventory
| Service | Purpose | SPF Include | DKIM Selector |
|---|---|---|---|
| Primary MTA | Employee email | | |
| Google Workspace | Employee email | `_spf.google.com` | `google` |
| Microsoft 365 | Employee email | `spf.protection.outlook.com` | `selector1`, `selector2` |
| SendGrid | Transactional | `sendgrid.net` | `s1`, `s2` |
| Mailchimp | Marketing | `servers.mcsv.net` | `k1` |
| Amazon SES | Notifications | `amazonses.com` | Custom |
| Salesforce | CRM emails | `_spf.salesforce.com` | Custom |

## SPF Record Design
```
v=spf1 [mechanisms] [qualifier]
```

### DNS Lookup Budget (Max 10)
| # | Mechanism | Lookups |
|---|---|---|
| 1 | | |
| 2 | | |
| Total | | /10 |

## DKIM Configuration
| Selector | Key Length | Service | DNS Record |
|---|---|---|---|
| | 2048-bit | | |

## DMARC Rollout Plan
| Phase | Policy | pct | Duration | Start Date |
|---|---|---|---|---|
| 1 - Monitor | none | 100 | 4 weeks | |
| 2 - Quarantine Low | quarantine | 10 | 2 weeks | |
| 3 - Quarantine Medium | quarantine | 50 | 2 weeks | |
| 4 - Quarantine Full | quarantine | 100 | 2 weeks | |
| 5 - Reject Low | reject | 10 | 2 weeks | |
| 6 - Reject Medium | reject | 50 | 2 weeks | |
| 7 - Reject Full | reject | 100 | Ongoing | |

## DMARC Report Monitoring
- **Aggregate reports (rua)**: `mailto:dmarc-aggregate@[domain]`
- **Forensic reports (ruf)**: `mailto:dmarc-forensic@[domain]`
- **Analysis tool**: [dmarcian / Valimail / Postmark]
- **Review frequency**: Weekly during rollout, monthly after enforcement

## Validation Checklist
- [ ] SPF record validates at mxtoolbox.com/spf.aspx
- [ ] SPF DNS lookup count is under 10
- [ ] DKIM key is 2048-bit minimum
- [ ] DKIM signature verified on test email
- [ ] DMARC record validates at mxtoolbox.com/dmarc.aspx
- [ ] Aggregate reports receiving data
- [ ] All legitimate senders pass authentication
- [ ] No false positives in quarantine/reject

## Rollback Plan
If authentication causes delivery issues:
1. Change DMARC policy back to `p=none`
2. Investigate failing sources in aggregate reports
3. Update SPF/DKIM for legitimate failing senders
4. Re-start enforcement rollout at lower pct
