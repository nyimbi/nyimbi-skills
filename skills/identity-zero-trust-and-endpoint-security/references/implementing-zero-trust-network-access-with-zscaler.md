# Implementing Zero Trust Network Access With Zscaler

## API Reference

## ZPA Management API

### Authentication
```
POST https://config.private.zscaler.com/signin
Body: client_id=X&client_secret=Y
Returns: {"access_token": "...", "token_type": "Bearer"}
```

### Application Segments
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{id}/application` | List app segments |
| POST | `/mgmtconfig/v1/admin/customers/{id}/application` | Create app segment |

### Server Groups
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{id}/serverGroup` | List server groups |

### Access Policies
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{id}/policySet/rules` | List policy rules |

### Connectors
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/mgmtconfig/v1/admin/customers/{id}/connector` | List connectors |

### App Segment Fields
| Field | Description |
|-------|-------------|
| `name` | Application segment name |
| `enabled` | Whether segment is active |
| `bypassType` | `NEVER`, `ALWAYS`, or `ON_NET` |
| `domainNames` | FQDN list for the segment |
| `tcpPortRanges` | Allowed TCP port ranges |

### Bypass Types
| Value | Security Implication |
|-------|---------------------|
| `NEVER` | Always enforce ZPA (recommended) |
| `ALWAYS` | Bypass ZPA entirely (high risk) |
| `ON_NET` | Bypass when on corporate network |

## References
- ZPA API: https://help.zscaler.com/zpa/about-zpa-api
- ZPA Admin Guide: https://help.zscaler.com/zpa

---

## Standards and Controls

## NIST SP 800-207: Zero Trust Architecture

### Core Tenets Applicable to ZTNA
1. **All data sources and computing services are considered resources** - Every application behind ZPA is treated as a discrete resource requiring explicit access grants
2. **All communication is secured regardless of network location** - ZPA encrypts all tunnels end-to-end regardless of whether users are on-premises or remote
3. **Access to individual enterprise resources is granted on a per-session basis** - ZPA evaluates policy for each connection request rather than granting persistent network access
4. **Access to resources is determined by dynamic policy** - ZPA policies incorporate identity, device posture, location, and behavioral signals
5. **The enterprise monitors and measures the integrity and security posture of all owned and associated assets** - Device posture checks validate endpoint compliance before granting access
6. **All resource authentication and authorization are dynamic and strictly enforced before access is allowed** - ZPA requires authentication through IdP and authorization through policy engine for every session

### NIST ZTA Deployment Models
- **Enhanced Identity Governance**: ZPA implements this model by using identity as the primary decision factor combined with device trust signals
- **Micro-Segmentation**: ZPA application segments function as software-defined microsegments at the application layer
- **Software Defined Perimeters**: ZPA directly implements the SDP model with its broker-based architecture

### NIST SP 800-207A: Zero Trust Architecture Model for Cloud-Native Applications
- Extends zero trust principles to multi-cloud environments
- ZPA App Connectors can be deployed across AWS, Azure, GCP, and on-premises
- Supports workload-to-workload zero trust with ZPA for workloads

## CISA Zero Trust Maturity Model v2.0

### Network Pillar
| Maturity Level | Capability | ZPA Implementation |
|---|---|---|
| Traditional | Macro-segmentation with static rules | Legacy VPN replaced by ZPA |
| Initial | Define network architecture with isolation | App Connectors isolate segments |
| Advanced | Micro-perimeters with identity-based access | Per-app segments with IdP integration |
| Optimal | Dynamic microsegmentation with continuous verification | Real-time posture + behavioral analytics |

### Identity Pillar
| Maturity Level | Capability | ZPA Implementation |
|---|---|---|
| Traditional | Password-based, agency-managed | Basic IdP integration |
| Initial | MFA for privileged users, federated identity | SAML/OIDC with IdP, SCIM provisioning |
| Advanced | MFA for all users, phishing-resistant | Conditional access with posture checks |
| Optimal | Continuous validation, risk-based authentication | ZPA + CrowdStrike/UEBA integration |

