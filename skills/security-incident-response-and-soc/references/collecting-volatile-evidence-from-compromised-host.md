# Collecting Volatile Evidence From Compromised Host

## API Reference

## RFC 3227 Order of Volatility
| Priority | Source | Persistence |
|----------|--------|------------|
| 1 | CPU registers, cache | Nanoseconds |
| 2 | Physical memory (RAM) | Power cycle |
| 3 | Network state | Seconds-minutes |
| 4 | Running processes | Minutes |
| 5 | Disk (filesystem) | Persistent |
| 6 | Remote logging / monitoring | Persistent |
| 7 | Physical configuration | Persistent |
| 8 | Archival media | Long-term |

## Memory Acquisition Tools
| Tool | Platform | Command |
|------|----------|---------|
| AVML | Linux | `avml /path/to/output.lime` |
| WinPmem | Windows | `winpmem_mini_x64.exe output.raw` |
| LiME | Linux | `insmod lime.ko "path=/tmp/mem.lime format=lime"` |
| Magnet RAM Capture | Windows | GUI-based acquisition |

## Linux Collection Commands
```bash
# Network connections
ss -tunap > /evidence/netstat.txt

# Process list with tree
ps auxwwf > /evidence/processes.txt

# Open files
lsof -nP > /evidence/open_files.txt

# Network config
ip addr show > /evidence/ifconfig.txt
ip route show > /evidence/routes.txt
ip neigh show > /evidence/arp.txt

# Logged-in users
w > /evidence/users.txt
last -50 > /evidence/last_logins.txt

# Cron jobs
crontab -l > /evidence/crontab.txt
ls -la /etc/cron.d/ >> /evidence/crontab.txt
```

## Windows Collection Commands
```cmd
:: Network connections
netstat -anob > C:\evidence\netstat.txt

:: Process list
tasklist /V /FO CSV > C:\evidence\processes.csv
wmic process get ProcessId,Name,CommandLine /format:csv > C:\evidence\wmic_procs.csv

:: Network config
ipconfig /all > C:\evidence\ipconfig.txt
route print > C:\evidence\routes.txt
arp -a > C:\evidence\arp.txt

:: DNS cache
ipconfig /displaydns > C:\evidence\dns_cache.txt

:: Scheduled tasks
schtasks /query /FO CSV /V > C:\evidence\schtasks.csv

:: Logged-in users
query user > C:\evidence\users.txt
```

## Evidence Integrity
```bash
# Hash collected files
sha256sum /evidence/*.txt > /evidence/checksums.sha256

# Verify later
sha256sum -c /evidence/checksums.sha256
```

---

## Standards and Controls

## RFC 3227 - Guidelines for Evidence Collection and Archiving
- Defines the order of volatility for digital evidence:
  1. Registers, cache
  2. Routing table, ARP cache, process table, kernel statistics, memory
  3. Temporary file systems
  4. Disk
  5. Remote logging and monitoring data
  6. Physical configuration, network topology
  7. Archival media
- Key principles: minimize data alteration, document actions, use trusted tools
- Reference: https://www.rfc-editor.org/rfc/rfc3227

## NIST SP 800-86 - Guide to Integrating Forensic Techniques
- Section 4: Using Data from Data Sources
  - 4.2: Data Files - Volatile and non-volatile OS data
  - 4.3: Operating System Data - Memory, processes, network connections
- Forensic process: Collection, Examination, Analysis, Reporting
- Emphasis on preserving data integrity through proper acquisition
- Reference: https://csrc.nist.gov/pubs/sp/800/86/final

## NIST SP 800-61 Rev. 3 - Evidence Handling
- **Respond (RS)** function alignment:
  - RS.AN-03: Analysis to establish incident scope
- Evidence must be collected in a forensically sound manner
- Document all collection activities and maintain chain of custody

