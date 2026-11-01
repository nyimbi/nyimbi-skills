# Implementing Identity Verification For Zero Trust

## API Reference

## CISA Zero Trust Maturity Model - Identity Pillar

| Level | Description | Requirements |
|-------|-------------|-------------|
| Traditional | Password-based, static policies | Basic auth |
| Initial | MFA deployed, basic conditional access | MFA for all users |
| Advanced | Phishing-resistant MFA, risk-based | FIDO2, risk signals |
| Optimal | Continuous verification, passwordless | Behavioral analytics |

## Azure AD Conditional Access API

```python
import requests
headers = {"Authorization": "Bearer <token>"}
policies = requests.get(
    "https://graph.microsoft.com/v1.0/identity/conditionalAccess/policies",
    headers=headers).json()
```

## FIDO2/WebAuthn Registration

```javascript
const credential = await navigator.credentials.create({
    publicKey: {
        rp: { name: "Example Corp" },
        user: { id: userId, name: email, displayName: name },
        challenge: serverChallenge,
        pubKeyCredParams: [{ type: "public-key", alg: -7 }],
        authenticatorSelection: { residentKey: "required" },
    }
});
```

## Conditional Access Signals

| Signal | Source | Zero Trust Level |
|--------|--------|-----------------|
| Device compliance | MDM/Intune | Initial |
| Location/IP | Network context | Initial |
| User risk | Identity Protection | Advanced |
| Sign-in risk | Real-time analysis | Advanced |
| Session behavior | UEBA | Optimal |

## Okta Authentication Policies API

```bash
curl -X GET "https://DOMAIN.okta.com/api/v1/policies?type=ACCESS_POLICY" \
  -H "Authorization: SSWS <token>"
```

### References

- CISA Zero Trust Maturity Model: https://www.cisa.gov/zero-trust-maturity-model
- NIST SP 800-207: https://csrc.nist.gov/pubs/sp/800/207/final
- FIDO Alliance: https://fidoalliance.org/fido2/

---

## Standards and Controls

## NIST SP 800-207: Zero Trust Architecture - Identity

### Core Identity Tenets
- All resource authentication and authorization are dynamic and strictly enforced before access is allowed
- The enterprise collects as much information as possible about the current state of assets, network infrastructure, and communications and uses it to improve its security posture
- Access decisions should consider behavioral attributes, environmental attributes, and the identity of the requester

### Policy Engine Identity Inputs
The Policy Engine (PE) uses the following identity-related inputs:
- User identity and attributes from the IdP
- Device identity and posture from the endpoint management system
- Behavioral attributes from user and entity behavior analytics (UEBA)
- Environmental attributes (location, time, network)

## NIST SP 800-63B: Digital Identity Guidelines

### Authentication Assurance Levels (AAL)
| AAL | Description | Methods | Zero Trust Mapping |
|---|---|---|---|
| AAL1 | Some assurance | Single-factor (password) | Insufficient for ZT |
| AAL2 | High confidence | Multi-factor (push notification, OTP) | Minimum for ZT |
| AAL3 | Very high confidence | Hardware-based (FIDO2, PIV card) | Target for ZT |

### Phishing-Resistant Authenticators
- FIDO2/WebAuthn: Cryptographic authentication bound to origin domain
- PIV/CAC smart cards: Certificate-based authentication
- Not phishing-resistant: SMS OTP, voice calls, push notifications, TOTP

## CISA Zero Trust Maturity Model v2.0 - Identity Pillar

| Maturity Level | Authentication | Identity Store | Risk Assessment | Visibility |
|---|---|---|---|---|
| Traditional | Password + basic MFA | Multiple disconnected stores | None | Basic audit logs |
| Initial | MFA for all users | Federated IdP | Static risk rules | Centralized auth logs |
| Advanced | Phishing-resistant MFA | Single authoritative IdP with SCIM | Risk-based conditional access | Identity analytics |
| Optimal | Continuous verification | Automated lifecycle governance | AI-driven threat detection | Real-time UEBA |

## FIDO Alliance Standards

### FIDO2 / WebAuthn
- W3C Web Authentication specification for passwordless authentication
- Public-key cryptography: private key never leaves the authenticator
- Origin-bound: authentication is cryptographically tied to the service domain
- Resistant to phishing, replay, and man-in-the-middle attacks

### Passkeys
- Evolution of FIDO2 for consumer and enterprise use
- Synced across devices via platform credential managers (iCloud Keychain, Google Password Manager)
- Discoverable credentials eliminate need to remember usernames

## Microsoft Entra (Azure AD) Identity Protection

