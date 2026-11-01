# Performing Active Directory Compromise Investigation

## API Reference

## Windows Security Event IDs

| Event ID | Description | Compromise Indicator |
|----------|-------------|---------------------|
| 4662 | Directory service object accessed | DCSync (replication GUIDs) |
| 4769 | Kerberos service ticket requested | Kerberoasting (RC4 encryption) |
| 4768 | Kerberos TGT requested | Golden Ticket (anomalous source) |
| 4672 | Special privileges assigned | Privileged logon tracking |
| 4624 | Successful logon | Lateral movement (Type 3) |
| 4648 | Explicit credential logon | Pass-the-hash, PsExec |
| 4720 | User account created | Persistence |
| 4728 | Member added to global group | Privilege escalation |
| 4732 | Member added to local group | Privilege escalation |

## DCSync Detection

### Replication GUIDs (Event 4662 ObjectType)

| GUID | Right |
|------|-------|
| `1131f6aa-9c07-11d1-f79f-00c04fc2dcd2` | DS-Replication-Get-Changes |
| `1131f6ad-9c07-11d1-f79f-00c04fc2dcd2` | DS-Replication-Get-Changes-All |
| `89e95b76-444d-4c62-991a-0facbeda640c` | DS-Replication-Get-Changes-In-Filtered-Set |

When a non-DC account triggers 4662 with these GUIDs, it indicates DCSync attack (Mimikatz lsadump::dcsync).

## Kerberoasting Detection

Event 4769 with `TicketEncryptionType = 0x17` (RC4-HMAC) for service accounts. Normal behavior uses AES (0x11 or 0x12). RC4 requests by user accounts against service SPNs indicate offline cracking attempts.

## Golden Ticket Detection

Event 4768 TGT requests from IPs that are not domain controllers. Golden tickets forged offline will show TGT requests from workstations rather than DCs.

## Lateral Movement Detection

- **Type 3 logon** (Event 4624, LogonType=3): Network logon via SMB, WMI, PsExec
- **Event 4648**: Explicit credential use (runas, remote tools)
- Pattern: Multiple Type 3 logons from same source to different targets

## Event Log JSON Format

The agent accepts JSON-exported event logs:
```json
[
  {
    "EventID": 4769,
    "TimeCreated": "2024-01-15T10:30:00Z",
    "EventData": {
      "TargetUserName": "svc_sql",
      "ServiceName": "MSSQLSvc/db01:1433",
      "TicketEncryptionType": "0x17"
    }
  }
]
```

Export from PowerShell:
```powershell
Get-WinEvent -LogName Security | ConvertTo-Json -Depth 5 > events.json
```

## Output Schema

```json
{
  "report": "ad_compromise_investigation",
  "total_events_analyzed": 50000,
  "total_findings": 15,
  "severity_summary": {"critical": 3, "high": 7, "medium": 5},
  "findings": [{"type": "dcsync_detected", "severity": "critical"}]
}
```

## CLI Usage

```bash
python agent.py --log events.json --output report.json
```

---

## Standards and Controls

## NIST SP 800-61 Rev 2 - Computer Security Incident Handling Guide
- Provides incident response lifecycle: Preparation, Detection & Analysis, Containment, Eradication & Recovery, Post-Incident Activity
- AD compromise investigations follow all four phases with emphasis on scoping the identity compromise

## CISA Alert: Detecting and Mitigating Active Directory Compromises
- Published guidance on AD-specific threats and detection methods
- Covers DCSync, Golden Ticket, Silver Ticket, and Kerberoasting attacks
- Recommends tiered administration, Protected Users group, and credential hygiene
- Reference: https://www.cisa.gov/resources-tools/resources/detecting-and-mitigating-active-directory-compromises

## MITRE ATT&CK Framework - Credential Access Tactics
- T1003.006: OS Credential Dumping - DCSync
- T1558.001: Steal or Forge Kerberos Tickets - Golden Ticket
- T1558.002: Steal or Forge Kerberos Tickets - Silver Ticket
- T1558.003: Steal or Forge Kerberos Tickets - Kerberoasting
- T1550.002: Use Alternate Authentication Material - Pass the Hash
- T1484.001: Domain Policy Modification - Group Policy Modification
- T1098: Account Manipulation

## Microsoft Security Best Practices
- Tiered administration model for Active Directory
- Privileged Access Workstations (PAWs) for domain admin tasks
- Microsoft Advanced Threat Analytics (ATA) / Defender for Identity
- LAPS (Local Administrator Password Solution) deployment
- Protected Users security group enforcement
- Reference: https://learn.microsoft.com/en-us/security/privileged-access-workstations/overview

