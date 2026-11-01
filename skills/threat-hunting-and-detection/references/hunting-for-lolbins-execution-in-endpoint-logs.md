# Hunting For Lolbins Execution In Endpoint Logs

## API Reference

## Libraries Used
- **csv**: Parse exported endpoint log CSV files from SIEM or EDR
- **python-evtx** (Evtx): Parse Windows Sysmon EVTX event logs directly
- **re**: Regex matching for suspicious command-line patterns

## CLI Interface

```
python agent.py csv --file <csv_path> [--process-col Image] [--cmdline-col CommandLine]
python agent.py evtx --file <evtx_path>
```

## Core Functions

### `scan_csv_logs(csv_file, process_col, cmdline_col)`
Scans CSV-exported endpoint logs for LOLBin process executions with suspicious arguments.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `csv_file` | str | Path to CSV log file |
| `process_col` | str | Column name for process image path (default: `Image`) |
| `cmdline_col` | str | Column name for command line (default: `CommandLine`) |

**Returns:** dict with `total_findings`, `by_binary` counts, `by_mitre` counts, `findings` list.

### `scan_evtx_sysmon(evtx_file)`
Parses Sysmon EVTX logs for Event ID 1 (Process Creation) matching LOLBin signatures.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `evtx_file` | str | Path to Sysmon .evtx file |

**Returns:** dict with `total_findings` and `findings` with record IDs, binary names, MITRE IDs.

## LOLBins Detected (14 binaries)
certutil.exe, mshta.exe, regsvr32.exe, rundll32.exe, bitsadmin.exe, wmic.exe,
msiexec.exe, cmstp.exe, forfiles.exe, pcalua.exe, csc.exe, installutil.exe,
msbuild.exe, powershell.exe

## Output Format
```json
{
  "total_findings": 12,
  "by_binary": {"powershell.exe": 5, "certutil.exe": 4},
  "by_mitre": {"T1059.001": 5, "T1140": 4},
  "findings": [{"binary": "...", "mitre": "...", "command_line": "..."}]
}
```

## Dependencies
```
pip install python-evtx
```

---

## Standards and Controls

## MITRE ATT&CK LOLBin Techniques

| Technique | Binary | Abuse Pattern |
|-----------|--------|---------------|
| T1218.001 | Compiled HTML (hh.exe) | Execute payloads from CHM files |
| T1218.003 | CMSTP | UAC bypass and proxy execution |
| T1218.005 | Mshta | Execute HTA files with scripts |
| T1218.010 | Regsvr32 | Squiblydoo - remote SCT execution |
| T1218.011 | Rundll32 | Proxy execution of malicious DLLs |
| T1127.001 | MSBuild | Execute inline C#/VB tasks |
| T1197 | Bitsadmin | Stealthy file downloads via BITS |
| T1140 | Certutil | Download and decode files |
| T1059.001 | PowerShell | Script execution and download cradles |
| T1059.005 | Wscript/Cscript | VBScript/JScript execution |
| T1047 | WMIC | Remote execution and XSL script execution |
| T1053.005 | Schtasks | Scheduled task creation for persistence |

## Top 8 LOLBins by Threat Actor Usage (CrowdStrike Research)

| LOLBin | Common Abuse | Detection Priority |
|--------|-------------|-------------------|
| PowerShell.exe | Download cradles, encoded commands, AMSI bypass | Critical |
| Cmd.exe | Script execution, chaining with other LOLBins | Critical |
| Rundll32.exe | DLL proxy execution from user directories | Critical |
| Certutil.exe | File download (-urlcache), decode (-decode) | High |
| Mshta.exe | Remote HTA execution, inline scripts | High |
| Regsvr32.exe | SCT execution (Squiblydoo), COM object abuse | High |
| MSBuild.exe | Inline task execution bypassing AppLocker | High |
| WMIC.exe | Remote process creation, XSL execution | Medium |

## Suspicious Parent-Child Process Relationships

| Parent Process | Child LOLBin | Indicates |
|---------------|-------------|-----------|
| winword.exe | mshta.exe | Weaponized Office document |
| excel.exe | certutil.exe | Macro downloading payload |
| outlook.exe | powershell.exe | Phishing payload execution |
| wmiprvse.exe | cmd.exe | WMI-based lateral movement |
| explorer.exe | regsvr32.exe | User-triggered exploitation |
| svchost.exe | msbuild.exe | Service-based code execution |
| w3wp.exe | cmd.exe | Web shell activity |

## Sysmon Events for LOLBin Detection

| Event ID | Description | LOLBin Relevance |
|----------|-------------|-----------------|
| 1 | Process Creation | Primary detection - command line and parent process |
| 3 | Network Connection | LOLBin outbound connections (download/C2) |
| 7 | Image Loaded | DLLs loaded by LOLBins |
| 11 | File Created | Files dropped by LOLBin execution |
| 15 | FileCreateStreamHash | Alternate data stream creation |
| 22 | DNS Query | DNS resolution from LOLBin processes |

---

## Workflows

## Phase 1: Establish LOLBin Baseline

