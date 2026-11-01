# Implementing Endpoint Dlp Controls

## API Reference

## Sensitive Data Patterns

| Pattern | Regex | Severity |
|---------|-------|----------|
| SSN | `\d{3}-\d{2}-\d{4}` | HIGH |
| Credit Card | `4[0-9]{12}(?:[0-9]{3})?` | HIGH |
| AWS Key | `AKIA[0-9A-Z]{16}` | CRITICAL |
| Private Key | `-----BEGIN.*PRIVATE KEY-----` | CRITICAL |
| API Key | `api[_-]?key\s*[:=]\s*[a-zA-Z0-9]{20,}` | HIGH |

## DLP Channels

| Channel | Monitoring Method |
|---------|-------------------|
| USB/Removable | Device event logs |
| Cloud Storage | URL/domain filtering |
| Email | Attachment scanning |
| Clipboard | Process monitoring |
| Print | Print spooler events |

## Microsoft Purview DLP API

```python
import requests
headers = {"Authorization": "Bearer <token>"}
resp = requests.get(
    "https://graph.microsoft.com/v1.0/security/alerts_v2",
    headers=headers,
    params={"$filter": "category eq 'DataLossPrevention'"})
```

## CrowdStrike Falcon DLP

```bash
curl -X GET "https://api.crowdstrike.com/dlp/entities/policies/v1" \
  -H "Authorization: Bearer $TOKEN"
```

## File Scanning

```python
from pathlib import Path
import re
SENSITIVE_EXTS = {".pem", ".key", ".env", ".kdbx", ".pfx"}
for f in Path("/data").rglob("*"):
    if f.suffix in SENSITIVE_EXTS or re.search(r"AKIA", f.read_text()):
        print(f"ALERT: {f}")
```

### References

- Microsoft Purview DLP: https://learn.microsoft.com/en-us/purview/dlp-learn-about-dlp
- CrowdStrike Falcon DLP: https://www.crowdstrike.com/platform/data-protection/

---

## Standards and Controls

- **NIST SP 800-53 SC-7**: Boundary Protection - DLP enforces data boundaries
- **PCI DSS 4.0 Req 3**: Protect stored account data
- **GDPR Article 32**: Security of processing - preventing unauthorized data transfer
- **HIPAA 164.312(e)(1)**: Transmission security for ePHI
- **Microsoft Purview DLP**: https://learn.microsoft.com/en-us/purview/dlp-learn-about-dlp

---

## Workflows

## DLP Deployment
```
[Identify sensitive data types] → [Create SITs and policies]
  → [Deploy in audit mode] → [Review Activity Explorer for 2-4 weeks]
  → [Tune rules and exclusions] → [Enable enforcement]
  → [Monitor alerts and override rates] → [Quarterly policy review]
```

---

## Working Template

## Policy Summary
| Policy Name | SITs | Action | Scope |
|------------|------|--------|-------|
| | | Audit / Block | Devices |

## Monitoring Metrics
| Metric | Value |
|--------|-------|
| Policy matches (weekly) | |
| Override rate | % |
| Top triggered SIT | |
| False positive rate | % |

## Sign-Off
| Role | Name | Date |
|------|------|------|
| Data Protection Officer | | |
| Security | | |
