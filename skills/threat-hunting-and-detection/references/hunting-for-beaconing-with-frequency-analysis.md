# Hunting For Beaconing With Frequency Analysis

## API Reference

## Beaconing Characteristics

| Characteristic | Description |
|---------------|-------------|
| Regular intervals | Connections at fixed time periods |
| Low jitter | Small variance in intervals |
| Persistent | Continues over hours/days |
| Consistent size | Similar packet sizes |

## Jitter Calculation

### Standard Deviation of Intervals
```python
import math
intervals = [t[i+1] - t[i] for i in range(len(t)-1)]
mean = sum(intervals) / len(intervals)
variance = sum((x - mean)**2 for x in intervals) / len(intervals)
jitter = math.sqrt(variance)
jitter_percent = (jitter / mean) * 100
```

### Jitter Thresholds
| Jitter % | Confidence | Likely Cause |
|----------|------------|--------------|
| < 5% | HIGH | Automated C2 beacon |
| 5-15% | MEDIUM | Possible C2 with sleep jitter |
| 15-30% | LOW | May be legitimate polling |
| > 30% | NONE | Likely human/random |

## Zeek conn.log Format

### Fields
| Index | Name | Description |
|-------|------|-------------|
| 0 | ts | Unix timestamp |
| 2 | id.orig_h | Source IP |
| 3 | id.orig_p | Source port |
| 4 | id.resp_h | Destination IP |
| 5 | id.resp_p | Destination port |
| 6 | proto | Protocol |
| 9 | orig_bytes | Sent bytes |
| 10 | resp_bytes | Received bytes |

## RITA (Real Intelligence Threat Analytics)

### Analyze Zeek Logs
```bash
rita import /path/to/zeek/logs dataset_name
rita show-beacons dataset_name
```

### Output Columns
| Column | Description |
|--------|-------------|
| Score | Beacon probability (0-1) |
| Source | Source IP |
| Destination | Destination IP |
| Connections | Total connections |
| Avg Bytes | Average data transfer |

## Splunk SPL — Beacon Detection

```spl
index=network sourcetype=zeek:conn
| bin _time span=60s
| stats count by src_ip, dest_ip, dest_port, _time
| streamstats window=100 stdev(count) as jitter avg(count) as avg_count by src_ip, dest_ip
| where jitter/avg_count < 0.15
| stats count as beacon_count by src_ip, dest_ip, dest_port
| where beacon_count > 100
```

## Elastic SIEM — Beacon Detection

```json
{
  "query": {
    "bool": {
      "must": [
        {"range": {"@timestamp": {"gte": "now-24h"}}},
        {"exists": {"field": "destination.ip"}}
      ]
    }
  },
  "aggs": {
    "by_flow": {
      "composite": {
        "sources": [
          {"src": {"terms": {"field": "source.ip"}}},
          {"dst": {"terms": {"field": "destination.ip"}}}
        ]
      }
    }
  }
}
```

## Common C2 Beacon Intervals

| Framework | Default Interval |
|-----------|-----------------|
| Cobalt Strike | 60 seconds |
| Metasploit | 5 seconds |
| Empire | 5 seconds |
| Covenant | 10 seconds |
| Sliver | 60 seconds |

---

## Standards and Controls

## MITRE ATT&CK Command and Control (TA0011)

| Technique | Name | Beacon Indicators |
|-----------|------|-------------------|
| T1071.001 | Web Protocols | HTTP/HTTPS periodic connections with regular intervals |
| T1071.004 | DNS | DNS query patterns, tunneling with high entropy subdomains |
| T1573.001 | Symmetric Cryptography | Encrypted C2 channels with consistent packet sizes |
| T1573.002 | Asymmetric Cryptography | TLS C2 with custom or self-signed certificates |
| T1572 | Protocol Tunneling | DNS-over-HTTPS, ICMP tunneling with periodic patterns |
| T1568.002 | Domain Generation Algorithms | Algorithmically generated domains with high entropy |
| T1568.001 | Fast Flux DNS | Rapidly rotating IP addresses for C2 infrastructure |
| T1132.001 | Standard Encoding | Base64/hex encoded data in C2 traffic |
| T1095 | Non-Application Layer Protocol | ICMP, raw TCP/UDP for covert C2 |
| T1090 | Proxy | Multi-hop C2 infrastructure obscuring origin |
| T1102 | Web Service | C2 over legitimate cloud services |

## Beaconing Detection Thresholds