### Devices Pillar
| Maturity Level | Capability | ZPA Implementation |
|---|---|---|
| Traditional | Limited device visibility | Manual device inventory |
| Initial | Compliance enforcement for some devices | Basic posture profiles |
| Advanced | Real-time device analytics | CrowdStrike ZTA score integration |
| Optimal | Continuous diagnostics and mitigation | EDR-driven dynamic access decisions |

## CSA Software-Defined Perimeter Specification v2.0

### SDP Architecture Mapping to ZPA
| SDP Component | ZPA Equivalent |
|---|---|
| SDP Controller | ZPA Service Edge + Policy Engine |
| Initiating Host (IH) | Client Connector |
| Accepting Host (AH) | App Connector |
| SDP Gateway | ZPA Service Edge |

### SDP Deployment Models
- **Client-to-Gateway**: Standard ZPA deployment (user to application via Service Edge)
- **Client-to-Server**: ZPA Browser Access (direct browser connection through Service Edge)
- **Server-to-Server**: ZPA Workload-to-Workload (App Connector to App Connector)
- **Client-to-Server-to-Client**: Not directly supported in ZPA

## DoD Zero Trust Reference Architecture v2.0

### Pillar Alignment
- ZPA maps to the **Network & Environment** pillar through application-layer microsegmentation
- ZPA maps to the **User** pillar through IdP integration and continuous authentication
- ZPA maps to the **Device** pillar through endpoint posture assessment
- ZPA maps to the **Application & Workload** pillar through per-application access control
- Visibility & Analytics pillar addressed through ZPA log streaming and analytics dashboards

## Compliance Mapping

| Regulation | Requirement | ZPA Capability |
|---|---|---|
| NIST 800-53 AC-4 | Information flow enforcement | Application segment policies |
| NIST 800-53 AC-17 | Remote access | ZTNA replaces VPN |
| PCI DSS 4.0 Req 1 | Network security controls | Microsegmentation per cardholder segment |
| HIPAA 164.312(e) | Transmission security | End-to-end encrypted tunnels |
| SOX Section 404 | Access controls over financial systems | Auditable per-session access logs |
| FedRAMP | Continuous monitoring | ZPA FedRAMP Moderate authorized |

---

## Workflows

## Workflow 1: Initial ZPA Deployment

```
┌─────────────────┐
│ Pre-Assessment   │
│ - Inventory apps │
│ - Map user groups│
│ - Classify data  │
└───────┬─────────┘
        v
┌─────────────────────┐
│ IdP Integration      │
│ - SAML/OIDC config   │
│ - SCIM provisioning  │
│ - MFA enrollment     │
│ - Test SSO flow      │
└───────┬─────────────┘
        v
┌─────────────────────┐
│ App Connector Deploy │
│ - Provision VMs      │
│ - Generate enroll key│
│ - Install + enroll   │
│ - Health validation  │
└───────┬─────────────┘
        v
┌─────────────────────┐
│ Application Segments │
│ - Define apps by     │
│   FQDN/IP + ports   │
│ - Create seg groups  │
│ - Map to server grps │
└───────┬─────────────┘
        v
┌─────────────────────┐
│ Access Policies      │
│ - User->App mapping  │
│ - Posture conditions │
│ - Deny rules         │
│ - Priority ordering  │
└───────┬─────────────┘
        v
┌─────────────────────┐
│ Client Deployment    │
│ - Package connector  │
│ - MDM distribution   │
│ - Forwarding profile │
│ - User acceptance    │
└───────┬─────────────┘
        v
┌─────────────────────┐
│ Validation & Monitor │
│ - Access testing     │
│ - SIEM integration   │
│ - Dashboard setup    │
│ - Incident playbooks │
└─────────────────────┘
```

## Workflow 2: Access Request Evaluation (Runtime)

