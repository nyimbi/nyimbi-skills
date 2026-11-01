# Hunting For Suspicious Scheduled Tasks

## API Reference

## Windows Event IDs

| Event ID | Source | Description |
|----------|--------|-------------|
| 4698 | Security | Scheduled task created |
| 4699 | Security | Scheduled task deleted |
| 4702 | Security | Scheduled task updated |
| 106 | TaskScheduler | Task registered |
| 200/201 | TaskScheduler | Task executed / completed |

## python-evtx

```python
import Evtx.Evtx as evtx
import xml.etree.ElementTree as ET

with evtx.Evtx("Security.evtx") as log:
    for record in log.records():
        root = ET.fromstring(record.xml())
        ns = {"ns": "http://schemas.microsoft.com/win/2004/08/events/event"}
        eid = root.find(".//ns:EventID", ns).text
        if eid == "4698":
            data = {d.get("Name"): d.text
                    for d in root.findall(".//ns:Data", ns)}
```

## Splunk SPL

```spl
index=wineventlog EventCode=4698
| spath output=TaskName path=EventData.TaskName
| spath output=TaskContent path=EventData.TaskContent
| where NOT match(TaskName, "\\\\Microsoft\\\\Windows\\\\")
| where match(TaskContent, "(?i)(powershell|cmd|wscript|http)")
| table _time Computer SubjectUserName TaskName TaskContent
```

## KQL (Microsoft Sentinel)

```kql
SecurityEvent
| where EventID == 4698
| extend TaskContent = tostring(EventData.TaskContent)
| where TaskContent has_any ("powershell", "cmd.exe", "Temp", "AppData")
| project TimeGenerated, Computer, Account, TaskContent
```

## PowerShell Enumeration

```powershell
Get-ScheduledTask | Where-Object {
    $_.Actions.Execute -match 'powershell|cmd|wscript' -or
    $_.Actions.Execute -match '\\Temp\\|\\AppData\\'
} | Select-Object TaskName, TaskPath, @{N='Action';E={$_.Actions.Execute}}
```

### References

- MITRE T1053.005: https://attack.mitre.org/techniques/T1053/005/
- python-evtx: https://github.com/williballenthin/python-evtx
- Sigma rules for schtasks: https://github.com/SigmaHQ/sigma

---

## Standards and Controls

## MITRE ATT&CK References
| Technique | Name | Usage |
|-----------|------|-------|
| T1053.005 | Scheduled Task | Primary persistence/execution technique |
| T1053.003 | Cron (Linux) | Scheduled execution on Linux |
| T1078 | Valid Accounts | Tasks running under legitimate accounts |

## Windows Event IDs
| Event ID | Source | Description |
|----------|--------|-------------|
| 4698 | Security | Scheduled task created |
| 4699 | Security | Scheduled task deleted |
| 4700 | Security | Scheduled task enabled |
| 4701 | Security | Scheduled task disabled |
| 4702 | Security | Scheduled task updated |
| 106 | TaskScheduler/Operational | Task registered |
| 200 | TaskScheduler/Operational | Action started |
| 201 | TaskScheduler/Operational | Action completed |

## Suspicious Task Indicators
| Indicator | Description |
|-----------|-------------|
| User-writable paths | Actions executing from TEMP, AppData, Downloads |
| Encoded commands | Base64 or -EncodedCommand in arguments |
| Script interpreters | PowerShell, cmd, wscript, cscript as actions |
| Short intervals | Trigger repeating every 1-5 minutes |
| System startup trigger | Task runs at boot for persistence |
| Remote creation | Task created from remote system |
| Name mimicry | Task name similar to legitimate Windows tasks |
| Hidden SD | Security Descriptor modified to hide task |

---

## Workflows

## Phase 1: Task Enumeration
```powershell
# Full task export with details
Get-ScheduledTask | Where-Object { $_.TaskPath -notmatch "\\Microsoft\\" } |
    ForEach-Object { $_ | Get-ScheduledTaskInfo; $_.Actions | Select-Object Execute, Arguments }

# Check for hidden tasks in registry
Get-ChildItem "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tree" -Recurse
```

## Phase 2: SIEM Analysis
```spl
index=wineventlog EventCode=4698
| spath output=TaskName path=EventData.TaskName
| spath output=TaskContent path=EventData.TaskContent
| rex field=TaskContent "<Command>(?<cmd>[^<]+)</Command>"
| rex field=TaskContent "<Arguments>(?<args>[^<]+)</Arguments>"
| table _time Computer SubjectUserName TaskName cmd args
```

## Phase 3: Remote Task Creation Detection
```spl
index=sysmon EventCode=1 Image="*\\schtasks.exe"
| where match(CommandLine, "(?i)/create.*/s\s+")
| rex field=CommandLine "/s\s+(?<remote_host>\S+)"
| table _time Computer User remote_host CommandLine
```

## Phase 4: Response
1. Remove malicious scheduled tasks
2. Check task XML definitions for hidden parameters
3. Audit all non-Microsoft scheduled tasks across fleet
4. Deploy detection rules for suspicious task creation

---

## Working Template

## Hunt Metadata
| Field | Value |
|-------|-------|
| Hunt ID | TH-SCHTASK-YYYY-MM-DD-NNN |
| Analyst | |
| Date | |
| Status | [ ] In Progress / [ ] Complete |

## Hypothesis
> Adversaries have established persistence via scheduled tasks that execute malicious payloads at system startup, user logon, or recurring intervals.

## Task Findings

| # | Host | Task Name | Action | Trigger | Created By | Created Time | Risk |
|---|------|-----------|--------|---------|-----------|-------------|------|
| 1 | | | | | | | |

## Recommendations
1. **Remove**: [Malicious scheduled tasks]
2. **Investigate**: [Executed payloads and their impact]
3. **Detect**: [Deploy 4698 monitoring rules]
4. **Baseline**: [Establish known-good task inventory]
