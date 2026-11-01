# Detecting T1548 Abuse Elevation Control Mechanism

## API Reference

## MITRE ATT&CK T1548 Sub-Techniques

| Sub-technique | Name | Platform |
|---------------|------|----------|
| T1548.001 | Setuid and Setgid | Linux/macOS |
| T1548.002 | Bypass User Account Control | Windows |
| T1548.003 | Sudo and Sudo Caching | Linux/macOS |
| T1548.004 | Elevated Execution with Prompt | macOS |

## UAC Bypass — Auto-Elevate Binaries

### Known Auto-Elevate Targets
| Binary | Bypass Method |
|--------|---------------|
| `fodhelper.exe` | Registry key hijack |
| `computerdefaults.exe` | ms-settings handler |
| `eventvwr.exe` | mscfile handler |
| `sdclt.exe` | App paths hijack |
| `wsreset.exe` | Bypasses defender |
| `cmstp.exe` | INF file execution |

### Registry Keys for UAC Bypass
```
HKCU\Software\Classes\ms-settings\Shell\Open\command
HKCU\Software\Classes\mscfile\Shell\Open\command
```

## Windows UAC Configuration

### Check UAC Level
```powershell
Get-ItemProperty HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System
# EnableLUA = 1 (UAC enabled)
# ConsentPromptBehaviorAdmin = 0-5
```

### ConsentPromptBehaviorAdmin Values
| Value | Behavior |
|-------|----------|
| 0 | Elevate without prompting |
| 1 | Prompt for credentials on secure desktop |
| 2 | Prompt for consent on secure desktop |
| 5 | Prompt for consent (default) |

## Linux Privilege Escalation

### sudo Configuration Check
```bash
sudo -l                    # List allowed commands
cat /etc/sudoers           # Full sudoers file
visudo -c                  # Validate syntax
```

### Find SUID Binaries
```bash
find / -perm -4000 -type f 2>/dev/null
find / -perm -2000 -type f 2>/dev/null   # SGID
```

### GTFOBins Sudo Escapes
| Binary | Escape |
|--------|--------|
| `vim` | `sudo vim -c ':!/bin/bash'` |
| `find` | `sudo find . -exec /bin/bash \;` |
| `python` | `sudo python -c 'import os; os.system("/bin/bash")'` |
| `nmap` | `sudo nmap --interactive` (old versions) |

## Sysmon Detection Rules

### Event 13 — Registry Value Set
```xml
<RegistryEvent onmatch="include">
  <TargetObject condition="contains">ms-settings\Shell\Open\command</TargetObject>
  <TargetObject condition="contains">mscfile\Shell\Open\command</TargetObject>
</RegistryEvent>
```

## Sigma Rule — UAC Bypass
```yaml
title: UAC Bypass via Fodhelper
logsource:
    product: windows
    category: registry_set
detection:
    selection:
        TargetObject|contains: 'ms-settings\Shell\Open\command'
    condition: selection
level: critical
```

---

## Standards and Controls

## MITRE ATT&CK Sub-Techniques

| Sub-Technique | Platform | Description |
|--------------|----------|-------------|
| T1548.001 | Linux/macOS | Setuid and Setgid binary abuse |
| T1548.002 | Windows | Bypass User Account Control |
| T1548.003 | Linux/macOS | Sudo and Sudo Caching |
| T1548.004 | macOS | Elevated Execution with Prompt |

## Known UAC Bypass Methods (60+ documented)

| Method | Binary | Registry Key | Detection |
|--------|--------|-------------|-----------|
| fodhelper | fodhelper.exe | ms-settings\shell\open\command | Registry + process creation |
| eventvwr | eventvwr.exe | mscfile\shell\open\command | Registry + process creation |
| sdclt | sdclt.exe | exefile\shell\open\command | Registry + process creation |
| computerdefaults | computerdefaults.exe | ms-settings\shell\open\command | Registry + process creation |
| CMSTP | cmstp.exe | N/A (INF file) | Process creation with /s /ni |
| slui | slui.exe | exefile\shell\open\command | Registry + process creation |
| DiskCleanup | cleanmgr.exe | Environment variable hijack | Environment + process |

## UAC-Related Registry Keys to Monitor

