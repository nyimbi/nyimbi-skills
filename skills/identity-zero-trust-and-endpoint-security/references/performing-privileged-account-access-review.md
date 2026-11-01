# Performing Privileged Account Access Review

## API Reference

## CSV Input Format

The agent consumes a CSV file with these columns:

| Column | Type | Description |
|--------|------|-------------|
| `username` | string | Account identifier (SAMAccountName or UPN) |
| `owner` | string | Assigned account owner / manager |
| `roles` | string | Semicolon-separated privilege roles |
| `last_used` | string | ISO date `YYYY-MM-DD` of last interactive logon |
| `last_certified` | string | ISO date `YYYY-MM-DD` of most recent access review |
| `account_type` | string | `human`, `service`, or `shared` |

## Checks Performed

### Stale Account Detection
Flags accounts whose `last_used` date exceeds a configurable threshold (default 90 days). Accounts without a `last_used` value are automatically flagged as high severity.

### Shared Account Detection
Matches `username` against common shared-account patterns: `admin`, `root`, `service`, `svc_`, `shared`, `generic`, `temp`. Flags accounts matching these patterns that lack an assigned `owner`.

### Excessive Privilege Detection
Compares the `roles` field against high-risk role names: Domain Admin, Enterprise Admin, Schema Admin, Global Admin, Super Admin, Root. Any match triggers a critical finding.

### Recertification Compliance
Compares `last_certified` against a configurable interval (default 180 days). Accounts never certified are flagged as critical.

## Output Schema

```json
{
  "report": "privileged_account_access_review",
  "generated_at": "ISO-8601 timestamp",
  "total_accounts": 150,
  "total_findings": 12,
  "severity_summary": {"critical": 3, "high": 7, "medium": 2},
  "findings": [
    {
      "account": "svc_backup",
      "issue": "shared_account_no_owner",
      "severity": "critical",
      "detail": "Appears shared (matches 'svc_') with no assigned owner"
    }
  ]
}
```

## Compliance Frameworks

- **NIST SP 800-53 AC-2**: Account Management — periodic review of privileged accounts
- **CIS Controls v8 5.3**: Disable dormant accounts after 45 days of inactivity
- **PCI DSS 8.1.4**: Remove/disable inactive user accounts within 90 days
- **SOX Section 404**: Internal controls over financial reporting require access reviews
- **ISO 27001 A.9.2.5**: Review of user access rights at planned intervals

## CLI Usage

```bash
python agent.py --input accounts.csv --stale-days 90 --cert-days 180 --output report.json
```

---

## Standards and Controls

## Regulatory Requirements

### SOC 2 Type II - CC6.1, CC6.2, CC6.3
- CC6.1: Logical and physical access controls restrict access to information assets
- CC6.2: Prior to issuing system credentials, the entity registers and authorizes new users
- CC6.3: The entity authorizes, modifies, or removes access in a timely manner
- Quarterly privileged access reviews required for audit evidence

### PCI DSS v4.0 - Requirement 7
- 7.1: Processes and mechanisms for restricting access are defined and understood
- 7.2: Access to system components and data is appropriately defined and assigned
- 7.2.4: All user accounts and related access privileges are reviewed at least every six months
- 7.2.5: All application and system accounts and privileges are reviewed at least every six months

### HIPAA Security Rule - 164.312(a)(1)
- Access control standard requiring unique user identification
- Emergency access procedure (break-glass accounts)
- Automatic logoff and encryption/decryption
- Periodic review and modification of access rights

### SOX Section 404
- Internal controls over financial reporting
- Segregation of duties enforcement
- Access to financial systems must be reviewed quarterly
- Evidence of review decisions must be retained

### NIST SP 800-53 Rev 5 - Access Control Family
- AC-2: Account Management (review periodically)
- AC-2(3): Disable Accounts (within defined time period)
- AC-2(4): Automated Audit Actions
- AC-2(12): Account Monitoring for Atypical Usage
- AC-6: Least Privilege
- AC-6(7): Review of User Privileges

## Industry Frameworks

### CIS Controls v8
- Control 5.1: Establish and maintain an inventory of accounts
- Control 5.2: Use unique passwords
- Control 5.3: Disable dormant accounts
- Control 5.4: Restrict administrator privileges to dedicated administrator accounts
- Control 5.5: Establish and maintain an inventory of service accounts

### NIST Cybersecurity Framework 2.0
- PR.AA-01: Identities and credentials for authorized users are managed
- PR.AA-02: Identities are proofed and bound to credentials
- PR.AA-03: Users, services, and hardware are authenticated
- PR.AA-05: Access permissions, entitlements, and authorizations are defined

---

## Workflows

## Quarterly Review Cycle

