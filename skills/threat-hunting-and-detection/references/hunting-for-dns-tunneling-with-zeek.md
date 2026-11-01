# Hunting For DNS Tunneling With Zeek

## API Reference

## Detection Heuristics

| Indicator | Threshold | Score |
|-----------|-----------|-------|
| Shannon entropy | > 3.5 | +40 |
| Avg subdomain length | > 30 chars | +30 |
| Tunnel query type ratio | > 50% TXT/NULL/CNAME | +20 |
| High query volume | > 500 queries | +10 |

## Zeek dns.log Fields

| Index | Field | Description |
|-------|-------|-------------|
| 0 | `ts` | Timestamp |
| 2 | `id.orig_h` | Source IP |
| 4 | `id.resp_h` | DNS server |
| 9 | `query` | Query name |
| 13 | `qtype_name` | Query type (A, TXT, etc.) |
| 21 | `answers` | Response answers |

## DNS Tunneling Tools (for detection reference)

| Tool | Encoding | Query Type |
|------|----------|-----------|
| iodine | Base128 | NULL, TXT |
| dnscat2 | Hex/Base64 | CNAME, TXT, MX |
| dns2tcp | Base64 | TXT |
| Cobalt Strike | Hex | A, AAAA, TXT |

## Shannon Entropy Reference

| Data Type | Entropy |
|-----------|---------|
| Normal hostnames | 2.0 - 3.0 |
| Base32 encoded | 3.5 - 4.0 |
| Base64 encoded | 4.0 - 5.0 |
| Hex encoded | 3.5 - 4.0 |

## Python Libraries

| Library | Use |
|---------|-----|
| `math` | Entropy calculation |
| `csv` | TSV log parsing |
| `collections.defaultdict` | Domain aggregation |
| `dpkt` | PCAP DNS parsing |
| `dnslib` | DNS packet construction |

## Zeek Scripts for DNS Analysis

```zeek
@load base/protocols/dns
redef DNS::max_pending_queries = 1000;
event dns_request(c: connection, msg: dns_msg, query: string, qtype: count) {
    if (|query| > 50) print fmt("Long query: %s", query);
}
```

---

## Standards and Controls

## MITRE ATT&CK References

| Technique | Name | Description |
|-----------|------|-------------|
| T1071.004 | Application Layer Protocol: DNS | DNS-based C2 communication |
| T1048.003 | Exfiltration Over Unencrypted Non-C2 Protocol | Data theft via DNS |
| T1572 | Protocol Tunneling | IP-over-DNS tunneling |
| T1568.002 | Domain Generation Algorithms | Algorithmically generated domains |
| T1132.001 | Data Encoding: Standard Encoding | Base32/64 in DNS queries |

## DNS Tunneling Detection Thresholds

| Indicator | Threshold | Rationale |
|-----------|-----------|-----------|
| Query length | > 50 characters | Normal queries average 20-30 chars |
| Subdomain label length | > 30 characters | Max label is 63; tunneling uses near-max |
| Subdomain entropy | > 3.5 bits/char | Base32/64 encoding produces high entropy |
| Unique subdomains per domain | > 100/hour | Legitimate domains have few unique subs |
| Query volume to single domain | > 100/hour | Sustained high volume indicates tunneling |
| TXT record query ratio | > 50% to domain | TXT queries carry more data |
| NULL record queries | Any volume | Rarely used legitimately |

## DNS Tunneling Tools

| Tool | Protocol | Record Types | Data Rate | Detection Difficulty |
|------|----------|-------------|-----------|---------------------|
| iodine | IP-over-DNS | NULL, TXT, CNAME, A | ~100 Kbps | Medium |
| dnscat2 | C2 over DNS | TXT, CNAME, MX | ~10 Kbps | Medium |
| DNSExfiltrator | Exfil over DNS | TXT, A | ~5 Kbps | Medium-Hard |
| Cobalt Strike DNS | C2 | A, TXT | Variable | Hard |
| dns2tcp | TCP-over-DNS | TXT, KEY | ~50 Kbps | Medium |
| Heyoka | DNS exfiltration | All types | Variable | Hard |

## Zeek Log Fields for DNS Analysis

