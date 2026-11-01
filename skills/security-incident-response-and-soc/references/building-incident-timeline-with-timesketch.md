# Building Incident Timeline With Timesketch

## API Reference

## Authentication
```
POST /login/
Content-Type: application/x-www-form-urlencoded
Body: username=USER&password=PASS
```

## Sketch Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/sketches/` | List all sketches |
| POST | `/api/v1/sketches/` | Create new sketch |
| GET | `/api/v1/sketches/{id}/` | Get sketch details |
| DELETE | `/api/v1/sketches/{id}/` | Delete sketch |

## Timeline Upload
```
POST /api/v1/upload/
Content-Type: multipart/form-data
Fields: name, sketch_id, file (Plaso/CSV/JSONL)
```

## Event Search (Explore)
```
POST /api/v1/sketches/{id}/explore/
{
  "query": "source_short:EVT AND message:*logon*",
  "limit": 500,
  "fields": ["datetime", "timestamp_desc", "message", "source_short"],
  "filter": {
    "chips": [
      {"type": "datetime_range", "value": "2024-01-01T00:00:00,2024-01-31T23:59:59", "active": true}
    ]
  }
}
```

## Event Annotation
```
POST /api/v1/sketches/{id}/event/annotate/
{
  "annotation": "suspicious,lateral-movement",
  "annotation_type": "tag",
  "events": {"event_id": "abc123"}
}
```

## Supported Timeline Formats
| Format | Extension | Description |
|--------|-----------|-------------|
| Plaso | `.plaso` | log2timeline output |
| CSV | `.csv` | Timesketch CSV (datetime, message, timestamp_desc) |
| JSONL | `.jsonl` | One JSON event per line |

## Event Fields
| Field | Description |
|-------|-------------|
| `datetime` | Event timestamp (ISO 8601) |
| `timestamp_desc` | Timestamp meaning (e.g., "Creation Time") |
| `message` | Human-readable event description |
| `source_short` | Source type (EVT, FILE, LOG, REG) |
| `source_long` | Full source name |

## Analyzers
```
POST /api/v1/sketches/{id}/analyzer/
{"analyzer_names": ["domain", "similarity_scorer", "tagger"]}
```

## Python Client
```python
from timesketch_api_client import config as ts_config
from timesketch_api_client import client as ts_client

ts = ts_client.TimesketchApi(host, username, password)
sketch = ts.get_sketch(sketch_id)
results = sketch.explore(query="*", return_fields="datetime,message")
```

---

## Standards and Controls

## NIST SP 800-86 - Guide to Integrating Forensic Techniques
- Provides guidelines for collecting, examining, and analyzing digital evidence
- Emphasizes importance of timeline reconstruction in incident investigation
- Defines evidence handling procedures for forensic analysis

## SANS FOR508 - Advanced Incident Response, Threat Hunting, and Digital Forensics
- Super timeline creation methodology
- Evidence source prioritization for timeline building
- Plaso/log2timeline artifact parsing techniques
- Timeline analysis for APT detection

## RFC 3339 / ISO 8601 - Timestamp Standardization
- Standard format for representing dates and times in timelines
- Timesketch normalizes all timestamps to UTC ISO 8601 format
- Ensures consistent chronological ordering across diverse sources

## DFRWS (Digital Forensic Research Workshop) Standards
- Forensic timeline analysis research and best practices
- Timesketch presented at DFRWS conferences as reference implementation
- Evidence integrity and chain of custody in digital forensics

## Plaso/log2timeline Documentation
- Official parser documentation for 200+ artifact types
- Filter file syntax for targeted evidence collection
- Output format specifications for Timesketch integration
- Reference: https://plaso.readthedocs.io/

## OpenSearch/Elasticsearch Indexing Standards
- Event storage and retrieval optimization
- Index lifecycle management for large investigations
- Query DSL for advanced timeline searching

## Sigma Detection Standard
- Open signature format for SIEM systems
- Timesketch Sigma analyzer integration
- Community detection rules for common attack patterns
- Reference: https://github.com/SigmaHQ/sigma

## MITRE ATT&CK Framework Integration
- Mapping timeline events to ATT&CK techniques
- Tactic-based timeline segmentation
- Attack chain reconstruction methodology

---

## Workflows

## Workflow 1: Evidence Processing Pipeline

```
START: Evidence Collection Complete
  |
  v
[Mount Evidence / Extract Artifacts]
  |-- Mount disk image (read-only)
  |-- Extract event logs from triage package
  |-- Collect cloud service logs
  |-- Gather network device logs
  |
  v
[Process with Plaso/log2timeline]
  |-- Select appropriate parsers
  |-- Configure filter files for scope
  |-- Run log2timeline on each source
  |-- Verify output .plaso files
  |
  v
[Import into Timesketch]
  |-- Create sketch for investigation
  |-- Upload each timeline with descriptive name
  |-- Wait for indexing to complete
  |-- Verify event counts per timeline
  |
  v
[Run Automated Analyzers]
  |-- Domain analyzer
  |-- Sigma rule analyzer
  |-- Chain of events analyzer
  |-- Feature extraction analyzer
  |
  v
[Manual Analysis and Tagging]
  |-- Search for key indicators
  |-- Tag events by attack phase
  |-- Add investigator annotations
  |-- Build investigation story
  |
  v
END: Timeline Ready for Analysis
```

