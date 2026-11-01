# Hunting For Living Off The Land Binaries

## API Reference

## Libraries Used
- **elasticsearch** (elasticsearch-py): Query Elastic SIEM for LOLBin process events
- **python-evtx** (Evtx): Parse Windows EVTX event logs for Sysmon process creation
- **re**: Regex matching against suspicious command-line argument patterns

## CLI Interface

```
python agent.py hunt --es-host <url> --index <pattern> [--api-key <key>] [--hours <n>]
python agent.py sysmon --evtx-file <path>
```

## Core Functions

### `hunt_lolbins_elastic(es_host, es_index, api_key=None, hours=24)`
Queries Elasticsearch for 12 LOLBin binaries with suspicious argument patterns.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `es_host` | str | Elasticsearch host URL |
| `es_index` | str | Index pattern (default: `logs-*`) |
| `api_key` | str | Optional API key |
| `hours` | int | Lookback window in hours |

**Returns:** dict with `detections` list (each with `binary`, `mitre`, `count`, `events`).

### `scan_sysmon_log(evtx_file)`
Parses Sysmon EVTX logs for Event ID 1 (Process Creation) matching LOLBin names.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `evtx_file` | str | Path to Sysmon .evtx file |

**Returns:** dict with `lolbin_events` count and `findings` list.

## LOLBins Covered

| Binary | MITRE Technique | Suspicious Pattern Examples |
|--------|----------------|---------------------------|
| certutil.exe | T1140, T1105 | `-urlcache`, `-decode`, `-encode` |
| mshta.exe | T1218.005 | `vbscript:`, `javascript:`, HTTP URLs |
| regsvr32.exe | T1218.010 | `/s /n /u /i:`, `scrobj.dll` |
| rundll32.exe | T1218.011 | `javascript:`, `shell32.dll` |
| bitsadmin.exe | T1197 | `/transfer`, `/download` |
| wmic.exe | T1047 | `process call create`, `/node:` |
| powershell.exe | T1059.001 | `-enc`, `IEX`, `DownloadString`, `-w hidden` |

## Dependencies
```
pip install elasticsearch>=8.0 python-evtx
```

---

## Standards and Controls

## MITRE ATT&CK Mappings

### Primary Techniques
- **T1218 - Signed Binary Proxy Execution**: Use of trusted binaries to proxy execution of malicious payloads
  - T1218.001 - Compiled HTML File
  - T1218.002 - Control Panel
  - T1218.003 - CMSTP
  - T1218.004 - InstallUtil
  - T1218.005 - Mshta
  - T1218.007 - Msiexec
  - T1218.009 - Regsvcs/Regasm
  - T1218.010 - Regsvr32
  - T1218.011 - Rundll32
  - T1218.012 - Verclsid
  - T1218.013 - Mavinject
  - T1218.014 - MMC

### Supporting Techniques
- **T1197 - BITS Jobs**: Abuse of Background Intelligent Transfer Service
- **T1140 - Deobfuscate/Decode Files or Information**: certutil decode operations
- **T1059.001 - PowerShell**: Script execution through PowerShell LOLBin
- **T1047 - Windows Management Instrumentation**: WMIC-based execution
- **T1216 - Signed Script Proxy Execution**: Trusted script execution (cscript, wscript)
- **T1127 - Trusted Developer Utilities Proxy Execution**: MSBuild, dnx, rcsi

### Tactics Covered
- **TA0002 - Execution**: LOLBins used to execute malicious code
- **TA0005 - Defense Evasion**: Bypassing security controls through trusted binaries
- **TA0003 - Persistence**: Some LOLBins used for persistent execution

## LOLBAS Project Reference

The LOLBAS (Living Off The Land Binaries, Scripts, and Libraries) Project maintains a comprehensive catalog:
- Website: https://lolbas-project.github.io/
- GitHub: https://github.com/LOLBAS-Project/LOLBAS

