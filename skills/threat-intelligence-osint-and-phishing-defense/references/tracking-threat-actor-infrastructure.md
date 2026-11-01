# Tracking Threat Actor Infrastructure

## API Reference

## Pivoting Techniques

| Technique | Source | Discovers |
|-----------|--------|-----------|
| Passive DNS | DNS resolvers | Domains on same IP, historical mappings |
| Reverse WHOIS | Registrar data | Domains by same registrant |
| SSL Certificate | CT logs, direct | Shared certs, SANs, issuers |
| Shodan/Censys | Internet scanning | Open ports, services, banners |
| HTTP fingerprint | Server responses | Body hash, headers, favicon |
| JARM/JA3S | TLS handshake | C2 framework identification |

## API Endpoints

| Service | Endpoint | Auth |
|---------|----------|------|
| Shodan Host | `GET /shodan/host/{ip}?key=` | API key |
| VirusTotal IP | `GET /api/v3/ip-addresses/{ip}` | x-apikey header |
| VirusTotal Domain | `GET /api/v3/domains/{domain}` | x-apikey header |
| SecurityTrails | `GET /v1/domain/{d}/subdomains` | APIKEY header |
| RDAP WHOIS | `GET https://rdap.org/domain/{d}` | None |

## Network Fingerprinting

| Method | Tool | Description |
|--------|------|-------------|
| JARM | jarm.py | Active TLS server fingerprint |
| JA3S | Zeek/Wireshark | Passive TLS Server Hello hash |
| Favicon hash | Shodan `http.favicon.hash` | mmh3 hash of favicon.ico |
| HTTP body hash | SHA-256 | Response body fingerprint |
| Server banner | HTTP Server header | Software identification |

## Python Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| `requests` | >=2.28 | API queries to Shodan/VT |
| `ssl` | stdlib | TLS certificate retrieval |
| `socket` | stdlib | DNS resolution, connections |
| `hashlib` | stdlib | Certificate/content fingerprinting |

## References

- Shodan API: https://developer.shodan.io/api
- VirusTotal API v3: https://docs.virustotal.com/reference/overview
- Certificate Transparency: https://certificate.transparency.dev/
- JARM: https://github.com/salesforce/jarm

---

## Standards and Controls

## STIX 2.1 Infrastructure Object
```json
{
  "type": "infrastructure",
  "name": "C2 Server",
  "infrastructure_types": ["command-and-control"],
  "description": "Cobalt Strike TeamServer at 198.51.100.1",
  "first_seen": "2025-01-01T00:00:00Z",
  "last_seen": "2025-06-01T00:00:00Z"
}
```

## Diamond Model of Intrusion Analysis
- **Adversary**: Threat actor or group
- **Capability**: Tools, techniques, and malware
- **Infrastructure**: C2 servers, domains, hosting
- **Victim**: Targeted organization or individual

## Infrastructure Types (STIX vocabulary)
- command-and-control, botnet, exfiltration, hosting-malware
- hosting-target-lists, phishing, staging, undefined

## Network Fingerprinting Methods
| Method | Type | Description |
|--------|------|-------------|
| JARM | Active | TLS server fingerprint from 10 TLS handshakes |
| JA3S | Passive | Server Hello hash from TLS negotiation |
| JA3 | Passive | Client Hello hash for client fingerprinting |
| Favicon Hash | Active | HTTP favicon file hash |
| HTTP Headers | Active/Passive | Server banner and header fingerprinting |
| SSH Key | Active | SSH host key fingerprint |

## Passive DNS Record Types
- A/AAAA: Domain to IP mapping
- CNAME: Domain alias
- MX: Mail server records
- NS: Nameserver records
- TXT: Text records (SPF, DKIM, verification)

## References
- [Diamond Model Paper](https://www.activeresponse.org/wp-content/uploads/2013/07/diamond.pdf)
- [STIX Infrastructure](https://docs.oasis-open.org/cti/stix/v2.1/os/stix-v2.1-os.html#_jo3k1o6lr9)
- [JARM](https://github.com/salesforce/jarm)
- [JA3/JA3S](https://github.com/salesforce/ja3)

---

## Workflows

## Workflow 1: IP-Centric Pivoting
```
[Known C2 IP] --> [Shodan/Censys] --> [Service Fingerprints]
      |                                      |
      v                                      v
[Passive DNS] --> [Associated Domains] --> [WHOIS Analysis] --> [Registrant Pivot]
      |                                                               |
      v                                                               v
[SSL Certs] --> [Subject Alt Names] --> [New Domains] --> [Additional IPs]
```

## Workflow 2: Domain-Centric Pivoting
```
[Known C2 Domain] --> [DNS History] --> [Historical IPs] --> [Co-hosted Domains]
        |                                                          |
        v                                                          v
  [CT Logs] --> [Subdomains] --> [Infrastructure Map] --> [Shared Hosting Analysis]
        |
        v
  [WHOIS] --> [Registrant/Email] --> [Other Registered Domains]
```

## Workflow 3: C2 Framework Hunting
```
[C2 Signature] --> [Shodan Search] --> [Candidate Servers] --> [Validation]
                                                                    |
                                                                    v
                                                          [JARM Fingerprint]
                                                                    |
                                                                    v
                                                          [Confirm C2 Type]
                                                                    |
                                                                    v
                                                          [Track Over Time]
```

## Workflow 4: Continuous Monitoring
```
[Watchlist IPs/Domains] --> [Scheduled Scans] --> [Change Detection] --> [Alerts]
                                                         |
                                                +--------+--------+
                                                |        |        |
                                                v        v        v
                                          [New Port] [DNS Change] [New Cert]
                                                |        |        |
                                                v        v        v
                                          [Investigate] [Update TI] [Share]
```

---

## Working Template

## Report Metadata
| Field | Value |
|-------|-------|
| Report ID | INFRA-YYYY-NNNN |
| Date | YYYY-MM-DD |
| Classification | TLP:AMBER |
| Analyst | [Name] |

## Infrastructure Summary
| Metric | Count |
|--------|-------|
| C2 Servers Identified | |
| Domains Tracked | |
| SSL Certificates Found | |
| ASNs Involved | |
| Countries | |

## C2 Servers
| IP Address | Ports | Framework | ASN | Country | First Seen | Last Seen |
|-----------|-------|-----------|-----|---------|-----------|----------|
| | | | | | | |

## Associated Domains
| Domain | Resolved IP | First Seen | Last Seen | Source |
|--------|-----------|-----------|----------|--------|
| | | | | pDNS/CT/WHOIS |

## SSL Certificates
| Common Name | Issuer | Not Before | Not After | SANs |
|------------|--------|-----------|----------|------|
| | | | | |

## Pivot Map
```
[Seed IP] --> [Domain A] --> [IP B] --> [Domain C]
                  |                         |
                  v                         v
            [CT: Domain D]           [WHOIS: Domain E]
```

## Recommendations
1. Block identified C2 IPs and domains at network perimeter
2. Deploy JARM/JA3S signatures for C2 framework detection
3. Monitor CT logs for new certificates matching tracked domains
4. Set up passive DNS alerts for domain resolution changes
