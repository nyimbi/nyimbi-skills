# Recovering From Ransomware Attack

## API Reference

## Recovery Priority Order

| Priority | Systems | Why First |
|----------|---------|-----------|
| 1 | Domain Controllers | All auth depends on AD |
| 2 | DNS/DHCP | Network functionality |
| 3 | Authentication (SSO/MFA) | User access |
| 4 | Email | Communication |
| 5 | Database Servers | Business data |
| 6 | Application Servers | Business operations |
| 7 | File Servers | Data access |
| 8 | Workstations | End user devices |

## KRBTGT Reset Procedure

| Step | Command | Note |
|------|---------|------|
| 1 | `Reset-KrbtgtPassword` | First reset |
| 2 | Wait 12 hours | Allow replication |
| 3 | `Reset-KrbtgtPassword` | Second reset |
| 4 | `dcdiag /v` | Validate DC health |

## Backup Verification Commands

| Command | Description |
|---------|-------------|
| `veeamcli verify` | Verify Veeam backup integrity |
| `wbadmin get versions` | List Windows Server backups |
| `aws s3api head-object` | Check S3 backup metadata |

## 3-2-1-1-0 Backup Strategy

| Component | Description |
|-----------|-------------|
| 3 copies | Production + 2 backups |
| 2 media types | Disk + tape/cloud |
| 1 offsite | Geographically separate |
| 1 offline | Air-gapped or immutable |
| 0 errors | Verified with restore tests |

## Python Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| `json` | stdlib | Recovery tracking |
| `datetime` | stdlib | Timeline documentation |
| `pathlib` | stdlib | Backup path verification |

## References

- CISA Ransomware Guide: https://www.cisa.gov/stopransomware/ransomware-guide
- NIST SP 1800-26: https://www.nccoe.nist.gov/data-integrity-recovering-ransomware
- NoMoreRansom: https://www.nomoreransom.org/

---

## Standards and Controls

## Frameworks
- NIST SP 800-61r3: Computer Security Incident Handling Guide (Recover phase)
- NIST IR 8374: Ransomware Risk Management - Recovery section
- CISA #StopRansomware Guide: Recovery checklist
- CIS Controls v8: Control 11 (Data Recovery)
- NIST CSF 2.0: Recover function (RC.RP, RC.CO)

## AD Recovery
- Microsoft: AD Forest Recovery Guide - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/ad-forest-recovery-guide
- DSInternals: https://github.com/MichaelGrafnetter/DSInternals
- krbtgt reset guidance: https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/forest-recovery-guide/ad-forest-recovery-resetting-the-krbtgt-password

## MITRE ATT&CK (Recovery Validation)
- T1053: Scheduled Task/Job (persistence to check)
- T1543: Create or Modify System Process (persistence to check)
- T1547: Boot or Logon Autostart Execution (persistence to check)
- T1558.001: Golden Ticket (must reset krbtgt)
- T1098: Account Manipulation (check for backdoor accounts)

---

## Workflows

## Workflow 1: Recovery Decision and Planning

```
Containment Complete + Forensics Initiated
  |
  v
[Assess backup availability]
  |-- Immutable copies intact? --> Primary recovery path
  |-- Air-gapped copies available? --> Secondary recovery path
  |-- No clean backups? --> Consider decryption key (paid or NoMoreRansom)
  |
  v
[Determine recovery scope]
  |-- Full rebuild vs. selective restore
  |-- Identify minimum viable recovery set
  |
  v
[Map system dependencies]
  |-- AD/DNS -> Database -> Application -> Web
  |
  v
[Estimate recovery timeline per tier]
  |
  v
[Brief executive team on recovery plan and timeline]
  |
  v
[Begin recovery]
```

## Workflow 2: System Recovery Execution

```
[Establish clean recovery VLAN]
  |
  v
[Phase 1: Identity Recovery]
  |-- Restore DCs from verified backup
  |-- Reset krbtgt (2x)
  |-- Reset all admin passwords
  |-- Validate AD health (dcdiag)
  |
  v
[Phase 2: Critical Systems]
  |-- Restore databases
  |-- Verify data consistency
  |-- Restore core applications
  |-- Test application functionality
  |
  v
[Phase 3: Important Systems]
  |-- Restore in groups of 5-10
  |-- Validate each before proceeding
  |
  v
[Phase 4: Remaining Systems]
  |
  v
[Each system: Scan for persistence -> Patch -> Deploy EDR -> Connect]
  |
  v
[Post-recovery monitoring (7-14 days elevated alert)]
```
