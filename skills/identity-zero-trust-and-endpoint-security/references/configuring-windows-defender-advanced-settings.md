# Configuring Windows Defender Advanced Settings

## API Reference

## PowerShell Cmdlets

| Cmdlet | Description |
|--------|-------------|
| `Get-MpComputerStatus` | Defender service status, signature version |
| `Get-MpPreference` | All Defender configuration preferences |
| `Set-MpPreference` | Modify Defender settings |
| `Get-MpThreatDetection` | Recent threat detections |
| `Add-MpPreference -AttackSurfaceReductionRules_Ids` | Enable ASR rules |

## Critical ASR Rule GUIDs

| GUID | Rule |
|------|------|
| `be9ba2d9-53ea-4cdc-84e5-9b1eeee46550` | Block executable from email |
| `d4f940ab-401b-4efc-aadc-ad5f3c50688a` | Block Office child processes |
| `3b576869-a4ec-4529-8536-b80a7769e899` | Block Office executable creation |
| `5beb7efe-fd9a-4556-801d-275e5ffc04cc` | Block obfuscated scripts |
| `56a863a9-875e-4185-98a7-b882c64b5ce5` | Block exploited signed drivers |

## ASR Rule Actions

| Value | Action |
|-------|--------|
| 0 | Disabled |
| 1 | Block |
| 2 | Audit |
| 6 | Warn |

## External References

