# Performing Indicator Lifecycle Management

## API Reference

## Libraries Used
- **csv**: Parse IOC feed CSV files
- **re**: Pattern matching for IOC extraction (IP, domain, hash, URL, email, CVE)
- **pathlib**: Read text reports for IOC extraction

## CLI Interface
```
python agent.py extract --file threat_report.txt
python agent.py ingest --csv ioc_feed.csv
python agent.py expire --csv ioc_db.csv [--ttl 90]
python agent.py dedup --csv ioc_feed.csv
python agent.py report --csv ioc_db.csv [--ttl 90]
```

## Core Functions

### `extract_iocs(text_file)` — Extract IOCs from unstructured text
Regex patterns for: IPv4, domain, MD5, SHA1, SHA256, URL, email, CVE.

### `ingest_ioc_feed(csv_file)` — Normalize IOC feed data
Auto-detects IOC type if not specified. Normalizes column names across feed formats.

### `check_expiration(ioc_db_file, ttl_days)` — Identify expired indicators
Compares first_seen date against TTL threshold (default 90 days).

### `deduplicate_iocs(csv_file)` — Merge duplicate IOCs
Groups by indicator value, tracks source attribution and occurrence count.

### `generate_lifecycle_report(csv_file, ttl_days)` — Full lifecycle status
Combines ingestion, deduplication, and expiration into single report.

## IOC Pattern Types
| Type | Example |
|------|---------|
| ipv4 | 192.168.1.1 |
| domain | evil.example.com |
| md5 | d41d8cd98f00b204e9800998ecf8427e |
| sha256 | e3b0c44298fc1c149afbf4c8996fb924... |
| url | https://malware.example.com/payload |
| cve | CVE-2024-12345 |

## Dependencies
No external packages — Python standard library only.

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