### Risk Detection Categories
| Risk Type | Detection | Response |
|---|---|---|
| Anonymous IP | Sign-in from anonymous proxy/VPN | Require MFA |
| Atypical travel | Impossible travel between sign-in locations | Block + investigate |
| Malware-linked IP | Sign-in from known malicious IP | Block |
| Unfamiliar sign-in | Unusual sign-in properties | Step-up auth |
| Leaked credentials | Credentials found in dark web dumps | Force password reset |
| Token anomaly | Unusual token characteristics | Revoke session |

### Continuous Access Evaluation Protocol (CAEP)
- Real-time token revocation on security events
- Critical events: user disabled, password changed, high risk detected
- Reduces token lifetime gap from hours to near real-time
- Supported by Microsoft 365, Exchange Online, SharePoint Online

## Okta Identity Security

### Okta ThreatInsight
- Pre-authentication threat detection using IP reputation
- Credential stuffing protection
- Bot detection and rate limiting
- Anomalous location and device detection

### Okta FastPass
- Passwordless, phishing-resistant authentication
- Device-bound biometric verification
- Continuous device trust assessment
- No shared secrets transmitted over network

---

## Workflows

## Workflow 1: Zero Trust Authentication Flow

```
User Initiates Access
    │
    v
┌─────────────────────────┐
│ 1. Pre-Authentication    │
│ - Check IP reputation    │
│ - Rate limit evaluation  │
│ - Bot detection          │
│ - Geo-blocking check     │
└──────────┬──────────────┘
           v
┌─────────────────────────┐
│ 2. Primary Authentication│
│ - FIDO2 key challenge    │
│ - Biometric verification │
│ - Certificate validation │
│ - Passwordless flow      │
└──────────┬──────────────┘
           v
┌─────────────────────────┐
│ 3. Context Assessment    │
│ - Device compliance      │
│ - Network location       │
│ - Time of access         │
│ - Behavioral baseline    │
│ - Previous session state │
└──────────┬──────────────┘
           v
┌─────────────────────────┐
│ 4. Risk Calculation      │
│ - User risk level        │
│ - Sign-in risk level     │
│ - Aggregate score        │
└───┬──────────┬──────┬───┘
    │          │      │
  LOW        MED    HIGH
    │          │      │
    v          v      v
┌──────┐ ┌────────┐ ┌────────┐
│Grant │ │Step-Up │ │Block + │
│Token │ │ Auth   │ │Alert   │
└──────┘ └────────┘ └────────┘
```

## Workflow 2: Continuous Access Evaluation

```
Active Session
    │
    v
┌──────────────────────────────┐
│ Continuous Monitoring Loop    │
│                               │
│  ┌─── Check every N minutes ──┐
│  │                             │
│  │  ┌─────────────────────┐   │
│  │  │ Signal Collection    │   │
│  │  │ - Device compliance  │   │
│  │  │ - User risk change   │   │
│  │  │ - Location shift     │   │
│  │  │ - Behavior anomaly   │   │
│  │  └──────────┬──────────┘   │
│  │             v               │
│  │  ┌─────────────────────┐   │
│  │  │ Critical Events      │   │
│  │  │ - Account disabled   │   │
│  │  │ - Password changed   │   │
│  │  │ - MFA registration   │   │
│  │  │ - Admin revocation   │   │
│  │  └──────────┬──────────┘   │
│  │             v               │
│  │  ┌─────────────────────┐   │
│  │  │ Re-Evaluate Access   │   │
│  │  │ - Recalculate risk   │   │
│  │  │ - Apply policy       │   │
│  │  └───┬─────────┬───────┘   │
│  │      │         │           │
│  │   Continue   Revoke        │
│  │   Session    Token         │
│  └──────┘         │           │
│                   v           │
│           ┌──────────────┐    │
│           │ Force Re-Auth│    │
│           │ or Terminate │    │
│           └──────────────┘    │
└──────────────────────────────┘
```

## Workflow 3: FIDO2 Enrollment

```
Admin Initiates Enrollment Campaign
    │
    v
┌──────────────────────────┐
│ 1. User Notification      │
│ - Email with instructions │
│ - Self-service portal URL │
│ - Deadline for enrollment │
└──────────┬───────────────┘
           v
┌──────────────────────────┐
│ 2. User Self-Service      │
│ - Authenticate with       │
│   existing credentials    │
│ - Register security key   │
│   (YubiKey, Titan key)    │
│ - Register platform auth  │
│   (Windows Hello, TouchID)│
│ - Register backup method  │
└──────────┬───────────────┘
           v
┌──────────────────────────┐
│ 3. Verification           │
│ - Test sign-in with FIDO2 │
│ - Confirm backup works    │
│ - Record key serial/ID    │
└──────────┬───────────────┘
           v
┌──────────────────────────┐
│ 4. Policy Enforcement     │
│ - Enable phishing-resist  │
│   conditional access      │
│ - Disable legacy MFA      │
│ - Monitor compliance rate │
└──────────────────────────┘
```

