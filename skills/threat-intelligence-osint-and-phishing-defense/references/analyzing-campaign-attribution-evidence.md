# Analyzing Campaign Attribution Evidence

## API Reference

## Diamond Model of Intrusion Analysis

### Four Core Features
| Feature | Description | Attribution Value |
|---------|-------------|-------------------|
| Adversary | Threat actor identity | Direct attribution |
| Capability | Malware, exploits, tools | Indirect - shared tooling |
| Infrastructure | C2, domains, IPs | Strong - operational overlap |
| Victim | Targets, sectors, regions | Contextual - targeting pattern |

### Pivot Analysis
```
Adversary ←→ Capability ←→ Infrastructure ←→ Victim
    ↕              ↕              ↕              ↕
  (HUMINT)     (Malware DB)   (WHOIS/DNS)   (Victimology)
```

## Analysis of Competing Hypotheses (ACH)

### Matrix Format
```
Evidence \ Hypothesis  |  APT28  |  APT29  |  Lazarus  |  Unknown
-----------------------------------------------------------------
Infrastructure overlap  |   ++    |    -    |     -     |    N
TTP consistency        |   ++    |   ++    |     -     |    N
Malware similarity     |    +    |    -    |     -     |    N
Timing (UTC+3)         |   ++    |   ++    |     -     |    N
Language (Russian)     |   ++    |   ++    |     -     |    N
```

### Scoring
| Symbol | Meaning | Weight |
|--------|---------|--------|
| `++` | Strongly consistent | +2 |
| `+` | Consistent | +1 |
| `N` | Neutral | 0 |
| `-` | Inconsistent | -1 |
| `--` | Strongly inconsistent | -2 |

## MITRE ATT&CK Group Queries

### Python (mitreattack-python)
```python
from mitreattack.stix20 import MitreAttackData
attack = MitreAttackData("enterprise-attack.json")
group = attack.get_group_by_alias("APT29")
techniques = attack.get_techniques_used_by_group(group.id)
```

### STIX2 Relationship Query
```python
from stix2 import Filter
relationships = src.query([
    Filter("type", "=", "relationship"),
    Filter("source_ref", "=", group_id),
    Filter("relationship_type", "=", "uses"),
])
```

## Infrastructure Overlap Tools

### PassiveTotal / RiskIQ
```bash
# WHOIS history
curl -u user:key "https://api.passivetotal.org/v2/whois?query=domain.com"

# Passive DNS
curl -u user:key "https://api.passivetotal.org/v2/dns/passive?query=1.2.3.4"
```

### VirusTotal Relations
```bash
curl -H "x-apikey: KEY" \
  "https://www.virustotal.com/api/v3/domains/example.com/communicating_files"
```

## Confidence Assessment Framework

| Level | Score Range | Criteria |
|-------|------------|---------|
| HIGH | 0.8-1.0 | Multiple independent evidence types converge |
| MEDIUM | 0.5-0.8 | Significant evidence with some gaps |
| LOW | 0.2-0.5 | Limited evidence, alternative hypotheses remain |
| NEGLIGIBLE | 0.0-0.2 | Insufficient evidence for attribution |

## STIX Attribution Objects

### Campaign Object
```json
{
  "type": "campaign",
  "name": "Operation DarkShadow",
  "first_seen": "2024-01-15T00:00:00Z",
  "last_seen": "2024-03-20T00:00:00Z",
  "objective": "Espionage targeting defense sector"
}
```

### Attribution Relationship
```json
{
  "type": "relationship",
  "relationship_type": "attributed-to",
  "source_ref": "campaign--abc123",
  "target_ref": "intrusion-set--def456",
  "confidence": 75
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
