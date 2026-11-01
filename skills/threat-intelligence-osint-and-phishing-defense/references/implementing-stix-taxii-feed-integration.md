# Implementing Stix Taxii Feed Integration

## API Reference

## Libraries Used

| Library | Purpose |
|---------|---------|
| `taxii2-client` | TAXII 2.0/2.1 client for fetching CTI collections |
| `stix2` | Parse and create STIX 2.1 objects (indicators, malware, etc.) |
| `requests` | HTTP fallback for custom TAXII endpoints |
| `json` | Serialize and filter STIX bundles |

## Installation

```bash
pip install taxii2-client stix2 requests
```

## Authentication

### TAXII Server with HTTP Basic Auth
```python
from taxii2client.v21 import Server, Collection
import os

TAXII_URL = os.environ["TAXII_URL"]  # e.g., "https://cti-taxii.mitre.org/taxii2/"
server = Server(
    TAXII_URL,
    user=os.environ.get("TAXII_USER"),
    password=os.environ.get("TAXII_PASS"),
)
```

### TAXII Server with API Key
```python
from taxii2client.v21 import Server as Server21

server = Server21(
    url=TAXII_URL,
    headers={"Authorization": f"Bearer {os.environ['TAXII_TOKEN']}"},
)
```

## TAXII 2.1 Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /taxii2/` | Server discovery — returns API roots |
| `GET /{api-root}/` | API root information |
| `GET /{api-root}/collections/` | List available collections |
| `GET /{api-root}/collections/{id}/` | Get collection details |
| `GET /{api-root}/collections/{id}/objects/` | Get STIX objects from collection |
| `GET /{api-root}/collections/{id}/manifest/` | Object manifest (metadata only) |
| `POST /{api-root}/collections/{id}/objects/` | Add objects to a collection |
| `GET /{api-root}/status/{id}/` | Check status of a POST operation |

## Core Operations

### Discover Collections
```python
for api_root in server.api_roots:
    print(f"API Root: {api_root.title}")
    for collection in api_root.collections:
        print(f"  Collection: {collection.title} ({collection.id})")
        print(f"    Can read: {collection.can_read}, Can write: {collection.can_write}")
```

### Fetch STIX Objects from a Collection
```python
from taxii2client.v21 import Collection

collection = Collection(
    f"{TAXII_URL}collections/{collection_id}/",
    user=os.environ.get("TAXII_USER"),
    password=os.environ.get("TAXII_PASS"),
)

# Get all objects
stix_bundle = collection.get_objects()

# Filter by STIX type
indicators = collection.get_objects(type=["indicator"])

# Filter by time range
from datetime import datetime
recent = collection.get_objects(
    added_after=datetime(2025, 1, 1).strftime("%Y-%m-%dT%H:%M:%SZ")
)
```

### Parse STIX Objects
```python
import stix2

bundle = stix2.parse(stix_bundle, allow_custom=True)
for obj in bundle.objects:
    if obj.type == "indicator":
        print(f"Indicator: {obj.name}")
        print(f"  Pattern: {obj.pattern}")
        print(f"  Valid: {obj.valid_from} — {getattr(obj, 'valid_until', 'N/A')}")
    elif obj.type == "malware":
        print(f"Malware: {obj.name} — {obj.malware_types}")
    elif obj.type == "attack-pattern":
        print(f"TTP: {obj.name}")
```

### Extract IOCs from STIX Indicators
```python
import re

def extract_iocs(stix_objects):
    iocs = {"ipv4": [], "domain": [], "url": [], "sha256": [], "md5": []}
    for obj in stix_objects:
        if obj.get("type") != "indicator":
            continue
        pattern = obj.get("pattern", "")
        # IPv4
        for ip in re.findall(r"ipv4-addr:value\s*=\s*'([^']+)'", pattern):
            iocs["ipv4"].append(ip)
        # Domain
        for domain in re.findall(r"domain-name:value\s*=\s*'([^']+)'", pattern):
            iocs["domain"].append(domain)
        # SHA-256
        for sha in re.findall(r"file:hashes\.'SHA-256'\s*=\s*'([^']+)'", pattern):
            iocs["sha256"].append(sha)
    return iocs
```

