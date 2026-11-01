# Detecting T1003 Credential Dumping With Edr

## API Reference

## MITRE ATT&CK T1003 Sub-Techniques

| Sub-technique | Name | Detection |
|---------------|------|-----------|
| T1003.001 | LSASS Memory | Sysmon Event 10 |
| T1003.002 | SAM Registry | Event 4688 |
| T1003.003 | NTDS.dit | Event 4688, VSS events |
| T1003.004 | LSA Secrets | Registry access |
| T1003.005 | Cached Domain Creds | Registry access |
| T1003.006 | DCSync | Event 4662 |

## Sysmon Events for Credential Dumping

### Event ID 10 — ProcessAccess
| Field | Description |
|-------|-------------|
| SourceProcessId | PID of accessing process |
| SourceImage | Path of accessing process |
| TargetProcessId | PID of target (lsass.exe) |
| TargetImage | Path of target process |
| GrantedAccess | Access mask |

### Suspicious Access Masks
| Mask | Meaning |
|------|---------|
| 0x1010 | QUERY_LIMITED + VM_READ |
| 0x1FFFFF | PROCESS_ALL_ACCESS |
| 0x1410 | QUERY_INFO + VM_READ |
| 0x0040 | DUP_HANDLE |

### Event ID 1 — ProcessCreate
```xml
<Data Name="Image">C:\tools\mimikatz.exe</Data>
<Data Name="CommandLine">mimikatz.exe "sekurlsa::logonpasswords"</Data>
```

## Windows Security Event Log

### Event 4688 — Process Creation
```powershell
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4688}
```

### Event 4662 — Object Access (DCSync detection)
```
Properties: {1131f6aa-9c07-11d1-f79f-00c04fc2dcd2}  # DS-Replication-Get-Changes
Properties: {1131f6ad-9c07-11d1-f79f-00c04fc2dcd2}  # DS-Replication-Get-Changes-All
```

## CrowdStrike Falcon — Detection Query

### Search for credential access alerts
```http
GET https://api.crowdstrike.com/detects/queries/detects/v1
    ?filter=behaviors.tactic:'Credential Access'
Authorization: Bearer {token}
```

## Microsoft Defender ATP — Advanced Hunting

### LSASS Access KQL
```kql
DeviceProcessEvents
| where FileName == "lsass.exe"
| join kind=inner (
    DeviceProcessEvents
    | where InitiatingProcessFileName !in ("svchost.exe", "csrss.exe")
) on DeviceId
| project Timestamp, DeviceName, InitiatingProcessFileName
```

## Sigma Rules

### LSASS Memory Access
```yaml
title: LSASS Memory Access by Non-System Process
logsource:
    product: windows
    category: process_access
detection:
    selection:
        TargetImage|endswith: '\lsass.exe'
        GrantedAccess|contains:
            - '0x1010'
            - '0x1FFFFF'
    filter:
        SourceImage|endswith:
            - '\svchost.exe'
            - '\csrss.exe'
    condition: selection and not filter
level: critical
```

---

## Standards and Controls

## MITRE ATT&CK Credential Dumping Sub-Techniques

| Sub-Technique | Target | Common Tools | Primary Detection |
|--------------|--------|-------------|-------------------|
| T1003.001 | LSASS Memory | Mimikatz, ProcDump, comsvcs.dll | Sysmon Event 10, EDR LSASS alerts |
| T1003.002 | SAM Database | reg save, Mimikatz | Registry access auditing |
| T1003.003 | NTDS.dit | ntdsutil, vssadmin, secretsdump | VSS creation + file access |
| T1003.004 | LSA Secrets | Mimikatz, reg save | Registry access to SECURITY hive |
| T1003.005 | Cached Domain Creds | Mimikatz, cachedump | SECURITY hive access |
| T1003.006 | DCSync | Mimikatz, Impacket | Event 4662 replication GUIDs |

## LSASS Access Masks for Credential Dumping

| Access Mask | Meaning | Risk Level |
|-------------|---------|-----------|
| 0x1FFFFF | PROCESS_ALL_ACCESS | Critical |
| 0x1F3FFF | Near-full access | Critical |
| 0x143A | Mimikatz typical access | Critical |
| 0x1F0FFF | Full minus synchronize | Critical |
| 0x0040 | PROCESS_VM_READ | High |
| 0x1010 | PROCESS_VM_READ + QUERY_INFO | High |

## Protection Controls

| Control | Description | Effectiveness |
|---------|-------------|---------------|
| Credential Guard | Virtualizes LSASS secrets | High -- prevents plaintext extraction |
| RunAsPPL | Protected Process Light for LSASS | Medium -- blocks unsigned callers |
| ASR Rules | Attack Surface Reduction for LSASS | Medium -- blocks common tools |
| LSASS SACL | Audit logging for LSASS access | Detection only |
| Windows Defender Credential Guard | Hardware-backed isolation | High |

