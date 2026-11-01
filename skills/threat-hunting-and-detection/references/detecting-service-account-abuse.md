# Detecting Service Account Abuse

## API Reference

## Active Directory PowerShell Module

### Get Service Accounts (SPN-based)
```powershell
Get-ADUser -Filter {ServicePrincipalName -ne "$null"} -Properties `
    ServicePrincipalName, LastLogonDate, Enabled, PasswordLastSet, `
    PasswordNeverExpires, AdminCount, MemberOf
```

### Get Managed Service Accounts
```powershell
Get-ADServiceAccount -Filter * -Properties `
    PrincipalsAllowedToRetrieveManagedPassword, LastLogonDate
```

### Check Kerberos Delegation
```powershell
Get-ADUser -Filter {TrustedForDelegation -eq $true} -Properties `
    TrustedForDelegation, TrustedToAuthForDelegation, `
    msDS-AllowedToDelegateTo
```

## Windows Event Log Queries

### Logon Type Values
| Type | Description | Concern for Service Accounts |
|------|-------------|------------------------------|
| 2 | Interactive | HIGH — should not happen |
| 3 | Network | Normal for services |
| 5 | Service | Normal |
| 10 | RemoteInteractive (RDP) | HIGH — should not happen |

### Event IDs
| ID | Log | Description |
|----|-----|-------------|
| 4624 | Security | Successful logon |
| 4625 | Security | Failed logon |
| 4648 | Security | Explicit credential use |
| 4672 | Security | Special privilege logon |
| 4720 | Security | Account created |
| 4738 | Security | Account modified |

## Microsoft Graph API — Service Principal Audit

### List Service Principals
```http
GET https://graph.microsoft.com/v1.0/servicePrincipals
Authorization: Bearer {token}
```

### List App Role Assignments
```http
GET https://graph.microsoft.com/v1.0/servicePrincipals/{id}/appRoleAssignments
```

### Audit Sign-In Logs
```http
GET https://graph.microsoft.com/v1.0/auditLogs/signIns
    ?$filter=appId eq '{service-principal-app-id}'
```

## AWS IAM — Service Role Audit

### List service-linked roles
```bash
aws iam list-roles --query "Roles[?starts_with(Path, '/aws-service-role/')]"
```

### Get role last used
```bash
aws iam get-role --role-name MyServiceRole \
    --query "Role.RoleLastUsed"
```

### Access Analyzer findings
```bash
aws accessanalyzer list-findings --analyzer-arn {arn} \
    --filter '{"resourceType":{"eq":["AWS::IAM::Role"]}}'
```

---

## Standards and Controls

## MITRE ATT&CK Mappings

| Technique | Name | Description |
|-----------|------|-------------|
| T1078.002 | Domain Accounts | See attack.mitre.org/techniques/T1078/002 |
| T1078.001 | Default Accounts | See attack.mitre.org/techniques/T1078/001 |
| T1021 | Remote Services | See attack.mitre.org/techniques/T1021 |

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
index=wineventlog EventCode=4624 Logon_Type IN (2, 10)
| where match(Account_Name, "(?i)(svc_|service|admin_)")
| stats count values(Computer) as hosts by Account_Name Source_Network_Address
| sort -count
```

### KQL Query (Microsoft Defender for Endpoint)
```kql
SecurityEvent
| where EventID == 4624 and LogonType in (2, 10)
| where SubjectUserName startswith "svc_" or SubjectUserName contains "service"
| summarize count(), Hosts=make_set(Computer) by SubjectUserName, IpAddress
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

- [ ] T1078.002 - Domain Accounts
- [ ] T1078.001 - Default Accounts
- [ ] T1021 - Remote Services

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