### Create and Push STIX Objects
```python
indicator = stix2.Indicator(
    name="Malicious IP",
    pattern="[ipv4-addr:value = '198.51.100.42']",
    pattern_type="stix",
    valid_from=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
    labels=["malicious-activity"],
)
bundle = stix2.Bundle(objects=[indicator])

collection.add_objects(bundle.serialize())
```

## Public TAXII Feeds

| Provider | URL | Content |
|----------|-----|---------|
| MITRE ATT&CK | `https://cti-taxii.mitre.org/taxii2/` | ATT&CK Enterprise, Mobile, ICS |
| AlienVault OTX | OTX API + STIX export | Community threat intel |
| Anomali STAXX | STAXX TAXII endpoint | Curated threat feeds |

## Output Format

```json
{
  "type": "bundle",
  "id": "bundle--a1b2c3d4",
  "objects": [
    {
      "type": "indicator",
      "id": "indicator--e5f6a7b8",
      "created": "2025-01-15T10:30:00Z",
      "name": "Malicious C2 IP",
      "pattern": "[ipv4-addr:value = '198.51.100.42']",
      "pattern_type": "stix",
      "valid_from": "2025-01-15T10:30:00Z",
      "labels": ["malicious-activity"]
    }
  ]
}
```

---

## Standards and Controls

## STIX 2.1 Standard (OASIS)

### Core Concepts
- **STIX Bundle**: Top-level container for STIX objects (type: "bundle")
- **STIX ID Format**: `type--uuid` (e.g., `indicator--a1b2c3d4-...`)
- **Versioning**: Objects use `modified` timestamp for version tracking
- **Confidence**: 0-100 scale for reliability assessment

### STIX Domain Objects (SDOs)
| Type | Purpose | Key Properties |
|------|---------|---------------|
| attack-pattern | ATT&CK technique | name, kill_chain_phases |
| campaign | Related intrusion activity | name, first_seen, objective |
| identity | Individuals/orgs | name, identity_class, sectors |
| indicator | Detection pattern | pattern, pattern_type, valid_from |
| infrastructure | Adversary systems | name, infrastructure_types |
| intrusion-set | Threat group | name, aliases, goals |
| malware | Malware family | name, malware_types, is_family |
| note | Analyst annotation | content, object_refs |
| report | CTI document | name, published, object_refs |
| threat-actor | Human adversary | name, threat_actor_types, roles |
| tool | Legitimate software | name, tool_types |
| vulnerability | CVE/weakness | name, external_references |

### STIX Patterning Language
```
[file:hashes.'SHA-256' = 'abc...']
[ipv4-addr:value = '198.51.100.1']
[domain-name:value = 'malware.example.com']
[network-traffic:dst_ref.type = 'ipv4-addr' AND network-traffic:dst_port = 443]
[process:name = 'cmd.exe' AND process:command_line MATCHES '.*powershell.*']
```

## TAXII 2.1 Standard (OASIS)

### Endpoints
| Endpoint | Method | Purpose |
|----------|--------|---------|
| /taxii2/ | GET | Server discovery |
| /{api-root}/ | GET | API root information |
| /{api-root}/collections/ | GET | List collections |
| /{api-root}/collections/{id}/ | GET | Collection details |
| /{api-root}/collections/{id}/objects/ | GET/POST | Get/add objects |
| /{api-root}/collections/{id}/manifest/ | GET | Object manifest |
| /{api-root}/status/{id}/ | GET | Status of add operation |

### HTTP Headers
- Content-Type: `application/stix+json;version=2.1`
- Accept: `application/taxii+json;version=2.1`

### Pagination Parameters
- `limit`: Maximum number of objects per response
- `next`: Cursor for next page
- `added_after`: Filter objects by timestamp

## Marking Definitions (TLP)
```json
{"definition_type": "tlp", "definition": {"tlp": "clear"}}
{"definition_type": "tlp", "definition": {"tlp": "green"}}
{"definition_type": "tlp", "definition": {"tlp": "amber"}}
{"definition_type": "tlp", "definition": {"tlp": "amber+strict"}}
{"definition_type": "tlp", "definition": {"tlp": "red"}}
```

