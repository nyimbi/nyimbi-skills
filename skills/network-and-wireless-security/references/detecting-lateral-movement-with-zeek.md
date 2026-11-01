# Detecting Lateral Movement With Zeek

## API Reference

## CLI Usage

```bash
# Analyze current Zeek logs
python agent.py /opt/zeek/logs/current/

# Analyze specific date
python agent.py /opt/zeek/logs/2026-03-18/

# Pipe JSON output for further processing
python agent.py /opt/zeek/logs/current/ 2>/dev/null | python -m json.tool
```

## Zeek Log Files Analyzed

| Log File | Fields Used | Detection Purpose |
|----------|-------------|-------------------|
| conn.log | ts, id.orig_h, id.resp_h, id.resp_p, service, orig_bytes, resp_bytes | Internal lateral-port connections (SMB 445, RDP 3389, WinRM 5985) |
| smb_mapping.log | ts, id.orig_h, id.resp_h, path, share_type | Admin share access (C$, ADMIN$, IPC$) |
| smb_files.log | ts, id.orig_h, id.resp_h, action, path, name, size | Executable file writes to network shares |
| dce_rpc.log | ts, id.orig_h, id.resp_h, endpoint, operation, named_pipe | Remote service creation (svcctl), scheduled tasks (atsvc) |
| ntlm.log | ts, id.orig_h, id.resp_h, username, domainname, success | Pass-the-Hash detection, NTLM brute force |
| kerberos.log | ts, id.orig_h, id.resp_h, request_type, client, service, error_msg | Pass-the-Ticket, Kerberos pre-auth failures |

## Lateral Movement Ports Tracked

| Port | Service | ATT&CK Technique |
|------|---------|-------------------|
| 445 | SMB | T1021.002 - SMB/Windows Admin Shares |
| 135 | DCE/RPC | T1021.003 - Distributed Component Object Model |
| 139 | NetBIOS-SSN | T1021.002 - SMB/Windows Admin Shares |
| 3389 | RDP | T1021.001 - Remote Desktop Protocol |
| 5985 | WinRM-HTTP | T1021.006 - Windows Remote Management |
| 5986 | WinRM-HTTPS | T1021.006 - Windows Remote Management |
| 22 | SSH | T1021.004 - SSH |

## Suspicious DCE/RPC Endpoints

| Endpoint | Description | Severity |
|----------|-------------|----------|
| svcctl | Service Control Manager (PsExec pattern) | CRITICAL |
| atsvc | AT Scheduler Service (at.exe / schtasks) | CRITICAL |
| ITaskSchedulerService | Task Scheduler v2 (schtasks) | CRITICAL |
| winreg | Remote Registry manipulation | HIGH |
| samr | SAM Remote Protocol (user enumeration) | HIGH |
| lsarpc | LSA Remote Protocol (policy enumeration) | HIGH |
| srvsvc | Server Service (share/session enumeration) | HIGH |
| wkssvc | Workstation Service (user enumeration) | HIGH |

## Detection Types in Output

| Finding Type | Severity | Description |
|-------------|----------|-------------|
| lateral_port_connection | INFO | Internal connection on a lateral-movement-associated port |
| admin_share_access | HIGH | Access to C$, ADMIN$, or IPC$ administrative share |
| smb_file_write | MEDIUM/CRITICAL | File write to SMB share (CRITICAL if executable) |
| suspicious_dce_rpc | HIGH/CRITICAL | DCE/RPC call to remote execution endpoint |
| multi_source_ntlm_auth | HIGH | Single user NTLM authenticating from 3+ source IPs |
| ntlm_brute_force | HIGH | 5+ failed NTLM auth attempts from same source |
| multi_source_tgt_request | HIGH | Kerberos TGT requested from 3+ source IPs |
| kerberos_preauth_failure | MEDIUM | Kerberos pre-authentication failure |
| psexec_pattern | CRITICAL | Correlated SMB exe write + svcctl service creation |

## Report Output Schema

