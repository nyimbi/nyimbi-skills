# Implementing SAML SSO With Okta

## API Reference

## Okta Admin API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/apps` | GET | List applications (filter by SAML) |
| `/api/v1/apps/{id}/sso/saml/metadata` | GET | Retrieve SAML metadata XML |
| `/api/v1/apps/{id}/users` | GET | List user assignments |
| `/api/v1/apps/{id}/groups` | GET | List group assignments |
| `/api/v1/policies?type=OKTA_SIGN_ON` | GET | Check MFA policies |

## SAML Security Checks

| Check | Severity | Description |
|-------|----------|-------------|
| SHA-256 signature | High | SignatureMethod must not use SHA-1 |
| Assertion encryption | Medium | Encrypt assertions in transit |
| AudienceRestriction | High | Must limit assertion audience |
| Certificate expiry | Critical | Monitor signing cert expiration |
| SingleLogoutService | Medium | SLO endpoint should be configured |
| MFA enforcement | High | Require MFA for SAML authentication |

## SAML XML Namespaces

| Prefix | URI |
|--------|-----|
| md | `urn:oasis:names:tc:SAML:2.0:metadata` |
| ds | `http://www.w3.org/2000/09/xmldsig#` |
| saml | `urn:oasis:names:tc:SAML:2.0:assertion` |

## Python Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| `requests` | >=2.28 | Okta API communication |
| `xml.etree.ElementTree` | stdlib | SAML metadata parsing |
| `ssl` | stdlib | Certificate expiry checking |

## References

- Okta SAML Docs: https://developer.okta.com/docs/concepts/saml/
- Okta API: https://developer.okta.com/docs/reference/api/apps/
- OWASP SAML Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/SAML_Security_Cheat_Sheet.html

---

## Standards and Controls

## SAML 2.0 Standards
- **OASIS SAML 2.0 Core**: Defines assertions, protocols, bindings, and profiles
  - http://docs.oasis-open.org/security/saml/v2.0/saml-core-2.0-os.pdf
- **SAML 2.0 Bindings**: HTTP Redirect, HTTP POST, HTTP Artifact, SOAP
  - http://docs.oasis-open.org/security/saml/v2.0/saml-bindings-2.0-os.pdf
- **SAML 2.0 Profiles**: Web Browser SSO Profile, Single Logout Profile
  - http://docs.oasis-open.org/security/saml/v2.0/saml-profiles-2.0-os.pdf

## NIST Standards
- **NIST SP 800-63B**: Digital Identity Guidelines - Authentication and Lifecycle Management
  - https://pages.nist.gov/800-63-3/sp800-63b.html
- **NIST SP 800-53 Rev 5**: Security and Privacy Controls
  - IA-2: Identification and Authentication (Organizational Users)
  - IA-8: Identification and Authentication (Non-Organizational Users)
  - AC-3: Access Enforcement
  - AU-3: Content of Audit Records
  - SC-23: Session Authenticity
- **NIST SP 1800-35**: Implementing a Zero Trust Architecture
  - https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1800-35.pdf

## Okta Documentation
- **Okta SAML Integration Guide**: https://developer.okta.com/docs/guides/build-sso-integration/saml2/main/
- **Understanding SAML with Okta**: https://developer.okta.com/docs/concepts/saml/
- **Okta SAML App Configuration**: https://help.okta.com/en-us/content/topics/apps/apps-about-saml.htm

## Security Best Practices
- **OWASP SAML Security Cheat Sheet**: Covers SAML signature wrapping attacks, XML injection
- **SSO Best Practices 2025**: SHA-256 enforcement, assertion encryption, certificate rotation
  - https://clerk.com/articles/sso-best-practices-for-secure-scalable-logins

## XML Security Standards
- **XML Signature (XMLDSig)**: W3C standard for XML digital signatures
- **XML Encryption**: W3C standard for encrypting XML content
- **XML Canonicalization (C14N)**: Required for consistent signature verification

## Compliance Frameworks
- **SOC 2 Type II**: Logical access controls through SSO
- **ISO 27001**: A.9.4.2 Secure log-on procedures
- **PCI DSS 4.0**: Requirement 8 - Identify Users and Authenticate Access

