# Implementing Zero Standing Privilege With Cyberark

## API Reference

## CyberArk PVWA REST API v2

### Authentication
```python
POST /api/auth/CyberArk/Logon
Body: {"username": "admin", "password": "pass"}
Returns: Session token string
```

### Key Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/Safes` | List all safes |
| GET | `/api/Safes/{name}/Members` | List safe members and permissions |
| GET | `/api/Platforms` | List configured platforms |
| GET | `/api/Accounts` | List privileged accounts |
| GET | `/api/LiveSessions` | List active privileged sessions |
| POST | `/api/Accounts/{id}/CheckIn` | Release exclusive account access |

### Safe Member Permissions
| Permission | ZSP Implication |
|------------|----------------|
| `useAccounts` | Can initiate privileged sessions |
| `retrieveAccounts` | Can retrieve passwords |
| `listAccounts` | Can see account inventory |
| `requestsAuthorizationLevel1` | Dual-control approval required |

### Session Properties
| Field | Description |
|-------|-------------|
| `User` | Session initiator |
| `AccountName` | Target privileged account |
| `Duration` | Session length in seconds |
| `RemoteMachine` | Target host |

## TEA Framework
| Component | API Field | Purpose |
|-----------|-----------|---------|
| Time | `MaxSessionDuration` | Auto-revoke after timeout |
| Entitlements | `AllowedPermissions` | Scoped access per session |
| Approvals | `requestsAuthorizationLevel` | Require approval workflow |

## References
- CyberArk REST API: https://docs.cyberark.com/pam-self-hosted/latest/en/Content/SDK/CyberArk%20REST%20API.htm
- CyberArk Secure Cloud Access: https://docs.cyberark.com/secure-cloud-access/

---

## Standards and Controls

## Zero Trust Frameworks

### NIST SP 800-207 - Zero Trust Architecture
- Never trust, always verify
- Least privilege access to resources
- Microsegmentation and policy enforcement points
- Dynamic, risk-based access policies

### CISA Zero Trust Maturity Model
- Identity pillar: JIT/JEA access for all identities
- Advanced maturity: Automated privilege provisioning/deprovisioning
- Optimal maturity: Continuous verification with ephemeral access

## TEA Framework Components

### Time
- Session duration: minimum required for task completion
- CyberArk default: 1 hour, configurable 15 min to 8 hours
- Business hours enforcement optional
- Auto-termination on session inactivity

### Entitlements
- Principle of least privilege
- Dynamic role creation scoped to specific resources
- Permission boundaries to prevent escalation
- Entitlement analytics for right-sizing

### Approvals
- Risk-based approval routing
- Multi-level approval for critical access
- Auto-approval for previously approved, low-risk requests
- ITSM integration (ServiceNow, Jira) for audit trail

## Compliance Requirements

### SOC 2 - CC6
- CC6.1: Logical access security restricted
- CC6.3: Access authorized, modified, removed timely
- ZSP provides evidence of no standing privileges

### PCI DSS v4.0
- 7.2.1: Access limited to least privilege
- 7.2.4: Access reviewed at least every 6 months
- ZSP eliminates the review burden by removing standing access

### SOX Section 404
- Separation of duties enforcement
- Access to financial systems must be controlled
- JIT access provides clear audit trail of who accessed what, when

---

## Workflows

## JIT Access Request Workflow

```
Developer needs to access AWS production environment
    │
    ├── Opens CyberArk Secure Cloud Access portal
    │
    ├── Selects target: AWS Account "Production" (123456789012)
    │
    ├── Selects policy: "Developer Production Read Access"
    │
    ├── Specifies duration: 2 hours
    │
    ├── Provides justification: "Investigating PROD-1234 latency issue"
    │
    ├── Submits request
    │
    ├── CyberArk evaluates TEA policy:
    │   ├── Time: 2 hours within allowed range
    │   ├── Entitlements: Read-only production access
    │   └── Approval: Manager approval required
    │
    ├── Approval request sent to manager (Slack/email)
    │
    ├── Manager approves
    │
    ├── CyberArk provisions ephemeral IAM role:
    │   ├── Creates role with ReadOnlyAccess + resource restrictions
    │   ├── Sets session duration to 2 hours
    │   └── Generates temporary STS credentials
    │
    ├── Developer accesses AWS console/CLI with temp credentials
    │   └── All actions recorded in session log
    │
    └── After 2 hours: role deleted, credentials revoked
```

