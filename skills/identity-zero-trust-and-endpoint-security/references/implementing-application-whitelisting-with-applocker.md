# Implementing Application Whitelisting With Applocker

## API Reference

## PowerShell AppLocker Management

```powershell
# Export current policy
Get-AppLockerPolicy -Effective -Xml | Out-File applocker_policy.xml

# Import policy from XML
Set-AppLockerPolicy -XmlPolicy applocker_policy.xml

# Test if file is allowed
Test-AppLockerPolicy -XmlPolicy policy.xml -Path "C:\app.exe" -User Everyone

# Get AppLocker event logs
Get-WinEvent -LogName "Microsoft-Windows-AppLocker/EXE and DLL"
```

## AppLocker Event IDs

| Event ID | Type | Meaning |
|----------|------|---------|
| 8002 | EXE/DLL | Allowed |
| 8003 | EXE/DLL | Blocked |
| 8004 | EXE/DLL | Would block (audit) |
| 8005 | Script | Allowed |
| 8006 | Script | Blocked |
| 8007 | Script | Would block (audit) |

## Rule Collections

| Collection | File Types |
|------------|------------|
| Executable | .exe, .com |
| Windows Installer | .msi, .msp, .mst |
| Script | .ps1, .bat, .cmd, .vbs, .js |
| DLL | .dll, .ocx |
| Packaged App | AppX/MSIX |

## GPO Configuration Path

```
Computer Configuration > Policies > Windows Settings >
  Security Settings > Application Control Policies > AppLocker
```

## Default Rule Paths

```
%PROGRAMFILES%\*     - Allow Everyone
%WINDIR%\*           - Allow Everyone
*                    - Allow BUILTIN\Administrators
```

### References

- AppLocker: https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/applocker/applocker-overview
- AppLocker PowerShell: https://learn.microsoft.com/en-us/powershell/module/applocker/

---

## Standards and Controls

## Primary Standards

### NIST SP 800-167 - Guide to Application Whitelisting
- **Publisher**: NIST
- **URL**: https://csrc.nist.gov/publications/detail/sp/800-167/final
- **Scope**: Comprehensive guidance on planning, implementing, and maintaining application whitelisting
- **Key sections**: Technology overview, planning process, policy creation, maintenance operations

### ACSC Essential Eight - Application Control
- **Publisher**: Australian Cyber Security Centre
- **URL**: https://www.cyber.gov.au/resources-business-and-government/essential-cyber-security/essential-eight
- **Scope**: Application control is Mitigation Strategy #1 in the Essential Eight
- **Maturity levels**: L1 (block executables in user profiles), L2 (block from all user-writable paths), L3 (Microsoft recommended block rules + WDAC)

### CIS Control 2 - Software Inventory and Control
- **Publisher**: Center for Internet Security
- **Relevance**: CIS Controls v8 Control 2 requires software allowlisting for authorized applications

## Compliance Mappings

| Framework | Requirement | AppLocker Coverage |
|-----------|------------|-------------------|
| PCI DSS 4.0 | 6.4.3 - Restrict active content | AppLocker script rules block unauthorized scripts |
| NIST 800-53 | CM-7 - Least Functionality | AppLocker enforces minimum required software |
| NIST 800-53 | CM-11 - User-Installed Software | AppLocker prevents unauthorized software installation |
| NIST 800-171 | 3.4.8 - Application whitelisting | Direct requirement for application control |
| ISO 27001 | A.12.5.1 - Installation of software on operational systems | AppLocker restricts installation capability |
| HIPAA | 164.312(a)(1) - Access Control | Restricts executable access to authorized applications |

## Microsoft Documentation

- **AppLocker Overview**: https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/applocker/applocker-overview
- **AppLocker Policies Design Guide**: https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/applocker/applocker-policies-design-guide
- **WDAC and AppLocker Feature Availability**: Comparison of capabilities between AppLocker and WDAC
- **Microsoft Recommended Block Rules**: https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/design/applications-that-can-bypass-appcontrol

## Supporting References

- **LOLBAS Project**: https://lolbas-project.github.io/ - Living Off The Land Binaries reference for deny rule creation
- **AaronLocker (GitHub)**: Open-source toolkit for generating robust AppLocker policies
- **UltimateAppLockerByPassList**: Security research on AppLocker bypass techniques for defense awareness

---

## Workflows

## Workflow 1: Initial AppLocker Deployment

```
[Application Inventory]
    │
    ├── Scan reference endpoints for installed applications
    ├── Catalog all approved software by publisher/path/hash
    ├── Identify admin tools vs. standard user applications
    │
    ▼
[Policy Design]
    │
    ├── Create default allow rules (Program Files, Windows)
    ├── Create publisher rules for third-party vendors
    ├── Create deny rules for LOLBins (standard users only)
    ├── Create script control rules
    │
    ▼
[Audit Mode Deployment]
    │
    ├── Deploy via GPO to pilot OU (Audit Only)
    ├── Enable Application Identity service
    ├── Monitor for 2-4 weeks
    │
    ▼
[Audit Log Analysis]
    │
    ├── Export blocked events (8003, 8006)
    ├── Identify legitimate applications being blocked
    │
    ├── Blocked app is legitimate ──► [Create allow rule]
    │                                       │
    │                                       ▼
    │                                  [Re-audit 1 week]
    │
    └── All blocked apps are unauthorized ──► [Proceed to enforcement]
                                                    │
                                                    ▼
                                               [Switch to Enforce mode (phased)]
                                                    │
                                                    ├── Week 1: EXE rules
                                                    ├── Week 2: Script rules
                                                    ├── Week 3: MSI rules
                                                    └── Week 4: DLL rules (optional)
```

