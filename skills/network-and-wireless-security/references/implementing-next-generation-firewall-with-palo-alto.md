# Implementing Next Generation Firewall With Palo Alto

## API Reference

## PAN-OS XML API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/?type=keygen` | GET | Generate API key |
| `/api/?type=config&action=get` | GET | Get configuration |
| `/api/?type=config&action=set` | GET | Set configuration |
| `/api/?type=op` | POST | Operational commands |

## Authentication
```
GET https://<fw>/api/?type=keygen&user=admin&password=admin
```

## Configuration XPaths

| XPath | Description |
|-------|-------------|
| `/config/devices/.../vsys/.../rulebase/security/rules` | Security rules |
| `/config/devices/.../vsys/.../profiles` | Security profiles |
| `/config/devices/.../deviceconfig/system` | System config |

## pan-python Library

```bash
pip install pan-python
```
| Method | Description |
|--------|-------------|
| `pan.xapi.PanXapi(hostname, api_key)` | Create API client |
| `xapi.get(xpath)` | Get config element |
| `xapi.set(xpath, element)` | Set config element |

## Key Libraries

| Library | Use |
|---------|-----|
| `requests` | REST API calls |
| `pan-python` | PAN-OS SDK |
| `xml.etree` | XML response parsing |

---

## Standards and Controls

## Industry Standards

- **NIST SP 800-41 Rev 1** - Guidelines on Firewalls and Firewall Policy
- **NIST SP 800-53 Rev 5** - SC-7 (Boundary Protection), AC-4 (Information Flow Enforcement)
- **CIS Controls v8** - Control 4 (Secure Configuration), Control 9 (Email and Web Browser Protections), Control 13 (Network Monitoring and Defense)
- **PCI DSS v4.0** - Requirement 1 (Install and Maintain Network Security Controls)
- **ISO 27001:2022** - A.13.1 (Network Security Management)

## Palo Alto Specific Standards

- **PAN-OS Security Configuration Benchmark** - CIS Benchmark for Palo Alto firewalls
- **Best Practices for Completing NGFW Deployment** - docs.paloaltonetworks.com
- **Security Policy Best Practices** - Application-based rules, zone segmentation
- **SSL Decryption Best Practices** - Certificate management, excluded categories
- **Threat Prevention Best Practices** - Profile configuration for AV, AS, VP, URL, WildFire

## Compliance Mapping

| Control | PAN-OS Feature |
|---------|---------------|
| Access Control (AC-4) | Security Policies with App-ID and User-ID |
| Boundary Protection (SC-7) | Zone-based architecture with inter-zone policies |
| Malicious Code Protection (SI-3) | WildFire, Anti-Virus, Anti-Spyware profiles |
| Audit and Accountability (AU-3) | Traffic, Threat, URL, WildFire logging |
| Encryption (SC-8) | SSL/TLS decryption and inspection |
| DoS Protection (SC-5) | Zone Protection profiles with flood thresholds |

---

## Workflows

## Deployment Workflow

```
Phase 1: Planning
├── Document network topology and traffic flows
├── Define security zones and trust levels
├── Inventory applications and required access
├── Plan IP addressing and interface assignments
└── Define decryption policy scope and exclusions

Phase 2: Base Configuration
├── Configure management interface and system settings
├── Set up HA pair (active/passive)
├── Configure network interfaces and zones
├── Set up Zone Protection profiles
├── Configure routing (static or dynamic)
└── Integrate with DNS, NTP, LDAP/AD

Phase 3: Security Policy Development
├── Create Security Profile Groups (AV, AS, VP, URL, FB, WF)
├── Build application-based Security Policies
├── Configure SSL Decryption policies
├── Set up User-ID integration with AD
├── Create NAT policies
└── Configure DoS Protection policies

Phase 4: Logging and Monitoring
├── Configure Syslog/SIEM forwarding
├── Set up log forwarding profiles
├── Configure SNMP monitoring
├── Enable Cortex Data Lake integration
└── Create custom reports and dashboards

Phase 5: Testing and Validation
├── Validate application classification with Policy Optimizer
├── Test threat prevention with EICAR and test URLs
├── Verify SSL decryption certificate chain
├── Conduct penetration test against firewall
├── Review and remediate audit findings
└── Document final configuration baseline

Phase 6: Operations
├── Schedule automatic content updates
├── Monitor threat and traffic dashboards
├── Review Security Policy rule hit counts monthly
├── Conduct quarterly firewall rule review
├── Test HA failover quarterly
└── Upgrade PAN-OS per vendor schedule
```

## Change Management Workflow

```
1. Submit change request with business justification
2. Review impact analysis (affected zones, applications, users)
3. Approve through CAB (Change Advisory Board)
4. Clone current configuration as backup
5. Implement change in maintenance window
6. Validate with `validate full` before commit
7. Commit changes and monitor logs for 24 hours
8. Document changes in configuration management database
```

---

## Working Template

## Pre-Deployment Checklist

- [ ] Network topology documented with zone boundaries
- [ ] IP addressing scheme finalized for all interfaces
- [ ] HA pair hardware matched (same model, same licenses)
- [ ] Management network access configured
- [ ] DNS and NTP servers available
- [ ] Active Directory credentials for User-ID agent
- [ ] Internal CA certificate generated for SSL Forward Proxy
- [ ] License keys activated (Threat Prevention, URL Filtering, WildFire)
- [ ] Syslog/SIEM endpoint configured and reachable
- [ ] Change management ticket approved

## Zone Definitions Template

| Zone Name | Interfaces | Trust Level | Description |
|-----------|-----------|-------------|-------------|
| Trust | eth1/1 | High | Corporate LAN |
| Untrust | eth1/2 | None | Internet |
| DMZ | eth1/3 | Medium | Public-facing servers |
| Guest | eth1/4 | Low | Guest wireless |
| DC | eth1/5 | High | Data center servers |

## Security Profile Group Template

```
Group: Standard-Security-Profiles
├── Anti-Virus: default
├── Anti-Spyware: strict (sinkhole enabled)
├── Vulnerability: strict
├── URL Filtering: corporate-policy
├── File Blocking: block-dangerous-types
└── WildFire: forward-all-files
```

## Security Policy Template

| # | Name | From | To | Source | Destination | Application | Action | Profile |
|---|------|------|----|--------|-------------|-------------|--------|---------|
| 1 | Allow-DNS | Trust | Untrust | Any | DNS-Servers | dns | Allow | Standard |
| 2 | Allow-Web | Trust | Untrust | Any | Any | web-browsing,ssl | Allow | Standard |
| 3 | Allow-Business | Trust | Untrust | Any | Any | office365,salesforce | Allow | Standard |
| 4 | Block-HighRisk | Any | Any | Any | Any | bittorrent,tor | Deny | N/A |
| 5 | DMZ-Inbound | Untrust | DMZ | Any | Web-Servers | web-browsing,ssl | Allow | Standard |
| 6 | Deny-All | Any | Any | Any | Any | Any | Deny | N/A |

## Post-Deployment Validation

- [ ] All zones show correct interface assignments
- [ ] Traffic logs show App-ID classification working
- [ ] Threat Prevention blocking EICAR test file
- [ ] URL Filtering blocking test malware URLs
- [ ] SSL decryption certificate trusted by endpoints
- [ ] User-ID mapping active users correctly
- [ ] HA failover tested successfully
- [ ] SIEM receiving forwarded logs
- [ ] Zone Protection profiles applied to all zones
- [ ] No shadowed or unused rules in policy
