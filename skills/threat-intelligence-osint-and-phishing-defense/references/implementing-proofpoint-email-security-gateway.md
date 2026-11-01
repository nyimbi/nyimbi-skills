# Implementing Proofpoint Email Security Gateway

## API Reference

## Libraries Used

| Library | Purpose |
|---------|---------|
| `requests` | HTTP client for Proofpoint TAP API v2 |
| `json` | Parse threat and message event data |
| `os` | Read `PROOFPOINT_SP` and `PROOFPOINT_SECRET` credentials |
| `datetime` | Build ISO-8601 time range queries |

## Installation

```bash
pip install requests
```

## Authentication

Proofpoint TAP API uses HTTP Basic Auth with service principal and secret:

```python
import requests
import os
from requests.auth import HTTPBasicAuth

PROOFPOINT_URL = "https://tap-api-v2.proofpoint.com"
auth = HTTPBasicAuth(
    os.environ["PROOFPOINT_SP"],       # Service Principal
    os.environ["PROOFPOINT_SECRET"],   # Secret
)
```

## TAP API v2 Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v2/siem/messages/blocked` | Messages blocked by Proofpoint |
| GET | `/v2/siem/messages/delivered` | Messages delivered (with threats) |
| GET | `/v2/siem/clicks/blocked` | Blocked URL clicks |
| GET | `/v2/siem/clicks/permitted` | Permitted URL clicks (with threats) |
| GET | `/v2/siem/all` | All events (messages + clicks) |
| GET | `/v2/siem/issues` | Campaign and threat issues |
| GET | `/v2/people/vap` | Very Attacked People report |
| GET | `/v2/forensics` | Threat forensics detail |
| POST | `/v2/quarantine/release` | Release message from quarantine |
| POST | `/v2/quarantine/delete` | Delete message from quarantine |

## Core Operations

### Fetch Blocked Messages
```python
from datetime import datetime, timedelta

def get_blocked_messages(hours_back=1):
    since = (datetime.utcnow() - timedelta(hours=hours_back)).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    resp = requests.get(
        f"{PROOFPOINT_URL}/v2/siem/messages/blocked",
        auth=auth,
        params={
            "sinceTime": since,
            "format": "json",
        },
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json().get("messagesBlocked", [])
```

### Fetch Permitted Clicks with Threats
```python
def get_permitted_clicks(hours_back=24):
    since = (datetime.utcnow() - timedelta(hours=hours_back)).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    resp = requests.get(
        f"{PROOFPOINT_URL}/v2/siem/clicks/permitted",
        auth=auth,
        params={"sinceTime": since, "format": "json"},
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json().get("clicksPermitted", [])
```

### Get All SIEM Events
```python
def get_all_events(hours_back=1):
    since = (datetime.utcnow() - timedelta(hours=hours_back)).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    resp = requests.get(
        f"{PROOFPOINT_URL}/v2/siem/all",
        auth=auth,
        params={"sinceTime": since, "format": "json"},
        timeout=120,
    )
    resp.raise_for_status()
    data = resp.json()
    return {
        "messages_blocked": data.get("messagesBlocked", []),
        "messages_delivered": data.get("messagesDelivered", []),
        "clicks_blocked": data.get("clicksBlocked", []),
        "clicks_permitted": data.get("clicksPermitted", []),
    }
```

### Get Very Attacked People (VAP)
```python
def get_vap_report(days=30):
    resp = requests.get(
        f"{PROOFPOINT_URL}/v2/people/vap",
        auth=auth,
        params={"window": days, "size": 100},
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json().get("users", [])
```

### Extract Threat IOCs
```python
def extract_iocs(events):
    iocs = {"urls": set(), "senders": set(), "subjects": set(), "sha256": set()}
    for msg in events.get("messages_blocked", []) + events.get("messages_delivered", []):
        iocs["senders"].add(msg.get("sender", ""))
        iocs["subjects"].add(msg.get("subject", ""))
        for threat in msg.get("threatsInfoMap", []):
            if threat.get("threatUrl"):
                iocs["urls"].add(threat["threatUrl"])
            if threat.get("sha256"):
                iocs["sha256"].add(threat["sha256"])
    return {k: list(v) for k, v in iocs.items()}
```

## Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `sinceTime` | ISO-8601 | Start time (required, max 1 hour back for `/all`) |
| `sinceSeconds` | int | Seconds before now (alternative to sinceTime) |
| `format` | string | Response format: `json` (default) or `syslog` |
| `threatType` | string | Filter: `url`, `attachment`, `messageText` |
| `threatStatus` | string | Filter: `active`, `cleared`, `falsePositive` |

## Output Format

```json
{
  "messagesBlocked": [
    {
      "GUID": "abc123-def456",
      "QID": "r1234567",
      "sender": "attacker@malicious.example.com",
      "recipient": ["user@company.com"],
      "subject": "Invoice #12345 Attached",
      "messageTime": "2025-01-15T10:30:00Z",
      "threatsInfoMap": [
        {
          "threat": "https://evil.example.com/payload",
          "threatType": "url",
          "threatStatus": "active",
          "classification": "phish",
          "sha256": "a1b2c3d4e5f6..."
        }
      ],
      "malwareScore": 100,
      "phishScore": 95,
      "spamScore": 0
    }
  ]
}
```

---

## Standards and Controls

## Industry Standards
- **NIST SP 800-177 Rev.1**: Trustworthy Email - guidelines for email security deployment
- **RFC 7208**: Sender Policy Framework (SPF) for authorizing use of domains in email
- **RFC 6376**: DomainKeys Identified Mail (DKIM) Signatures
- **RFC 7489**: Domain-based Message Authentication, Reporting & Conformance (DMARC)
- **CIS Controls v8 Control 9**: Email and Web Browser Protections

## MITRE ATT&CK References
- **T1566.001**: Phishing: Spearphishing Attachment
- **T1566.002**: Phishing: Spearphishing Link
- **T1566.003**: Phishing: Spearphishing via Service
- **T1534**: Internal Spearphishing
- **T1598**: Phishing for Information
- **T1114.003**: Email Collection: Email Forwarding Rule

## Proofpoint-Specific References
- **Proofpoint Email Protection (PPS)**: On-premises protection platform
- **Proofpoint on Demand (PoD)**: Cloud-hosted email security service
- **Proofpoint TAP (Targeted Attack Protection)**: Advanced threat detection
- **Proofpoint TRAP (Threat Response Auto-Pull)**: Post-delivery remediation
- **Proofpoint Nexus Threat Graph**: Cross-customer threat intelligence

## Compliance Alignment
| Framework | Control | Description |
|---|---|---|
| SOC 2 | CC6.1 | Logical and physical access controls |
| HIPAA | 164.312(a)(1) | Access control for ePHI |
| PCI DSS 4.0 | 5.2 | Anti-malware solutions |
| NIST CSF 2.0 | PR.DS-1 | Data-at-rest and data-in-transit protection |
| ISO 27001 | A.8.23 | Web filtering |

## Email Security Gateway Market
- Proofpoint processes 2.8+ billion messages daily (2024)
- Gartner Magic Quadrant Leader for Email Security (2019-2024)
- Over 50% of Fortune 100 companies use Proofpoint

---

## Workflows

## Workflow 1: Inbound Mail Processing Pipeline

```
External sender sends email
  |
  v
[DNS MX lookup resolves to Proofpoint]
  |
  v
[Connection-level filtering]
  +-- IP reputation check (Proofpoint Nexus)
  +-- Rate limiting and connection throttling
  +-- REJECT if known-bad IP
  |
  v
[Authentication checks]
  +-- SPF validation
  +-- DKIM signature verification
  +-- DMARC policy evaluation
  +-- FAIL actions: quarantine or reject per policy
  |
  v
[Content analysis]
  +-- Anti-spam scoring (ML classifier)
  +-- Anti-virus scanning (multi-engine)
  +-- Impostor classifier (BEC detection)
  +-- NLP analysis for social engineering language
  |
  v
[URL Defense]
  +-- Extract all URLs from body and attachments
  +-- Rewrite URLs through Proofpoint proxy
  +-- Pre-delivery URL reputation check
  +-- BLOCK if known malicious
  |
  v
[Attachment Defense]
  +-- Static analysis (signatures, heuristics)
  +-- Dynamic sandbox detonation (if suspicious)
  +-- Wait for sandbox verdict (up to 7 minutes)
  +-- QUARANTINE if malicious
  |
  v
[Policy action]
  +-- DELIVER: Clean email to mailbox
  +-- TAG: Add warning banner for external/suspicious
  +-- QUARANTINE: Hold for admin/user review
  +-- REJECT: Block with NDR to sender
```

