# Detecting Ransomware Precursors In Network

## API Reference

## Zeek (Bro) Log Fields

### conn.log
| Field | Type | Description |
|-------|------|-------------|
| `ts` | time | Connection start timestamp (Unix epoch) |
| `id.orig_h` | addr | Source IP address |
| `id.orig_p` | port | Source port |
| `id.resp_h` | addr | Destination IP address |
| `id.resp_p` | port | Destination port |
| `proto` | enum | Transport protocol (tcp/udp/icmp) |
| `orig_bytes` | count | Bytes sent by originator |
| `resp_bytes` | count | Bytes sent by responder |
| `conn_state` | string | Connection state (SF=normal, S0=no reply, REJ=rejected) |
| `duration` | interval | Duration of connection |

### smb_files.log
| Field | Type | Description |
|-------|------|-------------|
| `action` | enum | SMB action (SMB_FILE_OPEN, SMB_FILE_WRITE, SMB_FILE_DELETE) |
| `path` | string | Full UNC path accessed |
| `name` | string | Filename |
| `size` | count | File size in bytes |
| `id.orig_h` | addr | Source host (accessor) |
| `id.resp_h` | addr | Target host |

### kerberos.log
| Field | Type | Description |
|-------|------|-------------|
| `request_type` | string | KRB_AS_REQ, KRB_TGS_REQ |
| `client` | string | Client principal |
| `service` | string | Service principal (SPN) |
| `success` | bool | Whether request succeeded |
| `error_msg` | string | Error type (e.g., KDC_ERR_PREAUTH_REQUIRED) |

## Suricata CLI

### Start in IDS mode
```bash
suricata -c /etc/suricata/suricata.yaml -i eth0
```

### Start in IPS mode (NFQUEUE)
```bash
suricata -c /etc/suricata/suricata.yaml -q 0
# Configure iptables to send traffic to NFQUEUE:
iptables -I FORWARD -j NFQUEUE --queue-num 0
```

### Run on pcap file
```bash
suricata -c /etc/suricata/suricata.yaml -r capture.pcap -l /var/log/suricata/
```

### Update rules with suricata-update
```bash
suricata-update                          # Update all enabled sources
suricata-update list-sources             # List available rule sources
suricata-update enable-source et/open    # Enable Emerging Threats Open
suricata-update enable-source ptresearch/attackdetection  # PT Research rules
suricata-update update-sources           # Refresh source index
suricata-update --no-reload              # Update without live reload
```

### Reload rules without restart
```bash
kill -USR2 $(pidof suricata)
# Or via Unix socket:
suricatasc -c reload-rules
```

### Query eve.json for alerts
```bash
# Ransomware-related alerts in last hour
jq 'select(.event_type=="alert") | select(.alert.signature | test("ransomware|cobalt|mimikatz|psexec";"i"))' \
  /var/log/suricata/eve.json | jq -r '[.timestamp,.src_ip,.dest_ip,.alert.signature] | @tsv'

# Top 10 alert signatures
jq -r 'select(.event_type=="alert") | .alert.signature' /var/log/suricata/eve.json | \
  sort | uniq -c | sort -rn | head -10
```

## RITA (Real Intelligence Threat Analytics)

### Import Zeek logs and analyze
```bash
rita import --input /var/log/zeek/current/ --database my_network
rita analyze my_network
```

### Beacon detection output
```bash
rita show-beacons my_network --human-readable
# Columns: Score | Source | Dest | Connections | Avg Bytes | TS Delta
# Score 0.9+ = high confidence beacon
```

### DNS tunneling detection
```bash
rita show-exploded-dns my_network | head -20
rita show-long-connections my_network --human-readable
```

## Splunk SPL — Ransomware Precursor Queries

### Internal lateral movement via SMB/RDP/WinRM
```spl
index=zeek sourcetype=zeek_conn
  id.resp_p IN (445, 135, 3389, 5985, 5986)
  id.orig_h IN 10.0.0.0/8
  id.resp_h IN 10.0.0.0/8
| stats dc(id.resp_h) as targets count as conns by id.orig_h
| where targets >= 10
| sort -targets
```

### Detect beaconing (regular connection intervals)
```spl
index=zeek sourcetype=zeek_conn
| bucket _time span=1m
| stats count as conns by id.orig_h, id.resp_h, id.resp_p, _time
| stats stdev(conns) as jitter avg(conns) as avg_conns count as minutes
    by id.orig_h, id.resp_h, id.resp_p
| where minutes > 10 AND jitter < 2 AND avg_conns > 0
| eval beacon_score = round(1 - (jitter / (avg_conns + 0.001)), 2)
| where beacon_score > 0.8
| sort -beacon_score
```

