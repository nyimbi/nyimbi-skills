# Detecting Spearphishing With Email Gateway

## API Reference

## Python email Module

### Parse EML file
```python
import email
from email import policy

with open("message.eml", "rb") as f:
    msg = email.message_from_binary_file(f, policy=policy.default)
```

### Security Headers
| Header | Purpose |
|--------|---------|
| `Received-SPF` | SPF check result |
| `Authentication-Results` | SPF, DKIM, DMARC combined |
| `DKIM-Signature` | DKIM signing info |
| `ARC-Authentication-Results` | ARC chain results |
| `X-Mailer` | Client used to send |
| `Return-Path` | Envelope sender |

### Authentication-Results Values
```
Authentication-Results: mx.google.com;
    dkim=pass header.d=example.com;
    spf=pass smtp.mailfrom=example.com;
    dmarc=pass
```

## SPF Record Lookup
```bash
dig TXT example.com | grep "v=spf1"
# v=spf1 include:_spf.google.com ~all
```

### SPF Results
| Result | Meaning |
|--------|---------|
| `pass` | Authorized sender |
| `fail` | Unauthorized (reject) |
| `softfail` | Unauthorized (accept with mark) |
| `neutral` | No assertion |
| `none` | No SPF record |

## DKIM Verification
```bash
opendkim-testkey -d example.com -s selector -vvv
```

## DMARC Record
```bash
dig TXT _dmarc.example.com
# v=DMARC1; p=reject; rua=mailto:dmarc@example.com
```

## Microsoft Defender for Office 365 API

### Get email threat assessment
```http
POST https://graph.microsoft.com/v1.0/informationProtection/threatAssessmentRequests
Authorization: Bearer {token}

{
  "contentType": "mail",
  "expectedAssessment": "block",
  "category": "phishing",
  "mailInfo": {
    "internetMessageId": "<message-id>"
  }
}
```

## Proofpoint TAP API

### Get blocked messages
```http
GET https://tap-api-v2.proofpoint.com/v2/siem/messages/blocked
    ?sinceSeconds=3600
Authorization: Basic {base64_credentials}
```

### Response Fields
| Field | Description |
|-------|-------------|
| `spamScore` | Spam confidence (0-100) |
| `phishScore` | Phishing confidence (0-100) |
| `threatsInfoMap` | Threat details array |
| `fromAddress` | Envelope sender |

## Mimecast API — URL Protection

### Decode Mimecast URL
```http
POST https://api.mimecast.com/api/ttp/url/decode-url
Authorization: MC {access-key}:{secret-key}

{
  "data": [{"url": "https://protect.mimecast.com/..."}]
}
```

---

## Standards and Controls

## MITRE ATT&CK References
- **T1566.001**: Phishing: Spearphishing Attachment
- **T1566.002**: Phishing: Spearphishing Link
- **T1566.003**: Phishing: Spearphishing via Service
- **T1598.002**: Phishing for Information: Spearphishing Attachment
- **T1598.003**: Phishing for Information: Spearphishing Link
- **T1534**: Internal Spearphishing

## NIST Guidelines
- **NIST SP 800-177 Rev.1**: Trustworthy Email
- **NIST SP 800-53 Rev.5**: SI-8 Spam Protection, SI-3 Malicious Code Protection
- **NIST CSF**: PR.AT (Awareness & Training), DE.CM (Security Continuous Monitoring)

## CIS Controls v8
- **CIS Control 9**: Email and Web Browser Protections
  - 9.1: Ensure only approved browsers and email clients are used
  - 9.2: Use DNS filtering services
  - 9.3: Maintain and enforce network-based URL filters
  - 9.6: Block unnecessary file types
  - 9.7: Deploy and maintain email server anti-malware protections

## Email Gateway Feature Matrix

| Feature | Microsoft Defender | Proofpoint | Mimecast | Barracuda |
|---|---|---|---|---|
| Impersonation detection | Anti-phishing policy | Impostor Classifier | Brand Exploit Protect | Impersonation Protection |
| URL detonation | Safe Links | URL Defense | URL Protect | Link Protection |
| Attachment sandbox | Safe Attachments | Targeted Attack Protection | Attachment Protect | Advanced Threat Protection |
| DMARC enforcement | Built-in | Built-in | DMARC Analyzer | Built-in |
| AI/ML detection | Yes (multiple models) | NexusAI | Yes | Yes |
| User reporting | Report Message add-in | PhishAlarm | Built-in | Phishline |
| SIEM integration | Microsoft Sentinel | Splunk, QRadar | Splunk, Sentinel | Various |
| Auto-remediation (ZAP) | Yes | CLEAR | Yes | Yes |

## Detection Indicators for Spearphishing

| Indicator | Weight | Description |
|---|---|---|
| Display name spoofing VIP | High | From name matches protected user but different email |
| Lookalike domain | High | Domain differs by 1-2 characters from legitimate |
| First-time sender to VIP | Medium | No prior communication history |
| Urgency keywords | Medium | "urgent", "immediately", "wire transfer", "confidential" |
| Reply-to mismatch | High | Reply-to differs from From address |
| External sender with internal branding | High | Email mimics internal templates |
| Newly registered domain | High | Sending domain < 30 days old |
| Authentication failure | High | SPF/DKIM/DMARC fail |

---

## Workflows

## Workflow 1: Multi-Layer Detection Pipeline

