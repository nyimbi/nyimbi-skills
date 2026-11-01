# Implementing Honeypot For Ransomware Detection

## API Reference

## Canary File Strategy

| Name Pattern | Extension | Purpose |
|-------------|-----------|---------|
| `!Accounting_*` | .docx, .xlsx | Sorted first alphabetically |
| `~$Confidential_*` | .pdf, .csv | Mimics temp/open Office files |
| `!Payroll_*` | .xlsx, .bak | High-value bait |

## Integrity Monitoring

```python
import hashlib
from pathlib import Path
content = Path("canary.docx").read_bytes()
sha256 = hashlib.sha256(content).hexdigest()
```

## Ransomware Extension Indicators

| Extension | Ransomware Family |
|-----------|------------------|
| `.encrypted` | Generic |
| `.locked` | LockBit, GandCrab |
| `.crypto` | CryptoLocker variants |
| `.ransom` | Generic |
| `.enc` | Various |

## Samba Honeypot Share (full_audit VFS)

```ini
[FinanceArchive]
    path = /srv/honeypot
    vfs objects = full_audit
    full_audit:success = open opendir write rename unlink
    full_audit:failure = open
    full_audit:facility = LOCAL7
    full_audit:priority = NOTICE
```

## Thinkst Canary API

```bash
# List incidents
curl "https://DOMAIN.canary.tools/api/v1/incidents/all" \
  -d auth_token=TOKEN

# Acknowledge incident
curl "https://DOMAIN.canary.tools/api/v1/incident/acknowledge" \
  -d auth_token=TOKEN -d incident=INC_ID
```

## Detection Thresholds

| Metric | Threshold | Severity |
|--------|----------|----------|
| Files modified in 60s | > 50 | CRITICAL |
| Canary file deleted | Any | CRITICAL |
| Canary hash changed | Any | CRITICAL |
| Known ransom extensions | Any | CRITICAL |

### References

- Thinkst Canary: https://canary.tools/
- CISA Ransomware Guide: https://www.cisa.gov/stopransomware
- Canarytokens: https://canarytokens.org/

---

## Standards and Controls

## MITRE ATT&CK
- T1486: Data Encrypted for Impact (detection via canary file modification)
- T1021.002: SMB/Windows Admin Shares (detection via honeypot share access)
- T1083: File and Directory Discovery (detection via honeypot folder browsing)

## NIST SP 800-53 Rev 5
- SI-4: System Monitoring (honeypots as monitoring component)
- AU-6: Audit Record Review, Analysis, and Reporting (canary file audit logging)

## CIS Controls v8
- Control 13.1: Centralize security event alerting (integrate honeypot alerts into SIEM)
- Control 13.8: Deploy intrusion detection/prevention systems

## Tools Documentation
- Thinkst Canary: https://canary.tools/
- Canarytokens: https://canarytokens.org/
- OpenCanary: https://github.com/thinkst/opencanary
- FSRM: https://learn.microsoft.com/en-us/windows-server/storage/fsrm/fsrm-overview
- Elastic Ransomware Protection: https://www.elastic.co/security-labs/ransomware-in-the-honeypot-how-we-capture-keys

---

## Workflows

## Workflow 1: Canary File Deployment

```
Start
  |
  v
[Inventory all file shares] --> Map share names, paths, user population
  |
  v
[Select canary file placement strategy]
  |-- Root of each share (first files encrypted)
  |-- Key subdirectories (finance, HR, executive)
  |-- Alphabetically early names (!_, 000_, AAA_)
  |
  v
[Generate canary files with realistic content]
  |-- .docx, .xlsx, .pdf formats
  |-- Realistic filenames matching share context
  |-- Hidden attribute to prevent user interaction
  |
  v
[Deploy monitoring]
  |-- FSRM file screens for ransomware extensions
  |-- FileSystemWatcher for canary file changes
  |-- Audit logging on canary files
  |
  v
[Integrate with SIEM and automated containment]
  |
  v
[Test with controlled encryption tool]
  |
  v
End
```

## Workflow 2: Honeypot Alert Response

```
Canary Alert Triggered
  |
  v
[Identify source IP and user from alert]
  |
  v
[Automated containment (within 30 seconds)]
  |-- NAC: Quarantine source IP
  |-- EDR: Isolate endpoint
  |-- AD: Disable user account
  |
  v
[SOC validates alert]
  |-- Check for legitimate activity (file migration, AV scan)
  |-- If FP --> Restore access, tune alerting
  |-- If TP --> Escalate to IR team
  |
  v
[IR team assesses scope]
  |-- How many canary files triggered?
  |-- How many endpoints involved?
  |-- Is encryption spreading?
  |
  v
[Full incident response activation]
  |
  v
End
```

---

## Working Template

## Deployment Plan

| Share | Canary Count | File Types | Naming Convention | Monitoring Method |
|-------|-------------|------------|-------------------|-------------------|
| | | | | |

## Canary File Inventory

| File Path | Type | Hash (SHA-256) | Deploy Date | Status |
|-----------|------|----------------|-------------|--------|
| | | | | |

## Honeypot Shares

| Share Name | Server | Apparent Content | Access Logging | Alert Destination |
|-----------|--------|-----------------|---------------|-------------------|
| | | | | |

## Alert Integration

- [ ] SIEM webhook configured
- [ ] Automated NAC quarantine tested
- [ ] EDR isolation API integrated
- [ ] Email/SMS alerts configured for on-call
- [ ] Canary alerts have CRITICAL priority in SIEM

## Validation Testing

| Test Date | Method | Canaries Triggered | Alert Time | Containment Time | Result |
|-----------|--------|-------------------|------------|------------------|--------|
| | | | | | |
