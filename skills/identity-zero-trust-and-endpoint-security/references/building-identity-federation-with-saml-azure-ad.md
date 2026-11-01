# Building Identity Federation With SAML azure AD

## API Reference

## Federation Metadata URL
```
https://login.microsoftonline.com/{tenant-id}/federationmetadata/2007-06/federationmetadata.xml
```

## SAML 2.0 Endpoints
| Endpoint | URL |
|----------|-----|
| SSO (POST) | `https://login.microsoftonline.com/{tenant}/saml2` |
| SSO (Redirect) | `https://login.microsoftonline.com/{tenant}/saml2` |
| Logout | `https://login.microsoftonline.com/{tenant}/saml2` |

## SP Metadata Required Fields
| Field | Description |
|-------|-------------|
| `entityID` | SP unique identifier |
| `AssertionConsumerService` | ACS URL (POST binding) |
| `NameIDFormat` | emailAddress or persistent |
| `SingleLogoutService` | SLO URL (optional) |

## XML Namespaces
```python
ns = {
    "md": "urn:oasis:names:tc:SAML:2.0:metadata",
    "ds": "http://www.w3.org/2000/09/xmldsig#",
    "saml": "urn:oasis:names:tc:SAML:2.0:assertion",
}
```

## SAML Bindings
| Binding | URI |
|---------|-----|
| HTTP-POST | `urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST` |
| HTTP-Redirect | `urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect` |
| SOAP | `urn:oasis:names:tc:SAML:2.0:bindings:SOAP` |

## Azure AD Graph API (App Registration)
```
POST https://graph.microsoft.com/v1.0/servicePrincipals
Authorization: Bearer TOKEN
{
  "appId": "app-id",
  "preferredSingleSignOnMode": "saml",
  "loginUrl": "https://app.example.com/login"
}
```

## Validation Checks
| Check | Severity |
|-------|----------|
| HTTPS on ACS URL | High |
| Certificate present | Critical |
| HTTP-POST binding available | Medium |
| NameID format configured | Medium |

---

## Standards and Controls

## Federation Protocols

### SAML 2.0 (OASIS)
- Security Assertion Markup Language version 2.0
- XML-based framework for exchanging authentication/authorization data
- Profiles: Web Browser SSO, Enhanced Client or Proxy, Single Logout
- Bindings: HTTP Redirect, HTTP POST, HTTP Artifact, SOAP

### WS-Federation (OASIS)
- Web Services Federation Language
- Used by AD FS for passive federation (browser-based)
- Token types: SAML 1.1, SAML 2.0

### OpenID Connect
- Built on OAuth 2.0
- JSON/REST-based (vs. SAML XML)
- Used by Azure AD as primary protocol for modern applications
- JWT tokens instead of SAML assertions

## Microsoft Entra ID Federation Requirements

### Supported Federation Protocols
| Protocol | Use Case | Token Format |
|----------|----------|-------------|
| SAML 2.0 | Enterprise SSO, third-party apps | SAML assertion (XML) |
| WS-Federation | Legacy applications, AD FS | SAML token |
| OpenID Connect | Modern web/mobile apps | JWT |

### Domain Federation Requirements
- Domain must be verified in Azure AD
- Only one federation configuration per domain
- Password hash sync recommended as backup
- Azure AD Connect for hybrid identity sync

## Compliance Mapping

### NIST SP 800-63C - Federation and Assertions
- FAL1: Bearer assertion, direct presentation
- FAL2: Bearer assertion with additional security
- FAL3: Holder-of-key assertion

### FedRAMP
- IA-2: Identification and Authentication
- IA-5: Authenticator Management
- IA-8: Identification and Authentication (Non-Organizational Users)
- Federation required for cross-organization access

### ISO 27001:2022
- A.5.16: Identity management
- A.5.17: Authentication information
- A.8.5: Secure authentication

---

## Workflows

## Federation Setup Workflow

```
Phase 1: PREREQUISITES
    ├── Verify domain ownership in Azure AD
    ├── Install and configure Azure AD Connect for user sync
    ├── Deploy AD FS farm (if using on-premises federation)
    ├── Obtain public TLS certificate for federation endpoint
    └── Configure DNS for federation service name

Phase 2: FEDERATION CONFIGURATION
    ├── Configure AD FS relying party trust for Azure AD
    ├── Set up claims issuance rules (UPN, ImmutableID)
    ├── Convert Azure AD domain from managed to federated
    ├── Verify federation with Test-MgDomainFederationConfiguration
    └── Test user sign-in through federation flow

Phase 3: APPLICATION SSO
    ├── Add SaaS applications to Azure AD enterprise apps
    ├── Configure SAML SSO for each application
    ├── Map user attributes and claims
    ├── Test SSO for each application
    └── Assign users/groups to applications

Phase 4: SECURITY HARDENING
    ├── Enable conditional access policies
    ├── Configure MFA at AD FS or Azure AD level
    ├── Enable smart lockout and extranet lockout
    ├── Set up certificate auto-rollover
    └── Forward AD FS audit logs to SIEM
```

