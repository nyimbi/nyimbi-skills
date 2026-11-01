# Building Detection Rule With Splunk Spl

## API Reference

## Splunk REST API - Saved Searches
```
POST /servicesNS/{owner}/{app}/saved/searches
Authorization: Bearer TOKEN
```
| Field | Description |
|-------|-------------|
| `name` | Saved search name |
| `search` | SPL query string |
| `is_scheduled` | 1 for scheduled |
| `cron_schedule` | Cron expression (e.g., `*/5 * * * *`) |
| `dispatch.earliest_time` | Start of search window |
| `alert.severity` | 1-5 (info to critical) |
| `alert_type` | `number of events` |
| `alert_threshold` | Trigger threshold |

## Key SPL Commands
| Command | Description |
|---------|-------------|
| `stats count by field` | Aggregate events |
| `where count > N` | Filter results |
| `table field1, field2` | Select fields |
| `eval` | Compute new fields |
| `lookup` | Enrich from lookup table |
| `tstats` | Accelerated data model search |
| `join` | Join two datasets |

## Windows Event IDs for Detection
| EventCode | Source | Description |
|-----------|--------|-------------|
| 4624 | Security | Successful logon |
| 4625 | Security | Failed logon |
| 4648 | Security | Explicit credential logon |
| 4698 | Security | Scheduled task created |
| 4104 | PowerShell | Script block logging |
| 1 | Sysmon | Process creation |
| 3 | Sysmon | Network connection |
| 10 | Sysmon | Process access |

## Alert Severity Levels
| Level | Value | Description |
|-------|-------|-------------|
| Info | 1 | Informational |
| Low | 2 | Low risk |
| Medium | 3 | Medium risk |
| High | 4 | High risk |
| Critical | 5 | Critical risk |

---

## Standards and Controls

## Industry Standards

### MITRE ATT&CK Framework
- Primary mapping standard for detection rule categorization
- Version 18.1 (December 2025) is the latest release
- Use ATT&CK Navigator for visual coverage mapping

### Splunk Common Information Model (CIM)
- Standard field naming convention for normalized data
- Data models: Authentication, Network_Traffic, Endpoint, Web, Email
- Enables cross-sourcetype correlation searches

### NIST SP 800-92 - Guide to Computer Security Log Management
- Log management planning and policy guidance
- Defines log collection, analysis, and retention best practices

### NIST SP 800-61 Rev 2 - Computer Security Incident Handling Guide
- Incident detection and analysis procedures
- Defines severity classification for generated alerts

## Splunk Enterprise Security Resources

### Correlation Search Framework
- Supports scheduled searches with adaptive response actions
- Risk-based alerting (RBA) aggregates risk events by entity
- Notable events are the primary output for SOC analyst review

### Data Model Acceleration
- tstats provides fast summary-based searching
- Accelerated data models required for production correlation searches
- CIM compliance ensures cross-source detection capability

### Key Splunk SPL Commands for Detection

| Command | Purpose |
|---|---|
| `stats` | Aggregate events by fields |
| `tstats` | Fast search over accelerated data models |
| `eventstats` | Add aggregated stats inline to events |
| `streamstats` | Running statistics over ordered events |
| `transaction` | Group related events into transactions |
| `lookup` | Enrich events with external data |
| `where` | Filter results with boolean expressions |
| `eval` | Create calculated fields |

## Detection Engineering Maturity Model

### Level 1 - Basic Threshold Rules
- Simple count-based thresholds
- Single data source correlation

### Level 2 - Multi-Source Correlation
- Cross-source event correlation
- Asset and identity enrichment

### Level 3 - Behavioral Analytics
- Baseline deviation detection
- User and entity behavior profiling

### Level 4 - Risk-Based Alerting
- Cumulative risk scoring per entity
- Context-aware severity assignment

### Level 5 - Automated Response
- Adaptive response action integration
- SOAR playbook triggering from notable events

---

## Workflows

## Detection Rule Development Workflow

