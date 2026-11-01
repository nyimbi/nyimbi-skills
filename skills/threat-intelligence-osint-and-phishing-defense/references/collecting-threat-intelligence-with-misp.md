# Collecting Threat Intelligence With Misp

## API Reference

## PyMISP Installation
```bash
pip install pymisp
```

## Client Initialization
```python
from pymisp import PyMISP

misp = PyMISP(
    url="https://misp.example.org",
    key=os.environ["MISP_API_KEY"],
    ssl=True
)
```

## Event Search
```python
# By tags
events = misp.search("events", tags=["tlp:white", "type:OSINT"], pythonify=True)

# By date range
events = misp.search("events", date_from="2025-01-01", date_to="2025-01-31", pythonify=True)

# Published only
events = misp.search("events", published=True, limit=100, pythonify=True)
```

## Attribute Search
```python
# By type
attrs = misp.search("attributes", type_attribute="ip-dst", to_ids=True, pythonify=True)

# By event
attrs = misp.search("attributes", eventid=42, pythonify=True)

# By value
attrs = misp.search("attributes", value="198.51.100.42", pythonify=True)
```

## REST API (curl)
```bash
# Search events
curl -X POST "https://misp/events/restSearch" \
  -H "Authorization: $KEY" \
  -H "Content-Type: application/json" \
  -d '{"tags":["tlp:white"],"limit":50}'

# Get event
curl -H "Authorization: $KEY" "https://misp/events/view/42"

# STIX 2 export
curl -H "Authorization: $KEY" "https://misp/events/restSearch/stix2"
```

## Common Attribute Types
| Type | Category | Example |
|------|----------|---------|
| ip-dst | Network activity | 198.51.100.42 |
| domain | Network activity | evil.example.com |
| url | Network activity | https://evil.com/mal |
| sha256 | Payload delivery | a1b2c3... |
| md5 | Payload delivery | d41d8c... |
| email-src | Payload delivery | attacker@evil.com |
| filename | Payload delivery | malware.exe |

## Feed Management
```python
# List feeds
feeds = misp.feeds()

# Enable feed
misp.enable_feed(feed_id=1)

# Fetch and cache
misp.fetch_feed(feed_id=1)
misp.cache_feeds()
```

---

## Standards and Controls

## MISP Standards

### MISP Core Format
- **MISP JSON Format**: Native event format used for synchronization between instances
- **MISP Galaxy**: Cluster-based knowledge base linked to MITRE ATT&CK, threat actors, tools
- **MISP Taxonomies**: Machine-readable tagging schemes (TLP, PAP, admiralty-scale, OSINT)
- **MISP Warninglists**: Lists of well-known indicators to reduce false positives (Alexa Top 1M, Office 365 IPs)

### STIX 2.1 (Structured Threat Information Expression)
- Standard language for representing cyber threat intelligence
- MISP supports import/export of STIX 2.1 bundles
- Object types: Indicator, Malware, Threat Actor, Attack Pattern, Campaign, Observed Data
- Relationship types: uses, targets, attributed-to, indicates, mitigates

### TAXII 2.1 (Trusted Automated Exchange of Intelligence Information)
- Transport protocol for sharing CTI over HTTPS
- MISP can consume TAXII feeds and serve as a TAXII server
- Collection-based model: discovery, API root, collections, objects
- Supports pagination and filtering by added_after, type, version

## MITRE ATT&CK Integration
- MISP Galaxy clusters map directly to ATT&CK techniques (T-codes)
- Events can be tagged with ATT&CK tactics: Initial Access, Execution, Persistence, etc.
- ATT&CK Navigator integration for visualizing technique coverage
- Sub-technique support (e.g., T1566.001 - Spearphishing Attachment)

## Traffic Light Protocol (TLP)
- **TLP:CLEAR** (formerly TLP:WHITE): Unlimited disclosure
- **TLP:GREEN**: Limited disclosure within community
- **TLP:AMBER**: Limited disclosure within organization
- **TLP:AMBER+STRICT**: Restricted to organization only
- **TLP:RED**: Restricted to specific recipients only

