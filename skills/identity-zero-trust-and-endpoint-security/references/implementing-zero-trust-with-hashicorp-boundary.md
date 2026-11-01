# Implementing Zero Trust With Hashicorp Boundary

## API Reference

## Boundary CLI (JSON output)

### Core Commands
```bash
boundary scopes list -scope-id=global -format=json
boundary targets list -scope-id=<id> -format=json
boundary host-catalogs list -scope-id=<id> -format=json
boundary credential-stores list -scope-id=<id> -format=json
boundary sessions list -scope-id=<id> -format=json
boundary auth-methods list -scope-id=global -format=json
```

### Environment Variables
| Variable | Description |
|----------|-------------|
| `BOUNDARY_ADDR` | Controller address (e.g., `http://127.0.0.1:9200`) |
| `BOUNDARY_TOKEN` | Authentication token |

### Target Fields
| Field | Description |
|-------|-------------|
| `name` | Target display name |
| `type` | `tcp` or `ssh` |
| `session_max_seconds` | Maximum session duration |
| `session_connection_limit` | Max concurrent connections (-1 = unlimited) |

### Credential Store Types
| Type | Description |
|------|-------------|
| `vault` | Vault-brokered dynamic credentials (recommended) |
| `static` | Static credentials stored in Boundary |

### Auth Method Types
| Type | Zero Trust Suitability |
|------|----------------------|
| `oidc` | Recommended (SSO, MFA support) |
| `ldap` | Acceptable with MFA |
| `password` | Not recommended for zero trust |

### Session Recording
```bash
boundary targets update tcp -id=<id> -enable-session-recording=true \
  -storage-bucket-id=<bucket-id>
```

## References
- Boundary docs: https://developer.hashicorp.com/boundary/docs
- Boundary CLI: https://developer.hashicorp.com/boundary/docs/commands
- Boundary API: https://developer.hashicorp.com/boundary/api-docs

---

## Standards and Controls

## Core Standards

### NIST SP 800-207: Zero Trust Architecture
- Boundary implements identity-aware proxy architecture (Section 3.2.2)
- Default-deny access model aligns with ZTA core principle
- Dynamic credential brokering eliminates standing privileges
- Session-level authorization satisfies continuous verification

### NIST SP 800-53: Security Controls
- AC-2: Account Management (identity lifecycle via OIDC)
- AC-3: Access Enforcement (role-based grants)
- AC-6: Least Privilege (fine-grained permissions)
- AU-2: Audit Events (session recording and logging)
- AU-3: Content of Audit Records (session playback)
- IA-2: Identification and Authentication (OIDC/LDAP)
- SC-7: Boundary Protection (identity-aware proxy)

### SOC 2 Compliance
- CC6.1: Logical and Physical Access Controls
- CC6.2: Prior to Access, Identity is Established
- CC6.3: Role-Based Access Controls
- CC7.2: Monitoring of System Components
- CC8.1: Change Management

## Boundary Security Model

### Identity-Aware Access
- Authentication via OIDC, LDAP, or password auth methods
- Managed groups for automatic role assignment from IdP claims
- Session tokens with configurable expiry
- No direct network access to targets without Boundary session

### Credential Management
- Brokered credentials: Vault generates and returns credentials to user
- Injected credentials: Boundary injects credentials directly (user never sees them)
- SSH certificate signing: Vault CA issues short-lived SSH certificates
- Dynamic database credentials: just-in-time access with automatic revocation

### Session Controls
- Maximum session duration enforcement
- Connection limits per session
- Session recording for privileged access audit
- Automatic credential revocation on session end

## Integration Standards

### HashiCorp Vault Integration
- Transit KMS for Boundary encryption keys
- Database secrets engine for dynamic credentials
- SSH secrets engine for certificate-based access
- PKI secrets engine for TLS certificate management

### Terraform Infrastructure as Code
- Boundary Terraform provider for declarative configuration
- Version-controlled access policies
- Automated deployment and updates
- Drift detection for access control changes

---

## Workflows

## Workflow 1: Initial Boundary Deployment

