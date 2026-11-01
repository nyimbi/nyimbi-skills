# Hunting For Persistence Via Wmi Subscriptions

## API Reference

## Libraries Used
- **subprocess**: Execute WMIC and PowerShell commands for WMI enumeration
- **python-evtx** (Evtx): Parse Sysmon EVTX for WMI-related events (IDs 19, 20, 21)
- **re**: Pattern matching for suspicious WMI consumer payloads

## CLI Interface

```
python agent.py enumerate                  # WMIC-based WMI subscription enumeration
python agent.py powershell                 # PowerShell Get-WMIObject enumeration
python agent.py sysmon --evtx-file <path>  # Scan Sysmon EVTX for WMI events
```

## Core Functions

### `enumerate_wmi_subscriptions()`
Queries four WMI subscription classes via WMIC and flags entries matching suspicious patterns.

**Returns:** dict with `classes` (EventFilter, EventConsumer, ActiveScriptEventConsumer, FilterToConsumerBinding) and `suspicious` list.

### `scan_sysmon_wmi_events(evtx_file)`
Parses Sysmon EVTX for Event IDs 19 (WmiEventFilter), 20 (WmiEventConsumer), 21 (WmiEventBinding).

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `evtx_file` | str | Path to Sysmon .evtx file |

### `query_powershell_wmi()`
Uses PowerShell `Get-WMIObject` to enumerate WMI subscriptions in `root\Subscription` namespace.

## WMI Classes Enumerated

| Class | Description |
|-------|-------------|
| `__EventFilter` | Defines the WQL query that triggers the subscription |
| `CommandLineEventConsumer` | Executes a command when the filter matches |
| `ActiveScriptEventConsumer` | Runs VBScript/JScript when the filter matches |
| `__FilterToConsumerBinding` | Links a filter to its consumer |

## Sysmon Event IDs

| Event ID | Description |
|----------|-------------|
| 19 | WmiEvent - Filter activity detected |
| 20 | WmiEvent - Consumer activity detected |
| 21 | WmiEvent - Consumer-to-filter binding |

## Dependencies
```
pip install python-evtx  # Optional, for EVTX parsing
```

---

## Standards and Controls

## MITRE ATT&CK References

| Technique | Name | Description |
|-----------|------|-------------|
| T1546.003 | WMI Event Subscription | Primary persistence technique |
| T1047 | WMI | WMI execution for lateral movement |
| T1059.005 | Visual Basic | VBScript in ActiveScriptEventConsumer |
| T1059.007 | JavaScript | JScript in ActiveScriptEventConsumer |

## WMI Subscription Components

| Component | WMI Class | Purpose |
|-----------|-----------|---------|
| Event Filter | __EventFilter | Defines the trigger (WQL query) |
| Event Consumer | __EventConsumer | Defines the action |
| Binding | __FilterToConsumerBinding | Links filter to consumer |

## Consumer Types and Risk

| Consumer Class | Risk Level | Description |
|---------------|-----------|-------------|
| ActiveScriptEventConsumer | Critical | Executes VBScript/JScript code |
| CommandLineEventConsumer | Critical | Executes arbitrary commands |
| LogFileEventConsumer | Low | Writes to a log file |
| NTEventLogEventConsumer | Low | Writes to Windows Event Log |
| SMTPEventConsumer | Medium | Sends email notifications |

## Common Malicious Filter Queries

| Filter Type | WQL Query | Usage |
|-------------|-----------|-------|
| Process Start | SELECT * FROM __InstanceCreationEvent WITHIN 5 WHERE TargetInstance ISA 'Win32_Process' | Execute on specific process start |
| System Startup | SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_PerfFormattedData_PerfOS_System' | Execute shortly after boot |
| Timer-Based | SELECT * FROM __TimerEvent WHERE TimerID='MyTimer' | Execute at intervals |
| User Logon | SELECT * FROM __InstanceCreationEvent WHERE TargetInstance ISA 'Win32_LogonSession' | Execute on user logon |

## Detection Events

| Source | Event ID | Description |
|--------|----------|-------------|
| Sysmon | 19 | WmiEventFilter activity detected |
| Sysmon | 20 | WmiEventConsumer activity detected |
| Sysmon | 21 | WmiEventConsumerToFilter activity detected |
| WMI-Activity | 5861 | WMI permanent event subscription created |
| Security | 4688 | Process creation (mofcomp.exe, WmiPrvSe.exe children) |

## Known APT Usage

| Group | Technique Details |
|-------|-------------------|
| APT29 | ActiveScriptEventConsumer with encoded VBScript backdoor |
| APT32 (OceanLotus) | WMI subscription for persistence in targeted attacks |
| FIN8 | CommandLineEventConsumer for PowerShell execution |
| Turla | WMI event subscription combined with COM hijacking |
| HEXANE | WMI persistence in Middle Eastern energy sector attacks |