### High-Priority LOLBins for Hunting

| Binary | ATT&CK ID | Capabilities |
|--------|-----------|-------------|
| certutil.exe | T1140 | Download, encode/decode, ADS |
| mshta.exe | T1218.005 | Execute HTA/VBS, download |
| rundll32.exe | T1218.011 | Execute DLL exports, proxy load |
| regsvr32.exe | T1218.010 | Execute COM scriptlets remotely |
| msiexec.exe | T1218.007 | Install remote MSI packages |
| cmstp.exe | T1218.003 | Execute INF SCT files |
| wmic.exe | T1047 | Remote command execution |
| bitsadmin.exe | T1197 | File transfer, persistence |
| msbuild.exe | T1127.001 | Compile and execute inline tasks |
| installutil.exe | T1218.004 | Execute managed code |
| cscript.exe | T1059.005 | Script execution |
| wscript.exe | T1059.005 | Script execution |
| forfiles.exe | T1202 | Indirect command execution |
| pcalua.exe | T1202 | Program compatibility execution |

## Threat Intelligence References

- CISA Alert AA23-136A: LOLBin abuse in Volt Typhoon campaigns
- Symantec: Living off the Land Techniques in Targeted Attacks
- Microsoft Threat Intelligence: Nation-state LOLBin campaigns
- Red Canary Threat Detection Report: Annual LOLBin detection trends

## Detection Data Sources

| Data Source | Event IDs | Content |
|-------------|----------|---------|
| Sysmon | 1 | Process creation with command line |
| Sysmon | 3 | Network connection from LOLBin |
| Sysmon | 7 | Image loaded (DLL loads) |
| Sysmon | 11 | File creation by LOLBin |
| Windows Security | 4688 | Process creation (enhanced) |
| Windows PowerShell | 4103, 4104 | Script block logging |
| Firewall/Proxy | - | Outbound connections from LOLBins |

---

## Workflows

## Phase 1: Intelligence Gathering

### Step 1.1 - Review Current Threat Landscape
- Check LOLBAS Project for newly added binaries
- Review threat intel feeds for active campaigns abusing LOLBins
- Correlate with CISA advisories and vendor threat reports
- Identify LOLBins relevant to your environment's OS versions

### Step 1.2 - Prioritize Target LOLBins
- Rank LOLBins by prevalence in current threat campaigns
- Consider which LOLBins have no existing detection rules
- Focus on LOLBins with download, execute, and encode capabilities
- Map to MITRE ATT&CK navigator for coverage gaps

## Phase 2: Data Collection

### Step 2.1 - Sysmon Process Creation Query (Event ID 1)
```
EventID=1 AND (
  Image CONTAINS "certutil.exe" OR
  Image CONTAINS "mshta.exe" OR
  Image CONTAINS "rundll32.exe" OR
  Image CONTAINS "regsvr32.exe" OR
  Image CONTAINS "msiexec.exe" OR
  Image CONTAINS "cmstp.exe" OR
  Image CONTAINS "wmic.exe" OR
  Image CONTAINS "bitsadmin.exe" OR
  Image CONTAINS "msbuild.exe"
)
```

### Step 2.2 - Splunk SPL Query for LOLBin Network Activity
```spl
index=sysmon EventCode=3
| where match(Image, "(?i)(certutil|mshta|rundll32|regsvr32|msiexec|bitsadmin)\.exe$")
| stats count by Image, DestinationIp, DestinationPort, User
| where DestinationIp!="10.*" AND DestinationIp!="172.16.*" AND DestinationIp!="192.168.*"
| sort -count
```

### Step 2.3 - KQL Query for Microsoft Defender for Endpoint
```kql
DeviceProcessEvents
| where Timestamp > ago(7d)
| where FileName in~ ("certutil.exe","mshta.exe","rundll32.exe","regsvr32.exe","bitsadmin.exe","cmstp.exe")
| where ProcessCommandLine has_any ("http","ftp","urlcache","-decode","/i:","scrobj.dll","-enc")
| project Timestamp, DeviceName, AccountName, FileName, ProcessCommandLine, InitiatingProcessFileName
| order by Timestamp desc
```