```json
{
  "summary": {
    "total_findings": 42,
    "by_severity": {"CRITICAL": 3, "HIGH": 15, "MEDIUM": 24},
    "by_type": {"admin_share_access": 8, "suspicious_dce_rpc": 5}
  },
  "top_connection_pairs": [
    {"pair": "10.0.1.50->10.0.1.100:445", "connections": 287}
  ],
  "top_data_transfer_pairs": [
    {"pair": "10.0.1.50->10.0.1.100:445", "bytes": 104857600, "megabytes": 100.0}
  ],
  "findings": []
}
```

## Zeek CLI Commands

```bash
# Install BZAR package for ATT&CK detections
zkg install zeek/mitre-attack/bzar

# Extract SMB admin share access
zeek-cut ts id.orig_h id.resp_h path share_type < smb_mapping.log | grep -iE '(C\$|ADMIN\$)'

# Extract DCE/RPC service creation
zeek-cut ts id.orig_h id.resp_h endpoint operation < dce_rpc.log | grep -i svcctl

# Extract failed NTLM authentications
zeek-cut ts id.orig_h id.resp_h username success < ntlm.log | awk '$5 == "F"'
```

## References

- Zeek Documentation: https://docs.zeek.org/
- BZAR (ATT&CK Zeek Analysis Rules): https://github.com/mitre-attack/bzar
- MITRE ATT&CK Lateral Movement: https://attack.mitre.org/tactics/TA0008/
- Zeek Log Formats: https://docs.zeek.org/en/master/logs/index.html
- Zeek SMB Protocol Analyzer: https://docs.zeek.org/en/master/scripts/base/protocols/smb/

---

## Standards and Controls

## MITRE ATT&CK — Lateral Movement (TA0008)
- **T1021.001** Remote Desktop Protocol
- **T1021.002** SMB/Windows Admin Shares
- **T1021.003** DCOM
- **T1021.006** Windows Remote Management
- **T1550.002** Pass the Hash
- **T1570** Lateral Tool Transfer
- **T1210** Exploitation of Remote Services

