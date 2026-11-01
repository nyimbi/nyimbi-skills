# Detecting Qr Code Phishing With Email Security

## API Reference

## pyzbar — QR/Barcode Decoding

### Installation
```bash
pip install pyzbar Pillow
# On Linux: apt-get install libzbar0
```

### Core Functions
```python
from pyzbar.pyzbar import decode
from PIL import Image

results = decode(Image.open("qr.png"))
for r in results:
    print(r.type)     # "QRCODE"
    print(r.data)     # b"https://..."
    print(r.rect)     # Rect(left=40, top=40, width=200, height=200)
```

### Decoded Object Attributes
| Attribute | Type | Description |
|-----------|------|-------------|
| `data` | bytes | Decoded content |
| `type` | str | Barcode type (QRCODE, EAN13, etc.) |
| `rect` | Rect | Bounding rectangle |
| `polygon` | list | Corner points |
| `quality` | int | Decode quality score |

## Python email Module — EML Parsing

### Parsing an EML file
```python
import email
from email import policy

with open("message.eml", "rb") as f:
    msg = email.message_from_binary_file(f, policy=policy.default)

subject = msg["Subject"]
sender = msg["From"]
```

### Walking MIME Parts
```python
for part in msg.walk():
    ctype = part.get_content_type()
    if ctype.startswith("image/"):
        payload = part.get_payload(decode=True)
        filename = part.get_filename()
```

## URL Analysis Indicators

### Suspicious TLD List
`.xyz`, `.top`, `.club`, `.work`, `.buzz`, `.tk`, `.ml`, `.ga`, `.cf`, `.gq`

### Phishing URL Patterns
| Pattern | Risk |
|---------|------|
| IP address in domain | High |
| Domain > 40 chars | Medium |
| HTTP (no TLS) | Medium |
| 3+ subdomains | Medium |
| URL shortener | High |
| Base64 in path | High |

## Microsoft Defender for Office 365 — Safe Links API

### Check URL reputation
```http
POST https://graph.microsoft.com/v1.0/security/tiIndicators
Content-Type: application/json
Authorization: Bearer {token}

{
  "targetProduct": "Azure Sentinel",
  "threatType": "Phishing",
  "url": "https://suspicious-domain.xyz/login"
}
```

## VirusTotal URL Scan API

### Submit URL
```http
POST https://www.virustotal.com/api/v3/urls
x-apikey: {API_KEY}
Content-Type: application/x-www-form-urlencoded

url=https://suspicious-domain.xyz
```

### Response Fields
| Field | Description |
|-------|-------------|
| `data.attributes.last_analysis_stats.malicious` | Engines flagging as malicious |
| `data.attributes.last_analysis_stats.harmless` | Engines flagging as clean |
| `data.attributes.categories` | URL categorization |

---

## Standards and Controls

## Industry Statistics (2025-2026)
- Quishing incidents grew from 46,000 to 250,000 between Aug-Nov 2025 (Kaspersky)
- 89.3% of QR code phishing targets credential theft
- 12% of January 2026 attacks used ASCII text-based QR codes
- Only 36% of quishing incidents accurately identified by recipients
- 25% year-over-year growth in quishing incidents

## MITRE ATT&CK References
- **T1566.001**: Phishing: Spearphishing Attachment (QR in PDF/image)
- **T1566.002**: Phishing: Spearphishing Link (QR-encoded URL)
- **T1204.001**: User Execution: Malicious Link (user scans QR)
- **T1598.003**: Phishing for Information: Spearphishing Link

## Quishing Attack Patterns
| Pattern | Description | Detection Difficulty |
|---|---|---|
| Inline QR image | QR code embedded directly in email body | Medium |
| PDF attachment QR | QR code inside attached PDF document | High |
| Split QR code | QR divided into two benign-looking images | Very High |
| ASCII QR code | QR rendered as text characters | Very High |
| Nested QR code | QR within QR with intermediate redirect | High |
| Styled QR code | Artistic QR with logos/colors | Medium |

## Common Quishing Themes
- MFA enrollment/reset requiring QR scan
- Document signing via QR code
- Voicemail notification with QR access
- Package delivery QR confirmation
- IT security update requiring QR authentication
- Shared document access via QR

## Detection Technologies
- Multimodal AI (OCR + deep image + NLP)
- Computer vision QR code detection
- URL reputation analysis for decoded URLs
- Mobile threat defense QR scanning
- Behavioral analysis of image-only emails