## Phase 3: Baseline Analysis

### Step 3.1 - Establish Normal Usage Patterns
- Count daily executions per LOLBin per endpoint
- Document standard parent processes (explorer.exe -> certutil.exe for IT admin)
- Record typical command-line arguments for legitimate use
- Note time-of-day patterns (business hours vs. off-hours)

### Step 3.2 - Build Frequency Analysis
```spl
index=sysmon EventCode=1
| where match(Image, "(?i)(certutil|mshta|rundll32)\.exe$")
| timechart span=1h count by Image
| eventstats avg(certutil.exe) as avg_certutil, stdev(certutil.exe) as stdev_certutil
| where certutil.exe > (avg_certutil + 3*stdev_certutil)
```

## Phase 4: Anomaly Detection

### Step 4.1 - Suspicious Command-Line Indicators
| LOLBin | Suspicious Argument | Reason |
|--------|---------------------|--------|
| certutil.exe | `-urlcache -split -f` | Remote file download |
| certutil.exe | `-encode` / `-decode` | Data encoding/obfuscation |
| mshta.exe | `javascript:` or `vbscript:` | Inline script execution |
| regsvr32.exe | `/s /n /u /i:http` | Remote SCT execution (Squiblydoo) |
| rundll32.exe | `javascript:` | Script execution proxy |
| bitsadmin.exe | `/transfer` with URL | File download |
| msiexec.exe | `/q /i http://` | Silent remote MSI install |
| cmstp.exe | `/s /ns` with INF file | UAC bypass |

### Step 4.2 - Anomalous Parent-Child Relationships
Flag when these parent processes spawn LOLBins:
- `winword.exe` -> `certutil.exe` (document downloading payload)
- `outlook.exe` -> `mshta.exe` (email launching HTA)
- `wmiprvse.exe` -> `rundll32.exe` (WMI lateral movement)
- `svchost.exe` -> `regsvr32.exe` (service spawning proxy execution)

## Phase 5: Correlation and Enrichment

### Step 5.1 - Network Correlation
- Match LOLBin network connections to threat intel domain/IP lists
- Check destination IPs against VirusTotal, AbuseIPDB
- Verify if domains are newly registered (DGA detection)
- Correlate with DNS query logs for suspicious resolutions

### Step 5.2 - File Activity Correlation
- Track files created by LOLBin processes
- Check file hashes against threat intel feeds
- Monitor for files written to unusual directories (Temp, AppData, ProgramData)
- Look for ADS (Alternate Data Streams) usage

## Phase 6: Documentation and Response

### Step 6.1 - Document Findings
- Record all true positive findings with evidence
- Document false positive patterns for tuning
- Update detection analytics with new signatures
- Create IOC lists for identified threats

### Step 6.2 - Update Detection Coverage
- Write or update Sigma rules for identified patterns
- Deploy new EDR detection rules
- Update SIEM correlation rules
- Add findings to MITRE ATT&CK Navigator heatmap

---

## Working Template

## Hunt Metadata

| Field | Value |
|-------|-------|
| Hunt ID | TH-LOLBIN-YYYY-MM-DD-NNN |
| Analyst | |
| Date Started | |
| Date Completed | |
| Status | [ ] In Progress / [ ] Complete |
| Priority | [ ] Critical / [ ] High / [ ] Medium / [ ] Low |

## Hypothesis

> **Hypothesis Statement**: [e.g., "Adversaries are using certutil.exe to download second-stage payloads from external infrastructure, bypassing web proxy controls."]

**Basis for Hypothesis**:
- [ ] Threat Intelligence Report: [Reference]
- [ ] Previous Incident Finding
- [ ] MITRE ATT&CK Gap Analysis
- [ ] Red Team Exercise Result
- [ ] Anomaly in Monitoring Data