| Metric | Threshold | Rationale |
|--------|-----------|-----------|
| Coefficient of Variation (CV) | < 0.20 | Strong indicator of periodic automated communication |
| Minimum Beacon Interval | > 30 seconds | Below this may be streaming or polling traffic |
| Maximum Beacon Interval | < 86400 seconds | Beyond 24 hours reduces statistical significance |
| Minimum Connection Count | > 50 per 24 hours | Needed for reliable statistical analysis |
| Data Size CV | < 0.30 | Consistent payloads suggest automated heartbeats |
| Domain Age | < 30 days | Newly registered domains associated with C2 infrastructure |

## Known C2 Framework Default Beacon Profiles

| Framework | Default Interval | Default Jitter | Protocols | Detection Notes |
|-----------|-----------------|----------------|-----------|-----------------|
| Cobalt Strike | 60s | 0-50% | HTTPS, DNS | Malleable C2 profiles can change all defaults |
| Sliver | 60s | 0-30% | HTTPS, mTLS, WireGuard, DNS | Supports domain fronting |
| Brute Ratel C4 | 60s | 10-30% | HTTPS, DNS, SMB | Designed to evade EDR detection |
| Metasploit Meterpreter | 5s | 0% | TCP, HTTP/S | Highly configurable via handlers |
| Havoc | 5s | 0-20% | HTTPS | Demon agent with sleep obfuscation |
| Mythic | Configurable | Configurable | HTTP/S, TCP, WebSocket | Agent-dependent behavior |
| Covenant | 10s | 10% | HTTP/S | .NET-based C2 framework |
| Empire/Starkiller | 5s | 0-20% | HTTP/S | Python-based listeners |

## Statistical Methods for Beacon Detection

| Method | Description | Best For |
|--------|-------------|----------|
| Coefficient of Variation | stdev/mean of intervals | Regular beacons with low jitter |
| Fast Fourier Transform (FFT) | Frequency domain analysis | Detecting periodic signals in noisy data |
| Autocorrelation | Self-correlation at various lags | Identifying repeating patterns |
| Median Absolute Deviation | Robust measure of variability | Beacon detection resistant to outliers |
| Kullback-Leibler Divergence | Distribution comparison | Comparing observed intervals to uniform distribution |

## RITA Beacon Scoring Algorithm

RITA scores beacons on a 0-1 scale using:
- **Timestamp score**: Regularity of connection intervals
- **Data size score**: Consistency of bytes transferred
- **Connection count**: Volume of connections in analysis window
- **Duration**: How long the beaconing pattern has persisted

Composite score above 0.70 is considered high-confidence beaconing.

---

## Workflows

## Phase 1: Data Collection and Preparation

### Step 1.1 - Gather Network Connection Logs
Collect at minimum 24 hours (ideally 7 days) of:
- Proxy/firewall logs with timestamps, source/destination, bytes
- Zeek conn.log for connection metadata
- Zeek dns.log for DNS query analysis
- Zeek ssl.log for TLS certificate and JA3 fingerprinting
- NetFlow/IPFIX for high-level flow data

### Step 1.2 - Normalize Timestamps
Ensure all timestamps are in a consistent format (epoch or ISO 8601) and timezone (UTC). Misaligned timestamps will corrupt interval calculations.

## Phase 2: Statistical Frequency Analysis

### Step 2.1 - Splunk Interval Calculation
```spl
index=proxy OR index=firewall
| where NOT match(dest, "(?i)(microsoft|google|amazonaws|cloudflare|akamai|apple|adobe)")
| bin _time span=1s
| stats count by src_ip dest _time
| streamstats current=f last(_time) as prev_time by src_ip dest
| eval interval=_time-prev_time
| stats count avg(interval) as avg_interval stdev(interval) as stdev_interval
  min(interval) as min_interval max(interval) as max_interval
  dc(interval) as unique_intervals by src_ip dest
| where count > 50
| eval cv=stdev_interval/avg_interval
| eval jitter_pct=round((stdev_interval/avg_interval)*100, 1)
| where cv < 0.25 AND avg_interval > 30 AND avg_interval < 86400
| sort cv
| table src_ip dest count avg_interval stdev_interval cv jitter_pct
```

### Step 2.2 - Elastic Query for Beacon Detection
```json
{
  "aggs": {
    "by_pair": {
      "composite": {
        "sources": [
          {"src": {"terms": {"field": "source.ip"}}},
          {"dst": {"terms": {"field": "destination.domain"}}}
        ]
      },
      "aggs": {
        "timestamps": {
          "date_histogram": {"field": "@timestamp", "fixed_interval": "1s"}
        },
        "stats": {
          "extended_stats": {"field": "event.duration"}
        }
      }
    }
  }
}
```

### Step 2.3 - RITA Automated Analysis
```bash
# Import Zeek logs into RITA
rita import /path/to/zeek/logs mydataset

# Analyze beacons
rita show-beacons mydataset

# Export results as CSV
rita show-beacons mydataset --csv > beacon_results.csv

# Show long connections
rita show-long-connections mydataset
```

