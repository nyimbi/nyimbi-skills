# Configuring Microsegmentation For Zero Trust

## API Reference

## Libraries

| Library | Install | Purpose |
|---------|---------|---------|
| boto3 | `pip install boto3` | AWS security group audit |
| requests | `pip install requests` | Illumio / Guardicore API client |

## Key boto3 EC2 Methods

| Method | Description |
|--------|-------------|
| `describe_security_groups()` | List SGs with inbound/outbound rules |
| `authorize_security_group_ingress()` | Add inbound rule |
| `revoke_security_group_ingress()` | Remove inbound rule |

## Illumio PCE API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v2/orgs/{id}/workloads` | List managed workloads |
| GET | `/api/v2/orgs/{id}/sec_policy/draft/rule_sets` | List rule sets |
| PUT | `/api/v2/orgs/{id}/workloads/{id}` | Update workload enforcement mode |

## Segmentation Enforcement Modes

| Mode | Description |
|------|-------------|
| Visibility Only | Monitor traffic without blocking |
| Selective | Block specific flows, allow rest |
| Full | Deny all, allow by policy (zero trust) |

## External References

- [Illumio API Guide](https://docs.illumio.com/core/23.5/API-Reference/index.html)
- [NIST SP 800-207 Zero Trust Architecture](https://csrc.nist.gov/publications/detail/sp/800-207/final)
- [AWS Security Groups Best Practices](https://docs.aws.amazon.com/vpc/latest/userguide/security-group-rules.html)

---

## Standards and Controls

## NIST SP 800-207: Zero Trust Architecture

### Microsegmentation as ZTA Deployment Model
NIST SP 800-207 identifies microsegmentation as one of three primary deployment approaches for zero trust:
- Places individual or groups of resources on a unique network segment protected by a gateway security component
- The enterprise places infrastructure devices such as intelligent switches, next-generation firewalls, or special-purpose gateway devices to act as PEPs protecting each resource or group of resources
- This approach can be implemented using software-defined networking (SDN) or hypervisor-level enforcement

### Applicable Controls
- **AC-4 (Information Flow Enforcement)**: Microsegmentation enforces approved information flows between workloads
- **SC-7 (Boundary Protection)**: Each microsegment boundary acts as a security boundary
- **SI-4 (Information System Monitoring)**: Microsegmentation tools provide flow telemetry for monitoring

## CISA Zero Trust Maturity Model v2.0

### Network Pillar - Microsegmentation Maturity

| Level | Network Segmentation | Microsegmentation | Traffic Management |
|---|---|---|---|
| Traditional | Large, macro-segmented perimeters | None | Static ACLs |
| Initial | Defined architecture with some isolation | Initial workload isolation | Basic flow visibility |
| Advanced | Ingress/egress micro-perimeters | Workload-level microsegmentation | Identity-based traffic rules |
| Optimal | Full microsegmentation, dynamically defined | Automated, adaptive policies | ML-driven anomaly detection |

### Cross-Cutting: Visibility and Analytics
- Flow telemetry from microsegmentation agents feeds into SIEM/SOAR
- Application dependency maps provide baseline for anomaly detection
- Policy violation alerts enable real-time incident detection

## PCI DSS v4.0

### Microsegmentation for Scope Reduction
- **Requirement 1.3**: Network controls restrict access to and from the cardholder data environment (CDE)
- **Requirement 1.4**: Network connections between trusted and untrusted networks are controlled
- Microsegmentation can reduce PCI scope by isolating CDE workloads from non-CDE systems
- Compensating control: host-based microsegmentation validated by QSA as equivalent to network segmentation

## Forrester Zero Trust eXtended (ZTX) Framework

### Workload Security Pillar
- Microsegmentation is a core capability for securing workloads
- Policies should be based on workload identity and context, not network location
- Continuous monitoring of east-west traffic for anomaly detection
- Integration with DevOps pipelines for automated policy management

## VMware NSX Distributed Firewall

### Architecture
- Stateful Layer 4-7 firewall embedded in the hypervisor kernel
- Policies evaluated at the vNIC level before traffic reaches the physical network
- Context-aware rules using Active Directory groups, VM tags, and application identification
- No network topology changes required for deployment

## Illumio Core Platform

### Architecture
- Virtual Enforcement Node (VEN) agents installed on workloads
- Policy Compute Engine (PCE) centralizes policy management and visualization
- Enforcement via native OS firewall (iptables on Linux, WFP on Windows)
- Label-based policy model: Role, Application, Environment, Location

## Guardicore (Akamai)

### Architecture
- Lightweight agents provide process-level visibility and enforcement
- Reveal module builds application dependency maps
- Centra management platform for policy creation and monitoring
- Supports bare-metal, VM, container, and cloud workloads

---

## Workflows

## Workflow 1: Microsegmentation Deployment Lifecycle

```
┌──────────────────────┐
│ 1. Discovery          │
│ - Deploy agents       │
│ - Collect traffic     │
│   telemetry (2-4 wks)│
│ - Build flow map      │
└──────────┬───────────┘
           v
┌──────────────────────┐
│ 2. Classification     │
│ - Assign workload     │
│   labels (role, app,  │
│   env, location)      │
│ - Validate with CMDB  │
│ - Group by app tier   │
└──────────┬───────────┘
           v
┌──────────────────────┐
│ 3. Policy Design      │
│ - Define zones        │
│ - Create allow-list   │
│   rules per app       │
│ - Set default-deny    │
│ - Document exceptions │
└──────────┬───────────┘
           v
┌──────────────────────┐
│ 4. Test Mode          │
│ - Enable policies in  │
│   visibility mode     │
│ - Monitor would-block │
│   events (1-2 weeks)  │
│ - Refine rules        │
└──────────┬───────────┘
           v
┌──────────────────────┐
│ 5. Enforcement        │
│ - Enforce per-app,    │
│   starting low-risk   │
│ - Monitor 24-48 hrs   │
│ - Proceed to next app │
└──────────┬───────────┘
           v
┌──────────────────────┐
│ 6. Continuous Ops     │
│ - Weekly violation    │
│   review              │
│ - Quarterly audits    │
│ - CI/CD integration   │
│ - Incident response   │
└──────────────────────┘
```

## Workflow 2: Policy Creation Flow

```
Identify Application
    │
    v
┌─────────────────────┐
│ Map Dependencies     │
│ - Inbound sources    │
│ - Outbound targets   │
│ - Ports/protocols    │
│ - Process names      │
└──────────┬──────────┘
           v
┌─────────────────────┐
│ Define Labels        │
│ Role: web/app/db     │
│ App: erp/crm/hr      │
│ Env: prod/dev/stg    │
│ Loc: dc1/aws/azure   │
└──────────┬──────────┘
           v
┌─────────────────────┐
│ Create Rules         │
│ Allow: web→app:8080  │
│ Allow: app→db:3306   │
│ Allow: mon→all:9090  │
│ Deny: all other      │
└──────────┬──────────┘
           v
┌─────────────────────┐
│ Test and Validate    │
│ - Simulate in test   │
│ - Check flow map     │
│ - App owner sign-off │
└──────────┬──────────┘
           v
┌─────────────────────┐
│ Enforce and Monitor  │
│ - Switch to enforce  │
│ - Alert on violations│
│ - Log to SIEM        │
└─────────────────────┘
```

## Workflow 3: Ring-Fencing Critical Assets

```
Identify Critical Asset (e.g., PCI CDE Database)
    │
    v
┌──────────────────────────────────────┐
│ 1. Baseline Traffic                   │
│ - Observe all inbound/outbound flows │
│ - Document legitimate connections    │
│ - Identify unnecessary connections   │
└──────────────┬───────────────────────┘
               v
┌──────────────────────────────────────┐
│ 2. Define Ring-Fence Rules            │
│ - Allow: app-server → db:5432        │
│ - Allow: backup-agent → db:5432      │
│ - Allow: monitoring → db:9100        │
│ - Deny: ALL other inbound            │
│ - Deny: ALL outbound (except DNS,NTP)│
└──────────────┬───────────────────────┘
               v
┌──────────────────────────────────────┐
│ 3. Test with Production Traffic       │
│ - Enable in test mode                 │
│ - Verify zero false positives         │
│ - Validate backup and monitoring work │
└──────────────┬───────────────────────┘
               v
┌──────────────────────────────────────┐
│ 4. Enforce and Lock Down              │
│ - Switch to enforcement               │
│ - Enable alerting on any violation    │
│ - Review violations daily             │
│ - QSA validation for PCI scope       │
└──────────────────────────────────────┘
```

## Workflow 4: Incident Response with Microsegmentation

```
Alert: Unusual East-West Traffic Detected
    │
    v
┌─────────────────────────┐
│ 1. Investigate           │
│ - Review flow in console │
│ - Check source workload  │
│ - Identify destination   │
│ - Cross-ref with SIEM    │
└──────────┬──────────────┘
           v
┌──────────────────────────────┐
│ 2. Contain                    │
│ - Apply quarantine policy     │
│   (deny all except forensic) │
│ - Isolate compromised         │
│   workload instantly          │
└──────────┬───────────────────┘
           v
┌─────────────────────────┐
│ 3. Assess Impact         │
│ - Check if lateral move  │
│   was blocked by policy  │
│ - Review adjacent zones  │
│ - Determine blast radius │
└──────────┬──────────────┘
           v
┌─────────────────────────┐
│ 4. Remediate             │
│ - Patch/reimagevworkload │
│ - Strengthen policies    │
│ - Remove quarantine      │
│ - Post-incident review   │
└─────────────────────────┘
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
| Segmentation Tool | [Illumio / VMware NSX / Guardicore / Cisco ACI] |

## Workload Inventory

| Workload | IP Address | OS | Role | Application | Environment | Location |
|---|---|---|---|---|---|---|
| | | | web | | prod | |
| | | | app | | prod | |
| | | | db | | prod | |

## Segmentation Zone Design

### Zone Definitions

| Zone Name | Description | Workloads | Default Policy |
|---|---|---|---|
| PCI-CDE | Cardholder data environment | [list] | Deny-all |
| HR-Systems | HR applications | [list] | Deny-all |
| DMZ | Internet-facing services | [list] | Deny-all |
| Management | Admin/monitoring | [list] | Restricted |

### Inter-Zone Communication Matrix

| Source Zone | Destination Zone | Ports/Protocols | Justification |
|---|---|---|---|
| DMZ | App-Tier | 8080/tcp | Web application traffic |
| App-Tier | DB-Tier | 3306/tcp | Database queries |
| Management | All Zones | 22/tcp, 9090/tcp | SSH and monitoring |

## Policy Rules

### Allow Rules

| Rule ID | Source | Destination | Port | Protocol | Process | Justification |
|---|---|---|---|---|---|---|
| 1 | | | | tcp | | |
| 2 | | | | tcp | | |

### Default Deny
- All traffic not explicitly allowed is denied
- Deny rule logged and alerted

## Enforcement Schedule

| Week | Activity | Applications | Risk Level |
|---|---|---|---|
| 1-2 | Agent deployment and discovery | All | Low |
| 3-4 | Label assignment and validation | All | Low |
| 5-6 | Policy design and test mode | All | Low |
| 7 | Enforce: Dev/Test environments | Dev apps | Low |
| 8 | Enforce: Low-risk production | Non-critical | Medium |
| 9-10 | Enforce: Business-critical apps | ERP, CRM | High |
| 11-12 | Enforce: Regulated environments | PCI, HIPAA | High |

## Validation Tests

- [ ] Legitimate traffic flows uninterrupted after enforcement
- [ ] Unauthorized cross-zone traffic is blocked
- [ ] Lateral movement from compromised workload is contained
- [ ] Policy violation alerts appear in SIEM
- [ ] Break-glass procedure works for emergency access
- [ ] Application dependency map matches actual flows

## Sign-Off

| Stakeholder | Role | Approval | Date |
|---|---|---|---|
| | Security Architecture | | |
| | Network Operations | | |
| | Application Owners | | |
| | Compliance/Audit | | |
