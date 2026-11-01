# Detecting Insider Threat Behaviors

## API Reference

## Risk Indicator Weights

| Indicator | Weight | Description |
|-----------|--------|-------------|
| resignation_correlated | 35 | Activity after resignation notice |
| privilege_escalation | 30 | Unauthorized privilege use |
| usb_mass_copy | 30 | Mass copy to removable media |
| mass_download | 25 | Bulk file download/copy (>50 files) |
| unusual_destination | 20 | Data sent to unusual destination |
| cloud_upload | 20 | Upload to personal cloud storage |
| off_hours_access | 15 | Activity outside 8am-6pm |
| email_to_personal | 15 | Forwarding to personal email |

## UEBA Data Sources

| Source | Indicators |
|--------|------------|
| DLP logs | File downloads, USB copies, email attachments |
| Proxy logs | Cloud storage uploads, personal email |
| VPN logs | Off-hours access, unusual locations |
| AD logs | Privilege changes, group modifications |
| Endpoint logs | Application usage, screen captures |

## Splunk SPL - Mass Download Detection

```spl
index=dlp action IN ("download", "copy", "export")
| bin _time span=1h
| stats count by user, _time
| where count > 50
| sort -count
```

## Microsoft Sentinel - Off-Hours Access

```kql
SigninLogs
| where TimeGenerated between (datetime(22:00)..datetime(06:00))
| where ResultType == 0
| summarize count() by UserPrincipalName, bin(TimeGenerated, 1h)
| where count_ > 5
```

## Personal Cloud Domains

```python
CLOUD_STORAGE = {
    "dropbox.com", "drive.google.com",
    "onedrive.live.com", "box.com",
    "mega.nz", "wetransfer.com"
}
```

## Risk Score Calculation

```python
score = sum(RISK_INDICATORS[ind]["weight"] for ind in detected_indicators)
risk = "CRITICAL" if score >= 80 else "HIGH" if score >= 50 else "MEDIUM"
```

## CLI Usage

```bash
python agent.py --activity-log user_activity.jsonl
python agent.py --activity-log events.csv --download-threshold 100
```

---

## Standards and Controls

## MITRE ATT&CK Mappings

| Technique | Name | Description |
|-----------|------|-------------|
| T1078 | Valid Accounts | See attack.mitre.org/techniques/T1078 |
| T1530 | Data from Cloud Storage Object | See attack.mitre.org/techniques/T1530 |
| T1567 | Exfiltration Over Web Service | See attack.mitre.org/techniques/T1567 |

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
index=wineventlog EventCode=5145
| where match(Share_Name, "(?i)(finance|hr|legal|confidential|executive)")
| stats count dc(Relative_Target_Name) as unique_files by Account_Name Source_Address
| where unique_files > 100
| sort -unique_files
```

### KQL Query (Microsoft Defender for Endpoint)
```kql
CloudAppEvents
| where ActionType in ("FileDownloaded","FileCopied","FileShared")
| summarize FileCount=count(), UniqueFiles=dcount(ObjectName) by AccountObjectId, IPAddress
| where FileCount > 100
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

- [ ] T1078 - Valid Accounts
- [ ] T1530 - Data from Cloud Storage Object
- [ ] T1567 - Exfiltration Over Web Service

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
