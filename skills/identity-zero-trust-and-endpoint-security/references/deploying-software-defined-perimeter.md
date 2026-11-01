# Deploying Software Defined Perimeter

## API Reference

## Core SDP Concepts

| Component | Description |
|-----------|-------------|
| SDP Controller | Central policy engine managing authentication and authorization |
| SDP Gateway | Enforces access policies, terminates encrypted tunnels |
| SDP Client | End-user agent performing Single Packet Authorization (SPA) |
| SPA (Single Packet Authorization) | Cryptographic knock before TCP connection allowed |

## Appgate SDP Admin API

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/admin/login` | Authenticate and get Bearer token |
| GET | `/admin/sites` | List configured sites |
| GET | `/admin/policies` | List access policies |
| GET | `/admin/entitlements` | List entitlements (resource access rules) |
| GET | `/admin/appliances` | List SDP gateways and controllers |
| GET | `/admin/identity-providers` | List identity providers |
| POST | `/admin/entitlements` | Create new entitlement |

## Dark Port Scanning

```python
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(5)
result = sock.connect_ex((host, port))  # Non-zero = port dark (SDP enforced)
```

## Mutual TLS Verification

```python
import ssl
ctx = ssl.create_default_context()
ctx.load_cert_chain("client.crt", "client.key")
with ctx.wrap_socket(socket.socket(), server_hostname=host) as s:
    s.connect((host, 443))
```

## SPA Packet Structure

| Field | Description |
|-------|-------------|
| Random Data | 16 bytes of random padding |
| Username | SDP client identity |
| Timestamp | Prevents replay attacks |
| HMAC | SHA-256 authentication code |

## External References

- [Appgate SDP API Docs](https://sdphelp.appgate.com/adminguide/rest-api-guide.html)
- [CSA SDP Specification](https://cloudsecurityalliance.org/research/sdp/)
- [fwknop SPA Tool](https://www.cipherdyne.org/fwknop/)

---

## Standards and Controls

## CSA Software-Defined Perimeter Specification v2.0

### Core Architecture
- **SDP Controller**: Central policy and authentication authority
- **Initiating Host (IH)**: Client device requesting access
- **Accepting Host (AH)**: Gateway protecting backend resources
- **Single Packet Authorization (SPA)**: Pre-authentication mechanism making services invisible

### SDP Workflow
1. IH authenticates to SDP Controller
2. Controller validates identity, device posture, and policy
3. Controller instructs AH to accept connection from specific IH
4. IH sends SPA packet to AH
5. AH validates SPA and opens temporary port
6. mTLS tunnel established between IH and AH
7. Application traffic flows through encrypted tunnel

### Deployment Models
| Model | Use Case | Architecture |
|---|---|---|
| Client-to-Gateway | Remote user access | IH → AH Gateway → Backend servers |
| Client-to-Server | Direct application access | IH → AH (application server) |
| Server-to-Server | Workload communication | IH (server) → AH (server) |
| Gateway-to-Gateway | Site-to-site connectivity | AH₁ → Controller → AH₂ |

## NIST SP 800-207: SDP as Zero Trust Deployment

### SDP Mapping to NIST ZTA Components
| NIST Component | SDP Equivalent |
|---|---|
| Policy Engine (PE) | SDP Controller policy evaluation |
| Policy Administrator (PA) | SDP Controller session management |
| Policy Enforcement Point (PEP) | SDP Gateway (Accepting Host) |

### NIST ZTA Tenets Addressed by SDP
- All communication secured regardless of network location (mTLS tunnels)
- Per-session access grants (dynamic SDP connections)
- Dynamic policy evaluation (controller real-time decisions)
- Asset integrity monitoring (device posture checks)

## CISA Zero Trust Maturity Model v2.0

### Network Pillar - SDP Alignment
| Maturity | SDP Capability |
|---|---|
| Traditional | No SDP, perimeter-based VPN |
| Initial | SDP for remote access, basic SPA |
| Advanced | Full SDP with device posture, context-aware |
| Optimal | Dynamic SDP with continuous verification, ML-driven |

## Single Packet Authorization (SPA) Technical Details

### SPA Packet Structure
- Encrypted with shared key or asymmetric cryptography
- Contains: source IP, timestamp, HMAC, requested service
- Single UDP packet (no TCP handshake visible)
- Anti-replay protection via timestamp and sequence number

### fwknop Implementation
- Open-source SPA implementation
- Supports AES-256 and GnuPG encryption
- Integrates with iptables/nftables for firewall rule insertion
- Temporary rule created for authenticated session only

## mTLS Configuration Standards

### Certificate Requirements
- Minimum RSA 2048-bit or ECDSA P-256 keys
- Short-lived certificates (24-72 hours) preferred
- OCSP stapling for real-time revocation checking
- Certificate pinning for additional security

---

## Workflows

## Workflow 1: SDP Connection Establishment

```
┌────────────┐     ┌──────────────┐     ┌────────────┐
│ IH (Client) │     │ SDP Controller│     │ AH (Gateway)│
└──────┬─────┘     └──────┬───────┘     └──────┬─────┘
       │                   │                     │
       │ 1. Authenticate   │                     │
       │──────────────────>│                     │
       │                   │                     │
       │ 2. Validate ID,   │                     │
       │    device, policy │                     │
       │                   │                     │
       │ 3. Auth response  │                     │
       │<──────────────────│                     │
       │  (SPA key, AH IP) │                     │
       │                   │ 4. Notify AH to     │
       │                   │    expect IH        │
       │                   │────────────────────>│
       │                   │                     │
       │ 5. Send SPA packet│                     │
       │─────────────────────────────────────────>│
       │                   │                     │
       │                   │  6. Validate SPA    │
       │                   │     Open port       │
       │                   │                     │
       │ 7. mTLS handshake │                     │
       │<════════════════════════════════════════>│
       │                   │                     │
       │ 8. Application    │                     │
       │    traffic flows  │                     │
       │<═══════════════════════════════════════=>│
