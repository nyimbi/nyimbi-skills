# Building Threat Intelligence Enrichment In Splunk

## API Reference

## Splunk KV Store REST API
```bash
# Create collection
curl -k -u admin:pass -X POST \
  "https://localhost:8089/servicesNS/nobody/SA-ThreatIntelligence/storage/collections/config" \
  -d name=ip_intel

# Insert record
curl -k -u admin:pass -X POST \
  "https://localhost:8089/servicesNS/nobody/SA-ThreatIntelligence/storage/collections/data/ip_intel" \
  -H "Content-Type: application/json" \
  -d '{"ip":"198.51.100.42","threat_key":"c2_server","weight":"3"}'

# Batch insert
curl -k -u admin:pass -X POST \
  "https://localhost:8089/servicesNS/nobody/SA-ThreatIntelligence/storage/collections/data/ip_intel/batch_save" \
  -H "Content-Type: application/json" \
  -d '[{"ip":"1.2.3.4","threat_key":"malware"},{"ip":"5.6.7.8","threat_key":"c2"}]'
```

## Splunk Enterprise Security TI Framework
| Collection | Lookup | Data Model |
|-----------|--------|------------|
| ip_intel | ip_intel_lookup | Network_Traffic |
| domain_intel | domain_intel_lookup | Network_Resolution |
| file_intel | file_intel_lookup | Endpoint |
| email_intel | email_intel_lookup | Email |
| http_intel | http_intel_lookup | Web |

## SPL Threat Matching
```spl
| tstats summariesonly=t count from datamodel=Network_Traffic
  by All_Traffic.dest_ip
| rename All_Traffic.dest_ip as ip
| lookup ip_intel_lookup ip OUTPUT threat_key description
| where isnotnull(threat_key)
```

## AlienVault OTX API
```bash
# Get pulse indicators
curl "https://otx.alienvault.com/api/v1/pulses/PULSE_ID/indicators"

# Search pulses
curl -H "X-OTX-API-KEY: $OTX_KEY" \
  "https://otx.alienvault.com/api/v1/search/pulses?q=ransomware&page=1"
```

## Splunk Python SDK
```python
import splunklib.client as client

service = client.connect(
    host="localhost", port=8089,
    username="admin", password="changeme"
)

# Access KV store collection
collection = service.kvstore["ip_intel"]
collection.data.insert(json.dumps({
    "ip": "198.51.100.42",
    "threat_key": "c2_server"
}))
```

---

## Standards and Controls

## Threat Intelligence Standards

### STIX (Structured Threat Information eXpression)
- Version 2.1 is the current standard for representing threat intelligence
- Defines objects: Indicator, Malware, Attack Pattern, Threat Actor, Campaign
- Used as the interchange format between TI platforms and SIEMs

### TAXII (Trusted Automated eXchange of Indicator Information)
- Transport mechanism for STIX data
- TAXII 2.1 provides RESTful API for feed collection
- Supports Collection and Channel sharing models

### OpenIOC
- Mandiant's open framework for sharing IOCs
- XML-based format for indicator definitions

### OCSF (Open Cybersecurity Schema Framework)
- Industry standard for normalizing security event data
- Version 1.0 released at BlackHat 2023

## Splunk CIM Data Models for TI

| Data Model | TI Correlation Fields |
|---|---|
| Network_Traffic | src_ip, dest_ip, dest_port |
| Web | url, http_user_agent, domain |
| Email | src_user, file_hash, url |
| Endpoint | process_hash, file_hash, dest |
| Authentication | src_ip, user, app |
| DNS | query, answer, src_ip |

## IOC Types and Confidence Levels

| IOC Type | Splunk Field | Confidence Threshold |
|---|---|---|
| IP Address | ip_intel | > 70% |
| Domain | domain_intel | > 70% |
| File Hash (SHA256) | file_intel | > 80% |
| URL | url_intel | > 75% |
| Email Address | email_intel | > 80% |

---

## Workflows

## TI Feed Integration Workflow

```
1. Identify Relevant TI Sources
   - Commercial feeds (Recorded Future, Mandiant)
   - Open source (OTX, AbuseIPDB, VirusTotal)
   - Industry ISACs
   - Internal threat lists
   |
   v
2. Configure Modular Inputs
   - Set polling intervals
   - Configure authentication
   - Map feed fields to Splunk schema
   |
   v
3. Normalize to KV Store
   - Parse raw feed data
   - Map to standard field names
   - Set confidence scores
   - Add source attribution
   |
   v
4. Create Lookup Definitions
   - Define transforms.conf entries
   - Set field mappings
   - Enable automatic lookups where appropriate
   |
   v
5. Build Correlation Searches
   - Match events against IOC lookups
   - Add asset/identity enrichment
   - Set severity based on confidence
   |
   v
6. Monitor and Maintain
   - Track feed freshness
   - Remove stale indicators
   - Measure hit rates per source
```

## IOC Lifecycle Management

```
Ingestion --> Validation --> Active Use --> Aging --> Expiration --> Removal
    |              |            |            |           |
    v              v            v            v           v
  Raw feeds    Dedup and    Correlation   Reduce      Archive
  parsed       confidence   matching     confidence   or delete
               scoring                   weighting
```

## Feed Quality Assessment

| Metric | Good | Warning | Critical |
|---|---|---|---|
| Feed latency | < 1 hour | 1-24 hours | > 24 hours |
| False positive rate | < 5% | 5-15% | > 15% |
| Hit rate | > 1% | 0.1-1% | < 0.1% |
| Coverage overlap | < 30% | 30-60% | > 60% |
| Indicator freshness | < 7 days | 7-30 days | > 30 days |

---

## Working Template

## Feed Configuration

| Field | Value |
|---|---|
| Feed Name | |
| Source | |
| Feed Type | STIX/TAXII / CSV / API / Manual |
| Polling Interval | |
| IOC Types | IP / Domain / Hash / URL / Email |
| Confidence Threshold | |

## KV Store Collection

| Field | Type | Description |
|---|---|---|
| _key | string | Unique indicator hash |
| indicator_value | string | IOC value |
| threat_type | string | C2/Phishing/Malware/Scanner |
| confidence | number | 0-100 |
| source | string | Feed name |
| severity | string | critical/high/medium/low |
| first_seen | time | First observation |
| last_seen | time | Last observation |

## Correlation Search Template

```spl
| tstats summariesonly=true count
    from datamodel=<DataModel>
    by <fields>, _time span=5m
| rename "<DataModel>.*" as *
| lookup <lookup_name> <match_field> as <event_field>
    OUTPUT threat_type, confidence, source as ti_source
| where isnotnull(threat_type) AND confidence > <threshold>
| eval description="TI match: ".<matched_field>." (".<threat_type>.")"
```

## Feed Health Dashboard

| Metric | Current | Target |
|---|---|---|
| Total active indicators | | |
| Feed freshness (avg age) | | < 7 days |
| Hit rate (last 30 days) | | > 0.5% |
| False positive rate | | < 5% |
| Feed overlap rate | | < 30% |
