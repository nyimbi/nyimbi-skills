# Implementing SOAR Playbook With Palo Alto Xsoar

## API Reference

## Libraries Used

| Library | Purpose |
|---------|---------|
| `requests` | HTTP client for XSOAR REST API |
| `json` | Parse incident and playbook payloads |
| `os` | Read `XSOAR_URL` and `XSOAR_API_KEY` environment variables |

## Installation

```bash
pip install requests
```

## Authentication

```python
import requests
import os

XSOAR_URL = os.environ["XSOAR_URL"]  # e.g., "https://xsoar.example.com"
headers = {
    "Authorization": os.environ["XSOAR_API_KEY"],
    "Content-Type": "application/json",
    "Accept": "application/json",
}
```

## REST API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/incident` | Create a new incident |
| POST | `/incident/search` | Search incidents |
| GET | `/incident/{id}` | Get incident details |
| POST | `/incident/close` | Close an incident |
| POST | `/playbook/search` | Search playbooks |
| GET | `/playbook/{id}` | Get playbook details |
| POST | `/entry/execute/{playbook}` | Run a playbook on an incident |
| POST | `/automation/search` | Search automation scripts |
| POST | `/automation/execute` | Execute an automation command |
| GET | `/settings/integration/search` | List integrations |
| POST | `/indicators/search` | Search indicators (IOCs) |
| POST | `/indicators` | Create indicators |
| GET | `/health` | System health check |
| GET | `/user` | Get current user info |

## Core Operations

### Create an Incident
```python
incident = {
    "name": "Phishing Alert - Suspicious Email",
    "type": "Phishing",
    "severity": 3,  # 0=Unknown, 1=Low, 2=Medium, 3=High, 4=Critical
    "labels": [
        {"type": "Email/from", "value": "attacker@evil.com"},
        {"type": "Email/subject", "value": "Urgent: Verify Account"},
    ],
    "customFields": {
        "sourceemail": "attacker@evil.com",
        "reportedby": "soc-analyst-1",
    },
}
resp = requests.post(
    f"{XSOAR_URL}/incident",
    headers=headers,
    json=incident,
    timeout=30,
)
incident_id = resp.json()["id"]
```

### Search Incidents
```python
search = {
    "filter": {
        "query": "type:Phishing AND severity:>=3",
        "period": {"fromValue": "7 days ago"},
    },
    "page": 0,
    "size": 50,
}
resp = requests.post(
    f"{XSOAR_URL}/incident/search",
    headers=headers,
    json=search,
    timeout=30,
)
incidents = resp.json().get("data", [])
```

### Execute a Playbook on an Incident
```python
resp = requests.post(
    f"{XSOAR_URL}/entry/execute/{playbook_name}",
    headers=headers,
    json={"investigationId": incident_id},
    timeout=30,
)
```

### Search Playbooks
```python
resp = requests.post(
    f"{XSOAR_URL}/playbook/search",
    headers=headers,
    json={
        "query": "name:*phishing*",
        "page": 0,
        "size": 20,
    },
    timeout=30,
)
playbooks = resp.json().get("playbooks", [])
for pb in playbooks:
    print(f"{pb['name']} — tasks: {len(pb.get('tasks', {}))}")
```

### Run an Automation Command
```python
resp = requests.post(
    f"{XSOAR_URL}/automation/execute",
    headers=headers,
    json={
        "script": "!ip ip=8.8.8.8",
        "investigationId": incident_id,
    },
    timeout=60,
)
```

### Search Indicators (IOCs)
```python
resp = requests.post(
    f"{XSOAR_URL}/indicators/search",
    headers=headers,
    json={
        "query": "type:IP AND verdict:malicious",
        "size": 100,
    },
    timeout=30,
)
indicators = resp.json().get("iocObjects", [])
```

### Check Integration Health
```python
resp = requests.get(
    f"{XSOAR_URL}/settings/integration/search",
    headers=headers,
    timeout=30,
)
integrations = resp.json().get("instances", [])
for inst in integrations:
    status = "healthy" if inst.get("enabled") else "disabled"
    print(f"{inst['name']} — brand: {inst['brand']} — {status}")
```

## Output Format

```json
{
  "id": "12345",
  "name": "Phishing Alert - Suspicious Email",
  "type": "Phishing",
  "severity": 3,
  "status": 1,
  "created": "2025-01-15T10:30:00Z",
  "phase": "Triage",
  "playbooks": ["Phishing Investigation - Generic v2"],
  "labels": [
    {"type": "Email/from", "value": "attacker@evil.com"}
  ]
}
```

---

## Standards and Controls

## SOAR Industry Standards

### Gartner SOAR Definition
Security Orchestration, Automation and Response (SOAR) combines:
- Security Orchestration and Automation (SOA)
- Security Incident Response Platforms (SIRP)
- Threat Intelligence Platforms (TIP)

### NIST SP 800-61 Rev 2 - Incident Handling
SOAR playbooks implement the NIST incident response lifecycle:
1. Preparation
2. Detection and Analysis
3. Containment, Eradication, and Recovery
4. Post-Incident Activity

