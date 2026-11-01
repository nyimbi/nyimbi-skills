# Detecting Process Hollowing Technique

## API Reference

## Process Hollowing API Sequence

| Step | API Call | Purpose |
|------|----------|---------|
| 1 | CreateProcess(SUSPENDED) | Create target suspended |
| 2 | NtUnmapViewOfSection | Unmap legitimate code |
| 3 | VirtualAllocEx | Allocate for payload |
| 4 | WriteProcessMemory | Write malicious code |
| 5 | SetThreadContext | Redirect execution |
| 6 | ResumeThread | Execute payload |

## Commonly Hollowed Processes

| Process | Reason |
|---------|--------|
| svchost.exe | Trusted, always running |
| explorer.exe | UI process |
| notepad.exe | Simple, rarely monitored |
| dllhost.exe | COM surrogate |

## Sysmon Detection Events

| Event ID | Detection |
|----------|-----------|
| 1 | Suspicious parent-child |
| 8 | CreateRemoteThread into hollowed target |
| 10 | Process Access with PROCESS_ALL_ACCESS |

## Splunk SPL

```spl
index=sysmon EventCode=10
| where TargetImage IN ("*\svchost.exe","*\explorer.exe")
| where GrantedAccess IN ("0x1FFFFF","0x1F3FFF")
| table _time SourceImage TargetImage GrantedAccess Computer
```

## CLI Usage

```bash
python agent.py --sysmon-log Sysmon.evtx
```

---

## Standards and Controls

## MITRE ATT&CK Mappings

### T1055.012 - Process Injection: Process Hollowing
- **Tactic**: Defense Evasion (TA0005), Privilege Escalation (TA0004)
- **Platforms**: Windows
- **Data Sources**: Process modification, OS API execution, Process access

### Related Process Injection Sub-Techniques
| Sub-Technique | Name |
|---------------|------|
| T1055.001 | Dynamic-link Library Injection |
| T1055.002 | Portable Executable Injection |
| T1055.003 | Thread Execution Hijacking |
| T1055.004 | Asynchronous Procedure Call |
| T1055.005 | Thread Local Storage |
| T1055.008 | Ptrace System Calls |
| T1055.009 | Proc Memory |
| T1055.011 | Extra Window Memory Injection |
| T1055.012 | Process Hollowing |
| T1055.013 | Process Doppelganging |
| T1055.014 | VDSO Hijacking |
| T1055.015 | ListPlanting |

## Process Hollowing API Call Sequence

```
1. CreateProcess(CREATE_SUSPENDED)     -> Create target in suspended state
2. NtQueryInformationProcess           -> Get PEB address
3. ReadProcessMemory(PEB)              -> Read image base from PEB
4. NtUnmapViewOfSection(ImageBase)     -> Unmap original image
5. VirtualAllocEx(ImageBase, size)     -> Allocate memory at same base
6. WriteProcessMemory(PE headers)      -> Write malicious PE headers
7. WriteProcessMemory(PE sections)     -> Write malicious code sections
8. SetThreadContext(EntryPoint)        -> Set new entry point
9. ResumeThread                        -> Resume execution with malicious code
```

## Detection Data Sources

| Source | Event/Indicator | Description |
|--------|----------------|-------------|
| Sysmon Event 1 | Process Create | Process created with suspicious parent |
| Sysmon Event 8 | CreateRemoteThread | Remote thread in target process |
| Sysmon Event 25 | ProcessTampering | Image file replaced (Sysmon v13+) |
| ETW | Microsoft-Windows-Kernel-Process | Kernel-level process events |
| MDE | ProcessTampering | AlertType for hollowing detection |
| Memory | Malfind | Volatility plugin for injected code |
| Memory | VAD analysis | Virtual Address Descriptor anomalies |

## Volatility Forensic Commands

```bash
# Detect injected/hollowed processes
volatility -f memory.dmp --profile=Win10x64 malfind

# Compare process memory to disk image
volatility -f memory.dmp --profile=Win10x64 procdump -p <PID> -D ./dump/

# Analyze process memory sections
volatility -f memory.dmp --profile=Win10x64 vadinfo -p <PID>

# Check process image path vs loaded modules
volatility -f memory.dmp --profile=Win10x64 dlllist -p <PID>
```

## Known Malware Using Process Hollowing

| Malware | Target Process | Notes |
|---------|---------------|-------|
| Emotet | Multiple | Uses hollowing for persistence |
| TrickBot | svchost.exe | Hollows svchost for C2 |
| Dridex | explorer.exe | Financial trojan |
| FormBook | Various | Infostealer using hollowing |
| AgentTesla | RegAsm.exe, MSBuild.exe | Targets .NET processes |
| Remcos | Common utilities | RAT using hollowing |
| NanoCore | Various | RAT with hollowing capability |
| AsyncRAT | Various .NET processes | Open-source RAT |

---

## Workflows

## Phase 1: Sysmon-Based Detection

### Step 1.1 - Process Tampering Events (Sysmon v13+)
```spl
index=sysmon EventCode=25
| table _time Computer User Image Type
| sort -_time
```