## Phase 3: Jitter-Aware Detection

### Step 3.1 - Detect Beacons with Jitter
Cobalt Strike adds configurable jitter (0-50%) to its sleep timer. A 60-second beacon with 30% jitter produces intervals between 42-78 seconds.

```spl
index=proxy
| stats count by src_ip dest _time
| streamstats current=f last(_time) as prev_time by src_ip dest
| eval interval=_time-prev_time
| stats count avg(interval) as avg stdev(interval) as sd
  percentile25(interval) as p25 percentile75(interval) as p75 by src_ip dest
| where count > 50
| eval iqr=p75-p25
| eval jitter_ratio=iqr/avg
| where jitter_ratio < 0.50 AND avg > 30
| sort jitter_ratio
```

## Phase 4: Data Size Consistency Analysis

### Step 4.1 - Payload Size Regularity
```spl
index=proxy
| stats count avg(bytes_out) as avg_bytes stdev(bytes_out) as sd_bytes
  by src_ip dest
| where count > 50
| eval data_cv=sd_bytes/avg_bytes
| where data_cv < 0.30
| sort data_cv
```

## Phase 5: Domain Intelligence Enrichment

### Step 5.1 - Check Domain Age via WHOIS
Flag any beaconing destination with domain registration under 30 days. Newly registered domains correlate strongly with C2 infrastructure.

### Step 5.2 - JA3/JA4 TLS Fingerprinting
```spl
index=zeek sourcetype=bro_ssl
| stats count dc(id.resp_h) as unique_dests values(server_name) as domains by ja3
| lookup ja3_known_c2 ja3 OUTPUT framework
| where isnotnull(framework)
| table ja3 framework count unique_dests domains
```

## Phase 6: Endpoint Correlation

### Step 6.1 - Map Network to Process
```spl
index=sysmon EventCode=3
| where NOT cidrmatch("10.0.0.0/8", DestinationIp)
  AND NOT cidrmatch("172.16.0.0/12", DestinationIp)
  AND NOT cidrmatch("192.168.0.0/16", DestinationIp)
| stats count values(DestinationPort) as ports dc(DestinationIp) as unique_ips
  by Image Computer DestinationIp
| where count > 50 AND unique_ips < 3
| sort -count
```

## Phase 7: Verification and Response

### Step 7.1 - Confirm C2 Activity
1. Capture packet sample of suspected C2 traffic
2. Analyze TLS certificate (self-signed, unusual issuer, short validity)
3. Cross-reference domain/IP against multiple TI sources
4. Review process tree on source endpoint
5. Check for associated lateral movement or tool transfers

### Step 7.2 - Containment Actions
1. Block C2 domain/IP at firewall, proxy, and DNS sinkhole
2. Isolate compromised endpoint via EDR network containment
3. Preserve memory dump and disk image for forensics
4. Reset credentials used on affected systems
5. Sweep environment for additional infections using discovered IOCs

---

## Working Template

## Hunt Metadata
| Field | Value |
|-------|-------|
| Hunt ID | TH-BEACON-YYYY-MM-DD-NNN |
| Analyst | |
| Date | |
| Data Window | [Start] to [End] |
| Status | [ ] In Progress / [ ] Complete |

## Hypothesis
> Compromised endpoints are beaconing to adversary C2 infrastructure using periodic HTTP/HTTPS/DNS connections with detectable frequency patterns.

## Data Sources
- [ ] Proxy logs
- [ ] Firewall logs
- [ ] Zeek conn.log
- [ ] Zeek dns.log
- [ ] Zeek ssl.log
- [ ] Sysmon Event ID 3 (Network Connection)

## Beaconing Findings

| # | Source IP | Source Host | Destination | Protocol | Avg Interval | CV | Jitter % | Connections | Risk |
|---|----------|-------------|-------------|----------|--------------|-----|----------|-------------|------|
| 1 | | | | | | | | | |

## Domain Intelligence

| Domain/IP | WHOIS Age | VirusTotal Score | PassiveDNS | JA3 Match | Assessment |
|-----------|-----------|------------------|------------|-----------|------------|
| | | | | | |

## Endpoint Correlation

| Host | Process | PID | User | Parent Process | File Path | Suspicious |
|------|---------|-----|------|----------------|-----------|------------|
| | | | | | | |

## IOC List
| Type | Value | Confidence | Source |
|------|-------|-----------|--------|
| Domain | | | |
| IP | | | |
| JA3 | | | |
| User-Agent | | | |

## Recommendations
1. **Block**: [Domains/IPs to block at firewall and proxy]
2. **Isolate**: [Endpoints to contain via EDR]
3. **Detect**: [New detection rules to deploy]
4. **Hunt**: [Additional IOCs to sweep for across the environment]