| Registry Key | Purpose |
|-------------|---------|
| HKCU\Software\Classes\ms-settings\shell\open\command | fodhelper/computerdefaults bypass |
| HKCU\Software\Classes\mscfile\shell\open\command | eventvwr bypass |
| HKCU\Software\Classes\exefile\shell\open\command | sdclt/slui bypass |
| HKCU\Software\Classes\Folder\shell\open\command | Folder handler bypass |
| HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\EnableLUA | UAC disable |
| HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\ConsentPromptBehaviorAdmin | UAC level |

## Detection Events

| Source | Event ID | Description |
|--------|----------|-------------|
| Sysmon | 1 | Auto-elevate process creation |
| Sysmon | 12 | Registry key creation (UAC keys) |
| Sysmon | 13 | Registry value modification |
| Security | 4688 | Process creation with elevation |
| Security | 4657 | Registry value modification audit |

---

## Workflows

## Phase 1: Registry-Based UAC Bypass Detection

### Step 1.1 - Monitor UAC Registry Keys
```spl
index=sysmon (EventCode=12 OR EventCode=13)
| where match(TargetObject, "(?i)(ms-settings|mscfile|exefile|Folder)\\\\shell\\\\open\\\\command")
| table _time Computer User Image TargetObject Details EventCode
```

### Step 1.2 - Detect UAC Policy Changes
```spl
index=sysmon EventCode=13
| where match(TargetObject, "(?i)Policies\\\\System\\\\(EnableLUA|ConsentPromptBehaviorAdmin)")
| table _time Computer User Image TargetObject Details
```

## Phase 2: Auto-Elevating Process Chain Detection

### Step 2.1 - Suspicious Auto-Elevate Launches
```spl
index=sysmon EventCode=1
| where match(Image, "(?i)(fodhelper|computerdefaults|eventvwr|sdclt|slui)\.exe$")
| where NOT match(ParentImage, "(?i)(explorer\.exe|svchost\.exe)$")
| stats count by Image ParentImage Computer User
```

### Step 2.2 - Children of Auto-Elevate Processes
```spl
index=sysmon EventCode=1
| where match(ParentImage, "(?i)(fodhelper|computerdefaults|eventvwr|sdclt|slui)\.exe$")
| where match(Image, "(?i)(cmd|powershell|wscript|cscript|mshta)\.exe$")
| table _time Computer Image CommandLine ParentImage User
```

## Phase 3: Linux Elevation Abuse

### Step 3.1 - Setuid Binary Hunting
```bash
find / -perm -4000 -type f 2>/dev/null
find / -perm -2000 -type f 2>/dev/null
```

### Step 3.2 - Sudo Abuse Detection
```spl
index=linux sourcetype=syslog
| where match(_raw, "(?i)sudo.*COMMAND=")
| where NOT match(_raw, "(?i)(apt-get|yum|systemctl|service)")
| table _time host user command
```

## Phase 4: Response
1. Revert malicious registry modifications
2. Investigate what was executed with elevated privileges
3. Set UAC to highest level (Always Notify)
4. Deploy ASR rules against UAC bypasses
5. Monitor for repeated escalation attempts

---

## Working Template

## Hunt Metadata
| Field | Value |
|-------|-------|
| Hunt ID | TH-UAC-YYYY-MM-DD-NNN |
| Analyst | |
| Date | |
| Status | [ ] In Progress / [ ] Complete |

## Hypothesis
> Adversaries are bypassing User Account Control or other elevation mechanisms to gain administrative privileges without triggering user consent prompts.

## Registry Modification Findings

| # | Time | Host | Registry Key | Value Set | Modifying Process | Severity |
|---|------|------|-------------|-----------|-------------------|----------|
| 1 | | | | | | |

## Auto-Elevate Process Abuse

| # | Time | Host | Auto-Elevate Binary | Unexpected Parent | Child Process | Severity |
|---|------|------|--------------------|--------------------|---------------|----------|
| 1 | | | | | | |

## Recommendations
1. **Remediate**: [Revert registry modifications]
2. **Investigate**: [Actions taken with elevated privileges]
3. **Harden**: [Set UAC to Always Notify, deploy ASR rules]
4. **Monitor**: [Registry keys and auto-elevate process chains]
