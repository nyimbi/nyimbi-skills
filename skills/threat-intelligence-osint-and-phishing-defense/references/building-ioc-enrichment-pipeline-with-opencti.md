# Building IOC Enrichment Pipeline With Opencti

## API Reference

## pycti — OpenCTI Python Client

### Installation
```bash
pip install pycti
```

### Client Initialization
```python
from pycti import OpenCTIApiClient

client = OpenCTIApiClient(
    url="http://localhost:8080",
    token=os.environ.get("OPENCTI_TOKEN", "")
)
```

### Indicator Operations
```python
# List indicators with filter
filters = {
    "mode": "and",
    "filters": [{"key": "value", "values": ["198.51.100.42"]}],
    "filterGroups": []
}
indicators = client.indicator.list(filters=filters)

# Create indicator
client.indicator.create(
    name="Malicious IP",
    pattern="[ipv4-addr:value = '198.51.100.42']",
    pattern_type="stix",
    x_opencti_score=80,
    valid_from="2025-01-01T00:00:00Z"
)
```

### Observable Operations
```python
# Search observables
obs = client.stix_cyber_observable.list(filters=filters)

# Create observable
client.stix_cyber_observable.create(
    observableData={
        "type": "ipv4-addr",
        "value": "198.51.100.42"
    }
)
```

### Relationship Queries
```python
# Get relationships from entity
rels = client.stix_core_relationship.list(
    filters={
        "mode": "and",
        "filters": [{"key": "fromId", "values": [entity_id]}],
        "filterGroups": []
    }
)
```

## OpenCTI GraphQL API

### Endpoint
```
POST /graphql
Authorization: Bearer <token>
Content-Type: application/json
```

### Example Query
```graphql
query {
  indicators(filters: {
    mode: and
    filters: [{ key: "value", values: ["198.51.100.42"] }]
    filterGroups: []
  }) {
    edges {
      node {
        id
        pattern
        x_opencti_score
        createdBy { name }
        objectLabel { value }
      }
    }
  }
}
```

## STIX Indicator Patterns
| Type | STIX Pattern |
|------|-------------|
| IPv4 |  |
| Domain |  |
| URL |  |
| SHA-256 |  |
| MD5 |  |
| Email |  |

---

## Standards and Controls

## STIX 2.1 (Native Data Model for OpenCTI)

### STIX Domain Objects (SDOs)
- **Indicator**: Contains detection patterns (STIX patterning, YARA, Sigma)
- **Malware**: Represents malware families and variants
- **Threat Actor**: Describes adversary groups and individuals
- **Campaign**: Groups related intrusion activity
- **Attack Pattern**: Maps to MITRE ATT&CK techniques
- **Infrastructure**: Represents adversary-owned systems (C2, exploit kits)
- **Tool**: Legitimate software used by adversaries

### STIX Cyber Observables (SCOs)
- **IPv4-Addr / IPv6-Addr**: Network addresses
- **Domain-Name**: DNS domain names
- **URL**: Full URL indicators
- **StixFile**: File hashes (MD5, SHA-1, SHA-256)
- **Email-Addr**: Email addresses
- **Artifact**: Binary content (malware samples)
- **Process**: Running process information
- **Network-Traffic**: Network flow data

### STIX Relationship Objects (SROs)
- **Relationship**: Connects two SDOs (e.g., Threat Actor "uses" Malware)
- **Sighting**: Records observation of an indicator or malware

## OpenCTI Connector Standards

### Connector Types
1. **EXTERNAL_IMPORT**: Ingest data from external sources (MISP, TAXII feeds)
2. **INTERNAL_IMPORT_FILE**: Parse uploaded files (PDF reports, STIX bundles)
3. **INTERNAL_ENRICHMENT**: Enrich existing observables with external data
4. **INTERNAL_ANALYSIS**: Analyze content for indicators
5. **STREAM**: Real-time export to external systems (SIEM, SOAR)