```

## Workflow 2: SDP Deployment Lifecycle

```
Phase 1: Planning (Weeks 1-2)
├── Inventory protected applications
├── Map user-to-application access requirements
├── Design PKI infrastructure for mTLS
├── Select SDP solution (open-source or commercial)
└── Plan network architecture changes

Phase 2: Controller Setup (Weeks 3-4)
├── Deploy SDP controller with HA
├── Integrate with IdP (SAML/OIDC)
├── Configure PKI and certificate templates
├── Define application catalog and policies
└── Test controller authentication flow

Phase 3: Gateway Deployment (Weeks 5-6)
├── Deploy gateways in each app environment
├── Configure default-drop firewall rules
├── Enable SPA listeners
├── Register applications with controller
└── Verify gateway invisibility (port scan test)

Phase 4: Client Rollout (Weeks 7-10)
├── Package SDP client with certificates
├── Deploy to pilot user group
├── Validate end-to-end connectivity
├── Expand to all user groups
└── Decommission legacy VPN access

Phase 5: Operations (Ongoing)
├── Monitor SDP controller and gateway health
├── Rotate certificates on schedule
├── Review and update access policies
├── Conduct quarterly penetration tests
└── Update SDP components for security patches
```

## Workflow 3: SPA Validation

```
Incoming Packet to Gateway
    │
    v
┌─────────────────────┐
│ Is it a SPA packet?  │
│ (Check magic bytes)  │
└───┬──────────┬──────┘
    │          │
   YES        NO
    │          │
    v          v
┌──────────┐  ┌──────────┐
│ Decrypt  │  │ DROP     │
│ SPA data │  │ silently │
└────┬─────┘  └──────────┘
     v
┌─────────────────────┐
│ Validate timestamp   │
│ (within 60s window)  │
└───┬──────────┬──────┘
   VALID    EXPIRED
    │          │
    v          v
┌──────────┐  ┌──────────┐
│ Check    │  │ DROP +   │
│ HMAC     │  │ Log      │
└────┬─────┘  └──────────┘
     v
┌─────────────────────┐
│ Verify replay        │
│ (check sequence DB)  │
└───┬──────────┬──────┘
   NEW      REPLAY
    │          │
    v          v
┌──────────┐  ┌──────────┐
│ Open port │  │ DROP +   │
│ for src IP│  │ Alert    │
│ (30s TTL) │  └──────────┘
└──────────┘
```

---

## Working Template

## Project Information

| Field | Value |
|---|---|
| Project Name | |
| SDP Solution | [Appgate SDP / Zscaler / Open-source / Other] |
| Project Lead | |
| Start Date | |

## Application Inventory

| Application | FQDN/IP | Port | Protocol | Criticality | Gateway Assignment |
|---|---|---|---|---|---|
| | | | | | |

## SDP Controller Configuration

| Parameter | Value |
|---|---|
| HA Mode | [Active-Active / Active-Passive] |
| IdP Integration | [SAML / OIDC] |
| IdP Provider | [Azure AD / Okta / Ping] |
| PKI Backend | [Internal CA / HashiCorp Vault / EJBCA] |
| Client Cert Lifetime | [24h / 48h / 72h] |
| Audit Log Destination | [SIEM / Syslog / Cloud storage] |

## Gateway Deployment

| Gateway Name | Location | Protected Apps | SPA Enabled | mTLS Enabled | Default-Drop |
|---|---|---|---|---|---|
| | | | Yes | Yes | Yes |

## Access Policy Matrix

| User Group | Application | Conditions | Action |
|---|---|---|---|
| | | Device posture + MFA | Allow |
| Default | All | None | Deny |

## Security Validation

- [ ] Port scan confirms gateway invisibility
- [ ] SPA validation working correctly
- [ ] mTLS handshake succeeds with valid certs
- [ ] Invalid SPA packets dropped silently
- [ ] Revoked certificates denied access
- [ ] Lateral movement between apps blocked
- [ ] Logs captured in SIEM

## Sign-Off

| Stakeholder | Role | Approval | Date |
|---|---|---|---|
| | Security Architecture | | |
| | Network Engineering | | |
| | Application Owners | | |
