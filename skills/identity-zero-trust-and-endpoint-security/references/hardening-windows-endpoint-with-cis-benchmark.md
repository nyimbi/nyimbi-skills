# Hardening Windows Endpoint With Cis Benchmark

## API Reference

## CIS Benchmark Sections

| Section | Topic |
|---------|-------|
| 1 | Account Policies (passwords, lockout) |
| 2 | Local Policies (audit, user rights, security options) |
| 9 | Windows Firewall |
| 17 | Advanced Audit Policy |
| 18 | Administrative Templates |
| 19 | User Configuration |

## PowerShell Commands

### Password Policy
```powershell
net accounts
# or
Get-ADDefaultDomainPasswordPolicy
```

### Audit Policy
```powershell
auditpol /get /category:*
```

### Firewall Status
```powershell
Get-NetFirewallProfile | Select-Object Name, Enabled
```

### Registry Checks
```powershell
Get-ItemProperty -Path 'HKLM:\...' -Name 'ValueName'
```

## Key Registry Settings

| Path | Value | Recommended |
|------|-------|-------------|
| `HKLM\SYSTEM\CurrentControlSet\Control\Lsa\LmCompatibilityLevel` | DWORD | 5 (NTLMv2 only) |
| `HKLM\...\Policies\System\EnableLUA` | DWORD | 1 (UAC enabled) |
| `HKLM\...\LanManServer\Parameters\SMB1` | DWORD | 0 (disabled) |
| `HKLM\...\Policies\System\ConsentPromptBehaviorAdmin` | DWORD | 2 |

## Password Policy Settings

| Setting | CIS Recommendation |
|---------|-------------------|
| Minimum length | >= 14 characters |
| Maximum age | <= 365 days |
| Minimum age | >= 1 day |
| Complexity | Enabled |
| Lockout threshold | <= 5 attempts |
| Lockout duration | >= 15 minutes |

## Advanced Audit Policy

| Subcategory | Recommended |
|-------------|-------------|
| Credential Validation | Success and Failure |
| Logon/Logoff | Success and Failure |
| Account Management | Success |
| Process Creation | Success |
| Policy Change | Success |

## GPO Export and Analysis

### Export GPO
```powershell
gpresult /H gpo-report.html
```

### Secedit Export
```cmd
secedit /export /cfg security-config.inf
```

## Automated Tools

### Microsoft Security Compliance Toolkit
```powershell
# Download from Microsoft
# Includes GPO baselines and LGPO tool
LGPO.exe /g .\GPO-Backup
```

### CIS-CAT
```bash
# CIS Configuration Assessment Tool
cis-cat.bat -b benchmark.xml -p "CIS Windows 11 Enterprise"
```

## Windows Optional Features

### Check SMBv1
```powershell
Get-WindowsOptionalFeature -Online -FeatureName SMB1Protocol
```

### Disable SMBv1
```powershell
Disable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol
```

---

## Standards and Controls

## Primary Standards

### CIS Microsoft Windows 11 Enterprise Benchmark v3.0.0
- **Publisher**: Center for Internet Security (CIS)
- **URL**: https://www.cisecurity.org/benchmark/microsoft_windows_desktop
- **Scope**: 400+ security configuration recommendations organized into 19 sections
- **Profiles**: Level 1 (Corporate), Level 2 (High Security), BitLocker (BL), Next Generation Windows Security (NG)

### CIS Microsoft Windows Server 2022 Benchmark v3.0.0
- **Publisher**: CIS
- **URL**: https://www.cisecurity.org/benchmark/microsoft_windows_server
- **Scope**: Server-specific recommendations for Member Server and Domain Controller roles
- **Profiles**: Level 1 (MS/DC), Level 2 (MS/DC)

### NIST SP 800-123 - Guide to General Server Security
- **Publisher**: NIST
- **Relevance**: Foundational server hardening guidance that CIS benchmarks operationalize
- **Key sections**: OS hardening, user account management, resource access controls

## Compliance Mappings

### PCI DSS v4.0 Mapping
| PCI DSS Requirement | CIS Benchmark Section |
|---------------------|----------------------|
| 2.2 - Develop configuration standards | CIS Benchmark entire scope |
| 5.2 - Anti-malware mechanisms | Section 18.10 (Windows Defender) |
| 8.3 - Strong authentication | Section 1.1 (Password Policy) |
| 10.2 - Audit trail implementation | Section 17 (Advanced Audit Policy) |

### NIST 800-53 Rev 5 Mapping
| NIST Control | CIS Benchmark Section |
|-------------|----------------------|
| CM-6 Configuration Settings | Entire CIS Benchmark |
| AC-2 Account Management | Section 1 (Account Policies) |
| AU-2 Audit Events | Section 17 (Advanced Audit Policy) |
| SC-7 Boundary Protection | Section 9 (Windows Firewall) |

### HIPAA Security Rule Mapping
| HIPAA Requirement | CIS Benchmark Section |
|------------------|----------------------|
| 164.312(a)(1) Access Control | Section 2.3 (Security Options) |
| 164.312(b) Audit Controls | Section 17 (Advanced Audit Policy) |
| 164.312(a)(2)(iv) Encryption | BitLocker Profile |
| 164.312(c)(1) Integrity | Section 18.9 (Windows Defender) |

## Supporting References