## SANS DFIR - Live Evidence Collection Best Practices
- Collect evidence from most volatile to least volatile
- Use external trusted tools (not tools from compromised system)
- Hash all evidence immediately after collection
- Document system time offset from UTC
- Minimize footprint on compromised system
- Reference: https://www.sans.org/white-papers/

## MITRE ATT&CK - Evidence Sources for Detection
| Data Source | ATT&CK Reference | Evidence Type |
|------------|-------------------|---------------|
| Process (DS0009) | Process creation, command line | Running processes |
| Network Traffic (DS0029) | Connection creation, flow | Network connections |
| File (DS0022) | File creation, modification | Open handles, temp files |
| Windows Registry (DS0024) | Registry key modification | Autostart entries |
| Logon Session (DS0028) | Logon creation | Active user sessions |
| Module (DS0011) | Module load | Loaded DLLs/shared objects |

## ACPO Good Practice Guide for Digital Evidence
- Principle 1: No action should change data on digital devices
- Principle 2: Competent person must access original data when necessary
- Principle 3: Audit trail of all processes applied to evidence
- Principle 4: Person in charge ensures law and principles are adhered to

## ISO/IEC 27037 - Guidelines for Identification, Collection, Acquisition, and Preservation
- Defines procedures for handling digital evidence
- Specifies requirements for first responders and forensic specialists
- Covers volatile and non-volatile evidence acquisition
- Emphasizes competency of evidence handlers

## SWGDE Best Practices for Computer Forensics
- Scientific Working Group on Digital Evidence
- Standards for evidence acquisition, examination, and reporting
- Quality assurance requirements for forensic processes

---

## Workflows

## Order of Volatility Collection Sequence

### Priority 1: Memory (Most Volatile) - Collect First
1. Connect forensic USB with memory acquisition tool
2. Run memory dump tool from USB (NOT from compromised disk)
3. Save memory image to external storage
4. Record start time, end time, and memory size
5. Generate SHA256 hash of memory image immediately
6. Document any errors during acquisition

### Priority 2: Network State
1. Capture all active TCP/UDP connections with process IDs
2. Capture ARP cache (maps IP to MAC addresses)
3. Capture DNS resolver cache
4. Capture routing table
5. Capture active firewall rules
6. Capture listening ports and associated processes
7. Hash all network evidence files

### Priority 3: Running Processes
1. List all processes with full command lines
2. List parent-child process relationships (process tree)
3. List all loaded modules/DLLs per process
4. List all open file handles per process
5. List process network connections per PID
6. Capture process creation timestamps
7. Hash all process evidence files

### Priority 4: User Sessions
1. List all currently logged-in users
2. List active remote sessions (RDP, SSH, SMB)
3. List mapped network drives
4. Capture recent authentication events
5. List active tokens and session keys (if accessible)

### Priority 5: System Configuration
1. Capture system time and UTC offset
2. Export autostart/persistence locations (Registry Run keys, crontab)
3. List all services and their states
4. Capture environment variables
5. List installed software
6. Export relevant event log entries

### Priority 6: Temporary/Cache Data
1. Capture browser history and cache (if relevant)
2. Capture clipboard contents (if accessible)
3. Capture temp directory contents
4. Capture recent file lists
5. Capture prefetch files (Windows)

## Platform-Specific Collection Procedures

### Windows Collection Checklist
```
[ ] Memory: WinPmem/Magnet RAM Capture
[ ] Processes: tasklist /V, wmic process, Get-Process
[ ] Network: netstat -anob, Get-NetTCPConnection
[ ] Users: query user, net session
[ ] Registry: Run keys, Services, Startup
[ ] Services: sc queryex, Get-Service
[ ] Scheduled Tasks: schtasks /query
[ ] DNS Cache: ipconfig /displaydns
[ ] ARP: arp -a
[ ] Firewall: netsh advfirewall
[ ] Event Logs: wevtutil (Security, System, Application)
[ ] Prefetch: %SystemRoot%\Prefetch\*
[ ] Time: w32tm /query /status
```