| Field | Description | Tunnel Relevance |
|-------|-------------|-----------------|
| query | Full DNS query name | Length and entropy analysis |
| qtype_name | Query record type | TXT/NULL/CNAME anomalies |
| answers | Response content | Response size analysis |
| rcode_name | Response code | NXDOMAIN patterns |
| id.orig_h | Source IP | Source identification |
| AA | Authoritative answer | Non-authoritative responses |
| rejected | Query rejected | Filtering effectiveness |

---

## Workflows

## Phase 1: Query Length and Volume Analysis

### Step 1.1 - Identify Domains with Long Queries
```spl
index=zeek sourcetype=bro_dns
| eval query_len=len(query)
| where query_len > 50
| rex field=query "\.(?<basedomain>[^.]+\.[^.]+)$"
| stats count avg(query_len) as avg_len max(query_len) as max_len dc(query) as unique_queries by id.orig_h basedomain
| where count > 50
| sort -avg_len
```

### Step 1.2 - High Volume DNS to Single Domain
```spl
index=zeek sourcetype=bro_dns
| rex field=query "\.(?<basedomain>[^.]+\.[^.]+)$"
| bin _time span=1h
| stats count by id.orig_h basedomain _time
| where count > 100
| sort -count
```

## Phase 2: Entropy Analysis

### Step 2.1 - Shannon Entropy Calculation
```python
import math
from collections import Counter

def shannon_entropy(text):
    if not text:
        return 0.0
    counts = Counter(text)
    length = len(text)
    return -sum((c/length) * math.log2(c/length) for c in counts.values())

# Flag subdomains with entropy > 3.5
```

### Step 2.2 - Splunk Entropy Approximation
```spl
index=zeek sourcetype=bro_dns
| rex field=query "^(?<subdomain>[^.]+)"
| where len(subdomain) > 20
| eval has_numbers=if(match(subdomain, "[0-9]"), 1, 0)
| eval has_mixed_case=if(match(subdomain, "[A-Z]") AND match(subdomain, "[a-z]"), 1, 0)
| stats count avg(len(subdomain)) as avg_sub_len sum(has_numbers) as numeric_count by id.orig_h basedomain
| eval numeric_ratio=numeric_count/count
| where avg_sub_len > 25 AND numeric_ratio > 0.3
```

## Phase 3: Record Type Analysis

### Step 3.1 - Unusual Record Types
```spl
index=zeek sourcetype=bro_dns
| where qtype_name IN ("TXT", "NULL", "CNAME", "MX", "KEY", "SRV")
| rex field=query "\.(?<basedomain>[^.]+\.[^.]+)$"
| stats count dc(query) as unique by id.orig_h basedomain qtype_name
| where count > 50
| sort -count
```

## Phase 4: RITA Automated Analysis

```bash
# Full Zeek log import and DNS analysis
rita import /opt/zeek/logs/current dns_hunt
rita show-dns-tunneling dns_hunt
rita show-exploded-dns dns_hunt | sort -k2 -n -r | head -20
```

## Phase 5: Correlation and Response

### Step 5.1 - Map DNS Source to Endpoint
Correlate dns.log source IPs with DHCP logs or endpoint inventory to identify affected hosts and processes.

### Step 5.2 - Response Actions
1. DNS sinkhole the identified tunneling domain
2. Block at DNS resolver and firewall
3. Isolate source endpoint
4. Capture memory and disk forensics
5. Assess scope of data exfiltration

---

## Working Template

## Hunt Metadata
| Field | Value |
|-------|-------|
| Hunt ID | TH-DNSTUNNEL-YYYY-MM-DD-NNN |
| Analyst | |
| Date | |
| Status | [ ] In Progress / [ ] Complete |

## Hypothesis
> Adversaries are using DNS tunneling to establish covert C2 channels or exfiltrate data by encoding information in DNS query subdomain labels.

## DNS Tunneling Findings

| # | Source IP | Host | Domain | Queries | Unique Subs | Avg Length | Entropy | Record Types | Risk |
|---|----------|------|--------|---------|-------------|-----------|---------|-------------|------|
| 1 | | | | | | | | | |

## Data Exfiltration Estimate

| Domain | Total Queries | Avg Subdomain Size | Estimated Data Volume | Assessment |
|--------|--------------|--------------------|-----------------------|------------|
| | | | | |

## Recommendations
1. **Sinkhole**: [DNS domains to sinkhole]
2. **Block**: [Domains at DNS resolver and firewall]
3. **Isolate**: [Source endpoints for investigation]
4. **Monitor**: [Deploy DNS tunneling detection rules]