```
Inbound Email Arrives at Gateway
  |
  v
[Layer 1: Connection Filtering]
  +-- Check sender IP reputation
  +-- Check RBL/DNSBL blacklists
  +-- Rate limiting / throttling
  |
  v
[Layer 2: Authentication]
  +-- Verify SPF alignment
  +-- Verify DKIM signature
  +-- Evaluate DMARC policy
  +-- Check ARC headers (forwarded mail)
  |
  v
[Layer 3: Impersonation Detection]
  +-- Compare display name against VIP list
  +-- Check domain similarity (Levenshtein distance)
  +-- Evaluate sender reputation
  +-- First-time sender analysis
  |
  v
[Layer 4: Content Analysis]
  +-- NLP analysis for urgency/social engineering
  +-- Business context anomaly detection
  +-- Keyword pattern matching
  +-- Language analysis
  |
  v
[Layer 5: URL Analysis]
  +-- URL reputation check
  +-- Domain age verification
  +-- Real-time URL detonation
  +-- Redirect chain following
  +-- Visual similarity to legitimate sites
  |
  v
[Layer 6: Attachment Analysis]
  +-- File type validation
  +-- Sandbox detonation
  +-- Macro analysis
  +-- Embedded object detection
  |
  v
[Decision Engine]
  +-- Aggregate scores from all layers
  +-- Apply organizational policy
  |
  +-- DELIVER: Low risk
  +-- TAG: Add warning banner
  +-- QUARANTINE: Moderate risk
  +-- BLOCK: High risk, drop message
```

## Workflow 2: VIP Impersonation Detection

```
Email arrives with From display name matching VIP list
  |
  v
[Check: Is sending domain authorized for this VIP?]
  |
  +-- YES: Check DKIM/SPF --> If pass, deliver normally
  |
  +-- NO: Impersonation suspected
       |
       v
  [Calculate domain similarity score]
       |
       +-- Exact match (different email): CRITICAL - Block
       +-- Lookalike domain (1-2 char diff): HIGH - Quarantine
       +-- Similar but different: MEDIUM - Tag with warning
       |
       v
  [Additional checks]
       +-- Has this sender emailed before?
       +-- Is the sending infrastructure legitimate?
       +-- Does email content match typical VIP communication?
       |
       v
  [Action: Quarantine + Alert SOC + Notify recipient manager]
```

## Workflow 3: Spearphishing Response

```
Gateway detects potential spearphishing
  |
  v
[Automated Response]
  +-- Quarantine message
  +-- Generate alert in SIEM
  +-- Extract IOCs (sender, domain, URLs, hashes)
  |
  v
[SOC Analyst Review]
  +-- Review quarantined message
  +-- Analyze full headers
  +-- Investigate sending infrastructure
  +-- Check if other users received similar emails
  |
  +-- FALSE POSITIVE
  |     +-- Release from quarantine
  |     +-- Whitelist if legitimate
  |     +-- Update detection rules
  |
  +-- CONFIRMED SPEARPHISHING
        +-- Block sender domain organization-wide
        +-- Search mailboxes for similar messages (retroactive)
        +-- Auto-purge any delivered copies (ZAP)
        +-- Notify targeted users
        +-- Submit IOCs to threat intelligence
        +-- Check for any successful credential compromise
        +-- Update VIP protection list if needed
```

## Workflow 4: Gateway Tuning Cycle

```
Monthly Review
  |
  +-- Pull detection statistics from gateway
  +-- Analyze false positive rate
  +-- Analyze false negative rate (user-reported misses)
  +-- Review quarantine volumes
  |
  v
[Identify gaps]
  +-- New impersonation patterns?
  +-- New sending domains to whitelist/blacklist?
  +-- Policy thresholds too aggressive/permissive?
  |
  v
[Adjust configuration]
  +-- Update VIP protection list (new hires, departures)
  +-- Tune sensitivity thresholds
  +-- Add custom transport rules
  +-- Update URL/domain blocklists
  |
  v
[Validate changes]
  +-- Send test phishing emails
  +-- Verify legitimate mail still flows
  +-- Document changes
```

---

## Working Template

## Gateway Information
- **Product**: [Microsoft Defender for O365 / Proofpoint / Mimecast / Barracuda]
- **Version**: []
- **Configuration Date**: [YYYY-MM-DD]
- **Configured By**: []

## VIP Protection List
| Name | Title | Email | Risk Level |
|---|---|---|---|
| | CEO | | Critical |
| | CFO | | Critical |
| | CTO | | Critical |
| | VP Finance | | High |
| | HR Director | | High |

## Impersonation Detection Rules
| Rule | Trigger | Action | Severity |
|---|---|---|---|
| VIP display name match | External email with VIP name | Quarantine + Alert | Critical |
| Lookalike domain | Levenshtein distance <= 2 | Quarantine | High |
| First-time sender to VIP | No prior communication | Tag warning | Medium |
| Reply-to mismatch | Reply-to differs from From | Tag + Log | Medium |

## URL Protection Settings
| Setting | Value |
|---|---|
| URL rewriting enabled | Yes |
| Time-of-click verification | Yes |
| Block new domains (< days) | 30 |
| Follow redirects | Yes (max 5 hops) |
| Detonate suspicious URLs | Yes |

## Attachment Protection Settings
| Setting | Value |
|---|---|
| Sandbox detonation | Enabled |
| Dynamic delivery | Enabled |
| Block macros from external | Yes |
| Block executable types | .exe, .scr, .bat, .cmd, .ps1, .vbs, .js |

## Alert Configuration
| Event | Alert Method | Recipients |
|---|---|---|
| VIP impersonation detected | Email + SIEM | SOC team |
| Credential harvest URL blocked | SIEM | SOC team |
| Malicious attachment blocked | Email + SIEM | SOC team |
| DMARC failure from partner domain | Email | Email admin |

## Quarterly Review Checklist
- [ ] Update VIP protection list
- [ ] Review false positive rates
- [ ] Analyze user-reported phishing misses
- [ ] Update domain allow/block lists
- [ ] Test detection with simulated phishing
- [ ] Review and update custom rules
- [ ] Verify SIEM integration working
