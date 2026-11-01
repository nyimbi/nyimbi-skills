# Performing External Network Penetration Test

## API Reference

## Libraries Used
- **socket**: TCP port scanning and banner grabbing
- **subprocess**: Execute nmap with XML output parsing
- **dns.resolver** (dnspython): DNS record enumeration and subdomain discovery
- **ssl**: TLS certificate inspection and cipher analysis
- **xml.etree.ElementTree**: Parse nmap XML output

## CLI Interface
```
python agent.py scan --host <target_ip> [--ports 22 80 443]
python agent.py nmap --target <ip_or_range> [--type quick|full|vuln|udp]
python agent.py dns --domain <domain>
python agent.py ssl --host <hostname> [--port 443]
```

## Core Functions

### `tcp_port_scan(host, ports)` — Scan TCP ports with banner grabbing
Scans 22 common ports by default. Returns open ports with service banners.

### `run_nmap_scan(target, scan_type)` — Execute nmap and parse XML results
Scan types: `quick` (top 100 -sV), `full` (-p- -sC), `vuln` (NSE vuln scripts), `udp` (top 50 UDP).

### `dns_enumeration(domain)` — Enumerate DNS records and subdomains
Queries A, AAAA, MX, NS, TXT, SOA, CNAME records. Tests 10 common subdomain prefixes.

### `ssl_check(host, port)` — Inspect TLS certificate and cipher suite
Returns subject, issuer, validity dates, TLS version, and negotiated cipher.

## Default Port List
21 (FTP), 22 (SSH), 23 (Telnet), 25 (SMTP), 53 (DNS), 80 (HTTP), 110 (POP3),
135 (RPC), 139 (NetBIOS), 143 (IMAP), 443 (HTTPS), 445 (SMB), 993/995 (IMAPS/POP3S),
1433 (MSSQL), 1521 (Oracle), 3306 (MySQL), 3389 (RDP), 5432 (PostgreSQL),
5900 (VNC), 8080/8443 (HTTP Proxy/Alt HTTPS)

## Dependencies
```
pip install dnspython
```
System: nmap (optional, for advanced scanning)

---

## Standards and Controls

## Primary Standards

### PTES (Penetration Testing Execution Standard)
- Website: http://www.pentest-standard.org/
- Phases: Pre-engagement, Intelligence Gathering, Threat Modeling, Vulnerability Analysis, Exploitation, Post-Exploitation, Reporting
- Best for: Comprehensive network penetration testing engagements

### NIST SP 800-115
- Title: Technical Guide to Information Security Testing and Assessment
- URL: https://csrc.nist.gov/publications/detail/sp/800-115/final
- Covers: Review techniques, target identification, vulnerability analysis, planning, execution, post-testing

### OSSTMM v3 (Open Source Security Testing Methodology Manual)
- URL: https://www.isecom.org/OSSTMM.3.pdf
- Focus: Operational security testing across physical, wireless, telecommunications, data networks, and human channels

### OWASP Testing Guide v4.2
- URL: https://owasp.org/www-project-web-security-testing-guide/
- Focus: Web application security testing methodology
- Complement to network-level testing

## Compliance Frameworks

| Framework | Requirement | Pentest Frequency |
|-----------|------------|-------------------|
| PCI DSS v4.0 | Requirement 11.4 | Annual + after significant changes |
| SOC 2 Type II | CC7.1 | Annual |
| ISO 27001 | A.12.6, A.18.2 | Annual recommended |
| HIPAA | §164.308(a)(8) | Annual recommended |
| FedRAMP | CA-8 | Annual |

## CVSS v3.1 Scoring Reference

| Metric Group | Components |
|-------------|-----------|
| Base Score | Attack Vector, Attack Complexity, Privileges Required, User Interaction, Scope, Confidentiality, Integrity, Availability |
| Temporal Score | Exploit Code Maturity, Remediation Level, Report Confidence |
| Environmental Score | Modified Base Metrics, Security Requirements |

Calculator: https://www.first.org/cvss/calculator/3.1

## CVE and Vulnerability Databases

- NVD (National Vulnerability Database): https://nvd.nist.gov/
- CVE: https://cve.mitre.org/
- Exploit-DB: https://www.exploit-db.com/
- VulnDB: https://vuldb.com/

---

## Workflows

## End-to-End Workflow

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│ Pre-Engagement   │───>│  Reconnaissance   │───>│ Vulnerability        │
│ - Scoping        │    │  - Passive OSINT  │    │ Analysis             │
│ - RoE signing    │    │  - Active scanning│    │ - Automated scans    │
│ - Legal docs     │    │  - Enum subdomains│    │ - Manual validation  │
└─────────────────┘    └──────────────────┘    └─────────────────────┘
                                                          │
┌─────────────────┐    ┌──────────────────┐    ┌──────────▼──────────┐
│   Reporting      │<───│ Post-Exploitation │<───│   Exploitation       │
│ - Findings doc   │    │  - Priv escalation│    │ - Service exploits   │
│ - CVSS scoring   │    │  - Persistence    │    │ - Web app attacks    │
│ - Remediation    │    │  - Pivoting proof  │    │ - Password attacks   │
│ - Executive brief│    │  - Evidence gather │    │ - Credential spray   │
└─────────────────┘    └──────────────────┘    └─────────────────────┘
```

## Daily Testing Workflow

```
Morning:
  1. Review previous day's findings
  2. Update target list with new discoveries
  3. Run updated scans on newly discovered hosts
  4. Verify scan results and triage

Afternoon:
  5. Manual exploitation of high-value targets
  6. Attempt lateral movement from compromised hosts
  7. Document all successful and failed exploitation attempts

