# Implementing Zero Trust DNS With Nextdns

## API Reference

## NextDNS REST API

### Authentication
```
Header: X-Api-Key: <your-api-key>
Base URL: https://api.nextdns.io
```

### Profile Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/profiles/{id}` | Get profile configuration |
| GET | `/profiles/{id}/security` | Get security feature settings |
| GET | `/profiles/{id}/denylist` | Get blocked domains list |
| GET | `/profiles/{id}/allowlist` | Get allowed domains list |
| GET | `/profiles/{id}/logs` | Get DNS query logs |
| GET | `/profiles/{id}/analytics/status` | Query volume analytics |
| GET | `/profiles/{id}/analytics/domains` | Top queried domains |
| GET | `/profiles/{id}/analytics/blockedReasons` | Block reason breakdown |

### Security Feature Keys
| Key | Feature |
|-----|---------|
| `threatIntelligenceFeeds` | Real-time threat intel blocking |
| `aiDetection` | AI-based threat detection |
| `googleSafeBrowsing` | Google Safe Browsing integration |
| `cryptojacking` | Cryptomining domain blocking |
| `dnsRebinding` | DNS rebinding attack protection |
| `idnHomographs` | IDN homograph attack protection |
| `typosquatting` | Typosquatting domain detection |
| `dga` | Domain generation algorithm blocking |
| `nrd` | Newly registered domain blocking |

### Log Entry Fields
| Field | Description |
|-------|-------------|
| `domain` | Queried domain name |
| `status` | `allowed`, `blocked`, or `default` |
| `reasons` | Array of block reasons |
| `clientIp` | Requesting client IP |
| `timestamp` | Query timestamp (ISO 8601) |

## References
- NextDNS API: https://nextdns.github.io/api/
- NextDNS Security: https://nextdns.io/security

---

## Standards and Controls

## DNS Security Standards

### RFC 8484: DNS Queries over HTTPS (DoH)
- Encrypts DNS queries over HTTPS on port 443
- Prevents DNS eavesdropping and manipulation
- Browser and OS-level support

### RFC 7858: DNS over Transport Layer Security (DoT)
- Encrypts DNS queries over TLS on port 853
- Dedicated port enables network-level policy control
- Supported by Android 9+, systemd-resolved, Unbound

### RFC 9250: DNS over Dedicated QUIC Connections (DoQ)
- Lower latency than DoH/DoT
- Multiplexed queries without head-of-line blocking
- Supported by NextDNS and Adguard

### NIST SP 800-81-2: Secure Domain Name System Deployment Guide
- DNS infrastructure security requirements
- DNSSEC validation recommendations
- DNS monitoring and logging guidance

## Zero Trust DNS Standards

### Microsoft ZTDNS (Windows 11)
- Enforces that endpoints only use approved DNS resolvers
- Windows Firewall blocks traffic to domains not resolved through protected DNS
- Integration with Windows Defender for endpoint protection

### CISA ZTMM - Network Pillar
- DNS encryption requirement for zero trust compliance
- DNS monitoring for visibility and analytics
- DNS filtering as network security control

## Compliance Mapping

### NIST SP 800-53
- SC-20: Secure Name/Address Resolution Service (Authoritative Source)
- SC-21: Secure Name/Address Resolution Service (Recursive or Caching Resolver)
- SC-22: Architecture and Provisioning for Name/Address Resolution Service
- SI-4: Information System Monitoring (DNS logging)

### CIS Controls v8
- Control 9.2: Use DNS Filtering Services
- Control 9.3: Maintain and Enforce Network-Based URL Filters
- Control 13.3: Deploy Network Intrusion Detection (DNS monitoring)

---

## Workflows

## Workflow 1: Initial NextDNS Deployment

