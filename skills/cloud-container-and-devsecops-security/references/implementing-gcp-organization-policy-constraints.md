# Implementing GCP Organization Policy Constraints

## API Reference

## gcloud CLI Commands

```bash
# List all org policies
gcloud org-policies list --organization=ORG_ID

# Describe specific constraint
gcloud org-policies describe constraints/compute.vmExternalIpAccess --organization=ORG_ID

# Set policy from YAML
gcloud resource-manager org-policies set-policy policy.yaml --organization=ORG_ID

# Set custom constraint
gcloud org-policies set-custom-constraint custom-constraint.yaml

# Check effective policy on project
gcloud org-policies list --project=PROJECT_ID
```

## Baseline Security Constraints

| Constraint | Type | Purpose |
|-----------|------|---------|
| `compute.vmExternalIpAccess` | List/Deny | Block public VM IPs |
| `compute.requireOsLogin` | Boolean | Mandate OS Login for SSH |
| `compute.disableSerialPortAccess` | Boolean | Disable serial port |
| `storage.uniformBucketLevelAccess` | Boolean | Uniform bucket ACLs |
| `sql.restrictPublicIp` | Boolean | No public Cloud SQL |
| `iam.disableServiceAccountKeyCreation` | Boolean | Force Workload Identity |
| `gcp.resourceLocations` | List/Allow | Restrict to approved regions |

## Policy YAML Formats

### Boolean Policy
```yaml
constraint: constraints/compute.requireOsLogin
booleanPolicy:
  enforced: true
```

### List Policy (Deny All)
```yaml
constraint: constraints/compute.vmExternalIpAccess
listPolicy:
  allValues: DENY
```

### List Policy (Allow Specific)
```yaml
constraint: constraints/gcp.resourceLocations
listPolicy:
  allowedValues:
    - "in:us-locations"
    - "in:eu-locations"
```

## Terraform Resource

```hcl
resource "google_organization_policy" "example" {
  org_id     = var.org_id
  constraint = "constraints/compute.requireOsLogin"
  boolean_policy { enforced = true }
}
```

### References

- GCP Org Policy: https://cloud.google.com/resource-manager/docs/organization-policy/overview
- Constraint List: https://cloud.google.com/resource-manager/docs/organization-policy/org-policy-constraints
- CIS GCP Benchmark: https://www.cisecurity.org/benchmark/google_cloud_computing_platform

---

## Standards and Controls

## CIS GCP Foundations Benchmark v3.0

| Section | Control | Constraint |
|---------|---------|-----------|
| 1.4 | Ensure user-managed service account keys are rotated within 90 days | iam.disableServiceAccountKeyCreation |
| 3.10 | Ensure VPC Flow Logs are enabled | N/A (use custom constraint) |
| 4.4 | Ensure OS Login is enabled for a project | compute.requireOsLogin |
| 4.5 | Ensure serial port access is disabled | compute.disableSerialPortAccess |
| 6.2 | Ensure Cloud SQL instances are not publicly accessible | sql.restrictPublicIp |
| 5.1 | Ensure uniform bucket-level access is enabled | storage.uniformBucketLevelAccess |

## NIST 800-53 Controls Mapping

- AC-3: Access Enforcement
- AC-6: Least Privilege
- CM-7: Least Functionality
- SC-7: Boundary Protection
- SC-12: Cryptographic Key Establishment

## Google Cloud Security Best Practices

- Principle of least privilege for organization policies
- Hierarchical policy inheritance model
- Dry-run testing before enforcement
- Separate exception management from baseline policies

---

## Workflows

## Implementation Workflow

```
1. Inventory Phase
   ├── List all existing organization policies
   ├── Identify current resource configurations
   ├── Map compliance requirements to constraints
   └── Document exceptions needed per team/project

2. Design Phase
   ├── Select constraints for baseline enforcement
   ├── Define exception policies for specific folders/projects
   ├── Plan hierarchy (Org → Folder → Project overrides)
   └── Document policy inheritance chain

3. Testing Phase
   ├── Deploy constraints in dry-run mode
   ├── Monitor violation logs for 2-4 weeks
   ├── Identify legitimate use cases requiring exceptions
   └── Refine policies based on dry-run results

4. Enforcement Phase
   ├── Convert dry-run policies to enforced mode
   ├── Apply exceptions at appropriate hierarchy level
   ├── Communicate changes to engineering teams
   └── Monitor for new violations

5. Ongoing Governance
   ├── Review policies quarterly
   ├── Audit exception requests
   ├── Update constraints for new GCP services
   └── Integrate with change management process
```

## Exception Management Workflow

```
1. Request → Developer requests exception for specific constraint
2. Review → Security team evaluates risk and business justification
3. Approve → Exception approved with scope (project/folder) and duration
4. Implement → Policy override applied at lowest necessary scope
5. Audit → Regular review of active exceptions
6. Expire → Time-bound exceptions automatically revert
```

---

## Working Template

## Organization Details

| Field | Value |
|-------|-------|
| Organization ID | |
| Organization Name | |
| Implementation Date | |
| Policy Administrator | |

## Baseline Constraints Checklist

| Constraint | Scope | Status | Exceptions |
|-----------|-------|--------|------------|
| compute.vmExternalIpAccess | Org | [ ] Enforced | |
| compute.requireOsLogin | Org | [ ] Enforced | |
| compute.disableSerialPortAccess | Org | [ ] Enforced | |
| iam.disableServiceAccountKeyCreation | Org | [ ] Enforced | |
| storage.uniformBucketLevelAccess | Org | [ ] Enforced | |
| sql.restrictPublicIp | Org | [ ] Enforced | |
| gcp.resourceLocations | Org | [ ] Enforced | |
| compute.disableNestedVirtualization | Org | [ ] Enforced | |

## Exception Requests

| Constraint | Requesting Team | Project/Folder | Justification | Approved By | Expiry |
|-----------|----------------|----------------|---------------|-------------|--------|
| | | | | | |

## Dry-Run Results

| Constraint | Violations Found | Affected Resources | Remediation Plan |
|-----------|-----------------|-------------------|-----------------|
| | | | |
