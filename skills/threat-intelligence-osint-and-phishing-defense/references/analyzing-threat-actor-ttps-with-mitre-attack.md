# Analyzing Threat Actor Ttps With Mitre Attack

## API Reference

## ATT&CK STIX Data

### Download
```bash
curl -o enterprise-attack.json   https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json
```

### STIX Object Types
| Type | Description |
|------|-------------|
| `attack-pattern` | Techniques and sub-techniques |
| `intrusion-set` | Threat actor groups |
| `relationship` | Links (group "uses" technique) |
| `malware` | Malware families |
| `tool` | Legitimate tools abused |

## mitreattack-python

### Installation
```bash
pip install mitreattack-python
```

### Query Techniques
```python
from mitreattack.stix20 import MitreAttackData
attack = MitreAttackData("enterprise-attack.json")

# Get all techniques
techniques = attack.get_techniques()

# Get group techniques
group = attack.get_group_by_alias("APT29")
techs = attack.get_techniques_used_by_group(group.id)
```

### Get Technique Mitigations
```python
mitigations = attack.get_mitigations_mitigating_technique(technique.id)
for m in mitigations:
    print(m.name, m.description)
```

## ATT&CK Navigator Layer Format

### Technique Entry
```json
{
  "techniqueID": "T1566.001",
  "tactic": "initial-access",
  "color": "#ff6666",
  "score": 100,
  "comment": "Spearphishing Attachment",
  "enabled": true
}
```

## ATT&CK Tactic IDs

| Tactic | ID |
|--------|----|
| Reconnaissance | TA0043 |
| Resource Development | TA0042 |
| Initial Access | TA0001 |
| Execution | TA0002 |
| Persistence | TA0003 |
| Privilege Escalation | TA0004 |
| Defense Evasion | TA0005 |
| Credential Access | TA0006 |
| Discovery | TA0007 |
| Lateral Movement | TA0008 |
| Collection | TA0009 |
| Command and Control | TA0011 |
| Exfiltration | TA0010 |
| Impact | TA0040 |

## TAXII Server Access
```python
from stix2 import TAXIICollectionSource, Filter
from taxii2client.v20 import Collection

collection = Collection(
    "https://cti-taxii.mitre.org/stix/collections/95ecc380-afe9-11e4-9b6c-751b66dd541e/"
)
src = TAXIICollectionSource(collection)
groups = src.query([Filter("type", "=", "intrusion-set")])
```

---

## Standards and Controls

## MITRE ATT&CK Framework

### Matrix Structure
- **Enterprise ATT&CK**: Windows, macOS, Linux, Cloud (AWS, Azure, GCP, SaaS, Office 365), Network, Containers
- **Mobile ATT&CK**: Android, iOS
- **ICS ATT&CK**: Industrial Control Systems

### 14 Enterprise Tactics (Kill Chain Order)
1. **Reconnaissance** (TA0043): Gathering information for planning
2. **Resource Development** (TA0042): Establishing resources for operations
3. **Initial Access** (TA0001): Gaining initial foothold
4. **Execution** (TA0002): Running adversary-controlled code
5. **Persistence** (TA0003): Maintaining access across restarts
6. **Privilege Escalation** (TA0004): Gaining higher-level permissions
7. **Defense Evasion** (TA0005): Avoiding detection
8. **Credential Access** (TA0006): Stealing credentials
9. **Discovery** (TA0007): Understanding the environment
10. **Lateral Movement** (TA0008): Moving through the environment
11. **Collection** (TA0009): Gathering data of interest
12. **Command and Control** (TA0011): Communicating with compromised systems
13. **Exfiltration** (TA0010): Stealing data
14. **Impact** (TA0040): Manipulating, interrupting, or destroying systems

### Technique Naming Convention
- **Technique**: T[NNNN] (e.g., T1059 - Command and Scripting Interpreter)
- **Sub-technique**: T[NNNN].[NNN] (e.g., T1059.001 - PowerShell)
- **Group**: G[NNNN] (e.g., G0016 - APT29)
- **Software**: S[NNNN] (e.g., S0154 - Cobalt Strike)
- **Mitigation**: M[NNNN] (e.g., M1049 - Antivirus/Antimalware)

