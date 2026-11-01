# Building Phishing Reporting Button Workflow

## API Reference

## Email Parsing (Python email module)
```python
from email import policy
from email.parser import BytesParser

with open("report.eml", "rb") as f:
    msg = BytesParser(policy=policy.default).parse(f)
headers = {
    "from": msg["From"], "subject": msg["Subject"],
    "reply_to": msg["Reply-To"], "received": msg.get_all("Received")
}
```

## Phishing Indicators
| Indicator | Weight | Description |
|-----------|--------|-------------|
| Reply-To mismatch | 20 | From and Reply-To differ |
| SPF/DKIM fail | 25 | Authentication failure |
| Suspicious language | 10 | Urgency/credential patterns |
| Suspicious URL | 15 | Known bad TLDs or redirectors |
| Dangerous attachment | 30 | Executable file extensions |

## VirusTotal URL Scan
```
GET https://www.virustotal.com/api/v3/urls/{url_id}
x-apikey: YOUR_KEY
```
URL ID = base64url(url) or sha256(url)

## Dangerous File Extensions
| Category | Extensions |
|----------|-----------|
| Executables | `.exe`, `.scr`, `.bat`, `.cmd` |
| Scripts | `.js`, `.vbs`, `.ps1`, `.hta` |
| Disk images | `.iso`, `.img`, `.vhd` |
| Archives | `.zip` (password-protected), `.rar` |
| Documents | `.docm`, `.xlsm` (macro-enabled) |

## Verdict Classification
| Score | Verdict | Action |
|-------|---------|--------|
| >= 50 | Phishing | Block sender, quarantine, create ticket |
| 25-49 | Suspicious | Analyst review required |
| < 25 | Benign | Close report, notify user |

## Ticketing Integration
```
POST /api/v2/tickets
Authorization: Bearer TOKEN
{
  "title": "Phishing Report: ...",
  "severity": "high",
  "description": "...",
  "indicators": ["Reply-To mismatch", ...]
}
```

## Microsoft Report Message Add-in
```
POST https://graph.microsoft.com/v1.0/users/{id}/messages/{msgId}/move
{"destinationId": "phishing-mailbox-id"}
```

---

## Standards and Controls

## MITRE ATT&CK References
- **T1566.001**: Phishing: Spearphishing Attachment
- **T1566.002**: Phishing: Spearphishing Link
- **T1204**: User Execution
- **D3-RERE**: User Reporting (MITRE D3FEND)

## Industry Standards
- **NIST SP 800-61 Rev.2**: Computer Security Incident Handling Guide
- **CIS Controls v8 Control 14**: Security Awareness and Skills Training
- **ISO 27001 A.6.3**: Information Security Awareness, Education and Training

## Reporting Platform Comparison
| Platform | Type | Integration | Auto-Triage |
|---|---|---|---|
| Microsoft Report Button | Built-in | M365 native | Via Sentinel/API |
| Cofense Reporter + Triage | Third-party | M365, Google | Yes (Cofense Triage) |
| KnowBe4 PAB | Third-party | M365, Google | Yes (KMSAT) |
| Proofpoint CLEAR | Third-party | M365, Google | Yes (built-in) |
| Hoxhunt | Third-party | M365, Google | Yes (AI-powered) |

## Key Metrics
- **Report Rate**: Percentage of phishing simulations reported (target: >70%)
- **Mean Time to Triage**: Time from report to classification (target: <10 min)
- **False Positive Rate**: Legitimate emails reported as phishing
- **Threat Catch Rate**: Real threats first detected by user reports
- **Reporter Accuracy**: Percentage of reports that are actual threats

---

## Workflows

## Workflow 1: Automated Phishing Report Triage

```
User clicks "Report Phishing" button
  |
  v
[Email forwarded to reporting mailbox]
  +-- Original email preserved with full headers
  +-- Reporter identity recorded
  |
  v
[SOAR platform ingests report]
  |
  v
[Automated IOC extraction]
  +-- Extract sender address and domain
  +-- Extract all URLs from body
  +-- Extract attachment hashes (MD5, SHA256)
  +-- Parse email headers for authentication results
  |
  v
[Automated analysis (parallel)]
  +-- URLs -> VirusTotal, URLScan.io, PhishTank
  +-- Attachments -> Sandbox detonation
  +-- Sender -> Threat intelligence lookup
  +-- Headers -> SPF/DKIM/DMARC validation
  |
  v
[Classification]
  +-- CONFIRMED PHISHING: High-confidence malicious
  +-- SUSPICIOUS: Moderate indicators, needs analyst review
  +-- SPAM: Unwanted but not malicious
  +-- SIMULATION: Matches internal phishing test
  +-- CLEAN: Legitimate email, false report
  |
  v
[Automated response by classification]
  +-- PHISHING: Retract from all inboxes + block sender
  +-- SUSPICIOUS: Escalate to SOC analyst
  +-- SPAM: Move to junk for all recipients
  +-- SIMULATION: Credit reporter in training platform
  +-- CLEAN: Return to inbox
  |
  v
[Feedback to reporter]
  +-- "Thank you for reporting" (immediate)
  +-- Classification result (when complete)
  +-- Training tip (if false positive)
```

## Workflow 2: SOC Analyst Escalation

```
SOAR classifies report as SUSPICIOUS
  |
  v
[SOC analyst reviews]
  +-- Examine full email content and headers
  +-- Verify automated analysis results
  +-- Check for similar reports from other users
  |
  v
[Analyst decision]
  +-- Confirm malicious --> Trigger remediation playbook
  +-- Confirm clean --> Close and notify reporter
  +-- Need more info --> Contact reporter for context
```

---

## Working Template

## Reporting Button Configuration
| Setting | Value | Status |
|---|---|---|
| Button type | Microsoft built-in Report | |
| Reporting mailbox | phishing-reports@company.com | |
| Also send to Microsoft | Yes | |
| Supported platforms | Desktop, Web, Mobile | |

## Triage Automation Rules
| Classification | Criteria | Auto-Action |
|---|---|---|
| Confirmed Phishing | Score >= 50 | Retract + Block sender |
| Suspicious | Score 25-49 | Escalate to SOC analyst |
| Spam | Score 10-24 | Move to junk for all |
| Simulation | Matches sim subject | Credit reporter |
| Clean | Score < 10 | Return to inbox |

## Reporting Metrics Dashboard
| Metric | Target | Current |
|---|---|---|
| Report volume (monthly) | | |
| Mean time to triage | < 10 min | |
| Confirmed phishing caught | | |
| User report rate (sim) | > 70% | |
| False positive rate | < 30% | |
| Top reporter recognition | Monthly | |
