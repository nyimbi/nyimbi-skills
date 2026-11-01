# Deploying Tailscale For Zero Trust VPN

## API Reference

## Libraries

| Library | Install | Purpose |
|---------|---------|---------|
| requests | `pip install requests` | Tailscale API v2 client |

## Tailscale API v2 Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v2/tailnet/{tailnet}/devices` | List all devices in tailnet |
| GET | `/api/v2/tailnet/{tailnet}/acl` | Get ACL policy |
| PUT | `/api/v2/tailnet/{tailnet}/acl` | Update ACL policy |
| GET | `/api/v2/tailnet/{tailnet}/dns/nameservers` | Get DNS nameservers |
| GET | `/api/v2/tailnet/{tailnet}/keys` | List auth keys |
| GET | `/api/v2/device/{deviceid}` | Get device details |
| DELETE | `/api/v2/device/{deviceid}` | Remove device from tailnet |
| GET | `/api/v2/tailnet/{tailnet}/webhooks` | List webhooks |

## Base URL & Authentication

```
Base: https://api.tailscale.com
Header: Authorization: Bearer <api-key>
```

## ACL Policy Structure

| Field | Description |
|-------|-------------|
| `acls` | Access control rules (src, dst, action) |
| `groups` | Named groups of users |
| `tagOwners` | Tag-based device ownership |
| `ssh` | Tailscale SSH access rules |
| `autoApprovers` | Auto-approve routes and exit nodes |
| `tests` | ACL policy unit tests |

## Device Fields

| Field | Description |
|-------|-------------|
| `hostname` | Device hostname |
| `os` | Operating system |
| `clientVersion` | Tailscale client version |
| `keyExpiryDisabled` | Whether key expiry is disabled |
| `online` | Current online status |
| `lastSeen` | Last seen timestamp |
| `addresses` | Tailscale IP addresses |

## External References

