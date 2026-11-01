# Detecting Kerberoasting Attacks

## API Reference

## python-evtx Library
```python
from Evtx.Evtx import FileHeader
with open("Security.evtx", "rb") as f:
    fh = FileHeader(f)
    for record in fh.records():
        xml_string = record.xml()
```

## Event ID 4769 - Kerberos TGS Request
```xml
<EventData>
  <Data Name="TargetUserName">svc_sql</Data>
  <Data Name="ServiceName">MSSQLSvc/db01.corp.local:1433</Data>
  <Data Name="TicketEncryptionType">0x17</Data>
  <Data Name="TicketOptions">0x40810000</Data>
  <Data Name="IpAddress">::ffff:10.0.0.50</Data>
  <Data Name="Status">0x0</Data>
</EventData>
```

## Encryption Type Values
| Hex | Type | Risk |
|-----|------|------|
| 0x17 | RC4-HMAC | Kerberoasting indicator |
| 0x18 | RC4-HMAC-EXP | Kerberoasting indicator |
| 0x11 | AES128-CTS-HMAC-SHA1 | Normal |
| 0x12 | AES256-CTS-HMAC-SHA1 | Normal |

## Detection Logic
1. Filter Event 4769 where TicketEncryptionType = 0x17 (RC4)
2. Exclude machine accounts (ServiceName ending in `$`)
3. Exclude krbtgt service
4. Alert on high-volume TGS from single source (>10 unique SPNs in 5 min)
5. Correlate with Event 4624 for source attribution

## Event ID 4624 - Logon Event (Correlation)
```xml
<Data Name="TargetUserName">attacker_user</Data>
<Data Name="LogonType">3</Data>
<Data Name="IpAddress">10.0.0.50</Data>
<Data Name="WorkstationName">WORKSTATION1</Data>
```

## MITRE ATT&CK Mapping
- T1558.003 - Kerberoasting
- T1558 - Steal or Forge Kerberos Tickets

---

## Standards and Controls

## MITRE ATT&CK Mappings

| Technique | Name | Description |
|-----------|------|-------------|
| T1558.003 | Kerberoasting | See attack.mitre.org/techniques/T1558/003 |
| T1558.004 | AS-REP Roasting | See attack.mitre.org/techniques/T1558/004 |
| T1558.001 | Golden Ticket | See attack.mitre.org/techniques/T1558/001 |

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
index=wineventlog EventCode=4769 Ticket_Encryption_Type=0x17
| where Service_Name!="krbtgt" AND NOT match(Service_Name, "\\$")
| stats count dc(Service_Name) as unique_services by Account_Name Client_Address
| where unique_services > 5
| sort -unique_services
```

### KQL Query (Microsoft Defender for Endpoint)
```kql
SecurityEvent
| where EventID == 4769
| where TicketEncryptionType == "0x17"
| where ServiceName !endswith "$" and ServiceName != "krbtgt"
| summarize ServiceCount=dcount(ServiceName), Services=make_set(ServiceName) by SubjectUserName, IpAddress
| where ServiceCount > 5
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
| Hunt ID | TH-DETECT-YYYY-MM-DD-NNN |
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

- [ ] T1558.003 - Kerberoasting
- [ ] T1558.004 - AS-REP Roasting
- [ ] T1558.001 - Golden Ticket

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