## Scope

**Target LOLBins**:
- [ ] certutil.exe (T1140)
- [ ] mshta.exe (T1218.005)
- [ ] rundll32.exe (T1218.011)
- [ ] regsvr32.exe (T1218.010)
- [ ] msiexec.exe (T1218.007)
- [ ] bitsadmin.exe (T1197)
- [ ] cmstp.exe (T1218.003)
- [ ] wmic.exe (T1047)
- [ ] msbuild.exe (T1127.001)
- [ ] installutil.exe (T1218.004)
- [ ] forfiles.exe (T1202)
- [ ] Other: _______________

**Time Range**: [Start Date/Time] to [End Date/Time]
**Endpoints in Scope**: [All / Specific OUs / High-Value Targets]
**Data Sources Used**:
- [ ] Sysmon Event ID 1 (Process Creation)
- [ ] Sysmon Event ID 3 (Network Connection)
- [ ] Sysmon Event ID 7 (Image Loaded)
- [ ] Sysmon Event ID 11 (File Create)
- [ ] Windows Security 4688
- [ ] EDR Telemetry: _______________
- [ ] Network Proxy Logs
- [ ] DNS Query Logs
- [ ] Firewall Logs

## Queries Executed

### Query 1: [Description]
```
[Query text]
```
**Results**: [Count] events returned
**Time to Execute**: [Duration]

### Query 2: [Description]
```
[Query text]
```
**Results**: [Count] events returned
**Time to Execute**: [Duration]

## Findings

### Finding 1
| Attribute | Details |
|-----------|---------|
| Severity | [ ] Critical / [ ] High / [ ] Medium / [ ] Low |
| LOLBin | |
| MITRE ATT&CK | |
| Host(s) | |
| User(s) | |
| Command Line | |
| Parent Process | |
| Network IOCs | |
| File IOCs | |
| Timestamp | |
| Evidence | |

**Analysis**: [Detailed description of finding]
**Verdict**: [ ] True Positive / [ ] False Positive / [ ] Benign True Positive

### Finding 2
| Attribute | Details |
|-----------|---------|
| Severity | |
| LOLBin | |
| MITRE ATT&CK | |
| Host(s) | |
| User(s) | |
| Command Line | |
| Parent Process | |
| Network IOCs | |
| File IOCs | |
| Timestamp | |
| Evidence | |

**Analysis**: [Detailed description]
**Verdict**: [ ] True Positive / [ ] False Positive / [ ] Benign True Positive

## IOC List

### Network IOCs
| Type | Value | Context |
|------|-------|---------|
| IP | | |
| Domain | | |
| URL | | |

### File IOCs
| Type | Value | Context |
|------|-------|---------|
| SHA256 | | |
| Filename | | |
| File Path | | |

### Behavioral IOCs
| LOLBin | Argument Pattern | Parent Process |
|--------|-----------------|----------------|
| | | |

## Hunt Results Summary

| Metric | Count |
|--------|-------|
| Total Events Analyzed | |
| Anomalies Identified | |
| True Positives | |
| False Positives | |
| Benign True Positives | |
| New IOCs Discovered | |
| Detection Rules Created | |
| Detection Rules Updated | |

## Recommendations

1. **Detection Improvements**: [New rules or tuning needed]
2. **Visibility Gaps**: [Missing data sources or coverage]
3. **Response Actions**: [Incidents to escalate, containment needed]
4. **Follow-up Hunts**: [Related hypotheses to investigate next]

## Hypothesis Outcome

- [ ] **Confirmed**: Evidence found supporting the hypothesis
- [ ] **Partially Confirmed**: Some evidence found, requires further investigation
- [ ] **Refuted**: No evidence found, hypothesis disproven
- [ ] **Inconclusive**: Insufficient data to confirm or refute
