# Implementing Beyondcorp Zero Trust Access Model

## API Reference

## Dependencies

| Library | Version | Purpose |
|---------|---------|---------|
| requests | >=2.28 | HTTP client for Google Cloud IAP and Access Context Manager APIs |

## CLI Usage

```bash
python scripts/agent.py \
  --project my-gcp-project \
  --output-dir /reports/ \
  --output beyondcorp_report.json
```

## Functions

### `get_gcloud_token() -> str`
Runs `gcloud auth print-access-token` to obtain Bearer token.

### `list_iap_resources(project_id, token) -> list`
GET IAP tunnel destination groups for the project.

### `get_iap_settings(project_id, resource, token) -> dict`
GET IAP settings for a specific compute service resource.

### `list_access_levels(org_id, policy_name, token) -> list`
GET `/accessPolicies/{name}/accessLevels` from Access Context Manager.

### `audit_iap_bindings(project_id, token) -> list`
POST `getIamPolicy` and filters for IAP-related role bindings.

### `assess_zero_trust_posture(project_id, token) -> dict`
Evaluates IAP coverage, binding security, checks for allUsers exposure.

### `generate_report(project_id, token) -> dict`
Computes zero trust score (0-100) based on findings.

## Google Cloud APIs Used

| API | Endpoint |
|-----|----------|
| IAP | `iap.googleapis.com/v1/projects/{id}/iap_tunnel/...` |
| Access Context Manager | `accesscontextmanager.googleapis.com/v1/accessPolicies/...` |
| Resource Manager | `cloudresourcemanager.googleapis.com/v1/projects/{id}:getIamPolicy` |

## Output Schema

```json
{
  "project": "my-project",
  "posture": {"iap_resources": 5, "findings": []},
  "zero_trust_score": 85
}
```

---

## Standards and Controls

## NIST SP 800-207: Zero Trust Architecture
- **Section 2**: Zero Trust Tenets - defines the core principles BeyondCorp implements
- **Section 3.1**: Policy Engine (PE) and Policy Administrator (PA) - maps to IAP and Access Context Manager
- **Section 3.2**: Trust Algorithm - corresponds to Access Levels evaluation
- **Section 4.1**: Device Agent/Gateway-Based Deployment - matches BeyondCorp connector model
- **URL**: https://csrc.nist.gov/publications/detail/sp/800-207/final

## CISA Zero Trust Maturity Model v2.0 (April 2023)
- **Identity Pillar**: MFA enforcement, continuous validation - maps to IAP re-authentication
- **Device Pillar**: Device health monitoring, compliance enforcement - maps to Endpoint Verification
- **Network Pillar**: Micro-segmentation, encrypted traffic - maps to IAP tunnel encryption
- **Application Pillar**: Application access authorization - maps to per-service IAP policies
- **Data Pillar**: Data access governance, DLP - maps to Chrome Enterprise Premium DLP
- **URL**: https://www.cisa.gov/zero-trust-maturity-model

## Google BeyondCorp Papers
- **BeyondCorp: A New Approach to Enterprise Security** (2014)
  - Describes the original BeyondCorp architecture eliminating the privileged intranet
  - URL: https://research.google/pubs/pub43231/
- **BeyondCorp: Design to Deployment at Google** (2016)
  - Details the migration strategy from VPN to BeyondCorp
  - URL: https://research.google/pubs/pub44860/
- **BeyondCorp: The Access Proxy** (2017)
  - Describes the access proxy component that became IAP
  - URL: https://research.google/pubs/pub45728/
- **Migrating to BeyondCorp** (2018)
  - Covers the phased migration approach and lessons learned
  - URL: https://research.google/pubs/pub46134/

## Google Cloud IAP Documentation
- **IAP Overview**: https://cloud.google.com/iap/docs/concepts-overview
- **IAP for Compute Engine**: https://cloud.google.com/iap/docs/enabling-compute-howto
- **IAP for App Engine**: https://cloud.google.com/iap/docs/app-engine-quickstart
- **Access Context Manager**: https://cloud.google.com/access-context-manager/docs
- **Endpoint Verification**: https://cloud.google.com/endpoint-verification/docs
- **BeyondCorp Enterprise**: https://cloud.google.com/beyondcorp-enterprise/docs

## NIST SP 800-63-3: Digital Identity Guidelines
- **Section 4**: Defines identity assurance levels (IAL1-3) relevant to access level design
- **URL**: https://pages.nist.gov/800-63-3/

## DoD Zero Trust Reference Architecture v2.0
- **Section 3.4**: Identity, Credential, and Access Management pillar
- **Section 3.5**: Device pillar - endpoint compliance requirements
- **URL**: https://dodcio.defense.gov/Portals/0/Documents/Library/ZTRAv2.0.pdf

---

## Workflows

## Phase 1: Discovery and Planning (Weeks 1-2)