## CIS Benchmarks for Active Directory
- CIS Microsoft Windows Server Benchmark for DC hardening
- Password policy requirements (minimum 14 characters)
- Account lockout policy configuration
- Audit policy settings for security event logging
- GPO security baseline configurations

## SANS FOR500 - Windows Forensic Analysis
- Windows artifact analysis methodology
- Registry analysis for persistence detection
- Event log forensics for authentication tracking
- Timeline analysis techniques for AD compromise

## Semperis Identity Forensics and Incident Response (IFIR)
- AD-specific forensic methodology
- Replication metadata analysis
- Change tracking and rollback capabilities
- Forest recovery procedures
- Reference: https://www.semperis.com/solutions/active-directory-breach-forensics/

## Key Windows Security Event IDs for AD Monitoring
- Microsoft documentation on security auditing events
- Advanced Audit Policy Configuration for DCs
- Kerberos event logging requirements
- Directory Service Access auditing

---

## Workflows

## Workflow 1: Initial Triage and Scoping

```
START: AD Compromise Alert Received
  |
  v
[Determine Scope of Potential Compromise]
  |-- Single account compromised?
  |-- Multiple accounts compromised?
  |-- Domain controller compromised?
  |-- Full domain compromise suspected?
  |
  v
[Collect Initial Evidence]
  |-- Export Security event logs from all DCs
  |-- Snapshot AD replication metadata
  |-- Export current GPO configurations
  |-- Document privileged group memberships
  |
  v
[Identify Compromised Accounts]
  |-- Analyze logon events (4624/4625)
  |-- Check for pass-the-hash patterns
  |-- Review Kerberos ticket activity
  |-- Cross-reference with threat intelligence
  |
  v
[Determine Attack Timeline]
  |-- First known malicious activity
  |-- Privilege escalation events
  |-- Lateral movement chain
  |-- Data access and exfiltration
  |
  v
[Report Findings and Escalate]
```

## Workflow 2: Kerberos Attack Investigation

```
START: Suspicious Kerberos Activity Detected
  |
  v
[Analyze Event ID 4768 - TGT Requests]
  |-- Normal TGT requests from user workstations?
  |-- TGT requests from unusual sources?
  |-- Encryption type analysis (AES vs RC4)
  |
  v
[Analyze Event ID 4769 - Service Ticket Requests]
  |-- High volume from single source? --> Kerberoasting
  |-- Service tickets without prior TGT? --> Silver Ticket
  |-- Unusual service names or SPNs?
  |
  v
[Check for Golden Ticket Indicators]
  |-- TGT lifetime exceeds 10 hours?
  |-- TGT for non-existent accounts?
  |-- TGT without matching AS-REQ?
  |-- krbtgt account age analysis
  |
  v
[Determine Remediation Actions]
  |-- Kerberoasting: Reset affected service account passwords
  |-- Golden Ticket: Double-rotate krbtgt password
  |-- Silver Ticket: Reset affected service account passwords
  |-- All: Review and harden SPN configurations
  |
  v
END: Remediation Complete + Monitoring Enhanced
```

## Workflow 3: DCSync Attack Investigation

```
START: Replication from Non-DC Source Detected
  |
  v
[Verify Replication Source]
  |-- Is source a legitimate domain controller?
  |-- Check Event ID 4662 for replication rights usage
  |-- Verify account has DS-Replication-Get-Changes-All
  |
  v
[If Unauthorized Replication Detected]
  |-- Identify compromised account with replication rights
  |-- Determine which credentials were replicated
  |-- Check for Mimikatz/Impacket artifacts on source
  |
  v
[Assess Credential Exposure]
  |-- All domain password hashes potentially compromised
  |-- krbtgt hash exposure enables Golden Ticket
  |-- Service account hashes enable Silver Tickets
  |-- Trust keys enable cross-domain attacks
  |
  v
[Execute Full Credential Reset]
  |-- Double-rotate krbtgt (wait for replication)
  |-- Reset all privileged account passwords
  |-- Reset all service account passwords
  |-- Force password change for all users
  |
  v
END: Monitor for Continued Unauthorized Replication
```

## Workflow 4: Post-Compromise Remediation

```
START: Compromise Scope Determined
  |
  v
[Immediate Containment]
  |-- Disable compromised accounts
  |-- Block attacker IP addresses
  |-- Isolate compromised systems
  |-- Revoke active sessions and tokens
  |
  v
[Credential Reset Sequence]
  |-- Step 1: Reset krbtgt (first rotation)
  |-- Step 2: Wait for full AD replication
  |-- Step 3: Reset krbtgt (second rotation)
  |-- Step 4: Wait for full AD replication
  |-- Step 5: Reset all privileged accounts
  |-- Step 6: Reset all service accounts
  |-- Step 7: Force user password changes
  |
  v
[Persistence Removal]
  |-- Remove unauthorized GPO modifications
  |-- Clean AdminSDHolder ACL entries
  |-- Remove SID History entries
  |-- Revoke rogue AD CS certificates
  |-- Remove skeleton key if detected
  |-- Clean scheduled tasks and services
  |
  v
[Hardening Implementation]
  |-- Deploy tiered administration model
  |-- Enable Protected Users group
  |-- Implement PAW for admin tasks
  |-- Deploy LAPS for local admin
  |-- Configure advanced audit policies
  |
  v
END: Continuous Monitoring Established
```

