# Deploying Edr Agent With Crowdstrike

## API Reference

## Libraries

| Library | Install | Purpose |
|---------|---------|---------|
| crowdstrike-falconpy | `pip install crowdstrike-falconpy` | Official CrowdStrike Falcon SDK |

## Key FalconPy Service Classes

| Class | Description |
|-------|-------------|
| `Hosts(client_id, client_secret)` | Host/device management |
| `Detections(client_id, client_secret)` | Detection queries and management |
| `RealTimeResponse(client_id, client_secret)` | RTR session management |
| `SensorDownload(client_id, client_secret)` | Sensor installer download |
| `Prevention(client_id, client_secret)` | Prevention policy management |

## Key Methods

| Method | Description |
|--------|-------------|
| `hosts.query_devices_by_filter(filter=, limit=)` | Query host IDs |
| `hosts.get_device_details(ids=[])` | Get host details |
| `hosts.perform_action(action_name="contain", ids=[])` | Contain/lift containment |
| `detections.query_detects(filter=, sort=)` | Query detection IDs |
| `detections.get_detect_summaries(body={"ids": []})` | Get detection details |

## FQL Filter Examples

```
platform_name:'Windows' + status:'normal'
last_seen:>='2024-01-01T00:00:00Z'
hostname:'*server*'
```

## External References