### 1.1 Application Inventory
1. Enumerate all internal applications accessed via VPN or corporate network
2. Classify each application by:
   - Hosting environment: GCP (App Engine, GKE, Compute Engine, Cloud Run), on-premises, SaaS
   - Protocol: HTTPS, TCP, SSH, RDP
   - Authentication method: SAML, OIDC, Kerberos, LDAP, custom
   - Sensitivity: Public, Internal, Confidential, Restricted
3. Document current access patterns: which groups access which applications
4. Identify applications that cannot be proxied (raw UDP, custom protocols)

### 1.2 Device Inventory
1. Enumerate all corporate-managed and BYOD devices
2. Document OS distribution: Windows, macOS, ChromeOS, Linux, iOS, Android
3. Verify device management coverage: Intune, Jamf, Chrome Enterprise
4. Identify gaps in device management enrollment

### 1.3 Access Level Design
1. Define trust tiers based on organizational risk appetite:
   - **Tier 1 (Basic)**: Any authenticated user from any device
   - **Tier 2 (Standard)**: Authenticated user from enrolled device with screen lock
   - **Tier 3 (Enhanced)**: Authenticated user from compliant device with disk encryption
   - **Tier 4 (High)**: Authenticated user from managed device with EDR, specific geography
2. Map applications to required trust tiers
3. Define exception process for access level overrides

## Phase 2: Infrastructure Setup (Weeks 3-4)

### 2.1 Google Cloud Configuration
1. Enable required APIs: IAP, Access Context Manager, BeyondCorp Enterprise, Cloud Audit Logs
2. Configure OAuth consent screen and IAP OAuth clients
3. Set up IAP service accounts with minimal permissions
4. Configure Cloud DNS for IAP-protected applications

### 2.2 Access Context Manager Setup
1. Create access policy at the organization level
2. Define access levels using basic conditions (device policy, IP ranges, regions)
3. Define custom access levels using CEL expressions for complex conditions
4. Test access levels with a pilot group before broad deployment

### 2.3 Endpoint Verification Deployment
1. Deploy Endpoint Verification Chrome extension via Google Admin Console policy
2. Configure extension settings: data collection scope, reporting frequency
3. Allow 1-2 weeks for device inventory population
4. Validate device attribute collection against access level requirements

## Phase 3: Application Migration (Weeks 5-10)

### 3.1 GCP-Hosted HTTPS Applications
1. Ensure applications are behind an HTTPS Load Balancer
2. Enable IAP on each backend service
3. Configure IAM bindings with access level conditions
4. Test access with pilot users before expanding
5. Monitor IAP access logs for false denials

### 3.2 On-Premises Applications
1. Deploy BeyondCorp Enterprise connectors in on-premises DMZ
2. Create app connections mapping external DNS to internal endpoints
3. Configure IAP tunnels for TCP-based applications
4. Validate network connectivity from connector to internal applications
5. Test end-to-end access through IAP connector

### 3.3 SaaS Applications
1. Configure SAML/OIDC federation from Google Workspace to SaaS apps
2. Apply conditional access policies at the IdP level
3. Enable session controls and re-authentication requirements

## Phase 4: Policy Enforcement (Weeks 11-12)

### 4.1 Gradual Enforcement
1. Start with audit-only mode: log but do not block non-compliant access
2. Review audit logs to identify users/devices that would be blocked
3. Communicate requirements and provide remediation guidance
4. Enable enforcement in stages: Tier 2 first, then Tier 3, then Tier 4

### 4.2 Re-authentication Configuration
1. Set session duration per application based on sensitivity:
   - General applications: 8-hour session
   - Sensitive applications: 4-hour session
   - Critical applications: 1-hour session
2. Configure re-authentication method: LOGIN (full re-auth) or SECURE_KEY (FIDO2 touch)

## Phase 5: VPN Decommission (Weeks 13-16)

### 5.1 Parallel Operation
1. Run VPN and BeyondCorp in parallel for 30 days
2. Monitor VPN usage to identify remaining dependencies
3. Migrate stragglers and address edge cases
4. Document break-glass procedures for BeyondCorp failure scenarios

### 5.2 VPN Retirement
1. Disable new VPN connections
2. Notify all users of VPN decommission date
3. Remove VPN client from managed devices
4. Decommission VPN infrastructure
5. Redirect VPN DNS entries to BeyondCorp access portal

## Phase 6: Continuous Monitoring (Ongoing)

### 6.1 Access Analytics
1. Build BigQuery dashboards for access pattern analysis
2. Configure alerting for anomalous access patterns:
   - Access from new geographies
   - Access outside business hours
   - Repeated authentication failures
   - Device compliance changes
3. Perform monthly access reviews of IAP bindings

### 6.2 Policy Optimization
1. Review access level effectiveness quarterly
2. Adjust device posture requirements based on threat landscape
3. Update session duration policies based on incident trends
4. Validate break-glass procedures monthly

---

## Working Template

