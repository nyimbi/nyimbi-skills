# Detecting T1055 Process Injection With Sysmon

## API Reference

## MITRE ATT&CK T1055 Sub-Techniques

| Sub-technique | Method | Sysmon Event |
|---------------|--------|--------------|
| T1055.001 | DLL Injection | Event 7, 8, 10 |
| T1055.002 | PE Injection | Event 8, 10 |
| T1055.003 | Thread Execution Hijacking | Event 8 |
| T1055.004 | Asynchronous Procedure Call | Event 8, 10 |
| T1055.005 | Thread Local Storage | Event 8 |
| T1055.012 | Process Hollowing | Event 1, 10, 25 |

## Sysmon Event IDs

### Event 8 — CreateRemoteThread
| Field | Index | Description |
|-------|-------|-------------|
| SourceProcessGuid | 1 | GUID of injecting process |
| SourceProcessId | 2 | PID of injecting process |
| SourceImage | 4 | Path of injecting binary |
| TargetProcessGuid | 5 | GUID of target process |
| TargetProcessId | 6 | PID of target process |
| TargetImage | 7 | Path of target binary |
| StartAddress | 8 | Thread start address |
| StartFunction | 9 | Thread entry function |

### Event 10 — ProcessAccess
| Field | Index | Description |
|-------|-------|-------------|
| SourceProcessId | 3 | Accessing PID |
| SourceImage | 4 | Accessing binary path |
| TargetProcessId | 7 | Accessed PID |
| TargetImage | 8 | Accessed binary path |
| GrantedAccess | 10 | Access rights mask |

### Event 7 — Image Loaded
| Field | Index | Description |
|-------|-------|-------------|
| Image | 3 | Process that loaded DLL |
| ImageLoaded | 5 | DLL path |
| Signed | 6 | Signature status |
| SignatureStatus | 8 | Valid/Invalid/Unknown |

## Process Access Masks

| Mask | Right | Injection Use |
|------|-------|---------------|
| 0x0008 | PROCESS_VM_OPERATION | VirtualAllocEx |
| 0x0010 | PROCESS_VM_READ | ReadProcessMemory |
| 0x0020 | PROCESS_VM_WRITE | WriteProcessMemory |
| 0x0800 | PROCESS_SUSPEND_RESUME | Hollowing |
| 0x001F0FFF | PROCESS_ALL_ACCESS | Full control |

## Sysmon Configuration for Injection Detection
```xml
<Sysmon>
  <EventFiltering>
    <ProcessAccess onmatch="include">
      <GrantedAccess condition="is">0x1F0FFF</GrantedAccess>
      <GrantedAccess condition="is">0x001F0FFF</GrantedAccess>
    </ProcessAccess>
    <CreateRemoteThread onmatch="exclude">
      <SourceImage condition="is">C:\Windows\System32\svchost.exe</SourceImage>
    </CreateRemoteThread>
  </EventFiltering>
</Sysmon>
```

## Sigma Rule Example
```yaml
title: CreateRemoteThread into System Process
logsource:
    product: windows
    category: create_remote_thread
detection:
    selection:
        TargetImage|endswith:
            - '\svchost.exe'
            - '\explorer.exe'
            - '\lsass.exe'
    filter:
        SourceImage|startswith: 'C:\Windows\System32\'
    condition: selection and not filter
level: critical
```

---

## Standards and Controls

## MITRE ATT&CK Process Injection Sub-Techniques

