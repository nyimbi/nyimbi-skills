# Hunting For Persistence Mechanisms In Windows

## API Reference

## Libraries Used
- **subprocess**: Execute `reg query`, `schtasks`, `wmic` commands to enumerate persistence
- **csv**: Parse schtasks CSV output for scheduled task analysis
- **re**: Pattern matching for suspicious command-line indicators

## CLI Interface

```
python agent.py registry    # Enumerate registry Run keys
python agent.py tasks       # Enumerate scheduled tasks
python agent.py services    # Enumerate suspicious services
python agent.py all         # Run all persistence hunts
```

## Core Functions

### `enumerate_registry_persistence()`
Queries 11 common registry persistence locations using `reg query` and flags entries matching suspicious indicators.

**Returns:** dict with `total_entries`, `suspicious_entries`, and `findings` list (each with `key`, `name`, `type`, `value`, `suspicious`).

### `enumerate_scheduled_tasks()`
Runs `schtasks /query /fo CSV /v` and flags tasks with suspicious actions or non-Microsoft authors.

**Returns:** dict with `total_tasks`, `suspicious_tasks`, and `findings` list.

### `enumerate_services()`
Uses `wmic service get` to list services and flags those running from unusual filesystem paths.

**Returns:** dict with `total_services`, `suspicious_services`, and filtered `findings`.

### `parse_reg_output(output, parent_key)`
Parses `reg query` text output into structured entries with key, name, type, value fields.

## Registry Keys Checked
| Key Path | Persistence Type |
|----------|-----------------|
| `HKLM\...\CurrentVersion\Run` | Auto-start programs |
| `HKLM\...\Winlogon` | Logon scripts, shell replacement |
| `HKLM\...\Active Setup` | Per-user component execution |
| `HKLM\...\Services` | Service binary paths |
| `HKLM\...\Image File Execution Options` | Debugger hijacking |

## Suspicious Indicators
Patterns flagging entries: `\\temp\\`, `powershell.*-enc`, `mshta.exe`, `rundll32.exe`, `base64`, `downloadstring`, `\\users\\public\\`

## Dependencies
No external packages required — uses only Python standard library and Windows built-in commands.

---

## Standards and Controls

## MITRE ATT&CK Persistence Techniques (TA0003)

### Boot or Logon Autostart Execution (T1547)
| Sub-Technique | Name | Registry/Location |
|---------------|------|-------------------|
| T1547.001 | Registry Run Keys / Startup Folder | HKLM/HKCU Run, RunOnce, Startup |
| T1547.002 | Authentication Package | HKLM\SYSTEM\CurrentControlSet\Control\Lsa |
| T1547.003 | Time Providers | HKLM\System\CurrentControlSet\Services\W32Time\TimeProviders |
| T1547.004 | Winlogon Helper DLL | HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon |
| T1547.005 | Security Support Provider | HKLM\SYSTEM\CurrentControlSet\Control\Lsa\Security Packages |
| T1547.006 | Kernel Modules and Extensions | Driver loading |
| T1547.009 | Shortcut Modification | .lnk files in Startup |
| T1547.010 | Port Monitors | HKLM\SYSTEM\CurrentControlSet\Control\Print\Monitors |
| T1547.012 | Print Processors | HKLM\SYSTEM\CurrentControlSet\Control\Print\Environments |
| T1547.014 | Active Setup | HKLM\SOFTWARE\Microsoft\Active Setup\Installed Components |
| T1547.015 | Login Items | (macOS) |

### Create or Modify System Process (T1543)
| Sub-Technique | Name |
|---------------|------|
| T1543.003 | Windows Service |
| T1543.004 | Launch Daemon (macOS/Linux) |

### Scheduled Task/Job (T1053)
| Sub-Technique | Name |
|---------------|------|
| T1053.005 | Scheduled Task |
| T1053.003 | Cron |
| T1053.002 | At |

### Event Triggered Execution (T1546)
| Sub-Technique | Name |
|---------------|------|
| T1546.001 | Change Default File Association |
| T1546.002 | Screensaver |
| T1546.003 | WMI Event Subscription |
| T1546.004 | Unix Shell Configuration Modification |
| T1546.007 | Netsh Helper DLL |
| T1546.008 | Accessibility Features (sethc, utilman, narrator) |
| T1546.010 | AppInit DLLs |
| T1546.011 | Application Shimming |
| T1546.012 | Image File Execution Options Injection |
| T1546.013 | PowerShell Profile |
| T1546.015 | COM Hijacking |
| T1546.016 | Installer Packages |

