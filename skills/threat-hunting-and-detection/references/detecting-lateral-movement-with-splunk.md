# Detecting Lateral Movement With Splunk

## API Reference

## Key Lateral Movement Techniques

| Technique | MITRE ID | Event Source |
|-----------|----------|-------------|
| Pass-the-Hash | T1550.002 | Event 4624 Logon_Type=3 NTLM |
| PSExec | T1569.002 | Sysmon Event 1 (PSEXESVC.exe) |
| WMI Remote Exec | T1047 | Sysmon Event 1 (wmiprvse.exe) |
| RDP Pivoting | T1021.001 | Event 4624 Logon_Type=10 |
| SMB/Admin Share | T1021.002 | Network logs dest_port=445 |
| WinRM | T1021.006 | Sysmon Event 1 (wsmprovhost.exe) |

## Splunk SPL Syntax

```spl
# Pass-the-Hash detection
index=wineventlog EventCode=4624 Logon_Type=3
| where Authentication_Package="NTLM"
| stats dc(Computer) as targets by Source_Network_Address
| where targets > 3

# PSExec detection
index=sysmon EventCode=1
| where ParentImage="*\\services.exe" AND Image="*\\PSEXESVC.exe"
```

## splunklib Python SDK

```python
import splunklib.client as client
import splunklib.results as results

service = client.connect(host="splunk", port=8089, token="...")
job = service.jobs.create("search index=wineventlog EventCode=4624")
for result in results.JSONResultsReader(job.results(output_mode="json")):
    print(result)
```

## Windows Logon Types

| Type | Description |
|------|-------------|
| 2 | Interactive (console) |
| 3 | Network (SMB, PSExec) |
| 7 | Unlock |
| 10 | RemoteInteractive (RDP) |

## CLI Usage

```bash
python agent.py --generate-queries
python agent.py --generate-queries --techniques pass_the_hash psexec_execution
python agent.py --parse-results splunk_output.json
```

---

## Standards and Controls

## MITRE ATT&CK Lateral Movement (TA0008)

| Technique | Name | Event Indicators |
|-----------|------|-----------------|
| T1021.001 | Remote Desktop Protocol | Logon Type 10, RDP certificate events |
| T1021.002 | SMB/Windows Admin Shares | Logon Type 3, ADMIN$/C$/IPC$ access |
| T1021.003 | Distributed COM | Logon Type 3, DCOM process creation |
| T1021.004 | SSH | OpenSSH authentication events |
| T1021.006 | Windows Remote Management | WinRM/WSMan logon events |
| T1047 | Windows Management Instrumentation | WMI remote process creation |
| T1569.002 | Service Execution | PsExec service install + Type 3 logon |
| T1570 | Lateral Tool Transfer | File copy over SMB/RDP |
| T1550.002 | Pass the Hash | Type 3 logon with NTLM authentication |
| T1550.003 | Pass the Ticket | Kerberos TGS without preceding TGT |

## Windows Logon Types Reference

| Type | Name | Description |
|------|------|-------------|
| 2 | Interactive | Local console logon |
| 3 | Network | SMB, mapped drives, WinRM |
| 4 | Batch | Scheduled task execution |
| 5 | Service | Service startup |
| 7 | Unlock | Workstation unlock |
| 8 | NetworkCleartext | IIS basic auth |
| 9 | NewCredentials | RunAs /netonly |
| 10 | RemoteInteractive | RDP, Terminal Services |
| 11 | CachedInteractive | Cached domain logon |

## Key Windows Event IDs for Lateral Movement

| Event ID | Source | Description |
|----------|--------|-------------|
| 4624 | Security | Successful account logon |
| 4625 | Security | Failed account logon |
| 4648 | Security | Logon with explicit credentials |
| 4672 | Security | Special privileges assigned (admin logon) |
| 4768 | Security | Kerberos TGT requested |
| 4769 | Security | Kerberos TGS requested |
| 4776 | Security | NTLM credential validation |
| 5140 | Security | Network share accessed |
| 5145 | Security | Network share object access check |
| 7045 | System | New service installed |
| 1 | Sysmon | Process creation |
| 3 | Sysmon | Network connection |