```
User Request
    │
    v
┌──────────────────┐    ┌──────────────────┐
│ Client Connector  │───>│ ZPA Service Edge  │
│ - Capture request │    │ - Receive tunnel  │
│ - Forward to edge │    │ - Identify user   │
└──────────────────┘    └────────┬─────────┘
                                 │
                    ┌────────────v────────────┐
                    │ Authentication          │
                    │ - Redirect to IdP       │
                    │ - Validate SAML/OIDC    │
                    │ - Check MFA completion  │
                    └────────────┬────────────┘
                                 │
                    ┌────────────v────────────┐
                    │ Authorization            │
                    │ - Match access policies  │
                    │ - Evaluate posture       │
                    │ - Check context signals  │
                    │ - Apply least privilege  │
                    └────────────┬────────────┘
                                 │
                    ┌────YES─────┴─────NO────┐
                    v                         v
           ┌──────────────┐         ┌──────────────┐
           │ Grant Access  │         │ Deny Access   │
           │ - Select App  │         │ - Log denial  │
           │   Connector   │         │ - Alert SIEM  │
           │ - Stitch tunnel│        │ - User notify │
           │ - Monitor     │         └──────────────┘
           └──────────────┘
```

## Workflow 3: VPN-to-ZTNA Migration

```
Phase 1: Assessment (Weeks 1-2)
├── Catalog all VPN-accessed applications
├── Map user groups to applications
├── Identify application dependencies
├── Baseline VPN performance metrics
└── Document compliance requirements

Phase 2: Parallel Deployment (Weeks 3-6)
├── Deploy ZPA alongside existing VPN
├── Configure App Connectors for pilot apps
├── Create policies mirroring VPN ACLs
├── Deploy Client Connector to pilot users
└── Validate access and performance

Phase 3: Migration Waves (Weeks 7-16)
├── Wave 1: Low-risk web applications
├── Wave 2: Business-critical web apps
├── Wave 3: Non-web TCP/UDP applications
├── Wave 4: Legacy applications
└── Each wave: test → validate → migrate → monitor

Phase 4: VPN Decommission (Weeks 17-20)
├── Verify all applications accessible via ZPA
├── Disable VPN for migrated user groups
├── Monitor for access issues (2-week soak)
├── Decommission VPN concentrators
└── Update disaster recovery documentation
```

## Workflow 4: Device Posture Enforcement

```
┌───────────────────┐
│ Device Connects    │
└───────┬───────────┘
        v
┌───────────────────┐
│ Posture Assessment │
│ - OS version       │
│ - Patch level      │
│ - Disk encryption  │
│ - AV/EDR status    │
│ - Firewall enabled │
│ - Domain joined    │
└───────┬───────────┘
        v
┌───────────────────┐
│ Posture Evaluation │
│ Compare against    │
│ posture profiles   │
└───┬──────────┬────┘
    │          │
  PASS       FAIL
    │          │
    v          v
┌────────┐ ┌──────────────────┐
│ Full   │ │ Restricted Access │
│ Access │ │ - Browser only    │
└────────┘ │ - Limited apps    │
           │ - Remediation msg │
           └──────────────────┘
```

## Workflow 5: Incident Response with ZPA

```
Alert Triggered (SIEM/SOAR)
    │
    v
┌──────────────────┐
│ 1. Triage         │
│ - Review ZPA logs │
│ - Identify user   │
│ - Identify app    │
│ - Classify event  │
└───────┬──────────┘
        v
┌──────────────────┐
│ 2. Containment    │
│ - Revoke user     │
│   access in ZPA   │
│ - Isolate app     │
│   segment         │
│ - Block device    │
│   via posture     │
└───────┬──────────┘
        v
┌──────────────────┐
│ 3. Investigation  │
│ - Pull session    │
│   logs from ZPA   │
│ - Correlate with  │
│   IdP/EDR/SIEM    │
│ - Map lateral     │
│   movement        │
└───────┬──────────┘
        v
┌──────────────────┐
│ 4. Recovery       │
│ - Update policies │
│ - Re-enable access│
│ - Post-incident   │
│   review          │
└──────────────────┘
```

---

## Working Template

## Project Information

