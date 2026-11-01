# Configuring Multi Factor Authentication With Duo

## API Reference

## Libraries

| Library | Install | Purpose |
|---------|---------|---------|
| duo_client | `pip install duo_client` | Official Duo SDK for Python |
| requests | `pip install requests` | HTTP client for Admin API |

## Duo Admin API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/v1/users` | List all users with enrollment status |
| GET | `/admin/v1/users/{user_id}` | Get user details and devices |
| GET | `/admin/v1/info/summary` | Account summary (user count, integrations) |
| GET | `/admin/v2/logs/authentication` | Authentication logs (v2 with paging) |
| POST | `/admin/v1/users/enroll` | Enroll new user for MFA |
| POST | `/admin/v1/users/{id}/bypass_codes` | Generate bypass codes |

## Authentication (HMAC Signing)

```python
import duo_client
admin_api = duo_client.Admin(
    ikey="DIXXXXXXXXXXXXXXXXXX",
    skey="YourSecretKey",
    host="api-XXXXXXXX.duosecurity.com"
)
users = admin_api.get_users()
```

## User Status Values

| Status | Description |
|--------|-------------|
| active | User enrolled and can authenticate |
| bypass | MFA bypassed — security risk |
| disabled | User account disabled |
| locked_out | Temporarily locked due to failed attempts |

## External References

- [Duo Admin API Reference](https://duo.com/docs/adminapi)
- [duo_client Python SDK](https://github.com/duosecurity/duo_client_python)
- [Duo Auth API](https://duo.com/docs/authapi)

---

## Standards and Controls

## NIST Standards
- **NIST SP 800-63B**: Digital Identity Guidelines - Authentication and Lifecycle Management
  - AAL1: Single-factor authentication
  - AAL2: Multi-factor authentication (Duo Push, TOTP)
  - AAL3: Hardware-based phishing-resistant (FIDO2, PIV)
- **NIST SP 800-53 Rev 5**: IA-2, IA-2(1), IA-2(2), IA-2(6), IA-2(8), IA-3, IA-5

## Duo Documentation
- **Duo Authentication Proxy**: https://duo.com/docs/authproxy-reference
- **Duo for RDP**: https://duo.com/docs/rdp
- **Duo Unix (SSH)**: https://duo.com/docs/duounix
- **Duo Web SDK**: https://duo.com/docs/duoweb
- **Duo Verified Push**: https://duo.com/blog/webauthn-passwordless-fido2-explained-componens-passwordless-architecture
- **Duo Admin API**: https://duo.com/docs/adminapi

## CISA Guidance
- **CISA MFA Guidance**: Phishing-resistant MFA requirement for federal agencies
- **EO 14028**: Executive Order on Improving the Nation's Cybersecurity - MFA mandate

## Compliance
- **PCI DSS 4.0**: Requirement 8.3.1 - MFA for all access to CDE
- **HIPAA**: 45 CFR 164.312(d) - Person or entity authentication
- **SOX**: MFA for privileged financial system access
- **CMMC**: Level 2 - IA.L2-3.5.3 Multi-factor authentication

---

## Workflows

## Workflow 1: Duo Authentication Proxy Deployment
1. Install Duo Authentication Proxy on dedicated server
2. Configure authproxy.cfg with AD/LDAP primary auth
3. Add Duo API credentials (ikey, skey, api_host)
4. Set failmode=safe for initial testing, change to secure for production
5. Start Duo proxy service, verify connectivity
6. Configure VPN/application to use proxy as RADIUS server
7. Test with pilot group before full deployment

## Workflow 2: User Enrollment
1. Admin creates Duo user (manual or AD sync)
2. User receives enrollment email/link
3. User installs Duo Mobile app
4. User scans QR code to link device
5. User completes test authentication
6. Admin verifies enrollment status in Admin Panel

## Workflow 3: MFA Fatigue Attack Response
1. Detect multiple rapid push notifications to single user
2. Alert security team via SIEM integration
3. Temporarily lock user's Duo account
4. Contact user to verify if they initiated authentication
5. If unauthorized: reset credentials, investigate source
6. If authorized: educate user, enable Verified Push
7. Update policy to require Verified Push for affected group

## Workflow 4: Duo Failover and Emergency Access
1. Duo cloud service becomes unreachable
2. Authentication Proxy checks failmode setting
3. If failmode=secure: deny all access (most secure)
4. If failmode=safe: allow primary auth only (business continuity)
5. Admin monitors Duo status page for resolution
6. After restoration: review all authentications during outage
7. Investigate any suspicious access during failover period

---

## Working Template

## Duo Admin Panel Configuration
- [ ] Admin account secured with hardware security key
- [ ] Admin API credentials generated and stored securely
- [ ] AD Sync configured for user provisioning
- [ ] User groups created (Standard, Privileged, Contractors)

## Authentication Policy Matrix
| Group | Push | Verified Push | WebAuthn | TOTP | SMS | Phone | Remember |
|-------|------|---------------|----------|------|-----|-------|----------|
| Standard | Yes | No | Optional | Yes | No | No | 7 days |
| Privileged | No | Yes | Yes | Backup | No | No | None |
| Contractors | Yes | No | No | Yes | No | No | None |

## Integration Points
| System | Integration Method | Status |
|--------|--------------------|--------|
| VPN (Cisco ASA) | RADIUS via Auth Proxy | [ ] |
| VPN (Palo Alto) | RADIUS via Auth Proxy | [ ] |
| Windows RDP | Duo for Windows Logon | [ ] |
| Linux SSH | Duo Unix (PAM) | [ ] |
| Web Apps (SAML) | Duo SSO | [ ] |
| Office 365 | Duo + Azure AD | [ ] |

## Device Health Policy
- [ ] Require disk encryption
- [ ] Minimum OS version: Windows 10 22H2 / macOS 13 / iOS 16 / Android 12
- [ ] Require firewall enabled
- [ ] Block jailbroken/rooted devices
- [ ] Require screen lock

## Emergency Procedures
- [ ] Bypass code generation procedure documented
- [ ] Failmode configuration documented per integration
- [ ] Emergency contact list for Duo outage
- [ ] Alternative authentication path tested