## Known Credential Dumping Tools

| Tool | Method | Detection Signature |
|------|--------|-------------------|
| Mimikatz | Direct LSASS read via API | sekurlsa::, lsadump:: |
| ProcDump | LSASS dump via MiniDumpWriteDump | procdump -ma lsass |
| comsvcs.dll | Built-in DLL MiniDump function | comsvcs.dll,MiniDump |
| Task Manager | GUI-based LSASS dump | taskmgr.exe accessing lsass |
| ntdsutil | IFM creation for NTDS | "ac i ntds" "ifm" |
| secretsdump.py | Remote NTDS extraction | Impacket network activity |
| LaZagne | Multi-source credential harvesting | lazagne.exe all |

---

## Workflows

## Phase 1: LSASS Memory Access Detection

### Step 1.1 - Sysmon Event 10 Analysis
```spl
index=sysmon EventCode=10
| where match(TargetImage, "(?i)lsass\.exe$")
| where NOT match(SourceImage, "(?i)(csrss|lsass|svchost|MsMpEng|WmiPrvSE|SecurityHealthService|smartscreen)\.exe$")
| stats count values(GrantedAccess) as access_masks by SourceImage Computer
| sort -count
```

### Step 1.2 - EDR LSASS Alerts
```kql
AlertInfo
| where Title has_any ("LSASS", "credential", "Mimikatz")
| join AlertEvidence on AlertId
| project Timestamp, Title, DeviceName, FileName, ProcessCommandLine
```

## Phase 2: Credential Tool Detection

### Step 2.1 - Known Tool Command Lines
```spl
index=sysmon EventCode=1
| where match(CommandLine, "(?i)(sekurlsa|lsadump|kerberos::list|crypto::certificates|privilege::debug)")
    OR match(OriginalFileName, "(?i)mimikatz")
    OR (match(CommandLine, "(?i)procdump") AND match(CommandLine, "(?i)lsass"))
    OR match(CommandLine, "(?i)comsvcs.*MiniDump")
| table _time Computer User Image CommandLine Hashes
```

### Step 2.2 - NTDS.dit Extraction
```spl
index=sysmon EventCode=1
| where match(CommandLine, "(?i)(vssadmin.*create\s+shadow|wmic\s+shadowcopy|ntdsutil.*ifm|esentutl.*ntds)")
| table _time Computer User CommandLine ParentImage
```

### Step 2.3 - Registry Hive Export
```spl
index=sysmon EventCode=1
| where match(CommandLine, "(?i)reg\s+(save|export)\s+hklm\\\\(sam|security|system)")
| table _time Computer User CommandLine
```

## Phase 3: Post-Dump Lateral Movement

### Step 3.1 - Pass-the-Hash Detection
```spl
index=wineventlog EventCode=4624 LogonType=9
| where AuthenticationPackageName="Negotiate"
| table _time TargetUserName IpAddress WorkstationName LogonProcessName
```

### Step 3.2 - Suspicious Remote Logons After Dump
```spl
index=wineventlog EventCode=4624 LogonType=3
| where _time > [credential_dump_timestamp]
| stats count by TargetUserName IpAddress WorkstationName
| sort -count
```

## Phase 4: Response Actions
1. Isolate affected endpoints
2. Reset ALL credentials that were potentially on compromised systems
3. Rotate KRBTGT if domain-level compromise suspected
4. Enable Credential Guard and RunAsPPL
5. Deploy ASR rules for LSASS protection

---

## Working Template

## Hunt Metadata
| Field | Value |
|-------|-------|
| Hunt ID | TH-CRED-YYYY-MM-DD-NNN |
| Analyst | |
| Date | |
| Status | [ ] In Progress / [ ] Complete |

## Hypothesis
> An adversary with elevated privileges is dumping credentials from LSASS memory, SAM database, or NTDS.dit to enable lateral movement and privilege escalation.

## LSASS Access Findings

| # | Time | Host | Source Process | Access Mask | User | Severity |
|---|------|------|---------------|-------------|------|----------|
| 1 | | | | | | |

## Credential Tool Detections

| # | Time | Host | Tool | Command Line | Technique | Severity |
|---|------|------|------|-------------|-----------|----------|
| 1 | | | | | | |

## Impact Assessment
- [ ] LSASS memory potentially dumped
- [ ] Local SAM hashes at risk
- [ ] Domain NTDS.dit compromised
- [ ] Service account credentials exposed
- [ ] Kerberos tickets extracted

## Recommendations
1. **Reset**: [All credentials on affected systems]
2. **Enable**: [Credential Guard, RunAsPPL, ASR rules]
3. **Investigate**: [Lateral movement from compromised credentials]
4. **Rotate**: [KRBTGT if domain-level compromise]