### Connector Communication Protocol
- Connectors communicate via RabbitMQ message queues
- Messages contain STIX 2.1 bundles in JSON format
- Enrichment connectors receive entity_id and return STIX bundles
- Rate limiting and retry logic handled by connector framework

## Enrichment Service APIs

### VirusTotal v3 API
- Endpoint: `https://www.virustotal.com/api/v3/`
- Resources: files, urls, domains, ip_addresses
- Rate limits: 4 requests/minute (free), 1000/minute (premium)
- Returns: detection ratios, behavioral analysis, relationships

### Shodan API
- Endpoint: `https://api.shodan.io/`
- Resources: host/{ip}, dns/resolve, search
- Returns: open ports, services, banners, vulnerabilities, ASN info

### AbuseIPDB v2 API
- Endpoint: `https://api.abuseipdb.com/api/v2/`
- Resources: check, reports, blacklist
- Returns: abuse confidence score, total reports, categories, country

### GreyNoise v3 API
- Endpoint: `https://api.greynoise.io/v3/`
- Resources: community/{ip}, noise/context/{ip}
- Returns: classification (benign/malicious/unknown), RIOT status, tags

## MITRE ATT&CK Framework
- OpenCTI maps Attack Patterns to ATT&CK techniques
- Supports Enterprise, Mobile, and ICS matrices
- Technique relationships enable campaign-level analysis
- Sub-technique granularity (e.g., T1059.001 - PowerShell)