## Workflow 2: Post-Delivery Threat Response (TRAP)

```
Threat intelligence update received
  |
  v
[TRAP scans delivered messages retroactively]
  +-- URL becomes malicious after delivery
  +-- New malware signature matches delivered attachment
  |
  v
[Auto-Pull action triggered]
  +-- Move message from user inbox to quarantine
  +-- Log retraction in TRAP dashboard
  +-- Notify SOC team of post-delivery threat
  |
  v
[SOC investigation]
  +-- Review TRAP alert and threat details
  +-- Check if user clicked URL before retraction
  +-- If clicked: initiate incident response
  +-- If not clicked: close as contained
  |
  v
[Update policies]
  +-- Add sender/domain to block list if needed
  +-- Create detection rule for similar campaigns
  +-- Update TAP Dashboard threat tracking
```

## Workflow 3: Phishing Report and CLEAR Integration

```
User receives suspicious email
  |
  v
[User clicks "Report Phishing" button (Proofpoint CLEAR)]
  |
  v
[Email forwarded to Proofpoint analysis pipeline]
  +-- Automated classification (phishing/spam/clean)
  +-- URL and attachment analysis
  |
  v
[CLEAR verdict]
  +-- MALICIOUS: Auto-retract from all inboxes that received it
  +-- SPAM: Move to junk for all recipients
  +-- CLEAN: Return to inbox, thank reporter
  |
  v
[Metrics and feedback]
  +-- Track reporter accuracy rate
  +-- Update user risk score
  +-- Feed into security awareness metrics
```

---

## Working Template

## Pre-Deployment Checklist
- [ ] Proofpoint license type confirmed (PPS / PoD)
- [ ] Current MX records documented
- [ ] All legitimate sending sources inventoried
- [ ] SPF record updated with Proofpoint include
- [ ] DKIM keys generated and DNS records published
- [ ] DMARC record configured in monitoring mode
- [ ] Firewall rules updated for Proofpoint IP ranges
- [ ] Microsoft 365 / Google Workspace connector configured

## Policy Configuration
| Policy | Scope | Action | Status |
|---|---|---|---|
| Anti-spam (inbound) | All users | Quarantine high confidence | |
| Anti-virus | All users | Block + notify admin | |
| Impostor detection | VIP list | Quarantine + SOC alert | |
| URL Defense | All users | Rewrite + sandbox at click | |
| Attachment Defense | All users | Sandbox suspicious types | |
| TRAP auto-pull | All users | Retract post-delivery threats | |
| DLP (outbound) | All users | Block + manager notify | |

## VIP Protection List
| Name | Title | Email | Protected |
|---|---|---|---|
| | CEO | | Yes |
| | CFO | | Yes |
| | CTO | | Yes |
| | VP Finance | | Yes |

## MX Record Migration
| Record Type | Priority | Old Value | New Value |
|---|---|---|---|
| MX | 10 | | {org}.mail.protection.proofpoint.com |

## Post-Deployment Validation
- [ ] Test inbound mail delivery through Proofpoint
- [ ] Verify message headers show Proofpoint processing
- [ ] Test URL Defense rewriting on inbound links
- [ ] Test Attachment Defense with EICAR test file
- [ ] Verify TRAP can retract delivered message
- [ ] Confirm quarantine digest notifications working
- [ ] Validate SPF/DKIM/DMARC pass for outbound mail
- [ ] Review false positive rate after 48 hours
