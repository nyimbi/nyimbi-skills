# Triaging Security Incident With Ir Playbook

## API Reference

## Incident Classification Types

| Type | Keywords | Default Severity | Playbook |
|------|----------|-----------------|----------|
| Malware | trojan, ransomware, c2, beacon | High | malware-infection-playbook |
| Phishing | credential harvest, BEC, spear-phishing | Medium | phishing-response-playbook |
| Data Exfiltration | DLP, dns tunnel, large upload | Critical | data-exfiltration-playbook |
| Unauthorized Access | brute force, lateral movement | High | unauthorized-access-playbook |
| Denial of Service | DDoS, SYN flood, volumetric | High | ddos-response-playbook |
| Insider Threat | policy violation, terminated user | High | insider-threat-playbook |
| Web Attack | SQLi, XSS, web shell, RCE | High | web-attack-playbook |

## Severity Matrix

| Context Factor | Severity Override |
|----------------|-------------------|
| Crown jewel system affected | Critical |
| Active exploitation confirmed | Critical |
| Multiple systems (>5) affected | High |
| Single system affected | Medium |
| Reconnaissance only | Low |
| Minor policy violation | Informational |

## Escalation Paths

| Severity | Response Time | Escalation |
|----------|---------------|------------|
| Critical | 15 minutes | IR Team + CISO + Legal |
| High | 1 hour | SOC Tier 2 + IR Team |
| Medium | 4 hours | SOC Tier 2 |
| Low | 24 hours | SOC Tier 1 |
| Informational | Next business day | SOC Tier 1 |

## Python Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| `json` | stdlib | Alert parsing and report generation |
| `enum` | stdlib | Severity level enumeration |
| `pathlib` | stdlib | Output directory management |
| `datetime` | stdlib | Triage timestamps |

## References

- NIST SP 800-61r2: https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final
- SANS Incident Handler's Handbook: https://www.sans.org/white-papers/33901/
- TheHive: https://thehive-project.org/

---

## Standards and Controls

## NIST SP 800-61 Rev. 3 - Incident Triage Alignment
- **Detect (DE)**: Alert analysis and triage
  - DE.AE-02: Potentially adverse events are analyzed to better understand associated activities
  - DE.AE-03: Information is correlated from multiple sources
  - DE.AE-04: The estimated impact and scope of adverse events is understood
- **Respond (RS)**: Incident classification and escalation
  - RS.AN-03: Analysis performed to establish awareness of incident scope
  - RS.CO-02: Incidents reported consistent with established criteria

## SANS PICERL - Identification Phase
- Phase 2 focuses on detecting and validating security events
- Triage determines if an event qualifies as an incident
- Key activities: alert validation, initial scoping, severity assignment
- Triage SLAs: P1 <15 min, P2 <30 min, P3 <1 hour, P4 <4 hours

## NIST Severity Classification (SP 800-61 Rev. 2, Table 3-2)
| Category | Definition | Examples |
|----------|-----------|----------|
| CAT 1 - Unauthorized Access | Individual gains access without permission | Compromised credentials, privilege escalation |
| CAT 2 - Denial of Service | Disruption of service availability | DDoS, resource exhaustion |
| CAT 3 - Malicious Code | Infection by malware | Virus, worm, trojan, ransomware |
| CAT 4 - Improper Usage | Violation of acceptable use policy | Unauthorized software, policy breach |
| CAT 5 - Scans/Probes | Reconnaissance activity | Port scans, vulnerability scans |
| CAT 6 - Investigation | Unconfirmed suspicious activity | Anomalous behavior under review |

## MITRE ATT&CK - Triage Technique Mapping
- Map observed techniques to ATT&CK framework during triage
- Technique identification helps select appropriate playbook
- Tactic identification reveals attacker's current phase
- Reference: https://attack.mitre.org/

## FIRST CSIRT Services Framework
- Triage falls under "Event Management" service area
- Key functions: Monitoring and Detection, Event Analysis, Incident Coordination
- Reference: https://www.first.org/standards/frameworks/csirts/csirt_services_framework_v2.1

## US-CERT Federal Incident Reporting Guidelines
- Category definitions for federal incident reporting
- Reporting timeframes based on incident category
- Reference: https://www.cisa.gov/federal-incident-notification-guidelines

