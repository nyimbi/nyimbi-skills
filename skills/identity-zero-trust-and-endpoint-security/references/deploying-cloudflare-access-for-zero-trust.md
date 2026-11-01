# Deploying Cloudflare Access For Zero Trust

## API Reference

## Libraries

| Library | Install | Purpose |
|---------|---------|---------|
| requests | `pip install requests` | Cloudflare API v4 client |

## Cloudflare Access API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/accounts/{id}/access/apps` | List Access applications |
| GET | `/accounts/{id}/access/apps/{id}/policies` | List app policies |
| GET | `/accounts/{id}/access/groups` | List Access groups |
| GET | `/accounts/{id}/access/identity_providers` | List IdP configs |
| GET | `/accounts/{id}/access/service_tokens` | List service tokens |
| POST | `/accounts/{id}/access/apps` | Create application |
| PUT | `/accounts/{id}/access/apps/{id}` | Update application |

## Authentication

```python
headers = {
    "Authorization": "Bearer <api_token>",
    "Content-Type": "application/json"
}
```

## Access Policy Rule Types

| Rule | Description |
|------|-------------|
| `include` | Must match (OR within group) |
| `exclude` | Must not match |
| `require` | Must match (AND) |

## External References

- [Cloudflare Access API](https://developers.cloudflare.com/api/operations/access-applications-list-access-applications)
- [Cloudflare Zero Trust Docs](https://developers.cloudflare.com/cloudflare-one/)
- [cloudflare Python SDK](https://github.com/cloudflare/cloudflare-python)

---

## Standards and Controls

## NIST SP 800-207: Zero Trust Architecture
- **Section 2**: ZTA Tenets - Cloudflare Access implements per-request identity verification
- **Section 3.2**: Enhanced Identity Governance - Access policies enforce continuous authorization
- **Section 4.2**: Cloud-Based SDP - Cloudflare Tunnel maps to software-defined perimeter architecture
- **URL**: https://csrc.nist.gov/publications/detail/sp/800-207/final

## CISA Zero Trust Maturity Model v2.0
- **Identity**: SSO with MFA via integrated IdP support
- **Device**: WARP client posture checks for OS, encryption, EDR
- **Network**: Cloudflare Tunnel eliminates inbound firewall rules
- **Application**: Per-application Access policies with session controls
- **URL**: https://www.cisa.gov/zero-trust-maturity-model

## Cloudflare Documentation
- **Cloudflare One Overview**: https://developers.cloudflare.com/cloudflare-one/
- **Cloudflare Access**: https://developers.cloudflare.com/cloudflare-one/policies/access/
- **Cloudflare Tunnel**: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/
- **WARP Deployment**: https://developers.cloudflare.com/cloudflare-one/connections/connect-devices/warp/
- **Device Posture**: https://developers.cloudflare.com/cloudflare-one/identity/devices/
- **Logpush**: https://developers.cloudflare.com/logs/about/
- **Zero Trust Reference Architecture**: https://developers.cloudflare.com/reference-architecture/implementation-guides/zero-trust/

## SOC 2 Type II
- Cloudflare maintains SOC 2 Type II certification
- Access audit logs provide evidence for CC6.1 (Logical Access), CC6.3 (Role-Based Access)
- **URL**: https://www.cloudflare.com/trust-hub/compliance-resources/

## GDPR
- Cloudflare processes data per EU GDPR requirements
- Data localization options for EU-based traffic
- **URL**: https://www.cloudflare.com/trust-hub/gdpr/

---

## Workflows

## Phase 1: Account Setup (Day 1)

1. Create Cloudflare account and navigate to Zero Trust dashboard
2. Select team name (organization identifier for WARP enrollment)
3. Choose subscription plan based on user count
4. Configure authentication: add primary IdP (Okta, Entra ID, Google Workspace)
5. Add secondary IdP for contractors or partners if needed
6. Enable MFA requirements at the IdP level

## Phase 2: Tunnel Deployment (Day 2-3)

### 2.1 Install cloudflared
1. Install `cloudflared` on a server within the private network
2. Authenticate with `cloudflared tunnel login`
3. Create named tunnel: `cloudflared tunnel create <name>`
4. Configure ingress rules in `config.yml` mapping hostnames to internal services
5. Route DNS: `cloudflared tunnel route dns <tunnel> <hostname>`

### 2.2 High Availability
1. Deploy multiple `cloudflared` instances for redundancy
2. Use `cloudflared tunnel run --protocol quic` for better performance
3. Configure systemd service for automatic restart
4. Monitor tunnel health via Cloudflare dashboard

### 2.3 Private Network Routing
1. Add private network routes: `cloudflared tunnel route ip add 10.0.0.0/8 <tunnel-id>`
2. Configure split tunnel in WARP device settings
3. Set up DNS fallback domains for private DNS resolution

## Phase 3: Access Application Configuration (Day 4-5)

1. Create Access applications for each internal service
2. Define access policies per application:
   - Include rules: email domains, IdP groups, service tokens
   - Require rules: device posture, country restrictions
   - Exclude rules: specific users or IPs
3. Configure session duration per application sensitivity
4. Enable purpose justification for sensitive applications
5. Test access with pilot users

## Phase 4: WARP Client Deployment (Week 2)

1. Create device enrollment policies with email domain restrictions
2. Deploy WARP client via MDM (Intune, Jamf, SCCM)
3. Install Cloudflare root certificate for TLS inspection
4. Configure split tunnel settings for private network access
5. Enable device posture checks: OS version, disk encryption, firewall

## Phase 5: Gateway and DLP Configuration (Week 3)

1. Enable DNS filtering with block categories (malware, phishing)
2. Configure HTTP inspection policies
3. Set up DLP profiles for sensitive data detection
4. Enable browser isolation for high-risk web categories
5. Configure CASB for SaaS application monitoring

## Phase 6: Monitoring and Optimization (Ongoing)

1. Enable Logpush to SIEM (S3, Splunk, Datadog)
2. Monitor Access audit logs for denied requests
3. Review tunnel health metrics
4. Optimize split tunnel configuration
5. Conduct quarterly access policy reviews

---

## Working Template

## Project Information
| Field | Value |
|-------|-------|
| Organization | TechStartup Inc |
| Cloudflare Account | CF-XXXXXXX |
| Team Name | techstartup |
| Plan | Zero Trust Teams (50 seats) |
| Start Date | 2026-01-25 |

## Identity Provider Configuration
- [x] Primary IdP: Google Workspace (OIDC)
- [x] MFA enforced at IdP level
- [ ] Secondary IdP for contractors: GitHub OAuth
- [x] Email domain restriction: @techstartup.com

## Tunnel Deployment

| Tunnel Name | Server | Network | Routes | Status |
|-------------|--------|---------|--------|--------|
| prod-tunnel | prod-bastion (10.1.0.5) | Production VPC | wiki, grafana, api | Healthy |
| staging-tunnel | staging-bastion (10.2.0.5) | Staging VPC | staging-* | Healthy |

## Access Applications

| Application | Type | Domain | Session | Policies | Status |
|-------------|------|--------|---------|----------|--------|
| Internal Wiki | self_hosted | wiki.techstartup.com | 8h | 2 (Allow Eng, Deny All) | Active |
| Grafana | self_hosted | grafana.techstartup.com | 8h | 2 (Allow SRE, Deny All) | Active |
| Internal API | self_hosted | api.techstartup.com | 4h | 3 (Allow Backend, Service Token, Deny All) | Active |
| Staging Apps | self_hosted | staging.techstartup.com | 4h | 2 (Allow Eng, Deny All) | Active |
| SSH Jump | ssh | ssh.techstartup.com | 2h | 1 (Allow SRE) | Active |

## Device Posture Rules
- [x] Disk encryption: Required (Windows BitLocker, macOS FileVault)
- [x] OS version: Windows >= 10.0.19045, macOS >= 14.0
- [x] Firewall: Enabled
- [ ] CrowdStrike integration: Pending deployment

## WARP Enrollment

| Platform | Enrolled | Total | Coverage |
|----------|----------|-------|----------|
| macOS | 32 | 35 | 91.4% |
| Windows | 12 | 13 | 92.3% |
| Linux | 2 | 2 | 100% |
| Total | 46 | 50 | 92.0% |

## Sign-Off

| Role | Name | Date | Approved |
|------|------|------|----------|
| CTO | _________________ | __________ | [ ] |
| Security Lead | _________________ | __________ | [ ] |
