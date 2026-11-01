# Detecting Business Email Compromise

## API Reference

## Python email Library

```python
import email
from email import policy

# Parse .eml file
with open("message.eml") as f:
    msg = email.message_from_file(f, policy=policy.default)

msg.get("From")                # sender header
msg.get("Reply-To")            # reply-to header
msg.get("Authentication-Results")  # SPF/DKIM/DMARC results
body = msg.get_body(preferencelist=("plain", "html"))
body.get_content()             # decoded body text
```

## Authentication Header Patterns

| Result | Meaning |
|--------|---------|
| `spf=pass` | Sender IP authorized by domain SPF record |
| `spf=fail` | Sender IP NOT in SPF record |
| `dkim=pass` | DKIM signature valid |
| `dkim=fail` | DKIM signature invalid or missing |
| `dmarc=pass` | SPF or DKIM aligned with From domain |
| `dmarc=fail` | Neither SPF nor DKIM aligned |

## BEC Attack Types (FBI IC3)

| Type | Description |
|------|-------------|
| CEO Fraud | Impersonates executive requesting wire transfer |
| Invoice Fraud | Fake invoice with changed bank details |
| Account Compromise | Compromised email used for payment requests |
| Attorney Impersonation | Urgent legal matter requiring funds |
| Data Theft | Requests for W-2 / PII from HR |

## BEC Indicator Regex Patterns

```python
# Financial urgency
r"\b(wire transfer|bank transfer|routing number)\b"
# Secrecy pressure
r"\b(confidential|do not share|keep this between us)\b"
# Gift card fraud
r"\b(gift card|bitcoin|crypto|western union)\b"
# Account change
r"\b(change.*(bank|account|payment))\b"
```

## Microsoft Graph API - Mail Security

```http
GET https://graph.microsoft.com/v1.0/me/messages?$filter=internetMessageHeaders/any(h: h/name eq 'Authentication-Results')
Authorization: Bearer {token}
```

## CLI Usage

```bash
python agent.py --email-file suspicious.eml --vip-names "John Smith" "Jane CEO"
python agent.py --scan-dir /var/mail/quarantine/ --vip-names "CFO Name"
```

---

## Standards and Controls

## FBI IC3 BEC Classification
- **Type 1**: CEO Fraud / Executive Impersonation
- **Type 2**: Account Compromise (compromised employee email)
- **Type 3**: False Invoice / Vendor Email Compromise
- **Type 4**: Attorney Impersonation
- **Type 5**: Data Theft (W-2/PII requests)

## MITRE ATT&CK References
- **T1566.001/002**: Phishing (initial access for BEC)
- **T1534**: Internal Spearphishing
- **T1114.003**: Email Collection: Email Forwarding Rule
- **T1098.002**: Account Manipulation: Additional Email Delegate Access
- **T1586.002**: Compromise Accounts: Email Accounts

## NIST / Regulatory
- **NIST SP 800-177 Rev.1**: Trustworthy Email
- **FinCEN Advisory FIN-2019-A005**: Advisory on BEC targeting businesses
- **FBI IC3 Annual Report**: BEC statistics and trends ($2.9B losses in 2023)

## Detection Rule Categories
| Rule | Description | Priority |
|---|---|---|
| VIP impersonation | External email with internal VIP display name | Critical |
| Payment language | Wire transfer/payment keywords + urgency | High |
| Reply-to mismatch | Reply-to domain differs from From | High |
| First-time sender | No prior communication with recipient | Medium |
| Forwarding rule | New auto-forward rule to external address | Critical |
| Gift card request | Request for gift card purchase | High |
| Vendor change | Payment detail change notification | High |

---

## Workflows

## Workflow 1: BEC Detection Pipeline

```
Inbound email arrives
  |
  v
[Check: Does display name match VIP list?]
  +-- YES + external domain --> HIGH ALERT: Possible CEO fraud
  +-- NO --> Continue standard checks
  |
  v
[Check: Financial keywords present?]
  +-- "wire transfer", "payment", "invoice", "bank details" detected
  +-- Combined with urgency: "urgent", "confidential", "today"
  +-- YES --> ELEVATED: Flag for finance team review
  |
  v
[Check: Reply-To mismatch?]
  +-- Reply-To domain differs from From domain
  +-- YES --> HIGH: Likely BEC attempt
  |
  v
[Check: Communication pattern anomaly?]
  +-- First-time sender to finance/HR staff
  +-- Unusual time of day for this sender
  +-- YES --> MEDIUM: Requires verification
  |
  v
[Decision]
  +-- BLOCK: High-confidence BEC
  +-- QUARANTINE: Moderate confidence
  +-- TAG: Warning banner for recipient
  +-- DELIVER: Low risk
```

## Workflow 2: BEC Incident Response

```
BEC attempt detected or reported
  |
  v
[Immediate actions (first 30 minutes)]
  +-- Quarantine the email
  +-- Search for similar messages to other recipients
  +-- Alert affected users not to comply with request
  |
  v
[Investigation (next 2 hours)]
  +-- Analyze email headers for true origin
  +-- Check if any user already complied (check sent folders)
  +-- If payment was made: Initiate bank recall immediately
  +-- Search for compromised accounts (forwarding rules, login anomalies)
  |
  v
[Containment]
  +-- Block sender domain/IP
  +-- If account compromised: Force password reset, revoke sessions
  +-- Remove malicious forwarding rules
  +-- Notify finance to halt pending payments
  |
  v
[Recovery]
  +-- Work with bank for fund recovery
  +-- File FBI IC3 report (ic3.gov)
  +-- Notify affected parties
  +-- Update detection rules
  +-- Targeted training for affected employees
```

## Workflow 3: Vendor Payment Change Verification

```
Vendor requests payment detail change
  |
  v
[Do NOT use contact info from the email]
  |
  v
[Look up vendor contact from existing records]
  |
  v
[Call vendor using known phone number]
  +-- Verify the payment change request is legitimate
  |
  +-- CONFIRMED --> Process change with dual authorization
  +-- NOT CONFIRMED --> Report as BEC attempt, block sender
  +-- UNABLE TO REACH --> Hold payment, escalate
```

---

## Working Template

## VIP Protection List
| Name | Title | Email Domain | Protected Since |
|---|---|---|---|
| | CEO | | |
| | CFO | | |
| | CTO | | |

## BEC Detection Rules Deployed
| Rule | Condition | Action | Status |
|---|---|---|---|
| VIP name spoofing | External email with VIP display name | Quarantine + Alert | Active |
| Financial + Urgency | Wire transfer keywords + urgency | Tag + Alert | Active |
| Reply-To mismatch | Reply-To domain differs from From | Tag + Log | Active |
| Gift card request | Gift card keywords from "executive" | Quarantine | Active |
| Vendor payment change | Bank detail change language | Tag + Finance alert | Active |

## Financial Controls
- [ ] Dual authorization for transfers > $[threshold]
- [ ] Out-of-band verification for payment detail changes
- [ ] Vendor payment change requires callback on known number
- [ ] Gift card purchases require in-person manager approval

## BEC Incident Response Contacts
| Role | Name | Phone | Email |
|---|---|---|---|
| SOC Lead | | | |
| Finance Controller | | | |
| Bank Fraud Department | | | |
| FBI IC3 (filing) | N/A | N/A | ic3.gov |
| Legal Counsel | | | |
