# Conducting Internal Network Penetration Test

## API Reference

## Libraries

| Library | Install | Purpose |
|---------|---------|---------|
| ldap3 | `pip install ldap3` | LDAP queries for AD enumeration |
| impacket | `pip install impacket` | SMB relay, credential dumping, lateral movement tools |
| python-nmap | `pip install python-nmap` | Python wrapper for nmap scanning |

## Key Tools & Commands

| Tool | Command | Purpose |
|------|---------|---------|
| nmap | `nmap -sV -sC --top-ports 1000 <target>` | Service version and script scan |
| Responder | `responder -I eth0 -A` | LLMNR/NBT-NS poisoning (analyze mode) |
| CrackMapExec | `cme smb <target> --gen-relay-list` | Find hosts with SMB signing disabled |
| BloodHound | `bloodhound-python -d domain -u user -p pass` | AD attack path mapping |
| ntlmrelayx | `ntlmrelayx.py -t <target> -smb2support` | NTLM relay attack |

## Common Internal Vulnerabilities

| Vulnerability | Impact | CVSS |
|--------------|--------|------|
| SMB signing disabled | NTLM relay attacks | 7.5 |
| LLMNR/NBT-NS enabled | Credential capture | 7.0 |
| Default credentials | Unauthorized access | 9.0 |
| Unpatched EternalBlue (MS17-010) | Remote code execution | 9.8 |
| Kerberoasting-eligible SPNs | Offline password cracking | 7.5 |

## Windows Event IDs for Detection

| Event ID | Description |
|----------|-------------|
| 4625 | Failed logon attempt (brute force indicator) |
| 4648 | Logon with explicit credentials |
| 4768 | Kerberos TGT request |
| 4769 | Kerberos service ticket request |

## External References

- [nmap Reference Guide](https://nmap.org/book/man.html)
- [ldap3 Documentation](https://ldap3.readthedocs.io/)
- [impacket Examples](https://github.com/fortra/impacket/tree/master/examples)
- [PTES Technical Guidelines](http://www.pentest-standard.org/index.php/PTES_Technical_Guidelines)

---

## Standards and Controls

## Frameworks
- PTES: http://www.pentest-standard.org/
- OSSTMM v3: https://www.isecom.org/OSSTMM.3.pdf
- NIST SP 800-115: https://csrc.nist.gov/publications/detail/sp/800-115/final
- MITRE ATT&CK Enterprise: https://attack.mitre.org/matrices/enterprise/

## Key MITRE ATT&CK Techniques for Internal Testing

| Tactic | Technique | ID |
|--------|-----------|----|
| Discovery | Network Service Discovery | T1046 |
| Credential Access | LLMNR/NBT-NS Poisoning | T1557.001 |
| Credential Access | Kerberoasting | T1558.003 |
| Credential Access | OS Credential Dumping | T1003 |
| Lateral Movement | Remote Services: SMB | T1021.002 |
| Lateral Movement | Pass the Hash | T1550.002 |
| Privilege Escalation | Domain Policy Modification | T1484 |
| Collection | Data from Network Shared Drive | T1039 |

## Compliance Requirements

| Standard | Internal Pentest Requirement |
|----------|----------------------------|
| PCI DSS v4.0 | Req 11.4.2 — Internal penetration testing annually |
| ISO 27001 | A.18.2.3 — Technical compliance review |
| SOC 2 | CC7.1 — Detection and monitoring |
| NIST CSF | PR.IP-12, DE.CM |

---

## Workflows

## Attack Flow

```
Network Access (Ethernet/VPN)
    │
    ├── Network Discovery (Nmap, ARP scan)
    │
    ├── Credential Capture (Responder, mitm6)
    │       │
    │       └── Hash Cracking (Hashcat)
    │
    ├── AD Enumeration (BloodHound, LDAP)
    │       │
    │       ├── Kerberoasting
    │       ├── AS-REP Roasting
    │       └── GPP Password Extraction
    │
    ├── Lateral Movement (PsExec, WMI, WinRM)
    │       │
    │       └── Credential Harvesting (Mimikatz, LSASS dump)
    │
    ├── Privilege Escalation
    │       │
    │       ├── Local (unquoted paths, token impersonation)
    │       └── Domain (DCSync, Golden Ticket, ADCS)
    │
    └── Impact Demonstration
            ├── Sensitive data access
            ├── Domain compromise proof
            └── Attack path documentation
```

## Evidence Collection Workflow

```
evidence/
├── credentials/
│   ├── responder_captures/
│   ├── cracked_hashes/
│   └── dumped_creds/
├── screenshots/
├── bloodhound/
│   └── domain_data.json
├── scan_results/
│   ├── nmap/
│   └── shares/
└── attack_paths/
    └── path_documentation.md
```

---

## Working Template

## Document Control

| Field | Value |
|-------|-------|
| Client | [Client Name] |
| Assessment Type | Internal Network Penetration Test |
| Access Model | Assumed Breach / Unauthenticated |
| Test Period | [Start] — [End] |
| Classification | CONFIDENTIAL |

---

## 1. Executive Summary

### Scope
- **Subnet(s):** [Internal ranges]
- **Domain:** [AD domain]
- **Starting Position:** [Network drop location / VPN / credentials provided]

### Key Findings

| Severity | Count | Example |
|----------|-------|---------|
| Critical | [N] | Domain compromise via credential relay |
| High | [N] | Kerberoastable service accounts with weak passwords |
| Medium | [N] | SMB signing disabled on file servers |
| Low | [N] | Excessive share permissions |

### Attack Path Summary
[Describe the primary attack chain from initial access to domain compromise]

---

## 2. Technical Findings

### Finding [N]: [Title]

| Attribute | Detail |
|-----------|--------|
| Severity | [Critical/High/Medium/Low] |
| CVSS v3.1 | [Score] |
| MITRE ATT&CK | [Technique ID] |
| Affected Assets | [Hosts/accounts] |

**Description:** [Details]
**Steps to Reproduce:** [Steps]
**Evidence:** [Screenshots/logs]
**Remediation:** [Fix]

---

## 3. Recommendations Priority

| Priority | Action | Timeline |
|----------|--------|----------|
| P1 | Disable LLMNR/NBT-NS, enable SMB signing | 1 week |
| P2 | Deploy LAPS, implement tiered admin | 30 days |
| P3 | Enforce strong password policy | 30 days |
| P4 | Review share permissions | 60 days |