```
Step 1: Infrastructure Preparation
  - Provision PostgreSQL database for Boundary backend
  - Generate TLS certificates for controller and workers
  - Configure KMS (Vault Transit or AEAD for dev)
  - Set up network connectivity between components

Step 2: Controller Deployment
  - Install Boundary binary on controller hosts
  - Configure controller with database, KMS, and listeners
  - Initialize database schema
  - Verify controller health and API accessibility

Step 3: Worker Deployment
  - Install Boundary on worker hosts in each network zone
  - Configure worker with controller address and KMS
  - Register workers with tags for routing decisions
  - Verify worker registration and health

Step 4: Identity Provider Integration
  - Configure OIDC auth method with organizational IdP
  - Map IdP groups to Boundary managed groups
  - Test authentication flow end-to-end
  - Configure token and session expiry policies
```

## Workflow 2: Target Onboarding

```
Step 1: Create Scope Hierarchy
  - Define organization scope for each business unit
  - Create project scopes for environment isolation
  - Assign admin roles to scope owners

Step 2: Configure Host Catalogs
  - Static catalogs for fixed infrastructure
  - Dynamic catalogs for cloud resources (AWS, Azure, GCP)
  - Plugin-based catalogs for auto-discovery

Step 3: Define Targets
  - Map each target to host sets
  - Configure default ports and session limits
  - Enable session recording for privileged targets
  - Link credential sources (Vault libraries)

Step 4: Create Access Policies
  - Define roles with minimum necessary grants
  - Assign roles to managed groups from IdP
  - Test access with each role
  - Document access patterns and justifications
```

## Workflow 3: Vault Credential Integration

```
Step 1: Configure Vault Secrets Engines
  - Enable database secrets engine for dynamic credentials
  - Configure SSH secrets engine for certificate signing
  - Set up PKI engine for TLS certificates
  - Define roles with appropriate TTL and permissions

Step 2: Create Boundary Credential Stores
  - Create Vault credential store in Boundary
  - Provide Vault token with appropriate policies
  - Configure namespace if using Vault Enterprise

Step 3: Create Credential Libraries
  - Map Vault paths to Boundary credential libraries
  - Configure credential type (username_password, ssh_certificate)
  - Link libraries to targets as brokered or injected sources

Step 4: Test and Validate
  - Connect to target with dynamic credentials
  - Verify credentials are revoked after session end
  - Confirm session recording captures access
  - Validate audit logs contain credential events
```

## Workflow 4: Access Review and Audit

```
Step 1: Regular Access Review
  - Export role assignments and grant strings
  - Review with resource owners quarterly
  - Remove stale or unnecessary access
  - Update managed group filters if IdP groups change

Step 2: Session Recording Review
  - Review session recordings for privileged targets
  - Investigate anomalous session patterns
  - Export recordings for compliance evidence
  - Archive recordings per retention policy

Step 3: Compliance Reporting
  - Generate access control matrix from Boundary
  - Map controls to compliance framework requirements
  - Document exceptions and compensating controls
  - Present findings to audit and compliance teams
```

---

## Working Template

## Deployment Information
- **Organization**: _______________
- **Deployment Type**: [ ] Self-hosted [ ] HCP Boundary
- **Identity Provider**: _______________
- **Vault Integration**: [ ] Yes [ ] No

## Scope Hierarchy

| Scope Type | Name | Description | Owner |
|---|---|---|---|
| Organization | ___ | ___ | ___ |
| Project | ___ | ___ | ___ |
| Project | ___ | ___ | ___ |

## Targets Inventory

| Target Name | Type | Port | Hosts | Session Max | Recording | Credentials |
|---|---|---|---|---|---|---|
| ___ | ssh | 22 | ___ | 3600s | [ ] Yes | injected |
| ___ | tcp | 5432 | ___ | 1800s | [ ] Yes | brokered |
| ___ | tcp | 443 | ___ | 3600s | [ ] Yes | none |

## Role Assignments

| Role | Scope | Grants | Groups |
|---|---|---|---|
| ___ | ___ | ___ | ___ |

## Security Checklist

- [ ] OIDC authentication configured with MFA-enabled IdP
- [ ] Managed groups auto-assign roles from IdP claims
- [ ] Vault credential brokering enabled for database targets
- [ ] SSH certificate injection via Vault SSH engine
- [ ] Session recording enabled for privileged access
- [ ] Session duration limits configured per target
- [ ] KMS configured with Vault Transit (not static AEAD)
- [ ] Workers deployed in each network zone
- [ ] Audit logging enabled on controllers and workers
- [ ] Break-glass recovery KMS configured and secured
