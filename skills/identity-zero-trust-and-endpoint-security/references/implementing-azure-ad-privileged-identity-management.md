# Implementing azure AD Privileged Identity Management

## API Reference

## Dependencies

| Library | Version | Purpose |
|---------|---------|---------|
| requests | >=2.28 | HTTP client for Microsoft Graph API |

## CLI Usage

```bash
python scripts/agent.py \
  --tenant-id YOUR_TENANT_ID \
  --client-id YOUR_CLIENT_ID \
  --client-secret YOUR_SECRET \
  --output-dir /reports/ \
  --output pim_report.json
```

## Functions

### `PIMClient(tenant_id, client_id, client_secret)`
Authenticates via OAuth2 client credentials flow to Microsoft Graph API.

### `list_role_definitions() -> list`
GET `/roleManagement/directory/roleDefinitions` - Available directory roles.

### `list_eligible_assignments() -> list`
GET `/roleManagement/directory/roleEligibilityScheduleInstances` - PIM eligible roles.

### `list_active_assignments() -> list`
GET `/roleManagement/directory/roleAssignmentScheduleInstances` - Active assignments.

### `list_role_settings() -> list`
GET `/policies/roleManagementPolicyAssignments` - PIM policy configurations.

### `audit_permanent_assignments(active, eligible) -> list`
Identifies permanent role assignments not managed via PIM eligible workflow.

### `compute_pim_coverage(active, eligible) -> dict`
Calculates percentage of assignments managed through PIM.

## Microsoft Graph Endpoints

| Endpoint | Purpose |
|----------|---------|
| `POST /oauth2/v2.0/token` | Client credentials auth |
| `GET /roleManagement/directory/roleDefinitions` | Role catalog |
| `GET /roleManagement/directory/roleEligibilityScheduleInstances` | Eligible assignments |
| `GET /roleManagement/directory/roleAssignmentScheduleInstances` | Active assignments |

## Output Schema

```json
{
  "coverage": {"active_assignments": 15, "eligible_assignments": 42, "pim_coverage_pct": 73.7},
  "permanent_assignments": [{"role": "Global Administrator", "recommendation": "Convert to eligible"}],
  "recommendations": ["Convert 5 permanent assignments to PIM-eligible"]
}
```

---

## Standards and Controls

## Microsoft Entra ID Licensing

| Feature | Required License |
|---------|-----------------|
| PIM for Entra Roles | Entra ID P2 or Entra ID Governance |
| PIM for Azure Resources | Entra ID P2 or Entra ID Governance |
| PIM for Groups | Entra ID P2 or Entra ID Governance |
| Access Reviews | Entra ID P2 or Entra ID Governance |
| Conditional Access | Entra ID P1 (minimum) |

## Critical Entra Directory Roles

| Role | Risk Level | Recommended PIM Setting |
|------|-----------|------------------------|
| Global Administrator | Critical | Eligible, approval required, max 1hr activation |
| Privileged Role Administrator | Critical | Eligible, approval required |
| Security Administrator | High | Eligible, MFA required |
| Exchange Administrator | High | Eligible, MFA required |
| SharePoint Administrator | High | Eligible, MFA required |
| User Administrator | Medium | Eligible, MFA required |
| Application Administrator | High | Eligible, MFA required |
| Cloud Application Administrator | High | Eligible, MFA required |
| Intune Administrator | Medium | Eligible, justification required |
| Compliance Administrator | Medium | Eligible, justification required |

## Compliance Framework Mapping

### NIST SP 800-53 Rev 5
- AC-2(4): Automated Audit Actions (PIM audit logs)
- AC-2(5): Inactivity Logout (time-bound activations)
- AC-6(1): Authorize Access to Security Functions
- AC-6(2): Non-Privileged Access for Non-Security Functions
- AC-6(5): Privileged Accounts (eligible vs. active)

### CIS Microsoft 365 Foundations Benchmark
- 1.1.1: Ensure MFA is enabled for all users in admin roles
- 1.1.3: Ensure that between two and four Global Admins are designated
- 1.1.6: Ensure Administrative accounts are separate and cloud-only
- 1.3.1: Ensure PIM is used to manage roles

### SOC 2 Trust Service Criteria
- CC6.1: Logical and physical access controls
- CC6.2: Prior to issuing credentials, registration and authorization
- CC6.3: Authorize, modify, or remove access timely

---

## Workflows

## PIM Deployment Workflow