---

## Workflows

## Phase 1: Enumerate Existing Subscriptions

### Step 1.1 - PowerShell Enumeration
```powershell
# List all event filters
Get-WMIObject -Namespace root\Subscription -Class __EventFilter | Select-Object Name, Query, QueryLanguage

# List all event consumers
Get-WMIObject -Namespace root\Subscription -Class __EventConsumer | Select-Object Name, __CLASS

# List all bindings
Get-WMIObject -Namespace root\Subscription -Class __FilterToConsumerBinding | Select-Object Filter, Consumer

# Detailed ActiveScriptEventConsumer inspection
Get-WMIObject -Namespace root\Subscription -Class ActiveScriptEventConsumer | Select-Object Name, ScriptingEngine, ScriptText

# Detailed CommandLineEventConsumer inspection
Get-WMIObject -Namespace root\Subscription -Class CommandLineEventConsumer | Select-Object Name, ExecutablePath, CommandLineTemplate
```

### Step 1.2 - WMIC Enumeration
```cmd
wmic /namespace:\\root\subscription path __EventFilter get Name, Query
wmic /namespace:\\root\subscription path __EventConsumer get Name, __CLASS
wmic /namespace:\\root\subscription path __FilterToConsumerBinding get Filter, Consumer
```

## Phase 2: Monitor Creation Events

### Step 2.1 - Sysmon WMI Event Detection
```spl
index=sysmon (EventCode=19 OR EventCode=20 OR EventCode=21)
| eval event_type=case(
    EventCode=19, "EventFilter Created",
    EventCode=20, "EventConsumer Created",
    EventCode=21, "Binding Created"
)
| table _time Computer User event_type Name Query Consumer Destination
```

### Step 2.2 - Windows WMI Activity Log
```spl
index=wineventlog source="Microsoft-Windows-WMI-Activity/Operational"
| where EventCode IN (5857, 5858, 5859, 5860, 5861)
| table _time Computer EventCode NamespaceName Query Operation PossibleCause
```

## Phase 3: Hunt for WmiPrvSe.exe Suspicious Children

### Step 3.1 - Process Tree Analysis
```spl
index=sysmon EventCode=1
| where match(ParentImage, "(?i)WmiPrvSe\.exe$")
| where match(Image, "(?i)(cmd|powershell|wscript|cscript|mshta|rundll32|regsvr32)\.exe$")
| table _time Computer Image CommandLine User ParentImage
```

### Step 3.2 - MOF Compilation Detection
```spl
index=sysmon EventCode=1 Image="*\\mofcomp.exe"
| table _time Computer User CommandLine ParentImage
```

## Phase 4: Removal and Cleanup

### Step 4.1 - Remove Malicious Subscription
```powershell
# Remove specific subscription components
Get-WMIObject -Namespace root\Subscription -Class __EventFilter -Filter "Name='MaliciousFilter'" | Remove-WmiObject
Get-WMIObject -Namespace root\Subscription -Class CommandLineEventConsumer -Filter "Name='MaliciousConsumer'" | Remove-WmiObject
Get-WMIObject -Namespace root\Subscription -Class __FilterToConsumerBinding -Filter "Filter=""__EventFilter.Name='MaliciousFilter'""" | Remove-WmiObject
```

## Phase 5: Response
1. Document all found subscriptions with full details
2. Remove malicious subscriptions from all affected hosts
3. Block WMI subscription creation via Group Policy where possible
4. Deploy ongoing monitoring via Sysmon Events 19/20/21
5. Investigate initial infection vector that created the subscription

---

## Working Template

## Hunt Metadata
| Field | Value |
|-------|-------|
| Hunt ID | TH-WMI-YYYY-MM-DD-NNN |
| Analyst | |
| Date | |
| Status | [ ] In Progress / [ ] Complete |

## Hypothesis
> Adversaries have established persistence via WMI permanent event subscriptions to execute malicious code triggered by system events such as startup or user logon.

## WMI Subscription Findings

| # | Host | Subscription Name | Filter Query | Consumer Type | Consumer Action | Severity |
|---|------|-------------------|-------------|---------------|----------------|----------|
| 1 | | | | | | |

## WmiPrvSe.exe Child Process Findings

| # | Host | Child Process | Command Line | User | Timestamp |
|---|------|--------------|-------------|------|-----------|
| 1 | | | | | |

## Recommendations
1. **Remove**: [Malicious WMI subscriptions]
2. **Investigate**: [Initial infection vector]
3. **Harden**: [Restrict WMI subscription creation]
4. **Monitor**: [Deploy Sysmon Events 19/20/21 rules]
