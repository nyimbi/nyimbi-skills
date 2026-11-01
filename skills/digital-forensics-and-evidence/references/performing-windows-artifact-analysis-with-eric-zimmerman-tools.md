# Performing Windows Artifact Analysis With Eric Zimmerman Tools

## API Reference

## EZ Tools Suite

| Tool | Artifact | Description |
|------|----------|-------------|
| `MFTECmd.exe` | $MFT | Parse Master File Table |
| `PECmd.exe` | Prefetch | Parse prefetch files for execution history |
| `LECmd.exe` | LNK | Parse shortcut files |
| `JLECmd.exe` | Jump Lists | Parse automatic/custom jump lists |
| `SBECmd.exe` | ShellBags | Parse folder access history from registry |
| `AmcacheParser.exe` | Amcache | Parse application execution evidence |
| `AppCompatCacheParser.exe` | Shimcache | Parse application compatibility cache |
| `EvtxECmd.exe` | EVTX | Parse Windows event logs |
| `RECmd.exe` | Registry | Parse registry hives |

## Common CLI Flags

| Flag | Description |
|------|-------------|
| `-f <file>` | Input file path |
| `-d <directory>` | Input directory |
| `--csv <dir>` | Output directory for CSV |
| `--csvf <file>` | CSV output filename |
| `--json <dir>` | Output directory for JSON |
| `--body <dir>` | Output bodyfile for timeline |

## Key Artifacts and Locations

| Artifact | Path | Evidence |
|----------|------|----------|
| $MFT | `C:\$MFT` | File creation/modification/access |
| Prefetch | `C:\Windows\Prefetch\` | Program execution with timestamps |
| LNK Files | `%APPDATA%\Microsoft\Windows\Recent\` | Recently accessed files |
| Jump Lists | `%APPDATA%\Microsoft\Windows\Recent\AutomaticDestinations\` | Per-app recent files |
| ShellBags | NTUSER.DAT, UsrClass.dat | Folder browsing history |
| Amcache | `C:\Windows\AppCompat\Programs\Amcache.hve` | Application execution |

## Python Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| `subprocess` | stdlib | Execute EZ tools |
| `csv` | stdlib | Parse CSV output |
| `json` | stdlib | Report generation |

## References

- Eric Zimmerman Tools: https://ericzimmerman.github.io/
- SANS Windows Forensic Analysis Poster: https://www.sans.org/posters/windows-forensic-analysis/
- EZ Tools GitHub: https://github.com/EricZimmerman

---

## Standards and Controls

## Industry Standards

### NIST SP 800-86 - Guide to Integrating Forensic Techniques
- Framework for collecting, examining, and analyzing digital evidence
- Defines procedures for forensic acquisition and chain of custody
- EZ Tools align with NIST evidence handling and analysis guidelines

### ISO/IEC 27037 - Digital Evidence Collection
- International standard for identification, collection, acquisition, and preservation
- KAPE collection follows ISO 27037 acquisition methodology
- Timeline Explorer output supports ISO-compliant reporting

### SWGDE Best Practices for Computer Forensics
- Scientific Working Group on Digital Evidence guidelines
- Defines validation requirements for forensic tools
- EZ Tools undergo community-driven validation testing

## Tool References

### EZ Tools Suite Components
| Tool | Version | Purpose |
|------|---------|---------|
| KAPE | 1.3+ | Artifact collection and processing orchestration |
| MFTECmd | 1.2+ | NTFS Master File Table parser |
| PECmd | 1.5+ | Windows Prefetch file parser |
| RECmd | 2.0+ | Registry hive parser with batch processing |
| EvtxECmd | 1.5+ | Windows Event Log parser with maps |
| LECmd | 1.5+ | LNK shortcut file parser |
| JLECmd | 1.5+ | Jump List parser |
| SBECmd | 2.0+ | Shellbag parser |
| Timeline Explorer | 2.0+ | CSV analysis and visualization |
| Registry Explorer | 2.0+ | GUI registry hive viewer |
| ShellBags Explorer | 2.0+ | GUI shellbag viewer |
| AmcacheParser | 1.5+ | Amcache.hve parser |
| AppCompatCacheParser | 1.5+ | ShimCache parser |
| WxTCmd | 1.0+ | Windows Timeline database parser |
| RBCmd | 1.5+ | Recycle Bin artifact parser |
| bstrings | 1.5+ | Binary string extraction |

### SANS Training Courses
- FOR500: Windows Forensic Analysis
- FOR508: Advanced Incident Response, Threat Hunting, and Digital Forensics
- FOR498: Battlefield Forensics & Data Acquisition
- FOR610: Reverse-Engineering Malware

### MITRE ATT&CK Relevance
- T1070 - Indicator Removal: Timestomping detection via MFT analysis
- T1547 - Boot or Logon Autostart Execution: Registry persistence detection
- T1053 - Scheduled Task/Job: Task scheduler artifact analysis
- T1059 - Command and Scripting Interpreter: Prefetch execution evidence
- T1021 - Remote Services: Lateral movement via event log analysis

## Official Resources
- Eric Zimmerman's GitHub: https://ericzimmerman.github.io/
- KAPE GitHub Targets/Modules: https://github.com/EricZimmerman/KapeFiles
- EZ Tools Changelog: https://ericzimmerman.github.io/#!index.md
- SANS DFIR Blog: https://www.sans.org/blog/?focus-area=digital-forensics

---

## Workflows

## Workflow 1: Full Triage Collection and Processing

```
Step 1: Mount forensic image as read-only drive (E:)
    |
