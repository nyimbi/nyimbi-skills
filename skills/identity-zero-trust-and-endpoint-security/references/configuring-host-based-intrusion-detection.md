# Configuring Host Based Intrusion Detection

## API Reference

## Libraries

| Library | Install | Purpose |
|---------|---------|---------|
| requests | `pip install requests` | Wazuh REST API client |
| osquery | Binary install | SQL-based host inspection |
| hashlib | stdlib | File integrity hash computation |

## Wazuh API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/security/user/authenticate` | Obtain JWT token |
| GET | `/agents` | List managed agents |
| GET | `/agents/{id}` | Agent details |
| GET | `/sca/{agent_id}` | Security Configuration Assessment results |
| GET | `/rootcheck/{agent_id}` | Rootkit check results |
| GET | `/alerts` | Query security alerts |
| GET | `/rules` | List detection rules |

## Key osquery Tables

| Table | Description |
|-------|-------------|
| `processes` | Running processes with user, path, cmdline |
| `listening_ports` | Open network ports and bound processes |
| `users` | System user accounts |
| `file` | File metadata and hashes |
| `suid_bin` | SUID/SGID binaries |
| `crontab` | Scheduled cron jobs |

## OSSEC Rule IDs

| Rule ID Range | Category |
|---------------|----------|
| 500-599 | File integrity monitoring |
| 5700-5799 | SSH authentication |
| 18100-18199 | Linux audit events |
| 31100-31199 | Web attack detection |

## External References

- [Wazuh API Reference](https://documentation.wazuh.com/current/user-manual/api/reference.html)
- [osquery Schema](https://osquery.io/schema/)
- [OSSEC Rule Syntax](https://www.ossec.net/docs/syntax/head_rules.html)

---

## Standards and Controls

## Primary Standards

### NIST SP 800-94 Rev 1 - Guide to Intrusion Detection and Prevention Systems
- **Publisher**: NIST
- **Scope**: Architecture, deployment, and management of IDPS including host-based systems

### PCI DSS 4.0 Requirement 11.5 - File Integrity Monitoring
- **Publisher**: PCI SSC
- **Requirement**: Deploy FIM to alert on unauthorized modification of critical files
- **Scope**: System files, configuration files, content files on in-scope systems

### CIS Control 3 - Data Protection (v8)
- **Publisher**: CIS
- **Relevance**: Sub-control 3.14 requires monitoring for unauthorized changes to sensitive data

## Compliance Mappings

| Framework | Requirement | HIDS Coverage |
|-----------|------------|--------------|
| PCI DSS 4.0 | 11.5.2 - FIM mechanism deployed | Wazuh syscheck module |
| NIST 800-53 | SI-7 Software, Firmware, and Information Integrity | File integrity monitoring |
| NIST 800-53 | SI-4 System Monitoring | HIDS log analysis and alerting |
| HIPAA | 164.312(b) - Audit controls | File access and change monitoring |
| ISO 27001 | A.12.4.1 - Event logging | HIDS event collection and analysis |

## Supporting References

- **Wazuh Documentation**: https://documentation.wazuh.com/
- **OSSEC Documentation**: https://www.ossec.net/docs/
- **Wazuh FIM Reference**: https://documentation.wazuh.com/current/user-manual/capabilities/file-integrity/
- **Wazuh Ruleset**: https://github.com/wazuh/wazuh-ruleset

---

## Workflows

## Workflow 1: Wazuh HIDS Deployment

```
[Deploy Wazuh Manager]
    │
    ▼
[Configure FIM, rootcheck, and log analysis modules]
    │
    ▼
[Deploy agents to pilot endpoints]
    │
    ▼
[Establish baseline (48 hours)]
    │
    ▼
[Tune rules: suppress false positives, add exclusions]
    │
    ▼
[Deploy agents to production fleet]
    │
    ▼
[Integrate with SIEM]
    │
    ▼
[Create dashboards and alert workflows]
```

## Workflow 2: FIM Alert Investigation

```
[FIM alert: File modified]
    │
    ▼
[Check file path and change details]
    │
    ├── Known system update ──► [Correlate with patch window, close alert]
    ├── Authorized config change ──► [Verify change ticket, close alert]
    └── Unauthorized change ──► [Investigate]
                                     │
                                     ├── Determine who/what changed the file
                                     ├── Review process tree and timeline
                                     │
                                     ├── Malicious ──► [Escalate to IR]
                                     └── Operational ──► [Update change process]
```

---

## Working Template

## Deployment Information

| Field | Value |
|-------|-------|
| HIDS Platform | Wazuh / OSSEC / AIDE |
| Manager Address | |
| Agent Version | |
| Target Endpoints | |
| Deployment Date | |

## FIM Configuration

| Directory | Real-time | Check All | Exclusions |
|-----------|----------|-----------|------------|
| /etc | Yes | Yes | mtab, resolv.conf |
| /usr/bin | Yes | Yes | |
| /usr/sbin | Yes | Yes | |
| C:\Windows\System32 | Yes | Yes | *.log |

## Monitoring Modules

| Module | Status | Frequency |
|--------|--------|-----------|
| Syscheck (FIM) | Enabled | 12 hours |
| Rootcheck | Enabled | 12 hours |
| Log Analysis | Enabled | Real-time |
| Active Response | Enabled | Real-time |
| Vulnerability Detection | Enabled | 12 hours |

## Custom Rules

| Rule ID | Description | Level | Trigger |
|---------|-------------|-------|---------|
| | | | |

## Sign-Off

| Role | Name | Date |
|------|------|------|
| Security Engineer | | |
| SOC Analyst | | |