---

## Workflows

## Triage Decision Tree

```
Alert Received
    |
    v
Is alert from trusted/tuned detection rule?
    |-- No --> Check rule logic, verify data source --> Potential false positive
    |-- Yes --> Continue
    |
    v
Does alert match known false positive pattern?
    |-- Yes --> Document, close as false positive, tune rule
    |-- No --> Continue
    |
    v
Can indicator be enriched with external threat intel?
    |-- Yes --> Enrich with VT, AbuseIPDB, OTX --> Add context
    |-- No --> Continue with available data
    |
    v
What is the incident type?
    |-- Malware --> Malware playbook
    |-- Phishing --> Phishing playbook
    |-- Unauthorized Access --> Access compromise playbook
    |-- Data Exfiltration --> Data breach playbook
    |-- Ransomware --> Ransomware playbook
    |-- DoS/DDoS --> Availability playbook
    |-- Insider Threat --> Insider playbook
    |
    v
Assign severity based on:
    - Asset criticality x Threat level x Data sensitivity
    |
    v
Route to appropriate team with playbook
```

## Severity Assignment Matrix

### Impact Score (1-4)
| Score | Asset Criticality | Examples |
|-------|------------------|----------|
| 4 | Critical | Domain controllers, production databases, financial systems |
| 3 | High | Email servers, web applications, file servers |
| 2 | Medium | Development systems, internal tools |
| 1 | Low | Test systems, non-production workstations |

### Urgency Score (1-4)
| Score | Threat Status | Indicators |
|-------|-------------|------------|
| 4 | Active exploitation | Ongoing attack, real-time data loss |
| 3 | Confirmed compromise | Evidence of breach, but not active |
| 2 | Attempted attack | Blocked attack, no evidence of success |
| 1 | Reconnaissance | Scanning, probing, no exploitation attempt |

### Final Severity = Impact x Urgency
| Score Range | Severity | Response Time | Escalation |
|------------|----------|--------------|------------|
| 12-16 | P1 Critical | Immediate (15 min) | CISO + IR Lead + Senior Analysts |
| 8-11 | P2 High | 30 minutes | IR Lead + Available Analysts |
| 4-7 | P3 Medium | 2 hours | Next available analyst |
| 1-3 | P4 Low | 24 hours (business hours) | Queued for analyst review |

## Playbook Selection Guide

### By Alert Source
| Alert Source | Likely Playbook | Key Triage Actions |
|-------------|----------------|-------------------|
| EDR - Malware detection | Malware IR | Check quarantine status, verify family |
| Email gateway - Phishing | Phishing IR | Extract IOCs, check delivery scope |
| SIEM - Authentication anomaly | Account Compromise | Verify account, check lateral movement |
| IDS/IPS - Exploit attempt | Vulnerability Exploitation | Verify patch status, check success |
| DLP - Data transfer | Data Exfiltration | Classify data, verify authorization |
| Cloud - Impossible travel | Cloud Account Compromise | Verify user, check API calls |

### By MITRE ATT&CK Tactic
| Tactic | Playbook | Priority |
|--------|----------|----------|
| Initial Access (TA0001) | Perimeter Breach | P1-P2 |
| Execution (TA0002) | Malware/Code Execution | P1-P2 |
| Persistence (TA0003) | Backdoor/Implant | P2 |
| Privilege Escalation (TA0004) | Privilege Escalation | P1 |
| Defense Evasion (TA0005) | Security Tool Bypass | P2 |
| Credential Access (TA0006) | Credential Theft | P1-P2 |
| Discovery (TA0007) | Reconnaissance | P3 |
| Lateral Movement (TA0008) | Lateral Movement | P1 |
| Collection (TA0009) | Data Staging | P2 |
| Exfiltration (TA0010) | Data Breach | P1 |
| Impact (TA0040) | Ransomware/Destruction | P1 |

## IOC Enrichment Workflow

### Step 1: Automated Enrichment
1. Submit IPs to VirusTotal, AbuseIPDB, Shodan
2. Submit file hashes to VirusTotal, MalwareBazaar, Hybrid Analysis
3. Submit domains to URLScan.io, VirusTotal, PassiveTotal
4. Check against internal IOC database and watchlists