```
Phase 1: DISCOVERY
    ├── Export all permanent role assignments via Microsoft Graph
    ├── Identify users with multiple admin roles
    ├── Flag accounts without MFA enabled
    └── Document break-glass account strategy

Phase 2: PLANNING
    ├── Define activation settings per role (duration, MFA, approval)
    ├── Identify approvers for each critical role
    ├── Create communication plan for affected admins
    └── Schedule pilot group for initial rollout

Phase 3: CONFIGURATION
    ├── Configure PIM role settings (activation, assignment, notification)
    ├── Convert permanent assignments to eligible (except break-glass)
    ├── Configure conditional access policies for admin activation
    └── Enable audit logging and SIEM integration

Phase 4: TESTING
    ├── Test role activation with pilot users
    ├── Test approval workflow end-to-end
    ├── Test MFA enforcement during activation
    ├── Test auto-deactivation after duration expires
    └── Validate audit logs capture all PIM events

Phase 5: ROLLOUT
    ├── Convert remaining permanent assignments to eligible
    ├── Notify all affected users with activation instructions
    ├── Monitor for activation failures and help desk tickets
    └── Configure access reviews on quarterly schedule
```

## Role Activation Workflow

```
Admin needs to perform privileged task
    │
    ├── Navigate to PIM portal (Entra Admin Center > PIM > My Roles)
    │
    ├── Click "Activate" on the needed role
    │
    ├── Select activation duration (up to configured max)
    │
    ├── Enter justification and optional ticket number
    │
    ├── Complete MFA challenge
    │
    ├── [If approval required]
    │   ├── Request submitted to approvers
    │   ├── Approvers receive email notification
    │   ├── Approver reviews justification and approves/denies
    │   └── Admin receives approval notification
    │
    ├── Role becomes active
    │
    ├── Admin performs required task
    │
    └── Role automatically deactivates when duration expires
        (or admin manually deactivates early)
```

## Access Review Workflow

```
Quarterly Access Review Triggered
    │
    ├── PIM sends review notifications to designated reviewers
    │
    ├── For each eligible assignment:
    │   ├── Reviewer checks: Is this role still needed?
    │   ├── Reviewer checks: When was role last activated?
    │   ├── Decision: Approve (maintain), Deny (remove), or Don't know
    │   └── Provide justification for decision
    │
    ├── Review period expires (14 days default)
    │
    ├── Auto-apply results:
    │   ├── Approved assignments maintained
    │   ├── Denied assignments removed
    │   └── No-response: configurable (remove or maintain)
    │
    └── Review summary report generated for compliance
```

## Break-Glass Account Workflow

```
Normal Operations:
    └── Break-glass accounts exist as ACTIVE Global Admin
        ├── Stored in secure physical safe (password printout)
        ├── Excluded from conditional access policies
        ├── Monitored by Azure Monitor alert rule
        └── Monthly verification: confirm no unauthorized sign-ins

Emergency Use:
    ├── Primary admin methods unavailable (MFA outage, PIM issue)
    ├── Retrieve break-glass credentials from safe
    ├── Sign in and resolve the emergency
    ├── Document all actions taken
    ├── Reset break-glass credentials after use
    └── Review and document in incident log
```

---

## Working Template

## Tenant Details

| Field | Value |
|-------|-------|
| Tenant ID | |
| Tenant Name | |
| License | Entra ID P2 / Entra ID Governance |
| Implementation Date | |
| Project Lead | |

## Role Configuration Matrix

| Role | Assignment Type | Max Activation | MFA Required | Approval Required | Approver |
|------|----------------|---------------|--------------|-------------------|----------|
| Global Administrator | Eligible | 1 hour | Yes | Yes | |
| Security Administrator | Eligible | 4 hours | Yes | Yes | |
| Exchange Administrator | Eligible | 8 hours | Yes | No | |
| User Administrator | Eligible | 8 hours | Yes | No | |
| Application Administrator | Eligible | 8 hours | Yes | No | |

## Break-Glass Accounts

| Account | UPN | Assignment | MFA | Storage Location |
|---------|-----|-----------|-----|-----------------|
| Break-Glass 1 | | Active Global Admin | FIDO2 key | |
| Break-Glass 2 | | Active Global Admin | FIDO2 key | |

## Migration Checklist

- [ ] All permanent role assignments inventoried
- [ ] Break-glass accounts identified and documented
- [ ] PIM role settings configured for each role
- [ ] Approval workflows configured with designated approvers
- [ ] MFA enforced for all role activations
- [ ] Permanent assignments converted to eligible (except break-glass)
- [ ] Notification settings configured (admin, security team)
- [ ] Access reviews scheduled (quarterly)
- [ ] PIM alerts enabled and monitored
- [ ] Audit logs forwarded to SIEM
- [ ] User communication sent with activation instructions
- [ ] Help desk trained on PIM troubleshooting

## Access Review Schedule

| Role | Frequency | Reviewer | Auto-Apply | Duration |
|------|-----------|----------|------------|----------|
| Global Administrator | Monthly | Security Lead | Yes - Remove | 7 days |
| Security Administrator | Quarterly | CISO | Yes - Remove | 14 days |
| All Other Admin Roles | Quarterly | Manager | Yes - Remove | 14 days |