## SAML Authentication Flow (Federated Domain)

```
User accesses cloud application
    │
    ├── Application redirects to Azure AD
    │   (Azure AD acts as IdP for the application)
    │
    ├── Azure AD identifies user's domain as federated
    │
    ├── Azure AD redirects user to on-premises AD FS
    │   (AD FS is the IdP for the federated domain)
    │
    ├── AD FS authenticates user against Active Directory:
    │   ├── Kerberos (if on corporate network)
    │   ├── Forms-based authentication (if external)
    │   └── MFA challenge (if configured)
    │
    ├── AD FS issues SAML assertion with claims:
    │   ├── UPN (user principal name)
    │   ├── ImmutableID (objectGUID base64-encoded)
    │   ├── Email, display name, groups
    │   └── Signed with token-signing certificate
    │
    ├── SAML assertion posted to Azure AD
    │
    ├── Azure AD validates assertion:
    │   ├── Verify signature against known AD FS certificate
    │   ├── Match ImmutableID to synced user
    │   ├── Apply conditional access policies
    │   └── Issue Azure AD token for the application
    │
    └── User accesses the cloud application
```

## Failover Workflow (AD FS Outage)

```
AD FS becomes unavailable
    │
    ├── Users cannot authenticate through federation
    │
    ├── OPTION 1: Staged Rollout to Managed Authentication
    │   ├── Enable password hash sync as backup (should already be active)
    │   ├── Use Azure AD staged rollout to move groups to managed auth
    │   └── Users authenticate directly with Azure AD (password hash)
    │
    ├── OPTION 2: Convert Domain to Managed
    │   ├── Run: Convert-MgDomainToManaged (emergency procedure)
    │   ├── All users switch to Azure AD authentication
    │   └── Requires password hash sync to be active
    │
    └── After AD FS restored:
        ├── Re-establish federation trust
        ├── Convert domain back to federated
        └── Verify authentication flow
```

## Certificate Rotation Workflow

```
AD FS token-signing certificate approaching expiry
    │
    ├── Auto-Rollover Enabled (recommended):
    │   ├── AD FS generates new certificate 20 days before expiry
    │   ├── New cert is added as secondary
    │   ├── Azure AD automatically picks up via metadata refresh
    │   ├── New cert promoted to primary at expiry
    │   └── Old cert removed after grace period
    │
    └── Manual Rotation:
        ├── Generate new signing certificate in AD FS
        ├── Add as secondary: Set-AdfsCertificate ... -IsPrimary $false
        ├── Update Azure AD: Update-MgDomainFederationConfiguration
        ├── Wait for replication (allow 24-48 hours)
        ├── Promote to primary: Set-AdfsCertificate ... -IsPrimary $true
        └── Remove old certificate
```

---

## Working Template

## Federation Details

| Setting | Value |
|---------|-------|
| Azure AD Tenant ID | |
| Federated Domain | |
| AD FS Farm Name | |
| AD FS Service URL | `https://fs.___/adfs/ls/` |
| Federation Protocol | SAML 2.0 / WS-Federation |
| Backup Auth | Password Hash Sync / Pass-Through Auth |

## AD FS Configuration

| Setting | Value |
|---------|-------|
| AD FS Version | |
| Service Account | gMSA recommended |
| Token-Signing Cert Expiry | |
| Auto-Rollover Enabled | Yes / No |
| WAP Deployed | Yes / No |

## Claims Rules

| Rule Name | Source Attribute | Claim Type | Description |
|-----------|-----------------|------------|-------------|
| UPN | userPrincipalName | NameID | Primary identifier |
| ImmutableID | objectGUID (base64) | ImmutableID | Azure AD anchor |
| Email | mail | emailaddress | User email |

## Validation Results

| Test | Status | Notes |
|------|--------|-------|
| AD FS metadata reachable | Pass/Fail | |
| Token-signing certificate valid | Pass/Fail | |
| Domain federation configured in Azure AD | Pass/Fail | |
| SP-initiated SSO flow | Pass/Fail | |
| IdP-initiated SSO flow | Pass/Fail | |
| MFA enforcement | Pass/Fail | |
| Smart lockout configured | Pass/Fail | |
| Sign-in logs showing federated auth | Pass/Fail | |

## Disaster Recovery

- [ ] Password hash sync enabled as backup
- [ ] Staged rollout to managed auth tested
- [ ] Break-glass cloud-only admin accounts created
- [ ] AD FS farm disaster recovery plan documented
- [ ] Secondary AD FS farm in DR site (if applicable)