---

## Workflows

## Workflow 1: SP-Initiated SSO Flow

```
User -> Service Provider -> Okta IdP -> User Authenticates -> Okta -> Service Provider -> User
```

### Detailed Steps:
1. User accesses protected resource on Service Provider
2. SP checks for existing session - none found
3. SP generates SAML AuthnRequest with:
   - Issuer (SP Entity ID)
   - AssertionConsumerServiceURL
   - NameIDPolicy (email format)
   - RequestID (for InResponseTo validation)
4. SP redirects user to Okta SSO URL with base64-encoded AuthnRequest
5. Okta authenticates user (credentials, MFA if configured)
6. Okta generates SAML Response containing:
   - Signed assertion with SHA-256
   - Subject NameID (user identifier)
   - Conditions (NotBefore, NotOnOrAfter, AudienceRestriction)
   - AuthnStatement (authentication context)
   - AttributeStatement (mapped user attributes)
7. Okta POSTs SAML Response to SP ACS URL
8. SP validates SAML Response:
   - Verify XML signature against Okta certificate
   - Check InResponseTo matches original request ID
   - Validate time conditions (with clock skew tolerance)
   - Verify audience restriction matches SP Entity ID
   - Check authentication context class
9. SP extracts user identity and attributes
10. SP creates local session and grants access

## Workflow 2: IdP-Initiated SSO Flow

### Steps:
1. User logs into Okta dashboard
2. User clicks on application tile
3. Okta generates unsolicited SAML Response (no InResponseTo)
4. Okta POSTs to SP ACS URL
5. SP validates assertion (no InResponseTo check)
6. SP creates session

### Security Note:
IdP-initiated SSO is less secure because it cannot validate InResponseTo, making it more susceptible to replay attacks. Use SP-initiated flow when possible.

## Workflow 3: Certificate Rotation

### Steps:
1. Generate new X.509 certificate in Okta (Admin > Settings > Security)
2. Download new certificate (do not yet set as active)
3. Install new certificate on SP alongside existing certificate
4. Configure SP to accept assertions signed with either certificate
5. Activate new certificate in Okta
6. Monitor for authentication failures
7. After validation period, remove old certificate from SP
8. Update SAML metadata on both sides

### Timeline:
- Day 0: Generate new certificate and distribute to SP team
- Day 1-7: SP installs new certificate (dual-cert mode)
- Day 8: Activate new certificate in Okta
- Day 8-14: Monitor authentication logs for failures
- Day 15: Remove old certificate from SP

## Workflow 4: Single Logout (SLO)

### Steps:
1. User initiates logout at SP
2. SP generates SAML LogoutRequest
3. SP sends LogoutRequest to Okta SLO endpoint
4. Okta terminates IdP session
5. Okta sends LogoutRequest to all other SPs in session
6. Each SP terminates local session
7. Okta sends LogoutResponse to initiating SP
8. SP confirms logout to user

## Workflow 5: Troubleshooting Authentication Failures

### Diagnostic Steps:
1. Install SAML Tracer browser extension
2. Reproduce the failed SSO attempt
3. Capture the SAML AuthnRequest and Response
4. Check for common issues:
   - **Signature Invalid**: Certificate mismatch or SHA-1 vs SHA-256
   - **Audience Mismatch**: SP Entity ID doesn't match Okta config
   - **Time Condition Failed**: Clock skew > configured tolerance
   - **NameID Format Mismatch**: SP expects different format
   - **Missing Attributes**: Attribute mapping not configured
5. Review Okta System Log for error details
6. Verify SP metadata matches Okta configuration

---

## Working Template

## Project Information
| Field | Value |
|-------|-------|
| Service Provider | [Application Name] |
| Identity Provider | Okta |
| Implementation Lead | [Name] |
| Target Go-Live Date | [Date] |
| Environment | [ ] Development [ ] Staging [ ] Production |

## Pre-Implementation Checklist

