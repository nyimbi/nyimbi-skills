# Hunting For Data Exfiltration Indicators

## API Reference

## Exfiltration Methods (MITRE ATT&CK)

| Technique | ID | Description |
|-----------|----|-------------|
| Exfiltration Over C2 Channel | T1041 | Via existing C2 |
| Exfiltration Over Alternative Protocol | T1048 | DNS, ICMP, etc. |
| Exfiltration Over Web Service | T1567 | Cloud storage |
| Automated Exfiltration | T1020 | Scripted transfer |

## DNS Exfiltration Indicators

| Indicator | Threshold |
|-----------|-----------|
| Shannon entropy | > 3.5 |
| Subdomain length | > 40 chars |
| Query volume per domain | > 100/hour |
| TXT record responses | > 500 bytes |

## Zeek Log Fields

### conn.log
| Field | Description |
|-------|-------------|
| `ts` | Timestamp |
| `id.orig_h` | Source IP |
| `id.resp_h` | Destination IP |
| `orig_bytes` | Bytes from source |
| `resp_bytes` | Bytes from destination |

### dns.log
| Field | Description |
|-------|-------------|
| `query` | DNS query name |
| `qtype_name` | Query type (A, TXT, etc.) |
| `answers` | Response answers |

## Python Libraries

| Library | Use |
|---------|-----|
| `csv` | Parse Zeek TSV logs |
| `math` | Shannon entropy calculation |
| `collections.defaultdict` | Aggregate statistics |
| `dpkt` | PCAP parsing |
| `scapy` | Packet-level analysis |

## Shannon Entropy Formula

```
H(X) = -sum(p(x) * log2(p(x)))
```
Normal domain: H < 3.0, Exfil encoded: H > 3.5

---

## Standards and Controls

## MITRE ATT&CK Exfiltration (TA0010)

| Technique | Name | Channel |
|-----------|------|---------|
| T1041 | Exfiltration Over C2 Channel | Uses existing C2 connection |
| T1048.001 | Symmetric Encrypted Non-C2 | Custom encrypted protocol |
| T1048.002 | Asymmetric Encrypted Non-C2 | TLS to non-C2 server |
| T1048.003 | Unencrypted/Obfuscated Non-C2 | FTP, HTTP, raw TCP |
| T1567.001 | Exfiltration to Code Repository | GitHub, GitLab |
| T1567.002 | Exfiltration to Cloud Storage | S3, GDrive, Dropbox, OneDrive |
| T1567.003 | Exfiltration to Text Storage | Pastebin, paste.ee |
| T1567.004 | Exfiltration Over Webhook | Slack, Discord, Teams webhooks |
| T1052.001 | Exfiltration Over USB | Removable media |
| T1537 | Transfer Data to Cloud Account | Cloud-to-cloud exfiltration |
| T1020 | Automated Exfiltration | Script-based bulk transfer |
| T1029 | Scheduled Transfer | Periodic small transfers |
| T1030 | Data Transfer Size Limits | Size-limited staged transfer |

## Detection Thresholds

| Metric | Alert Threshold | Notes |
|--------|----------------|-------|
| Outbound data per host/day | > 2x 30-day average | Volume anomaly |
| DNS query length | > 50 characters | DNS tunneling indicator |
| DNS TXT record queries | > 100/hour per domain | DNS exfiltration |
| Cloud upload volume | > 500MB/day per user | Cloud exfiltration |
| Email attachment size | > 25MB per email | Email exfiltration |
| Off-hours data transfer | Any > 100MB | Unusual timing |
| Transfer to new destination | > 50MB first time | New destination risk |

## Data Sources

| Source | Event Type | Exfiltration Indicator |
|--------|-----------|----------------------|
| Proxy logs | HTTP POST/PUT | Large upload bytes |
| Firewall | Connection data | Bytes-out anomalies |
| DNS server | Query logs | Long subdomain names, TXT queries |
| Email gateway | Message logs | Attachment sizes, external recipients |
| CASB | Cloud activity | Uploads to personal cloud |
| Sysmon Event 3 | Network connections | Process-level data transfer |
| DLP | Content inspection | Sensitive data classification |
| USB audit | Removable media | Device insertion + file copy |

