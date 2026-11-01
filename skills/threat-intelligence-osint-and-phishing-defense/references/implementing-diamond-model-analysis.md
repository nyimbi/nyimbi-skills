# Implementing Diamond Model Analysis

## API Reference

## Dependencies

| Library | Version | Purpose |
|---------|---------|---------|
| (stdlib only) | Python 3.8+ | Dataclass-based Diamond Model event modeling |

## CLI Usage

```bash
python scripts/agent.py --data /intel/events.json --output-dir /reports/
```

## Functions

### `DiamondEvent` (dataclass)
Four vertices: adversary, capability, infrastructure, victim. Plus: phase, result, confidence, notes.

### `create_event(adversary, capability, infrastructure, victim, **kwargs) -> DiamondEvent`
Factory for creating Diamond Model events with auto-generated ID and timestamp.

### `load_events(data_path) -> list`
Loads events from JSON file with `{"events": [...]}` structure.

### `pivot_on_vertex(events, vertex, value) -> list`
Analytic pivot: returns all events sharing a specific vertex value.

### `build_activity_thread(events, adversary) -> dict`
Groups events by adversary chronologically. Lists capabilities, infrastructure, victims.

### `cluster_by_infrastructure(events) -> dict`
Groups event IDs by shared infrastructure for campaign identification.

### `compute_vertex_statistics(events) -> dict`
Counts unique values per vertex and confidence distribution.

## Input Format

```json
{
  "events": [{
    "adversary": "APT29",
    "capability": "Cobalt Strike",
    "infrastructure": "185.220.101.42",
    "victim": "finance-server-01",
    "phase": "Lateral Movement",
    "confidence": "high"
  }]
}
```

## Output Schema

```json
{
  "statistics": {"total_events": 15, "unique_adversaries": 2},
  "activity_threads": [{"adversary": "APT29", "event_count": 8}],
  "infrastructure_clusters": {"185.220.101.42": ["evt1", "evt5"]}
}
```

---

## Standards and Controls

## Applicable Standards
- **STIX 2.1**: Structured Threat Information eXpression for CTI data representation
- **TAXII 2.1**: Transport protocol for sharing CTI over HTTPS
- **MITRE ATT&CK**: Adversary tactics, techniques, and procedures taxonomy
- **Diamond Model**: Intrusion analysis framework (Adversary, Capability, Infrastructure, Victim)
- **Traffic Light Protocol (TLP)**: Information sharing classification (CLEAR, GREEN, AMBER, RED)

## MITRE ATT&CK Relevance
- Technique mapping for threat actor behavior classification
- Data sources for detection capability assessment
- Mitigation strategies linked to specific techniques

## Industry Frameworks
- NIST Cybersecurity Framework (CSF) 2.0 - Identify function
- ISO 27001:2022 - A.5.7 Threat Intelligence
- FIRST Standards - TLP, CSIRT, vulnerability coordination

## References
- [STIX 2.1 Specification](https://docs.oasis-open.org/cti/stix/v2.1/stix-v2.1.html)
- [MITRE ATT&CK](https://attack.mitre.org/)
- [Diamond Model Paper](https://www.activeresponse.org/wp-content/uploads/2013/07/diamond.pdf)
- [NIST CSF 2.0](https://www.nist.gov/cyberframework)

---

## Workflows

## Workflow 1: Collection and Analysis
```
[Intelligence Sources] --> [Data Collection] --> [Analysis] --> [Reporting]
        |                        |                   |               |
        v                        v                   v               v
  OSINT/HUMINT/SIGINT    Normalize/Enrich    Assess/Correlate  Disseminate
```

### Steps:
1. **Planning**: Define intelligence requirements and collection priorities
2. **Collection**: Gather data from relevant sources
3. **Processing**: Normalize data formats and filter noise
4. **Analysis**: Apply analytical frameworks and correlate findings
5. **Production**: Generate intelligence products and reports
6. **Dissemination**: Share with stakeholders via appropriate channels
7. **Feedback**: Collect consumer feedback to refine future collection

## Workflow 2: Continuous Monitoring
```
[Watchlist] --> [Automated Monitoring] --> [Change Detection] --> [Alert/Update]
```

### Steps:
1. **Define Watchlist**: Identify indicators, actors, and topics to monitor
2. **Configure Monitoring**: Set up automated collection from relevant sources
3. **Change Detection**: Identify new or changed intelligence
4. **Assessment**: Evaluate significance of changes
5. **Alerting**: Notify stakeholders of significant intelligence updates
6. **Archive**: Store intelligence for historical analysis and trending

---

## Working Template

## Report Metadata
| Field | Value |
|-------|-------|
| Report ID | CTI-YYYY-NNNN |
| Date | YYYY-MM-DD |
| Classification | TLP:AMBER |
| Analyst | [Name] |
| Confidence | High/Moderate/Low |

## Executive Summary
[Brief overview of key findings and their significance]

## Key Findings
1. [Finding 1 with supporting evidence]
2. [Finding 2 with supporting evidence]
3. [Finding 3 with supporting evidence]

## Detailed Analysis
### Finding 1
- **Evidence**: [Description of evidence]
- **Confidence**: High/Moderate/Low
- **MITRE ATT&CK**: [Relevant technique IDs]
- **Impact Assessment**: [Potential impact to organization]

## Indicators of Compromise
| Type | Value | Context | Confidence |
|------|-------|---------|-----------|
| | | | |

## Recommendations
1. **Immediate**: [Actions requiring immediate attention]
2. **Short-term**: [Actions within 1-2 weeks]
3. **Long-term**: [Strategic improvements]

## References
- [Source 1]
- [Source 2]
