# Implementing AWS IAM Permission Boundaries

## API Reference

## Dependencies

| Library | Version | Purpose |
|---------|---------|---------|
| boto3 | >=1.28 | AWS SDK for IAM permission boundary management |

## CLI Usage

```bash
python scripts/agent.py \
  --profile security-admin \
  --region us-east-1 \
  --audit \
  --output-dir /reports/ \
  --output iam_boundary_report.json
```

## Functions

### `get_iam_client(profile, region)`
Creates boto3 IAM client with optional named profile.

### `create_permission_boundary(client, policy_name, allowed_services, allowed_regions) -> dict`
Creates an IAM policy for use as a permission boundary. Includes a DenyBoundaryChanges statement to prevent boundary removal. Uses `client.create_policy()`.

### `attach_boundary_to_role(client, role_name, boundary_arn) -> dict`
Calls `client.put_role_permissions_boundary()` to attach a boundary to a role.

### `audit_roles_without_boundary(client) -> list`
Paginates `client.list_roles()` and identifies roles missing `PermissionsBoundary`.

### `audit_boundary_effectiveness(client, role_name) -> dict`
Calls `client.get_role()`, `list_attached_role_policies()`, `list_role_policies()` to show effective policy stack.

### `generate_report(client) -> dict`
Orchestrates audit and generates compliance report.

## boto3 IAM Methods Used

| Method | Purpose |
|--------|---------|
| `create_policy(PolicyName, PolicyDocument)` | Create boundary policy |
| `put_role_permissions_boundary(RoleName, PermissionsBoundary)` | Attach boundary |
| `list_roles()` | Enumerate all roles |
| `get_role(RoleName)` | Get role details including boundary |

## Output Schema

```json
{
  "roles_without_boundary_count": 12,
  "roles_without_boundary": [{"role_name": "dev-role", "arn": "arn:aws:iam::..."}],
  "recommendations": ["Attach permission boundaries to 12 roles"]
}
```

---

## Standards and Controls

## AWS IAM Policy Types

| Policy Type | Scope | Purpose |
|-------------|-------|---------|
| Identity-Based | Attached to users/roles/groups | Grants permissions |
| Resource-Based | Attached to resources (S3, KMS) | Cross-account access |
| Permission Boundary | Attached to users/roles | Maximum permission limit |
| Organizations SCP | Attached to OUs/accounts | Organization-wide limit |
| Session Policy | Passed during AssumeRole | Session-level limit |

## AWS Well-Architected Framework - Security Pillar

### SEC02 - Identity Management
- SEC02-BP02: Use temporary credentials (permission boundaries enforce this)
- SEC02-BP05: Audit and rotate credentials regularly
- SEC02-BP06: Employ user groups and attributes for fine-grained access

### SEC03 - Permissions Management
- SEC03-BP01: Define access requirements (boundary defines maximum)
- SEC03-BP02: Grant least privilege access
- SEC03-BP06: Manage access based on lifecycle
- SEC03-BP07: Analyze public and cross-account access

## CIS AWS Foundations Benchmark v3.0

- 1.4: Ensure no root account access key exists
- 1.15: Ensure IAM users receive permissions only through groups
- 1.16: Ensure IAM policies that allow full admin privileges are not attached
- 1.17: Ensure a support role has been created for incident management
- 1.22: Ensure IAM policies with admin access are reviewed regularly

## NIST SP 800-53 Mapping

- AC-2: Account Management (boundary controls role creation)
- AC-3: Access Enforcement (intersection of policies)
- AC-5: Separation of Duties (boundary prevents security role access)
- AC-6: Least Privilege (boundary enforces maximum permissions)
- AC-6(1): Authorize Access to Security Functions
- AC-6(5): Privileged Accounts (boundary limits even admin roles)

---

## Workflows

## Boundary Policy Creation Workflow

```
1. Security team identifies allowed services for developer workloads
       │
2. Draft permission boundary policy (JSON)
       │
3. Peer review by second security engineer
       │
4. Test in sandbox account:
       ├── Create test role with boundary
       ├── Verify allowed actions succeed
       ├── Verify blocked actions are denied
       └── Verify boundary cannot be self-modified
       │
5. Commit policy to version control (IaC repository)
       │
6. Deploy via CI/CD pipeline (Terraform/CloudFormation)
       │
7. Attach boundary to all developer-created roles
```

## Developer Role Creation Workflow (with Boundary)

```
Developer wants to create a new IAM role
       │
├── Developer writes role policy (only app-* prefixed)
│
├── Developer creates role with --permissions-boundary flag
│       │
│       └── If boundary not attached → API returns AccessDenied
│
├── AWS IAM validates:
│   ├── Role name matches required prefix (app-*)
│   ├── Permission boundary ARN matches required boundary
│   └── Developer has iam:CreateRole with boundary condition
│
├── Role created successfully with boundary attached
│
└── Effective permissions = identity policy ∩ boundary policy
```

## Privilege Escalation Prevention Workflow

```
Attacker attempts to escalate privileges:

Attempt 1: Create role without boundary
    → Denied by developer policy (condition requires boundary)

Attempt 2: Modify the boundary policy itself
    → Denied by boundary's own deny statements

Attempt 3: Remove boundary from existing role
    → Denied by boundary deny on DeleteRolePermissionsBoundary

Attempt 4: Create policy granting iam:* access
    → Policy can only grant actions within boundary intersection

Attempt 5: Assume a role without boundary
    → Developer can only create roles with boundary condition

All escalation paths blocked ✓
```

## Boundary Audit Workflow

```
Monthly audit:
    │
    ├── List all IAM roles in account
    │
    ├── Check each role for boundary attachment:
    │   ├── Has boundary → Verify correct boundary ARN
    │   └── No boundary → Flag for remediation
    │
    ├── Review boundary policy changes (CloudTrail)
    │
    ├── Check for new IAM actions added to AWS services
    │   └── Update boundary if new actions should be restricted
    │
    └── Generate compliance report
```

---

## Working Template

## Boundary Policy Details

| Field | Value |
|-------|-------|
| Policy Name | |
| AWS Account ID | |
| Target Roles | (prefix pattern, e.g., app-*) |
| Allowed Services | |
| Created By | |
| Date | |

## Allowed Service Actions

| Service | Actions Allowed | Justification |
|---------|----------------|---------------|
| S3 | s3:* | Application data storage |
| DynamoDB | dynamodb:* | Application database |
| Lambda | lambda:* | Serverless compute |
| CloudWatch | cloudwatch:*, logs:* | Monitoring and logging |
| | | |

## Denied Actions (Escalation Prevention)

| Action | Reason |
|--------|--------|
| iam:DeleteRolePermissionsBoundary | Prevent boundary removal |
| iam:DeleteUserPermissionsBoundary | Prevent boundary removal |
| iam:CreatePolicyVersion (on boundary) | Prevent boundary modification |
| iam:SetDefaultPolicyVersion (on boundary) | Prevent boundary modification |

## Testing Results

| Test Case | Expected Result | Actual Result | Pass/Fail |
|-----------|----------------|---------------|-----------|
| Create role with boundary | Success | | |
| Create role without boundary | AccessDenied | | |
| Use allowed service (e.g., S3) | Success | | |
| Use blocked service (e.g., IAM admin) | AccessDenied | | |
| Remove own boundary | AccessDenied | | |
| Modify boundary policy | AccessDenied | | |

## Sign-Off

| Role | Name | Date |
|------|------|------|
| Security Engineer | | |
| Cloud Architect | | |
| DevOps Lead | | |
