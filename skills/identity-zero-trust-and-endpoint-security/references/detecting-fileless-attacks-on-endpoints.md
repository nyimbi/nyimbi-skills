# Detecting Fileless Attacks On Endpoints

## API Reference

## Key Event Sources

| Source | Event ID | Detection |
|--------|----------|-----------|
| PowerShell Script Block | 4104 | Malicious script content |
| Sysmon Process Create | 1 | Encoded command execution |
| Sysmon CreateRemoteThread | 8 | Reflective DLL injection |
| Sysmon WMI EventFilter | 19 | WMI persistence |
| Sysmon WMI EventConsumer | 20 | WMI persistence |
| Sysmon WMI Binding | 21 | WMI persistence |

## python-evtx Usage

```python
import Evtx.Evtx as evtx
with evtx.Evtx("PowerShell-Operational.evtx") as log:
    for record in log.records():
        xml = record.xml()
        # Parse Event 4104 ScriptBlockText
```

## Suspicious PowerShell Patterns

```python
# Dynamic execution
r"Invoke-Expression|IEX\s*\("
# Reflective loading
r"System\.Reflection\.Assembly.*Load"
# Memory injection APIs
r"VirtualAlloc|VirtualProtect|CreateThread"
# WMI persistence
r"Register-WMI|__EventFilter|__EventConsumer"
# Encoded commands
r"-enc\s|-encodedcommand\s"
```

## Splunk SPL - Fileless Detection

```spl
index=powershell EventCode=4104
| where match(ScriptBlockText, "(?i)(Invoke-Expression|IEX|VirtualAlloc|FromBase64)")
| stats count by ScriptBlockText, Computer, UserID
```

## AMSI (Anti-Malware Scan Interface)

```powershell
# Enable AMSI logging
Set-MpPreference -EnableNetworkProtection Enabled
# Check AMSI status
Get-MpComputerStatus | Select AMServiceEnabled, AntispywareEnabled
```

## WMI Persistence Detection

```powershell
# List WMI event subscriptions
Get-WMIObject -Namespace root\Subscription -Class __EventFilter
Get-WMIObject -Namespace root\Subscription -Class __EventConsumer
Get-WMIObject -Namespace root\Subscription -Class __FilterToConsumerBinding
```

## CLI Usage

```bash
python agent.py --ps-log PowerShell-Operational.evtx
python agent.py --sysmon-log Sysmon.evtx --check-wmi --check-injection
```

---

## Standards and Controls

- **MITRE ATT&CK T1059.001**: PowerShell execution
- **MITRE ATT&CK T1055**: Process Injection (all sub-techniques)
- **MITRE ATT&CK T1546.003**: WMI Event Subscription persistence
- **MITRE ATT&CK T1620**: Reflective Code Loading
- **Microsoft AMSI Documentation**: https://learn.microsoft.com/en-us/windows/win32/amsi/
- **PowerShell Logging**: https://learn.microsoft.com/en-us/powershell/scripting/windows-powershell/wmf/whats-new/script-logging

---

## Workflows

## Fileless Attack Detection
```
[Enable telemetry (Sysmon, PS logging, AMSI)] → [Build detection rules per technique]
  → [Deploy rules in SIEM] → [Threat hunt for historical fileless indicators]
  → [Triage alerts] → [Investigate memory for confirmed incidents]
  → [Extract IOCs from memory analysis] → [Tune detections]
```

---

## Working Template

## Telemetry Status
| Source | Enabled | Event IDs |
|--------|---------|-----------|
| Sysmon | Yes/No | 1,7,8,10,19,20,21 |
| PowerShell Script Block | Yes/No | 4104 |
| AMSI | Yes/No | 1116 |

## Detection Rules
| Rule Name | Technique | SIEM Query | Status |
|-----------|-----------|-----------|--------|
| | T1059.001 | | Active/Draft |

## Sign-Off
| Role | Name | Date |
|------|------|------|
| Detection Engineer | | |
| SOC Lead | | |
