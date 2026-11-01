# Hunting For Unusual Network Connections

## API Reference

## Connection Analysis Indicators

| Indicator | Threshold | Severity |
|-----------|-----------|----------|
| Known bad port (4444, 31337) | Any connection | CRITICAL |
| Non-standard port | Not in common set | MEDIUM |
| Rare destination (< 3 conns) | Unique in environment | HIGH |
| Long connection (> 1hr) | Duration > 3600s | HIGH |
| Periodic beaconing (CV < 0.3) | Low interval variance | CRITICAL |

## Splunk SPL - Rare Destinations

```spl
index=firewall action=allowed
| stats dc(src_ip) as src_count count by dest_ip dest_port
| where src_count == 1 AND count < 5
| sort -count
| table dest_ip dest_port count src_count
```

## KQL - Non-Standard Ports

```kql
DeviceNetworkEvents
| where RemotePort !in (80, 443, 53, 22, 25, 8080)
| summarize ConnectionCount=count(), dcount(DeviceId) by RemoteIP, RemotePort
| where ConnectionCount < 5
| sort by ConnectionCount asc
```

## Zeek conn.log Analysis

```python
from zat.log_to_dataframe import LogToDataFrame
df = LogToDataFrame().create_dataframe("conn.log")
# Filter rare external destinations
external = df[~df["id.resp_h"].str.startswith(("10.", "172.16.", "192.168."))]
rare = external.groupby("id.resp_h").size().reset_index(name="count")
rare = rare[rare["count"] < 3]
```

## Beaconing Detection

```python
import numpy as np
intervals = np.diff(sorted_timestamps)
cv = np.std(intervals) / np.mean(intervals)
# CV < 0.3 = high periodicity (likely beacon)
```

## Sysmon Event ID 3 (Network Connection)

```xml
<EventData>
  <Data Name="Image">C:\Windows\System32\svchost.exe</Data>
  <Data Name="DestinationIp">203.0.113.50</Data>
  <Data Name="DestinationPort">4444</Data>
</EventData>
```

### References

- MITRE T1071: https://attack.mitre.org/techniques/T1071/
- MITRE T1571: https://attack.mitre.org/techniques/T1571/
- ZAT: https://github.com/SuperCowPowers/zat
- Sysmon: https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon

---

## Standards and Controls

## MITRE ATT&CK Mappings

| Technique | Name | Description |
|-----------|------|-------------|
| T1071 | Application Layer Protocol | See attack.mitre.org/techniques/T1071 |
| T1095 | Non-Application Layer Protocol | See attack.mitre.org/techniques/T1095 |
| T1571 | Non-Standard Port | See attack.mitre.org/techniques/T1571 |

## Detection Data Sources

| Source | Event ID | Purpose |
|--------|----------|---------|
| Sysmon | 1 | Process creation with command line |
| Sysmon | 3 | Network connection initiated |
| Sysmon | 7 | Image loaded (DLL) |
| Sysmon | 10 | Process access (LSASS) |
| Sysmon | 11 | File creation |
| Sysmon | 12/13 | Registry create/set |
| Sysmon | 22 | DNS query |
| Sysmon | 25 | Process tampering |
| Windows Security | 4624 | Successful logon |
| Windows Security | 4625 | Failed logon |
| Windows Security | 4648 | Explicit credential logon |
| Windows Security | 4672 | Special privileges assigned |
| Windows Security | 4688 | Process creation |
| Windows Security | 4697 | Service installed |
| Windows Security | 4698 | Scheduled task created |
| Windows Security | 4769 | Kerberos TGS requested |
| Windows Security | 5140 | Network share accessed |

## References

- MITRE ATT&CK Framework: https://attack.mitre.org/
- Sigma Detection Rules: https://github.com/SigmaHQ/sigma
- LOLBAS Project: https://lolbas-project.github.io/
- Atomic Red Team Tests: https://github.com/redcanaryco/atomic-red-team
- Red Canary Threat Detection Report
- SANS Threat Hunting Summit Resources

---

## Workflows

## Phase 1: Data Collection and Querying

### Splunk SPL Query
```spl
index=sysmon EventCode=3
| where NOT match(DestinationIp, "^(10\\.|172\\.(1[6-9]|2[0-9]|3[01])\\.|192\\.168\\.)")
| stats count dc(DestinationIp) as unique_ips values(DestinationPort) as ports by Image Computer
| where count > 50 OR unique_ips > 10
| sort -count
```

### KQL Query (Microsoft Defender for Endpoint)
```kql
DeviceNetworkEvents
| where RemoteIPType == "Public"
| summarize ConnectionCount=count(), UniqueIPs=dcount(RemoteIP), Ports=make_set(RemotePort) by InitiatingProcessFileName, DeviceName
| where ConnectionCount > 50 or UniqueIPs > 10
```

