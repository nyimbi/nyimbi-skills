# Performing Open Source Intelligence Gathering

## API Reference

## Libraries Used
- **requests**: HTTP requests for tech fingerprinting and social media checks
- **dns.resolver** (dnspython): DNS record enumeration and subdomain discovery
- **python-whois**: Domain WHOIS registration data
- **re**: Email pattern extraction
- **socket**: Network connectivity

## CLI Interface
```
python agent.py whois --domain example.com
python agent.py dns --domain example.com
python agent.py email --domain example.com
python agent.py tech --url https://example.com
python agent.py social --name "John Doe"
```

## Core Functions

### `whois_lookup(domain)` — Domain registration data
Returns registrar, creation/expiration dates, name servers, registrant info.

### `dns_enumeration(domain)` — DNS record and subdomain discovery
Queries 7 record types. Tests 15 common subdomain prefixes.

### `email_harvest(domain)` — Email address discovery
Uses Hunter.io API and regex pattern matching.

### `technology_fingerprint(url)` — Web technology identification
Detects: web server, framework, CMS. Audits 6 security headers.

### `social_media_search(target_name)` — Profile enumeration
Checks: LinkedIn, Twitter/X, GitHub, Facebook, Instagram.

## Security Headers Checked
Strict-Transport-Security, Content-Security-Policy, X-Frame-Options,
X-Content-Type-Options, X-XSS-Protection, Referrer-Policy

## Dependencies
```
pip install requests dnspython python-whois
```

---

## Standards and Controls

## MITRE ATT&CK - Reconnaissance (TA0043)

| Technique ID | Name | Description |
|-------------|------|-------------|
| T1595.001 | Active Scanning: Scanning IP Blocks | Scanning target IP ranges for active hosts |
| T1595.002 | Active Scanning: Vulnerability Scanning | Scanning for vulnerabilities on discovered hosts |
| T1592.001 | Gather Victim Host Information: Hardware | Identifying target hardware configurations |
| T1592.002 | Gather Victim Host Information: Software | Identifying installed software and versions |
| T1592.004 | Gather Victim Host Information: Client Configurations | Discovering client-side configurations |
| T1589.001 | Gather Victim Identity Information: Credentials | Searching for exposed credentials |
| T1589.002 | Gather Victim Identity Information: Email Addresses | Harvesting email addresses |
| T1589.003 | Gather Victim Identity Information: Employee Names | Collecting employee information |
| T1590.001 | Gather Victim Network Information: Domain Properties | DNS and domain enumeration |
| T1590.002 | Gather Victim Network Information: DNS | DNS record collection |
| T1590.004 | Gather Victim Network Information: Network Topology | Mapping network architecture |
| T1590.005 | Gather Victim Network Information: IP Addresses | Identifying target IP addresses |
| T1591.001 | Gather Victim Org Information: Determine Physical Locations | Physical location mapping |
| T1591.002 | Gather Victim Org Information: Business Relationships | Identifying vendors and partners |
| T1591.004 | Gather Victim Org Information: Identify Roles | Mapping organizational roles |
| T1593.001 | Search Open Websites/Domains: Social Media | Social media intelligence |
| T1593.002 | Search Open Websites/Domains: Search Engines | Google dorking and search engine recon |
| T1594 | Search Victim-Owned Websites | Analyzing target websites |
| T1596.001 | Search Open Technical Databases: DNS/Passive DNS | Passive DNS intelligence |
| T1596.005 | Search Open Technical Databases: Scan Databases | Shodan, Censys, ZoomEye queries |
| T1597.001 | Search Closed Sources: Threat Intel Vendors | Threat intelligence platform queries |

## PTES - Intelligence Gathering

### Level 1: Passive Information Gathering
- WHOIS lookups
- DNS enumeration
- Search engine queries
- Social media analysis
- Public records review

### Level 2: Semi-Passive Information Gathering
- Website analysis and spidering
- Metadata extraction from documents
- Job posting analysis
- Technology stack identification

### Level 3: Active Information Gathering
- Port scanning
- Service enumeration
- Web application fingerprinting
- Active subdomain brute-forcing

