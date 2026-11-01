# Configuring Oauth2 Authorization Flow

## API Reference

## Libraries

| Library | Install | Purpose |
|---------|---------|---------|
| requests | `pip install requests` | HTTP client for OAuth endpoints |
| authlib | `pip install authlib` | Full OAuth 2.0 / OIDC client library |
| PyJWT | `pip install PyJWT[crypto]` | JWT token validation and inspection |

## OIDC Discovery Endpoint

```
GET {issuer}/.well-known/openid-configuration
```

Returns: authorization_endpoint, token_endpoint, jwks_uri, supported grant types, scopes.

## OAuth 2.0 Grant Types

| Grant Type | Use Case | Security |
|------------|----------|----------|
| authorization_code | Server-side apps | Recommended with PKCE |
| client_credentials | Machine-to-machine | Service accounts only |
| implicit | (DEPRECATED) SPAs | Avoid — tokens in URL fragment |
| password | (DEPRECATED) Legacy | Avoid — credentials exposed to client |
| urn:ietf:params:oauth:grant-type:device_code | IoT/CLI | Approved for limited-input devices |

## Security Best Practices

| Practice | RFC |
|----------|-----|
| PKCE (Proof Key for Code Exchange) | RFC 7636 |
| Token Binding | RFC 8471 |
| DPoP (Demonstrating Proof of Possession) | RFC 9449 |
| Sender-Constrained Tokens | OAuth 2.0 Security BCP |

## External References

