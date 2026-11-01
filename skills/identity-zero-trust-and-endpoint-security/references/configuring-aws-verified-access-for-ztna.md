# Configuring AWS Verified Access For Ztna

## API Reference

## Libraries

| Library | Install | Purpose |
|---------|---------|---------|
| boto3 | `pip install boto3` | AWS SDK — EC2 Verified Access API |

## Key boto3 EC2 Methods

| Method | Description |
|--------|-------------|
| `describe_verified_access_instances()` | List VA instances |
| `describe_verified_access_groups()` | List VA groups with policies |
| `describe_verified_access_endpoints()` | List VA application endpoints |
| `describe_verified_access_trust_providers()` | List identity/device trust providers |
| `create_verified_access_instance()` | Create new VA instance |
| `create_verified_access_group(VerifiedAccessInstanceId=)` | Create group under instance |
| `create_verified_access_endpoint()` | Expose application via VA |
| `modify_verified_access_group_policy()` | Update Cedar policy document |

## Cedar Policy Language

```cedar
permit(principal, action, resource)
when {
    context.identity.groups has "engineering" &&
    context.identity.email.address like "*@company.com" &&
    context.device.status == "compliant"
};
```

## Trust Provider Types

| Type | Description |
|------|-------------|
| user / iam-identity-center | AWS IAM Identity Center OIDC |
| user / oidc | Third-party OIDC provider |
| device / jamf | Jamf device trust |
| device / crowdstrike | CrowdStrike device posture |

## External References

- [AWS Verified Access Docs](https://docs.aws.amazon.com/verified-access/)
- [Cedar Policy Language](https://www.cedarpolicy.com/en)
- [boto3 EC2 Verified Access](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_verified_access_instances.html)

---

## Standards and Controls

## AWS Verified Access Standards

### Cedar Policy Language
- Developed by AWS for fine-grained access control
- Supports permit and forbid policies with conditions
- Evaluates context attributes (identity, device posture, request metadata)
- Open-source specification at cedarpolicy.com

### AWS Well-Architected Framework - Security Pillar
- SEC03-BP01: Define access requirements
- SEC03-BP02: Grant least privilege access
- SEC03-BP05: Define permission guardrails for organization
- SEC05-BP03: Automate network protection

## Zero Trust Standards

### NIST SP 800-207
- Verified Access implements enhanced identity governance (Section 3.1)
- Per-request policy evaluation aligns with continuous verification
- Device posture assessment satisfies device trust requirements
- Integration with identity providers meets identity pillar requirements

### CISA Zero Trust Maturity Model
- Identity Pillar: OIDC integration with MFA-enabled providers
- Device Pillar: CrowdStrike/Jamf device posture assessment
- Network Pillar: VPN-less access eliminates implicit network trust
- Application Pillar: Per-application access policies

## Compliance Mappings

### SOC 2
- CC6.1: Logical access security through Cedar policies
- CC6.2: Identity verification via trust providers
- CC6.3: Role-based access through group policies
- CC7.2: System monitoring through access logging

### FedRAMP
- AC-2: Account Management via identity provider integration
- AC-3: Access Enforcement through Cedar policies
- AC-6: Least Privilege via per-application policies
- AU-2: Auditable Events through CloudWatch logging
- SC-7: Boundary Protection via Verified Access endpoints

---

## Workflows

## Workflow 1: Initial Setup

```
Step 1: Create Verified Access Instance
  - Deploy instance in target AWS region
  - Tag with environment and ownership information

Step 2: Configure Trust Providers
  - Set up identity trust provider (IAM Identity Center or OIDC)
  - Set up device trust provider (CrowdStrike, Jamf, JumpCloud)
  - Attach both providers to the Verified Access instance

Step 3: Create Access Groups
  - Define groups based on application tiers or teams
  - Write group-level Cedar policies
  - Set baseline identity and device requirements

Step 4: Create Endpoints
  - Map each application to a Verified Access endpoint
  - Configure ALB or ENI attachment
  - Set application domain and certificate
  - Write endpoint-specific Cedar policies

Step 5: Configure DNS and Certificates
  - Create ACM certificate for application domain
  - Configure Route 53 CNAME to endpoint domain
  - Validate certificate and DNS resolution
```

## Workflow 2: Cedar Policy Development

```
Step 1: Define Access Requirements
  - Map user groups to application access needs
  - Define device compliance requirements
  - Identify time-based or context-based restrictions

Step 2: Write and Test Policies
  - Start with permit policies for known good access
  - Add forbid policies for explicit denials
  - Test with various identity and device contexts
  - Validate in non-production environment

Step 3: Deploy Policies
  - Apply group-level policies first
  - Add endpoint-specific policies for sensitive apps
  - Monitor access logs for false denials
  - Iterate based on user feedback

Step 4: Ongoing Maintenance
  - Review policies quarterly
  - Update device trust thresholds
  - Add new groups as teams change
  - Remove deprecated application endpoints
```

## Workflow 3: Multi-Account Deployment

```
Step 1: Design Architecture
  - Deploy Verified Access in dedicated networking account
  - Plan group sharing via AWS RAM
  - Define organizational unit boundaries

Step 2: Share Resources
  - Create RAM resource shares
  - Associate Verified Access groups
  - Share with target OUs or accounts

Step 3: Create Endpoints in Workload Accounts
  - Accept RAM shares in workload accounts
  - Create endpoints using shared groups
  - Configure application-specific settings

Step 4: Centralized Monitoring
  - Aggregate access logs to central S3 bucket
  - Configure cross-account CloudWatch dashboards
  - Set up centralized alerting for policy violations
```

---

## Working Template

## Deployment Configuration
- **AWS Region**: _______________
- **Account Type**: [ ] Single-account [ ] Multi-account (RAM)
- **Identity Provider**: [ ] IAM Identity Center [ ] Okta [ ] Other OIDC
- **Device Trust Provider**: [ ] CrowdStrike [ ] Jamf [ ] JumpCloud

## Trust Providers

| Provider | Type | Reference Name | Status |
|---|---|---|---|
| ___ | user (identity) | ___ | [ ] Configured |
| ___ | device | ___ | [ ] Configured |

## Access Groups

| Group Name | Policy Summary | Endpoint Count | Min Device Score |
|---|---|---|---|
| ___ | ___ | ___ | ___ |

## Application Endpoints

| Application | Domain | Port | Group | Policy Level |
|---|---|---|---|---|
| ___ | ___ | 443 | ___ | group/endpoint |

## Cedar Policy Checklist
- [ ] Group-level policies defined for all groups
- [ ] Endpoint-level policies added for sensitive applications
- [ ] Device trust score thresholds set appropriately
- [ ] Forbid policies block unmanaged devices
- [ ] Admin access requires high device trust (>90)
- [ ] Policies tested in non-production first

## Monitoring Setup
- [ ] Access logs sent to CloudWatch Logs
- [ ] Access logs archived to S3
- [ ] CloudWatch alarms for high denial rates
- [ ] Dashboard created for access metrics