## References
- [STIX 2.1 Spec](https://docs.oasis-open.org/cti/stix/v2.1/stix-v2.1.html)
- [TAXII 2.1 Spec](https://docs.oasis-open.org/cti/taxii/v2.1/taxii-v2.1.html)
- [CTI Documentation](https://oasis-open.github.io/cti-documentation/)

---

## Workflows

## Workflow 1: TAXII Feed Consumption

```
[TAXII Discovery] --> [API Root Enumeration] --> [Collection Selection] --> [Object Polling]
                                                                                 |
                                                                                 v
                                                                     [STIX Parsing] --> [IOC Extraction]
                                                                                              |
                                                                                              v
                                                                                    [SIEM/TIP Ingestion]
```

### Steps:
1. **Discovery**: Query TAXII server discovery endpoint for available API roots
2. **Root Enumeration**: List available API roots and their supported features
3. **Collection Listing**: Enumerate collections with read/write permissions
4. **Incremental Polling**: Fetch new objects using added_after timestamp filter
5. **STIX Parsing**: Deserialize JSON into typed STIX objects
6. **IOC Extraction**: Extract indicators, observables, and relationships
7. **Platform Ingestion**: Push to SIEM, MISP, or OpenCTI

## Workflow 2: STIX Bundle Production

```
[IOC Sources] --> [Normalization] --> [STIX Object Creation] --> [Bundle Assembly]
                                                                        |
                                                                        v
                                                              [TAXII Publication]
```

### Steps:
1. **Source Collection**: Gather IOCs from internal analysis, feeds, incident response
2. **Normalization**: Standardize IOC formats and remove duplicates
3. **Object Creation**: Create STIX Indicators, Observables, and Relationships
4. **TLP Marking**: Apply appropriate TLP marking definitions
5. **Bundle Assembly**: Package objects into STIX 2.1 bundles
6. **TAXII Push**: POST bundles to writable TAXII collections

## Workflow 3: Multi-Feed Aggregation

```
[TAXII Feed A] --+
                  |--> [Deduplication] --> [Correlation] --> [Unified Store]
[TAXII Feed B] --+                                                |
                  |                                                v
[STIX File C] ---+                                      [Dashboard/Alerts]
```

### Steps:
1. **Feed Registration**: Configure multiple TAXII and file-based STIX sources
2. **Parallel Polling**: Poll all feeds concurrently with rate limiting
3. **Deduplication**: Remove duplicate objects by STIX ID and modified timestamp
4. **Correlation**: Link related objects across feeds via relationships
5. **Unified Storage**: Store in MemoryStore, FileSystemStore, or database-backed store
6. **Output**: Generate alerts, dashboards, or exports for downstream consumers

---

## Working Template

## Feed Configuration
| Field | Value |
|-------|-------|
| TAXII Server | |
| API Root | |
| Collection ID | |
| Collection Name | |
| Last Poll Timestamp | |
| Authentication | API Key / Basic / Certificate |

## Discovery Summary
| Metric | Count |
|--------|-------|
| API Roots | |
| Collections (Read) | |
| Collections (Write) | |

## Poll Results
| Metric | Count |
|--------|-------|
| Total Objects Fetched | |
| New Since Last Poll | |
| Indicators | |
| Malware | |
| Threat Actors | |
| Attack Patterns | |
| Relationships | |
| Observables | |

## Extracted IOCs

### Network Indicators
| Type | Value | Confidence | Valid From | Valid Until |
|------|-------|-----------|-----------|------------|
| IP | | | | |
| Domain | | | | |
| URL | | | | |

### File Indicators
| Hash Type | Value | Confidence | Associated Malware |
|-----------|-------|-----------|-------------------|
| SHA-256 | | | |
| MD5 | | | |

## Integration Status
| Downstream System | Status | Records Pushed |
|-------------------|--------|---------------|
| SIEM (Splunk/Elastic) | Success/Failed | |
| MISP | Success/Failed | |
| OpenCTI | Success/Failed | |
| Firewall Blocklist | Success/Failed | |