- **Microsoft Security Baselines**: https://learn.microsoft.com/en-us/windows/security/operating-system-security/device-management/windows-security-configuration-framework/windows-security-baselines
- **CIS Controls v8**: Maps to Implementation Group (IG) 1, 2, and 3 for prioritized implementation
- **STIGs (DoD)**: DISA Security Technical Implementation Guides provide overlapping but more restrictive benchmarks for government systems
- **ACSC Essential Eight**: Australian Cyber Security Centre hardening framework with overlap to CIS benchmark categories

---

## Workflows

## Workflow 1: Initial Baseline Deployment

```
[Select Windows Version & CIS Benchmark]
    │
    ▼
[Choose Profile Level (L1 or L2)]
    │
    ▼
[Download CIS Build Kit GPOs from CIS WorkBench]
    │
    ▼
[Import GPOs into Active Directory via GPMC]
    │
    ▼
[Link GPO to Pilot OU with 5-10 test endpoints]
    │
    ▼
[Run CIS-CAT assessment on pilot endpoints]
    │
    ├── Score >= 95% ──► [Test application compatibility for 2 weeks]
    │                         │
    │                         ├── No issues ──► [Deploy GPO to production OUs]
    │                         │
    │                         └── Issues found ──► [Document exceptions, add compensating controls]
    │                                                  │
    │                                                  ▼
    │                                              [Redeploy with exceptions]
    │
    └── Score < 95% ──► [Investigate GPO application failures]
                              │
                              ▼
                         [Fix WMI filters, security filtering, or GPO precedence]
                              │
                              ▼
                         [Re-run CIS-CAT assessment]
```

## Workflow 2: Continuous Compliance Monitoring

```
[Weekly CIS-CAT Scheduled Scan]
    │
    ▼
[Parse XML results → ingest into SIEM]
    │
    ▼
[Compare against baseline score]
    │
    ├── Score drift > 2% ──► [Generate compliance drift alert]
    │                              │
    │                              ▼
    │                         [Identify changed settings via GPResult /H]
    │                              │
    │                              ▼
    │                         [Determine if change was authorized]
    │                              │
    │                              ├── Authorized ──► [Update baseline, document exception]
    │                              │
    │                              └── Unauthorized ──► [Revert change, investigate as security incident]
    │
    └── Score stable ──► [Log compliance status, update dashboard]
```

## Workflow 3: New CIS Benchmark Version Upgrade

```
[CIS releases new benchmark version]
    │
    ▼
[Download updated benchmark and Build Kit]
    │
    ▼
[Diff new vs. current benchmark recommendations]
    │
    ▼
[Identify new/changed/removed recommendations]
    │
    ▼
[Impact assessment: Will new settings break applications?]
    │
    ├── Yes ──► [Lab test, document new exceptions]
    │
    └── No ──► [Update GPO with new Build Kit]
                    │
                    ▼
               [Deploy to pilot OU first]
                    │
                    ▼
               [Run CIS-CAT with new benchmark profile]
                    │
                    ▼
               [Production rollout after 2-week pilot]
```

## Workflow 4: Standalone Endpoint Hardening (Non-Domain)

```
[Identify standalone Windows endpoint]
    │
    ▼
[Download LGPO.exe from Microsoft SCT]
    │
    ▼
[Export CIS Build Kit GPO to local policy format]
    │
    ▼
[Apply via LGPO.exe: LGPO.exe /g C:\CIS-Policy]
    │
    ▼
[Run CIS-CAT Lite assessment]
    │
    ▼
[Document results and exceptions]
    │
    ▼
[Schedule quarterly manual reassessment]
```

---

## Working Template

## Endpoint Information

| Field | Value |
|-------|-------|
| Hostname | |
| OS Version | Windows 11 Enterprise 23H2 |
| Domain/Workgroup | |
| CIS Benchmark Version | v3.0.0 |
| Profile Applied | Level 1 / Level 2 |
| Assessment Date | |
| Assessor | |

## Pre-Hardening Checklist

- [ ] Verified current OS patch level
- [ ] Documented installed applications and services
- [ ] Created system restore point / VM snapshot
- [ ] Identified business-critical applications for compatibility testing
- [ ] Obtained CIS Build Kit GPO for target OS version
- [ ] Confirmed Active Directory OU structure for GPO deployment

## CIS-CAT Assessment Results

| Metric | Value |
|--------|-------|
| Total Rules Assessed | |
| Passed | |
| Failed | |
| Not Applicable | |
| Compliance Score | % |
| Target Score | 95% (L1) / 90% (L2) |

## Failed Controls Summary

| CIS ID | Recommendation | Severity | Remediation Plan | Exception? |
|--------|---------------|----------|-----------------|------------|
| | | | | |

## Exception Register

| CIS ID | Recommendation | Business Justification | Compensating Control | Review Date | Approved By |
|--------|---------------|----------------------|---------------------|-------------|-------------|
| | | | | | |

## Post-Hardening Validation

- [ ] Re-ran CIS-CAT assessment after GPO application
- [ ] Verified all business applications function correctly
- [ ] Confirmed remote management tools (RDP, WinRM) still accessible
- [ ] Validated endpoint joins domain and receives policies
- [ ] Tested user login and MFA functionality
- [ ] Verified antivirus/EDR agent status

## Compliance Tracking

| Scan Date | Score | Delta | New Failures | Resolved | Notes |
|-----------|-------|-------|-------------|----------|-------|
| | | | | | Initial baseline |

## Sign-Off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| System Administrator | | | |
| Security Analyst | | | |
| CISO / Security Manager | | | |