Step 2: Run KAPE with KapeTriage target
    |-- Collects: $MFT, $J, Registry, Event Logs, Prefetch, LNK, Jump Lists
    |
Step 3: Run KAPE with !EZParser module
    |-- Processes all collected artifacts with appropriate EZ Tools
    |
Step 4: Open CSV outputs in Timeline Explorer
    |-- Sort by timestamp, filter by artifact type
    |
Step 5: Build investigation timeline
    |-- Cross-reference MFT, Event Logs, Prefetch, Registry
    |
Step 6: Document findings and export filtered results
```

## Workflow 2: Timestomping Detection

```
Step 1: Parse $MFT with MFTECmd
    |
Step 2: Open MFT CSV in Timeline Explorer
    |
Step 3: Compare $SI timestamps (Created0x10) vs $FN timestamps (Created0x30)
    |-- Flag entries where Created0x10 < Created0x30
    |-- Flag entries where all four $SI timestamps are identical
    |
Step 4: Cross-reference flagged files with USN Journal entries
    |
Step 5: Verify with event log correlation (process creation, file access)
```

## Workflow 3: Program Execution Timeline

```
Step 1: Parse Prefetch with PECmd
    |
Step 2: Parse Amcache.hve with AmcacheParser
    |
Step 3: Parse ShimCache with AppCompatCacheParser
    |
Step 4: Parse UserAssist from NTUSER.DAT with RECmd
    |
Step 5: Merge and correlate execution timestamps
    |-- Prefetch: Run count + last 8 execution times
    |-- Amcache: First execution + SHA1 hash
    |-- ShimCache: Last modified time (execution indicator)
    |-- UserAssist: GUI program execution tracking
    |
Step 6: Build execution timeline in Timeline Explorer
```

## Workflow 4: Lateral Movement Investigation

```
Step 1: Parse Security.evtx with EvtxECmd
    |-- Filter Event ID 4624 (Logon Type 3, 10)
    |-- Filter Event ID 4625 (Failed logons)
    |
Step 2: Parse TerminalServices event logs
    |-- Microsoft-Windows-TerminalServices-LocalSessionManager
    |-- Microsoft-Windows-TerminalServices-RDPClient
    |
Step 3: Correlate with registry RDP MRU entries
    |-- NTUSER.DAT\Software\Microsoft\Terminal Server Client\Servers
    |
Step 4: Analyze LNK files for network path access
    |
Step 5: Review scheduled task creation from event logs
    |
Step 6: Map lateral movement path across systems
```

## Workflow 5: USB Device Investigation

```
Step 1: Parse SYSTEM hive with RECmd
    |-- SYSTEM\CurrentControlSet\Enum\USBSTOR
    |-- SYSTEM\CurrentControlSet\Enum\USB
    |-- SYSTEM\MountedDevices
    |
Step 2: Parse NTUSER.DAT with RECmd
    |-- MountPoints2 for user-level device associations
    |
Step 3: Parse setupapi.dev.log for device installation timestamps
    |
Step 4: Analyze LNK files referencing removable drive letters
    |
Step 5: Check Shellbags for folder browsing on USB devices
    |
Step 6: Correlate with Event Logs (Microsoft-Windows-Partition/Diagnostic)
```

---

## Working Template

## Case Information

| Field | Value |
|-------|-------|
| Case Number | |
| Examiner | |
| Date of Analysis | |
| Evidence Source | |
| Evidence Hash (SHA-256) | |
| EZ Tools Version | |

## Artifacts Processed

| Artifact | Tool Used | Status | Records Parsed |
|----------|-----------|--------|----------------|
| $MFT | MFTECmd | | |
| $J (USN Journal) | MFTECmd | | |
| Prefetch Files | PECmd | | |
| LNK Files | LECmd | | |
| Jump Lists | JLECmd | | |
| Event Logs | EvtxECmd | | |
| Registry Hives | RECmd | | |
| Shellbags | SBECmd | | |
| Recycle Bin | RBCmd | | |
| Amcache | AmcacheParser | | |
| ShimCache | AppCompatCacheParser | | |

## Key Findings

### Program Execution Evidence
| Executable | First Execution | Last Execution | Run Count | Source |
|-----------|----------------|---------------|-----------|--------|
| | | | | |

### Timestomping Indicators
| File | $SI Created | $FN Created | Anomaly |
|------|------------|------------|---------|
| | | | |

### User Activity Timeline
| Timestamp | Activity | Artifact Source | Details |
|-----------|----------|----------------|---------|
| | | | |

### Lateral Movement Indicators
| Timestamp | Source IP | Target System | Logon Type | Event ID |
|-----------|----------|--------------|------------|----------|
| | | | | |

### USB Device Connections
| Device | Serial Number | First Connected | Last Connected | Volume Name |
|--------|--------------|----------------|---------------|-------------|
| | | | | |

## Conclusion

_(Summary of findings based on artifact analysis)_

## Chain of Custody

| Date/Time | Action | Performed By | Notes |
|-----------|--------|-------------|-------|
| | | | |