## Standing Privilege Migration Workflow

```
Phase 1: DISCOVERY AND ANALYSIS
    ├── Export all IAM users/roles with standing admin access
    ├── Analyze CloudTrail logs for actual permission usage
    ├── Identify which permissions are actually used vs. assigned
    ├── Calculate right-sized policy for each use case
    └── Map standing privileges to CyberArk ZSP policies

Phase 2: POLICY CREATION
    ├── Create CyberArk SCA policies for each access pattern
    ├── Define TEA parameters:
    │   ├── Maximum session duration per policy
    │   ├── Entitlement scope (AWS managed policies + custom)
    │   └── Approval requirements (auto vs. manual)
    ├── Configure approval workflows
    └── Test policies with pilot group

Phase 3: PILOT MIGRATION (2-4 weeks)
    ├── Assign ZSP policies to pilot users
    ├── Remove standing privileges from pilot users
    ├── Monitor for access denied errors
    ├── Adjust policies based on feedback
    └── Measure: request volume, approval time, session duration

Phase 4: FULL MIGRATION (4-8 weeks)
    ├── Migrate teams in waves (1 team per week)
    ├── Remove standing privileges after ZSP confirmed working
    ├── Configure auto-detect for new standing privilege creation
    └── Report metrics to security leadership

Phase 5: CONTINUOUS GOVERNANCE
    ├── Weekly: Review and right-size ZSP policies
    ├── Monthly: Audit for any standing privilege re-creation
    ├── Quarterly: Entitlement optimization report
    └── Alert on: New standing admin roles created outside CyberArk
```

## Emergency Break-Glass Workflow

```
CyberArk SCA unavailable or network issue
    │
    ├── Retrieve break-glass credentials from:
    │   ├── Physical safe (sealed envelope)
    │   ├── Or secondary vault (Azure Key Vault / AWS Secrets Manager)
    │
    ├── Authenticate with break-glass credentials
    │
    ├── Perform emergency actions
    │
    ├── Document all actions taken
    │
    └── Post-incident:
        ├── Rotate break-glass credentials
        ├── Review session logs for the emergency access
        ├── File incident report
        └── Verify no unauthorized changes made
```

---

## Working Template

## Project Overview

| Field | Value |
|-------|-------|
| Organization | |
| CyberArk Platform Version | |
| Target Clouds | AWS / Azure / GCP |
| Project Lead | |
| Start Date | |

## Standing Privilege Inventory

| Identity | Cloud | Type | Admin Policy | Last Used | Migration Wave |
|----------|-------|------|-------------|-----------|----------------|
| | AWS/Azure/GCP | User/Role | | | |

## ZSP Policy Definitions

| Policy Name | Target Cloud | Entitlements | Max Duration | Approval | Certifier |
|-------------|-------------|-------------|-------------|----------|-----------|
| | | | | Auto/Manual | |

## Migration Progress

| Wave | Team | Identities | Migrated | Standing Removed | Status |
|------|------|-----------|----------|-----------------|--------|
| 1 | | | Yes/No | Yes/No | |

## Validation

- [ ] All standing privileges discovered and documented
- [ ] ZSP policies created for each access pattern
- [ ] Approval workflows tested end-to-end
- [ ] Pilot migration successful
- [ ] All standing privileges removed after migration
- [ ] Break-glass procedure documented and tested
- [ ] Session monitoring and recording enabled
- [ ] SIEM integration receiving ZSP access logs