### Step 1.1 - Profile Normal LOLBin Usage
```spl
index=sysmon EventCode=1
| where match(Image, "(?i)(certutil|mshta|rundll32|regsvr32|msbuild|installutil|cmstp|bitsadmin|wmic)\.exe$")
| stats count by Image CommandLine ParentImage User Computer
| sort -count
```

### Step 1.2 - Identify Standard Parent-Child Relationships
```spl
index=sysmon EventCode=1
| where match(Image, "(?i)(certutil|mshta|rundll32|regsvr32)\.exe$")
| stats count by ParentImage Image
| sort -count
| head 50
```

## Phase 2: Hunt for Download Cradles

### Step 2.1 - Certutil Download Detection
```spl
index=sysmon EventCode=1 Image="*\\certutil.exe"
| where match(CommandLine, "(?i)(-urlcache|-decode|-encode|-verifyctl)")
| table _time Computer User Image CommandLine ParentImage
```

### Step 2.2 - Bitsadmin Transfer Detection
```spl
index=sysmon EventCode=1 Image="*\\bitsadmin.exe"
| where match(CommandLine, "(?i)(/transfer|/create|/addfile|/resume)")
| table _time Computer User CommandLine ParentImage
```

### Step 2.3 - PowerShell Download Cradles
```spl
index=sysmon EventCode=1 Image="*\\powershell.exe"
| where match(CommandLine, "(?i)(DownloadString|DownloadFile|DownloadData|Invoke-WebRequest|iwr|wget|curl|Start-BitsTransfer|Net\.WebClient)")
| table _time Computer User CommandLine ParentImage
```

## Phase 3: Hunt for Proxy Execution

### Step 3.1 - Regsvr32 Squiblydoo
```spl
index=sysmon EventCode=1 Image="*\\regsvr32.exe"
| where match(CommandLine, "(?i)(/s.*(/n|/i:))|scrobj\.dll|http")
| table _time Computer User CommandLine ParentImage
```

### Step 3.2 - MSBuild Inline Task Execution
```spl
index=sysmon EventCode=1 Image="*\\MSBuild.exe"
| where NOT match(ParentImage, "(?i)(devenv|msbuild|visual studio)")
| where match(CommandLine, "(?i)\\\\(temp|appdata|users|public)")
| table _time Computer User CommandLine ParentImage
```

### Step 3.3 - Mshta Remote Execution
```spl
index=sysmon EventCode=1 Image="*\\mshta.exe"
| where match(CommandLine, "(?i)(http|https|javascript|vbscript)")
| table _time Computer User CommandLine ParentImage
```

## Phase 4: Hunt for Unusual Parent Processes

### Step 4.1 - Office Applications Spawning LOLBins
```spl
index=sysmon EventCode=1
| where match(ParentImage, "(?i)(winword|excel|powerpnt|outlook|onenote)\.exe$")
| where match(Image, "(?i)(cmd|powershell|certutil|mshta|rundll32|regsvr32|wscript|cscript)\.exe$")
| table _time Computer User ParentImage Image CommandLine
```

### Step 4.2 - Web Server Spawning System Binaries
```spl
index=sysmon EventCode=1
| where match(ParentImage, "(?i)(w3wp|httpd|nginx|tomcat)\.exe$")
| where match(Image, "(?i)(cmd|powershell|certutil|whoami|net|net1|nltest)\.exe$")
| table _time Computer User ParentImage Image CommandLine
```

## Phase 5: Correlate with Network Activity

### Step 5.1 - LOLBin Network Connections
```spl
index=sysmon EventCode=3
| where match(Image, "(?i)(certutil|mshta|rundll32|regsvr32|msbuild|bitsadmin|wscript)\.exe$")
| where NOT cidrmatch("10.0.0.0/8", DestinationIp)
| table _time Computer Image DestinationIp DestinationPort DestinationHostname
```

## Phase 6: Response Actions

1. Block identified malicious URLs and IPs at proxy/firewall
2. Isolate endpoint if active compromise confirmed
3. Collect process memory dump for malware analysis
4. Deploy targeted detection rules for observed patterns
5. Update application control policies to restrict LOLBin abuse

---

## Working Template

## Hunt Metadata
| Field | Value |
|-------|-------|
| Hunt ID | TH-LOLBIN-YYYY-MM-DD-NNN |
| Analyst | |
| Date | |
| Status | [ ] In Progress / [ ] Complete |

## Hypothesis
> Adversaries are abusing legitimate Windows system binaries to execute malicious payloads, download tools, or bypass application control in the environment.

## LOLBin Findings

| # | Timestamp | Host | User | LOLBin | Command Line | Parent Process | Category | Severity |
|---|-----------|------|------|--------|-------------|----------------|----------|----------|
| 1 | | | | | | | | |

## Suspicious Parent-Child Relationships

| Parent Process | Child LOLBin | Host | User | Assessment |
|---------------|-------------|------|------|------------|
| | | | | |

## Network Activity from LOLBins

| LOLBin | Host | Destination IP | Destination Port | Domain | Assessment |
|--------|------|---------------|-----------------|--------|------------|
| | | | | | |

## Recommendations
1. **Block**: [URLs/IPs contacted by LOLBins]
2. **Detect**: [New detection rules for observed patterns]
3. **Harden**: [Application control policy updates]
4. **Investigate**: [Endpoints requiring forensic analysis]
