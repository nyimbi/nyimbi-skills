# Implementing Passwordless Authentication With Fido2

## API Reference

## WebAuthn Registration Flow

```javascript
// 1. Server generates challenge
const options = await navigator.credentials.create({
  publicKey: {
    challenge: new Uint8Array(32),
    rp: { name: "Example Corp", id: "example.com" },
    user: { id: userId, name: "user@example.com", displayName: "User" },
    pubKeyCredParams: [
      { type: "public-key", alg: -7 },   // ES256
      { type: "public-key", alg: -257 }, // RS256
    ],
    authenticatorSelection: {
      authenticatorAttachment: "platform",  // or "cross-platform"
      residentKey: "required",              // for passkeys
      userVerification: "required",
    },
    attestation: "direct",
  }
});
```

## WebAuthn Authentication Flow

```javascript
const assertion = await navigator.credentials.get({
  publicKey: {
    challenge: serverChallenge,
    rpId: "example.com",
    allowCredentials: [],  // empty for discoverable credentials (passkeys)
    userVerification: "required",
  }
});
```

## python-fido2 Server Library

```python
from fido2.server import Fido2Server
from fido2.webauthn import PublicKeyCredentialRpEntity

rp = PublicKeyCredentialRpEntity(id="example.com", name="Example")
server = Fido2Server(rp)

# Registration
registration_data, state = server.register_begin(user, credentials)
auth_data = server.register_complete(state, response)

# Authentication
request_data, state = server.authenticate_begin(credentials)
server.authenticate_complete(state, credentials, credential_id, client_data, auth_data, signature)
```

## FIDO2 Authenticator Types

| Type | Example | Attachment | Passkey Support |
|------|---------|------------|-----------------|
| Platform | Windows Hello, Touch ID | platform | Yes |
| Roaming | YubiKey, Titan Key | cross-platform | Yes (FIDO2) |
| Software | 1Password, iCloud Keychain | platform | Yes |

## COSE Algorithm Identifiers

| COSE ID | Algorithm | Use |
|---------|-----------|-----|
| -7 | ES256 (P-256) | Preferred for FIDO2 |
| -257 | RS256 | Legacy compatibility |
| -8 | EdDSA (Ed25519) | Strong, compact |
| -35 | ES384 (P-384) | Higher security |

## NIST SP 800-63B AAL Levels

| Level | Requirements | FIDO2 Mapping |
|-------|-------------|---------------|
| AAL1 | Single factor | Not applicable |
| AAL2 | Two factors | FIDO2 + PIN/biometric |
| AAL3 | Hardware crypto + verifier impersonation resistance | FIDO2 hardware key |

## Azure AD FIDO2 Configuration

```powershell
# Enable FIDO2 in Azure AD
Set-MgBetaPolicyAuthenticationMethodPolicyAuthenticationMethodConfiguration `
  -AuthenticationMethodConfigurationId "fido2" `
  -State "enabled" `
  -AdditionalProperties @{
    isSelfServiceRegistrationAllowed = $true
    isAttestationEnforced = $true
  }
```

### References

- WebAuthn Spec: https://www.w3.org/TR/webauthn-3/
- FIDO Alliance: https://fidoalliance.org/specifications/
- NIST SP 800-63B: https://pages.nist.gov/800-63-3/sp800-63b.html
- python-fido2: https://github.com/Yubico/python-fido2

---

## Standards and Controls

## FIDO Standards
- **FIDO2 Specification**: https://fidoalliance.org/specifications/
- **WebAuthn Level 2**: W3C Web Authentication API
- **CTAP2**: Client to Authenticator Protocol 2.0

## NIST Standards
- **NIST SP 800-63B**: AAL3 - Hardware-based phishing-resistant authenticator
- **NIST SP 800-53 Rev 5**: IA-2(6), IA-2(8) Replay-resistant authentication
- **NIST SP 800-157**: PIV Derived Credentials

## CISA Guidance
- **Phishing-Resistant MFA**: Required for federal agencies under EO 14028
- **OMB M-22-09**: Federal zero trust strategy requiring phishing-resistant MFA

## Vendor Resources
- **Yubico FIDO2**: https://www.yubico.com/authentication-standards/fido2/
- **Microsoft Passkeys**: https://www.microsoft.com/en-us/security/business/security-101/what-is-fido2
- **Google Passkeys**: Android and Chrome WebAuthn support

---

## Workflows

## Workflow 1: Security Key Enrollment
1. User receives FIDO2 security key (YubiKey, Titan Key)
2. User navigates to enrollment portal
3. System generates WebAuthn registration challenge
4. Browser prompts user to insert/tap security key
5. User verifies with PIN or biometric on key
6. Key generates unique public/private key pair
7. Public key registered with relying party
8. User tests authentication with enrolled key

## Workflow 2: Passkey Authentication Flow
1. User visits login page, enters username
2. Server sends WebAuthn authentication challenge
3. Browser prompts for authenticator (key, biometric, passkey)
4. User verifies identity (touch key, scan fingerprint, enter PIN)
5. Authenticator signs challenge with private key
6. Server validates signature with stored public key
7. User authenticated, session created

## Workflow 3: Migration from Passwords to Passwordless
1. Phase 1: Deploy FIDO2 to pilot group (IT, security teams)
2. Phase 2: Enable coexistence (password + FIDO2)
3. Phase 3: Expand FIDO2 enrollment to all users
4. Phase 4: Set FIDO2-only policy per group
5. Phase 5: Disable password authentication for migrated groups
6. Phase 6: Monitor for fallback authentication attempts

## Workflow 4: Lost/Stolen Key Recovery
1. User reports lost security key
2. Admin disables lost key in identity provider
3. User authenticates via backup method (recovery codes, backup key)
4. User enrolls replacement security key
5. Old key permanently revoked
6. Security team reviews for unauthorized usage of lost key