## OSSTMM - Information Security Testing

### Section 5: Human Security Testing
- Social engineering reconnaissance
- Personnel profiling
- Communication channel mapping

### Section 6: Physical Security Testing
- Location reconnaissance
- Access control assessment
- Surveillance analysis

## NIST SP 800-115 Section 3: Review Techniques
- Documentation review
- Log review
- Ruleset review
- System configuration review
- Network sniffing (passive)

---

## Workflows

## Workflow 1: Domain and Infrastructure Reconnaissance

### Step 1: Passive DNS and WHOIS
```bash
# WHOIS lookup
whois targetdomain.com

# DNS record enumeration
dig targetdomain.com ANY
dig targetdomain.com MX
dig targetdomain.com TXT
dig targetdomain.com NS

# Reverse DNS
dig -x <IP_ADDRESS>

# Zone transfer attempt
dig axfr @ns1.targetdomain.com targetdomain.com
```

### Step 2: Subdomain Enumeration
```bash
# Using Subfinder for passive enumeration
subfinder -d targetdomain.com -o subdomains.txt

# Using Amass for comprehensive enumeration
amass enum -passive -d targetdomain.com -o amass_results.txt

# Certificate Transparency log search
curl -s "https://crt.sh/?q=%.targetdomain.com&output=json" | jq -r '.[].name_value' | sort -u

# Using httpx to probe discovered subdomains
cat subdomains.txt | httpx -status-code -title -tech-detect -o live_subdomains.txt
```

### Step 3: IP Range and ASN Discovery
```bash
# ASN lookup
whois -h whois.radb.net -- '-i origin AS12345'

# BGP prefix lookup via Hurricane Electric
curl -s "https://bgp.he.net/AS12345#_prefixes"

# Shodan search for organization
shodan search "org:Target Corporation" --fields ip_str,port,product
```

### Step 4: Cloud Asset Discovery
```bash
# AWS S3 bucket enumeration
python3 cloud_enum.py -k targetcorp -l cloud_results.txt

# Azure blob storage check
for name in targetcorp targetcorp-dev targetcorp-backup; do
  curl -s -o /dev/null -w "%{http_code}" "https://${name}.blob.core.windows.net/"
done

# GCP bucket check
gsutil ls gs://targetcorp-*
```

## Workflow 2: Personnel Intelligence

### Step 1: Employee Enumeration
```bash
# theHarvester for email and name harvesting
theHarvester -d targetdomain.com -b all -l 500 -f harvest_results

# LinkedIn enumeration (manual + tools)
# Use LinkedIn search operators:
# site:linkedin.com/in "targetcorp" "security engineer"
# site:linkedin.com/in "targetcorp" "system administrator"

# CrossLinked for LinkedIn name harvesting
python3 crosslinked.py -f '{first}.{last}@targetdomain.com' "Target Corporation"
```

### Step 2: Email Validation
```bash
# Verify email format using Hunter.io API
curl "https://api.hunter.io/v2/domain-search?domain=targetdomain.com&api_key=YOUR_KEY"

# SMTP verification (careful - can be logged)
# Use tools like EmailHippo or NeverBounce for passive verification
```

### Step 3: Social Media Profiling
```bash
# Sherlock for username enumeration across platforms
python3 sherlock username --timeout 5 --output sherlock_results.txt

# Social media searching
# Twitter advanced search: from:username targetcorp
# Instagram: #targetcorp
# GitHub: org:targetcorp
```

## Workflow 3: Credential and Data Leak Discovery

### Step 1: Breach Database Search
```bash
# Have I Been Pwned API check
curl "https://haveibeenpwned.com/api/v3/breachedaccount/user@targetdomain.com" \
  -H "hibp-api-key: YOUR_KEY"

# DeHashed search (requires subscription)
curl "https://api.dehashed.com/search?query=domain:targetdomain.com" \
  -u email:api_key
```

