# Implementing Mimecast Targeted Attack Protection

## API Reference

## Mimecast API Authentication

```python
import requests
headers = {"Authorization": "MC access_key:secret_key",
           "x-mc-app-id": "app-id"}
resp = requests.post("https://us-api.mimecast.com/api/ttp/url/get-logs",
                     headers=headers, json={"data": [{"from": "2024-01-01"}]})
```

## TTP API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/api/ttp/url/get-logs` | URL Protection logs |
| `/api/ttp/attachment/get-logs` | Attachment sandbox logs |
| `/api/ttp/impersonation/get-logs` | Impersonation detections |

## URL Protection Actions

| Action | Description |
|--------|-------------|
| allow | URL permitted |
| block | URL blocked (malicious) |
| warn | User warned before click |
| sandbox | Deferred for sandbox analysis |

## Attachment Sandbox Results

| Result | Severity |
|--------|----------|
| safe | INFO |
| suspicious | MEDIUM |
| malicious | CRITICAL |
| sandbox_timeout | HIGH |

## Impersonation Types

| Type | Description |
|------|-------------|
| Internal | Employee name spoofing |
| External | Vendor/partner spoofing |
| Domain | Similar domain detection |

### References

- Mimecast API: https://developer.services.mimecast.com/
- TTP URL Protection: https://developer.services.mimecast.com/docs/threatsintel/1/routes/ttp/url/get-logs/post

---

## Standards and Controls

## MITRE ATT&CK References
- **T1566.001**: Phishing: Spearphishing Attachment
- **T1566.002**: Phishing: Spearphishing Link
- **T1534**: Internal Spearphishing
- **T1598**: Phishing for Information
- **T1656**: Impersonation
- **T1204.001**: User Execution: Malicious Link
- **T1204.002**: User Execution: Malicious File

## Mimecast TTP Components
| Component | Version | Key Feature |
|---|---|---|
| URL Protect | Current | Pre-delivery hold (Nov 2025 default) |
| Attachment Protect | Current | Safe File + Dynamic sandbox |
| Impersonation Protect | Current | Hit 1 (VIP) / Hit 3 (Default) |
| Internal Email Protect | Current | Journal-based internal scanning |

## Compliance Alignment
- **CIS Controls v8 Control 9.2**: Use DNS filtering services
- **CIS Controls v8 Control 9.6**: Block unnecessary file types
- **NIST SP 800-177**: Trustworthy Email
- **SOC 2 CC6.1**: Logical and physical access controls
- **ISO 27001 A.8.23**: Web filtering

## Impersonation Protection Indicators
| Indicator | Description | Weight |
|---|---|---|
| Display name match | External sender uses internal VIP display name | High |
| Domain similarity | Sender domain visually similar to internal domain | High |
| Reply-to mismatch | Reply-to differs from From address | Medium |
| Newly observed | First-time sender to recipient | Medium |
| Header anomaly | Unusual mail routing or missing authentication | Medium |

## Integration Points
- Microsoft 365 via connector and journaling
- Google Workspace via gateway routing
- SIEM via syslog or API (Splunk, QRadar, Sentinel)
- SOAR platforms via Mimecast API
- Directory sync via Active Directory / Azure AD

---

## Workflows

## Workflow 1: URL Protect Processing

```
Inbound email with URLs arrives
  |
  v
[Pre-delivery URL check]
  +-- Extract all URLs from body and attachments
  +-- Check against Mimecast threat intelligence
  +-- KNOWN MALICIOUS --> Hold/Block message
  +-- SUSPICIOUS --> Hold for deeper analysis
  +-- CLEAN --> Proceed to rewriting
  |
  v
[URL rewriting]
  +-- Replace original URLs with Mimecast proxy URLs
  +-- Preserve original URL in encoded format
  +-- Apply per-policy rewriting rules
  |
  v
[Message delivered to user inbox]
  |
  v
[User clicks rewritten URL]
  |
  v
[Time-of-click analysis]
  +-- Real-time page scan and sandbox
  +-- Check for credential harvesting forms
  +-- Check for malware downloads
  |
  v
[Decision]
  +-- SAFE: Redirect to original URL
  +-- MALICIOUS: Display block page
  +-- SUSPICIOUS: Display warning with proceed option
```

## Workflow 2: Attachment Protect Pipeline

```
Email with attachment arrives
  |
  v
[Static analysis]
  +-- File type identification
  +-- Signature matching
  +-- Known malware hash check
  |
  v
[Policy evaluation]
  +-- Safe File mode: Convert to safe format (PDF)
  +-- Dynamic mode: Full sandbox detonation
  +-- Bypass: Whitelisted sender/type
  |
  v
[Dynamic sandbox (if configured)]
  +-- Execute in isolated environment
  +-- Monitor for malicious behavior
  +-- Check for C2 callbacks, file drops, registry changes
  +-- Timeout: up to 7 minutes
  |
  v
[Verdict]
  +-- CLEAN: Deliver original attachment
  +-- MALICIOUS: Quarantine, notify admin
  +-- TIMEOUT: Deliver with warning or hold per policy
```

## Workflow 3: Impersonation Protect Analysis

```
Inbound email arrives
  |
  v
[Identifier check against VIP list]
  +-- Compare display name to VIP names
  +-- Check domain similarity to internal domains
  +-- Verify reply-to alignment
  +-- Check if sender is newly observed
  |
  v
[Hit scoring]
  +-- Hit 1 policy (VIP): 1+ indicator match
  +-- Hit 3 policy (Default): 3+ indicator matches
  |
  v
[Action based on hit level]
  +-- QUARANTINE: High confidence impersonation
  +-- TAG: Moderate confidence, add warning banner
  +-- LOG: Low confidence, record for analysis
  +-- DELIVER: No indicators matched
```

---

## Working Template

## TTP Policy Configuration
| Module | Status | Mode | Scope |
|---|---|---|---|
| URL Protect | | Rewrite + Pre-delivery Hold | All inbound |
| Attachment Protect | | Dynamic sandbox | All inbound |
| Impersonation Protect (Default) | | Hit 3 | All inbound |
| Impersonation Protect (VIP) | | Hit 1 | VIP senders |
| Internal Email Protect | | URL + Attachment scan | Journaled |

## VIP List for Impersonation Protect
| Name | Title | Email | Domain |
|---|---|---|---|
| | CEO | | |
| | CFO | | |
| | CTO | | |
| | VP Finance | | |
| | General Counsel | | |

## Deployment Phases
- [ ] Phase 1: Configure URL Protect (pilot group)
- [ ] Phase 2: Configure Attachment Protect (pilot group)
- [ ] Phase 3: Configure Impersonation Protect with VIP list
- [ ] Phase 4: Enable Internal Email Protect via journaling
- [ ] Phase 5: Roll out to all users
- [ ] Phase 6: Tune policies based on false positive feedback

## Validation Checklist
- [ ] URL Protect rewrites links in test email
- [ ] URL Pre-delivery Hold stops weaponized link
- [ ] Attachment Protect sandboxes EICAR test file
- [ ] Impersonation Protect flags test BEC email
- [ ] Internal Email Protect detects test internal phishing
- [ ] Threat Dashboard shows detection metrics