---

## Working Template

## Case Information

| Field | Details |
|-------|---------|
| Case ID | IR-AD-YYYY-XXX |
| Investigator | |
| Date Initiated | |
| Organization | |
| Domain(s) Affected | |
| Domain Controllers | |
| Estimated Compromise Date | |

## Executive Summary

[Brief description of the AD compromise, scope, and critical findings]

## Scope of Investigation

### Domain Controllers Examined
| DC Name | OS Version | IP Address | Role | Status |
|---------|-----------|------------|------|--------|
| | | | | |

### Log Sources Collected
- [ ] Security Event Logs (all DCs)
- [ ] System Event Logs
- [ ] Directory Service Logs
- [ ] DNS Server Logs
- [ ] PowerShell Transcription Logs
- [ ] Replication Metadata
- [ ] GPO Configuration Export
- [ ] Privileged Group Membership Export

## Attack Timeline

| Timestamp | Event | Source | Severity |
|-----------|-------|--------|----------|
| | Initial access | | |
| | Privilege escalation | | |
| | Lateral movement | | |
| | Domain compromise | | |
| | Data access/exfiltration | | |

## Findings

### Finding 1: [Attack Category]
- **Severity:** CRITICAL / HIGH / MEDIUM / LOW
- **Evidence:** [Event IDs, log entries, artifacts]
- **Impact:** [Accounts, systems, data affected]
- **MITRE ATT&CK:** [Technique ID and name]

### Finding 2: [Attack Category]
- **Severity:**
- **Evidence:**
- **Impact:**
- **MITRE ATT&CK:**

## Compromised Accounts

| Account | Type | Privileges | Compromise Method | Status |
|---------|------|------------|-------------------|--------|
| | Domain Admin | | DCSync | Disabled |
| | Service Account | | Kerberoasting | Reset |

## Kerberos Analysis

### Golden Ticket Assessment
- [ ] krbtgt password age: _____ days
- [ ] TGTs with abnormal lifetimes detected: Yes / No
- [ ] RC4 encryption on tickets detected: Yes / No
- [ ] Service tickets without TGT requests: Yes / No

### Kerberoasting Assessment
- [ ] Bulk TGS requests from single source: Yes / No
- [ ] Service accounts with weak passwords: Yes / No
- [ ] Service accounts targeted: _____ accounts

## Lateral Movement Map

```
[Source] --> [Hop 1] --> [Hop 2] --> [Domain Controller]
   |
   +--> [Hop 1b] --> [File Server]
```

## Persistence Mechanisms Found

- [ ] AdminSDHolder ACL modifications
- [ ] SID History injection
- [ ] Rogue GPO policies
- [ ] Skeleton Key malware
- [ ] DCShadow objects
- [ ] Rogue AD CS certificates
- [ ] Scheduled tasks via GPO
- [ ] Modified login scripts
- [ ] Custom WMI subscriptions

## Remediation Actions

### Immediate (0-24 hours)
- [ ] Disable all compromised accounts
- [ ] Isolate compromised systems
- [ ] Block attacker IP addresses at firewall
- [ ] Double-rotate krbtgt password
- [ ] Revoke all active sessions

### Short-term (24-72 hours)
- [ ] Reset all privileged account passwords
- [ ] Reset all service account passwords
- [ ] Remove unauthorized group memberships
- [ ] Revert malicious GPO changes
- [ ] Remove persistence mechanisms

### Long-term (1-4 weeks)
- [ ] Force all user password changes
- [ ] Implement tiered administration model
- [ ] Deploy Privileged Access Workstations
- [ ] Enable Microsoft Defender for Identity
- [ ] Implement LAPS for local admin passwords
- [ ] Configure advanced audit policies
- [ ] Add critical accounts to Protected Users group

## Indicators of Compromise

### Accounts
| Account | Type | Activity |
|---------|------|----------|
| | | |

### IP Addresses
| IP | Activity | First Seen | Last Seen |
|----|----------|------------|-----------|
| | | | |

### Tools Detected
| Tool | Hash | Location | Purpose |
|------|------|----------|---------|
| | | | |

## Appendix

### Event Log Analysis Summary
### BloodHound Attack Path Diagrams
### GPO Change Detail
### Network Diagram with Lateral Movement Overlay