| Field | Value |
|---|---|
| Project Name | |
| Organization | |
| Project Lead | |
| Start Date | |
| Target Completion | |
| ZPA Tenant ID | |

## Current State Assessment

### Existing Remote Access
- **VPN Solution**: [e.g., Cisco AnyConnect, Palo Alto GlobalProtect]
- **Concurrent VPN Users**: [number]
- **VPN Concentrator Locations**: [list]
- **Known VPN Issues**: [latency, split-tunnel risks, capacity]

### Application Inventory

| App Name | FQDN/IP | Port | Protocol | User Groups | Criticality | Migration Wave |
|---|---|---|---|---|---|---|
| | | | | | | |
| | | | | | | |

### Identity Provider
- **Primary IdP**: [Azure AD / Okta / Ping Identity / Other]
- **MFA Enabled**: [Yes/No - Method]
- **SCIM Supported**: [Yes/No]
- **Federation Protocol**: [SAML 2.0 / OIDC]

## ZPA Architecture Design

### App Connector Placement

| Environment | Location | VM Count | Server Group |
|---|---|---|---|
| Primary DC | | 2 | |
| DR Site | | 2 | |
| AWS VPC | | 2 | |
| Azure VNet | | 2 | |

### Application Segments

| Segment Name | Domains/IPs | TCP Ports | UDP Ports | Server Group | Browser Access |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |

### Access Policy Matrix

| Policy Name | User Groups | App Segments | Posture Profile | Conditions | Action |
|---|---|---|---|---|---|
| | | | | | Allow |
| | | | | | Allow |
| Block Default | All | All | None | None | Deny |

### Device Posture Profiles

| Profile Name | OS | Min Version | Disk Encryption | AV/EDR Required | Domain Joined |
|---|---|---|---|---|---|
| Corporate Managed | Windows | 10 22H2+ | BitLocker | CrowdStrike | Yes |
| Corporate Managed | macOS | 14.0+ | FileVault | CrowdStrike | No |
| BYOD | Any | Current-1 | Any | Any | No |

## Migration Plan

### Wave 1: Low-Risk Web Applications (Weeks 1-2)
- [ ] Applications: [list]
- [ ] User groups: [list]
- [ ] Success criteria: [define]
- [ ] Rollback plan: [define]

### Wave 2: Business-Critical Web Apps (Weeks 3-5)
- [ ] Applications: [list]
- [ ] User groups: [list]
- [ ] Success criteria: [define]
- [ ] Rollback plan: [define]

### Wave 3: Non-Web TCP/UDP Applications (Weeks 6-8)
- [ ] Applications: [list]
- [ ] User groups: [list]
- [ ] Success criteria: [define]
- [ ] Rollback plan: [define]

### Wave 4: Legacy Applications (Weeks 9-12)
- [ ] Applications: [list]
- [ ] User groups: [list]
- [ ] Success criteria: [define]
- [ ] Rollback plan: [define]

## SIEM Integration

| Field | Value |
|---|---|
| SIEM Platform | [Splunk / Sentinel / QRadar / Other] |
| Log Streaming Method | [HTTPS / Syslog / Cloud NSS] |
| Log Types | [User Activity / App Connector Status / Policy Violations] |
| Retention Period | |
| Alert Rules | |

## Testing Plan

### Functional Tests
- [ ] User authentication via IdP
- [ ] Application access per policy
- [ ] Device posture enforcement
- [ ] Browser Access for web apps
- [ ] Failover between App Connectors
- [ ] Client Connector auto-update

### Security Tests
- [ ] Unauthorized user access denied
- [ ] Non-compliant device blocked or restricted
- [ ] No lateral movement between segments
- [ ] Log events captured in SIEM
- [ ] Incident response playbook tested

### Performance Tests
- [ ] Application latency within SLA
- [ ] Throughput meets requirements
- [ ] Service Edge selection optimal for user locations

## Sign-Off

| Stakeholder | Role | Approval | Date |
|---|---|---|---|
| | Network Security | | |
| | Identity Team | | |
| | Application Owners | | |
| | CISO / Security Lead | | |
| | IT Operations | | |
