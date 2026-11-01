# Building Threat Intelligence Platform

## API Reference

## STIX 2.1 Indicator Object
```json
{
  "type": "indicator",
  "spec_version": "2.1",
  "id": "indicator--<uuid5>",
  "created": "2025-01-15T10:00:00.000Z",
  "modified": "2025-01-15T10:00:00.000Z",
  "name": "Malicious IP",
  "pattern": "[ipv4-addr:value = '198.51.100.42']",
  "pattern_type": "stix",
  "valid_from": "2025-01-15T10:00:00.000Z",
  "confidence": 85,
  "object_marking_refs": ["marking-definition--f88d31f6-486f-44da-b317-01333bde0b82"]
}
```

## TLP Marking Definition IDs (STIX 2.1)
| TLP Level | STIX Marking Definition ID |
|-----------|---------------------------|
| TLP:CLEAR | marking-definition--613f2e26-407d-48c7-9eca-b8e91df99dc9 |
| TLP:GREEN | marking-definition--34098fce-860f-48ae-8e50-ebd3cc5e41da |
| TLP:AMBER | marking-definition--f88d31f6-486f-44da-b317-01333bde0b82 |
| TLP:AMBER+STRICT | marking-definition--826578e1-40a3-4b46-a8d8-b9931fdd750e |
| TLP:RED | marking-definition--5e57c739-391a-4eb3-b6be-7d15ca92d5ed |

## TAXII 2.1 Endpoints
```bash
# Discovery
curl https://taxii.server.com/taxii2/

# Collections
curl https://taxii.server.com/taxii2/collections/

# Get objects from collection
curl "https://taxii.server.com/taxii2/collections/{id}/objects?type=indicator"

# Add objects
curl -X POST "https://taxii.server.com/taxii2/collections/{id}/objects" \
  -H "Content-Type: application/stix+json;version=2.1" \
  -d @bundle.json
```

## OpenCTI GraphQL API
```graphql
mutation {
  indicatorAdd(input: {
    name: "Malicious IP"
    pattern: "[ipv4-addr:value = '198.51.100.42']"
    pattern_type: "stix"
    x_opencti_score: 80
  }) {
    id
    standard_id
  }
}
```

## MISP REST API
```bash
# Add attribute
curl -X POST "https://misp/attributes/add/EVENT_ID" \
  -H "Authorization: MISP_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type":"ip-dst","value":"198.51.100.42","category":"Network activity","to_ids":true}'
```

---

## Standards and Controls

## TIP Architecture Standards
- **STIX 2.1**: Native data model for CTI representation
- **TAXII 2.1**: Transport protocol for CTI sharing
- **MITRE ATT&CK**: Technique taxonomy for TTP mapping
- **Diamond Model**: Intrusion analysis framework
- **Kill Chain**: Lockheed Martin Cyber Kill Chain for attack phase tracking

## Platform Component Standards
| Component | Protocol | Data Format |
|-----------|----------|-------------|
| MISP | REST API | MISP JSON, STIX 2.1 |
| OpenCTI | GraphQL API | STIX 2.1 |
| TheHive | REST API | TheHive JSON |
| Cortex | REST API | Cortex Report JSON |
| Elasticsearch | REST API | JSON |

## Integration Standards
- **MISP Sync Protocol**: Push/Pull over HTTPS with API key auth
- **OpenCTI Connectors**: RabbitMQ-based message queue for async processing
- **Cortex Analyzers**: Docker-based analyzers with standardized I/O
- **SIEM Integration**: Syslog, Kafka, REST API, or file-based export

## References
- [OpenCTI Architecture](https://docs.opencti.io/latest/deployment/overview/)
- [MISP Architecture](https://www.misp-project.org/features/)
- [TheHive Documentation](https://docs.strangebee.com/)

---

## Workflows

## Workflow 1: End-to-End Intelligence Pipeline
```
[External Feeds] --> [MISP] --> [OpenCTI] --> [Enrichment (Cortex)] --> [SIEM/TheHive]
    |                   |            |                |                       |
    v                   v            v                v                       v
OSINT/Commercial   Correlate    Knowledge Graph   VT/Shodan/AIPDB    Alerts/Cases
```

## Workflow 2: Incident-to-Intelligence Feedback Loop
```
[SOC Alert] --> [TheHive Case] --> [Cortex Analysis] --> [IOC Extraction]
                                                               |
                                                               v
                                                    [MISP Event Creation]
                                                               |
                                                               v
                                                    [OpenCTI Knowledge Update]
                                                               |
                                                               v
                                                    [Updated Detections --> SIEM]
```

## Workflow 3: Platform Health Monitoring
```
[Prometheus/Grafana] --> [Component Health] --> [Feed Status] --> [Alert on Failure]
                              |                      |
                              v                      v
                     [ES Cluster Health]    [Connector Status]
```

---

## Working Template

## Platform Health
| Component | Status | Version | URL |
|-----------|--------|---------|-----|
| MISP | Healthy/Unhealthy | | |
| OpenCTI | Healthy/Unhealthy | | |
| TheHive | Healthy/Unhealthy | | |
| Cortex | Healthy/Unhealthy | | |
| Elasticsearch | Healthy/Unhealthy | | |

## Feed Ingestion Status
| Feed Name | Source | Status | Last Fetch | Events Generated |
|-----------|--------|--------|-----------|-----------------|
| | | Active/Error | | |

## Platform Metrics
| Metric | MISP | OpenCTI | Combined |
|--------|------|---------|----------|
| Total Events/Reports | | | |
| Total Indicators | | | |
| Active Feeds | | | |
| Enrichment Jobs (24h) | | | |

## Connector Status
| Connector | Type | Active | Last Run |
|-----------|------|--------|---------|
| | Import/Enrichment/Stream | Yes/No | |

## Recommendations
1. [Platform maintenance recommendations]
2. [Feed configuration improvements]
3. [Integration enhancements]
