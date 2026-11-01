# Implementing Google Workspace SSO Configuration

## API Reference

## SAML 2.0 Endpoints

| Endpoint | URL |
|----------|-----|
| SP ACS URL | `https://accounts.google.com/samlrp/acs?rpid=RPID` |
| SP Entity ID | `google.com/a/DOMAIN` |
| SP Metadata | `https://accounts.google.com/samlrp/metadata?rpid=RPID` |

## Admin Console Path

```
Admin Console > Security > Authentication > SSO with third-party IdP
```

## SAML Configuration Fields

| Field | Description |
|-------|-------------|
| Sign-in page URL | IdP SSO endpoint (HTTPS required) |
| Sign-out page URL | IdP SLO endpoint |
| Change password URL | IdP password change page |
| Verification certificate | IdP X.509 signing cert (PEM, RSA 2048+) |
| Domain-specific issuer | Use domain in SAML issuer |

## Certificate Validation (Python cryptography)

```python
from cryptography import x509
cert = x509.load_pem_x509_certificate(pem_data)
print(cert.not_valid_after_utc)
print(cert.subject.rfc4514_string())
print(cert.public_key().key_size)
```

## Admin SDK Reports API (Login Activity)

```python
from googleapiclient.discovery import build
service = build("admin", "reports_v1", credentials=creds)
activities = service.activities().list(
    userKey="all", applicationName="login",
    eventName="login_success").execute()
```

## Common IdP Providers

| IdP | SAML SSO URL Pattern |
|-----|---------------------|
| Okta | `https://DOMAIN.okta.com/app/APP_ID/sso/saml` |
| Azure AD | `https://login.microsoftonline.com/TENANT/saml2` |
| ADFS | `https://ADFS_HOST/adfs/ls/` |
| Ping Identity | `https://sso.connect.pingidentity.com/sso/sp/initsso` |

### References

- Google Workspace SSO: https://support.google.com/a/answer/60224
- SAML 2.0 Admin Guide: https://support.google.com/a/answer/6349809
- Admin SDK: https://developers.google.com/admin-sdk/reports/v1/guides/manage-audit-login

---

## Standards and Controls

## SAML 2.0 Standard

### OASIS SAML 2.0 Core
- Assertions: Authentication statements, attribute statements
- Protocols: AuthnRequest, Response, LogoutRequest
- Bindings: HTTP Redirect, HTTP POST, Artifact
- Profiles: Web Browser SSO, Single Logout

