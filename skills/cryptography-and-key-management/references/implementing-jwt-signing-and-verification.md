# Implementing JWT Signing And Verification

## API Reference

## PyJWT Library

```python
import jwt
# Sign with HS256
token = jwt.encode({"sub": "user1", "exp": time.time() + 3600}, "secret", algorithm="HS256")
# Verify
payload = jwt.decode(token, "secret", algorithms=["HS256"])
# Sign with RS256
token = jwt.encode(payload, private_key, algorithm="RS256")
payload = jwt.decode(token, public_key, algorithms=["RS256"])
```

## JWT Algorithms

| Algorithm | Type | Key Size | Use Case |
|-----------|------|----------|----------|
| HS256 | HMAC | 256-bit secret | Internal services |
| RS256 | RSA | 2048+ bit | Public verification |
| ES256 | ECDSA | P-256 curve | Compact tokens |
| EdDSA | Ed25519 | 256-bit | High performance |
| none | - | - | NEVER use in production |

## Standard JWT Claims (RFC 7519)

| Claim | Type | Description |
|-------|------|-------------|
| `iss` | String | Issuer |
| `sub` | String | Subject |
| `aud` | String/Array | Audience |
| `exp` | NumericDate | Expiration time |
| `nbf` | NumericDate | Not before |
| `iat` | NumericDate | Issued at |
| `jti` | String | JWT ID (unique) |

## Common JWT Attacks

| Attack | Description | Mitigation |
|--------|-------------|-----------|
| Algorithm confusion | Switch RS256 to HS256 | Explicit algorithm allowlist |
| none algorithm | Remove signature | Reject alg=none |
| JKU/JWK injection | Inject attacker key | Ignore JKU/JWK headers |
| Token replay | Reuse valid token | Use jti + short exp |

### References

- RFC 7519 (JWT): https://datatracker.ietf.org/doc/html/rfc7519
- PyJWT: https://pyjwt.readthedocs.io/
- jose (JavaScript): https://github.com/panva/jose
- JWT.io Debugger: https://jwt.io/

---

## Standards and Controls

## Primary Standards

### RFC 7519 - JSON Web Token (JWT)
- **URL**: https://www.rfc-editor.org/rfc/rfc7519
- **Description**: JWT format and claims specification

### RFC 7515 - JSON Web Signature (JWS)
- **URL**: https://www.rfc-editor.org/rfc/rfc7515
- **Description**: Signature mechanism for JWTs

### RFC 7517 - JSON Web Key (JWK)
- **URL**: https://www.rfc-editor.org/rfc/rfc7517
- **Description**: Key format for JWT signing keys

### RFC 7518 - JSON Web Algorithms (JWA)
- **URL**: https://www.rfc-editor.org/rfc/rfc7518
- **Description**: Cryptographic algorithms for JWS/JWE

### RFC 8725 - JWT Best Current Practices
- **URL**: https://www.rfc-editor.org/rfc/rfc8725
- **Description**: Security best practices for JWT implementations

## OWASP References

### OWASP JWT Cheat Sheet
- **URL**: https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html

## Python Libraries

### PyJWT
- **URL**: https://pyjwt.readthedocs.io/
- **PyPI**: https://pypi.org/project/PyJWT/

### python-jose
- **URL**: https://python-jose.readthedocs.io/
- **PyPI**: https://pypi.org/project/python-jose/

---

## Workflows

## Workflow 1: Token Issuance

```
[Authentication Request] (username + password)
      |
[Validate Credentials]
      |
[Build JWT Claims]:
  - sub: user ID
  - iss: issuer URL
  - aud: audience
  - exp: expiration (now + 15 min)
  - iat: issued at
  - jti: unique token ID
      |
[Sign with Private Key / Secret]
(RS256 / ES256 / HS256)
      |
[Return: access_token + refresh_token]
```

## Workflow 2: Token Verification

```
[Incoming Request with Bearer Token]
      |
[Extract Token from Authorization Header]
      |
[Decode Header (without verification)]
[Check alg against allowlist]
      |
[Verify Signature]
(using public key / shared secret)
      |
[Validate Claims]:
  - exp: not expired
  - nbf: not before current time
  - iss: expected issuer
  - aud: expected audience
      |
[Accept / Reject Request]
```

## Workflow 3: Key Rotation

```
[Generate New Signing Key]
      |
[Add to JWK Set with unique kid]
      |
[Update /.well-known/jwks.json]
(new key + old key)
      |
[New tokens signed with new key]
[Old tokens still verify with old key]
      |
[After grace period: remove old key]
```

---

## Working Template

## Algorithm Selection Guide

| Use Case | Recommended Algorithm | Reason |
|----------|----------------------|--------|
| Single server | HS256 | Simple, fast, shared secret |
| Microservices | RS256 / ES256 | Asymmetric, verify without secret |
| Mobile/IoT | ES256 | Small key/signature size |
| High performance | EdDSA | Fastest asymmetric signing |

## JWT Claims Checklist

- [ ] `sub` - Subject (user ID)
- [ ] `iss` - Issuer (your app identifier)
- [ ] `aud` - Audience (intended recipient)
- [ ] `exp` - Expiration (short-lived: 15 min access, 7 day refresh)
- [ ] `nbf` - Not before (prevents premature use)
- [ ] `iat` - Issued at (token creation time)
- [ ] `jti` - JWT ID (unique, for revocation)

## Security Checklist

- [ ] Algorithm allowlist enforced (never accept unknown alg)
- [ ] `alg: none` explicitly rejected
- [ ] Short expiration (access: 15 min, refresh: 7 days)
- [ ] Issuer and audience validation enabled
- [ ] Secrets >= 256 bits for HMAC algorithms
- [ ] RSA keys >= 2048 bits
- [ ] Tokens stored securely on client (httpOnly cookies preferred)
- [ ] Token refresh mechanism implemented
- [ ] Token revocation mechanism available (blacklist/JTI check)
