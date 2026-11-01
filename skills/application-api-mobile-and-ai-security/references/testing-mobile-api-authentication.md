# Testing Mobile API Authentication

## API Reference

## Common Mobile Auth Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| /api/v1/login | POST | Username/password authentication |
| /api/v1/register | POST | New account creation |
| /api/v1/token | POST | OAuth token exchange |
| /api/v1/refresh | POST | Token refresh flow |
| /api/v1/logout | POST | Session termination |
| /api/v1/verify-otp | POST | MFA code verification |
| /api/v1/me | GET | Current user profile |

## Mobile-Specific JWT Claims

| Claim | Purpose | Security Impact |
|-------|---------|-----------------|
| device_id / did | Bind token to device | Prevents token theft across devices |
| platform | iOS/Android identifier | Enables platform-specific policy |
| app_version | Client version tracking | Version-gated feature access |
| exp | Token expiration | Missing = permanent access |

## Test Categories

| Test | Severity | Description |
|------|----------|-------------|
| No auth access | Critical | Endpoints accessible without token |
| IDOR | Critical | Access other users' resources |
| Weak JWT secret | Critical | Brute-force HMAC signing key |
| Token reuse after logout | High | Token valid after logout |
| No rate limiting | High | Unlimited login attempts |
| Missing device binding | Medium | Token works on any device |

## Python Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| `requests` | >=2.28 | HTTP API testing |
| `base64` | stdlib | JWT decoding |
| `hmac` | stdlib | HMAC signature verification |
| `hashlib` | stdlib | Hash functions for JWT |

## References

- OWASP Mobile Top 10: https://owasp.org/www-project-mobile-top-10/
- OWASP API Security Top 10: https://owasp.org/API-Security/
- MASVS Authentication: https://mas.owasp.org/MASVS/05-MASVS-AUTH/

---

## Standards and Controls

## OWASP Mobile Top 10 2024

| OWASP ID | Risk | Testing Focus |
|----------|------|---------------|
| M1 | Improper Credential Usage | Hardcoded API keys, credential transmission |
| M3 | Insecure Authentication/Authorization | Auth bypass, IDOR, privilege escalation |

## OWASP API Security Top 10 2023

| API Risk | Test Case |
|----------|-----------|
| API1: Broken Object Level Authorization | Modify object IDs, test cross-user access |
| API2: Broken Authentication | JWT vulnerabilities, token replay, session management |
| API3: Broken Object Property Level Auth | Mass assignment, property-level access |
| API5: Broken Function Level Authorization | Admin endpoint access with user tokens |

## OWASP MASVS v2.0 - MASVS-AUTH

| Control | Test Method |
|---------|-------------|
| MASVS-AUTH-1 | Verify authentication enforcement on all sensitive endpoints |
| MASVS-AUTH-2 | Test token generation, validation, and revocation |
| MASVS-AUTH-3 | Assess multi-factor authentication implementation |

## CWE Mappings

| CWE | Title | Test |
|-----|-------|------|
| CWE-287 | Improper Authentication | Missing auth on endpoints |
| CWE-639 | Authorization Bypass Through User-Controlled Key | IDOR testing |
| CWE-798 | Hardcoded Credentials | API key in APK/IPA |
| CWE-613 | Insufficient Session Expiration | Token lifetime testing |
| CWE-384 | Session Fixation | Pre-auth token reuse |

---

## Workflows

## Workflow 1: Authentication Assessment

```
[Intercept traffic] --> [Map auth endpoints] --> [Analyze token format]
                                                        |
                                          +-------------+-------------+
                                          |             |             |
                                    [JWT analysis] [OAuth flow]  [Session mgmt]
                                    [None alg]     [PKCE check]  [Expiration]
                                    [Key brute]    [Redirect URI] [Logout invalidation]
                                          |             |             |
                                          +-------------+-------------+
                                                        |
                                                 [IDOR testing]
                                                 [Privilege escalation]
                                                 [Report findings]
```

## Decision Matrix: Token Vulnerability Testing

| Token Type | Primary Tests | Tools |
|-----------|--------------|-------|
| JWT (HS256) | Key brute force, none algorithm, claim manipulation | jwt_tool, hashcat |
| JWT (RS256) | Algorithm confusion, public key retrieval, key ID manipulation | jwt_tool |
| Opaque | Entropy analysis, predictability, server-side invalidation | Burp Sequencer |
| OAuth Bearer | Scope escalation, redirect URI manipulation, PKCE enforcement | Burp, Postman |

---

## Working Template

## Target
| Field | Value |
|-------|-------|
| API Base URL | [URL] |
| Application | [APP_NAME] |
| Token Type | [JWT/OAuth/Opaque] |
| Test Date | [DATE] |

## JWT/Token Analysis
| Check | Result | Severity |
|-------|--------|----------|
| Algorithm | [ALG] | [SEVERITY] |
| Expiration | [DURATION] | [SEVERITY] |
| Sensitive Claims | [YES/NO] | [SEVERITY] |
| Signing Key Strength | [WEAK/STRONG] | [SEVERITY] |

## Authentication Tests
| Test | Endpoint | Result | Severity |
|------|----------|--------|----------|
| Missing Auth | [ENDPOINT] | [PASS/FAIL] | [SEVERITY] |
| Expired Token | [ENDPOINT] | [PASS/FAIL] | [SEVERITY] |
| Empty Token | [ENDPOINT] | [PASS/FAIL] | [SEVERITY] |

## Authorization Tests (IDOR)
| Endpoint | Own ID | Other ID | Accessible | Severity |
|----------|--------|----------|-----------|----------|
| [ENDPOINT] | [ID] | [ID] | [YES/NO] | [SEVERITY] |

## Recommendations
1. [RECOMMENDATION]