```
Step 1: Create NextDNS Configuration Profile
  - Sign up at nextdns.io
  - Create configuration profile with unique ID
  - Configure security settings (all threat protection enabled)
  - Configure privacy settings (blocklists, native tracking)
  - Set log retention policy

Step 2: Deploy to Network Infrastructure
  - Configure router-level DNS (DoH/DoT)
  - Block plaintext DNS (port 53) at firewall for bypass prevention
  - Configure split DNS for internal domains
  - Test resolution of allowed and blocked domains

Step 3: Deploy to Endpoints
  - Install NextDNS CLI on managed endpoints
  - Configure mobile devices via app or Private DNS
  - Deploy MDM profile for iOS devices
  - Verify per-device identification in NextDNS dashboard

Step 4: Monitor and Tune
  - Review blocked domains for false positives
  - Add necessary allowlist entries
  - Monitor query patterns for anomalies
  - Adjust blocklists based on organizational needs
```

## Workflow 2: DNS Security Policy Enforcement

```
Step 1: Define DNS Security Policy
  - Mandatory security protections (threat intel, DGA, NRD)
  - Privacy protections (tracker blocking, telemetry)
  - Compliance-specific blocking categories
  - Exception handling process

Step 2: Block Plaintext DNS Bypass
  - Firewall rule: Block outbound port 53 UDP/TCP
  - Exception: Only NextDNS CLI or approved resolvers
  - Block known DoH endpoints not managed by organization
  - Disable browser-level DoH in favor of system DNS

Step 3: Implement Monitoring
  - Set up API integration for log export
  - Forward DNS logs to SIEM
  - Create alerts for suspicious DNS patterns
  - Monitor for DNS tunneling indicators
```

## Workflow 3: Incident Response with DNS Logs

```
Step 1: Detect Suspicious Activity
  - Alert on high-frequency queries to single domain
  - Alert on queries to known C2 domains (auto-blocked)
  - Alert on DGA-like domain patterns
  - Alert on DNS tunneling indicators (high entropy, long subdomains)

Step 2: Investigate
  - Query NextDNS API for device-level DNS logs
  - Correlate blocked domains with threat intelligence
  - Identify affected devices and users
  - Determine scope of potential compromise

Step 3: Respond
  - Add malicious domains to denylist for immediate blocking
  - Isolate affected endpoints
  - Update firewall rules as needed
  - Document findings for incident report
```

---

## Working Template

## Configuration
- **NextDNS Config ID**: _______________
- **Plan**: [ ] Free [ ] Pro [ ] Business [ ] Enterprise
- **Log Retention**: _____ days
- **Log Storage Region**: [ ] US [ ] EU [ ] UK [ ] Switzerland

## Security Settings Checklist
- [ ] Threat Intelligence Feeds enabled
- [ ] AI-Driven Threat Detection enabled
- [ ] Google Safe Browsing enabled
- [ ] Cryptojacking Protection enabled
- [ ] DNS Rebinding Protection enabled
- [ ] IDN Homograph Attack Protection enabled
- [ ] Typosquatting Protection enabled
- [ ] DGA Protection enabled
- [ ] NRD Protection (< 30 days) enabled
- [ ] DDNS Blocking enabled
- [ ] Parked Domains blocking enabled

## Privacy Settings Checklist
- [ ] Blocklists configured (list: ___)
- [ ] Native Tracking Protection enabled
- [ ] CNAME Cloaking Protection enabled

## Deployment Targets

| Target | Method | Status | Config Verified |
|---|---|---|---|
| Router | DoT/DoH | [ ] Complete | [ ] Verified |
| Windows endpoints | NextDNS CLI | [ ] Complete | [ ] Verified |
| macOS endpoints | NextDNS CLI | [ ] Complete | [ ] Verified |
| Linux servers | systemd-resolved | [ ] Complete | [ ] Verified |
| iOS devices | MDM profile | [ ] Complete | [ ] Verified |
| Android devices | Private DNS | [ ] Complete | [ ] Verified |

## Network Controls
- [ ] Plaintext DNS (port 53) blocked at firewall
- [ ] Unauthorized DoH endpoints blocked
- [ ] Split DNS configured for internal domains
- [ ] Browser DoH disabled in favor of system DNS