## Zeek Documentation
- [Zeek SMB Analyzer](https://docs.zeek.org/en/current/scripts/base/protocols/smb/)
- [Zeek DCE-RPC Analyzer](https://docs.zeek.org/en/current/scripts/base/protocols/dce-rpc/)
- [Zeek NTLM Analyzer](https://docs.zeek.org/en/current/scripts/base/protocols/ntlm/)
- [zeek-cut Reference](https://docs.zeek.org/en/current/auxil/zeek-cut/)

## Detection References
- SANS: Detecting Lateral Movement with Zeek
- Red Canary Threat Detection Report — Lateral Movement chapter

---

## Workflows

## Overview

This document describes the end-to-end workflow for detecting lateral movement using Zeek network logs, from data collection through investigation and response.

## Workflow Stages

### Stage 1: Data Collection

```
Network Traffic (Span/TAP)
         │
         ▼
    Zeek Sensor
         │
         ├── conn.log          (all connections)
         ├── smb_mapping.log   (SMB share access)
         ├── dce_rpc.log       (DCE/RPC calls)
         ├── ntlm.log          (NTLM authentication)
         ├── files.log          (file transfers)
         └── notice.log        (Zeek-generated alerts)
```

**Requirements:**
- Zeek deployed on network tap/span port covering internal segments
- Protocol analyzers loaded: SMB, DCE/RPC, NTLM, RDP
- Log rotation configured (recommended: daily rotation, 90-day retention)

### Stage 2: Detection Rules

Apply detection logic via Zeek scripts and/or post-processing:

| Detection | Input Logs | Method |
|---|---|---|
| Admin Share Access | smb_mapping.log | Pattern match on `C$`, `ADMIN$`, `IPC$` |
| PsExec Execution | dce_rpc.log | Match `svcctl` endpoint + `CreateServiceW` |
| RDP Pivoting | conn.log | Graph analysis: host is both RDP client and server |
| NTLM Account Spray | ntlm.log | Same user from N+ distinct sources in time window |
| DCSync | dce_rpc.log | `drsuapi` endpoint + opnum 3 from non-DC |
| Tool Transfer | files.log | PE MIME type between internal hosts |

### Stage 3: Alert Triage

```
Detection Fires
      │
      ▼
┌─────────────────┐
│  Initial Triage  │
│                   │
│ 1. Is source a    │
│    known admin    │──Yes──▶ Log & reduce priority
│    workstation?   │
│                   │
│ 2. Is activity    │
│    during change  │──Yes──▶ Verify change ticket
│    window?        │
│                   │
│ 3. Multiple       │
│    indicators?    │──Yes──▶ ESCALATE immediately
└─────────────────┘
         │
         No match
         │
         ▼
   Standard investigation
```

### Stage 4: Investigation

For each confirmed alert, follow the investigation checklist (see `assets/template.md`):

1. **Identify the source host**
   - Query `conn.log` for all connections from the source in the alert timeframe
   - Check `ntlm.log` for authentication patterns
   - Look for preceding inbound connections (initial access vector)

2. **Map the movement chain**
   ```bash
   # Build connection graph for suspect host
   cat conn.log | zeek-cut id.orig_h id.resp_h id.resp_p | \
       awk '$1 == "SUSPECT_IP" || $2 == "SUSPECT_IP"' | sort -u
   ```

3. **Identify transferred payloads**
   ```bash
   # Find files transferred by suspect
   cat files.log | zeek-cut tx_hosts rx_hosts filename mime_type total_bytes | \
       grep "SUSPECT_IP"
   ```

4. **Check authentication anomalies**
   ```bash
   # NTLM auth from suspect host
   cat ntlm.log | zeek-cut ts id.orig_h username domainname success | \
       grep "SUSPECT_IP"
   ```

5. **Timeline reconstruction**
   - Correlate all log entries by timestamp
   - Build a chronological sequence of events
   - Identify initial compromise, lateral movement, and objectives

### Stage 5: Response

| Finding | Response Action |
|---|---|
| Confirmed lateral movement | Isolate affected hosts from network |
| NTLM Account Spray detected | Force password reset for compromised accounts |
| DCSync detected | Rotate krbtgt and affected credentials, audit DC access |
| Tool transfer identified | Extract and analyze transferred files |
| RDP pivot chain | Disable RDP on non-essential hosts, enforce NLA |

### Stage 6: Post-Incident

1. **Update baselines** — Add legitimate admin share usage to allowlists
2. **Tune detections** — Adjust thresholds based on false positive analysis
3. **Document findings** — Update incident report with Zeek evidence
4. **Improve coverage** — Deploy additional Zeek scripts for newly discovered TTPs

## Automation Integration

### SIEM Forwarding

```bash
# Forward Zeek logs to SIEM via syslog
# Add to local.zeek:
@load policy/tuning/json-logs.zeek

# Configure rsyslog/filebeat to ship JSON logs to SIEM
```

### SOAR Playbook Triggers

- Admin share access from non-admin workstation → Auto-isolate + ticket
- DCSync from non-DC → Emergency alert + auto-isolate
- NTLM Account Spray threshold exceeded → Auto-disable account + alert

## Continuous Improvement

- Review detection efficacy monthly
- Test with red team exercises quarterly
- Update MITRE ATT&CK mappings as new sub-techniques emerge
- Correlate Zeek findings with endpoint telemetry (EDR) for higher fidelity

---

## Working Template

## Incident Details

| Field | Value |
|---|---|
| **Incident ID** | |
| **Date/Time Detected** | |
| **Analyst** | |
| **Detection Source** | Zeek — lateral movement detection |
| **Severity** | ☐ Critical ☐ High ☐ Medium ☐ Low |

## Initial Triage

- [ ] Review Zeek notice.log for lateral movement alerts
- [ ] Identify the suspected source host (patient zero)
- [ ] Determine the timeframe of suspicious activity
- [ ] Check if activity correlates with known maintenance/change windows
- [ ] Verify source host is not a known admin workstation

## SMB Admin Share Analysis (T1021.002)

- [ ] Query `smb_mapping.log` for admin share access (`C$`, `ADMIN$`, `IPC$`)
  ```bash
  cat smb_mapping.log | zeek-cut ts id.orig_h id.resp_h path | grep -iE '(ADMIN\$|C\$|IPC\$)'
  ```
- [ ] Identify the user account used for SMB authentication
- [ ] Check `dce_rpc.log` for `svcctl` service creation (PsExec indicator)
  ```bash
  cat dce_rpc.log | zeek-cut ts id.orig_h id.resp_h endpoint operation | grep -i svcctl
  ```
- [ ] List all hosts accessed via admin shares from the source
- [ ] Document share paths and timestamps

## RDP Pivot Analysis (T1021.001)

- [ ] Query `conn.log` for internal RDP connections
  ```bash
  cat conn.log | zeek-cut ts id.orig_h id.resp_h id.resp_p duration | awk '$4 == 3389'
  ```
- [ ] Identify hosts acting as both RDP client and server (pivot nodes)
- [ ] Map the full RDP pivot chain
- [ ] Check RDP session durations for anomalies
- [ ] Verify if RDP is authorized for identified hosts

## Pass-the-Hash Analysis (T1550.002)

- [ ] Query `ntlm.log` for multi-source authentication per user
  ```bash
  cat ntlm.log | zeek-cut ts id.orig_h username domainname success | sort -k3
  ```
- [ ] Identify accounts authenticating from 3+ distinct sources
- [ ] Check if flagged accounts are service accounts (expected multi-source)
- [ ] Determine if source hosts are authorized for the flagged accounts
- [ ] Cross-reference with Active Directory logon events

## DCSync Analysis (T1003.006)

- [ ] Query `dce_rpc.log` for `drsuapi` endpoint calls
  ```bash
  cat dce_rpc.log | zeek-cut ts id.orig_h id.resp_h endpoint operation | grep -i drsuapi
  ```
- [ ] Verify if source hosts are legitimate domain controllers
- [ ] If non-DC source detected: **ESCALATE IMMEDIATELY**
- [ ] Document source IP, destination DC, and timestamp
- [ ] Check if krbtgt or privileged accounts may be compromised

## Lateral Tool Transfer Analysis (T1570)

- [ ] Query `files.log` for executable transfers between internal hosts
  ```bash
  cat files.log | zeek-cut ts tx_hosts rx_hosts filename mime_type total_bytes | \
      grep -E 'x-dosexec|x-executable'
  ```
- [ ] Identify transferred filenames and sizes
- [ ] Extract file hashes from `files.log` for threat intelligence lookup
- [ ] Check if files were subsequently executed (correlate with endpoint logs)

## Scope Assessment

- [ ] Total number of affected hosts: ____
- [ ] Total number of compromised accounts: ____
- [ ] Earliest indicator timestamp: ____
- [ ] Latest indicator timestamp: ____
- [ ] Network segments affected: ____
- [ ] Any evidence of data exfiltration: ☐ Yes ☐ No ☐ Unknown

## Evidence Collection

- [ ] Preserve relevant Zeek logs (copy, do not modify originals)
- [ ] Capture full PCAPs for key timeframes if available
- [ ] Export timeline from `scripts/process.py` output
- [ ] Screenshot/export SIEM correlation results
- [ ] Document chain of custody

## Containment Actions

- [ ] Isolate confirmed compromised hosts from network
- [ ] Disable compromised user accounts
- [ ] Block lateral movement paths (firewall rules)
- [ ] If DCSync detected: initiate credential rotation
- [ ] If PtH detected: force password reset for affected accounts
- [ ] Restrict RDP access to authorized admin workstations only

## Post-Incident

- [ ] Update Zeek detection thresholds based on findings
- [ ] Add legitimate admin share usage to allowlists
- [ ] Document lessons learned
- [ ] Update incident response playbook
- [ ] Schedule follow-up threat hunt in 30 days
- [ ] Brief stakeholders on findings and remediation

## Notes

_Use this space for free-form investigation notes, timeline reconstruction, and analyst observations._

---

**Template version:** 1.0
**Last updated:** 2025-03-17
**MITRE ATT&CK references:** TA0008, T1021.001, T1021.002, T1550.002, T1570, T1003.006