### Step 2: GitHub Secret Scanning
```bash
# GitDorker for GitHub dorking
python3 GitDorker.py -tf tokens.txt -d dorks/alldorksv3 -q targetdomain.com

# truffleHog for repository scanning
trufflehog github --org=targetcorp --only-verified

# Manual GitHub dorking
# Search: "targetdomain.com" password
# Search: "targetdomain.com" api_key
# Search: "targetcorp" filename:.env
# Search: "targetcorp" filename:wp-config.php
```

### Step 3: Google Dorking
```
# Sensitive files
site:targetdomain.com filetype:pdf
site:targetdomain.com filetype:xlsx
site:targetdomain.com filetype:docx confidential

# Configuration files
site:targetdomain.com filetype:xml
site:targetdomain.com filetype:conf
site:targetdomain.com filetype:env

# Login pages and admin panels
site:targetdomain.com inurl:admin
site:targetdomain.com inurl:login
site:targetdomain.com intitle:"index of"

# Error messages with sensitive info
site:targetdomain.com "error" "sql" "syntax"
site:targetdomain.com "php error" "on line"
```

## Workflow 4: Technology Stack Identification

### Step 1: Web Technology Fingerprinting
```bash
# Wappalyzer CLI
wappalyzer https://targetdomain.com

# WhatWeb for technology identification
whatweb targetdomain.com -v

# Nuclei for technology detection
nuclei -u https://targetdomain.com -t technologies/
```

### Step 2: Service and Version Detection
```bash
# Nmap service detection (active - requires authorization)
nmap -sV -sC -p- targetdomain.com -oA nmap_results

# Shodan host lookup
shodan host <IP_ADDRESS>

# Censys host search
censys search "services.tls.certificates.leaf_data.subject.organization:Target Corp"
```

### Step 3: Job Posting Analysis
```
# Search job boards for technology mentions:
# LinkedIn Jobs: "Target Corporation" AND ("AWS" OR "Azure" OR "GCP")
# Indeed: "Target Corporation" "security" tools
# Glassdoor: Target Corporation technology stack

# Look for mentions of:
# - Cloud platforms (AWS, Azure, GCP)
# - Security tools (CrowdStrike, Carbon Black, Splunk)
# - Development languages and frameworks
# - Network equipment vendors (Cisco, Palo Alto, Fortinet)
# - Identity providers (Okta, Azure AD, Ping Identity)
```

## Workflow 5: Physical Intelligence

### Step 1: Location Mapping
```
# Google Maps reconnaissance:
# - Office locations and building layouts
# - Parking areas and entry points
# - Nearby businesses for staging
# - Delivery entrance locations

# Google Street View:
# - Access control systems (card readers, turnstiles)
# - Security camera locations
# - Badge/lanyard colors and designs
# - Building signage
```

### Step 2: Document Metadata Extraction
```bash
# ExifTool for document metadata
exiftool -r -ext pdf -ext docx -ext xlsx ./downloaded_documents/

# FOCA for metadata analysis (Windows)
# Import documents and analyze:
# - Author names and usernames
# - Software versions
# - Internal file paths
# - Printer names and network paths
```

## Workflow 6: OSINT Report Compilation

### Report Structure
```
1. Executive Summary
   - Key findings overview
   - Risk assessment

2. Attack Surface Map
   - External infrastructure diagram
   - Domain and subdomain inventory
   - Exposed services and applications

3. Personnel Intelligence
   - Key personnel profiles
   - Email address list
   - Organizational chart

4. Credential Exposure
   - Breach database findings
   - Leaked secrets and API keys
   - Password pattern analysis

5. Technology Stack
   - Identified technologies and versions
   - Known vulnerabilities for detected versions
   - Security tool coverage gaps

6. Recommended Attack Vectors
   - Prioritized initial access options
   - Social engineering target list
   - Technical vulnerability targets
```

---

## Working Template

## Document Control

| Field | Value |
|-------|-------|
| Target Organization | [NAME] |
| Target Domain(s) | [DOMAINS] |
| Engagement ID | [ID] |
| Collector | [NAME] |
| Date | [DATE] |
| Classification | CONFIDENTIAL |

---

## 1. Executive Summary

[Brief overview of OSINT findings and their impact on attack planning]

**Key Findings:**
- [Finding 1]
- [Finding 2]
- [Finding 3]

