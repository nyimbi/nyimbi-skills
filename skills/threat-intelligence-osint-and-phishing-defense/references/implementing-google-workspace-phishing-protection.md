# Implementing Google Workspace Phishing Protection

## API Reference

## Admin Console Path

```
Admin Console > Apps > Google Workspace > Gmail > Safety
```

## Gmail Safety Controls

| Control | Category | Severity if Missing |
|---------|----------|-------------------|
| Protect against similar domain spoofing | Spoofing | HIGH |
| Protect against employee name spoofing | Spoofing | HIGH |
| Protect against inbound domain spoofing | Spoofing | CRITICAL |
| Enhanced pre-delivery scanning | Scanning | HIGH |
| Attachment protection (encrypted/scripts) | Attachments | HIGH |
| Identify links behind shortened URLs | Links | MEDIUM |
| Show warning for unauthenticated email | Warnings | MEDIUM |
| Enhanced Safe Browsing | Browsing | HIGH |

## Admin SDK Directory API (GAM)

```bash
# List Gmail settings
gam print gmailsettings domain example.com
# List users with Advanced Protection
gam print users query "isAdvancedProtectionProgram=true"
```

## Google Workspace Alert Center API

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build
creds = service_account.Credentials.from_service_account_file("sa.json",
    scopes=["https://www.googleapis.com/auth/apps.alerts"])
service = build("alertcenter", "v1beta1", credentials=creds)
alerts = service.alerts().list().execute()
```

## Recommended Actions for Spoofing

| Detection | Action |
|-----------|--------|
| Similar domain spoofing | Quarantine |
| Employee name spoofing | Show warning + move to spam |
| Inbound domain spoofing | Quarantine |
| Unauthenticated email | Show warning banner |

### References

- Google Workspace Admin Help - Phishing: https://support.google.com/a/answer/9157861
- Advanced Protection Program: https://landing.google.com/advancedprotection/
- Gmail Safety Settings: https://support.google.com/a/answer/7380368

---

## Standards and Controls

## Google Workspace Security Settings Path
- Admin Console > Apps > Google Workspace > Gmail > Safety
- Admin Console > Security > Gmail Enhanced Safe Browsing
- Admin Console > Apps > Google Workspace > Gmail > Authenticate email

## MITRE ATT&CK References
- **T1566.001**: Phishing: Spearphishing Attachment
- **T1566.002**: Phishing: Spearphishing Link
- **T1656**: Impersonation
- **T1586.002**: Compromise Accounts: Email Accounts

## Key Protection Settings
| Setting | Location | Default | Recommended |
|---|---|---|---|
| Domain spoofing protection | Safety | Off | On - Quarantine |
| Employee name spoofing | Safety | Off | On - Warning |
| Pre-delivery scanning | Safety | On | On (enhanced) |
| Attachment protection | Safety | Partial | Full - all options |
| Enhanced Safe Browsing | Security | Off | On |
| Gmail Security Sandbox | Safety | Off | On (Enterprise) |

## Google Workspace License Requirements
| Feature | Business Starter | Business Standard | Enterprise |
|---|---|---|---|
| Basic phishing protection | Yes | Yes | Yes |
| Enhanced pre-delivery scanning | Yes | Yes | Yes |
| Gmail Security Sandbox | No | No | Yes |
| Security Investigation Tool | No | Partial | Yes |
| Advanced Protection Program | Yes | Yes | Yes |

---

## Workflows

## Workflow 1: Gmail Inbound Protection Pipeline

```
Inbound email arrives at Gmail
  |
  v
[Connection-level checks]
  +-- IP reputation
  +-- SPF validation
  +-- DKIM verification
  +-- DMARC evaluation
  |
  v
[Enhanced Pre-Delivery Scanning]
  +-- Content analysis for phishing indicators
  +-- URL expansion (shortened URLs)
  +-- Image scanning for embedded phishing
  +-- NLP analysis for social engineering
  |
  v
[Attachment Protection]
  +-- File type analysis
  +-- Script detection in attachments
  +-- Encrypted attachment from untrusted sender check
  +-- Security Sandbox detonation (Enterprise)
  |
  v
[Spoofing Detection]
  +-- Domain name similarity check
  +-- Employee name impersonation check
  +-- Internal domain spoofing check
  |
  v
[Delivery decision]
  +-- DELIVER: Clean message to inbox
  +-- WARN: Deliver with yellow warning banner
  +-- SPAM: Route to spam folder
  +-- QUARANTINE: Hold for admin review
  +-- REJECT: Block delivery entirely
```

## Workflow 2: Safe Browsing URL Protection

```
User clicks URL in Gmail
  |
  v
[Enhanced Safe Browsing check]
  +-- Real-time URL reputation lookup
  +-- Check against known phishing database
  +-- Dynamic page analysis
  |
  v
[Decision]
  +-- SAFE: Allow navigation
  +-- DANGEROUS: Display full-page warning
  +-- SUSPICIOUS: Display interstitial warning
```

---

## Working Template

## Safety Settings Checklist
- [ ] Domain spoofing protection enabled
- [ ] Employee name spoofing protection enabled
- [ ] Enhanced pre-delivery scanning enabled
- [ ] Encrypted attachment protection enabled
- [ ] Script attachment protection enabled
- [ ] Anomalous attachment type protection enabled
- [ ] Enhanced Safe Browsing enabled
- [ ] Security Sandbox enabled (Enterprise)

## Advanced Protection Program Enrollment
| User | Role | APP Enrolled | FIDO2 Key |
|---|---|---|---|
| | Super Admin | | |
| | CEO | | |
| | CFO | | |
| | VP Finance | | |

## Authentication Configuration
| Protocol | Status | Record |
|---|---|---|
| SPF | | v=spf1 include:_spf.google.com -all |
| DKIM | | google._domainkey.{domain} |
| DMARC | | v=DMARC1; p=reject; rua=... |
