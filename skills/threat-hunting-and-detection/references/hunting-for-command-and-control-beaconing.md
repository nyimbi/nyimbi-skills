# Hunting For Command And Control Beaconing

## API Reference

## Zeek Log Files

### conn.log Fields
| Index | Field | C2 Relevance |
|-------|-------|-------------|
| 0 | ts | Timing analysis |
| 2 | id.orig_h | Internal host |
| 4 | id.resp_h | C2 server |
| 5 | id.resp_p | C2 port |
| 8 | duration | Long = persistent C2 |
| 9 | orig_bytes | Upload size |
| 10 | resp_bytes | Download size |

### dns.log Fields
| Index | Field | C2 Relevance |
|-------|-------|-------------|
| 0 | ts | Query timing |
| 2 | id.orig_h | Querying host |
| 9 | query | Domain queried |
| 11 | answers | Resolution |
| 14 | qtype_name | Query type (TXT = tunneling) |

### http.log Fields
| Index | Field | C2 Relevance |
|-------|-------|-------------|
| 8 | host | C2 domain |
| 9 | uri | C2 path |
| 12 | user_agent | Identifies C2 framework |
| 13 | request_body_len | Upload size |
| 14 | response_body_len | Download size |

## C2 Framework Signatures

| Framework | User Agent | URI Pattern | Default Port |
|-----------|-----------|-------------|--------------|
| Cobalt Strike | Mozilla/5.0 | /submit.php, /activity | 443 |
| Metasploit | (varies) | /random 4-8 chars | 4444 |
| Empire | Mozilla/5.0 | /login/process.php | 443 |
| Sliver | (custom) | /random UUID | 443 |

## DNS Tunneling Indicators

| Indicator | Pattern |
|-----------|---------|
| Long subdomain | `[a-z0-9]{30,}\.domain\.com` |
| High query frequency | > 100 queries/hour to one domain |
| TXT record queries | Unusual volume of TXT lookups |
| High entropy | Shannon entropy > 3.5 in subdomain |

## JA3/JA3S TLS Fingerprinting

### JA3 Hash (Client)
```bash
# Zeek ssl.log field: ja3
# Known C2 JA3 hashes:
# Cobalt Strike: 72a589da586844d7f0818ce684948eea
# Metasploit: various
```

## Threat Intelligence Feeds

### Abuse.ch ThreatFox
```http
POST https://threatfox-api.abuse.ch/api/v1/
Content-Type: application/json

{"query": "search_ioc", "search_term": "1.2.3.4"}
```

### OTX AlienVault
```http
GET https://otx.alienvault.com/api/v1/indicators/IPv4/{ip}/general
X-OTX-API-KEY: {key}
```

## RITA Beacon Analysis
```bash
rita import /path/to/zeek/logs my_dataset
rita show-beacons my_dataset
rita show-long-connections my_dataset
rita show-dns-fqdn-pairs my_dataset
```

---

## Standards and Controls

## MITRE ATT&CK Command and Control (TA0011)

| Technique | Name | Indicators |
|-----------|------|-----------|
| T1071.001 | Web Protocols | HTTP/HTTPS periodic connections |
| T1071.004 | DNS | DNS query patterns, tunneling |
| T1573.001 | Symmetric Cryptography | Encrypted C2 channels |
| T1573.002 | Asymmetric Cryptography | TLS C2 with custom certs |
| T1572 | Protocol Tunneling | DNS over HTTPS, ICMP tunneling |
| T1568.002 | Domain Generation Algorithms | Random domain patterns |
| T1568.001 | Fast Flux DNS | Rapidly rotating IPs |
| T1132.001 | Standard Encoding | Base64 in C2 traffic |
| T1132.002 | Non-Standard Encoding | Custom encoding schemes |
| T1095 | Non-Application Layer Protocol | ICMP, raw TCP/UDP C2 |
| T1090 | Proxy | Multi-hop C2 infrastructure |
| T1090.002 | External Proxy | External relay points |
| T1102 | Web Service | Legitimate services for C2 |
| T1105 | Ingress Tool Transfer | Downloading tools via C2 |

## Beaconing Detection Thresholds