**Recommended Attack Vectors:**
1. [Vector 1 based on OSINT]
2. [Vector 2 based on OSINT]

---

## 2. External Attack Surface

### 2.1 Domain Inventory

| Domain | Registrar | Nameservers | Expiry Date |
|--------|-----------|-------------|-------------|
| | | | |

### 2.2 Subdomain Enumeration

| Subdomain | IP Address | Service | Status |
|-----------|-----------|---------|--------|
| | | | Active/Inactive |

### 2.3 IP Range and ASN

| ASN | Organization | IP Range | Country |
|-----|-------------|----------|---------|
| | | | |

### 2.4 Cloud Assets

| Provider | Asset Type | Identifier | Public Access |
|----------|-----------|------------|---------------|
| AWS | S3 Bucket | | Yes/No |
| Azure | Blob Storage | | Yes/No |
| GCP | Storage | | Yes/No |

---

## 3. Personnel Intelligence

### 3.1 Key Personnel

| Name | Title | Department | LinkedIn | Email |
|------|-------|------------|----------|-------|
| | | | | |

### 3.2 Email Format
- **Confirmed Format:** [first.last@domain.com]
- **Validation Method:** [How confirmed]

### 3.3 Social Engineering Targets

| Target | Role | Justification | Risk Level |
|--------|------|---------------|------------|
| | | | High/Medium/Low |

---

## 4. Technology Stack

### 4.1 Web Technologies

| Component | Technology | Version | Notes |
|-----------|-----------|---------|-------|
| Web Server | | | |
| Framework | | | |
| CMS | | | |
| CDN | | | |
| WAF | | | |

### 4.2 Security Posture

| Security Header | Status | Rating |
|----------------|--------|--------|
| HSTS | Present/Missing | |
| CSP | Present/Missing | |
| X-Frame-Options | Present/Missing | |
| X-Content-Type-Options | Present/Missing | |

### 4.3 Infrastructure

| Service | Product | Version | Port |
|---------|---------|---------|------|
| VPN | | | |
| Email | | | |
| Remote Access | | | |

---

## 5. Credential Exposure

### 5.1 Breach Database Results

| Source | Date | Records | Type |
|--------|------|---------|------|
| | | | Passwords/Hashes/Emails |

### 5.2 Code Repository Leaks

| Repository | File | Type of Secret | Status |
|-----------|------|----------------|--------|
| | | API Key/Password/Token | Active/Rotated |

### 5.3 Paste Site Findings

| Site | Date | Content Type | Relevance |
|------|------|-------------|-----------|
| | | | High/Medium/Low |

---

## 6. Physical Intelligence

### 6.1 Office Locations

| Address | Type | Access Controls | Notes |
|---------|------|-----------------|-------|
| | HQ/Branch/DC | | |

### 6.2 Physical Security Observations

| Observation | Location | Photo Reference |
|-------------|----------|-----------------|
| | | |

---

## 7. Attack Surface Summary

### 7.1 Priority Targets

| # | Target | Type | Rationale | Risk |
|---|--------|------|-----------|------|
| 1 | | Technical/Human/Physical | | Critical/High/Medium |

### 7.2 Recommended Initial Access Methods

| Method | MITRE ATT&CK | Likelihood | Required Resources |
|--------|-------------|------------|-------------------|
| Spearphishing | T1566.001 | | |
| Credential Stuffing | T1078 | | |
| External Exploit | T1190 | | |

---

## Appendix A: Raw Data Files

| File | Description | Location |
|------|-------------|----------|
| subdomains.txt | Full subdomain list | |
| emails.txt | Discovered email addresses | |
| dorks.txt | Google dorking queries | |
| tech_fingerprint.json | Technology details | |

## Appendix B: Tools Used

| Tool | Version | Purpose |
|------|---------|---------|
| | | |

## Appendix C: MITRE ATT&CK Techniques Used

| Technique ID | Name | Result |
|-------------|------|--------|
| T1593.002 | Search Engines | |
| T1596.005 | Scan Databases | |
| T1589.002 | Email Addresses | |