- [Tailscale API Docs](https://tailscale.com/api)
- [Tailscale ACL Policy](https://tailscale.com/kb/1018/acls)
- [Tailscale SSH](https://tailscale.com/kb/1193/tailscale-ssh)

---

## Standards and Controls

## Protocol Standards

### WireGuard Protocol
- **Encryption**: ChaCha20 for symmetric encryption
- **Key Exchange**: Curve25519 for Diffie-Hellman
- **MAC**: Poly1305 for message authentication
- **Hashing**: BLAKE2s for hashing
- **Framework**: Noise Protocol Framework for key negotiation

### NIST SP 800-207: Zero Trust Architecture
- Tailscale implements identity-aware proxying (Section 3.2.2)
- End-to-end encryption satisfies data-in-transit requirements
- ACL-based access control implements least privilege access
- Device identity via WireGuard keys maps to device trust

### NIST SP 800-77: Guide to IPsec VPNs
- WireGuard provides alternative to IPsec with reduced complexity
- Tailscale automates key distribution and NAT traversal
- Mesh topology eliminates single point of failure

## Tailscale Security Model

### Identity Layer
- Authentication via OIDC-compatible identity providers
- SSO integration with Okta, Azure AD, Google Workspace, GitHub
- MFA enforcement through identity provider policies
- Key expiry forces periodic re-authentication

### Network Layer
- Default deny ACL policy (zero trust)
- Per-connection authorization based on identity and tags
- No implicit trust based on network location
- All traffic encrypted with WireGuard (256-bit keys)

### Device Layer
- Unique WireGuard key pair per device
- Device authorization required before network access
- Network Lock prevents unauthorized node addition
- Ephemeral nodes for temporary workloads

## Compliance Considerations

### SOC 2
- End-to-end encryption for data in transit
- ACL-based access control for authorization
- Audit logging for all connection events
- Key management through coordination server

### GDPR
- Data minimization: Tailscale only routes traffic, does not inspect
- Encryption: All traffic encrypted end-to-end
- Self-hosted option (Headscale) for data sovereignty
- Log retention configurable per organization policy

---

## Workflows

## Workflow 1: Initial Tailnet Deployment

```
Step 1: Plan Network Architecture
  - Identify all devices and services requiring connectivity
  - Map existing network topology and access requirements
  - Define user groups and access policies
  - Plan subnet routing for legacy network integration
  - Determine exit node placement for internet routing

Step 2: Configure Identity Provider
  - Enable SSO with organizational identity provider
  - Configure MFA enforcement policies
  - Map identity provider groups to Tailscale groups
  - Set key expiry policy (recommended: 90 days)

Step 3: Deploy Tailscale Nodes
  - Install on critical infrastructure first (servers, databases)
  - Deploy to user endpoints (laptops, mobile devices)
  - Configure subnet routers for non-Tailscale networks
  - Set up exit nodes for secure internet access
  - Enable MagicDNS for hostname resolution

Step 4: Configure ACLs
  - Start with deny-all baseline
  - Define groups matching organizational structure
  - Create tag-based policies for infrastructure
  - Test ACLs in audit mode before enforcement
  - Document all ACL rules and their business justification

Step 5: Validate and Monitor
  - Test connectivity between all required paths
  - Verify ACL enforcement blocks unauthorized access
  - Enable audit logging
  - Configure alerts for connection anomalies
```

## Workflow 2: ACL Policy Development

```
Step 1: Inventory Access Requirements
  - List all user roles and their resource needs
  - Map application dependencies (service-to-service)
  - Identify privileged access paths
  - Document temporary/exception access needs

Step 2: Design Policy Structure
  - Define groups (users, teams, roles)
  - Define tags (environments, service types, sensitivity)
  - Map access rules: group/tag -> destination:ports
  - Plan SSH access policies with session recording

Step 3: Implement and Test
  - Write ACL JSON configuration
  - Deploy in test/staging tailnet first
  - Validate each rule with test connections
  - Verify deny rules block unauthorized access
  - Review with security team before production deployment

Step 4: Maintain and Audit
  - Review ACLs quarterly for stale rules
  - Audit access logs for policy violations
  - Update groups when team membership changes
  - Remove deprecated rules and tags
```

## Workflow 3: Headscale Self-Hosted Deployment

```
Step 1: Prepare Infrastructure
  - Provision server with public IP and domain
  - Configure TLS certificate (Let's Encrypt)
  - Set up PostgreSQL or SQLite database
  - Configure firewall rules (port 443, DERP relay ports)

Step 2: Install and Configure Headscale
  - Download latest Headscale binary
  - Generate configuration file
  - Configure OIDC provider integration
  - Set up DNS records for coordination server
  - Configure DERP relay servers

Step 3: Onboard Users and Devices
  - Create users/namespaces in Headscale
  - Generate pre-auth keys for automated deployment
  - Connect client devices to Headscale server
  - Configure ACLs via Headscale policy file

Step 4: Operational Maintenance
  - Monitor Headscale server health
  - Rotate pre-auth keys regularly
  - Backup database and configuration
  - Update Headscale and client versions
  - Review and rotate DERP relay configuration
```

---

## Working Template

## Network Architecture

- **Organization**: _______________
- **Tailnet Name**: _______________
- **Identity Provider**: _______________
- **Key Expiry Policy**: _______________
- **Self-hosted (Headscale)**: [ ] Yes [ ] No

## User Groups

| Group Name | Description | Members Count | Access Level |
|---|---|---|---|
| group:engineering | Development team | ___ | Development, Staging |
| group:sre | SRE/DevOps team | ___ | All environments |
| group:security | Security team | ___ | Monitoring, Audit |
| group:management | Leadership | ___ | Dashboards only |

## Infrastructure Tags

| Tag | Description | Owner Group | Environment |
|---|---|---|---|
| tag:production | Production servers | group:sre | Production |
| tag:staging | Staging servers | group:engineering | Staging |
| tag:development | Dev servers | group:engineering | Development |
| tag:database | Database servers | group:sre | All |
| tag:monitoring | Monitoring stack | group:sre | All |

## Subnet Routes

| CIDR | Description | Router Node | Auto-Approved |
|---|---|---|---|
| 10.0.0.0/16 | Corporate network | ___ | [ ] Yes |
| 192.168.0.0/24 | Lab network | ___ | [ ] Yes |

## Exit Nodes

| Hostname | Location | Purpose | Auto-Approved |
|---|---|---|---|
| ___ | ___ | Internet routing | [ ] Yes |
| ___ | ___ | Geo-specific access | [ ] Yes |

## Security Checklist

- [ ] Identity provider configured with MFA
- [ ] Key expiry enabled (recommended: 90 days)
- [ ] ACLs configured with deny-all default
- [ ] Network Lock enabled
- [ ] SSH access requires re-authentication for privileged users
- [ ] Audit logging enabled
- [ ] Subnet routes approved only for authorized nodes
- [ ] Exit nodes approved only for authorized nodes
- [ ] Untagged node policy defined
- [ ] Ephemeral keys used for CI/CD and temporary workloads

## Rollout Plan

### Phase 1: Infrastructure
- [ ] Deploy to servers and critical infrastructure
- [ ] Configure subnet routers
- [ ] Set up exit nodes
- [ ] Test ACL enforcement

### Phase 2: User Onboarding
- [ ] Pilot group deployment
- [ ] Full organization rollout
- [ ] VPN migration (decommission legacy VPN)
- [ ] User training and documentation

### Phase 3: Hardening
- [ ] Enable Network Lock
- [ ] Enable Tailscale SSH with session recording
- [ ] Configure auto-approvers
- [ ] Set up monitoring and alerting