### Data Sources
ATT&CK v16+ uses structured data sources:
- Process: Process Creation, Process Access, OS API Execution
- File: File Creation, File Modification, File Access
- Network Traffic: Network Connection Creation, Network Traffic Flow
- Command: Command Execution
- Module: Module Load
- Windows Registry: Windows Registry Key Modification

## STIX 2.1 Representation

### Attack Pattern (SDO)
Maps to ATT&CK techniques:
```json
{
  "type": "attack-pattern",
  "id": "attack-pattern--uuid",
  "name": "Spearphishing Attachment",
  "external_references": [
    {"source_name": "mitre-attack", "external_id": "T1566.001"}
  ],
  "kill_chain_phases": [
    {"kill_chain_name": "mitre-attack", "phase_name": "initial-access"}
  ]
}
```

### Intrusion Set (SDO)
Maps to ATT&CK groups:
```json
{
  "type": "intrusion-set",
  "name": "APT29",
  "aliases": ["Cozy Bear", "The Dukes", "NOBELIUM"],
  "goals": ["espionage"],
  "resource_level": "government"
}
```

## ATT&CK Navigator Layer Specification

### Layer Version 4.5 Schema
- `name`: Layer display name
- `domain`: enterprise-attack, mobile-attack, ics-attack
- `techniques[]`: Array of technique annotations
  - `techniqueID`: ATT&CK ID
  - `score`: Numeric score (0-100)
  - `color`: Hex color override
  - `comment`: Analyst notes
  - `enabled`: Show/hide technique
  - `metadata[]`: Key-value pairs for additional context

