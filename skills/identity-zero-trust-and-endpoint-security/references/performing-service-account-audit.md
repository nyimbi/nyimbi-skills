# Performing Service Account Audit

## API Reference

## Active Directory PowerShell Cmdlets

| Cmdlet | Description |
|--------|-------------|
| `Get-ADUser -Filter {ServicePrincipalName -ne '$null'}` | Find accounts with SPNs |
| `Get-ADServiceAccount -Filter *` | List managed service accounts |
| `Get-ADGroupMember -Identity "Domain Admins"` | List privileged group members |
| `Search-ADAccount -PasswordNeverExpires` | Find non-expiring passwords |
| `Search-ADAccount -AccountInactive -TimeSpan 90.00:00:00` | Find inactive accounts |

## AWS IAM CLI Commands

| Command | Description |
|---------|-------------|
| `aws iam list-users` | List all IAM users |
| `aws iam list-access-keys --user-name <name>` | List access keys for user |
| `aws iam get-access-key-last-used --access-key-id <id>` | Check key last used date |
| `aws iam list-user-policies --user-name <name>` | List inline policies |
| `aws iam list-attached-user-policies --user-name <name>` | List managed policies |
| `aws iam generate-credential-report` | Generate credential report |

## Azure CLI Commands

| Command | Description |
|---------|-------------|
| `az ad sp list --all` | List all service principals |
| `az ad app list --all` | List all app registrations |
| `az ad app credential list --id <app-id>` | List credential expiration |

## Risk Classification

| Level | Score Range | Criteria |
|-------|------------|----------|
| Critical | >= 40 | Domain admin + stale password + no owner |
| High | 25-39 | Privileged group membership or orphaned |
| Medium | 10-24 | Password age exceeded or PasswordNeverExpires |
| Low | 0-9 | Standard permissions, managed credentials |

## Python Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| `subprocess` | stdlib | Execute PowerShell and AWS CLI commands |
| `json` | stdlib | Parse CLI output |
| `ldap3` | >=2.9 | Direct LDAP queries to Active Directory |
| `boto3` | >=1.26 | AWS IAM programmatic access |

## References

- NIST SP 800-53 AC-2: Account Management
- CIS Benchmark for Active Directory
- AWS IAM Best Practices: https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html
- Microsoft gMSA: https://learn.microsoft.com/en-us/windows-server/security/group-managed-service-accounts/group-managed-service-accounts-overview

---

## Standards and Controls

## NIST Standards
- **NIST SP 800-53 Rev 5**: AC-2, AC-2(3), AC-6, IA-5, AU-6
- **NIST SP 800-171**: 3.1.1, 3.1.2, 3.5.1, 3.5.2

## Industry Frameworks
- **CIS Controls v8**: Control 5.3 - Disable Dormant Accounts, Control 5.4 - Restrict Administrator Privileges
- **MITRE ATT&CK**: T1078 (Valid Accounts), T1136 (Create Account)
- **PCI DSS 4.0**: 7.2.5 - Review user access, 8.6 - Application/system account management
- **SOX Section 404**: Service account access controls for financial systems

## Tools
- **Microsoft AD**: Get-ADServiceAccount, Get-ADUser with SPN filter
- **AWS IAM**: Access Analyzer, Credential Report, IAM Access Advisor
- **Azure Entra ID**: Service principal reports, App registration audit
- **CyberArk DNA**: Automated privileged account discovery
- **Stealthbits (Netwrix)**: Service account discovery and monitoring

---

## Workflows

## Workflow 1: Discovery Phase
1. Export AD service accounts using PowerShell/LDAP queries
2. Export cloud IAM service accounts (AWS credential report, Azure SP list, GCP SA list)
3. Query databases for application-specific service accounts
4. Consolidate into single inventory spreadsheet
5. Cross-reference with CMDB for ownership data

## Workflow 2: Assessment Phase
1. Check each account against privilege policy
2. Verify password/key rotation compliance (90-day max)
3. Check last logon/activity date
4. Validate owner assignment against HR data
5. Flag accounts meeting orphaned/stale/over-privileged criteria

## Workflow 3: Remediation Phase
1. Contact owners of over-privileged accounts for justification
2. Plan gMSA migration for eligible Windows service accounts
3. Disable orphaned accounts (staged: disable first, delete after 30 days)
4. Rotate stale credentials immediately
5. Update documentation, close findings, report to compliance

---

## Working Template

## Service Account Inventory
| Account Name | Platform | Type | Owner | Application | Privilege | Password Age | Last Used | Status |
|-------------|----------|------|-------|-------------|-----------|-------------|-----------|--------|
| | | | | | | | | |

## Risk Classification
| Risk Level | Criteria | Action Required |
|------------|----------|-----------------|
| Critical | Domain admin + no rotation | Immediate rotation, vault in PAM |
| High | Privileged + no owner | Assign owner within 7 days |
| Medium | Standard + stale password | Rotate within 30 days |
| Low | Read-only + managed | Include in next review cycle |

## Remediation Tracking
| Account | Finding | Assigned To | Due Date | Status |
|---------|---------|-------------|----------|--------|
| | | | | |

## Sign-Off
| Role | Name | Date |
|------|------|------|
| IT Security Lead | | |
| Compliance Officer | | |