## Splunk Data Model References

- `Authentication` data model for login events
- `Network_Traffic` data model for connection data
- `Endpoint.Processes` for process creation events
- `Change.Endpoint_Changes` for service installations

## Authentication Protocol Indicators

| Protocol | Lateral Movement | Event Indicators |
|----------|-----------------|-----------------|
| NTLM | Pass-the-Hash | Event 4776, NtLmSsp package |
| Kerberos | Pass-the-Ticket | Event 4768/4769, ticket anomalies |
| CredSSP | RDP | Event 4624 Type 10 |
| WSMan | WinRM | Event 4624 Type 3, WSMan source |

---

## Workflows

## Phase 1: Network Logon Analysis

### Step 1.1 - Type 3 Network Logons (SMB, WinRM)
```spl
index=wineventlog EventCode=4624 Logon_Type=3
| where NOT match(Account_Name, "(?i)(SYSTEM|ANONYMOUS|\\$)")
| stats count dc(Computer) as unique_destinations values(Computer) as destinations by Account_Name Source_Network_Address
| where unique_destinations > 3
| sort -unique_destinations
```

### Step 1.2 - Type 10 RDP Logons
```spl
index=wineventlog EventCode=4624 Logon_Type=10
| stats count by Account_Name Source_Network_Address Computer
| lookup dnslookup clientip as Source_Network_Address OUTPUT clienthost as src_hostname
| table Account_Name src_hostname Source_Network_Address Computer count
| sort -count
```

### Step 1.3 - Explicit Credential Logons (PsExec, RunAs)
```spl
index=wineventlog EventCode=4648
| where NOT match(Target_Server_Name, "(?i)(localhost|\\$)")
| stats count values(Target_Server_Name) as targets by Account_Name Process_Name Computer
| sort -count
```

## Phase 2: Admin Share Access Detection

### Step 2.1 - ADMIN$ and C$ Share Access
```spl
index=wineventlog EventCode=5140
| where Share_Name IN ("\\\\*\\ADMIN$", "\\\\*\\C$", "\\\\*\\IPC$")
| where NOT match(Account_Name, "(?i)(\\$|SYSTEM)")
| stats count values(Share_Name) as shares by Account_Name Source_Address Computer
| sort -count
```

### Step 2.2 - SMB File Operations on Admin Shares
```spl
index=wineventlog EventCode=5145
| where match(Share_Name, "(?i)(ADMIN\\$|C\\$)")
| where match(Relative_Target_Name, "(?i)(\\.exe|\\.dll|\\.ps1|\\.bat|\\.cmd)")
| stats count by Account_Name Source_Address Share_Name Relative_Target_Name Computer
```

## Phase 3: Service-Based Lateral Movement

### Step 3.1 - PsExec Service Installation
```spl
index=wineventlog EventCode=7045
| where match(Service_File_Name, "(?i)(psexec|PSEXESVC|cmd\.exe|powershell)")
| table _time Computer Service_Name Service_File_Name Service_Account
```

### Step 3.2 - Remote Service Creation Correlation
```spl
index=wineventlog EventCode=7045
| eval is_suspicious=if(match(Service_File_Name, "(?i)(temp|appdata|cmd|powershell)"), 1, 0)
| where is_suspicious=1
| join Computer [
    search index=wineventlog EventCode=4624 Logon_Type=3
    | rename Computer as Computer, Source_Network_Address as lateral_src
]
| table _time Computer Service_Name Service_File_Name lateral_src
```

## Phase 4: WMI and DCOM Lateral Movement

### Step 4.1 - Remote WMI Execution
```spl
index=sysmon EventCode=1
| where match(ParentImage, "(?i)WmiPrvSE\.exe") AND NOT match(Image, "(?i)(WmiApSrv|scrcons)")
| table _time Computer User ParentImage Image CommandLine
```

