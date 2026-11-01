# Deploying Osquery For Endpoint Monitoring

## API Reference

## Installation

| Platform | Command |
|----------|---------|
| macOS | `brew install osquery` |
| Ubuntu | `apt install osquery` |
| Windows | MSI installer from osquery.io |

## Key osquery Tables

| Table | Description |
|-------|-------------|
| `processes` | Running processes with pid, name, cmdline, uid |
| `listening_ports` | Open network ports with bound process |
| `suid_bin` | SUID/SGID binaries on the system |
| `crontab` | Scheduled cron jobs |
| `authorized_keys` | SSH authorized keys per user |
| `kernel_modules` | Loaded kernel modules |
| `docker_containers` | Docker container status |
| `startup_items` | Boot/login startup items |
| `file` | File metadata, hashes, timestamps |

## Fleet API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/fleet/hosts` | List enrolled hosts |
| GET | `/api/v1/fleet/hosts/{id}` | Host details |
| POST | `/api/v1/fleet/queries` | Create scheduled query |
| GET | `/api/v1/fleet/queries` | List queries |

## osquery CLI

```bash
osqueryi --json "SELECT * FROM processes LIMIT 5"
osqueryctl start   # Start osquery daemon
osqueryctl config-check  # Validate configuration
```

## External References

- [osquery Schema](https://osquery.io/schema/)
- [Fleet Documentation](https://fleetdm.com/docs)
- [osquery Packs](https://github.com/osquery/osquery/tree/master/packs)

---

## Standards and Controls

- **Osquery Documentation**: https://osquery.readthedocs.io/
- **Osquery Schema**: https://osquery.io/schema/
- **FleetDM Documentation**: https://fleetdm.com/docs
- **NIST SP 800-53 SI-4**: System Monitoring - osquery provides endpoint visibility
- **CIS Control 1**: Inventory of Enterprise Assets - osquery software/hardware inventory
- **CIS Control 2**: Software Inventory - osquery package/process queries

---

## Workflows

## Workflow 1: Osquery Fleet Deployment
```
[Install FleetDM server] → [Generate enrollment secret]
  → [Package osquery with fleet config] → [Deploy to pilot group]
  → [Verify enrollment and scheduled queries] → [Deploy to production]
  → [Create dashboards from query results] → [Ongoing monitoring]
```

## Workflow 2: Threat Hunt with Osquery
```
[Define hypothesis] → [Write SQL query targeting hypothesis]
  → [Execute via FleetDM live query across fleet]
  → [Analyze results] → [Investigate anomalies]
  → [Document findings] → [Create scheduled detection if recurrent]
```

---

## Working Template

## Deployment Info
| Field | Value |
|-------|-------|
| Osquery Version | |
| Fleet Server | |
| Target Endpoints | |
| Enrollment Secret | [stored securely] |

## Scheduled Queries
| Query Name | Interval | Description | Status |
|-----------|----------|-------------|--------|
| process_monitor | 300s | Fileless process detection | Active |
| listening_ports | 600s | Open port monitoring | Active |
| persistence_check | 3600s | Startup item monitoring | Active |

## Sign-Off
| Role | Name | Date |
|------|------|------|
| Security | | |
| IT Ops | | |