- [RFC 6749 OAuth 2.0](https://datatracker.ietf.org/doc/html/rfc6749)
- [RFC 7636 PKCE](https://datatracker.ietf.org/doc/html/rfc7636)
- [OAuth 2.0 Security BCP](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics)
- [authlib Documentation](https://docs.authlib.org/)

---

## Standards and Controls

## Core OAuth Standards
- **RFC 6749**: The OAuth 2.0 Authorization Framework
  - https://datatracker.ietf.org/doc/html/rfc6749
- **RFC 6750**: The OAuth 2.0 Authorization Framework: Bearer Token Usage
  - https://datatracker.ietf.org/doc/html/rfc6750
- **RFC 7636**: Proof Key for Code Exchange (PKCE)
  - https://datatracker.ietf.org/doc/html/rfc7636
- **RFC 9700**: OAuth 2.0 Security Best Current Practice
  - https://datatracker.ietf.org/doc/html/rfc9700
- **OAuth 2.1 Draft**: Consolidation of OAuth 2.0 with PKCE mandatory
  - https://oauth.net/2.1/

## Token Standards
- **RFC 7519**: JSON Web Token (JWT)
  - https://datatracker.ietf.org/doc/html/rfc7519
- **RFC 7515**: JSON Web Signature (JWS)
  - https://datatracker.ietf.org/doc/html/rfc7515
- **RFC 9449**: OAuth 2.0 Demonstrating Proof of Possession (DPoP)
  - https://datatracker.ietf.org/doc/html/rfc9449
- **RFC 7009**: OAuth 2.0 Token Revocation
  - https://datatracker.ietf.org/doc/html/rfc7009

## OpenID Connect
- **OpenID Connect Core 1.0**: Authentication layer on OAuth 2.0
  - https://openid.net/specs/openid-connect-core-1_0.html
- **OpenID Connect Discovery**: Provider metadata discovery
  - https://openid.net/specs/openid-connect-discovery-1_0.html

## Additional Grant Types
- **RFC 8628**: OAuth 2.0 Device Authorization Grant
  - https://datatracker.ietf.org/doc/html/rfc8628

## NIST Standards
- **NIST SP 800-63B**: Digital Identity Guidelines - Authentication
- **NIST SP 800-53 Rev 5**:
  - AC-3: Access Enforcement
  - IA-5: Authenticator Management
  - SC-13: Cryptographic Protection
  - SC-23: Session Authenticity
  - AU-3: Content of Audit Records

## Implementation Guides
- **Auth0 PKCE Guide**: https://auth0.com/docs/get-started/authentication-and-authorization-flow/authorization-code-flow-with-pkce
- **Microsoft OIDC Flow**: https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow
- **Okta OAuth Express**: https://developer.okta.com/blog/2025/07/28/express-oauth-pkce
- **PKCE Explained**: https://oauth.net/2/pkce/

## Security References
- **OWASP OAuth 2.0 Security**: Common vulnerabilities and mitigations
- **OAuth Security Workshop**: Annual research on OAuth attack vectors

---

## Workflows

## Workflow 1: Authorization Code Flow with PKCE

```
Client                     Auth Server              Resource Server
  |                            |                         |
  |-- Generate code_verifier --|                         |
  |-- Compute code_challenge --|                         |
  |                            |                         |
  |--- AuthZ Request --------->|                         |
  |  (code_challenge, state)   |                         |
  |                            |-- User Authenticates -->|
  |                            |<- User Consents --------|
  |<-- AuthZ Code + state -----|                         |
  |                            |                         |
  |--- Token Request --------->|                         |
  |  (code + code_verifier)    |                         |
  |<-- Access + Refresh Token--|                         |
  |                            |                         |
  |--- API Request (Bearer) ---|------------------------>|
  |<-- API Response ---------- |<------------------------|
```

### Step-by-Step:
1. Client generates `code_verifier`: random 43-128 char string (A-Z, a-z, 0-9, -._~)
2. Client computes `code_challenge = BASE64URL(SHA256(code_verifier))`
3. Client redirects to: `GET /authorize?response_type=code&client_id=xxx&redirect_uri=xxx&scope=xxx&state=RANDOM&code_challenge=xxx&code_challenge_method=S256`
4. User authenticates and consents at authorization server
5. Server redirects to: `redirect_uri?code=AUTH_CODE&state=RANDOM`
6. Client validates state matches original
7. Client exchanges code: `POST /token` with `grant_type=authorization_code&code=AUTH_CODE&code_verifier=xxx&redirect_uri=xxx`
8. Server validates SHA256(code_verifier) matches stored code_challenge
9. Server returns access_token, refresh_token, id_token (if OIDC)

## Workflow 2: Client Credentials Flow (Machine-to-Machine)

```
Service A                  Auth Server              Service B (API)
  |                            |                         |
  |--- Token Request --------->|                         |
  |  (client_id, secret, scope)|                         |
  |<-- Access Token -----------|                         |
  |                            |                         |
  |--- API Request (Bearer) ---|------------------------>|
  |<-- API Response ---------- |<------------------------|
```

### Step-by-Step:
1. Service registers with auth server (client_id + client_secret)
2. Service requests token: `POST /token` with `grant_type=client_credentials&scope=api:read`
3. Auth server validates client credentials
4. Auth server returns access_token (no refresh token, no user context)
5. Service calls API with `Authorization: Bearer ACCESS_TOKEN`

## Workflow 3: Token Refresh with Rotation

```
Client                     Auth Server
  |                            |
  |--- Refresh Request ------->|
  |  (refresh_token_v1)        |
  |<-- New Access Token -------|
  |<-- New Refresh Token (v2) -|
  |  (v1 invalidated)          |
  |                            |
  |--- Refresh Request ------->|
  |  (refresh_token_v2)        |
  |<-- New Access Token -------|
  |<-- New Refresh Token (v3) -|
  |                            |
  |--- THEFT: Reuse v1 ------->|
  |  (DETECTED: v1 reused)     |
  |<-- REVOKE ALL TOKENS ------|
```

### Rotation Detection:
- Each refresh token is single-use
- On reuse of an old refresh token, server detects theft
- All tokens in the grant chain are revoked
- User must re-authenticate

## Workflow 4: Device Authorization Grant

```
Device                     Auth Server              User (Browser)
  |                            |                         |
  |--- Device AuthZ Request -->|                         |
  |<-- device_code,            |                         |
  |    user_code,              |                         |
  |    verification_uri -------|                         |
  |                            |                         |
  |-- Display user_code ------>|                         |
  |   to user on screen        |                         |
  |                            |<-- User visits URI -----|
  |                            |<-- Enters user_code ----|
  |                            |<-- Authenticates -------|
  |                            |<-- Consents ------------|
  |                            |                         |
  |--- Poll Token Endpoint --->|                         |
  |  (device_code)             |                         |
  |<-- Access Token -----------|                         |
```

## Workflow 5: Token Revocation

### Steps:
1. Client sends revocation request: `POST /revoke` with `token=xxx&token_type_hint=refresh_token`
2. Auth server invalidates the token
3. If refresh token revoked, all associated access tokens also invalidated
4. Server returns 200 OK regardless of whether token was valid (prevents token fishing)

## Workflow 6: Security Incident - Token Compromise Response

### Steps:
1. Detect suspicious token usage (unusual IP, impossible travel)
2. Immediately revoke the compromised token via revocation endpoint
3. If refresh token compromised, revoke entire token family
4. Force re-authentication for affected user
5. Audit all API calls made with compromised token
6. Check for scope escalation attempts
7. Review authorization logs for the compromised session
8. Notify affected user and security team

---

## Working Template

## Application Registration
| Field | Value |
|-------|-------|
| Application Name | |
| Client ID | |
| Client Type | [ ] Public [ ] Confidential |
| Grant Types | [ ] Authorization Code [ ] Client Credentials [ ] Refresh Token [ ] Device Code |
| PKCE Required | [ ] Yes (mandatory for OAuth 2.1) |

## Redirect URI Configuration
| Environment | URI | Status |
|-------------|-----|--------|
| Development | http://localhost:3000/callback | [ ] Registered |
| Staging | https://staging.example.com/callback | [ ] Registered |
| Production | https://app.example.com/callback | [ ] Registered |

**Rules:**
- Exact match only - no wildcards
- HTTPS required for non-localhost URIs
- Each URI must be explicitly registered

## Scope Design
| Scope | Description | Sensitivity |
|-------|-------------|-------------|
| openid | OpenID Connect identity | Low |
| profile | User profile information | Low |
| email | User email address | Low |
| read:users | Read user records | Medium |
| write:users | Modify user records | High |
| admin:settings | Modify system settings | Critical |

## Token Configuration
| Parameter | Value | Justification |
|-----------|-------|---------------|
| Access Token Lifetime | 15 minutes | Minimize window of exposure |
| Refresh Token Lifetime | 8 hours | Align with business hours |
| Refresh Token Rotation | Enabled | Detect token theft via reuse |
| Refresh Token Absolute Expiry | 24 hours | Force re-authentication daily |
| ID Token Lifetime | 5 minutes | Only used for initial authentication |
| Token Format | JWT (signed) | Enable stateless validation |
| Signing Algorithm | RS256 | Asymmetric verification |

## Security Checklist
- [ ] PKCE enforced for all authorization code flows
- [ ] Implicit grant disabled
- [ ] ROPC (password) grant disabled
- [ ] State parameter validated
- [ ] Exact redirect URI matching enforced
- [ ] Refresh token rotation enabled
- [ ] Token revocation endpoint active
- [ ] DPoP enabled for high-security APIs
- [ ] Consent screen configured for sensitive scopes
- [ ] Token introspection secured with authentication

## Client Authentication Methods
| Method | Use Case | Security Level |
|--------|----------|---------------|
| none | Public clients (SPA, mobile) | Requires PKCE |
| client_secret_basic | Server-side web apps | Medium |
| client_secret_post | Server-side web apps | Medium |
| private_key_jwt | High-security services | High |
| tls_client_auth | mTLS-capable services | High |

## Monitoring & Alerting
- [ ] Token issuance rate monitoring
- [ ] Failed authentication attempts tracking
- [ ] Refresh token reuse detection alerts
- [ ] Scope escalation attempt alerts
- [ ] Unusual client_id activity monitoring
- [ ] Geographic anomaly detection for token usage