### Step 4.2 - DCOM Lateral Movement
```spl
index=sysmon EventCode=1
| where match(ParentImage, "(?i)(mmc\.exe|excel\.exe|outlook\.exe)")
| where match(Image, "(?i)(cmd\.exe|powershell\.exe|mshta\.exe)")
| table _time Computer User ParentImage Image CommandLine
```

## Phase 5: Authentication Graph Analysis

### Step 5.1 - Build Lateral Movement Graph
```spl
index=wineventlog EventCode=4624 Logon_Type IN (3, 10)
| where NOT match(Account_Name, "(?i)(\\$|SYSTEM|ANONYMOUS)")
| eval connection=Source_Network_Address."->".Computer
| stats count first(_time) as first_seen last(_time) as last_seen by connection Account_Name
| sort -count
```

### Step 5.2 - First-Time Source-Destination Pairs
```spl
index=wineventlog EventCode=4624 Logon_Type IN (3, 10) earliest=-1d
| where NOT match(Account_Name, "(?i)(\\$|SYSTEM)")
| eval pair=Account_Name.":".Source_Network_Address."->".Computer
| search NOT [
    | search index=wineventlog EventCode=4624 Logon_Type IN (3, 10) earliest=-30d latest=-1d
    | eval pair=Account_Name.":".Source_Network_Address."->".Computer
    | dedup pair
    | fields pair
]
| stats count by pair
| sort -count
```

## Phase 6: Anomaly Detection

### Step 6.1 - Velocity Anomaly (Rapid Multi-Host Access)
```spl
index=wineventlog EventCode=4624 Logon_Type=3
| where NOT match(Account_Name, "(?i)(\\$|SYSTEM)")
| bin _time span=10m
| stats dc(Computer) as hosts_accessed values(Computer) as destinations by _time Account_Name Source_Network_Address
| where hosts_accessed > 5
| sort -hosts_accessed
```

### Step 6.2 - Off-Hours Lateral Movement
```spl
index=wineventlog EventCode=4624 Logon_Type IN (3, 10)
| where NOT match(Account_Name, "(?i)(\\$|SYSTEM)")
| eval hour=strftime(_time, "%H")
| where hour < 6 OR hour > 22
| stats count by Account_Name Source_Network_Address Computer hour
| sort -count
```

### Step 6.3 - Service Account Lateral Movement
```spl
index=wineventlog EventCode=4624 Logon_Type=10
| where match(Account_Name, "(?i)(svc_|service|admin)")
| stats count by Account_Name Source_Network_Address Computer
| sort -count
```

---

## Working Template

## Hunt Metadata
| Field | Value |
|-------|-------|
| Hunt ID | TH-LATMOV-YYYY-MM-DD-NNN |
| Analyst | |
| Date | |
| Status | [ ] In Progress / [ ] Complete |

## Hypothesis
> [e.g., "Adversaries are moving laterally via SMB admin shares using compromised domain admin credentials."]

## Techniques Investigated
- [ ] T1021.001 - RDP
- [ ] T1021.002 - SMB/Admin Shares
- [ ] T1021.006 - WinRM
- [ ] T1047 - WMI
- [ ] T1569.002 - PsExec/Service Execution
- [ ] T1550.002 - Pass the Hash
- [ ] T1570 - Lateral Tool Transfer

## Lateral Movement Path Map

```
[Source A] --RDP--> [Host B] --SMB--> [Host C] --WMI--> [Host D]
     |                                    |
     +--PsExec--> [Host E]               +--WinRM--> [Server F]
```

## Findings

| # | Source | Destination | Account | Method | Logon Type | Time | Risk |
|---|--------|------------|---------|--------|-----------|------|------|
| 1 | | | | | | | |

## Affected Accounts
| Account | Type | Hosts Accessed | Movement Method |
|---------|------|---------------|----------------|
| | | | |

## Recommendations
1. **Containment**: [Isolate systems, disable accounts]
2. **Credential Reset**: [Scope of password resets needed]
3. **Detection**: [New rules for identified patterns]
