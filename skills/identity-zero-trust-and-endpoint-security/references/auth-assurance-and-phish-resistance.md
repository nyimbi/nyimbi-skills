# Authentication assurance and phish-resistance — the MFA decision

Map every authentication method to an assurance level, then let conditional
access require the level the resource actually needs. This is the single most
common identity design error: strong methods deployed, but policies still
satisfied by SMS OTP.

## Assurance mapping (NIST SP 800-63B)

| Method | AAL | Phish-resistant | Notes |
|---|---|---|---|
| Password + SMS/OTP push | AAL1–2 | No | Phishable, SIM-swap prone; acceptable only for low-risk resources |
| Password + authenticator app (TOTP) | AAL2 | No | Better than SMS; still relays to a fake site |
| Password + device-bound push with number matching | AAL2 | Partial | Stops bulk push fatigue; not proof against real-time relay |
| FIDO2/WebAuthn security key or platform passkey | AAL3 | Yes | Origin-bound signature; the credential cannot be replayed elsewhere |
| Certificate-based auth / Windows Hello for Business | AAL3 | Yes | Enterprise-managed, ties to device attestation |

## Conditional access signal ladder

Require progressively stronger proof as signals worsen; never make the policy
"all users, all apps, MFA once a day".

| Signal | Source | Effect on policy |
|---|---|---|
| User sign-in risk | IdP risk detection (Entra ID, Okta) | High risk → block or require phishing-resistant MFA |
| Device compliance | Intune / Jamf / CrowdStrike ZTA posture | Non-compliant → block or app-only with restricted session |
| Credential strength | Auth method used | Sensitive app → require AAL3, not any MFA |
| Network location | Named locations / geofence | Unfamiliar country → step-up, not blanket block |
| Application sensitivity | App inventory | Admin and data-export apps → strongest policy always |
| OAuth consent / grant | App consent audit | Unverified publisher or high-privilege scope → require admin approval |

Roll out in report-only first, read the impact report, exclude emergency access
accounts explicitly, and always keep one tested break-glass account outside the
policy set — a mis-scoped CA policy that locks out administrators is an outage.

## Method rollout order

1. Inventory current authentication methods and their usage counts.
2. Deploy FIDO2/passkeys to administrators and high-risk roles first
   (`implementing-hardware-security-key-authentication.md`,
   `implementing-passwordless-auth-with-microsoft-entra.md`,
   `implementing-passwordless-authentication-with-fido2.md`,
   `configuring-multi-factor-authentication-with-duo.md`).
3. Require AAL3 on Tier-0/admin resources via conditional access
   (`implementing-conditional-access-policies-azure-ad.md`,
   `implementing-identity-verification-for-zero-trust.md`).
4. Disable legacy/fallback methods (SMS, legacy auth protocols) last, after
   usage telemetry shows stragglers near zero.
5. Verify by attempting sign-in with a cloned-origin phish: the credential must
   refuse to authenticate.

Token-side protections belong to two neighbouring files:
[`attacking-oauth-with-device-code-phishing.md`](attacking-oauth-with-device-code-phishing.md)
(device-code and consent phishing against this skill) and
[`detecting-oauth-token-theft.md`](../../cloud-container-and-devsecops-security/references/detecting-oauth-token-theft.md)
(refresh-token replay and PRT abuse detection). The token *crypto* itself belongs
to
[`implementing-jwt-signing-and-verification.md`](../../cryptography-and-key-management/references/implementing-jwt-signing-and-verification.md).