- [FalconPy Documentation](https://www.falconpy.io/)
- [CrowdStrike API Swagger](https://assets.falcon.crowdstrike.com/support/api/swagger.html)
- [FalconPy GitHub](https://github.com/CrowdStrike/falconpy)

---

## Standards and Controls

## Primary Standards

### MITRE ATT&CK Enterprise Framework
- **Publisher**: MITRE Corporation
- **URL**: https://attack.mitre.org/
- **Relevance**: CrowdStrike Falcon maps detections to ATT&CK techniques; understanding ATT&CK is essential for tuning detection policies
- **Key tactics for EDR**: Initial Access, Execution, Persistence, Privilege Escalation, Defense Evasion, Lateral Movement

### NIST SP 800-83 Rev 1 - Guide to Malware Incident Prevention and Handling
- **Publisher**: NIST
- **Relevance**: Defines endpoint protection architecture including EDR placement and malware prevention controls

### CIS Control 10 - Malware Defenses
- **Publisher**: Center for Internet Security
- **Relevance**: CIS Controls v8 Control 10 mandates deploying anti-malware with centralized management and automated updates

## CrowdStrike-Specific References

### CrowdStrike Falcon Deployment Guide
- **Scope**: Official deployment procedures for Windows, macOS, Linux sensors
- **Key sections**: Silent install parameters, proxy configuration, sensor grouping tags
- **Access**: Falcon Console → Support → Documentation

### CrowdStrike Falcon API Documentation
- **URL**: https://falcon.crowdstrike.com/documentation/
- **Scope**: OAuth2 authentication, host management, detection management, RTR APIs
- **Key endpoints**: /devices/queries/devices/v1, /detects/queries/detects/v1

### Falcon SIEM Integration Guide
- **Scope**: Event streaming via SIEM Connector, FDR, and direct API
- **Supported SIEMs**: Splunk, Elastic, Microsoft Sentinel, IBM QRadar, ArcSight

## Compliance Mappings

| Framework | Requirement | CrowdStrike Coverage |
|-----------|------------|---------------------|
| PCI DSS 4.0 | 5.2 - Anti-malware on systems | Falcon sensor on all in-scope endpoints |
| HIPAA | 164.308(a)(5)(ii)(B) - Protection from malware | Falcon prevention + detection |
| SOC 2 | CC6.8 - Malicious software prevention | Falcon sensor with prevention policies |
| NIST 800-171 | 3.14.2 - Malicious code protection | Falcon ML + behavioral detection |
| ISO 27001 | A.12.2.1 - Controls against malware | Falcon sensor with automated response |

## Industry Benchmarks

- **MITRE Engenuity ATT&CK Evaluations**: CrowdStrike Falcon regularly achieves high detection scores in Enterprise evaluations
- **Gartner Magic Quadrant for Endpoint Protection**: CrowdStrike positioned as Leader
- **Forrester Wave Endpoint Detection and Response**: CrowdStrike rated Strong Performer/Leader

---

## Workflows

## Workflow 1: Enterprise Sensor Rollout

```
[Plan Deployment]
    │
    ├── Obtain Falcon Console access and CID
    ├── Download sensor installer for each OS
    ├── Create deployment groups (Workstations, Servers, VDI)
    │
    ▼
[Configure Policies Before Deployment]
    │
    ├── Create prevention policies per group
    ├── Configure sensor update policies (pinned vs. auto-update)
    ├── Set sensor grouping tags for auto-assignment
    │
    ▼
[Pilot Deployment (5% of endpoints)]
    │
    ├── Deploy via SCCM/Intune to pilot group
    ├── Monitor for 1 week: performance impact, false positives
    ├── Tune exclusions for LOB applications
    │
    ▼
[Validation]
    │
    ├── All pilot hosts show "Online" in Falcon Console
    ├── Test detection with CsTestDetect
    ├── No critical application breakage
    │
    ▼
[Production Rollout (phased)]
    │
    ├── Phase 1: Workstations (2 weeks)
    ├── Phase 2: Standard servers (2 weeks)
    ├── Phase 3: Critical servers (1 week, change window)
    │
    ▼
[Post-Deployment]
    │
    ├── Enable SIEM integration
    ├── Configure automated response policies
    ├── Establish exclusion review cadence (monthly)
    └── Train SOC on Falcon Console workflows
```

## Workflow 2: Detection Triage in Falcon Console

```
[New Detection Alert]
    │
    ▼
[Review Detection in Falcon Console]
    │
    ├── Severity: Critical/High/Medium/Low/Informational
    ├── Tactic & Technique (ATT&CK mapping)
    ├── Process tree visualization
    ├── Network connections
    │
    ▼
[Assess: True Positive or False Positive?]
    │
    ├── True Positive ──► [Contain Host via Network Containment]
    │                          │
    │                          ▼
    │                     [Launch RTR session for investigation]
    │                          │
    │                          ▼
    │                     [Collect artifacts, kill malicious processes]
    │                          │
    │                          ▼
    │                     [Remediate and release from containment]
    │
    └── False Positive ──► [Create exclusion rule]
                                │
                                ▼
                           [Document exclusion with justification]
                                │
                                ▼
                           [Mark detection as false positive]
```

## Workflow 3: Sensor Troubleshooting

```
[Sensor Issue Reported]
    │
    ▼
[Check Falcon Console Host Status]
    │
    ├── Online ──► [Issue is not connectivity; check policy assignment]
    │
    └── Offline / RFM ──► [Check network connectivity]
                               │
                               ├── Can reach ts01-b.cloudsink.net:443?
                               │     │
                               │     ├── Yes ──► [Check proxy settings]
                               │     │              ▼
                               │     │          [Reconfigure: falconctl -s --apd=false --aph=proxy --app=8080]
                               │     │
                               │     └── No ──► [Firewall blocking; add CrowdStrike domains to allowlist]
                               │
                               ▼
                          [Check sensor service status]
                               │
                               ├── Service running ──► [Review sensor logs in C:\Windows\System32\drivers\CrowdStrike\]
                               │
                               └── Service stopped ──► [Restart: sc start csagent (Windows) or systemctl start falcon-sensor (Linux)]
```

## Workflow 4: Sensor Version Upgrade

```
[New Sensor Version Available]
    │
    ▼
[Review Release Notes in Falcon Console]
    │
    ▼
[Test on pilot group (N-1 update policy)]
    │
    ├── No issues after 1 week ──► [Move production to N update policy]
    │
    └── Issues found ──► [Hold on current version, file support ticket]
                              │
                              ▼
                         [Pin current version in sensor update policy]
```

---

## Working Template

## Deployment Information

| Field | Value |
|-------|-------|
| Falcon Tenant | |
| Customer ID (CID) | |
| Sensor Version | |
| Deployment Tool | SCCM / Intune / GPO / Ansible / Manual |
| Target Environment | Production / Staging / Dev |
| Deployment Date | |
| Deployment Lead | |

## Pre-Deployment Checklist

- [ ] Falcon Console access verified with Administrator role
- [ ] CID obtained from Sensor downloads page
- [ ] Sensor installer downloaded for all target OS platforms
- [ ] Network connectivity verified: endpoints can reach ts01-b.cloudsink.net:443
- [ ] Proxy configuration documented (if applicable)
- [ ] Prevention policies created for each endpoint group
- [ ] Sensor update policy configured (auto-update or pinned version)
- [ ] Existing AV/EDR removal plan documented
- [ ] Exclusion list prepared for known LOB applications
- [ ] Change management ticket approved

## Deployment Scope

| Endpoint Group | Count | OS | Policy | Deployment Phase |
|---------------|-------|-----|--------|-----------------|
| Workstations | | Windows 11 | WS-Prevention-L1 | Phase 1 |
| Standard Servers | | Windows Server 2022 | SRV-Prevention | Phase 2 |
| Linux Servers | | Ubuntu 22.04 | LNX-Prevention | Phase 2 |
| macOS Endpoints | | macOS Ventura | MAC-Prevention | Phase 3 |
| Critical Servers | | Mixed | CRIT-Prevention | Phase 4 |

## Policy Configuration

### Prevention Policy Settings

| Setting | Workstations | Servers | Critical |
|---------|-------------|---------|----------|
| Cloud ML | Aggressive | Moderate | Aggressive |
| Sensor ML | Moderate | Cautious | Moderate |
| On Write | Enabled | Enabled | Enabled |
| Script-based Execution | Enabled | Enabled | Enabled |
| Ransomware Protection | Enabled | Enabled | Enabled |
| Exploit Protection | Enabled | Enabled | Enabled |

### Exclusions Applied

| Path/Process | Reason | Policy Group | Approved By |
|-------------|--------|-------------|-------------|
| | | | |

## Post-Deployment Validation

- [ ] All target endpoints show "Online" in Falcon Console
- [ ] Correct prevention policy applied to each host group
- [ ] Test detection generated with CsTestDetect and visible in console
- [ ] No RFM (Reduced Functionality Mode) hosts
- [ ] No critical application performance degradation reported
- [ ] SIEM integration receiving events
- [ ] RTR access verified for IR team

## Deployment Metrics

| Metric | Target | Actual |
|--------|--------|--------|
| Coverage (% of endpoints with sensor) | 100% | |
| Online rate | >98% | |
| Sensor version compliance | >95% same version | |
| Policy assignment accuracy | 100% | |
| Mean time to deploy (per phase) | <5 business days | |

## Issues and Remediation

| Issue | Affected Hosts | Root Cause | Resolution | Status |
|-------|---------------|------------|-----------|--------|
| | | | | |

## Sign-Off

| Role | Name | Date |
|------|------|------|
| Security Engineer | | |
| IT Operations | | |
| SOC Manager | | |