## References
- [OpenCTI Documentation](https://docs.opencti.io/)
- [STIX 2.1 Specification](https://docs.oasis-open.org/cti/stix/v2.1/stix-v2.1.html)
- [OpenCTI GitHub](https://github.com/OpenCTI-Platform/opencti)
- [OpenCTI Connectors Ecosystem](https://docs.opencti.io/latest/deployment/connectors/)
- [VirusTotal API v3](https://docs.virustotal.com/reference/overview)

---

## Workflows

## Workflow 1: Automatic Enrichment Pipeline

```
[New Observable Created] --> [RabbitMQ Queue] --> [Enrichment Connectors]
                                                        |
                                            +-----------+-----------+
                                            |           |           |
                                            v           v           v
                                      [VirusTotal] [Shodan]  [AbuseIPDB]
                                            |           |           |
                                            v           v           v
                                     [STIX Bundle] [STIX Bundle] [STIX Bundle]
                                            |           |           |
                                            +-----------+-----------+
                                                        |
                                                        v
                                              [Merged into OpenCTI]
                                                        |
                                                        v
                                              [Confidence Updated]
```

### Steps:
1. **Observable Ingestion**: New IP/domain/hash created via feed import or manual entry
2. **Queue Distribution**: OpenCTI sends observable to enrichment connector queues
3. **Parallel Enrichment**: Each connector queries its respective external API
4. **STIX Bundle Generation**: Connectors produce STIX 2.1 bundles with notes, labels, relationships
5. **Merge**: Enrichment results merged into the observable's knowledge graph
6. **Scoring**: Confidence score updated based on aggregated enrichment data

## Workflow 2: Analyst-Triggered Enrichment

```
[Analyst Selects Observable] --> [Manual Enrichment Request] --> [Selected Connectors]
         |                                                              |
         v                                                              v
  [Review Results] <-- [Enrichment Dashboard] <-- [Results Returned]
         |
         v
  [Update Tags/Labels] --> [Add to Investigation]
```

### Steps:
1. **Selection**: Analyst identifies observable requiring additional context
2. **Connector Choice**: Select specific enrichment connectors to run
3. **Execution**: Connectors query external services with observable value
4. **Review**: Analyst reviews enrichment results in observable detail view
5. **Curation**: Analyst updates labels, confidence, and adds notes
6. **Investigation**: Link enriched observable to ongoing investigation case

## Workflow 3: Bulk Enrichment Pipeline

```
[STIX Import] --> [Observable Extraction] --> [Batch Queue] --> [Rate-Limited Enrichment]
                                                                         |
                                                                         v
                                                              [Progress Tracking]
                                                                         |
                                                                         v
                                                              [Enrichment Report]
```

### Steps:
1. **Bulk Import**: Import STIX bundle with hundreds of observables
2. **Extraction**: OpenCTI extracts unique observables from imported data
3. **Queue Management**: Observables queued for enrichment with rate limiting
4. **Progressive Enrichment**: Connectors process queue respecting API rate limits
5. **Monitoring**: Track enrichment progress via connector status dashboard
6. **Reporting**: Generate enrichment summary with coverage statistics

## Workflow 4: Enrichment-Driven Scoring

```
[Raw IOC (Score: 0)] --> [VirusTotal] --> [Score += VT_detections/total * 30]
                              |
                              v
                         [AbuseIPDB] --> [Score += abuse_confidence * 0.3]
                              |
                              v
                         [GreyNoise] --> [Score += classification_weight]
                              |
                              v
                         [Shodan] --> [Score += open_ports_risk]
                              |
                              v
                    [Final Score (0-100)] --> [Priority Classification]
                              |
                    +---------+---------+
                    |         |         |
                    v         v         v
              [Critical]  [High]    [Low]
              (80-100)   (50-79)   (0-49)
```

### Steps:
1. **Baseline**: Observable starts with confidence score of 0
2. **VT Score**: VirusTotal detection ratio contributes up to 30 points
3. **Abuse Score**: AbuseIPDB confidence contributes up to 30 points
4. **Classification**: GreyNoise malicious/benign classification adds/subtracts points
5. **Exposure**: Shodan data on open ports and known vulnerabilities adds risk points
6. **Final Priority**: Aggregated score determines analyst priority queue placement

---

## Working Template

## Report Metadata
| Field | Value |
|-------|-------|
| Report ID | ENRICH-YYYY-NNNN |
| Date | YYYY-MM-DD HH:MM UTC |
| Platform | OpenCTI v6.x |
| Analyst | [Analyst Name] |
| Classification | TLP:AMBER |

## Observable Summary

| Observable | Type | Initial Score | Enriched Score | Priority |
|-----------|------|---------------|----------------|----------|
| x.x.x.x | IPv4-Addr | 0 | 85 | Critical |
| evil.com | Domain-Name | 0 | 62 | High |

## Enrichment Results

### Observable: [Value]
**Type**: IPv4-Addr / Domain-Name / StixFile

#### VirusTotal
| Metric | Value |
|--------|-------|
| Malicious Detections | X / Y engines |
| Suspicious | X |
| Reputation Score | X |
| AS Owner | |
| Country | |

#### Shodan
| Metric | Value |
|--------|-------|
| Open Ports | |
| Known Vulnerabilities | |
| ISP | |
| Organization | |
| Operating System | |

#### AbuseIPDB
| Metric | Value |
|--------|-------|
| Abuse Confidence Score | X% |
| Total Reports | X |
| Distinct Reporters | X |
| Is Tor Exit Node | Yes/No |
| Usage Type | |

#### GreyNoise
| Metric | Value |
|--------|-------|
| Classification | malicious/benign/unknown |
| Internet Noise | Yes/No |
| RIOT (Benign Service) | Yes/No |
| Name | |
| Last Seen | |

## Confidence Scoring Breakdown

| Source | Weight | Score Contribution |
|--------|--------|--------------------|
| VirusTotal | 30% | X points |
| AbuseIPDB | 30% | X points |
| GreyNoise | 20% | X points |
| Shodan | 20% | X points |
| **Total** | **100%** | **X / 100** |

## Recommended Actions

| Priority | Action | Observable | Reason |
|----------|--------|-----------|--------|
| Critical | Block immediately | | Score > 80 |
| High | Add to watchlist | | Score 50-79 |
| Medium | Monitor | | Score 20-49 |
| Low | No action needed | | Score < 20 |

## STIX Relationships Created

| Source | Relationship | Target |
|--------|-------------|--------|
| [Observable] | indicates | [Malware/Campaign] |
| [Observable] | related-to | [Infrastructure] |
| [Threat Actor] | uses | [Observable] |