### MITRE ATT&CK for Response
Playbooks should map containment actions to specific MITRE ATT&CK techniques being mitigated.

## XSOAR Architecture Standards

### Content Pack Structure
```
content-pack/
  Integrations/
    integration-name/
      integration-name.py
      integration-name.yml
      integration-name_test.py
  Playbooks/
    playbook-name.yml
  Scripts/
    script-name/
      script-name.py
      script-name.yml
  IncidentTypes/
  Layouts/
  Classifiers/
```

### Playbook Design Principles
1. Modular sub-playbooks for reusability
2. Error handling on every integration command
3. Manual review gates for destructive actions
4. SLA timers for response targets
5. Closing report generation for documentation

## Integration Best Practices

| Integration Category | Examples | Usage |
|---|---|---|
| SIEM | Splunk, Sentinel, QRadar | Alert ingestion, log queries |
| EDR | CrowdStrike, Defender, SentinelOne | Endpoint isolation, hash blocking |
| Email Security | O365, Proofpoint, Mimecast | Email analysis, sender blocking |
| Threat Intelligence | VirusTotal, MISP, OTX | IOC enrichment |
| Ticketing | Jira, ServiceNow | Incident tracking |
| Communication | Slack, Teams, PagerDuty | Notifications, approvals |

---

## Workflows

## Playbook Development Lifecycle

```
1. Identify Manual Process
   - Document current analyst workflow
   - Measure time per step
   |
   v
2. Design Playbook Logic
   - Map decision points
   - Identify automation candidates
   - Define manual review gates
   |
   v
3. Build in XSOAR
   - Create playbook in visual editor
   - Configure integration commands
   - Add conditional branches
   - Write custom scripts if needed
   |
   v
4. Test with Sample Data
   - Create test incidents
   - Verify each task executes correctly
   - Test error handling paths
   |
   v
5. Pilot in Production
   - Run on subset of incidents
   - Compare automated vs manual results
   - Gather analyst feedback
   |
   v
6. Full Deployment
   - Enable for all matching incidents
   - Monitor playbook performance
   - Track MTTR improvements
   |
   v
7. Continuous Improvement
   - Review failed tasks monthly
   - Update integrations as needed
   - Add new sub-playbooks
```

## Incident Lifecycle in XSOAR

```
Alert Ingestion (SIEM/EDR/Email)
    |
    v
Pre-Processing (Classification, Deduplication)
    |
    v
Incident Created (Type, Severity, Owner assigned)
    |
    v
Playbook Triggered Automatically
    |
    +-- Enrichment Phase (parallel)
    |   |-- IP/Domain/Hash lookup
    |   |-- User/Asset lookup
    |   |-- TI feed correlation
    |
    +-- Analysis Phase
    |   |-- Verdict determination
    |   |-- Risk scoring
    |
    +-- Response Phase
    |   |-- Containment actions (auto or manual approval)
    |   |-- Eradication steps
    |   |-- Recovery procedures
    |
    +-- Documentation Phase
    |   |-- War room timeline
    |   |-- Closing report
    |   |-- Ticket update
    |
    v
Incident Closed
```

## ROI Measurement Workflow

```
Before SOAR:
  Count manual hours per incident type per month

After SOAR:
  Measure automated handling time
  Calculate: Saved Hours = Manual Hours - Automated Hours
  Calculate: ROI = (Saved Hours * Analyst Hourly Cost) / SOAR License Cost
```

---

## Working Template

## Playbook Metadata

| Field | Value |
|---|---|
| Playbook Name | |
| Version | |
| Incident Type | |
| Description | |
| Author | |
| Created Date | |
| SLA Target | |

## Playbook Logic Flow

### Phase 1: Enrichment
- [ ] Extract indicators from alert/incident
- [ ] Enrich IPs via threat intelligence
- [ ] Enrich domains via threat intelligence
- [ ] Enrich file hashes via sandbox/TI
- [ ] Query asset database for affected hosts
- [ ] Query identity store for affected users

### Phase 2: Analysis
- [ ] Determine verdict (malicious/benign/unknown)
- [ ] Calculate risk score
- [ ] Check against allowlists/blocklists
- [ ] Correlate with existing incidents

### Phase 3: Response
- [ ] Manual approval gate for destructive actions
- [ ] Containment actions
- [ ] Eradication actions
- [ ] Recovery actions

### Phase 4: Documentation
- [ ] Update incident fields
- [ ] Generate closing report
- [ ] Update ticketing system
- [ ] Notify stakeholders

## Integrations Required

| Integration | Commands Used | Purpose |
|---|---|---|
| | | |

## Error Handling

| Task | Error Type | Handling |
|---|---|---|
| | | |

## Testing Checklist

- [ ] Test with known malicious sample
- [ ] Test with known benign sample
- [ ] Test error handling paths
- [ ] Verify manual gates function correctly
- [ ] Confirm notifications are sent
- [ ] Validate closing report content