- [Microsoft ASR Rules Reference](https://learn.microsoft.com/en-us/defender-endpoint/attack-surface-reduction-rules-reference)
- [Defender PowerShell Reference](https://learn.microsoft.com/en-us/powershell/module/defender/)
- [Tamper Protection](https://learn.microsoft.com/en-us/defender-endpoint/prevent-changes-to-security-settings-with-tamper-protection)

---

## Standards and Controls

## Primary Standards

### Microsoft Defender for Endpoint Documentation
- **Publisher**: Microsoft
- **URL**: https://learn.microsoft.com/en-us/defender-endpoint/
- **Scope**: Complete reference for MDE deployment, configuration, and management
- **Key sections**: ASR rules, exploit protection, network protection, controlled folder access

### MITRE ATT&CK Mapping for ASR Rules
- **Relevance**: Each ASR rule maps to specific ATT&CK techniques it mitigates
- **Key mappings**:
  - Block Office child processes → T1566.001 (Spearphishing Attachment)
  - Block credential stealing from LSASS → T1003.001 (OS Credential Dumping: LSASS)
  - Block PSExec/WMI → T1047 (WMI), T1570 (Lateral Tool Transfer)
  - Block WMI persistence → T1546.003 (WMI Event Subscription)

### CIS Microsoft Windows 11 Benchmark - Section 18.10
- **Publisher**: CIS
- **Relevance**: CIS benchmark sections covering Windows Defender configuration settings

## Compliance Mappings

| Framework | Requirement | MDE Coverage |
|-----------|------------|-------------|
| PCI DSS 4.0 | 5.2 - Anti-malware mechanisms | Defender AV + ASR rules + cloud protection |
| PCI DSS 4.0 | 5.3.1 - Anti-malware kept current | Automatic signature and engine updates |
| NIST 800-53 | SI-3 Malicious Code Protection | Defender real-time protection + BAFS |
| NIST 800-53 | SI-4 System Monitoring | MDE telemetry + advanced hunting |
| HIPAA | 164.308(a)(5)(ii)(B) - Malware protection | Defender AV + ransomware protection |
| ISO 27001 | A.12.2.1 - Controls against malware | Full MDE stack |
| ACSC E8 | Configure Microsoft Office macro settings | ASR rules for Office macro blocking |

## ASR Rule Reference

| GUID | Rule Name | Recommended Mode |
|------|----------|-----------------|
| BE9BA2D9-53EA-4CDC-84E5-9B1EEEE46550 | Block executable content from email | Block |
| D4F940AB-401B-4EFC-AADC-AD5F3C50688A | Block Office child processes | Block |
| 3B576869-A4EC-4529-8536-B80A7769E899 | Block Office from creating executables | Block |
| 75668C1F-73B5-4CF0-BB93-3ECF5CB7CC84 | Block Office from injecting into processes | Block |
| D3E037E1-3EB8-44C8-A917-57927947596D | Block JS/VBS launching executables | Block |
| 5BEB7EFE-FD9A-4556-801D-275E5FFC04CC | Block obfuscated scripts | Audit first |
| 92E97FA1-2EDF-4476-BDD6-9DD0B4DDDC7B | Block Win32 API calls from macros | Block |
| 9E6C4E1F-7D60-472F-BA1A-A39EF669E4B2 | Block credential stealing from LSASS | Block |
| D1E49AAC-8F56-4280-B9BA-993A6D77406C | Block PSExec/WMI process creation | Audit first |
| B2B3F03D-6A65-4F7B-A9C7-1C7EF74A9BA4 | Block untrusted USB processes | Block |
| E6DB77E5-3DF2-4CF1-B95A-636979351E5B | Block WMI event subscription persistence | Block |
| 56A863A9-875E-4185-98A7-B882C64B5CE5 | Block vulnerable signed drivers | Block |

## Supporting References

- **ASR Rules Reference**: https://learn.microsoft.com/en-us/defender-endpoint/attack-surface-reduction-rules-reference
- **Controlled Folder Access**: https://learn.microsoft.com/en-us/defender-endpoint/controlled-folders
- **Network Protection**: https://learn.microsoft.com/en-us/defender-endpoint/network-protection
- **Exploit Protection**: https://learn.microsoft.com/en-us/defender-endpoint/exploit-protection

---

## Workflows

## Workflow 1: ASR Rule Deployment

```
[Identify ASR rules to deploy]
    │
    ▼
[Deploy all rules in Audit mode via Intune/GPO]
    │
    ▼
[Monitor ASR audit events for 2-4 weeks]
    │
    ├── Review events in M365 Defender portal
    ├── Identify false positives per rule
    │
    ▼
[Create exclusions for legitimate applications]
    │
    ▼
[Switch low-risk rules to Block mode]
    │  (Office rules, email content, USB)
    │
    ▼
[Monitor for 1 week]
    │
    ├── No issues ──► [Switch remaining rules to Block mode]
    │
    └── Issues found ──► [Add exclusions, maintain Audit mode for affected rules]
                              │
                              ▼
                         [Re-evaluate after 2 weeks]
```

## Workflow 2: Controlled Folder Access Deployment

```
[Enable Controlled Folder Access in Audit mode]
    │
    ▼
[Monitor Event ID 1124 for blocked write attempts]
    │
    ▼
[Categorize blocked applications]
    │
    ├── Legitimate business app ──► [Add to allowed applications list]
    │
    ├── Backup/sync software ──► [Add to allowed applications list]
    │
    └── Unknown/suspicious ──► [Investigate, potentially malicious]
    │
    ▼
[Switch to Enabled (Block) mode]
    │
    ▼
[Add custom protected folders beyond defaults]
    │
    ▼
[Ongoing monitoring via M365 Defender dashboard]
```

## Workflow 3: Defender Configuration Audit

```
[Quarterly Defender Configuration Review]
    │
    ▼
[Export current Defender settings from all endpoints]
    │
    ├── PowerShell: Get-MpPreference | Export-Clixml
    ├── Intune: Endpoint security reports
    │
    ▼
[Compare against security baseline]
    │
    ├── All settings match baseline ──► [Document compliance, next review]
    │
    └── Drift detected ──► [Investigate cause]
                                │
                                ├── Unauthorized change ──► [Security incident, restore settings]
                                │
                                └── Authorized exception ──► [Document, update baseline]
```

## Workflow 4: False Positive Handling

```
[User reports blocked application]
    │
    ▼
[Identify which Defender feature blocked it]
    │
    ├── ASR rule ──► [Check ASR event log for specific rule GUID]
    │                     │
    │                     ▼
    │                [Create ASR exclusion for file/folder/process]
    │
    ├── Controlled Folder ──► [Add application to allowed list]
    │
    ├── Network Protection ──► [Review URL/domain, submit false positive to Microsoft]
    │
    └── Real-time AV ──► [Submit file for analysis, create AV exclusion if clean]
    │
    ▼
[Deploy exclusion via Intune/GPO]
    │
    ▼
[Verify application works, document exclusion]
```

---

## Working Template

## Environment Information

| Field | Value |
|-------|-------|
| Endpoint OS | Windows 10/11 Enterprise |
| MDE License | E5 / Defender P2 / Standalone |
| Deployment Method | Intune / SCCM / GPO |
| Configuration Date | |
| Configured By | |

## ASR Rule Configuration

| GUID | Rule Name | Mode | Exclusions |
|------|----------|------|------------|
| BE9BA2D9-... | Block executable content from email | Block / Audit | |
| D4F940AB-... | Block Office child processes | Block / Audit | |
| 3B576869-... | Block Office executable creation | Block / Audit | |
| 75668C1F-... | Block Office code injection | Block / Audit | |
| D3E037E1-... | Block JS/VBS launching executables | Block / Audit | |
| 5BEB7EFE-... | Block obfuscated scripts | Block / Audit | |
| 92E97FA1-... | Block Win32 API from macros | Block / Audit | |
| 9E6C4E1F-... | Block LSASS credential stealing | Block / Audit | |
| D1E49AAC-... | Block PSExec/WMI processes | Block / Audit | |
| B2B3F03D-... | Block untrusted USB processes | Block / Audit | |
| E6DB77E5-... | Block WMI persistence | Block / Audit | |
| 56A863A9-... | Block vulnerable signed drivers | Block / Audit | |

## Controlled Folder Access

| Setting | Value |
|---------|-------|
| Mode | Enabled / Audit |
| Protected Folders | Default + custom |
| Allowed Applications | |

### Custom Protected Folders

| Path | Justification |
|------|--------------|
| | |

### Allowed Applications

| Application Path | Reason |
|-----------------|--------|
| | |

## Network Protection

| Setting | Value |
|---------|-------|
| Network Protection | Enabled / Audit |
| Web Content Filtering | Enabled / Disabled |
| Blocked Categories | |

## Cloud Protection

| Setting | Value |
|---------|-------|
| MAPS Reporting | Advanced |
| Sample Submission | SendAllSamples |
| Block at First Sight | Enabled |
| Cloud Block Level | High |
| Cloud Timeout | 50 seconds |
| Tamper Protection | On |

## Exclusions Register

| Type | Value | Reason | Approved By | Review Date |
|------|-------|--------|-------------|-------------|
| Path | | | | |
| Process | | | | |
| Extension | | | | |

## Validation Checklist

- [ ] All ASR rules active (Block or Audit)
- [ ] Controlled Folder Access enabled
- [ ] Network Protection enabled
- [ ] Cloud protection set to Advanced
- [ ] Tamper Protection enabled in M365 portal
- [ ] Signature update interval set to hourly
- [ ] PUA protection enabled
- [ ] No excessive exclusions configured

## Sign-Off

| Role | Name | Date |
|------|------|------|
| Security Engineer | | |
| Endpoint Admin | | |