Evening:
  8. Compile evidence and screenshots
  9. Update findings tracker
  10. Plan next day's attack vectors
  11. Communicate critical findings to client immediately
```

## Reconnaissance Sub-Workflow

```
Domain Target
    │
    ├── DNS Enumeration ──> Subdomain Discovery ──> IP Resolution
    │                                                    │
    ├── WHOIS/ASN Lookup ──> IP Range Identification ────┤
    │                                                    │
    ├── Certificate Transparency ──> Hidden Subdomains ──┤
    │                                                    │
    ├── Shodan/Censys ──> Service Fingerprinting ────────┤
    │                                                    │
    └── OSINT (GitHub, Pastebin) ──> Credential Leaks    │
                                                         ▼
                                              Master Target List
                                           (IPs, Ports, Services)
```

## Vulnerability Triage Workflow

```
Scan Results
    │
    ├── Critical (CVSS >= 9.0) ──> Immediate exploitation attempt
    │                               ──> Notify client if RCE confirmed
    │
    ├── High (CVSS 7.0-8.9) ──> Validate and exploit within 24h
    │
    ├── Medium (CVSS 4.0-6.9) ──> Validate, exploit if time permits
    │
    └── Low/Info (CVSS < 4.0) ──> Document, include in final report
```

## Evidence Collection Workflow

```
For each successful exploitation:
  1. Screenshot the exploit execution
  2. Record terminal output (script command or asciinema)
  3. Capture network traffic (tcpdump/Wireshark)
  4. Document exact commands/payloads used
  5. Note timestamps (UTC)
  6. Hash any files extracted (SHA-256)
  7. Store evidence in organized folder structure:
     evidence/
     ├── {date}/
     │   ├── {target-ip}/
     │   │   ├── screenshots/
     │   │   ├── terminal_logs/
     │   │   ├── pcaps/
     │   │   └── notes.md
```

---

## Working Template

## Document Control

| Field | Value |
|-------|-------|
| Client | [Client Name] |
| Assessment Type | External Network Penetration Test |
| Test Period | [Start Date] — [End Date] |
| Report Version | 1.0 |
| Classification | CONFIDENTIAL |
| Prepared By | [Tester Name], [Certification] |
| Reviewed By | [QA Reviewer] |
| Authorization ID | [PENTEST-YYYY-EXT-NNN] |

---

## 1. Executive Summary

### 1.1 Engagement Overview
[Organization Name] engaged [Testing Company] to perform an external network penetration test against its internet-facing infrastructure. The assessment was conducted between [dates] following the PTES methodology.

### 1.2 Scope
- **IP Ranges:** [CIDR ranges]
- **Domains:** [domain list]
- **Exclusions:** [excluded assets]

### 1.3 Key Findings Summary

| Severity | Count |
|----------|-------|
| Critical | [N] |
| High | [N] |
| Medium | [N] |
| Low | [N] |
| Informational | [N] |

### 1.4 Overall Risk Rating
**[CRITICAL / HIGH / MEDIUM / LOW]**

[Brief narrative of overall security posture]

### 1.5 Top Strategic Recommendations
1. [Recommendation 1]
2. [Recommendation 2]
3. [Recommendation 3]

---

## 2. Technical Findings

### Finding [N]: [Title]

| Attribute | Detail |
|-----------|--------|
| Severity | [Critical/High/Medium/Low] |
| CVSS v3.1 | [Score] — [Vector String] |
| CVE | [CVE-YYYY-NNNNN] |
| CWE | [CWE-NNN] |
| Affected Asset | [IP/hostname:port] |
| Status | [Exploited / Validated / Potential] |

**Description:**
[Detailed description of the vulnerability]

**Impact:**
[Business and technical impact]

**Steps to Reproduce:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Evidence:**
![Screenshot](./evidence/finding_N_screenshot.png)

```
[Terminal output / HTTP request-response]
```

**Remediation:**
- [Primary fix]
- [Alternative mitigation]
- [Detection recommendation]

**References:**
- [URL to CVE/advisory]
- [Vendor documentation]

---

## 3. Methodology

### 3.1 Framework
- PTES (Penetration Testing Execution Standard)
- OWASP Testing Guide v4.2
- MITRE ATT&CK Framework

### 3.2 Tools Used

| Tool | Version | Purpose |
|------|---------|---------|
| Nmap | [ver] | Port scanning, service enumeration |
| Metasploit | [ver] | Exploitation framework |
| Burp Suite Pro | [ver] | Web application testing |
| Nuclei | [ver] | Vulnerability scanning |
| SQLMap | [ver] | SQL injection testing |
| Hashcat | [ver] | Password cracking |

### 3.3 Testing Timeline

| Date | Phase | Activities |
|------|-------|-----------|
| [Date] | Reconnaissance | OSINT, subdomain enum, port scanning |
| [Date] | Vulnerability Analysis | Automated and manual scanning |
| [Date] | Exploitation | Service and web application exploitation |
| [Date] | Post-Exploitation | Privilege escalation, evidence collection |
| [Date] | Reporting | Findings documentation and QA |

---

## 4. Appendices

### A. Full Scan Results
[Attached as separate files]

### B. Network Topology Discovered
[Network diagram]

### C. Credentials Obtained
| Source | Account Type | Method |
|--------|-------------|--------|
| [Service] | [Role] | [Attack method] |

### D. Glossary

| Term | Definition |
|------|-----------|
| CVSS | Common Vulnerability Scoring System |
| CVE | Common Vulnerabilities and Exposures |
| RCE | Remote Code Execution |
| PTES | Penetration Testing Execution Standard |

---

*This document is classified CONFIDENTIAL and intended solely for [Client Name].*
