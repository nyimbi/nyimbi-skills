# Configuring Zscaler Private Access For Ztna

## API Reference

## Libraries

| Library | Install | Purpose |
|---------|---------|---------|
| requests | `pip install requests` | ZPA REST API client |
| zscaler-sdk-python | `pip install zscaler-sdk-python` | Official Zscaler Python SDK |

## ZPA API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/signin` | Authenticate and get bearer token |
| GET | `/mgmtconfig/v1/admin/customers/{id}/application` | List app segments |
| GET | `/mgmtconfig/v1/admin/customers/{id}/connector` | List app connectors |
| GET | `/mgmtconfig/v1/admin/customers/{id}/serverGroup` | List server groups |
| GET | `/mgmtconfig/v1/admin/customers/{id}/policySet/rules` | List access policies |
| GET | `/mgmtconfig/v1/admin/customers/{id}/segmentGroup` | List segment groups |

## Key ZPA Concepts

| Component | Description |
|-----------|-------------|
| App Segment | Application definition with domain/IP and port ranges |
| App Connector | On-premise agent that brokers connections to apps |
| Server Group | Group of application servers behind connectors |
| Access Policy | Rules defining who can access which app segments |
| Segment Group | Logical grouping of app segments |

## External References

- [ZPA API Documentation](https://help.zscaler.com/zpa/api)
- [Zscaler SDK Python](https://github.com/zscaler/zscaler-sdk-python)
- [ZPA Admin Guide](https://help.zscaler.com/zpa)

---

## Standards and Controls

## NIST SP 800-207: Zero Trust Architecture
- **Section 2.1**: Zero Trust Tenets - ZPA implements "never trust, always verify" with per-session application access
- **Section 3.1**: Policy Engine / Policy Administrator - maps to ZPA access policy engine
- **Section 3.3**: Agent/Gateway Model - maps to Zscaler Client Connector + App Connector architecture
- **URL**: https://csrc.nist.gov/publications/detail/sp/800-207/final

## CISA Zero Trust Maturity Model v2.0
- **Network Pillar**: Application micro-segmentation - ZPA application segments eliminate network-level access
- **Identity Pillar**: Continuous validation - ZPA evaluates identity and posture per session
- **URL**: https://www.cisa.gov/zero-trust-maturity-model

## Zscaler Documentation
- **ZPA Admin Guide**: https://help.zscaler.com/zpa
- **Step-by-Step Configuration**: https://help.zscaler.com/zpa/step-step-configuration-guide-zpa
- **App Connector Deployment**: https://help.zscaler.com/zpa/about-app-connectors
- **Access Policy Configuration**: https://help.zscaler.com/zpa/configuring-access-policies
- **Browser Access**: https://help.zscaler.com/zpa/about-browser-access
- **Log Streaming Service**: https://help.zscaler.com/zpa/about-log-streaming-service
- **ZPA Reference Architecture (AWS)**: https://help.zscaler.com/downloads/zpa/reference-architecture

## NIST SP 800-63-3: Digital Identity Guidelines
- **Section 4-6**: Identity assurance levels relevant to ZPA IdP integration
- **URL**: https://pages.nist.gov/800-63-3/

## SOX Compliance (Sarbanes-Oxley)
- **Section 302/404**: Access controls for financial systems - ZPA provides auditable per-application access
- Application-level access logging satisfies audit trail requirements

## Gartner ZTNA Market Guide
- ZPA classified as agent-based ZTNA with service-initiated architecture
- Reference: Gartner Market Guide for Zero Trust Network Access (2024)

---

## Workflows

## Phase 1: Planning and Prerequisites (Week 1)

### 1.1 Architecture Design
1. Map current VPN access patterns: which users access which applications
2. Identify all internal applications by FQDN, IP, and port
3. Group applications into logical segments by business function and sensitivity
4. Design App Connector placement: minimum 2 connectors per data center for HA
5. Plan DNS resolution: App Connectors must resolve all application FQDNs

### 1.2 Identity Provider Integration
1. Configure SAML 2.0 or OIDC integration with corporate IdP (Okta, Entra ID, Ping)
2. Map IdP user groups to ZPA access policy groups
3. Configure SCIM provisioning for automated user/group sync
4. Test SSO authentication flow end-to-end

## Phase 2: Infrastructure Deployment (Week 2-3)

### 2.1 App Connector Deployment
1. Provision Linux VMs (CentOS/RHEL/Ubuntu) meeting minimum specs (2 vCPU, 4GB RAM)
2. Ensure outbound HTTPS (443) to ZPA cloud domains (*.private.zscaler.com, *.zpath.net)
3. Generate provisioning keys in ZPA Admin Portal (one per App Connector Group)
4. Install and configure App Connector packages
5. Verify connector enrollment and health status in portal
6. Deploy second connector per group for high availability

### 2.2 Server Group and Application Segment Configuration
1. Create server groups mapping to App Connector groups
2. Add application servers with FQDNs and ports to server groups
3. Create application segments grouping related applications
4. Configure health monitoring for each segment
5. Test application reachability from App Connector

## Phase 3: Policy Configuration (Week 3-4)

### 3.1 Access Policy Design
1. Create allow rules ordered from most specific to least specific
2. Map IdP groups to application segments in each rule
3. Add device posture profile requirements to rules
4. Configure time-based restrictions for contractor access
5. Create default deny rule as the last policy rule
6. Test each policy rule with representative users

### 3.2 Device Posture Configuration
1. Define posture profiles for each device category (managed, developer, BYOD)
2. Integrate CrowdStrike ZTA scores for real-time posture
3. Configure OS version, encryption, and firewall requirements
4. Test posture evaluation with compliant and non-compliant devices

## Phase 4: User Migration (Week 4-6)

### 4.1 Client Connector Deployment
1. Deploy Zscaler Client Connector via MDM (Intune, Jamf, SCCM)
2. Configure auto-enrollment with IdP authentication
3. Test client connectivity to ZPA cloud
4. Validate application access through Client Connector

### 4.2 Phased Rollout
1. Phase 1: IT/Security team (50 users) - validate all segments
2. Phase 2: Engineering (200 users) - validate developer tools
3. Phase 3: Business users (remaining) - validate general applications
4. Monitor access logs for denials and policy gaps at each phase

## Phase 5: Browser Access Configuration (Week 5)

1. Enable Browser Access for applications requiring clientless access
2. Configure custom domains and TLS certificates
3. Set session timeout and clipboard/file transfer policies
4. Test with contractor accounts

## Phase 6: VPN Decommission (Week 7-8)

1. Run VPN and ZPA in parallel for 2-3 weeks
2. Monitor VPN usage to identify remaining dependencies
3. Migrate remaining applications and users
4. Disable VPN and redirect users to ZPA
5. Decommission VPN infrastructure

---

## Working Template

## Project Information
| Field | Value |
|-------|-------|
| Organization | Acme Financial Corp |
| ZPA Customer ID | 12345678 |
| ZPA Cloud | zscaler.net (US) |
| Project Lead | Security Architecture Team |
| Start Date | 2026-01-20 |

## Pre-Deployment

### Identity Provider
- [x] IdP configured: Microsoft Entra ID (SAML 2.0)
- [x] SCIM provisioning enabled for user/group sync
- [x] MFA enforced for all users
- [x] User groups mapped: Engineering, HR, Finance, Contractors

### Network Requirements
- [x] Outbound HTTPS (443) to *.private.zscaler.com allowed
- [x] Outbound HTTPS (443) to *.zpath.net allowed
- [x] DNS resolution from App Connector VMs to all internal FQDNs verified
- [ ] Split-horizon DNS configured for hybrid access

## App Connector Deployment

| Connector Name | Group | Location | VM Specs | Status |
|---------------|-------|----------|----------|--------|
| ac-dc-east-01 | DC-East | AWS us-east-1 | t3.medium | Healthy |
| ac-dc-east-02 | DC-East | AWS us-east-1 | t3.medium | Healthy |
| ac-dc-west-01 | DC-West | AWS us-west-2 | t3.medium | Healthy |
| ac-dc-west-02 | DC-West | AWS us-west-2 | t3.medium | Healthy |

## Application Segments

| Segment Name | Applications | Ports | Server Group | Bypass |
|-------------|-------------|-------|-------------|--------|
| HR Applications | hr-portal.internal.corp | 443 | DC-East | Never |
| Finance Tools | finance.internal.corp, reports.internal.corp | 443 | DC-East | Never |
| Engineering | git.internal.corp, ci.internal.corp, wiki.internal.corp | 22, 443 | DC-East + DC-West | Never |
| Monitoring | grafana.internal.corp, prometheus.internal.corp | 443, 9090 | DC-West | Never |
| Contractor Portal | vendor.internal.corp | 443 | DC-East | Never |

## Access Policies

| Rule | Action | Users/Groups | Segments | Posture | Priority |
|------|--------|-------------|----------|---------|----------|
| HR Access | ALLOW | HR-Department | HR Applications | Corporate Managed | 1 |
| Finance Access | ALLOW | Finance-Team | Finance Tools | Corporate Managed | 2 |
| Engineering Access | ALLOW | Engineering, DevOps | Engineering | Developer Workstation | 3 |
| Monitoring Access | ALLOW | SRE-Team, Engineering | Monitoring | Corporate Managed | 4 |
| Contractor Access | ALLOW | Contractors | Contractor Portal | BYOD | 5 |
| Default Deny | DENY | All Users | All Segments | N/A | 99 |

## Device Posture Profiles

| Profile | CrowdStrike ZTA | OS Version | Encryption | Firewall |
|---------|----------------|------------|------------|----------|
| Corporate Managed | >= 60 | Win 10 21H2+ / macOS 13+ | Required | Required |
| Developer Workstation | >= 70 | Win 10 21H2+ / macOS 13+ | Required | Required |
| BYOD | N/A | Latest -1 | Recommended | N/A |

## Migration Tracker

| Phase | Users | Applications | Start | Status |
|-------|-------|-------------|-------|--------|
| Phase 1: IT/Security | 50 | All | 2026-02-01 | Complete |
| Phase 2: Engineering | 200 | Engineering, Monitoring | 2026-02-10 | Complete |
| Phase 3: Business | 250 | HR, Finance, Contractor | 2026-02-20 | In Progress |
| VPN Decommission | N/A | N/A | 2026-03-15 | Pending |

## Sign-Off

| Role | Name | Date | Approved |
|------|------|------|----------|
| CISO | _________________ | __________ | [ ] |
| Network Architect | _________________ | __________ | [ ] |
| IT Operations | _________________ | __________ | [ ] |
