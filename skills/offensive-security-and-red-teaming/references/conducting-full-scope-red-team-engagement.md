# Conducting Full Scope Red Team Engagement

## API Reference

## Libraries

| Library | Install | Purpose |
|---------|---------|---------|
| attackcti | `pip install attackcti` | MITRE ATT&CK STIX/TAXII client for technique enumeration |
| impacket | `pip install impacket` | AD attack tools (secretsdump, psexec, wmiexec) |
| requests | `pip install requests` | HTTP client for C2 API integration |

## Key attackcti Methods

| Method | Description |
|--------|-------------|
| `attack_client()` | Initialize MITRE ATT&CK client |
| `client.get_enterprise_techniques()` | List all Enterprise techniques |
| `client.get_enterprise_mitigations()` | List mitigations |
| `client.get_groups()` | List threat actor groups |
| `client.get_software()` | List tools and malware |

## Engagement Phases (PTES Framework)

| Phase | Duration | Key Activities |
|-------|----------|----------------|
| Pre-engagement | 1-2 weeks | Scoping, RoE, legal agreements |
| Reconnaissance | 3-5 days | OSINT, footprinting, enumeration |
| Initial Access | 5-7 days | Phishing, exploits, physical |
| Post-exploitation | 5-7 days | Lateral movement, persistence, privilege escalation |
| Objective | 2-3 days | Crown jewel access, exfiltration simulation |
| Reporting | 3-5 days | Findings, remediation, executive brief |

## C2 Frameworks

| Framework | Type | Protocol |
|-----------|------|----------|
| Cobalt Strike | Commercial | HTTPS, DNS, SMB |
| Sliver | Open source | mTLS, HTTPS, DNS, WireGuard |
| Mythic | Open source | HTTP, websocket, custom |

## External References

