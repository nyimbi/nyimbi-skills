# Detecting azure Service Principal Abuse

## API Reference

## Libraries

| Library | Install | Purpose |
|---------|---------|---------|
| azure-identity | `pip install azure-identity` | Azure AD authentication |
| requests | `pip install requests` | Microsoft Graph API client |

## Microsoft Graph API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v1.0/servicePrincipals` | List service principals |
| GET | `/v1.0/servicePrincipals/{id}` | Get SP details and credentials |
| GET | `/v1.0/servicePrincipals/{id}/appRoleAssignments` | SP role assignments |
| GET | `/v1.0/directoryRoles` | List directory roles |
| GET | `/v1.0/directoryRoles/{id}/members` | Role members (includes SPs) |
| GET | `/v1.0/auditLogs/signIns` | Sign-in logs for SP activity |
| GET | `/v1.0/auditLogs/directoryAudits` | Directory change audit logs |

## OAuth2 Token Endpoint

```
POST https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token
grant_type=client_credentials
scope=https://graph.microsoft.com/.default
```

## High-Privilege Directory Roles

| Role | Risk |
|------|------|
| Global Administrator | Full tenant control |
| Application Administrator | Can create/manage all apps |
| Cloud Application Administrator | Manage cloud app registrations |
| Privileged Role Administrator | Manage role assignments |

## Service Principal Abuse Indicators

| Indicator | Description | Severity |
|-----------|-------------|----------|
| Multiple password credentials | Possible backdoor persistence | HIGH |
| Expired credentials not removed | Credential hygiene gap | MEDIUM |
| SP with Global Admin role | Overprivileged automation | CRITICAL |
| Unusual sign-in location | Compromised SP credentials | HIGH |
| New credential added to SP | Persistence via credential injection | CRITICAL |

## MITRE ATT&CK Mapping

| Technique | ID | Description |
|-----------|----|-------------|
| Account Manipulation | T1098 | Add credentials to SP |
| Valid Accounts: Cloud | T1078.004 | Abuse SP credentials |
| Trusted Relationship | T1199 | Abuse multi-tenant SP trust |

## External References

- [Microsoft Graph API: Service Principals](https://learn.microsoft.com/en-us/graph/api/resources/serviceprincipal)
- [Azure AD Sign-in Logs](https://learn.microsoft.com/en-us/entra/identity/monitoring-health/concept-sign-ins)
- [Detecting Azure AD Backdoors](https://posts.specterops.io/)

---

## Standards and Controls

## MITRE ATT&CK Techniques
- T1098.001: Account Manipulation - Additional Cloud Credentials
- T1078.004: Valid Accounts - Cloud Accounts
- T1087.004: Account Discovery - Cloud Account
- T1528: Steal Application Access Token
- T1550.001: Use Alternate Authentication Material - Application Access Token

## CIS Microsoft Azure Foundations Benchmark v2.1
- 1.11: Ensure that multi-factor authentication is enabled for all privileged users
- 1.14: Ensure that guest users are reviewed on a regular basis
- 1.15: Ensure that User consent for applications is set to Do not allow user consent

## Microsoft Secure Score Recommendations
- Require admin approval for unmanaged applications
- Remove unused application permissions
- Limit service principal credential lifetime
- Implement Conditional Access for workload identities

---

## Workflows

## Detection Workflow
```
1. Log Collection → Ingest Azure AD Audit + Sign-in logs to SIEM
2. Rule Activation → Enable detection analytics for SP abuse patterns
3. Alert Triage → Validate alerts against known automation accounts
4. Investigation → Correlate credential changes with sign-in anomalies
5. Containment → Disable compromised SP, rotate credentials
6. Remediation → Remove unauthorized permissions, review ownership
```

## Investigation Workflow
```
1. Identify affected service principal (name, object ID, app ID)
2. Review recent credential changes (new secrets/certificates)
3. Check role assignments for privilege escalation
4. Analyze sign-in logs for unusual IPs/locations
5. Review application ownership chain
6. Assess blast radius of compromised permissions
7. Document findings and initiate incident response
```

---

## Working Template

## Investigation Checklist

| Check | Status | Notes |
|-------|--------|-------|
| Recent credential additions (7 days) | [ ] | |
| Privileged role assignments to SPs | [ ] | |
| Application ownership review | [ ] | |
| Sign-in anomalies for SPs | [ ] | |
| Admin consent grants review | [ ] | |
| OAuth permission escalation | [ ] | |

## Affected Service Principals

| Display Name | App ID | Object ID | Finding Type | Severity |
|-------------|--------|-----------|--------------|----------|
| | | | | |

## Remediation Actions

| Action | Status | Completed By | Date |
|--------|--------|-------------|------|
| Rotate compromised credentials | [ ] | | |
| Remove unauthorized role assignments | [ ] | | |
| Disable compromised service principal | [ ] | | |
| Review and restrict app ownership | [ ] | | |
| Enable Conditional Access for workload identities | [ ] | | |