### Step 1.2 - Suspicious Process Creation Patterns
```spl
index=sysmon EventCode=1
| where match(Image, "(?i)(svchost|explorer|rundll32|dllhost|conhost|taskhost)\.exe$")
| where NOT match(ParentImage, "(?i)(services\.exe|explorer\.exe|svchost\.exe|userinit\.exe|winlogon\.exe)")
| table _time Computer User Image ParentImage CommandLine
```

### Step 1.3 - KQL for MDE ProcessTampering
```kql
DeviceEvents
| where ActionType == "ProcessTampering"
| project Timestamp, DeviceName, FileName, ProcessCommandLine,
    InitiatingProcessFileName, InitiatingProcessCommandLine, AdditionalFields
| order by Timestamp desc
```

## Phase 2: Parent-Child Process Validation

### Step 2.1 - Invalid Parent-Child Relationships
Known legitimate parent-child pairs:
- services.exe -> svchost.exe
- explorer.exe -> user applications
- winlogon.exe -> userinit.exe
- svchost.exe -> specific service children

```spl
index=sysmon EventCode=1
| eval expected_parent=case(
    match(Image,"(?i)svchost\.exe$"), "services.exe",
    match(Image,"(?i)taskhost\.exe$"), "svchost.exe",
    match(Image,"(?i)userinit\.exe$"), "winlogon.exe",
    match(Image,"(?i)smss\.exe$"), "System",
    1=1, "any"
)
| eval parent_name=mvindex(split(ParentImage,"\\"),-1)
| where expected_parent!="any" AND NOT match(parent_name, expected_parent)
| table _time Computer Image ParentImage expected_parent parent_name CommandLine
```

## Phase 3: Memory Analysis

### Step 3.1 - pe-sieve Scanning
```powershell
# Scan all processes for hollowing
Get-Process | ForEach-Object {
    $pid = $_.Id
    & pe-sieve64.exe /pid $pid /shellc /dmode 1 /json
}
```

### Step 3.2 - Hollows Hunter Full Scan
```powershell
# Run Hollows Hunter for automated detection
hollows_hunter64.exe /loop /json /dir C:\hunt_output
```

### Step 3.3 - Volatility Malfind
```bash
# Detect injected/modified process memory
python vol.py -f memory.raw windows.malfind

# Dump suspicious processes
python vol.py -f memory.raw windows.pslist --dump
```

## Phase 4: Behavioral Analysis

### Step 4.1 - Process Behavior Mismatches
Look for processes whose network/file behavior contradicts their identity:
```spl
index=sysmon EventCode=3
| where match(Image, "(?i)(svchost|dllhost|taskhost|conhost)\.exe$")
| where NOT match(DestinationIp, "^(10\.|172\.(1[6-9]|2[0-9]|3[01])\.|192\.168\.)")
| where DestinationPort NOT IN (53, 80, 443, 123)
| stats count by Image DestinationIp DestinationPort Computer
```

### Step 4.2 - Hollowed Process C2 Indicators
```spl
index=sysmon EventCode=3
| where match(Image, "(?i)(svchost|explorer|rundll32)\.exe$")
| bin _time span=1s
| streamstats current=f last(_time) as prev by Image Computer DestinationIp
| eval interval=_time-prev
| stats count avg(interval) as avg_interval stdev(interval) as sd by Image Computer DestinationIp
| eval cv=sd/avg_interval
| where cv < 0.3 AND count > 20
```

## Phase 5: API Call Monitoring

### Step 5.1 - Critical API Sequences
Monitor for this specific API call chain:
1. `CreateProcessW` / `CreateProcessA` with `CREATE_SUSPENDED` (0x00000004)
2. `NtUnmapViewOfSection` / `ZwUnmapViewOfSection`
3. `VirtualAllocEx` with `PAGE_EXECUTE_READWRITE`
4. `WriteProcessMemory`
5. `SetThreadContext` / `NtSetContextThread`
6. `ResumeThread` / `NtResumeThread`

### Step 5.2 - ETW Process Hollowing Detection
```powershell
# Monitor for suspicious API patterns via ETW
# Requires elevated privileges
$session = New-EtwTraceSession -Name "ProcessHollowHunt"
Add-EtwTraceProvider -SessionName "ProcessHollowHunt" `
    -Guid "{22FB2CD6-0E7B-422B-A0C7-2FAD1FD0E716}" `
    -Level 5
```

---

## Working Template

## Hunt Metadata
| Field | Value |
|-------|-------|
| Hunt ID | TH-HOLLOW-YYYY-MM-DD-NNN |
| Analyst | |
| Date | |
| Status | [ ] In Progress / [ ] Complete |

## Hypothesis
> [e.g., "Adversaries have used process hollowing to inject malicious code into svchost.exe instances to evade detection."]

## Findings

| # | Host | Process | Parent | Expected Parent | Network Activity | Risk | Verdict |
|---|------|---------|--------|----------------|-----------------|------|---------|
| 1 | | | | | | | |

## Memory Analysis Results
| Process (PID) | Image Mismatch | Injected Code | VAD Anomaly | Verdict |
|--------------|----------------|---------------|-------------|---------|
| | | | | |

## Recommendations
1. **Memory Dump**: [Collect memory from affected hosts]
2. **Containment**: [Isolate compromised endpoints]
3. **Detection**: [Deploy Sysmon v13+ with Event ID 25]
4. **Prevention**: [Enable Attack Surface Reduction rules]