- [MITRE ATT&CK Enterprise Matrix](https://attack.mitre.org/matrices/enterprise/)
- [PTES Standard](http://www.pentest-standard.org/)
- [attackcti Documentation](https://attackcti.readthedocs.io/)
- [Sliver C2 Wiki](https://github.com/BishopFox/sliver/wiki)

---

## Standards and Controls

## MITRE ATT&CK Techniques

### Reconnaissance (TA0043)
- **T1593** - Search Open Websites/Domains
- **T1593.001** - Social Media
- **T1593.002** - Search Engines
- **T1589** - Gather Victim Identity Information
- **T1589.001** - Credentials
- **T1589.002** - Email Addresses
- **T1590** - Gather Victim Network Information
- **T1590.002** - DNS
- **T1590.005** - IP Addresses
- **T1591** - Gather Victim Org Information

### Resource Development (TA0042)
- **T1583.001** - Acquire Infrastructure: Domains
- **T1583.003** - Acquire Infrastructure: Virtual Private Server
- **T1587.001** - Develop Capabilities: Malware
- **T1587.003** - Develop Capabilities: Digital Certificates
- **T1608.001** - Stage Capabilities: Upload Malware

### Initial Access (TA0001)
- **T1566.001** - Phishing: Spearphishing Attachment
- **T1566.002** - Phishing: Spearphishing Link
- **T1190** - Exploit Public-Facing Application
- **T1078** - Valid Accounts
- **T1133** - External Remote Services
- **T1195.002** - Supply Chain Compromise: Compromise Software Supply Chain

### Execution (TA0002)
- **T1059.001** - Command and Scripting Interpreter: PowerShell
- **T1059.003** - Command and Scripting Interpreter: Windows Command Shell
- **T1204.001** - User Execution: Malicious Link
- **T1204.002** - User Execution: Malicious File
- **T1047** - Windows Management Instrumentation

### Persistence (TA0003)
- **T1053.005** - Scheduled Task/Job: Scheduled Task
- **T1547.001** - Boot or Logon Autostart Execution: Registry Run Keys
- **T1136.001** - Create Account: Local Account
- **T1098** - Account Manipulation

### Privilege Escalation (TA0004)
- **T1068** - Exploitation for Privilege Escalation
- **T1548.002** - Abuse Elevation Control Mechanism: Bypass User Account Control
- **T1134** - Access Token Manipulation

### Defense Evasion (TA0005)
- **T1055** - Process Injection
- **T1027** - Obfuscated Files or Information
- **T1562.001** - Impair Defenses: Disable or Modify Tools
- **T1070.004** - Indicator Removal: File Deletion

### Credential Access (TA0006)
- **T1003.001** - OS Credential Dumping: LSASS Memory
- **T1003.006** - OS Credential Dumping: DCSync
- **T1558.003** - Steal or Forge Kerberos Tickets: Kerberoasting
- **T1110** - Brute Force

### Discovery (TA0007)
- **T1087.002** - Account Discovery: Domain Account
- **T1018** - Remote System Discovery
- **T1069.002** - Permission Groups Discovery: Domain Groups
- **T1082** - System Information Discovery

### Lateral Movement (TA0008)
- **T1021.002** - Remote Services: SMB/Windows Admin Shares
- **T1021.001** - Remote Services: Remote Desktop Protocol
- **T1550.002** - Use Alternate Authentication Material: Pass the Hash
- **T1047** - Windows Management Instrumentation

### Collection (TA0009)
- **T1560** - Archive Collected Data
- **T1213** - Data from Information Repositories

### Exfiltration (TA0010)
- **T1041** - Exfiltration Over C2 Channel
- **T1048.003** - Exfiltration Over Alternative Protocol: Exfiltration Over Unencrypted Non-C2 Protocol

## NIST References

- **NIST SP 800-115** - Technical Guide to Information Security Testing and Assessment
- **NIST SP 800-53 Rev. 5** - Security and Privacy Controls (CA-8: Penetration Testing)
- **NIST SP 800-53A** - Assessing Security and Privacy Controls (CA-8 assessment procedures)
- **NIST CSF 2.0** - Identify, Protect, Detect, Respond, Recover functions

## Industry Frameworks

- **PTES** - Penetration Testing Execution Standard (Pre-engagement, Intelligence Gathering, Threat Modeling, Vulnerability Analysis, Exploitation, Post-Exploitation, Reporting)
- **OSSTMM** - Open Source Security Testing Methodology Manual v3
- **TIBER-EU** - European Central Bank Threat Intelligence-Based Ethical Red Teaming
- **CBEST** - Bank of England intelligence-led penetration testing framework
- **CREST** - Council of Registered Ethical Security Testers certification standards
- **STAR** - Simulated Targeted Attack and Response (Bank of Canada)

## Compliance Alignments

| Framework | Control | Description |
|---|---|---|
| PCI DSS 4.0 | 11.4 | External and internal penetration testing |
| SOC 2 | CC7.1 | Identification and management of vulnerabilities |
| ISO 27001 | A.18.2.3 | Technical compliance review |
| HIPAA | 164.308(a)(8) | Evaluation of security measures |
| FFIEC | IS.2.M.7 | Penetration testing program |

---

## Workflows

## Engagement Lifecycle Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    RED TEAM ENGAGEMENT LIFECYCLE                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. SCOPING & PLANNING                                           │
│     ├── Define Rules of Engagement (RoE)                         │
│     ├── Identify threat actors to emulate                        │
│     ├── Define objectives and success criteria                   │
│     ├── Establish communication channels and emergency stops     │
│     └── Legal authorization and sign-off                         │
│                                                                  │
│  2. RECONNAISSANCE (2-4 weeks)                                   │
│     ├── Passive OSINT collection                                 │
│     │   ├── DNS enumeration (Amass, subfinder)                   │
│     │   ├── Email harvesting (theHarvester)                      │
│     │   ├── Social media profiling (LinkedIn, Twitter)           │
│     │   └── Credential breach searches (DeHashed)                │
│     ├── Active scanning (if in scope)                            │
│     │   ├── Port/service scanning (Nmap)                         │
│     │   ├── Web application discovery (Aquatone)                 │
│     │   └── Vulnerability scanning (Nuclei)                      │
│     └── Target prioritization matrix                             │
│                                                                  │
│  3. WEAPONIZATION (1-2 weeks)                                    │
│     ├── Develop custom payloads                                  │
│     │   ├── Shellcode generation and encryption                  │
│     │   ├── Loader development (C/C++, Rust, Nim)                │
│     │   └── Sandbox evasion techniques                           │
│     ├── Configure C2 infrastructure                              │
│     │   ├── Deploy team server (Havoc/Cobalt Strike)             │
│     │   ├── Set up HTTPS redirectors                             │
│     │   ├── Configure domain fronting or CDN                     │
│     │   └── Test beacon callbacks                                │
│     └── Prepare phishing infrastructure                          │
│         ├── Register look-alike domains                          │
│         ├── Configure SPF/DKIM/DMARC                             │
│         └── Design email templates                               │
│                                                                  │
│  4. INITIAL ACCESS (1-2 weeks)                                   │
│     ├── Execute phishing campaign (T1566)                        │
│     ├── Exploit external services (T1190)                        │
│     ├── Credential stuffing/spraying (T1110)                     │
│     ├── Supply chain vectors (T1195)                             │
│     └── Physical access attempts (if in scope)                   │
│                                                                  │
│  5. POST-EXPLOITATION (2-4 weeks)                                │
│     ├── Establish persistence (T1053, T1547)                     │
│     ├── Privilege escalation                                     │
│     │   ├── Local priv esc (T1068, T1548)                        │
│     │   └── Domain priv esc (Kerberoasting, DCSync)              │
│     ├── Credential harvesting                                    │
│     │   ├── LSASS dump (T1003.001)                               │
│     │   ├── SAM database (T1003.002)                             │
│     │   └── Kerberos tickets (T1558)                             │
│     ├── Lateral movement                                         │
│     │   ├── SMB (T1021.002)                                      │
│     │   ├── WMI (T1047)                                          │
│     │   ├── WinRM (T1021.006)                                    │
│     │   └── RDP (T1021.001)                                      │
│     └── Objective pursuit                                        │
│         ├── Crown jewel identification                           │
│         ├── Data staging (T1074)                                 │
│         └── Exfiltration demonstration (T1041)                   │
│                                                                  │
│  6. REPORTING & DEBRIEF (1-2 weeks)                              │
│     ├── Attack narrative with timeline                           │
│     ├── MITRE ATT&CK heat map                                   │
│     ├── Detection gap analysis                                   │
│     ├── Remediation recommendations                              │
│     ├── Executive debrief presentation                           │
│     └── Purple team follow-up sessions                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Decision Tree: Initial Access Vector Selection

```
START: Select Initial Access Vector
│
├── Is phishing in scope?
│   ├── YES → Target high-value employees
│   │         ├── C-suite → CEO fraud / whale phishing
│   │         ├── IT Staff → Credential harvesting
│   │         └── HR/Finance → Malicious attachment
│   └── NO → Proceed to external attack surface
│
├── External-facing services found?
│   ├── VPN → Check for CVEs (Fortinet, Pulse Secure, Citrix)
│   ├── Exchange → ProxyShell/ProxyLogon
│   ├── Web Apps → OWASP Top 10, file upload, RCE
│   └── RDP → Brute force / credential stuffing
│
└── Physical access in scope?
    ├── Badge cloning (Proxmark3)
    ├── Tailgating
    └── Rogue device deployment (LAN Turtle)
```

## Operational Security (OPSEC) Checklist

1. **Infrastructure Separation**: Separate attack infrastructure from assessment infrastructure
2. **Redirectors**: Use HTTPS redirectors between C2 and targets
3. **Domain Aging**: Register domains 30+ days before engagement
4. **Categorization**: Categorize phishing domains before use (Bluecoat, Fortiguard)
5. **Payload Testing**: Test payloads against VirusTotal alternatives (antiscan.me)
6. **Log Rotation**: Rotate and encrypt operational logs
7. **Clean-up**: Remove all implants and artifacts post-engagement
8. **Communication**: Use encrypted channels for team coordination (Signal, Keybase)

## TTPs Execution Checklist

| Phase | TTP | Tool | Status |
|---|---|---|---|
| Recon | T1593 - Open Website Search | Amass, Recon-ng | [ ] |
| Recon | T1589 - Victim Identity Info | theHarvester, LinkedIn | [ ] |
| Initial Access | T1566.001 - Spearphishing | GoPhish, custom | [ ] |
| Execution | T1059.001 - PowerShell | Custom stager | [ ] |
| Persistence | T1053.005 - Scheduled Task | schtasks.exe | [ ] |
| Priv Esc | T1558.003 - Kerberoasting | Rubeus | [ ] |
| Defense Evasion | T1055 - Process Injection | Custom loader | [ ] |
| Credential Access | T1003.001 - LSASS Memory | Mimikatz/SafetyKatz | [ ] |
| Discovery | T1087.002 - Domain Account Discovery | BloodHound/SharpHound | [ ] |
| Lateral Movement | T1021.002 - SMB/Admin Shares | PsExec, wmiexec | [ ] |
| Collection | T1560 - Archive Data | 7-Zip, tar | [ ] |
| Exfiltration | T1041 - Exfil Over C2 | Havoc/CS download | [ ] |

---

## Working Template

## Document Control

| Field | Value |
|---|---|
| Engagement ID | RT-2025-XXX |
| Client Name | [Organization Name] |
| Report Date | YYYY-MM-DD |
| Classification | CONFIDENTIAL |
| Report Version | 1.0 |
| Lead Operator | [Name] |
| Reviewed By | [Name] |

---

## 1. Executive Summary

### 1.1 Engagement Overview

[Organization Name] engaged [Red Team Company] to conduct a full-scope red team assessment from [start date] to [end date]. The engagement simulated the tactics, techniques, and procedures (TTPs) of [Threat Actor], targeting [objectives].

### 1.2 Key Findings Summary

| # | Finding | Severity | Detected |
|---|---|---|---|
| 1 | [Finding Title] | Critical | No |
| 2 | [Finding Title] | High | Yes |
| 3 | [Finding Title] | High | No |
| 4 | [Finding Title] | Medium | Yes |

### 1.3 Overall Risk Rating

**[CRITICAL / HIGH / MEDIUM / LOW]**

The red team achieved [X of Y] defined objectives, with [Z]% of activities detected by the security operations center. Critical gaps were identified in [area 1], [area 2], and [area 3].

### 1.4 Metrics at a Glance

| Metric | Value |
|---|---|
| Total TTPs Executed | XX |
| Detection Rate | XX% |
| Mean Time to Detect | XX hours |
| Objectives Achieved | X/Y |
| Dwell Time (Undetected) | XX days |
| Unique Hosts Compromised | XX |
| Credentials Harvested | XX |

---

## 2. Scope and Rules of Engagement

### 2.1 Engagement Scope

**In-Scope:**
- Network ranges: [CIDR ranges]
- Domains: [domains]
- Physical locations: [if applicable]
- Personnel: [if social engineering in scope]

**Out-of-Scope:**
- [Systems/networks excluded]
- [Actions prohibited]

### 2.2 Rules of Engagement

- Authorization document reference: [RoE document ID]
- Approved hours of operation: [hours]
- Emergency contact: [name, phone]
- Deconfliction process: [description]

### 2.3 Threat Profile

**Emulated Adversary:** [Threat Actor Name]
- MITRE ATT&CK Group: [Group ID]
- Known Targets: [industries/regions]
- Typical TTPs: [summary of techniques]

---

## 3. Attack Narrative

### 3.1 Engagement Timeline

```
Day 1-5:   Reconnaissance and OSINT
Day 6-8:   Infrastructure setup and payload development
Day 9-12:  Initial access attempts
Day 13-20: Post-exploitation, lateral movement, persistence
Day 21-25: Objective pursuit and data exfiltration
Day 26-28: Cleanup and evidence collection
```

### 3.2 Phase 1: Reconnaissance

**Objective:** Identify attack surface and high-value targets

| Action | Technique | Result |
|---|---|---|
| Subdomain enumeration | T1593 | Found XX subdomains |
| Employee enumeration | T1589.002 | Identified XX employees |
| Credential search | T1589.001 | Found XX breached credentials |

**Key Discoveries:**
- [Discovery 1 with evidence]
- [Discovery 2 with evidence]

### 3.3 Phase 2: Initial Access

**Objective:** Establish initial foothold on target network

**Vector Used:** [T1566.001 Spearphishing / T1190 Exploit / etc.]

**Detailed Walkthrough:**
1. [Step 1 with screenshot reference]
2. [Step 2 with screenshot reference]
3. [Step 3 with screenshot reference]

**Detection Status:** [Detected/Undetected] by [source] at [time]

### 3.4 Phase 3: Post-Exploitation

**Objective:** Escalate privileges and establish persistence

| Action | Technique | Host | Result | Detected |
|---|---|---|---|---|
| Credential dump | T1003.001 | WS-XXX | Obtained X creds | Yes/No |
| Kerberoasting | T1558.003 | DC01 | Cracked X SPNs | Yes/No |
| Scheduled task | T1053.005 | WS-XXX | Persistence set | Yes/No |

### 3.5 Phase 4: Lateral Movement

**Objective:** Move toward crown jewel systems

**Attack Path:**
```
Initial Foothold (WS-042)
    └── Credential Reuse (T1078)
        └── File Server (FS01) via PsExec (T1021.002)
            └── Database Server (DB01) via RDP (T1021.001)
                └── Domain Controller (DC01) via DCSync (T1003.006)
```

### 3.6 Phase 5: Objective Achievement

| Objective | Status | Evidence |
|---|---|---|
| Domain Admin Access | Achieved | DCSync of krbtgt hash |
| PII Data Exfiltration | Achieved | 50MB exfiled over C2 |
| SCADA Network Access | Not Achieved | Network segmentation prevented access |

---

## 4. MITRE ATT&CK Mapping

### 4.1 Technique Heat Map

[Insert ATT&CK Navigator layer screenshot]

Navigator JSON file: `engagement_navigator.json`

### 4.2 Techniques Used

| Technique ID | Technique Name | Tactic | Used | Detected |
|---|---|---|---|---|
| T1566.001 | Spearphishing Attachment | Initial Access | Yes | Yes |
| T1059.001 | PowerShell | Execution | Yes | No |
| T1003.001 | LSASS Memory | Credential Access | Yes | Yes |
| T1558.003 | Kerberoasting | Credential Access | Yes | No |
| T1021.002 | SMB Admin Shares | Lateral Movement | Yes | No |
| T1003.006 | DCSync | Credential Access | Yes | Yes |
| T1041 | Exfil Over C2 Channel | Exfiltration | Yes | No |

---

## 5. Findings

### Finding 1: [Title]

| Field | Value |
|---|---|
| Severity | Critical |
| CVSS Score | 9.8 |
| Affected Systems | [list] |
| MITRE ATT&CK | [technique ID] |

**Description:** [Detailed description of the vulnerability or gap]

**Evidence:** [Screenshots, logs, proof of exploitation]

**Impact:** [Business impact assessment]

**Recommendation:** [Specific remediation steps]

---

## 6. Detection Gap Analysis

### 6.1 Summary

| Category | Count | Percentage |
|---|---|---|
| Actions Detected | X | XX% |
| Actions Undetected | X | XX% |
| Techniques with Zero Coverage | X | - |

### 6.2 Gaps by Tactic

| Tactic | Actions | Detected | Gap |
|---|---|---|---|
| Initial Access | X | X | XX% |
| Execution | X | X | XX% |
| Persistence | X | X | XX% |
| Credential Access | X | X | XX% |
| Lateral Movement | X | X | XX% |
| Exfiltration | X | X | XX% |

### 6.3 Priority Detection Rules Needed

1. **[Detection Rule Name]** - Detect [technique] via [data source]
2. **[Detection Rule Name]** - Detect [technique] via [data source]
3. **[Detection Rule Name]** - Detect [technique] via [data source]

---

## 7. Recommendations

### 7.1 Immediate (0-30 days)
1. [Critical remediation action]
2. [Critical remediation action]

### 7.2 Short-Term (30-90 days)
1. [High-priority improvement]
2. [High-priority improvement]

### 7.3 Long-Term (90-180 days)
1. [Strategic improvement]
2. [Strategic improvement]

---

## 8. Appendices

### Appendix A: Tools Used
| Tool | Purpose | Version |
|---|---|---|
| Havoc | C2 Framework | 0.7 |
| Impacket | AD Attacks | 0.11.0 |
| Rubeus | Kerberos Attacks | 2.3.0 |
| BloodHound | AD Reconnaissance | 4.3 |

### Appendix B: IOCs for Deconfliction
| Type | Value | Context |
|---|---|---|
| IP | X.X.X.X | C2 Server |
| Domain | c2.example.com | C2 Domain |
| Hash | [SHA256] | Payload |
| User-Agent | [string] | C2 Callback |

### Appendix C: Cleanup Confirmation
- [ ] All implants removed
- [ ] All persistence mechanisms removed
- [ ] All created accounts deleted
- [ ] All modified configurations restored
- [ ] Infrastructure decommissioned