## abuse.ch Threat Intelligence Feeds

### Feodo Tracker (C2 IPs — Cobalt Strike, BazarLoader)
```bash
# CSV format: first_seen,dst_ip,dst_port,c2_status,malware
curl -s https://feodotracker.abuse.ch/downloads/ipblocklist.csv | \
  grep -v "^#" | awk -F, '{print $2}' > /tmp/c2_ips.txt
```

### ThreatFox IOC API
```bash
# Query recent ransomware IOCs
curl -s -X POST https://threatfox-api.abuse.ch/api/v1/ \
  -H "Content-Type: application/json" \
  -d '{"query":"get_iocs","days":7,"tag":"ransomware"}' | \
  jq '.data[] | [.ioc_value,.ioc_type,.malware,.confidence_level] | @tsv' -r
```

## MITRE ATT&CK Ransomware Precursor Techniques
| Technique | ID | Network Indicator |
|-----------|----|-------------------|
| Remote Services: SMB/WMI | T1021.002 | SMB port 445 traffic to many hosts |
| OS Credential Dumping: DCSync | T1003.006 | DRS GetNCChanges from non-DC |
| Kerberoasting | T1558.003 | TGS-REQ for many SPNs |
| Command & Control | T1071.001 | Regular HTTPS beaconing |
| Lateral Tool Transfer | T1570 | Large SMB file writes across hosts |
| Network Service Scanning | T1046 | Port sweeps on 445/3389/135 |

---

## Standards and Controls

## MITRE ATT&CK Mapping

### Initial Access (TA0001)
- T1078: Valid Accounts (compromised credentials from IABs)
- T1133: External Remote Services (VPN/RDP exploitation)
- T1566: Phishing (email-based initial access)

### Command and Control (TA0011)
- T1071.001: Application Layer Protocol: Web (HTTPS beacons)
- T1071.004: Application Layer Protocol: DNS (DNS tunneling)
- T1573: Encrypted Channel (C2 over TLS)
- T1090: Proxy (redirectors and relay infrastructure)

### Credential Access (TA0006)
- T1558.003: Kerberoasting
- T1003.006: DCSync
- T1557: Adversary-in-the-Middle (NTLM relay)

### Discovery (TA0007)
- T1046: Network Service Discovery (port scanning)
- T1018: Remote System Discovery (AD enumeration)
- T1087: Account Discovery

### Lateral Movement (TA0008)
- T1021.002: Remote Services: SMB/Windows Admin Shares
- T1021.001: Remote Services: RDP
- T1047: Windows Management Instrumentation (WMI)
- T1569.002: System Services: Service Execution (PsExec)

## Industry References

### CISA Advisories
- AA23-136A: #StopRansomware - BianLian Ransomware Group
- AA23-158A: #StopRansomware - CL0P Ransomware Gang
- AA24-131A: #StopRansomware - Black Basta
- AA23-165A: Understanding Ransomware Threat Actors: LockBit

### NIST
- SP 800-94 Rev 1: Guide to Intrusion Detection and Prevention Systems
- SP 800-86: Guide to Integrating Forensic Techniques into Incident Response
- IR 8374: Ransomware Risk Management

### Threat Intelligence Sources
- abuse.ch Feodo Tracker: https://feodotracker.abuse.ch/
- abuse.ch ThreatFox: https://threatfox.abuse.ch/
- CISA Known Exploited Vulnerabilities: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- Emerging Threats Ruleset: https://rules.emergingthreats.net/

---

## Workflows

## Workflow 1: Network Sensor Deployment

```
Start
  |
  v
[Identify network chokepoints] --> Core switches, internet edge, DC segments
  |
  v
[Deploy network TAPs or configure SPAN ports]
  |
  v
[Install Zeek sensor] --> Configure local.zeek with site-specific networks
  |
  v
[Install Suricata IDS] --> Load ET Open + custom ransomware rules
  |
  v
[Configure log forwarding to SIEM]
  |-- Zeek: conn.log, ssl.log, dns.log, smb.log, kerberos.log, notice.log
  |-- Suricata: eve.json (alerts, flow, dns, tls)
  |
  v
[Deploy RITA for beacon analysis] --> Schedule hourly Zeek log imports
  |
  v
[Load threat intelligence feeds] --> Feodo, ThreatFox, CISA KEV
  |
  v
[Validate detection with controlled Cobalt Strike beacon test]
  |
  v
End
```