| Metric | Threshold | Notes |
|--------|-----------|-------|
| Coefficient of Variation | < 0.20 | Strong periodicity indicator |
| Min Beacon Interval | > 30 seconds | Below may be streaming |
| Unique Destinations | Single domain/IP | C2 typically targets 1 destination |
| Session Duration | > 24 hours | Persistent C2 activity |
| Data Size Consistency | < 20% variance | Heartbeat-like payload sizes |
| Connection Count | > 50/day | Meaningful sample for analysis |

## Known C2 Framework Signatures

| Framework | Default Interval | Jitter | Protocol | JA3 Hash |
|-----------|-----------------|--------|----------|----------|
| Cobalt Strike | 60s | 0-50% | HTTPS, DNS | Multiple known hashes |
| Metasploit Meterpreter | 5s | 0% | TCP, HTTP/S | Framework-dependent |
| Sliver | 60s | 0-30% | HTTPS, mTLS, WireGuard | Varies |
| Brute Ratel C4 | 60s | 10-30% | HTTPS, DNS | Varies |
| Havoc | 5s | 0-20% | HTTPS | Varies |
| Mythic | Configurable | Configurable | HTTP/S, TCP | Agent-dependent |
| Covenant | 10s | 10% | HTTP/S | .NET TLS |
| Empire/Starkiller | 5s | 0-20% | HTTP/S | Python TLS |

## Data Sources

| Source | Data Type | Use |
|--------|-----------|-----|
| Zeek conn.log | Connection metadata | Duration, bytes, frequency |
| Zeek dns.log | DNS queries | Domain analysis, DGA detection |
| Zeek http.log | HTTP headers | User-agent, URI patterns |
| Zeek ssl.log | TLS metadata | JA3, certificate analysis |
| Proxy logs | Full URL, user agent | Content inspection |
| Sysmon Event 3 | Network connections | Process-to-connection mapping |
| Sysmon Event 22 | DNS queries | DNS process attribution |
| NetFlow/IPFIX | Network flows | Volume and timing analysis |
| Firewall logs | Allow/deny with timing | Connection frequency |

## DNS Tunneling Indicators

| Indicator | Description |
|-----------|-------------|
| High query volume | > 100 queries/hour to single domain |
| Long subdomain labels | > 30 characters in subdomain |
| High entropy subdomains | Base32/64 encoded data |
| TXT record queries | Large TXT records for data transfer |
| NULL/CNAME responses | Unusual record types |
| Unique subdomain count | Many unique subdomains per domain |

---

## Workflows

## Phase 1: HTTP/HTTPS Beacon Detection

### Step 1.1 - Splunk Frequency Analysis
```spl
index=proxy OR index=firewall
| where NOT match(dest, "(?i)(microsoft|google|amazonaws|cloudflare|akamai)")
| bin _time span=1s
| stats count by src_ip dest _time
| streamstats current=f last(_time) as prev_time by src_ip dest
| eval interval=_time-prev_time
| stats count avg(interval) as avg_interval stdev(interval) as stdev_interval min(interval) as min_interval max(interval) as max_interval by src_ip dest
| where count > 50
| eval cv=stdev_interval/avg_interval
| where cv < 0.20 AND avg_interval > 30 AND avg_interval < 86400
| sort cv
| table src_ip dest count avg_interval stdev_interval cv
```

### Step 1.2 - KQL Beacon Detection
```kql
DeviceNetworkEvents
| where Timestamp > ago(24h)
| where RemoteIPType == "Public"
| summarize ConnectionTimes=make_list(Timestamp), Count=count() by DeviceName, RemoteIP, RemoteUrl
| where Count > 50
| extend Intervals = array_sort_asc(ConnectionTimes)
| mv-apply Intervals on (
    extend NextTime = next(Intervals)
    | where isnotempty(NextTime)
    | extend IntervalSec = datetime_diff('second', NextTime, Intervals)
    | summarize AvgInterval=avg(IntervalSec), StdDev=stdev(IntervalSec)
)
| extend CV = StdDev / AvgInterval
| where CV < 0.2 and AvgInterval > 30
```

## Phase 2: DNS Beaconing and Tunneling

### Step 2.1 - DNS Query Frequency Analysis
```spl
index=dns
| rex field=query "(?<subdomain>[^.]+)\.(?<domain>[^.]+\.[^.]+)$"
| stats count dc(subdomain) as unique_subdomains avg(len(query)) as avg_query_len by src_ip domain
| where count > 100 AND (unique_subdomains > 50 OR avg_query_len > 40)
| sort -count
```

