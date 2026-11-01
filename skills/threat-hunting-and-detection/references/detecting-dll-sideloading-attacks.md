# Detecting Dll Sideloading Attacks

## API Reference

## Sysmon Event ID 7 (Image Loaded)

```xml
<EventID>7</EventID>
<Data Name="Image">C:\Users\victim\app\signed.exe</Data>
<Data Name="ImageLoaded">C:\Users\victim\app\malicious.dll</Data>
<Data Name="Signed">false</Data>
<Data Name="SignatureStatus">Unavailable</Data>
<Data Name="Hashes">SHA256=abc123...</Data>
```

## python-evtx Usage

```python
import Evtx.Evtx as evtx
with evtx.Evtx("Sysmon.evtx") as log:
    for record in log.records():
        xml = record.xml()
        # Filter EventID 7, check Signed=false, non-standard path
```

## Known Sideloading Targets

| Legitimate Executable | Vulnerable DLL |
|----------------------|----------------|
| vmwaretray.exe | vmtools.dll |
| colorcpl.exe | colorui.dll |
| consent.exe | comctl32.dll |
| bginfo.exe | version.dll |
| teams.exe | version.dll |
| winword.exe | wwlib.dll |

## Splunk SPL Detection

```spl
index=sysmon EventCode=7 Signed=false
| where NOT match(ImageLoaded, "(?i)(System32|SysWOW64|Program Files)")
| stats count by Image, ImageLoaded, SignatureStatus, Computer
| where count > 0
```

## Sigma Rule Fields

```yaml
logsource:
  product: windows
  category: image_load
detection:
  selection:
    EventID: 7
    Signed: "false"
  filter:
    ImageLoaded|startswith:
      - "C:\\Windows\\System32\\"
      - "C:\\Program Files\\"
```

## CLI Usage

```bash
python agent.py --sysmon-log Sysmon.evtx
python agent.py --scan-dir C:\Users\victim\Downloads\app\
python agent.py --generate-sigma
```

---

## Standards and Controls

## MITRE ATT&CK Mappings

### T1574.002 - Hijack Execution Flow: DLL Side-Loading
- **Tactic**: Persistence (TA0003), Privilege Escalation (TA0004), Defense Evasion (TA0005)
- **Platforms**: Windows
- **Data Sources**: File monitoring, DLL monitoring, Process monitoring

### Related Techniques
| Technique | Name |
|-----------|------|
| T1574.001 | DLL Search Order Hijacking |
| T1574.006 | Dynamic Linker Hijacking |
| T1574.008 | Path Interception by Search Order |
| T1574.009 | Path Interception by Unquoted Service Path |
| T1574.011 | Services Registry Permissions Weakness |
| T1574.012 | COR_PROFILER |

## Windows DLL Search Order

1. Directory of the executable (or directory specified by SetDllDirectory)
2. System32 directory
3. 16-bit system directory
4. Windows directory
5. Current working directory
6. PATH environment variable directories

## Known Vulnerable Applications

| Application | Vulnerable DLL | Vendor | Notes |
|-------------|---------------|--------|-------|
| OneDriveUpdater.exe | version.dll | Microsoft | Frequently abused by APTs |
| Teams.exe | CRYPTSP.dll | Microsoft | Side-loading target |
| DismHost.exe | dismcore.dll | Microsoft | Signed binary side-loading |
| MpCmdRun.exe | mpclient.dll | Microsoft | AV binary abuse |
| WerFault.exe | dbgcore.dll | Microsoft | Error handler abuse |
| Grammarly | Various | Grammarly | User-space application |
| Zoom | Various | Zoom | Meeting application |

## Detection Data Sources

| Source | Event | Purpose |
|--------|-------|---------|
| Sysmon Event 7 | Image Loaded | DLL load with hash and signature |
| Sysmon Event 1 | Process Create | Application launch location |
| Windows Security 4688 | Process Create | Command line monitoring |
| ETW | DLL Load Events | Kernel-level DLL tracking |
| MDE | DeviceImageLoadEvents | DLL load telemetry |

---

## Workflows

## Phase 1: Sysmon DLL Load Analysis

### Step 1.1 - Unsigned DLLs Loaded by Signed Applications
```spl
index=sysmon EventCode=7 Signed=false
| where match(Image, "(?i)\\\\(Program Files|Windows)\\\\")
| where NOT match(ImageLoaded, "(?i)\\\\(Windows|Program Files)\\\\")
| stats count by Image ImageLoaded Signature Computer
| sort -count
```

### Step 1.2 - DLL Loads from Unusual Directories
```spl
index=sysmon EventCode=7
| where match(ImageLoaded, "(?i)(\\\\temp\\\\|\\\\appdata\\\\|\\\\public\\\\|\\\\downloads\\\\)")
| where Signed=false OR Signature="?"
| stats count by Image ImageLoaded Computer User
| sort -count
```

### Step 1.3 - KQL for MDE DLL Sideloading
```kql
DeviceImageLoadEvents
| where Timestamp > ago(7d)
| where InitiatingProcessFileName in~ ("OneDriveUpdater.exe","DismHost.exe","WerFault.exe")
| where not(FolderPath startswith "C:\\Windows" or FolderPath startswith "C:\\Program Files")
| project Timestamp, DeviceName, InitiatingProcessFileName, FolderPath, FileName, SHA256
```

## Phase 2: Legitimate App in Wrong Location

### Step 2.1 - Signed Binaries Running Outside Standard Paths
```spl
index=sysmon EventCode=1
| where NOT match(Image, "(?i)^(C:\\\\Windows|C:\\\\Program Files)")
| where match(Image, "(?i)(svchost|explorer|rundll32|dllhost|OneDrive|Teams)\.exe$")
| table _time Computer User Image CommandLine ParentImage Hashes
```

## Phase 3: Hash-Based Detection

### Step 3.1 - Known-Bad DLL Hashes
Compare loaded DLL hashes against threat intelligence:
```spl
index=sysmon EventCode=7
| rex field=Hashes "SHA256=(?<sha256>[A-Fa-f0-9]{64})"
| lookup threat_intel_hashes sha256 OUTPUT malware_family confidence
| where isnotnull(malware_family)
| table _time Computer Image ImageLoaded sha256 malware_family
```

## Phase 4: Behavioral Correlation

### Step 4.1 - Network Activity After DLL Load
Correlate DLL loads with subsequent network connections:
```spl
index=sysmon EventCode=7 Signed=false
| rename Image as proc_image
| join proc_image Computer [
    search index=sysmon EventCode=3
    | rename Image as proc_image
    | where NOT match(DestinationIp, "^(10\.|172\.|192\.168\.)")
]
| table _time Computer proc_image ImageLoaded DestinationIp DestinationPort
```

---

## Working Template

## Hunt Metadata
| Field | Value |
|-------|-------|
| Hunt ID | TH-SIDELOAD-YYYY-MM-DD-NNN |
| Analyst | |
| Date | |

## Hypothesis
> [e.g., "Adversaries are using DLL sideloading with legitimate signed applications to execute malicious payloads while evading detection."]

## Findings
| # | Host | Application | Sideloaded DLL | DLL Path | Signed | Risk | Verdict |
|---|------|------------|---------------|----------|--------|------|---------|
| 1 | | | | | | | |

## Recommendations
1. **Block**: [Quarantine malicious DLLs]
2. **Harden**: [Application directory permissions, DLL safe search mode]
3. **Detect**: [Sysmon Event ID 7 rules for known targets]
