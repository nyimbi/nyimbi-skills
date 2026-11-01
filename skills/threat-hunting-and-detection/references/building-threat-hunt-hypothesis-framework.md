# Building Threat Hunt Hypothesis Framework

## API Reference

## Hypothesis Structure
| Field | Description |
|-------|------------|
| hypothesis_id | Unique identifier (HYP-XXXXXXXX) |
| technique_id | MITRE ATT&CK technique (e.g. T1059.001) |
| hypothesis_statement | Natural language hypothesis |
| data_sources | Required log sources |
| priority | high / medium / low |
| status | planned / in_progress / completed |

## MITRE ATT&CK Data Sources
```bash
# Download ATT&CK STIX bundle
curl -O https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json

# Filter attack-pattern objects for technique data sources
python3 -c "
import json
bundle = json.load(open('enterprise-attack.json'))
for obj in bundle['objects']:
    if obj.get('type') == 'attack-pattern' and not obj.get('x_mitre_deprecated'):
        eid = obj['external_references'][0]['external_id']
        ds = [d['source_name'] for d in obj.get('x_mitre_data_sources', [])]
        print(f'{eid}: {ds}')
"
```

## Hunt Maturity Model (HMM)
| Level | Name | Description |
|-------|------|------------|
| HM0 | Initial | Ad hoc, no documented procedures |
| HM1 | Minimal | Basic procedures, limited data sources |
| HM2 | Procedural | Documented hypotheses, repeatable hunts |
| HM3 | Innovative | Custom analytics, TI-driven hypotheses |
| HM4 | Leading | Automated, ML-assisted, continuous hunting |

## Key Windows Event IDs for Hunting
| Event ID | Source | Use Case |
|----------|--------|----------|
| 4104 | PowerShell | Script block logging |
| 4688 | Security | Process creation |
| 4624/4625 | Security | Logon success/failure |
| 4698 | Security | Scheduled task created |
| 1 (Sysmon) | Sysmon | Process create with hashes |
| 3 (Sysmon) | Sysmon | Network connection |
| 10 (Sysmon) | Sysmon | Process access (LSASS) |
| 11 (Sysmon) | Sysmon | File create |

## Sigma Rule Integration
```yaml
title: Suspicious PowerShell Execution
status: experimental
logsource:
    product: windows
    service: powershell
detection:
    selection:
        EventID: 4104
        ScriptBlockText|contains:
            - 'Invoke-Mimikatz'
            - 'Invoke-Expression'
    condition: selection
level: high
```

---

## Standards and Controls

## MITRE ATT&CK Mappings

| Technique | Name | Description |
|-----------|------|-------------|
| TA0001 | Initial Access | See attack.mitre.org/techniques/TA0001 |
| TA0003 | Persistence | See attack.mitre.org/techniques/TA0003 |
| TA0008 | Lateral Movement | See attack.mitre.org/techniques/TA0008 |
| TA0010 | Exfiltration | See attack.mitre.org/techniques/TA0010 |

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
| makeresults
| eval hypothesis="Adversaries may be using [TECHNIQUE] to [OBJECTIVE] against [TARGET] via [VECTOR]"
| eval data_sources="[List required data sources]"
| eval queries="[Specific SPL queries to test hypothesis]"
| eval success_criteria="[What constitutes confirming/refuting hypothesis]"
```

### KQL Query (Microsoft Defender for Endpoint)
```kql
let HuntHypothesis = datatable(Component:string, Description:string)
[
    "Technique", "MITRE ATT&CK technique being hunted",
    "Target", "Systems or accounts in scope",
    "Data Sources", "Logs and telemetry required",
    "Indicators", "Observable evidence of technique",
    "Success Criteria", "What confirms or refutes hypothesis"
];
HuntHypothesis
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
| Hunt ID | TH-BUILDI-YYYY-MM-DD-NNN |
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

- [ ] TA0001 - Initial Access
- [ ] TA0003 - Persistence
- [ ] TA0008 - Lateral Movement
- [ ] TA0010 - Exfiltration

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
