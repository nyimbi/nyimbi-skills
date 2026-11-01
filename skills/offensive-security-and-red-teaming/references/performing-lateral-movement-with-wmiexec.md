# Performing Lateral Movement With Wmiexec

## API Reference

## Libraries Used
- **python-evtx**: Parse Windows EVTX logs for WMI process creation artifacts
- **subprocess**: Execute Impacket wmiexec, tshark PCAP analysis, WMIC queries
- **xml.etree.ElementTree**: Parse Sysmon/Security event XML
- **impacket** (external): wmiexec.py for authorized lateral movement testing

## CLI Interface
```
python agent.py detect --evtx security.evtx
python agent.py exec --target 10.0.0.5 --domain CORP --user admin [--cmd whoami]
python agent.py network --pcap capture.pcap
python agent.py persistence
```

## Core Functions

### `detect_wmiexec_artifacts_evtx(evtx_file)` — Detect WMIExec in event logs
Searches for: Sysmon EID 1 with wmiprvse.exe parent, EID 4624 type 3 logons, EID 7045 service installs.

### `run_wmiexec_impacket(target, domain, username, command)` — Execute remote command
Uses Impacket wmiexec for authorized penetration testing.

### `detect_wmi_network_traffic(pcap_file)` — PCAP analysis for WMI
Uses tshark to filter DCOM UUID 4d9f4ab8-7d1c-11cf-861e-0020af6e7c57 and port 135.

### `check_wmi_persistence()` — Local WMI subscription audit
Queries __EventFilter, CommandLineEventConsumer, __FilterToConsumerBinding.

## Detection Indicators
| Artifact | Event ID | Indicator |
|----------|----------|-----------|
| Process from WMI | Sysmon 1 | ParentImage = wmiprvse.exe |
| Network logon | Security 4624 | LogonType = 3 |
| Service install | System 7045 | BTOBTO/wmi patterns |

## Dependencies
```
pip install python-evtx impacket
```
System: tshark (optional, for PCAP analysis)

---

## Standards and Controls

## MITRE ATT&CK References

| Technique ID | Name | Tactic |
|-------------|------|--------|
| T1047 | Windows Management Instrumentation | Execution |
| T1021.003 | Remote Services: DCOM | Lateral Movement |
| T1550.002 | Use Alternate Authentication Material: Pass the Hash | Lateral Movement |
| T1059.001 | PowerShell | Execution |
| T1570 | Lateral Tool Transfer | Lateral Movement |

## Tools

- Impacket wmiexec.py: https://github.com/fortra/impacket
- CrackMapExec: https://github.com/byt3bl33d3r/CrackMapExec
- SharpWMI: https://github.com/GhostPack/SharpWMI

## Detection Resources

- Windows WMI Activity Log: Microsoft-Windows-WMI-Activity/Operational
- Event 5857: WMI provider loaded
- Event 5860/5861: WMI registration events
- Sysmon Event 19/20/21: WMI filter/consumer/binding creation

---

## Workflows

## Lateral Movement Chain

```
1. Initial Compromise → Credential Harvesting → WMIExec to target
2. On each new host:
   ├── Enumerate local users and groups
   ├── Harvest credentials (LaZagne, Mimikatz, SAM dump)
   ├── Check for domain admin sessions
   └── Pivot to next target using recovered credentials
```

## Multi-Method Fallback

```
Primary:   wmiexec.py (semi-interactive, output capture)
Fallback1: dcomexec.py (different DCOM object, avoids WMI-specific detection)
Fallback2: Native PowerShell CIM (blends with admin activity)
Fallback3: smbexec.py (uses SMB service, noisier but reliable)
```

---

## Working Template

## Movement Log

| # | Source | Target | Method | Credential | Time | Result |
|---|--------|--------|--------|------------|------|--------|
| 1 | | | wmiexec / dcomexec / native | | | |

## Access Summary

| Host | Admin Access | Credentials Recovered | Sessions Found |
|------|-------------|----------------------|----------------|
| | Yes/No | | |

## OPSEC Notes

- [ ] No services created on target hosts
- [ ] Temporary output files cleaned from ADMIN$
- [ ] WMI event subscription artifacts removed
- [ ] No persistent modifications left on targets
