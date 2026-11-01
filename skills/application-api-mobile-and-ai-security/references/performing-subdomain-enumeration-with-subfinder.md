# Performing Subdomain Enumeration With Subfinder

## API Reference

## Subfinder CLI Options

| Flag | Description |
|------|-------------|
| `-d <domain>` | Target domain to enumerate |
| `-dL <file>` | File containing list of domains |
| `-o <file>` | Output file for results |
| `-oJ` | JSON lines output format |
| `-oD <dir>` | Output directory (one file per domain) |
| `-all` | Use all passive sources (slower, more thorough) |
| `-silent` | Show only subdomains in output |
| `-recursive` | Enumerate subdomains of discovered subdomains |
| `-s <src1,src2>` | Use only specified sources |
| `-es <src>` | Exclude specific sources |
| `-cs` | Show source for each subdomain |
| `-rate-limit <n>` | Max requests per second |
| `-t <n>` | Number of concurrent threads |

## httpx CLI Options

| Flag | Description |
|------|-------------|
| `-l <file>` | Input file with hosts |
| `-ports <p1,p2>` | Ports to probe |
| `-status-code` | Show HTTP status code |
| `-title` | Show page title |
| `-tech-detect` | Detect web technologies |
| `-json` | JSON output format |
| `-silent` | Suppress banner |

## dnsx CLI Options

| Flag | Description |
|------|-------------|
| `-l <file>` | Input file with hosts |
| `-a` | Resolve A records |
| `-cname` | Resolve CNAME records |
| `-resp` | Show response data |
| `-json` | JSON output |

## Passive Sources

| Source | API Key Required |
|--------|-----------------|
| crt.sh | No |
| VirusTotal | Yes |
| Shodan | Yes |
| SecurityTrails | Yes |
| Censys | Yes |
| Chaos (ProjectDiscovery) | Yes |
| AlienVault OTX | No |
| HackerTarget | No |

## Python Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| `subprocess` | stdlib | Execute subfinder, httpx, dnsx CLI |
| `json` | stdlib | Parse JSON lines output |
| `pathlib` | stdlib | File path management |

## References

- Subfinder GitHub: https://github.com/projectdiscovery/subfinder
- httpx GitHub: https://github.com/projectdiscovery/httpx
- dnsx GitHub: https://github.com/projectdiscovery/dnsx
- Subfinder Config: https://docs.projectdiscovery.io/tools/subfinder/install

---

## Standards and Controls

## Industry Standards
- **OWASP Testing Guide v4.2** — OTG-INFO-004: Enumerate applications on web server through subdomain discovery
- **PTES (Penetration Testing Execution Standard)** — Intelligence Gathering phase requiring comprehensive asset enumeration
- **NIST SP 800-115** — Technical Guide to Information Security Testing and Assessment, passive reconnaissance methods
- **MITRE ATT&CK T1596** — Search Open Technical Databases for target infrastructure information

## Tool References
- Subfinder GitHub: https://github.com/projectdiscovery/subfinder
- ProjectDiscovery Documentation: https://docs.projectdiscovery.io/tools/subfinder/overview
- Certificate Transparency RFC 6962: https://www.rfc-editor.org/rfc/rfc6962
- crt.sh Certificate Search: https://crt.sh/

## API Provider Documentation
- Shodan API: https://developer.shodan.io/api
- Censys Search API: https://search.censys.io/api
- VirusTotal API v3: https://docs.virustotal.com/reference/overview
- SecurityTrails API: https://docs.securitytrails.com/reference
- Chaos ProjectDiscovery: https://chaos.projectdiscovery.io/

## Regulatory Considerations
- Passive subdomain enumeration does not involve active scanning and is generally legal
- Always verify scope and authorization before proceeding to active enumeration
- Bug bounty programs define specific scope for subdomain testing
- GDPR may apply when collecting data that reveals organizational structure

---

## Workflows

## Standard Enumeration Workflow
1. Configure API keys in provider-config.yaml for maximum source coverage
2. Run subfinder with `-all` flag against target domain(s)
3. Deduplicate results and remove out-of-scope entries
4. Validate live hosts with httpx including status codes and technologies
5. Resolve DNS records with dnsx to map IP infrastructure
6. Screenshot live hosts with gowitness for visual review
7. Feed live hosts into vulnerability scanner (nuclei) for automated checks

## Continuous Monitoring Workflow
1. Schedule subfinder runs via cron (daily or weekly)
2. Compare new results against baseline subdomain list
3. Alert on newly discovered subdomains via webhook or email
4. Automatically scan new subdomains for known vulnerabilities
5. Update asset inventory with new discoveries

## Bug Bounty Recon Pipeline
1. Collect target domains from bug bounty program scope
2. Run subfinder + amass + findomain for maximum coverage
3. Merge and deduplicate all results
4. Filter results to in-scope assets only
5. Probe for live HTTP services with httpx
6. Run nuclei templates for quick wins
7. Manually investigate interesting subdomains (dev, staging, api, admin)

## Integration Commands
```bash
# Full pipeline example
subfinder -d target.com -all -silent | \
  httpx -silent -status-code -title -tech-detect | \
  tee live_hosts.txt | \
  nuclei -t cves/ -t exposures/ -t misconfigurations/ -o findings.txt

# Delta monitoring
subfinder -d target.com -silent > today_subs.txt
comm -13 <(sort baseline_subs.txt) <(sort today_subs.txt) > new_subs.txt
```

---

## Working Template

## Engagement Details
- **Target Domain**: [domain]
- **Date**: [date]
- **Assessor**: [name]
- **Scope**: Passive subdomain enumeration only

## Executive Summary
Performed passive subdomain enumeration against [domain] using Subfinder and complementary tools. Discovered [N] unique subdomains, of which [M] are live and responding to HTTP requests.

## Methodology
1. Passive subdomain enumeration using Subfinder with all available sources
2. DNS resolution and validation using dnsx
3. HTTP probing with httpx for live host identification
4. CNAME analysis for subdomain takeover risk assessment

## Results Summary

| Metric | Count |
|--------|-------|
| Total Subdomains Discovered | |
| Live HTTP Hosts | |
| Unique IP Addresses | |
| Subdomain Takeover Candidates | |
| Cloud-Hosted Subdomains | |

## Live Hosts

| Subdomain | IP Address | Status Code | Title | Technologies |
|-----------|-----------|-------------|-------|-------------|
| | | | | |

## Subdomain Takeover Risks

| Subdomain | CNAME Target | Service | Risk Level |
|-----------|-------------|---------|------------|
| | | | |

## Recommendations
1. Remove dangling DNS records for decommissioned services
2. Claim or remove CNAME records pointing to unclaimed cloud resources
3. Restrict access to development and staging subdomains
4. Implement continuous subdomain monitoring for new asset detection
5. Review cloud service configurations for publicly accessible resources
