# Performing Alert Triage With Elastic SIEM

## API Reference

## elasticsearch-py Client

### Connection
```python
from elasticsearch import Elasticsearch
es = Elasticsearch(
    hosts=["https://elastic:9200"],
    api_key="base64-api-key",
    verify_certs=True
)
```

### SIEM Signals Index
Elastic Security stores alerts in `.siem-signals-<space>-*` indices.

## Querying Alerts

### Search Open Alerts
```python
es.search(
    index=".siem-signals-*",
    query={"bool": {"must": [
        {"range": {"@timestamp": {"gte": "now-24h"}}},
        {"term": {"signal.status": "open"}}
    ]}},
    sort=[{"@timestamp": {"order": "desc"}}],
    size=500
)
```

### Alert Fields

| Field | Path | Description |
|-------|------|-------------|
| Rule name | `signal.rule.name` | Detection rule that triggered |
| Rule ID | `signal.rule.id` | Unique rule identifier |
| Severity | `signal.rule.severity` | critical, high, medium, low |
| Risk score | `signal.rule.risk_score` | 0-100 numeric score |
| Status | `signal.status` | open, acknowledged, closed |
| Source IP | `source.ip` | Alert source address |
| Destination IP | `destination.ip` | Alert destination address |
| User | `user.name` | Associated username |
| Host | `host.name` | Affected hostname |
| Process | `process.name` | Triggering process |

### Aggregations
```python
es.search(
    index=".siem-signals-*",
    query={"bool": {"must": [...]}},
    aggs={
        "by_severity": {"terms": {"field": "signal.rule.severity", "size": 10}},
        "by_rule": {"terms": {"field": "signal.rule.name.keyword", "size": 20}},
        "by_host": {"terms": {"field": "host.name.keyword", "size": 20}}
    },
    size=0
)
```

## Alert Status Management

### Update Alert Status
```python
es.update(
    index=".siem-signals-default-000001",
    id="alert_doc_id",
    body={"doc": {"signal": {"status": "closed"}}}
)
```

## Triage Prioritization

### Severity Priority
1. Critical (risk score 90-100)
2. High (risk score 70-89)
3. Medium (risk score 40-69)
4. Low (risk score 0-39)

### Alert Clustering
Alerts from the same host within a time window are grouped as potential incidents. Three or more alerts from the same host suggest a multi-stage attack.

## Elastic Security API

### List Detection Rules
```
GET /api/detection_engine/rules/_find?per_page=100
```

### Get Rule Execution Status
```
GET /api/detection_engine/rules/_find_statuses
```

## Output Schema

```json
{
  "report": "elastic_siem_alert_triage",
  "total_open_alerts": 45,
  "severity_summary": {"critical": 3, "high": 12, "medium": 20, "low": 10},
  "alert_clusters": [{"host": "web01", "alert_count": 5, "max_severity": "high"}],
  "aggregations": {"by_severity": [{"key": "high", "count": 12}]}
}
```

## CLI Usage

```bash
python agent.py --host https://elastic:9200 --api-key "key" --hours 24 --output report.json
```

---

## Standards and Controls

## Elastic Common Schema (ECS)

ECS is a standardized field naming convention for Elasticsearch data. All Elastic Security detections and triage workflows rely on ECS compliance.

### Key ECS Field Categories for Triage

| Category | Fields | Usage |
|---|---|---|
| Base | `@timestamp`, `message`, `tags` | Event timing and classification |
| Agent | `agent.name`, `agent.type` | Data source identification |
| Host | `host.name`, `host.ip`, `host.os` | Affected system context |
| User | `user.name`, `user.domain` | Identity attribution |
| Process | `process.name`, `process.pid`, `process.command_line` | Execution context |
| Network | `source.ip`, `destination.ip`, `destination.port` | Network activity |
| File | `file.name`, `file.hash.sha256`, `file.path` | File-related events |
| Threat | `threat.tactic.name`, `threat.technique.id` | MITRE ATT&CK mapping |

## MITRE ATT&CK Integration

Elastic Security maps detection rules and alerts to MITRE ATT&CK tactics and techniques, providing a common taxonomy for triage prioritization.

## NIST SP 800-61 Rev 2

Triage aligns with NIST incident handling phases:
- Detection and Analysis (triage is the core of this phase)
- Prioritization based on functional impact, information impact, and recoverability

## SOC Maturity Model

### Triage Capability Levels

| Level | Capability |
|---|---|
| Level 1 | Manual review of individual alerts |
| Level 2 | Grouped alert triage with correlation |
| Level 3 | AI-assisted triage with automated enrichment |
| Level 4 | Automated classification with human oversight |
| Level 5 | Fully autonomous triage with exception-based review |

---

## Workflows

## 5-Step Rapid Triage Framework

```
1. Alert Reception (30 seconds)
   - Review alert title, severity, risk score
   - Check MITRE ATT&CK mapping
   |
   v
2. Context Assessment (2 minutes)
   - Examine affected host and user
   - Check asset criticality
   - Review process tree for endpoint alerts
   |
   v
3. Intelligence Enrichment (2 minutes)
   - Check threat intelligence feeds
   - Query for related alerts (same source/user)
   - Search for known IOCs
   |
   v
4. Classification (1 minute)
   - True Positive / False Positive / Needs Investigation
   - Assign confidence level
   |
   v
5. Action (2 minutes)
   - Document findings in alert notes
   - Escalate or close with rationale
   - Create tuning task if false positive
```

## Alert Grouping Strategy

### Smart Grouping Criteria
- Time window: Group alerts within 15-minute windows
- Entity: Group by affected host or user
- Kill chain stage: Group by MITRE ATT&CK tactic
- Source: Group by originating IP or detection rule

### Group Triage Process
1. Sort alert groups by highest severity member
2. Triage group as single unit when correlated
3. Escalate entire group if attack chain detected
4. Close group if false positive pattern identified

## Shift-Based Triage Queue Management

| Queue Priority | Alert Criteria | Analyst Tier |
|---|---|---|
| Immediate | Critical severity, critical assets | Tier 2+ |
| High | High severity or multiple related alerts | Tier 1/2 |
| Standard | Medium severity, standard assets | Tier 1 |
| Low | Low/info severity, non-critical | Tier 1 (batch review) |

---

## Working Template

## Alert Information

| Field | Value |
|---|---|
| Alert ID | |
| Rule Name | |
| Severity | |
| Risk Score | |
| Timestamp | |
| MITRE Tactic | |
| MITRE Technique | |

## Affected Entities

| Entity | Value | Criticality |
|---|---|---|
| Host | | |
| User | | |
| Source IP | | |
| Destination IP | | |

## Triage Assessment

### Initial Review
- [ ] Reviewed alert details and severity
- [ ] Checked MITRE ATT&CK mapping
- [ ] Examined process tree (endpoint alerts)

### Context Gathered
- [ ] Queried related host activity
- [ ] Checked user activity history
- [ ] Searched for related alerts from same source
- [ ] Reviewed network connections

### Threat Intelligence
- [ ] Checked IPs against TI feeds
- [ ] Checked file hashes against TI feeds
- [ ] Checked domains against TI feeds

## Classification

| Classification | Selected |
|---|---|
| True Positive | [ ] |
| False Positive | [ ] |
| Benign True Positive | [ ] |
| Needs Investigation | [ ] |

## Findings

### Evidence Summary


### Analyst Notes


### Recommended Actions


## Escalation

| Field | Value |
|---|---|
| Escalated | Yes / No |
| Escalated To | |
| Incident ID | |
| Reason | |