---

## Workflows

## Workflow 1: QR Code Email Detection Pipeline

```
Inbound email arrives at gateway
  |
  v
[Standard text/URL scanning]
  +-- Check text-based URLs (standard pipeline)
  +-- No malicious URLs found in text
  |
  v
[Image analysis module]
  +-- Scan all embedded images and attachments
  +-- Apply QR code detection algorithm
  +-- Check for ASCII/text-rendered QR codes
  +-- Scan PDF attachments for embedded QR codes
  |
  v
[QR code detected?]
  +-- NO --> Continue standard delivery
  +-- YES --> Extract encoded URL
  |
  v
[URL reputation and analysis]
  +-- Check URL against threat intelligence feeds
  +-- Check domain age and registration data
  +-- Submit to sandbox for real-time analysis
  +-- Check for credential harvesting indicators
  |
  v
[Decision]
  +-- MALICIOUS URL: Block email, alert SOC
  +-- SUSPICIOUS URL: Quarantine, add warning banner
  +-- UNKNOWN URL: Tag email with QR warning banner
  +-- CLEAN URL: Deliver with informational banner
```

## Workflow 2: Quishing Incident Response

```
User reports QR code phishing email
  |
  v
[Triage (15 minutes)]
  +-- Extract QR code and decode URL
  +-- Check if URL is active credential harvester
  +-- Search mailboxes for same email to other recipients
  |
  v
[Containment]
  +-- Block sender domain across email gateway
  +-- Retract email from all recipient inboxes
  +-- Block decoded URL at web proxy/firewall
  +-- If user scanned: check for credential compromise
  |
  v
[Investigation]
  +-- Did any user submit credentials on phishing page?
  +-- Check authentication logs for compromised accounts
  +-- If credentials entered: force password reset + revoke sessions
  +-- Review phishing page infrastructure
  |
  v
[Recovery and prevention]
  +-- Add QR URL pattern to detection rules
  +-- Update security awareness training
  +-- Send targeted alert to affected users
  +-- Document IOCs for threat intelligence sharing
```

## Workflow 3: Mobile QR Scanning Protection

```
User scans QR code with mobile device
  |
  v
[Mobile threat defense intercepts]
  +-- Decode QR destination URL
  +-- Check against mobile threat intelligence
  |
  v
[URL assessment]
  +-- KNOWN MALICIOUS: Block and alert user
  +-- SUSPICIOUS: Display warning, require confirmation
  +-- CREDENTIAL PAGE: Extra warning about entering passwords
  +-- CLEAN: Allow access
  |
  v
[If user proceeds to suspicious site]
  +-- Route through secure browser/VPN
  +-- Monitor for credential submission
  +-- Log URL and user action for SOC review
```

---

## Working Template

## Quishing Detection Rules
| Rule | Condition | Action | Status |
|---|---|---|---|
| QR in image | QR code detected in embedded image | Extract URL + analyze | |
| QR in PDF | QR code detected in PDF attachment | Extract URL + analyze | |
| ASCII QR | Text-rendered QR code pattern | Decode + analyze | |
| Image-only email | Email with image but minimal text | Flag for review | |
| MFA QR theme | QR + MFA/authentication language | High priority alert | |

## Common Quishing Themes to Monitor
- [ ] MFA enrollment requiring QR code scan
- [ ] Document signing via QR code
- [ ] Voicemail access via QR code
- [ ] Package delivery confirmation QR
- [ ] IT security update with QR authentication
- [ ] Shared document access via QR

## Mobile Protection Controls
- [ ] Mobile threat defense deployed with QR scanning
- [ ] MDM policy warns before opening QR URLs
- [ ] Corporate VPN required for QR destinations
- [ ] User training on safe QR scanning completed

## Incident Response for Quishing
| Step | Action | Responsible |
|---|---|---|
| 1 | Decode QR and extract URL | SOC Analyst |
| 2 | Check if URL is active phishing page | SOC Analyst |
| 3 | Search for same email across all mailboxes | Email Admin |
| 4 | Retract email from all recipients | Email Admin |
| 5 | Block URL at web proxy/firewall | Network Security |
| 6 | Check if any user scanned and submitted credentials | SOC Lead |
| 7 | Force password reset for affected users | IAM Team |