## Workflow 2: Rapid Triage Timeline

```
START: Incident Detected - Quick Timeline Needed
  |
  v
[Collect Quick-Win Artifacts]
  |-- Windows Event Logs (Security, System, PowerShell)
  |-- Prefetch files
  |-- Browser history
  |-- Recent file access (NTUSER.DAT)
  |
  v
[Fast Processing]
  |-- Targeted Plaso parsers only
  |   (winevtx, prefetch, chrome_history)
  |-- Or convert logs to CSV format
  |-- Import directly into Timesketch
  |
  v
[Initial Analysis]
  |-- Search for known IOCs
  |-- Run Sigma analyzer for quick wins
  |-- Identify suspicious time periods
  |-- Tag initial findings
  |
  v
[Expand if Needed]
  |-- Add additional evidence sources
  |-- Run full parser set
  |-- Broaden search scope
  |
  v
END: Initial Triage Complete
```

## Workflow 3: Multi-Source Correlation

```
START: Multiple Evidence Sources Available
  |
  v
[Normalize Timestamps]
  |-- Ensure all sources use UTC
  |-- Account for clock skew between systems
  |-- Document any time synchronization issues
  |
  v
[Import All Sources as Separate Timelines]
  |-- Timeline 1: Endpoint logs (Plaso)
  |-- Timeline 2: Network logs (CSV)
  |-- Timeline 3: Cloud logs (JSONL)
  |-- Timeline 4: Email logs (CSV)
  |-- Timeline 5: Firewall logs (CSV)
  |
  v
[Cross-Source Correlation]
  |-- Search across all timelines simultaneously
  |-- Identify same events seen from different perspectives
  |-- Build complete picture of attacker activity
  |-- Tag correlated events with shared labels
  |
  v
[Build Attack Narrative]
  |-- Create story in Timesketch
  |-- Link saved views for each attack phase
  |-- Add context and analysis notes
  |-- Export for final report
  |
  v
END: Correlated Timeline Analysis Complete
```

## Workflow 4: Collaborative Team Investigation

```
START: Investigation Assigned to Team
  |
  v
[Sketch Setup by Lead Investigator]
  |-- Create sketch with case details
  |-- Import initial timeline data
  |-- Define investigation objectives
  |-- Assign analysis areas to team members
  |
  v
[Parallel Analysis by Team]
  |-- Analyst 1: Network traffic analysis
  |-- Analyst 2: Endpoint artifact analysis
  |-- Analyst 3: Cloud/identity analysis
  |-- Each analyst tags and annotates findings
  |
  v
[Consolidation]
  |-- Review all tagged events
  |-- Resolve conflicting findings
  |-- Build unified attack narrative
  |-- Create investigation story
  |
  v
[Quality Review]
  |-- Lead reviews complete timeline
  |-- Verify attack chain is complete
  |-- Ensure all IOCs documented
  |-- Export findings for report
  |
  v
END: Team Investigation Complete
```

---

## Working Template

## Case Information

| Field | Details |
|-------|---------|
| Case ID | |
| Sketch Name | |
| Lead Investigator | |
| Date Started | |
| Timesketch Instance | |
| Number of Timelines | |
| Total Events Indexed | |

## Evidence Sources

| Timeline Name | Source Type | Host/System | Events | Time Range |
|--------------|------------|-------------|--------|------------|
| | Windows EVTX | | | |
| | Plaso Full | | | |
| | Cloud Logs | | | |
| | Network Logs | | | |

## Investigation Objectives

1. [ ] Determine initial access vector
2. [ ] Identify compromised accounts
3. [ ] Map lateral movement paths
4. [ ] Identify persistence mechanisms
5. [ ] Determine data access and exfiltration
6. [ ] Establish complete attack timeline

## Attack Timeline Summary

| Time (UTC) | Event | Source | Host | ATT&CK Technique | Tags |
|------------|-------|--------|------|-------------------|------|
| | | | | | |

## Key Findings

### Finding 1: [Title]
- **Timesketch Search:** `[query string]`
- **Events:** [count]
- **Time Range:** [start] to [end]
- **Description:** [analysis]
- **Impact:** [assessment]

## Analyzers Run

| Analyzer | Results | Findings |
|----------|---------|----------|
| Sigma Rules | | |
| Domain Analyzer | | |
| Chain of Events | | |
| Feature Extraction | | |

## Saved Views

| View Name | Query | Purpose |
|-----------|-------|---------|
| | | |

## IOC Summary

### IP Addresses
### Domains
### File Hashes
### User Accounts

## Recommendations

1.
2.
3.

## Appendix
- Timesketch sketch export
- Full query list
- Plaso parser configuration