```
Week 1: PREPARATION
    ├── Extract privileged account inventory from PAM/AD/Cloud
    ├── Identify new accounts since last review
    ├── Assign reviewers based on account ownership
    └── Send review campaign notifications

Week 2-3: REVIEW EXECUTION
    ├── Reviewers evaluate each account against criteria
    ├── Approve, revoke, or flag for investigation
    ├── Escalate unresponsive reviewers after 7 days
    └── Security team reviews flagged accounts

Week 4: REMEDIATION
    ├── Disable/remove revoked accounts
    ├── Rotate credentials for all reviewed accounts
    ├── Create tickets for privilege reduction
    └── Generate review completion report
```

## Account Discovery Workflow

```
1. Active Directory Enumeration
   ├── Query AdminCount=1 accounts
   ├── Enumerate privileged group memberships
   ├── Identify accounts with SPN (service accounts)
   └── Check for accounts with delegation rights

2. Cloud Platform Enumeration
   ├── AWS: List IAM users/roles with admin policies
   ├── Azure: Export Entra ID directory role assignments
   ├── GCP: List IAM bindings with Owner/Editor roles
   └── Cross-reference with known approved accounts

3. Database and Application Enumeration
   ├── Query database system role memberships
   ├── Export application admin role assignments
   └── Identify shared/generic admin accounts

4. Consolidation
   ├── Merge all discovered accounts into single inventory
   ├── Deduplicate accounts across platforms
   ├── Assign risk classification
   └── Identify accounts missing from PAM vault
```

## Reviewer Decision Workflow

```
Reviewer receives account for certification
    │
    ├── Is the account owner still employed?
    │   ├── NO → Revoke immediately, disable account
    │   └── YES → Continue
    │
    ├── Has the account been used in last 90 days?
    │   ├── NO → Recommend disable, notify owner
    │   └── YES → Continue
    │
    ├── Does the user's current role require this privilege?
    │   ├── NO → Revoke, provide lower-privilege alternative
    │   └── YES → Continue
    │
    ├── Can the privilege be reduced (least privilege)?
    │   ├── YES → Approve with remediation to reduce
    │   └── NO → Continue
    │
    ├── Are there SoD conflicts?
    │   ├── YES → Flag for risk acceptance or remediation
    │   └── NO → Continue
    │
    └── CERTIFY the access with documented justification
```

## Emergency Account Review Workflow

```
Break-glass account used
    │
    ├── Alert generated to security team
    │
    ├── Within 24 hours:
    │   ├── Verify incident ticket exists for the usage
    │   ├── Confirm authorized personnel used the account
    │   ├── Review session recording (if available)
    │   └── Validate actions taken were appropriate
    │
    ├── Within 48 hours:
    │   ├── Reset break-glass account credentials
    │   ├── Store new credentials in sealed envelope/vault
    │   └── Document usage in access review log
    │
    └── Monthly: Verify break-glass accounts have not been used
        without corresponding incident documentation
```

---

## Working Template

## Review Campaign Details

| Field | Value |
|-------|-------|
| Campaign Name | Q___ 20__ Privileged Access Review |
| Review Period | ___/___/20__ to ___/___/20__ |
| Due Date | ___/___/20__ |
| Scope | All privileged accounts |
| Reviewer | _______________ |

## Review Summary

| Metric | Count |
|--------|-------|
| Total Accounts in Scope | |
| Accounts Reviewed | |
| Accounts Certified (Approved) | |
| Accounts Revoked | |
| Accounts Flagged for Investigation | |
| Overdue Reviews | |

## Review Decisions Log

| # | Username | Platform | Privilege | Decision | Justification | Date |
|---|----------|----------|-----------|----------|---------------|------|
| 1 | | | | Approve/Revoke/Flag | | |
| 2 | | | | | | |
| 3 | | | | | | |

## Findings and Remediation

### Finding 1
- **Description**:
- **Risk Level**: Critical / High / Medium / Low
- **Affected Accounts**:
- **Remediation Action**:
- **Due Date**:
- **Assigned To**:

### Finding 2
- **Description**:
- **Risk Level**:
- **Affected Accounts**:
- **Remediation Action**:
- **Due Date**:
- **Assigned To**:

## Compliance Evidence

- [ ] Review campaign initiated with formal notification
- [ ] All accounts in scope were assigned to reviewers
- [ ] Reviewers completed decisions with documented justification
- [ ] Revoked accounts were disabled within SLA
- [ ] Credentials were rotated for certified accounts
- [ ] Review report signed off by security leadership
- [ ] Evidence archived for audit retention period

## Sign-Off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Reviewer | | | |
| Security Manager | | | |
| Compliance Officer | | | |
