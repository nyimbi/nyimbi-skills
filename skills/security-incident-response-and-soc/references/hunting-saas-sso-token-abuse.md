# Hunting Saas SSO Token Abuse

## API Reference

## Microsoft Entra ID (Sentinel / Log Analytics) Tables

| Table | Description |
|-------|-------------|
| `SigninLogs` | Interactive user sign-ins |
| `AADNonInteractiveUserSignInLogs` | Non-interactive sign-ins; common surface for replayed cookies/refresh tokens |
| `AADServicePrincipalSignInLogs` | Service-principal sign-ins |
| `AuditLogs` | Directory changes incl. OAuth consent / permission grants |
| `AADManagedIdentitySignInLogs` | Managed-identity authentications |

### Key correlation fields

| Field | Meaning |
|-------|---------|
| `SessionId` | Linkable identifier joining all artifacts from one root auth event |
| `UniqueTokenIdentifier` | Per-token identifier; correlate issuance to usage |
| `IPAddress` / `LocationDetails` | Source IP and GeoIP for impossible-travel/ASN checks |
| `AppDisplayName` / `ResourceDisplayName` | Which SaaS app/resource the token accessed |
| `ConditionalAccessStatus` | Whether CA applied (notApplied can indicate replay) |
| `ResultType` | `0` = success |

## Okta System Log API

`GET https://<org>.okta.com/api/v1/logs` with header `Authorization: SSWS <token>`.

| Parameter | Description |
|-----------|-------------|
| `filter` | SCIM filter, e.g. `eventType eq "policy.evaluate_sign_on"` |
| `since` / `until` | ISO-8601 time bounds |
| `q` | Free-text search |
| `limit` | Page size |

### Key event types and fields

| Item | Meaning |
|------|---------|
| `user.session.start` | New session created |
| `policy.evaluate_sign_on` | Sign-on policy evaluation (per-access) |
| `authentication.sso` | SSO into a downstream app |
| `authenticationContext.externalSessionId` | Session identifier for reuse detection |
| `client.ipAddress` / `client.userAgent.rawUserAgent` | Source context for divergence checks |
| `actor.alternateId` | The user |

## Response / Remediation

| Action | Command/API |
|--------|-------------|
| Revoke Entra sessions | `POST https://graph.microsoft.com/v1.0/users/{id}/revokeSignInSessions` |
| Clear Okta user sessions | `DELETE https://<org>.okta.com/api/v1/users/{id}/sessions` |
| Enforce token protection | Entra Conditional Access "Require token protection for sign-in sessions" |

---

## Standards and Controls

## NIST Cybersecurity Framework 2.0

| ID | Name | Rationale |
|----|------|-----------|
| DE.CM-01 | Networks and network services are monitored to find potentially adverse events | Hunting SSO/OAuth token replay across identity logs is continuous monitoring of authentication services for adverse events. |

## MITRE ATT&CK (Enterprise / Cloud)

| ID | Name | Rationale |
|----|------|-----------|
| T1550.001 | Use Alternate Authentication Material: Application Access Token | Core hunted technique — replaying stolen OAuth tokens/cookies. |
| T1539 | Steal Web Session Cookie | The cookie theft that enables pass-the-cookie. |
| T1528 | Steal Application Access Token | Token acquisition via phishing/illicit consent. |
| T1078.004 | Valid Accounts: Cloud Accounts | Replayed tokens provide valid-account SaaS access. |
| T1098.001 | Account Manipulation: Additional Cloud Credentials | Follow-on persistence after token abuse. |

## Supporting References

- MITRE ATT&CK T1550.001 — https://attack.mitre.org/techniques/T1550/001/
- Microsoft Entra sign-in log schema — https://learn.microsoft.com/en-us/entra/identity/monitoring-health/reference-azure-monitor-sign-ins-log-schema
- Okta System Log API — https://developer.okta.com/docs/reference/api/system-log/
- Mandiant M-Trends — https://www.mandiant.com/m-trends
- NIST CSF 2.0 — https://www.nist.gov/cyberframework