### Step 2.2 - DNS Entropy Analysis
```spl
index=dns query_type IN ("TXT", "NULL", "CNAME", "MX")
| rex field=query "^(?<subdomain>[^.]+)"
| eval entropy=0
| foreach * [eval entropy=entropy]
| where len(subdomain) > 20
| stats count by src_ip query domain
| where count > 20
```

### Step 2.3 - RITA-Style Beacon Analysis
RITA automatically analyzes Zeek logs for:
- Connection frequency with jitter tolerance
- DNS tunneling indicators
- Long connection durations
- Unusual user agents

## Phase 3: JA3/JA4 TLS Fingerprinting

### Step 3.1 - Unusual TLS Fingerprints
```spl
index=zeek sourcetype=bro_ssl
| stats count dc(id.resp_h) as unique_dests values(id.resp_h) as destinations by ja3 ja3s
| where count > 10
| lookup ja3_known_bad ja3
| where match="true"
| table ja3 ja3s count unique_dests destinations
```

### Step 3.2 - Self-Signed Certificate Detection
```spl
index=zeek sourcetype=bro_ssl
| where validation_status!="ok"
| stats count by id.orig_h id.resp_h server_name validation_status
| where count > 10
| sort -count
```

## Phase 4: Process-Level Correlation

### Step 4.1 - Map Processes to Network Connections
```spl
index=sysmon EventCode=3
| where NOT match(DestinationIp, "^(10\.|172\.(1[6-9]|2[0-9]|3[01])\.|192\.168\.)")
| stats count values(DestinationPort) as ports dc(DestinationIp) as unique_ips by Image Computer
| where count > 50 AND unique_ips < 5
| sort -count
```

### Step 4.2 - Unusual Process Network Activity
```spl
index=sysmon EventCode=3
| where match(Image, "(?i)(notepad|calc|mspaint|write|wordpad)")
| stats count by Image DestinationIp DestinationPort Computer
```

## Phase 5: Domain Intelligence

### Step 5.1 - New/Young Domain Detection
Check domains seen in beaconing analysis:
- WHOIS creation date < 30 days
- Domain registered with privacy protection
- Hosting on bulletproof infrastructure
- No historical passive DNS data

### Step 5.2 - DGA Domain Detection
Indicators of algorithmically generated domains:
- High character entropy (> 3.5 bits per char)
- No dictionary words in domain
- Unusual TLD combinations
- Sequential registration patterns

## Phase 6: Verification and Response

### Step 6.1 - Confirm C2 Activity
1. Capture packet sample of suspected C2 traffic
2. Analyze TLS certificate details
3. Check domain/IP against multiple TI sources
4. Review endpoint process tree
5. Look for associated file drops or tool transfers

### Step 6.2 - Response Actions
1. Block C2 domain/IP at firewall and proxy
2. Isolate compromised endpoint(s)
3. Preserve forensic evidence
4. Reset credentials used on affected systems
5. Hunt for additional infected hosts using same IOCs

---

## Working Template

## Hunt Metadata
| Field | Value |
|-------|-------|
| Hunt ID | TH-C2-YYYY-MM-DD-NNN |
| Analyst | |
| Date | |
| Status | [ ] In Progress / [ ] Complete |

## Hypothesis
> [e.g., "Compromised endpoints are beaconing to adversary C2 infrastructure using HTTPS with regular intervals."]

## Beaconing Findings

| # | Source | Destination | Protocol | Interval | Jitter | Connections | Risk |
|---|--------|-------------|----------|----------|--------|-------------|------|
| 1 | | | | | | | |

## DNS Tunneling Findings

| # | Source | Domain | Query Count | Unique Subdomains | Avg Length | Risk |
|---|--------|--------|-------------|-------------------|-----------|------|
| 1 | | | | | | |

## IOC List
| Type | Value | Confidence | Source |
|------|-------|-----------|--------|
| Domain | | | |
| IP | | | |
| JA3 | | | |

## Recommendations
1. **Block**: [Domains/IPs to block]
2. **Isolate**: [Endpoints to contain]
3. **Detect**: [New signatures to deploy]
