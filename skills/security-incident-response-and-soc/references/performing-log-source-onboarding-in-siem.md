# Performing Log Source Onboarding In SIEM

## API Reference

## Libraries Used
- **socket**: Test syslog connectivity (UDP/TCP) to SIEM collectors
- **re**: Log format detection via pattern matching
- **pathlib**: Read log sample files

## CLI Interface
```
python agent.py detect --file sample.log
python agent.py validate --host siem.corp.com [--port 514] [--protocol udp|tcp]
python agent.py parse-config --format syslog_rfc3164 --source-type firewall_logs
python agent.py checklist --source "Palo Alto FW" --format syslog_rfc3164 --siem-host siem.corp.com
```

## Core Functions

### `detect_log_format(sample_file)` — Auto-detect log format
Identifies: syslog RFC 3164/5424, CEF, LEEF, JSON, CSV, Windows Event, Apache combined.

### `validate_syslog_connectivity(host, port, protocol)` — Test SIEM collector
Sends test syslog message via UDP or TCP. Validates port reachability.

### `generate_parsing_config(log_format, source_type)` — Create parsing rules
Generates Splunk (props.conf/transforms.conf) and Elastic (Filebeat/Logstash) configs.

### `create_onboarding_checklist(...)` — 10-step onboarding workflow
Covers: sample collection, format validation, connectivity, parsing, correlation rules, documentation.

## Supported Log Formats
| Format | Pattern Indicator |
|--------|------------------|
| syslog_rfc3164 | `<PRI>Mon DD HH:MM:SS` |
| syslog_rfc5424 | `<PRI>VER YYYY-MM-DDT` |
| CEF | `CEF:0\|` |
| LEEF | `LEEF:1.0\|` |
| JSON | `{...}` |
| Apache combined | IP - - [timestamp] "METHOD" |

## Dependencies
No external packages — Python standard library only.

---

## Standards and Controls

## Common Information Models

| SIEM Platform | Schema | Documentation |
|---|---|---|
| Splunk | CIM (Common Information Model) | docs.splunk.com |
| Elastic | ECS (Elastic Common Schema) | elastic.co/guide/en/ecs |
| Microsoft Sentinel | ASIM (Azure Sentinel Information Model) | learn.microsoft.com |
| Google Chronicle | UDM (Unified Data Model) | cloud.google.com/chronicle |
| Industry Standard | OCSF (Open Cybersecurity Schema Framework) | ocsf.io |

## Log Collection Protocols

| Protocol | Port | Use Case | Security |
|---|---|---|---|
| Syslog UDP | 514 | Network devices, basic forwarding | None |
| Syslog TCP | 514 | Reliable delivery | None |
| Syslog TLS | 6514 | Encrypted syslog | TLS 1.2+ |
| HTTP/S | 443/8088 | REST API, HEC (Splunk) | TLS |
| Windows WEF | 5985/5986 | Windows Event Forwarding | Kerberos/TLS |
| SNMP | 161/162 | Network device monitoring | SNMPv3 |
| S3/Blob | N/A | Cloud log storage | IAM/SAS |

## NIST SP 800-92 Log Management Guidelines

- Establish log management infrastructure
- Define log retention requirements
- Ensure log data integrity (tamper evidence)
- Configure time synchronization across all sources
- Implement log review and analysis procedures

---

## Workflows

## Onboarding Workflow

```
1. Request Received (ticket/email)
   |
   v
2. Discovery & Assessment (1-2 days)
   - Identify log format and volume
   - Assess security value vs cost
   - Check for existing parser
   |
   v
3. Planning (1 day)
   - Determine collection method
   - Plan network access
   - Estimate storage impact
   |
   v
4. Implementation (2-5 days)
   - Install/configure collector
   - Build/customize parser
   - Map to CIM fields
   |
   v
5. Validation (1-2 days)
   - Verify data flow
   - Check field extraction
   - Confirm CIM compliance
   - Test detection rules
   |
   v
6. Production Release (1 day)
   - Enable detection rules
   - Update dashboards
   - Document in CMDB
   - Notify SOC team
```

## Volume Estimation Formula

```
Daily Volume (GB) = EPS * Average Event Size (bytes) * 86400 / 1,073,741,824

Example:
  EPS = 100
  Avg Event Size = 500 bytes
  Daily Volume = 100 * 500 * 86400 / 1,073,741,824 = 4.03 GB/day
  Monthly Volume = 4.03 * 30 = 120.9 GB/month
```

## Cost-Value Assessment Matrix

| Security Value | Low Volume (<1GB/day) | Medium (1-10GB) | High (>10GB) |
|---|---|---|---|
| Critical | Must have | Must have | Evaluate ROI |
| High | Should have | Should have | Evaluate ROI |
| Medium | Nice to have | Evaluate ROI | Defer |
| Low | Defer | Defer | Reject |

---

## Working Template

## Source Information

| Field | Value |
|---|---|
| Source Name | |
| System Type | |
| Log Format | syslog / CEF / JSON / XML / CSV / Windows Events |
| Estimated EPS | |
| Estimated Daily Volume (GB) | |
| Security Tier | Critical / High / Medium / Low |
| Collection Method | Syslog / Agent / API / File / Cloud |
| Network Location | |
| Owner/Contact | |

## Onboarding Checklist

- [ ] Discovery and assessment complete
- [ ] Planning approved
- [ ] Network connectivity confirmed
- [ ] Collection agent/method configured
- [ ] Parser/field extraction built
- [ ] CIM fields mapped
- [ ] Data quality validated
- [ ] Detection rules enabled
- [ ] Dashboards updated
- [ ] Documentation complete
- [ ] SOC team notified
- [ ] Production released

## CIM Field Mapping

| Raw Field | CIM Field | Data Model |
|---|---|---|
| | | |

## Validation Results

| Check | Result | Notes |
|---|---|---|
| Events arriving | Pass/Fail | |
| Field extraction | Pass/Fail | |
| CIM compliance | Pass/Fail | |
| Timestamp parsing | Pass/Fail | |
| Volume within budget | Pass/Fail | |