| Sub-Technique | Name | API Calls | Sysmon Detection |
|--------------|------|-----------|-----------------|
| T1055.001 | Dynamic-link Library Injection | VirtualAllocEx, WriteProcessMemory, CreateRemoteThread | Event 8, 10 |
| T1055.002 | Portable Executable Injection | VirtualAllocEx, WriteProcessMemory, SetThreadContext | Event 10 |
| T1055.003 | Thread Execution Hijacking | SuspendThread, SetThreadContext, ResumeThread | Event 10 |
| T1055.004 | Asynchronous Procedure Call | OpenThread, QueueUserAPC | Event 10 |
| T1055.005 | Thread Local Storage | TLS callback manipulation | Event 10 |
| T1055.012 | Process Hollowing | CreateProcess (SUSPENDED), NtUnmapViewOfSection, WriteProcessMemory | Event 25, 10 |
| T1055.013 | Process Doppelganging | NtCreateTransaction, NtCreateSection, NtRollbackTransaction | Event 25 |
| T1055.015 | ListPlanting | SendMessage to set list item text | Limited Sysmon coverage |

## Critical Sysmon Events for Injection Detection

| Event ID | Name | Detection Value |
|----------|------|----------------|
| 1 | Process Create | Baseline the originating process |
| 7 | Image Loaded | Detect DLL injection from unusual paths |
| 8 | CreateRemoteThread | Primary injection indicator |
| 10 | ProcessAccess | Cross-process handle acquisition |
| 25 | ProcessTampering | Process hollowing detection (Sysmon 13+) |

## ProcessAccess Granted Access Masks

| Access Mask | Permissions | Risk |
|-------------|------------|------|
| 0x1FFFFF | PROCESS_ALL_ACCESS | Critical - full process control |
| 0x1F3FFF | Nearly all access rights | Critical |
| 0x0040 | PROCESS_VM_READ | Medium - credential dumping |
| 0x0020 | PROCESS_VM_WRITE | High - memory modification |
| 0x0008 | PROCESS_VM_OPERATION | High - memory allocation |
| 0x0002 | PROCESS_CREATE_THREAD | High - thread creation |
| 0x143A | Combination used by Mimikatz | Critical |

## Common Injection Targets

| Process | Why Targeted |
|---------|-------------|
| svchost.exe | Many instances, network access, elevated privileges |
| explorer.exe | User context, always running, network access |
| lsass.exe | Credential access (T1003 overlap) |
| winlogon.exe | SYSTEM privileges, always running |
| spoolsv.exe | SYSTEM privileges, rarely monitored |
| dllhost.exe | COM surrogate, frequently overlooked |
| RuntimeBroker.exe | Common in modern Windows, rarely scrutinized |

## Recommended Sysmon Configuration for Injection Detection

```xml
<Sysmon schemaversion="4.90">
  <EventFiltering>
    <RuleGroup name="ProcessInjection" groupRelation="or">
      <CreateRemoteThread onmatch="exclude">
        <SourceImage condition="is">C:\Windows\System32\csrss.exe</SourceImage>
      </CreateRemoteThread>
      <ProcessAccess onmatch="include">
        <GrantedAccess condition="is">0x1FFFFF</GrantedAccess>
        <GrantedAccess condition="is">0x1F3FFF</GrantedAccess>
        <GrantedAccess condition="is">0x143A</GrantedAccess>
      </ProcessAccess>
      <ProcessTampering onmatch="include">
        <Type condition="is">Image is replaced</Type>
      </ProcessTampering>
    </RuleGroup>
  </EventFiltering>
</Sysmon>
```

---

## Workflows

## Phase 1: CreateRemoteThread Detection (Sysmon Event 8)

### Step 1.1 - Identify All Remote Thread Creation
```spl
index=sysmon EventCode=8
| where SourceImage!=TargetImage
| stats count by SourceImage TargetImage Computer
| sort -count
```

### Step 1.2 - Filter to High-Value Target Processes
```spl
index=sysmon EventCode=8
| where match(TargetImage, "(?i)(svchost|explorer|lsass|winlogon|spoolsv|dllhost|RuntimeBroker)\.exe$")
| where NOT match(SourceImage, "(?i)(csrss|lsass|services|svchost|MsMpEng|vmtoolsd)\.exe$")
| stats count values(Computer) as hosts by SourceImage TargetImage
| sort -count
```

## Phase 2: ProcessAccess Analysis (Sysmon Event 10)