### Google Workspace SAML Requirements
- SAML 2.0 compliant IdP
- HTTP POST binding for Assertion Consumer Service
- Signed SAML assertions (RSA-SHA256 recommended)
- NameID format: emailAddress (user's primary email)
- X.509 PEM certificate for signature verification

## Google Workspace SSO Parameters

| Parameter | Value |
|-----------|-------|
| ACS URL | `https://www.google.com/a/{domain}/acs` |
| Entity ID (domain-specific) | `google.com/a/{domain}` |
| Entity ID (generic) | `google.com` |
| NameID Format | `urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress` |
| SAML Version | 2.0 |
| Binding | HTTP-POST |

## Compliance Mapping

### NIST SP 800-63-3 (Digital Identity Guidelines)
- AAL2: Multi-factor authentication (enforced at IdP)
- Federation assurance levels (FAL1-FAL3)
- Assertion protection requirements

### SOC 2 - CC6.1
- Single sign-on centralizes access control
- Audit trail of authentication events
- Timely deprovisioning via IdP user removal

### ISO 27001:2022 - A.8.5
- Secure authentication through centralized IdP
- MFA enforcement via SSO configuration
- Session management controls

---

## Workflows

## SSO Configuration Workflow

```
1. PREPARE IDP
   ├── Create Google Workspace SAML application in IdP
   ├── Configure ACS URL: https://www.google.com/a/{domain}/acs
   ├── Configure Entity ID: google.com/a/{domain}
   ├── Set NameID to user email address
   ├── Map required attributes (firstName, lastName)
   └── Download IdP metadata (SSO URL, certificate, entity ID)

2. CONFIGURE GOOGLE ADMIN CONSOLE
   ├── Navigate to Security > Authentication > SSO with third-party IdP
   ├── Enable third-party SSO
   ├── Enter Sign-in page URL from IdP
   ├── Enter Sign-out page URL from IdP
   ├── Upload IdP verification certificate
   ├── Enable domain-specific issuer
   └── Save configuration

3. ASSIGN SSO PROFILE
   ├── Apply to entire organization OR
   ├── Apply to specific organizational units OR
   └── Apply to specific groups

4. TEST
   ├── Test IdP-initiated SSO (login from IdP portal)
   ├── Test SP-initiated SSO (login from Google page)
   ├── Test sign-out flow
   ├── Test with user not in IdP (should fail)
   └── Test break-glass Super Admin access (should bypass SSO)

5. ROLLOUT
   ├── Communicate changes to users
   ├── Apply to all organizational units
   ├── Monitor for authentication failures
   └── Update help desk with troubleshooting guide
```

## User Authentication Flow (SP-Initiated)

```
User navigates to mail.google.com/a/{domain}
    │
    ├── Google identifies federated domain
    │
    ├── Redirect to IdP with SAML AuthnRequest
    │   URL: {IdP SSO URL}?SAMLRequest={base64encoded}
    │
    ├── User authenticates at IdP:
    │   ├── Enter credentials
    │   ├── Complete MFA challenge
    │   └── IdP validates against directory
    │
    ├── IdP generates SAML Response:
    │   ├── Assertion with NameID (email)
    │   ├── Authentication context (MFA)
    │   ├── Digitally signed with IdP certificate
    │   └── Optionally encrypted
    │
    ├── Browser POSTs Response to Google ACS URL
    │
    ├── Google validates:
    │   ├── Signature against uploaded certificate
    │   ├── Assertion not expired
    │   ├── Audience matches entity ID
    │   ├── NameID matches a Google Workspace user
    │   └── InResponseTo matches original request
    │
    └── User logged in to Google Workspace
```

## Certificate Renewal Workflow

```
IdP signing certificate approaching expiration (30 days before)
    │
    ├── Generate new signing certificate in IdP
    │
    ├── Upload new certificate to Google Admin Console
    │   (Google supports multiple verification certificates)
    │
    ├── Promote new certificate as primary in IdP
    │
    ├── Verify SSO still works with new certificate
    │
    └── Remove old certificate from Google Admin Console after confirmation
```

## Troubleshooting Workflow

```
User reports SSO failure
    │
    ├── Check 1: Is user assigned to the Google Workspace app in IdP?
    │   └── NO → Assign user in IdP
    │
    ├── Check 2: Does NameID match user's Google email exactly?
    │   └── NO → Fix attribute mapping in IdP
    │
    ├── Check 3: Is the IdP certificate expired?
    │   └── YES → Upload renewed certificate
    │
    ├── Check 4: Is there clock skew between IdP and Google?
    │   └── YES → Sync NTP on IdP server (max 5 min skew allowed)
    │
    ├── Check 5: Is the SAML assertion properly signed?
    │   └── NO → Verify IdP signing algorithm matches uploaded cert
    │
    └── Check 6: Check IdP SAML debug logs for detailed error
```

---

## Working Template

## Configuration Details

| Setting | Value |
|---------|-------|
| Google Workspace Domain | |
| ACS URL | `https://www.google.com/a/{domain}/acs` |
| Entity ID | `google.com/a/{domain}` |
| IdP Name | Okta / Azure AD / ADFS / Other |
| IdP SSO URL | |
| IdP Sign-out URL | |
| Certificate Expiry | |

## Pre-Implementation Checklist

- [ ] Google Workspace Super Admin access confirmed
- [ ] IdP SAML application created for Google Workspace
- [ ] IdP signing certificate exported (X.509 PEM)
- [ ] User attributes mapped (NameID = email)
- [ ] Test users assigned in IdP
- [ ] Break-glass Super Admin account identified (bypasses SSO)

## Testing Results

| Test Case | Result | Notes |
|-----------|--------|-------|
| SP-initiated SSO (from Google login) | Pass/Fail | |
| IdP-initiated SSO (from IdP portal) | Pass/Fail | |
| User not in IdP (access denied) | Pass/Fail | |
| Sign-out flow | Pass/Fail | |
| Super Admin bypass | Pass/Fail | |
| MFA enforcement at IdP | Pass/Fail | |
| Clock skew tolerance | Pass/Fail | |

## Rollout Plan

- [ ] Phase 1: IT team pilot (1 week)
- [ ] Phase 2: Engineering department (1 week)
- [ ] Phase 3: All organizational units
- [ ] User communication sent
- [ ] Help desk trained
- [ ] Monitoring configured for auth failures