### Hijack Execution Flow (T1574)
| Sub-Technique | Name |
|---------------|------|
| T1574.001 | DLL Search Order Hijacking |
| T1574.002 | DLL Side-Loading |
| T1574.006 | Dynamic Linker Hijacking |
| T1574.008 | Path Interception by Search Order Hijacking |
| T1574.009 | Path Interception by Unquoted Service Path |
| T1574.011 | Services Registry Permissions Weakness |
| T1574.012 | COR_PROFILER |

## Key Registry Persistence Locations

```
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce
HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\RunServices
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run
HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run
HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\Shell
HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\Userinit
HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\Notify
HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\BootExecute
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\SharedTaskScheduler
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\ShellServiceObjectDelayLoad
HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options
HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\SilentProcessExit
HKLM\SOFTWARE\Classes\CLSID\{GUID}\InprocServer32
HKLM\SYSTEM\CurrentControlSet\Control\Lsa\Security Packages
HKLM\SYSTEM\CurrentControlSet\Control\Lsa\Authentication Packages
HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Custom
HKLM\SOFTWARE\Microsoft\Active Setup\Installed Components
```

## Detection Event IDs

| Source | Event ID | Meaning |
|--------|----------|---------|
| Sysmon | 12 | Registry object created/deleted |
| Sysmon | 13 | Registry value set |
| Sysmon | 14 | Registry object renamed |
| Sysmon | 19 | WMI EventFilter created |
| Sysmon | 20 | WMI EventConsumer created |
| Sysmon | 21 | WMI ConsumerToFilter binding |
| Windows Security | 4697 | Service installed |
| Windows Security | 4698 | Scheduled task created |
| Windows Security | 4699 | Scheduled task deleted |
| Windows Security | 7045 | New service installed |
| Task Scheduler | 106 | Task registered |
| Task Scheduler | 140 | Task updated |

---

## Workflows

## Phase 1: Registry Persistence Hunting

### Step 1.1 - Run Key Monitoring
```spl
index=sysmon (EventCode=12 OR EventCode=13)
| where match(TargetObject, "(?i)\\\\CurrentVersion\\\\(Run|RunOnce|Policies\\\\Explorer\\\\Run)")
| table _time Computer User EventType TargetObject Details Image
| sort -_time
```

### Step 1.2 - Winlogon Modification
```spl
index=sysmon EventCode=13
| where match(TargetObject, "(?i)\\\\Winlogon\\\\(Shell|Userinit|Notify)")
| table _time Computer User TargetObject Details Image
```

### Step 1.3 - IFEO Injection
```spl
index=sysmon EventCode=13
| where match(TargetObject, "(?i)Image File Execution Options.*\\\\(Debugger|GlobalFlag)")
| table _time Computer User TargetObject Details Image
```

### Step 1.4 - KQL for Registry Persistence
```kql
DeviceRegistryEvents
| where Timestamp > ago(7d)
| where RegistryKey has_any ("CurrentVersion\\Run","Winlogon\\Shell","Image File Execution Options")
| where ActionType in ("RegistryValueSet","RegistryKeyCreated")
| project Timestamp, DeviceName, RegistryKey, RegistryValueName, RegistryValueData, InitiatingProcessFileName
```

## Phase 2: Service Persistence Hunting

### Step 2.1 - New Service Installation
```spl
index=wineventlog (EventCode=7045 OR EventCode=4697)
| where NOT match(Service_File_Name, "(?i)(windows|program files|system32)")
| table _time Computer Service_Name Service_File_Name Service_Start_Type Service_Account
| sort -_time
```

### Step 2.2 - Service Binary Path Anomalies
```spl
index=wineventlog EventCode=7045
| where match(Service_File_Name, "(?i)(temp|appdata|public|programdata|users)")
    OR match(Service_File_Name, "(?i)(powershell|cmd\.exe|wscript|cscript|mshta)")
| table _time Computer Service_Name Service_File_Name
```