---

## Workflows

## Phase 1: Volume Anomaly Detection

### Step 1.1 - Outbound Data Volume per Host
```spl
index=proxy OR index=firewall
| where NOT match(dest, "(?i)(microsoft|windowsupdate|google|amazonaws)")
| stats sum(bytes_out) as total_bytes_out by src_ip
| eval MB_out=round(total_bytes_out/1048576, 2)
| sort -MB_out
| head 50
```

### Step 1.2 - Statistical Volume Anomaly
```spl
index=proxy earliest=-30d
| bin _time span=1d
| stats sum(bytes_out) as daily_bytes by src_ip _time
| eventstats avg(daily_bytes) as avg_daily stdev(daily_bytes) as sd_daily by src_ip
| where daily_bytes > (avg_daily + 3*sd_daily) AND daily_bytes > 104857600
| eval anomaly_factor=round(daily_bytes/avg_daily, 1)
| table _time src_ip daily_bytes avg_daily anomaly_factor
```

## Phase 2: Cloud Storage Exfiltration

### Step 2.1 - Cloud Upload Detection
```spl
index=proxy
| where match(dest, "(?i)(drive\.google|dropbox|box\.com|onedrive|mega\.nz|wetransfer|sendspace)")
| where method IN ("POST", "PUT")
| stats sum(bytes_out) as uploaded_bytes count by src_ip dest user
| eval MB_uploaded=round(uploaded_bytes/1048576, 2)
| where MB_uploaded > 50
| sort -MB_uploaded
```

## Phase 3: DNS Exfiltration

### Step 3.1 - DNS Tunneling Indicators
```spl
index=dns
| eval query_len=len(query)
| where query_len > 50
| rex field=query "^(?<subdomain>.+)\.(?<base_domain>[^.]+\.[^.]+)$"
| stats count avg(query_len) as avg_len dc(subdomain) as unique_subs by src_ip base_domain
| where count > 100 AND (avg_len > 40 OR unique_subs > 50)
| sort -count
```

## Phase 4: Email Exfiltration

### Step 4.1 - Large Email Attachments to External
```spl
index=email
| where match(recipient, "(?i)(gmail|yahoo|hotmail|protonmail|outlook)")
| where attachment_size > 10485760
| stats count sum(attachment_size) as total_size by sender recipient
| eval MB_sent=round(total_size/1048576, 2)
| sort -MB_sent
```

## Phase 5: File Access Correlation

### Step 5.1 - Sensitive File Access Before Exfiltration
Correlate file access events on sensitive shares with subsequent outbound data transfers:
```spl
index=wineventlog EventCode=5145
| where match(Share_Name, "(?i)(finance|hr|legal|confidential|restricted)")
| stats count values(Relative_Target_Name) as files by Account_Name Source_Address
| join Account_Name [
    search index=proxy method IN ("POST","PUT") earliest=-1h
    | stats sum(bytes_out) as upload_bytes by user
    | rename user as Account_Name
]
| where upload_bytes > 1048576
```

---

## Working Template

## Hunt Metadata
| Field | Value |
|-------|-------|
| Hunt ID | TH-EXFIL-YYYY-MM-DD-NNN |
| Analyst | |
| Date | |

## Hypothesis
> [e.g., "Compromised endpoints are exfiltrating sensitive data to cloud storage or via DNS tunneling."]

## Findings
| # | Source | Destination | Channel | Volume | Period | Risk | Verdict |
|---|--------|-------------|---------|--------|--------|------|---------|
| 1 | | | | | | | |

## Data Exposure Assessment
| Data Type | Volume | Classification | Impact |
|-----------|--------|---------------|--------|
| | | | |

## Recommendations
1. **Block**: [Destinations to block]
2. **DLP**: [Rules to deploy]
3. **Monitor**: [New detection rules]