### Step 2: Context Addition
1. Look up asset in CMDB for criticality and owner
2. Check user in HR system for role and access level
3. Verify network zone and data classification
4. Cross-reference with recent threat intelligence reports

### Step 3: Correlation
1. Search SIEM for related alerts in past 72 hours
2. Check if same IOCs appeared in other incidents
3. Correlate with ongoing threat campaigns
4. Verify if alert is part of a larger attack chain

## Triage Documentation Requirements
1. Alert details (source, time, raw data)
2. Enrichment results (reputation scores, intelligence hits)
3. Classification decision (incident type, severity, justification)
4. Selected playbook and version
5. Assigned team/analyst
6. Initial timeline of observed events
7. Known affected assets and accounts

---

## Working Template

## Alert Information
| Field | Value |
|-------|-------|
| Alert ID | |
| Alert Source | [SIEM/EDR/IDS/Email Gateway] |
| Alert Name/Rule | |
| Alert Time | YYYY-MM-DD HH:MM UTC |
| Triage Analyst | |
| Triage Start Time | YYYY-MM-DD HH:MM UTC |
| Triage End Time | YYYY-MM-DD HH:MM UTC |

## Alert Details
| Field | Value |
|-------|-------|
| Source IP | |
| Source Hostname | |
| Destination IP | |
| Destination Hostname | |
| Protocol/Port | |
| User Account | |
| File Hash (SHA256) | |
| Domain/URL | |

## IOC Enrichment Results

### IP Reputation
| Source | Score | Details |
|--------|-------|---------|
| VirusTotal | /100 | malicious detections |
| AbuseIPDB | % confidence | reports |
| Shodan | | Open ports/services |
| Internal Intel | | Previous incidents |

### File Hash Reputation
| Source | Score | Details |
|--------|-------|---------|
| VirusTotal | /70+ engines | Family: |
| MalwareBazaar | | Tags: |
| Internal IOC DB | | |

### Domain Reputation
| Source | Score | Details |
|--------|-------|---------|
| VirusTotal | /100 | |
| URLScan.io | | |
| PassiveTotal | | |

## Classification

### Incident Type
- [ ] Malware
- [ ] Ransomware
- [ ] Phishing
- [ ] Unauthorized Access
- [ ] Data Exfiltration
- [ ] DDoS
- [ ] Insider Threat
- [ ] Account Compromise
- [ ] Web Application Attack
- [ ] Privilege Escalation
- [ ] Other: ___________

### MITRE ATT&CK Mapping
| Tactic | Technique ID | Technique Name |
|--------|-------------|----------------|
| | | |

## Severity Assessment

### Scoring Factors
| Factor | Rating | Score |
|--------|--------|-------|
| Asset Criticality | [Critical/High/Medium/Low] | /4 |
| Data Sensitivity | [PII-PHI/PCI/Confidential/Public] | /4 |
| Threat Status | [Active/Confirmed/Attempted/Recon] | /4 |
| Scope | [Enterprise/Department/System/User] | /4 |
| **Total** | | **/16** |

### Severity Determination
| Field | Value |
|-------|-------|
| Severity | [Critical/High/Medium/Low] |
| Priority | [P1/P2/P3/P4] |
| Response SLA | [15 min/30 min/2 hours/24 hours] |
| Justification | |

## Triage Decision
- [ ] **Escalate** - Confirmed incident requiring immediate response
- [ ] **Investigate** - Needs further analysis before confirmation
- [ ] **Monitor** - Suspicious but insufficient evidence; enhanced monitoring
- [ ] **Close - False Positive** - Benign activity; rule tuning recommended
- [ ] **Close - Informational** - Expected/authorized activity

## Playbook Assignment
| Field | Value |
|-------|-------|
| Selected Playbook | |
| Playbook Version | |
| Assigned Team | |
| Primary Analyst | |
| Backup Analyst | |

## Initial Actions Taken
- [ ] Alert acknowledged in SIEM
- [ ] IOCs enriched with threat intel
- [ ] Incident ticket created (ID: ___)
- [ ] Playbook initiated
- [ ] Response team notified
- [ ] Stakeholders informed (if P1/P2)

## Notes
[Additional context, observations, or concerns from triage]