```
1. Identify Threat Scenario
   |
   v
2. Map to MITRE ATT&CK Technique
   |
   v
3. Identify Required Data Sources
   |
   v
4. Validate Data Availability in Splunk
   |
   v
5. Write Base SPL Query
   |
   v
6. Add Aggregation and Filtering
   |
   v
7. Add Enrichment (Lookups, Threat Intel)
   |
   v
8. Test Against Historical Data
   |
   v
9. Calculate False Positive Rate
   |
   v
10. Deploy as Correlation Search
    |
    v
11. Monitor Detection Metrics
    |
    v
12. Tune and Iterate
```

## Rule Testing Workflow

### Phase 1: Development
- Write SPL query in Search & Reporting
- Test with `earliest=-7d latest=now()`
- Verify expected events are captured

### Phase 2: Validation
- Run Atomic Red Team tests to generate known-bad events
- Confirm detection triggers on simulated attacks
- Check no duplicate or redundant notable events generated

### Phase 3: Tuning
- Identify false positives from 7-day burn-in period
- Add exclusions for known benign activity
- Adjust thresholds based on environment baseline

### Phase 4: Production
- Schedule as correlation search in ES
- Configure adaptive response actions
- Set notable event severity and urgency mapping

## Correlation Search Scheduling Guide

| Rule Severity | Schedule Interval | Time Window |
|---|---|---|
| Critical | Every 5 minutes | 10 minutes |
| High | Every 15 minutes | 20 minutes |
| Medium | Every 30 minutes | 35 minutes |
| Low | Every 60 minutes | 65 minutes |
| Informational | Every 4 hours | 4.5 hours |

Note: Time window should slightly exceed schedule interval to prevent event gaps.

## Alert Output Workflow

```
Correlation Search Fires
    |
    v
Notable Event Created in ES
    |
    v
SOC Analyst Reviews in Incident Review Dashboard
    |
    v
Analyst Triages: True Positive / False Positive / Needs Investigation
    |
    v
True Positive --> Create Investigation --> Escalate if needed
False Positive --> Document exclusion --> Update correlation search
```

---

## Working Template

## Rule Metadata

| Field | Value |
|---|---|
| Rule Name | |
| Rule ID | |
| Description | |
| Author | |
| Date Created | |
| Last Modified | |
| Severity | |
| MITRE ATT&CK | |
| Data Sources | |
| Status | Draft / Testing / Production / Retired |

## SPL Query

```spl
| tstats summariesonly=true count
    from datamodel=<DataModel>
    where <conditions>
    by <fields>, _time span=<interval>
| rename "<DataModel>.*" as *
| stats <aggregation> by <grouping_fields>
| where <threshold_condition>
| lookup asset_lookup ip as src OUTPUT asset_name, asset_priority
| lookup identity_lookup identity as user OUTPUT department, manager
| eval severity=case(<critical_condition>, "critical", <high_condition>, "high", true(), "medium")
| eval description="<dynamic description string>"
| eval mitre_technique="<T-number>"
```

## Detection Logic

### What This Rule Detects
<!-- Describe the adversary behavior being detected -->

### Data Sources Required
<!-- List all required data sources and their sourcetypes -->

| Source | Sourcetype | Index | Required Fields |
|---|---|---|---|
| | | | |

### Threshold Justification
<!-- Explain why the threshold values were chosen -->

### Enrichment Details
<!-- List lookups and threat intel sources used -->

## Testing Plan

### True Positive Test
<!-- Describe how to simulate the attack to validate detection -->

```
Step 1:
Step 2:
Step 3:
Expected Result:
```

### False Positive Analysis
<!-- Document known benign scenarios that trigger this rule -->

| Scenario | Source | Mitigation |
|---|---|---|
| | | |

## Tuning History

| Date | Change | Reason | Impact |
|---|---|---|---|
| | | | |

## Correlation Search Configuration

```
Schedule: */15 * * * *
Time Window: earliest=-20m latest=now
Suppress: 1h by src_ip
Notable Event Security Domain: threat
Adaptive Response: <actions>
```

## Analyst Guidance

### Triage Steps
1.
2.
3.

### Escalation Criteria
-

### Related Rules
-