## Workflow 4: Compromised Identity Response

```
Identity Threat Detected
    │
    v
┌──────────────────────────┐
│ 1. Detection Signal       │
│ - Impossible travel       │
│ - Leaked credentials      │
│ - Token anomaly           │
│ - Behavioral deviation    │
└──────────┬───────────────┘
           v
┌──────────────────────────┐
│ 2. Automated Response     │
│ - Revoke all sessions     │
│ - Disable account         │
│ - Trigger SOAR playbook   │
│ - Notify SOC analyst      │
└──────────┬───────────────┘
           v
┌──────────────────────────┐
│ 3. Investigation          │
│ - Review sign-in logs     │
│ - Check accessed resources│
│ - Correlate with EDR data │
│ - Interview user          │
└──────────┬───────────────┘
           v
┌──────────────────────────┐
│ 4. Remediation            │
│ - Reset all credentials   │
│ - Re-enroll FIDO2 keys    │
│ - Review and restrict     │
│   access permissions      │
│ - Re-enable account       │
│ - Update detection rules  │
└──────────────────────────┘
```

---

## Working Template

## Project Information

| Field | Value |
|---|---|
| Project Name | |
| Organization | |
| Identity Provider | [Azure AD / Okta / Ping Identity] |
| User Population | |
| Target Completion | |

## Current State Assessment

### Identity Infrastructure
- **Primary IdP**: |
- **Secondary IdPs**: |
- **Local Accounts**: [Count and locations] |
- **Shared Accounts**: [Count - target for elimination] |

### Current MFA State
| Method | Enabled | Users Enrolled | Phishing-Resistant |
|---|---|---|---|
| SMS OTP | | | No |
| Voice Call | | | No |
| TOTP App | | | No |
| Push Notification | | | No |
| FIDO2 Security Key | | | Yes |
| Windows Hello | | | Yes |
| Certificate/PIV | | | Yes |

### MFA Enrollment Target
- Current enrollment rate: ___%
- Target enrollment rate: 100%
- Phishing-resistant target: 100%

## Phishing-Resistant MFA Rollout Plan

### Hardware Key Distribution

| User Group | Key Type | Quantity | Distribution Method | Timeline |
|---|---|---|---|---|
| Executive Leadership | YubiKey 5 NFC | | In-person | Week 1 |
| IT Administrators | YubiKey 5C | | IT distribution | Week 2 |
| All Employees | YubiKey Security Key | | Self-service + mail | Weeks 3-8 |

### Enrollment Campaign
- [ ] Communication sent to all users
- [ ] Self-service portal configured
- [ ] Help desk trained on enrollment support
- [ ] Enrollment deadline set: ____
- [ ] Escalation path for non-compliant users

## Conditional Access Policies

| Policy Name | Users | Apps | Conditions | Grant Controls | Session Controls |
|---|---|---|---|---|---|
| Block Legacy Auth | All | All | Legacy clients | Block | N/A |
| Require MFA | All | All | Any | Require MFA | Sign-in freq: 8hr |
| Require Compliant Device | All | Sensitive Apps | Any | Compliant device | App enforced |
| Block Risky Sign-In | All | All | High sign-in risk | Block | N/A |
| Require FIDO2 for Admins | Admin roles | Admin portals | Any | FIDO2 only | 1hr frequency |

## Risk-Based Policies

| Risk Level | User Risk Response | Sign-In Risk Response |
|---|---|---|
| Low | Allow | Allow |
| Medium | Require MFA step-up | Require MFA step-up |
| High | Block + alert SOC | Block + alert SOC |

## Identity Governance

### Lifecycle Automation
- [ ] HR system integrated for joiner/mover/leaver
- [ ] Automatic provisioning on hire
- [ ] Role change triggers access review
- [ ] Automatic deprovisioning on termination
- [ ] Contractor access expiration configured

### Access Reviews
- Frequency: Quarterly
- Scope: All application assignments
- Reviewers: Direct managers
- Auto-action on non-response: Revoke access

## Monitoring and Detection

| Capability | Tool | Status |
|---|---|---|
| Sign-in log analysis | SIEM (Splunk/Sentinel) | |
| Identity threat detection | Entra ID Protection / ThreatInsight | |
| Impossible travel detection | IdP + UEBA | |
| Continuous Access Evaluation | CAE/CAEP | |
| Behavioral analytics | UEBA platform | |

## Sign-Off

| Stakeholder | Role | Approval | Date |
|---|---|---|---|
| | CISO | | |
| | Identity Team Lead | | |
| | Help Desk Manager | | |
| | HR Systems | | |
