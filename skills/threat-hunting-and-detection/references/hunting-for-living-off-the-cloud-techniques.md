# Hunting For Living Off The Cloud Techniques

## API Reference

## Libraries Used
- **elasticsearch** (elasticsearch-py): Query Elastic SIEM for cloud abuse indicators
- **re**: Pattern matching against cloud C2 domain patterns in DNS logs

## CLI Interface

```
python agent.py hunt --es-host <url> --index <pattern> [--api-key <key>] [--hours <n>]
python agent.py dns --log-file <path>
```

## Core Functions

### `hunt_lotc_elastic(es_host, es_index, api_key=None, hours=24)`
Executes five pre-built hunting queries against Elasticsearch to detect cloud service abuse.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `es_host` | str | Elasticsearch host URL (e.g., `https://es:9200`) |
| `es_index` | str | Index pattern (default: `logs-*`) |
| `api_key` | str | Optional API key for authentication |
| `hours` | int | Lookback window in hours |

**Returns:** dict with `hunts` list (each with `name`, `description`, `hits`, `events`) and `total_hits`.

### `analyze_dns_logs(log_file)`
Scans DNS query log files for connections to known cloud services used for C2, staging, and exfiltration.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `log_file` | str | Path to DNS query log file |

**Returns:** dict with `total_matches`, `findings` list, and `cloud_services_detected`.

## Hunting Queries

| Query Name | MITRE Technique | Description |
|-----------|----------------|-------------|
| `azure_storage_exfil` | T1567.002 | Large uploads to Azure Blob Storage |
| `aws_s3_staging` | T1537 | Unusual S3 bucket creation or large PutObject |
| `saas_c2_channel` | T1102 | Outbound connections to SaaS APIs (Telegram, Slack, Discord) |
| `cloud_function_invoke` | T1584.007 | Cloud function invocation via LOLBins |
| `github_raw_download` | T1105 | Payload downloads from raw GitHub content |

## Elasticsearch API Calls
- `Elasticsearch(hosts=[url], api_key=key)` — Initialize client
- `es.search(index=pattern, body=query)` — Execute search query
- Response: `resp["hits"]["total"]["value"]`, `resp["hits"]["hits"][]._source`

## Dependencies
```
pip install elasticsearch>=8.0
```

---

## Standards and Controls

## MITRE ATT&CK Mappings

| Technique | Name | Description |
|-----------|------|-------------|
| T1102 | Web Service | See attack.mitre.org/techniques/T1102 |
| T1567 | Exfiltration Over Web Service | See attack.mitre.org/techniques/T1567 |
| T1537 | Transfer Data to Cloud Account | See attack.mitre.org/techniques/T1537 |

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
index=proxy
| where match(dest, "(?i)(pastebin|discord|telegram|notion|trello|slack|github\.io|workers\.dev|azurewebsites\.net|firebaseio)")
| where method IN ("POST", "PUT")
| stats sum(bytes_out) as uploaded count by src_ip dest user
| where count > 20 OR uploaded > 10485760
```

### KQL Query (Microsoft Defender for Endpoint)
```kql
DeviceNetworkEvents
| where RemoteUrl has_any ("pastebin.com","discord.com","api.telegram.org","notion.so","trello.com")
| summarize Count=count(), BytesOut=sum(SentBytes) by DeviceName, RemoteUrl
| where Count > 20
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

- [ ] T1102 - Web Service
- [ ] T1567 - Exfiltration Over Web Service
- [ ] T1537 - Transfer Data to Cloud Account

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