## Permissible Actions Protocol (PAP)
- **PAP:RED**: Only passive actions (no external lookups)
- **PAP:AMBER**: Active actions allowed but not against infrastructure
- **PAP:GREEN**: Active actions allowed
- **PAP:CLEAR**: Unlimited use

## References
- [MISP Standard Format RFC](https://www.misp-standard.org/)
- [STIX 2.1 Specification](https://docs.oasis-open.org/cti/stix/v2.1/stix-v2.1.html)
- [TAXII 2.1 Specification](https://docs.oasis-open.org/cti/taxii/v2.1/taxii-v2.1.html)
- [MITRE ATT&CK](https://attack.mitre.org/)
- [TLP Standard](https://www.first.org/tlp/)

---

## Workflows

## Workflow 1: Automated Feed Collection Pipeline

```
[Community Feeds] --> [MISP Feed Manager] --> [Event Creation] --> [Correlation Engine]
     |                      |                       |                      |
     v                      v                       v                      v
- CIRCL OSINT        - Schedule fetch         - Auto-tag with       - Deduplicate
- Botvrij.eu         - Parse formats            TLP/PAP             - Cross-reference
- abuse.ch           - Validate IOCs          - Set distribution    - Cluster similar
- PhishTank          - Filter warninglists    - Publish/unpublish     events
```

### Steps:
1. **Feed Registration**: Add feeds via UI or PyMISP API with source_format, URL, and headers
2. **Scheduled Fetch**: Configure cron job or MISP scheduler to pull feeds at intervals
3. **Parsing and Validation**: MISP parses feed content, validates IOC formats, checks against warninglists
4. **Event Generation**: Each feed pull creates or updates events with parsed attributes
5. **Correlation**: MISP correlates new attributes against existing data, identifying overlaps
6. **Distribution**: Events are distributed based on TLP and sharing group configurations

## Workflow 2: Manual Intelligence Collection

```
[Analyst Report] --> [Manual Event Creation] --> [Attribute Addition] --> [Enrichment]
                                                                              |
                                                                              v
                                                                    [Galaxy Tagging]
                                                                              |
                                                                              v
                                                                    [Publication]
```

### Steps:
1. **Event Creation**: Create event with descriptive info, date, distribution, TLP tag
2. **IOC Entry**: Add attributes (IP, domain, hash, URL) with correct category and type
3. **Object Construction**: Group related attributes into MISP objects (file, domain-ip, email)
4. **Galaxy Linking**: Link event to MITRE ATT&CK techniques, threat actor clusters, malware families
5. **Enrichment**: Use MISP modules (VirusTotal, Shodan, CIRCL PassiveDNS) to enrich attributes
6. **Review and Publish**: Analyst reviews, sets to_ids flags, publishes for community sharing

## Workflow 3: TAXII Feed Integration

```
[TAXII Server] --> [TAXII Client] --> [STIX Parser] --> [MISP Import] --> [Correlation]
```

### Steps:
1. **Discovery**: Query TAXII server discovery endpoint for available API roots
2. **Collection Enumeration**: List available collections and their metadata
3. **Object Retrieval**: Fetch STIX 2.1 objects from collections with pagination
4. **STIX-to-MISP Mapping**: Map STIX Indicator, Malware, Threat Actor to MISP event/attributes
5. **Import**: Create MISP events from STIX bundles
6. **Correlation**: Run correlation against existing MISP data

## Workflow 4: Instance Synchronization

```
[MISP Instance A] <--sync--> [MISP Instance B] <--sync--> [MISP Instance C]
       |                              |                            |
       v                              v                            v
  [Org A Events]              [Shared Events]               [Org C Events]
```

### Steps:
1. **Server Registration**: Register remote MISP instance with URL, API key, organization
2. **Sync Configuration**: Set sync direction (push/pull), filter rules, preview mode
3. **Pull Sync**: Pull events from remote instance matching filter criteria
4. **Push Sync**: Push local events to remote instance based on distribution level
5. **Conflict Resolution**: Handle attribute conflicts with priority rules
6. **Audit Logging**: Log all sync activities for compliance and troubleshooting

## Workflow 5: IOC Export for Defensive Tools

```
[MISP Events] --> [Export Module] --> [Format Conversion] --> [Defensive Tool]
                                             |
                                    +--------+--------+
                                    |        |        |
                                    v        v        v
                              [Suricata] [Bro/Zeek] [SIEM]
                               Rules     Intel      CSV/JSON
```

### Steps:
1. **Filter Selection**: Select events by tag, date range, threat level, to_ids flag
2. **Format Selection**: Choose output format (Suricata, Snort, Bro/Zeek, CSV, STIX, OpenIOC)
3. **Rule Generation**: Generate IDS/IPS rules from network IOCs
4. **SIEM Export**: Export to CSV/JSON for SIEM ingestion (Splunk, Elastic, QRadar)
5. **Automation**: Set up ZMQ/Kafka publishing for real-time IOC distribution
6. **Feedback Loop**: Track hit counts on exported IOCs, feed back to MISP for scoring

---

## Working Template

## Report Metadata
| Field | Value |
|-------|-------|
| Report ID | MISP-COL-YYYY-NNNN |
| Date Generated | YYYY-MM-DD HH:MM UTC |
| MISP Instance | https://misp.example.com |
| Collection Period | YYYY-MM-DD to YYYY-MM-DD |
| Classification | TLP:AMBER |
| Analyst | [Analyst Name] |

## Executive Summary

Brief overview of threat intelligence collected during the reporting period, including total events processed, notable threat campaigns identified, and key IOCs requiring immediate action.

## Collection Statistics

| Metric | Count |
|--------|-------|
| Total Events Processed | |
| New Events Created | |
| Attributes Collected | |
| IDS-Flagged Indicators | |
| Warninglist Filtered | |
| Feeds Active | |
| Correlations Found | |

## Feed Status

| Feed Name | Provider | Last Fetch | Status | Events Generated |
|-----------|----------|------------|--------|-----------------|
| CIRCL OSINT | CIRCL | | Active/Error | |
| Botvrij.eu | Botvrij | | Active/Error | |
| URLhaus | abuse.ch | | Active/Error | |
| PhishTank | OpenDNS | | Active/Error | |

## Top IOC Categories

### Network Indicators
| Type | Count | Sample Values |
|------|-------|---------------|
| IP Addresses (dst) | | |
| IP Addresses (src) | | |
| Domains | | |
| URLs | | |
| Hostnames | | |

### File Indicators
| Type | Count | Sample Values |
|------|-------|---------------|
| MD5 Hashes | | |
| SHA-1 Hashes | | |
| SHA-256 Hashes | | |
| Filenames | | |

### Email Indicators
| Type | Count | Sample Values |
|------|-------|---------------|
| Email Addresses | | |
| Email Subjects | | |
| Attachment Names | | |

## Notable Campaigns

### Campaign 1: [Campaign Name]
- **Threat Actor**: [Actor Name/Group]
- **MITRE ATT&CK Techniques**: T1566, T1059, T1071
- **IOC Count**: N indicators
- **First Seen**: YYYY-MM-DD
- **TLP**: AMBER
- **Key Indicators**:
  - IP: x.x.x.x (C2 Server)
  - Domain: malicious-domain.com
  - SHA256: [hash]

## Correlation Highlights

Events sharing common indicators across multiple campaigns or threat actors:

| Indicator | Events Linked | Threat Actors | Confidence |
|-----------|--------------|---------------|------------|
| | | | High/Medium/Low |

## Export Summary

| Format | Destination | Record Count | Timestamp |
|--------|-------------|-------------|-----------|
| STIX 2.1 | OpenCTI | | |
| Suricata Rules | IDS/IPS | | |
| CSV | SIEM (Splunk) | | |
| JSON | Threat Hunting | | |

## Recommendations

1. **Immediate Actions**: Block high-confidence IOCs in firewall/proxy
2. **Monitoring**: Add medium-confidence IOCs to watchlists
3. **Investigation**: Review events tagged with threat level "high"
4. **Feed Maintenance**: Review and update feed configurations
5. **Sharing**: Publish sanitized events to community instances

## Appendix: IOC Export

Full IOC list exported to:
- `misp_iocs_export.csv` - CSV format for SIEM ingestion
- `misp_stix_bundle.json` - STIX 2.1 bundle for CTI platforms
- `misp_suricata.rules` - Suricata IDS rules for network detection
