# Performing Active Directory Penetration Test

## API Reference

## ldap3 Library

### Connection
```python
from ldap3 import Server, Connection, ALL, SUBTREE
server = Server("ldaps://dc.example.com", get_info=ALL, use_ssl=True)
conn = Connection(server, user="DOMAIN\\user", password="pass", auto_bind=True)
```

### Key LDAP Queries

| Purpose | Filter |
|---------|--------|
| All users | `(&(objectClass=user)(objectCategory=person))` |
| Users with SPNs | `(&(objectClass=user)(servicePrincipalName=*))` |
| AS-REP Roastable | `(&(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=4194304))` |
| Domain admins | `(&(objectClass=group)(cn=Domain Admins))` |
| Password policy | `(objectClass=domain)` |

### UserAccountControl Flags

| Flag | Hex | Test |
|------|-----|------|
| ACCOUNTDISABLE | 0x0002 | Account disabled |
| PASSWD_NOTREQD | 0x0020 | No password required |
| DONT_EXPIRE_PASSWORD | 0x10000 | Password never expires |
| DONT_REQ_PREAUTH | 0x400000 | No Kerberos pre-auth |

## Impacket Tools

### GetUserSPNs (Kerberoasting)
```bash
python3 -m impacket.examples.GetUserSPNs DOMAIN/user:pass -dc-ip 10.0.0.1 -request
```

### GetNPUsers (AS-REP Roasting)
```bash
python3 -m impacket.examples.GetNPUsers DOMAIN/ -usersfile users.txt -dc-ip 10.0.0.1
```

### secretsdump (Credential Extraction)
```bash
python3 -m impacket.examples.secretsdump DOMAIN/admin:pass@10.0.0.1
```

## Attack Techniques

### Kerberoasting
1. Enumerate users with SPNs via LDAP
2. Request TGS tickets for those SPNs
3. Extract ticket hashes
4. Crack offline with hashcat (mode 13100)

### AS-REP Roasting
1. Find accounts with pre-auth disabled
2. Request AS-REP without authentication
3. Extract encrypted part of AS-REP
4. Crack offline with hashcat (mode 18200)

### Password Policy Weaknesses
- Min length < 12 characters
- No account lockout threshold
- No password history enforcement
- Password never expires on service accounts

## Output Schema

```json
{
  "report": "ad_penetration_test",
  "domain_info": {"default_naming_context": "DC=example,DC=com"},
  "total_users": 500,
  "total_findings": 12,
  "severity_summary": {"critical": 1, "high": 8, "medium": 3}
}
```

## CLI Usage

```bash
python agent.py --server ldaps://dc.example.com --username "DOMAIN\\user" --password "pass" --output report.json
```

---

## Standards and Controls

## Key Frameworks
- MITRE ATT&CK for Enterprise: https://attack.mitre.org/matrices/enterprise/
- ANSSI AD Security Guide: https://www.cert.ssi.gouv.fr/uploads/guide-ad.html
- Microsoft Tiered Administration Model: https://learn.microsoft.com/en-us/security/privileged-access-workstations/privileged-access-access-model

## MITRE ATT&CK Techniques for AD Testing

| Technique | ID | Description |
|-----------|----|-------------|
| Kerberoasting | T1558.003 | Steal Kerberos TGS tickets for offline cracking |
| AS-REP Roasting | T1558.004 | Target accounts without pre-auth |
| DCSync | T1003.006 | Replicate domain credentials via DRSUAPI |
| Golden Ticket | T1558.001 | Forge TGT using krbtgt hash |
| Pass-the-Hash | T1550.002 | Authenticate using NTLM hash |
| Unconstrained Delegation | T1558 | Abuse delegation to steal TGTs |
| ADCS Abuse | T1649 | Exploit misconfigured certificate templates |

## AD Security Benchmarks
- CIS Microsoft Windows Server Benchmark
- STIG (Security Technical Implementation Guide) for Windows
- Microsoft Security Compliance Toolkit

---

## Workflows

## AD Attack Flow

```
Domain User Credentials
    │
    ├── Enumeration
    │   ├── BloodHound (attack paths)
    │   ├── LDAP queries (users, groups, GPOs)
    │   └── Service account discovery (SPNs)
    │
    ├── Kerberos Attacks
    │   ├── Kerberoasting → Hash cracking
    │   ├── AS-REP Roasting → Hash cracking
    │   └── Delegation abuse (unconstrained/constrained/RBCD)
    │
    ├── ADCS Attacks
    │   ├── ESC1-ESC8 template exploitation
    │   └── Certificate-based auth to DA
    │
    ├── Credential Harvesting
    │   ├── LSASS dump (Mimikatz)
    │   ├── SAM/SYSTEM extraction
    │   └── DPAPI credential decryption
    │
    ├── Domain Escalation
    │   ├── DCSync (krbtgt + all hashes)
    │   ├── Golden Ticket
    │   └── AdminSDHolder persistence
    │
    └── Impact Demonstration
        ├── Full domain hash extraction
        ├── Access to sensitive resources
        └── Cross-forest trust abuse
```

---

## Working Template

## Document Control
| Field | Value |
|-------|-------|
| Domain | [corp.local] |
| Test Type | Active Directory Security Assessment |
| Starting Access | Standard Domain User |
| Period | [Start] — [End] |

## Executive Summary
[Summary of AD security posture, key attack paths discovered, and domain compromise status]

## Attack Path Diagram
```
testuser (Domain User)
  → Kerberoasting svc_sql (T1558.003)
    → Cracked password: "SqlServer2024!"
      → Local admin on SQL01 (T1078)
        → Mimikatz LSASS dump (T1003.001)
          → DA credentials: da_admin
            → DCSync all hashes (T1003.006)
              → FULL DOMAIN COMPROMISE
```

## Findings

### Finding [N]: [Title]
| Attribute | Detail |
|-----------|--------|
| Severity | [Critical/High/Medium/Low] |
| MITRE ATT&CK | [Technique] |
| Affected | [Accounts/Systems] |
| Remediation | [Fix] |

## Remediation Priority
| # | Action | Timeline |
|---|--------|----------|
| 1 | Deploy gMSA for service accounts | 2 weeks |
| 2 | Fix ADCS vulnerable templates | 1 week |
| 3 | Implement tiered admin model | 30 days |
| 4 | Enable LAPS | 30 days |