## References
- [MITRE ATT&CK Enterprise](https://attack.mitre.org/matrices/enterprise/)
- [ATT&CK STIX Data Repository](https://github.com/mitre/cti)
- [Navigator Layer Format](https://github.com/mitre-attack/attack-navigator/blob/master/layers/LAYERFORMATv4_5.md)
- [ATT&CK Design and Philosophy](https://attack.mitre.org/docs/ATTACK_Design_and_Philosophy_March_2020.pdf)

---

## Workflows

## Workflow 1: Threat Actor TTP Mapping

```
[Threat Report] --> [Extract Behaviors] --> [Map to ATT&CK] --> [Navigator Layer]
                                                                       |
                                                                       v
                                                              [Detection Priorities]
```

### Steps:
1. **Report Ingestion**: Obtain threat intelligence report (vendor, OSINT, internal)
2. **Behavior Extraction**: Identify adversary actions described in the report
3. **Technique Mapping**: Map each behavior to ATT&CK technique IDs using the ATT&CK knowledge base
4. **Sub-technique Precision**: Drill down to sub-techniques where procedure details allow
5. **Layer Creation**: Generate ATT&CK Navigator layer with mapped techniques
6. **Priority Assessment**: Rank techniques by detection feasibility and impact

## Workflow 2: Detection Gap Analysis

```
[Current Detections] --> [Detection Layer] --> [Overlay with Threat Layer] --> [Gap Layer]
                                                                                    |
                                                                                    v
                                                                          [Engineering Backlog]
```

### Steps:
1. **Detection Inventory**: Catalog existing detection rules mapped to ATT&CK techniques
2. **Detection Layer**: Create Navigator layer showing detected techniques (green)
3. **Threat Layer**: Create layer showing adversary techniques (red)
4. **Overlay Analysis**: Combine layers to identify uncovered threat techniques
5. **Gap Prioritization**: Rank gaps by threat actor relevance and detection feasibility
6. **Engineering Plan**: Create detection engineering backlog from prioritized gaps

## Workflow 3: Cross-Actor Comparison

```
[Group A TTPs] --+
                 |--> [Intersection Analysis] --> [Common Techniques] --> [Priority Detections]
[Group B TTPs] --+                                                               |
                 |                                                               v
[Group C TTPs] --+                                                    [Unique Techniques per Group]
```

### Steps:
1. **Group Selection**: Choose threat groups relevant to your industry/region
2. **TTP Extraction**: Pull technique lists for each group from ATT&CK
3. **Common Analysis**: Find techniques shared across all selected groups
4. **Unique Analysis**: Identify techniques unique to specific groups
5. **Detection ROI**: Prioritize detections for commonly used techniques (highest coverage ROI)
6. **Actor Attribution**: Use unique techniques as potential attribution indicators

## Workflow 4: Campaign-to-TTP Analysis

```
[Campaign IOCs] --> [Sandbox/Analysis] --> [Behavior Extraction] --> [TTP Mapping]
                                                                          |
                                                                          v
                                                                 [Compare to Known Groups]
                                                                          |
                                                                          v
                                                                 [Attribution Hypothesis]
```

### Steps:
1. **IOC Collection**: Gather campaign IOCs (malware hashes, C2 domains, phishing emails)
2. **Dynamic Analysis**: Execute samples in sandbox, capture behavioral artifacts
3. **Behavior Documentation**: Document file operations, registry changes, network connections, process activity
4. **ATT&CK Mapping**: Map observed behaviors to techniques and sub-techniques
5. **Group Comparison**: Compare campaign TTPs against known group profiles
6. **Attribution Assessment**: Assess likelihood of attribution based on TTP overlap

## Workflow 5: Threat-Informed Defense

```
[ATT&CK Mappings] --> [Data Source Analysis] --> [Telemetry Assessment] --> [Control Mapping]
                                                                                   |
                                                                                   v
                                                                          [Security Roadmap]
```

### Steps:
1. **Threat Profile**: Identify relevant threat actors and their techniques
2. **Data Source Mapping**: Determine which data sources can detect each technique
3. **Telemetry Audit**: Assess which data sources are currently collected
4. **Control Assessment**: Map existing security controls to technique mitigations
5. **Gap Identification**: Find techniques with neither detection nor mitigation coverage
6. **Roadmap Creation**: Build security improvement roadmap addressing highest-risk gaps

---

## Working Template

## Report Metadata
| Field | Value |
|-------|-------|
| Report ID | TTP-YYYY-NNNN |
| Date | YYYY-MM-DD |
| Threat Actor | [Group Name] |
| ATT&CK ID | G[NNNN] |
| Classification | TLP:AMBER |
| Analyst | [Name] |

## Threat Actor Profile

| Attribute | Detail |
|-----------|--------|
| Name | |
| Aliases | |
| Suspected Origin | |
| Motivation | Espionage / Financial / Disruption |
| Active Since | |
| Targeted Sectors | |
| Targeted Regions | |
| Associated Malware | |

## TTP Summary

| Tactic | Technique Count | Key Techniques |
|--------|----------------|----------------|
| Reconnaissance | | |
| Resource Development | | |
| Initial Access | | |
| Execution | | |
| Persistence | | |
| Privilege Escalation | | |
| Defense Evasion | | |
| Credential Access | | |
| Discovery | | |
| Lateral Movement | | |
| Collection | | |
| Command and Control | | |
| Exfiltration | | |
| Impact | | |

## Detailed Technique Mapping

### [Tactic Name]

| ATT&CK ID | Technique | Sub-technique | Procedure Example |
|-----------|-----------|---------------|-------------------|
| T1566.001 | Phishing | Spearphishing Attachment | Actor sends macro-enabled documents |
| | | | |

## Detection Coverage

| Status | Count | Percentage |
|--------|-------|-----------|
| Detected | | % |
| Partial Detection | | % |
| No Detection (Gap) | | % |

## Detection Gaps (Priority Order)

| Priority | ATT&CK ID | Technique | Required Data Source | Effort |
|----------|-----------|-----------|---------------------|--------|
| 1 | | | | Low/Med/High |
| 2 | | | | |

## Recommended Data Sources

| Data Source | Techniques Covered | Current Status |
|------------|-------------------|----------------|
| Process Creation | X techniques | Collecting/Not Collecting |
| Network Traffic Flow | X techniques | |
| File Monitoring | X techniques | |

## ATT&CK Navigator Layer

Layer file: `[group]_navigator_layer.json`

Load at: https://mitre-attack.github.io/attack-navigator/

## Recommendations

1. **Immediate**: Deploy detections for [top 3 gap techniques]
2. **Short-term**: Enable [data source] collection to cover N techniques
3. **Long-term**: Build behavioral analytics for [tactic] coverage
