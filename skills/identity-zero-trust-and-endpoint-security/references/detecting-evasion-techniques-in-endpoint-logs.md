# Detecting Evasion Techniques In Endpoint Logs

## API Reference

## Key Windows Event IDs for Evasion

| Event ID | Source | Evasion Technique |
|----------|--------|-------------------|
| 1102 | Security | Audit log cleared (T1070.001) |
| Sysmon 2 | Sysmon | Timestomping (T1070.006) |
| Sysmon 8 | Sysmon | CreateRemoteThread (T1055) |
| Sysmon 10 | Sysmon | Process Access / LSASS (T1003) |
| 4688 | Security | Process creation with cmdline |

## python-evtx Usage

```python
import Evtx.Evtx as evtx
with evtx.Evtx("Sysmon.evtx") as log:
    for record in log.records():
        xml = record.xml()
        # Parse EventID, CommandLine, SourceImage, TargetImage
```

## Evasion Detection Patterns

```python
# Log clearing
r"wevtutil\s+(cl|clear-log)"
r"Clear-EventLog"
# Security tool disable
r"Set-MpPreference\s+-DisableRealtimeMonitoring\s+\$true"
r"sc\s+(stop|delete)\s+WinDefend"
# AMSI bypass
r"[Ref].Assembly.GetType.*AMSI"
r"amsiInitFailed"
```

## MITRE ATT&CK TA0005 Techniques

| Technique | ID | Detection |
|-----------|----|-----------|
| Indicator Removal | T1070 | Log clearing, file deletion |
| Timestomping | T1070.006 | Sysmon Event ID 2 |
| Process Injection | T1055 | Sysmon Event ID 8 |
| Impair Defenses | T1562.001 | AV/EDR disabling commands |
| AMSI Bypass | T1562.001 | PowerShell AMSI patching |

## Splunk SPL Detection

```spl
index=sysmon (EventCode=2 OR EventCode=8 OR EventCode=10)
| eval technique=case(
    EventCode=2, "Timestomping",
    EventCode=8, "Process Injection",
    EventCode=10, "Process Access")
| stats count by technique, SourceImage, Computer
```

## CLI Usage

```bash
python agent.py --evtx-file Sysmon.evtx
python agent.py --evtx-file Security.evtx
```

---

## Standards and Controls

## Primary Standards

### MITRE ATT&CK TA0005 - Defense Evasion
- **URL**: https://attack.mitre.org/tactics/TA0005/
- **Scope**: 43 techniques and 80+ sub-techniques for defense evasion
- **Key techniques**: T1055 (Process Injection), T1070 (Indicator Removal), T1036 (Masquerading), T1218 (System Binary Proxy Execution), T1562 (Impair Defenses)

### Sigma Detection Rules
- **URL**: https://github.com/SigmaHQ/sigma
- **Scope**: Community-maintained detection rules in vendor-agnostic format
- **Evasion rules**: rules/windows/process_creation/proc_creation_win_*, rules/windows/sysmon/

### LOLBAS Project
- **URL**: https://lolbas-project.github.io/
- **Scope**: Catalog of Windows binaries that can be used for defense evasion, with detection recommendations

## Compliance Mappings

| Framework | Requirement | Detection Coverage |
|-----------|------------|-------------------|
| NIST 800-53 | SI-4 System Monitoring | Evasion detection via endpoint logging |
| NIST 800-53 | AU-6 Audit Record Review | Log analysis for tampering indicators |
| PCI DSS 4.0 | 10.4.1 - Audit log review | Automated detection of log tampering |
| ISO 27001 | A.12.4.1 - Event logging | Integrity monitoring of security logs |

## Supporting References

- **Sysmon Configuration**: https://github.com/SwiftOnSecurity/sysmon-config
- **Olaf Hartong Sysmon Modular**: https://github.com/olafhartong/sysmon-modular
- **SANS Hunt Evil Poster**: Comprehensive guide to suspicious Windows process behavior
- **Elastic Detection Rules**: https://github.com/elastic/detection-rules

---

## Workflows

## Workflow 1: Evasion Technique Threat Hunt

```
[Select evasion technique to hunt]
    │
    ├── T1055 Process Injection
    ├── T1070 Log Tampering
    ├── T1036 Masquerading
    ├── T1562 Security Tool Disabling
    │
    ▼
[Craft detection query (Splunk/KQL/Elastic)]
    │
    ▼
[Execute across 30-90 days of endpoint telemetry]
    │
    ▼
[Triage results]
    │
    ├── Known-good (allowlist) ──► [Add to baseline, refine query]
    ├── Suspicious ──► [Deep investigation]
    │                       │
    │                       ├── Correlate with other telemetry
    │                       ├── Check process tree
    │                       ├── Review network connections
    │                       │
    │                       ├── True positive ──► [Escalate to IR]
    │                       └── False positive ──► [Tune detection]
    │
    └── No results ──► [Validate logging covers technique]
```

## Workflow 2: Detection Rule Deployment

```
[Create Sigma/SIEM detection rule]
    │
    ▼
[Test against historical data]
    │
    ├── High false positive rate ──► [Refine exclusions]
    │
    └── Acceptable FP rate ──► [Deploy in alert mode]
                                     │
                                     ▼
                                [Monitor for 2 weeks]
                                     │
                                     ▼
                                [Review alert quality]
                                     │
                                     ▼
                                [Promote to production detection]
```

## Workflow 3: Evasion Incident Response

```
[Evasion technique detected]
    │
    ▼
[Assess scope: Which endpoints affected?]
    │
    ▼
[Correlate with initial access and persistence]
    │
    ▼
[Determine if adversary achieved objectives]
    │
    ├── Active intrusion ──► [Full incident response]
    │
    └── Isolated event ──► [Remediate endpoint, enhance detection]
```

---

## Working Template

## Hunt Information

| Field | Value |
|-------|-------|
| Hunt Name | |
| Target Technique | MITRE ATT&CK ID |
| Hypothesis | |
| Data Sources | Sysmon / Windows Security / EDR |
| Time Range | |
| Analyst | |

## Detection Queries

| SIEM | Query | Expected Results |
|------|-------|-----------------|
| Splunk | | |
| Elastic KQL | | |
| MDE Advanced Hunting | | |

## Findings

| Timestamp | Host | Technique | Severity | Evidence | True/False Positive |
|-----------|------|-----------|----------|----------|-------------------|
| | | | | | |

## Tuning Actions

| Finding | Action | New Exclusion | Status |
|---------|--------|---------------|--------|
| | Allow / Investigate / Block | | |

## Sign-Off

| Role | Name | Date |
|------|------|------|
| Threat Hunter | | |
| SOC Lead | | |