## Workflow 2: Alert Triage for Ransomware Precursors

```
Alert Received
  |
  v
[Classify alert type]
  |-- C2 Beaconing --> Priority: CRITICAL, SLA: 15 min
  |-- Credential Harvesting --> Priority: CRITICAL, SLA: 15 min
  |-- Internal Scanning --> Priority: HIGH, SLA: 30 min
  |-- Admin Share Access --> Priority: HIGH, SLA: 30 min
  |-- RDP Brute Force --> Priority: MEDIUM, SLA: 1 hour
  |-- DNS Anomaly --> Priority: LOW, SLA: 4 hours
  |
  v
[Check for correlated alerts on same source IP]
  |-- Multiple categories? --> Elevate to CRITICAL regardless
  |-- Single category? --> Proceed with category SLA
  |
  v
[Verify source host context]
  |-- Known admin workstation? --> Check if scheduled activity
  |-- Server? --> Check for authorized maintenance window
  |-- Standard workstation? --> Likely compromise indicator
  |
  v
[Decision: True Positive or False Positive?]
  |
  TP --> [Contain host: network isolation via NAC/EDR]
  |       |
  |       v
  |       [Trigger incident response playbook]
  |
  FP --> [Document FP reason]
          |
          v
          [Update detection rule to reduce FP rate]
          |
          v
          End
```

## Workflow 3: Beacon Detection with RITA

```
Hourly Cron Job
  |
  v
[Import latest Zeek logs into RITA database]
  $ rita import /opt/zeek/logs/current rita-db
  |
  v
[Analyze beacons]
  $ rita show-beacons rita-db --human-readable
  |
  v
[Filter results by beacon score > 0.7]
  |
  v
[For each high-score beacon:]
  |-- Look up destination IP in threat intel
  |-- Check JA3/JA4 hash against known C2 fingerprints
  |-- Verify beacon interval and jitter pattern
  |
  v
[Score > 0.9 AND matches threat intel?]
  |
  Yes --> [Generate CRITICAL alert]
  |
  No --> [Score > 0.7?]
          |
          Yes --> [Generate MEDIUM alert for analyst review]
          |
          No --> [Log and continue monitoring]
  |
  v
End
```

---

## Working Template

## Network Sensor Placement

| Sensor Location | TAP/SPAN | Sensor Type | Protocols Monitored |
|----------------|----------|-------------|---------------------|
| Internet Edge | | Zeek + Suricata | All outbound |
| DC Segment | | Zeek | Kerberos, LDAP, SMB, DNS |
| Server VLAN | | Zeek + Suricata | SMB, RDP, WMI, WinRM |
| Workstation VLAN | | Zeek | SMB, HTTP/S, DNS |

## Detection Rules Deployed

| Rule ID | Category | Description | Severity | Status |
|---------|----------|-------------|----------|--------|
| | C2 Beaconing | | | |
| | Credential Harvest | | | |
| | Internal Scanning | | | |
| | Lateral Movement | | | |

## Threat Intelligence Feeds

| Feed | Source | Update Frequency | IOC Types |
|------|--------|-----------------|-----------|
| Feodo Tracker | abuse.ch | Hourly | IPs (C2) |
| ThreatFox | abuse.ch | Hourly | IPs, domains, hashes |
| ET Open Rules | Proofpoint | Daily | Suricata signatures |
| CISA KEV | CISA | As published | CVEs |

## Alert Triage SLAs

| Category | Priority | Triage SLA | Escalation Path |
|----------|----------|-----------|-----------------|
| Confirmed C2 | CRITICAL | 15 min | SOC -> IR Team -> CISO |
| Credential Harvest | CRITICAL | 15 min | SOC -> IR Team |
| Internal Scanning | HIGH | 30 min | SOC -> IR Team |
| Admin Share Enum | HIGH | 30 min | SOC -> IR Team |
| RDP Anomaly | MEDIUM | 1 hour | SOC Tier 2 |
| DNS Anomaly | LOW | 4 hours | SOC Tier 1 |

## Detection Tuning Log

| Date | Rule | Change | Reason | FP Rate Before | FP Rate After |
|------|------|--------|--------|----------------|---------------|
| | | | | | |
