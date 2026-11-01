# Implementing Email Sandboxing With Proofpoint

## API Reference

## Proofpoint TAP SIEM API

```python
import requests
resp = requests.get(
    "https://tap-api-v2.proofpoint.com/v2/siem/all",
    auth=(principal, secret),
    params={"sinceSeconds": 3600, "format": "json"})
data = resp.json()
# Keys: messagesDelivered, messagesBlocked, clicksPermitted, clicksBlocked
```

## TAP API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/v2/siem/all` | All threat events |
| `/v2/siem/messages/blocked` | Blocked messages only |
| `/v2/siem/messages/delivered` | Delivered threats |
| `/v2/siem/clicks/blocked` | Blocked URL clicks |
| `/v2/siem/clicks/permitted` | Permitted URL clicks |

## Threat Categories

| Category | Description | Severity |
|----------|-------------|----------|
| Malware | Malicious attachment | CRITICAL |
| Phish | Credential harvesting | HIGH |
| Impostor | BEC/spoofing | HIGH |
| Spam | Unsolicited | LOW |

## URL Defense Configuration

```json
{
  "url_defense": {
    "rewrite_all_urls": true,
    "real_time_scanning": true,
    "sandbox_detonation": true,
    "click_time_protection": true
  }
}
```

## Splunk Integration

```spl
index=proofpoint sourcetype=tap:siem
| where classification="malicious"
| stats count by sender, threatType, subject
```

### References

- Proofpoint TAP API: https://help.proofpoint.com/Threat_Insight_Dashboard/API_Documentation
- Proofpoint Email Protection: https://www.proofpoint.com/us/products/email-security-and-protection

---

## Standards and Controls

## MITRE ATT&CK Coverage
- **T1566.001**: Phishing: Spearphishing Attachment (primary detection)
- **T1566.002**: Phishing: Spearphishing Link (URL Defense)
- **T1204.001/002**: User Execution: Malicious Link/File
- **T1059**: Command and Scripting Interpreter (macro detection)
- **T1027**: Obfuscated Files or Information

## NIST Guidelines
- **NIST SP 800-177**: Trustworthy Email - attachment security
- **NIST SP 800-83 Rev.1**: Guide to Malware Incident Prevention
- **NIST SP 800-53**: SI-3 Malicious Code Protection, SI-8 Spam Protection

## Proofpoint TAP API Endpoints
| Endpoint | Description |
|---|---|
| `/v2/siem/all` | All threat events for SIEM |
| `/v2/siem/messages/blocked` | Blocked message events |
| `/v2/siem/messages/delivered` | Delivered message events with threats |
| `/v2/siem/clicks/blocked` | Blocked URL click events |
| `/v2/siem/clicks/permitted` | Permitted URL click events |
| `/v2/people/vap` | Very Attacked People list |
| `/v2/campaign/{id}` | Campaign details |

## Sandbox File Types
| Category | Extensions | Action |
|---|---|---|
| Executables | .exe, .dll, .scr, .com | Detonate + Block |
| Office docs | .doc(x/m), .xls(x/m), .ppt(x/m) | Detonate |
| PDF | .pdf | Detonate |
| Archives | .zip, .rar, .7z, .tar.gz | Extract + Detonate |
| Scripts | .js, .vbs, .ps1, .bat, .cmd | Block |
| Disk images | .iso, .img, .vhd | Detonate |

---

## Workflows

## Workflow 1: Attachment Detonation Pipeline
```
Email with attachment arrives at Proofpoint gateway
  |
  v
[Pre-filter: Check attachment type]
  +-- Blocked types (.bat, .ps1, .vbs) --> Quarantine immediately
  +-- Detonable types --> Send to sandbox
  +-- Known safe types (.txt, .csv) --> Deliver
  |
  v
[Sandbox detonation]
  +-- Execute in multiple environments (Win10, Win11, macOS)
  +-- Monitor: file system changes, registry, network, process creation
  +-- Timeout: 60-120 seconds per environment
  |
  v
[Verdict]
  +-- MALICIOUS --> Quarantine, alert, extract IOCs
  +-- SUSPICIOUS --> Quarantine for analyst review
  +-- CLEAN --> Deliver with dynamic delivery
```

## Workflow 2: URL Defense Time-of-Click
```
Email with URL arrives
  |
  v
[URL rewritten to Proofpoint URL Defense proxy]
  |
  v
[Email delivered to user]
  |
  v
[User clicks rewritten URL]
  |
  v
[Proofpoint performs real-time analysis]
  +-- Reputation check
  +-- Content analysis
  +-- Sandbox detonation of landing page
  |
  +-- SAFE --> Redirect to original URL
  +-- MALICIOUS --> Block access, show warning page
  +-- SUSPICIOUS --> Show interstitial warning, allow proceed
```

## Workflow 3: TAP Dashboard Monitoring
```
Daily operations:
  +-- Review TAP Dashboard threat digest
  +-- Check VAP (Very Attacked People) changes
  +-- Review campaign clusters
  +-- Investigate quarantined messages
  +-- Monitor false positive rate
  |
Weekly:
  +-- Analyze threat trends
  +-- Review sandboxing effectiveness
  +-- Tune policies based on FP/FN data
  +-- Update blocked file type list
  |
Monthly:
  +-- Generate executive report from TAP
  +-- Review VAP list with HR/management
  +-- Assess ROI and threat prevention metrics
```

---

## Working Template

## Deployment Info
- **Product**: Proofpoint Email Protection + TAP
- **Deployment Date**: [YYYY-MM-DD]
- **MX Records Updated**: Yes/No
- **SIEM Integration**: [Splunk / Sentinel / QRadar]

## Attachment Sandbox Policy
| File Type | Action | Sandbox Env | Timeout |
|---|---|---|---|
| .exe, .dll, .scr | Detonate + Block | Win10, Win11 | 120s |
| .doc(m), .xls(m), .ppt(m) | Detonate (dynamic delivery) | Win10 + Office | 90s |
| .pdf | Detonate | Win10 + Reader | 60s |
| .zip, .rar, .7z | Extract + Detonate contents | All | 120s |
| .iso, .img | Detonate | Win10 | 120s |
| .js, .vbs, .ps1, .bat | Block (no detonation) | N/A | N/A |

## URL Defense Policy
| Setting | Value |
|---|---|
| URL rewriting | All inbound email |
| Time-of-click analysis | Enabled |
| Block malicious URLs | Yes |
| Suspicious URL interstitial | Enabled |
| Allowed domains bypass | [list internal domains] |

## Monitoring Checklist
- [ ] Daily: Review TAP Dashboard threat digest
- [ ] Daily: Check quarantine for false positives
- [ ] Weekly: Review VAP list
- [ ] Weekly: Analyze threat trends
- [ ] Monthly: Generate executive threat report
- [ ] Quarterly: Policy tuning review