### Step 2.1 - High-Privilege Cross-Process Access
```spl
index=sysmon EventCode=10
| where GrantedAccess IN ("0x1FFFFF", "0x1F3FFF", "0x143A", "0x1F0FFF")
| where NOT match(SourceImage, "(?i)(MsMpEng|csrss|lsass|services|svchost|taskmgr|procexp)\.exe$")
| where match(TargetImage, "(?i)(lsass|svchost|explorer|winlogon)\.exe$")
| table _time Computer SourceImage TargetImage GrantedAccess CallTrace
```

### Step 2.2 - LSASS Access for Credential Theft
```spl
index=sysmon EventCode=10
| where match(TargetImage, "(?i)lsass\.exe$")
| where match(GrantedAccess, "(0x1FFFFF|0x1F3FFF|0x0040|0x143A)")
| where NOT match(SourceImage, "(?i)(csrss|lsass|svchost|MsMpEng|WmiPrvSE)\.exe$")
| table _time Computer SourceImage GrantedAccess CallTrace
```

## Phase 3: DLL Injection Detection (Sysmon Event 7)

### Step 3.1 - DLLs Loaded from User-Writable Paths
```spl
index=sysmon EventCode=7
| where match(ImageLoaded, "(?i)\\(temp|appdata|downloads|users\\[^\\]+\\desktop)\\")
| where match(Image, "(?i)(svchost|explorer|winlogon|services)\.exe$")
| table _time Computer Image ImageLoaded Hashes Signed
```

### Step 3.2 - Unsigned DLLs in System Processes
```spl
index=sysmon EventCode=7
| where Signed="false"
| where match(Image, "(?i)\\(svchost|services|lsass|explorer)\.exe$")
| table _time Computer Image ImageLoaded Hashes SignatureStatus
```

## Phase 4: Process Hollowing Detection (Sysmon Event 25)

### Step 4.1 - ProcessTampering Events
```spl
index=sysmon EventCode=25
| table _time Computer Image Type RuleName User
```

## Phase 5: Correlation and Investigation

### Step 5.1 - Build Full Attack Chain
```spl
index=sysmon (EventCode=1 OR EventCode=8 OR EventCode=10 OR EventCode=25)
| where match(SourceImage, "[suspected_injector]") OR match(Image, "[suspected_injector]")
| sort _time
| table _time EventCode Image SourceImage TargetImage CommandLine GrantedAccess
```

### Step 5.2 - Memory Analysis
For confirmed injection, capture process memory using:
- PE-sieve for automated scan of hollow/injected processes
- Moneta for memory region anomaly detection
- Volatility malfind plugin for offline memory forensics

## Phase 6: Response

1. Isolate affected endpoint via EDR
2. Capture memory dump before cleanup
3. Identify and remove injecting malware
4. Check for persistence mechanisms deployed by injected code
5. Sweep environment for same injection technique indicators

---

## Working Template

## Hunt Metadata
| Field | Value |
|-------|-------|
| Hunt ID | TH-INJECT-YYYY-MM-DD-NNN |
| Analyst | |
| Date | |
| Status | [ ] In Progress / [ ] Complete |

## Hypothesis
> Adversaries are injecting malicious code into legitimate system processes to evade detection and execute with elevated privileges.

## Injection Findings

| # | Time | Host | Source Process | Target Process | Event Type | Access Mask | Technique | Severity |
|---|------|------|---------------|----------------|------------|-------------|-----------|----------|
| 1 | | | | | | | | |

## Process Tampering Findings

| # | Time | Host | Image | Tampering Type | Severity |
|---|------|------|-------|----------------|----------|
| 1 | | | | | |

## Recommendations
1. **Isolate**: [Affected endpoints]
2. **Analyze**: [Memory dumps of injected processes]
3. **Detect**: [New Sysmon rules for observed patterns]
4. **Harden**: [Credential Guard, PPL for LSASS]