### Linux Collection Checklist
```
[ ] Memory: LiME kernel module or /proc/kcore
[ ] Processes: ps auxwwf, /proc/*/cmdline, /proc/*/maps
[ ] Network: ss -tulnp, /proc/net/tcp, /proc/net/udp
[ ] Users: who, w, last
[ ] Cron: crontab -l, /etc/cron.*
[ ] Services: systemctl list-units
[ ] DNS: systemd-resolve, /etc/resolv.conf
[ ] ARP: ip neigh
[ ] Firewall: iptables -L -n -v, nftables
[ ] Logs: /var/log/auth.log, /var/log/syslog
[ ] Open Files: lsof
[ ] Time: timedatectl
[ ] Loaded Modules: lsmod
```

## Evidence Integrity Procedures

### Hashing Protocol
1. Hash EVERY collected file immediately after creation
2. Use SHA256 (minimum) - SHA512 preferred for legal cases
3. Store hash manifest in separate file
4. Verify hashes before and after any transfer
5. Include hash in chain of custody documentation

### Chain of Custody Requirements
1. Record who collected each evidence item
2. Record exact time of collection (UTC)
3. Record collection method and tool version
4. Record any transfer of evidence
5. Record storage location and access controls
6. Record any analysis performed on copies (never originals)

## Common Pitfalls to Avoid
1. Running tools from the compromised system's disk
2. Forgetting to hash evidence immediately
3. Not recording system time offset from UTC
4. Installing collection tools on the compromised system
5. Rebooting the system before memory collection
6. Modifying file timestamps by browsing the filesystem
7. Not documenting collection steps in real-time
8. Collecting evidence without proper authorization

---

## Working Template

## Case Information
| Field | Value |
|-------|-------|
| Case ID | |
| System Hostname | |
| System IP Address | |
| System OS | |
| Collection Date/Time (UTC) | |
| Collector Name | |
| Authorization | [IR Plan / Legal Hold / HR Approval] |

## Collection Summary
| Evidence Category | Items Collected | Status |
|------------------|----------------|--------|
| Memory Dump | | Collected/Failed/Skipped |
| Network Connections | | Collected/Failed/Skipped |
| ARP Cache | | Collected/Failed/Skipped |
| DNS Cache | | Collected/Failed/Skipped |
| Routing Table | | Collected/Failed/Skipped |
| Running Processes | | Collected/Failed/Skipped |
| Open File Handles | | Collected/Failed/Skipped |
| Logged-in Users | | Collected/Failed/Skipped |
| System Configuration | | Collected/Failed/Skipped |
| Services | | Collected/Failed/Skipped |
| Scheduled Tasks | | Collected/Failed/Skipped |
| Registry/Config | | Collected/Failed/Skipped |

## Evidence Manifest
| Filename | SHA256 Hash | Size | Category |
|----------|------------|------|----------|
| | | | |

## Chain of Custody
| Date/Time (UTC) | Action | Person | Notes |
|-----------------|--------|--------|-------|
| | Evidence collected from live system | | |
| | Evidence transferred to forensic storage | | |
| | Evidence hash verified | | |
| | Evidence accessed for analysis | | |

## System Time Verification
| Field | Value |
|-------|-------|
| System Clock (UTC) | |
| Reference Time (UTC) | |
| Time Offset | |
| NTP Synchronized | Yes/No |
| NTP Server | |

## Notable Findings During Collection
[Any suspicious processes, connections, or artifacts noted during collection]

## Collection Tool Information
| Tool | Version | Source | SHA256 Hash |
|------|---------|--------|-------------|
| | | | |

## Collector Certification
I certify that the evidence described above was collected using forensically sound methods, from external trusted tools, and that all evidence was hashed immediately upon collection.

| Field | Value |
|-------|-------|
| Collector Name | |
| Collector Title | |
| Date | |
| Signature | |