## Project Information
| Field | Value |
|-------|-------|
| Organization | Acme Corporation |
| Project ID | acme-prod-beyondcorp |
| Lead Engineer | J. Smith, Security Architecture |
| Start Date | 2026-01-15 |
| Target Completion | 2026-04-15 |

## Pre-Migration Checklist

### Identity Provider Configuration
- [x] Google Workspace or Cloud Identity configured as primary IdP
- [x] MFA enforced for all users (FIDO2 security keys for privileged accounts)
- [x] User groups defined and synchronized (engineering, finance, contractors, executives)
- [x] Service accounts inventoried and mapped to applications
- [ ] Break-glass accounts created with documented access procedures

### Google Cloud Infrastructure
- [x] IAP API enabled on all production projects
- [x] Access Context Manager API enabled at organization level
- [x] BeyondCorp Enterprise API enabled
- [x] Cloud Audit Logs enabled for IAP data access
- [x] OAuth consent screen configured
- [ ] IAP OAuth clients created per application tier

### Endpoint Verification
- [x] Endpoint Verification extension deployed to Chrome managed browsers
- [x] Device inventory populated (2,847 devices enrolled)
- [ ] Device compliance baseline established (target: 95%)
- [ ] Non-compliant device remediation plan documented
- [ ] BYOD enrollment policy defined

## Access Level Design

| Access Level | Device Policy | Encryption | Screen Lock | Geo Restriction | Applications |
|-------------|---------------|------------|-------------|-----------------|-------------|
| basic-access | Any enrolled | Not required | Not required | None | Public wiki, cafeteria menu |
| standard-access | Enrolled + managed | Required | Required | US, GB, DE | Email, calendar, chat |
| enhanced-access | Managed + EDR | Required | Required | US, GB | Internal tools, CI/CD |
| high-trust | Managed + EDR + patched | Required | Required | US only | Finance, HR, admin panels |

## Application Migration Tracker

| Application | Hosting | Protocol | Current Access | IAP Status | Access Level | Migration Date |
|-------------|---------|----------|---------------|------------|-------------|---------------|
| Internal Wiki | App Engine | HTTPS | VPN | Enabled | basic-access | 2026-02-01 |
| CI/CD Dashboard | GKE | HTTPS | VPN | Enabled | enhanced-access | 2026-02-08 |
| HR Portal | On-prem | HTTPS | VPN | Connector deployed | high-trust | 2026-02-15 |
| Finance System | Compute Engine | HTTPS | VPN | Enabled | high-trust | 2026-02-22 |
| Git Repository | GKE | SSH+HTTPS | VPN | Enabled | enhanced-access | 2026-02-08 |
| Monitoring | Cloud Run | HTTPS | VPN | Enabled | standard-access | 2026-02-01 |
| Admin Console | On-prem | HTTPS | VPN | Connector pending | high-trust | 2026-03-01 |

## Session Policy Configuration

| Application Tier | Session Duration | Re-auth Method | Re-auth Trigger |
|-----------------|-----------------|----------------|-----------------|
| General (Tier 1) | 8 hours | LOGIN | Session expiry |
| Sensitive (Tier 2) | 4 hours | LOGIN | Session expiry, device change |
| Critical (Tier 3) | 1 hour | SECURE_KEY (FIDO2) | Session expiry, IP change |
| Admin (Tier 4) | 30 minutes | SECURE_KEY (FIDO2) | Any context change |

## Post-Migration Validation

### Functional Testing
- [ ] All migrated applications accessible through IAP without VPN
- [ ] Access denied for users not in authorized groups
- [ ] Access denied for non-compliant devices
- [ ] Re-authentication triggers working per policy
- [ ] Break-glass access procedure tested successfully
- [ ] On-premises connector failover tested

### Security Testing
- [ ] Direct application access blocked (only through IAP)
- [ ] IAP bypass attempts detected and logged
- [ ] Session hijacking mitigations verified
- [ ] Cross-tenant access properly denied
- [ ] Audit logs capturing all access decisions

### Monitoring
- [ ] BigQuery audit pipeline operational
- [ ] Alert policies configured for repeated denials
- [ ] Dashboard showing real-time access metrics
- [ ] Monthly access review process documented

## VPN Decommission Timeline

| Phase | Date | Action | Status |
|-------|------|--------|--------|
| Parallel Start | 2026-03-01 | VPN and BeyondCorp running side by side | Pending |
| VPN Monitoring | 2026-03-01 to 2026-03-15 | Track remaining VPN usage | Pending |
| VPN Block New | 2026-03-15 | Block new VPN connections | Pending |
| VPN Shutdown | 2026-04-01 | Decommission VPN infrastructure | Pending |
| Post-Mortem | 2026-04-15 | Migration lessons learned review | Pending |

## Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| CISO | _________________ | __________ | __________ |
| Security Architect | _________________ | __________ | __________ |
| IT Operations Lead | _________________ | __________ | __________ |
| Application Owner | _________________ | __________ | __________ |