## Workflow 2: New Application Approval

```
[User requests new application]
    │
    ▼
[Security review of application]
    │
    ├── Is it signed by trusted publisher? ──► [Create publisher rule]
    │
    ├── Unsigned but necessary? ──► [Create hash rule + document exception]
    │
    └── Fails security review ──► [Deny request, document reason]
    │
    ▼
[Add rule to AppLocker GPO]
    │
    ▼
[Deploy to pilot OU, verify no conflicts]
    │
    ▼
[Deploy to production OU]
    │
    ▼
[Update application inventory]
```

## Workflow 3: AppLocker Bypass Incident Response

```
[Detection: Unauthorized execution despite AppLocker]
    │
    ▼
[Identify bypass technique]
    │
    ├── LOLBin not blocked ──► [Add deny rule for specific binary]
    │
    ├── Execution from allowed path ──► [Restrict path rule scope]
    │
    ├── Admin user bypass ──► [Evaluate WDAC migration for admin enforcement]
    │
    └── DLL side-loading ──► [Enable DLL rules or deploy WDAC]
    │
    ▼
[Update AppLocker policy with fix]
    │
    ▼
[Verify fix in audit mode on test endpoint]
    │
    ▼
[Deploy fix to production]
    │
    ▼
[Update threat model and rule documentation]
```

## Workflow 4: AppLocker to WDAC Migration

```
[Decision: Migrate from AppLocker to WDAC]
    │
    ▼
[Audit current AppLocker policy]
    │
    ├── Export AppLocker rules as XML
    ├── Identify rules that need WDAC equivalents
    │
    ▼
[Create WDAC policy using WDAC Wizard]
    │
    ├── Convert publisher rules to WDAC signer rules
    ├── Convert path rules to WDAC filepath rules
    ├── Add Microsoft recommended block rules
    │
    ▼
[Deploy WDAC in Audit mode alongside AppLocker]
    │
    ▼
[Monitor WDAC audit events for 4 weeks]
    │
    ▼
[Resolve WDAC audit findings]
    │
    ▼
[Switch WDAC to Enforce mode]
    │
    ▼
[Disable AppLocker policy]
```

---

## Working Template

## Policy Information

| Field | Value |
|-------|-------|
| Policy Name | |
| Target OS | Windows 10/11 Enterprise |
| Profile | Workstation / Server / Kiosk |
| Enforcement Mode | Audit Only / Enforce |
| GPO Name | |
| Target OU | |
| Last Updated | |

## Approved Application Inventory

| Application | Publisher | Version | Rule Type | Justification |
|------------|----------|---------|-----------|---------------|
| Microsoft Office | Microsoft Corporation | 365 | Publisher | Business productivity |
| Google Chrome | Google LLC | * | Publisher | Approved browser |
| Adobe Acrobat | Adobe Inc. | * | Publisher | PDF processing |
| | | | | |

## Rule Collection Configuration

### Executable Rules (EXE, COM)

| Rule Name | Type | Action | Scope | Conditions |
|-----------|------|--------|-------|------------|
| Default - Windows | Path | Allow | Everyone | %WINDIR%\* |
| Default - Program Files | Path | Allow | Everyone | %PROGRAMFILES%\* |
| Deny - LOLBins | Path | Deny | Standard Users | mshta.exe, wscript.exe, etc. |
| | | | | |

### Script Rules (PS1, BAT, CMD, VBS, JS)

| Rule Name | Type | Action | Scope | Conditions |
|-----------|------|--------|-------|------------|
| Default - Windows scripts | Path | Allow | Everyone | %WINDIR%\* |
| Default - Program Files scripts | Path | Allow | Everyone | %PROGRAMFILES%\* |
| Deny - User profile scripts | Path | Deny | Standard Users | %USERPROFILE%\* |
| | | | | |

### Windows Installer Rules (MSI, MSP, MST)

| Rule Name | Type | Action | Scope | Conditions |
|-----------|------|--------|-------|------------|
| Default - Signed MSI | Publisher | Allow | Everyone | All signed installers |
| | | | | |

## LOLBin Deny List

| Binary | Path | ATT&CK Technique | Risk |
|--------|------|------------------|------|
| mshta.exe | %SYSTEM32% | T1218.005 | HTA execution for code delivery |
| wscript.exe | %SYSTEM32% | T1059.005 | VBScript execution |
| cscript.exe | %SYSTEM32% | T1059.005 | Command-line scripting |
| regsvr32.exe | %SYSTEM32% | T1218.010 | COM scriptlet execution |
| certutil.exe | %SYSTEM32% | T1140 | File download and decode |
| msbuild.exe | .NET Framework | T1127.001 | Inline task execution |

## Audit Results Tracking

| Audit Period | Blocked Events | Legitimate Blocks | Rules Added | Remaining Issues |
|-------------|---------------|-------------------|-------------|-----------------|
| | | | | |

## Exception Register

| Application | Reason for Exception | Compensating Control | Approved By | Review Date |
|------------|---------------------|---------------------|-------------|-------------|
| | | | | |

## Sign-Off

| Role | Name | Date |
|------|------|------|
| Security Engineer | | |
| IT Operations Lead | | |
| Change Manager | | |