## Phase 3: WMI Persistence Hunting

### Step 3.1 - WMI Event Subscription
```spl
index=sysmon (EventCode=19 OR EventCode=20 OR EventCode=21)
| table _time Computer User EventType Operation Destination Consumer Filter
| sort -_time
```

### Step 3.2 - PowerShell WMI Creation
```spl
index=sysmon EventCode=1 Image="*\\powershell.exe"
| where match(CommandLine, "(?i)(Register-WmiEvent|Set-WmiInstance|__EventFilter|CommandLineEventConsumer)")
| table _time Computer User CommandLine
```

## Phase 4: COM Hijacking

### Step 4.1 - InprocServer32 Modifications
```spl
index=sysmon EventCode=13
| where match(TargetObject, "(?i)\\\\InprocServer32\\\\$")
| where NOT match(Details, "(?i)(system32|syswow64|program files|windows)")
| table _time Computer User TargetObject Details Image
```

## Phase 5: Scheduled Task Persistence

### Step 5.1 - New Scheduled Tasks
```spl
index=wineventlog (EventCode=4698 OR source="Microsoft-Windows-TaskScheduler/Operational" EventCode=106)
| table _time Computer User Task_Name Task_Content
| sort -_time
```

## Phase 6: Cross-Reference and Validate

### Step 6.1 - Autoruns Comparison
- Export Autoruns data from reference system: `autorunsc.exe -a * -c -h -s -v -vt > autoruns_baseline.csv`
- Export from suspect system: `autorunsc.exe -a * -c -h -s -v -vt > autoruns_current.csv`
- Diff the two outputs to find new entries

### Step 6.2 - Verify Binary Signatures
For each suspicious persistence entry:
1. Check digital signature validity
2. Verify file hash against threat intel
3. Check VirusTotal reputation
4. Analyze with YARA rules
5. Submit to sandbox if needed

---

## Working Template

## Hunt Metadata

| Field | Value |
|-------|-------|
| Hunt ID | TH-PERSIST-YYYY-MM-DD-NNN |
| Analyst | |
| Date | |
| Status | [ ] In Progress / [ ] Complete |

## Hypothesis

> [e.g., "Adversaries have established persistence via registry Run keys or WMI event subscriptions on compromised endpoints."]

## Persistence Categories Investigated

- [ ] T1547.001 - Registry Run Keys / Startup Folder
- [ ] T1543.003 - Windows Services
- [ ] T1053.005 - Scheduled Tasks
- [ ] T1546.003 - WMI Event Subscriptions
- [ ] T1546.015 - COM Hijacking
- [ ] T1546.012 - IFEO Injection
- [ ] T1546.010 - AppInit DLLs
- [ ] T1547.004 - Winlogon Helper
- [ ] T1547.005 - Security Support Provider
- [ ] T1574.001 - DLL Search Order Hijacking

## Registry Persistence Findings

| # | Host | Key Path | Value | Modifying Process | Signed? | Risk | Verdict |
|---|------|----------|-------|-------------------|---------|------|---------|
| 1 | | | | | | | |

## Service Persistence Findings

| # | Host | Service Name | Binary Path | Account | Start Type | Risk | Verdict |
|---|------|-------------|-------------|---------|-----------|------|---------|
| 1 | | | | | | | |

## Scheduled Task Findings

| # | Host | Task Name | Action | Trigger | Risk | Verdict |
|---|------|-----------|--------|---------|------|---------|
| 1 | | | | | | |

## WMI Subscription Findings

| # | Host | Filter | Consumer | Binding | Risk | Verdict |
|---|------|--------|----------|---------|------|---------|
| 1 | | | | | | |

## Summary

| Persistence Type | Total Found | Malicious | Suspicious | Benign |
|-----------------|-------------|-----------|------------|--------|
| Registry | | | | |
| Services | | | | |
| Scheduled Tasks | | | | |
| WMI | | | | |
| COM Hijack | | | | |
| Other | | | | |

## Recommendations

1. **Remove Malicious Persistence**: [Specific entries to remove]
2. **Harden**: [GPO restrictions, Sysmon rules to add]
3. **Monitor**: [New detection rules for identified gaps]