## Phase 2: Baseline and Anomaly Detection

### Step 2.1 - Establish Normal Behavior Baseline
- Collect 30 days of historical data for the targeted technique
- Document expected patterns, frequencies, and legitimate use cases
- Identify known false positive sources and document exceptions
- Build statistical baseline (mean, standard deviation) for key metrics

### Step 2.2 - Identify Anomalies
- Compare current activity against the 30-day baseline
- Flag events exceeding 3 standard deviations from normal
- Prioritize anomalies by risk score and potential business impact
- Cross-reference with threat intelligence for known IOCs

## Phase 3: Investigation and Correlation

### Step 3.1 - Deep Dive Analysis
- For each anomaly, collect full process tree context
- Correlate with network activity, file operations, and authentication events
- Check binary signatures, file hashes, and certificate validity
- Review user account context and access patterns

### Step 3.2 - Attack Chain Reconstruction
- Map findings to MITRE ATT&CK kill chain stages
- Identify initial access vector if applicable
- Trace lateral movement and privilege escalation paths
- Determine data access and potential exfiltration

## Phase 4: Validation and Response

### Step 4.1 - True/False Positive Determination
- Verify findings with system owners and IT operations
- Check change management records for authorized activities
- Validate user context (authorized actions vs. compromised account)
- Document determination rationale for each finding

### Step 4.2 - Response Actions
- For confirmed threats: initiate incident response procedures
- For detection gaps: create or update detection rules
- For false positives: tune existing rules and update exclusions
- Update threat hunting playbook with lessons learned

## Phase 5: Documentation and Reporting

### Step 5.1 - Hunt Report
- Summarize hypothesis, methodology, and findings
- Include all queries executed and their results
- Document IOCs discovered and detection rules created
- Provide recommendations for security improvements

### Step 5.2 - Knowledge Base Update
- Add findings to threat intelligence platform
- Update MITRE ATT&CK coverage heatmap
- Share detection rules via Sigma format
- Schedule follow-up hunts for related techniques

---

## Working Template

## Hunt Metadata

| Field | Value |
|-------|-------|
| Hunt ID | TH-HUNTIN-YYYY-MM-DD-NNN |
| Analyst | |
| Date Started | |
| Date Completed | |
| Status | [ ] In Progress / [ ] Complete |
| Priority | [ ] Critical / [ ] High / [ ] Medium / [ ] Low |

## Hypothesis

> **Statement**: [Formulate a clear, testable hypothesis]
>
> **Basis**: [ ] Threat Intel / [ ] ATT&CK Gap / [ ] Anomaly / [ ] Incident Follow-up

## Target Techniques

- [ ] T1071 - Application Layer Protocol
- [ ] T1095 - Non-Application Layer Protocol
- [ ] T1571 - Non-Standard Port

## Data Sources

- [ ] Sysmon Event Logs
- [ ] Windows Security Event Logs
- [ ] EDR Telemetry (Platform: _____________)
- [ ] SIEM (Platform: _____________)
- [ ] Network Logs (Proxy/Firewall/DNS)
- [ ] Cloud Audit Logs
- [ ] Email Gateway Logs
- [ ] Application Logs

## Queries Executed

### Query 1: [Description]
```
[Query text]
```
**Results**: [Count] events | **Execution Time**: [Duration]

### Query 2: [Description]
```
[Query text]
```
**Results**: [Count] events | **Execution Time**: [Duration]

## Findings

| # | Timestamp | Host | User | Technique | Evidence Summary | Risk | Verdict |
|---|-----------|------|------|-----------|-----------------|------|---------|
| 1 | | | | | | | TP / FP / BTP |
| 2 | | | | | | | TP / FP / BTP |
| 3 | | | | | | | TP / FP / BTP |

## IOCs Discovered

### Network IOCs
| Type | Value | Context | Confidence |
|------|-------|---------|-----------|
| IP | | | |
| Domain | | | |
| URL | | | |

### Host IOCs
| Type | Value | Context | Confidence |
|------|-------|---------|-----------|
| SHA256 | | | |
| Filename | | | |
| Registry Key | | | |
| Scheduled Task | | | |

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

## Hypothesis Outcome

- [ ] **Confirmed**: Evidence supports the hypothesis
- [ ] **Partially Confirmed**: Some evidence found, further investigation needed
- [ ] **Refuted**: No evidence found
- [ ] **Inconclusive**: Insufficient data

## Recommendations

1. **Immediate Actions**: [Containment, remediation steps]
2. **Detection Improvements**: [New rules, tuning recommendations]
3. **Visibility Gaps**: [Missing data sources, coverage needs]
4. **Security Hardening**: [Configuration changes, policy updates]
5. **Follow-up Hunts**: [Related hypotheses to investigate]

## Analyst Notes

[Free-form notes, observations, and lessons learned]