### IdP (Okta) Configuration
- [ ] Okta organization provisioned and accessible
- [ ] Administrative access to Okta confirmed
- [ ] Okta MFA enabled for admin accounts
- [ ] Application created in Okta (SAML 2.0)
- [ ] SSO URL configured: `____________________________`
- [ ] Audience URI (SP Entity ID) set: `____________________________`
- [ ] Name ID Format selected: [ ] Email [ ] Persistent [ ] Transient
- [ ] Attribute statements configured:
  - [ ] email -> `user.email`
  - [ ] firstName -> `user.firstName`
  - [ ] lastName -> `user.lastName`
  - [ ] groups -> (group attribute filter)
- [ ] Signature algorithm set to SHA-256
- [ ] Response signed: [ ] Yes [ ] No
- [ ] Assertion signed: [ ] Yes [ ] No
- [ ] Assertion encryption enabled: [ ] Yes [ ] No
- [ ] Users/Groups assigned to application

### SP Configuration
- [ ] SP SAML library installed and configured
- [ ] ACS URL endpoint implemented: `____________________________`
- [ ] SP Entity ID configured: `____________________________`
- [ ] IdP metadata imported (certificate, SSO URL, Entity ID)
- [ ] Signature validation implemented (SHA-256)
- [ ] InResponseTo validation enabled
- [ ] Audience restriction validation enabled
- [ ] Time condition validation with clock skew tolerance
- [ ] Session creation after successful assertion
- [ ] Error handling for failed assertions

### Security Configuration
- [ ] All endpoints use HTTPS
- [ ] SHA-256 enforced (SHA-1 rejected)
- [ ] Assertion encryption with AES-256-CBC
- [ ] Certificate pinning or strong validation
- [ ] CSRF protection on ACS endpoint
- [ ] Rate limiting on authentication endpoints
- [ ] Session timeout configured: ____ minutes
- [ ] Idle timeout configured: ____ minutes
- [ ] Single Logout (SLO) endpoint configured

## Certificate Management

### Current Certificate
| Field | Value |
|-------|-------|
| Issuer | |
| Subject | |
| Serial Number | |
| Valid From | |
| Valid To | |
| SHA-256 Fingerprint | |
| Algorithm | |

### Certificate Rotation Schedule
| Date | Action | Status |
|------|--------|--------|
| | Generate new certificate in Okta | [ ] Done |
| | Distribute new certificate to SP team | [ ] Done |
| | Install new certificate on SP (dual-cert) | [ ] Done |
| | Activate new certificate on Okta | [ ] Done |
| | Monitor for authentication failures | [ ] Done |
| | Remove old certificate from SP | [ ] Done |

## Testing Checklist

### SP-Initiated SSO
- [ ] User redirected to Okta login page
- [ ] Successful authentication creates SP session
- [ ] User attributes correctly mapped
- [ ] Group memberships correctly populated
- [ ] Invalid credentials properly rejected
- [ ] MFA prompt appears when configured

### IdP-Initiated SSO
- [ ] Login from Okta dashboard tile works
- [ ] Session created correctly on SP
- [ ] Deep links preserved after authentication

### Single Logout
- [ ] SP-initiated logout terminates IdP session
- [ ] IdP-initiated logout terminates SP session
- [ ] All session cookies properly cleared

### Error Scenarios
- [ ] Expired assertion rejected
- [ ] Invalid signature rejected
- [ ] Wrong audience URI rejected
- [ ] Replay attack prevented (InResponseTo)
- [ ] Clock skew beyond tolerance rejected

## Post-Implementation

### Monitoring
- [ ] Authentication success/failure alerts configured
- [ ] Certificate expiration monitoring (30-day warning)
- [ ] Okta System Log integration with SIEM
- [ ] SP authentication logs forwarded to SIEM
- [ ] Dashboard for SSO health metrics

### Documentation
- [ ] Architecture diagram updated
- [ ] Runbook for SSO troubleshooting created
- [ ] Certificate rotation procedure documented
- [ ] Break-glass access procedure documented
- [ ] User communication sent

## Sign-Off
| Role | Name | Date | Signature |
|------|------|------|-----------|
| Security Lead | | | |
| Application Owner | | | |
| IAM Team Lead | | | |
| Change Manager | | | |
