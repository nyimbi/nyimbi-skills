# Performing Active Directory Bloodhound Analysis

## API Reference

## neo4j Python Driver
```python
from neo4j import GraphDatabase
driver = GraphDatabase.driver(uri, auth=(user, password))
driver.verify_connectivity()
with driver.session() as session:
    results = session.run(query, parameters)
    records = [dict(record) for record in results]
driver.close()
```

## Key BloodHound Cypher Queries

### Domain Admins
```cypher
MATCH (u:User)-[:MemberOf*1..]->(g:Group)
WHERE g.name STARTS WITH 'DOMAIN ADMINS'
RETURN u.name, u.enabled
```

### Shortest Path to DA
```cypher
MATCH p=shortestPath((u:User {owned:true})-[*1..]->(g:Group))
WHERE g.name STARTS WITH 'DOMAIN ADMINS'
RETURN u.name, length(p) AS hops ORDER BY hops
```

### Kerberoastable Users
```cypher
MATCH (u:User) WHERE u.hasspn=true AND u.enabled=true
RETURN u.name, u.serviceprincipalnames
```

### Unconstrained Delegation
```cypher
MATCH (c:Computer) WHERE c.unconstraineddelegation=true
RETURN c.name, c.operatingsystem
```

## BloodHound Node Types
| Node | Properties |
|------|-----------|
| User | name, enabled, hasspn, admincount, owned, dontreqpreauth |
| Computer | name, operatingsystem, unconstraineddelegation, enabled |
| Group | name, admincount, objectid |
| GPO | name, gpcpath |
| OU | name, guid |

## BloodHound Edge Types
| Edge | Meaning |
|------|---------|
| MemberOf | Group membership |
| AdminTo | Local admin rights |
| HasSession | Active session on computer |
| GenericAll | Full object control |
| WriteDacl | Can modify ACL |
| GpLink | GPO linked to OU |

---

## Standards and Controls

## MITRE ATT&CK Techniques

### Discovery (TA0007)
- **T1087.002** - Account Discovery: Domain Account
- **T1069.001** - Permission Groups Discovery: Local Groups
- **T1069.002** - Permission Groups Discovery: Domain Groups
- **T1018** - Remote System Discovery
- **T1482** - Domain Trust Discovery
- **T1615** - Group Policy Discovery
- **T1016** - System Network Configuration Discovery
- **T1049** - System Network Connections Discovery
- **T1033** - System Owner/User Discovery

### Lateral Movement (TA0008) - Paths Identified by BloodHound
- **T1550.002** - Use Alternate Authentication Material: Pass the Hash
- **T1550.003** - Use Alternate Authentication Material: Pass the Ticket
- **T1021.002** - Remote Services: SMB/Windows Admin Shares
- **T1021.001** - Remote Services: Remote Desktop Protocol
- **T1021.006** - Remote Services: Windows Remote Management

### Credential Access (TA0006) - Attacks Enabled by BloodHound
- **T1558.003** - Steal or Forge Kerberos Tickets: Kerberoasting
- **T1558.004** - Steal or Forge Kerberos Tickets: AS-REP Roasting
- **T1003.006** - OS Credential Dumping: DCSync
- **T1558.001** - Steal or Forge Kerberos Tickets: Golden Ticket

### Privilege Escalation (TA0004)
- **T1484.001** - Domain Policy Modification: Group Policy Modification
- **T1078.002** - Valid Accounts: Domain Accounts
- **T1134** - Access Token Manipulation

## BloodHound Software Entry
- **MITRE ATT&CK ID**: S0521
- **Type**: Tool
- **Platforms**: Windows, Azure AD
- **Associated Groups**: FIN7, APT29, Wizard Spider

## NIST References
- **NIST SP 800-53 Rev. 5** - AC-6: Least Privilege
- **NIST SP 800-53 Rev. 5** - AC-2: Account Management
- **NIST SP 800-53 Rev. 5** - IA-5: Authenticator Management
- **NIST SP 800-171** - 3.1.5: Least Privilege

## CIS Benchmarks
- **CIS Microsoft Windows Server 2022** - Section 2.3.10: Network access
- **CIS Active Directory Benchmark** - Section 1: Account Policies
- **CIS Controls v8** - Control 6: Access Control Management
- **CIS Controls v8** - Control 5: Account Management

## Active Directory Security Hardening Standards
- Microsoft Tier Model for Active Directory Administration
- Microsoft Privileged Access Workstation (PAW) Architecture
- ANSSI Active Directory Security Hardening Guide
- ASD Essential Eight: Restrict Administrative Privileges

---

## Workflows

## BloodHound Analysis Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│              BLOODHOUND ANALYSIS WORKFLOW                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. DATA COLLECTION                                              │
│     ├── Select collector (SharpHound/AzureHound)                 │
│     ├── Choose collection method                                 │
│     │   ├── All (comprehensive, noisy)                           │
│     │   ├── DCOnly (LDAP only, stealthier)                       │
│     │   ├── Session (user sessions on computers)                 │
│     │   └── ACL (permission relationships)                       │
│     ├── Execute collection                                       │
│     └── Exfiltrate ZIP to analysis workstation                   │
│                                                                  │
│  2. DATA IMPORT                                                  │
│     ├── Start BloodHound CE/Neo4j                                │
│     ├── Upload collection ZIP                                    │
│     ├── Verify node counts (Users, Computers, Groups)            │
│     └── Mark owned principals and high-value targets             │
│                                                                  │
│  3. INITIAL ANALYSIS                                             │
│     ├── Run pre-built analytics                                  │
│     │   ├── Find all Domain Admins                               │
│     │   ├── Find Kerberoastable accounts                         │
│     │   ├── Find AS-REP Roastable accounts                       │
│     │   ├── Find unconstrained delegation                        │
│     │   └── Find shortest paths to DA                            │
│     ├── Identify high-value targets                              │
│     └── Document initial findings                                │
│                                                                  │
│  4. ATTACK PATH IDENTIFICATION                                   │
│     ├── Mark owned nodes                                         │
│     ├── Shortest path from owned to DA                           │
│     ├── Analyze ACL abuse paths                                  │
│     │   ├── GenericAll / GenericWrite                             │
│     │   ├── WriteDACL / WriteOwner                               │
│     │   ├── ForceChangePassword                                  │
│     │   └── AddMember                                            │
│     ├── Analyze delegation abuse                                 │
│     ├── Analyze GPO abuse paths                                  │
│     └── Prioritize attack paths by feasibility                   │
│                                                                  │
│  5. EXPLOITATION                                                 │
│     ├── Execute selected attack path                             │
│     ├── Kerberoast service accounts                              │
│     ├── Abuse ACL misconfigurations                              │
│     ├── Leverage delegation settings                             │
│     └── Mark newly owned principals                              │
│                                                                  │
│  6. REPORTING                                                    │
│     ├── Export attack path screenshots                           │
│     ├── Document each hop in attack chain                        │
│     ├── Map to MITRE ATT&CK techniques                          │
│     ├── Provide remediation for each finding                     │
│     └── Generate AD hardening recommendations                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## SharpHound Collection Method Selection

```
Collection Method Decision
│
├── Need comprehensive data?
│   └── Use -c All (Collects everything)
│       Warning: Noisy, generates LDAP and SMB traffic
│
├── Need stealth?
│   └── Use -c DCOnly (Queries only DCs via LDAP)
│       Limitation: No session or local group data
│
├── Need session data over time?
│   └── Use -c Session --loop
│       Best for: Finding where admins are logged in
│
├── Azure AD environment?
│   └── Use AzureHound
│       Collects: Roles, App Registrations, Service Principals
│
└── Minimal footprint needed?
    └── Use -c Group,ACL
        Collects: Group memberships and ACL relationships only
```

## Attack Path Exploitation Decision Tree

```
BloodHound Shows Path to DA
│
├── Path via Kerberoastable account?
│   ├── Request TGS ticket (Rubeus/GetUserSPNs)
│   ├── Crack with hashcat (-m 13100)
│   └── Use cracked credential to continue path
│
├── Path via ACL abuse?
│   ├── GenericAll on user? → ForceChangePassword
│   ├── GenericAll on group? → Add self to group
│   ├── WriteDACL? → Grant self GenericAll, then abuse
│   ├── WriteOwner? → Change owner, then modify DACL
│   └── AddMember? → Add self to privileged group
│
├── Path via delegation?
│   ├── Unconstrained? → Coerce DC auth + capture TGT
│   ├── Constrained? → S4U2Self + S4U2Proxy abuse
│   └── RBCD? → Configure msDS-AllowedToActOnBehalf
│
├── Path via GPO?
│   ├── GenericWrite on GPO? → Add scheduled task
│   └── GpLink control? → Link malicious GPO to OU
│
└── Path via session?
    ├── Admin on computer with DA session?
    ├── Dump LSASS for DA credentials
    └── Or steal token/ticket
```

## BloodHound Edge Reference

| Edge Type | Meaning | Abuse Method |
|---|---|---|
| MemberOf | Group membership | Inherit group permissions |
| AdminTo | Local admin rights | PsExec, WMI, WinRM |
| HasSession | User logged in | Credential theft |
| GenericAll | Full control | Reset password, modify object |
| GenericWrite | Write properties | Set SPN, modify attributes |
| WriteDacl | Modify permissions | Grant self full control |
| WriteOwner | Change owner | Take ownership then WriteDacl |
| ForceChangePassword | Reset password | Change user password |
| AddMember | Add to group | Add self to privileged group |
| AllowedToDelegate | Constrained delegation | S4U2Proxy abuse |
| AllowedToAct | RBCD | Resource-based constrained delegation |
| CanRDP | RDP access | Remote desktop connection |
| CanPSRemote | WinRM access | PowerShell remoting |
| ExecuteDCOM | DCOM execution | Remote code execution |
| GPLink | GPO linked to OU | Modify GPO for code execution |

---

## Working Template

## Engagement Details

| Field | Value |
|---|---|
| Engagement ID | [ID] |
| Domain | [domain.local] |
| Collection Date | YYYY-MM-DD |
| Collector | SharpHound v2.x |
| Analyst | [Name] |

## Domain Statistics

| Metric | Count |
|---|---|
| Users | XXX |
| Enabled Users | XXX |
| Computers | XXX |
| Groups | XXX |
| Domain Admins | XX |
| OUs | XX |
| GPOs | XX |
| Trusts | XX |

## High-Risk Findings Summary

| # | Finding | Severity | Count | MITRE |
|---|---|---|---|---|
| 1 | Kerberoastable Accounts | Critical | XX | T1558.003 |
| 2 | Unconstrained Delegation (non-DC) | Critical | XX | T1558.001 |
| 3 | AS-REP Roastable Accounts | High | XX | T1558.004 |
| 4 | Constrained Delegation Abuse | High | XX | T1550.003 |
| 5 | Excessive ACL Permissions | High | XX | T1484 |
| 6 | Domain Users = Local Admin | High | XX | T1078.002 |
| 7 | Stale Admin Sessions | Medium | XX | T1550.002 |

## Attack Paths Identified

### Path 1: Kerberoasting to Domain Admin

```
[Owned User]
  -> Kerberoast SVC_SQL@CORP.LOCAL (T1558.003)
  -> Crack hash offline (hashcat -m 13100)
  -> SVC_SQL AdminTo SQL01 (T1078.002)
  -> SQL01 HasSession DA_ADMIN (T1033)
  -> Dump LSASS on SQL01 (T1003.001)
  -> Domain Admin achieved
```

**Feasibility:** High - Service account uses weak password
**Detection Risk:** Low - Kerberoasting generates minimal logs by default

### Path 2: ACL Abuse Chain

```
[Owned User]
  -> GenericAll on HELPDESK_ADMIN (T1484)
  -> ForceChangePassword on HELPDESK_ADMIN
  -> HELPDESK_ADMIN MemberOf IT_ADMINS
  -> IT_ADMINS AdminTo DC01
  -> Domain Admin achieved
```

**Feasibility:** Medium - Requires interaction with target account
**Detection Risk:** Medium - Password reset generates Event ID 4724

### Path 3: Delegation Abuse

```
[Owned User]
  -> AdminTo WEB01 (unconstrained delegation)
  -> Deploy Rubeus monitor on WEB01
  -> Coerce DC01 auth via PetitPotam (T1187)
  -> Capture DC01$ TGT
  -> Pass the Ticket to DC01 (T1550.003)
  -> DCSync (T1003.006)
  -> Domain Admin achieved
```

**Feasibility:** High - Unconstrained delegation on non-DC
**Detection Risk:** High - PetitPotam coercion may trigger alerts

## Kerberoastable Accounts

| Account | SPN | Privileged | Password Age | Risk |
|---|---|---|---|---|
| SVC_SQL@CORP.LOCAL | MSSQLSvc/SQL01:1433 | Yes (AdminCount) | 365 days | Critical |
| SVC_WEB@CORP.LOCAL | HTTP/WEB01 | No | 180 days | High |
| SVC_BACKUP@CORP.LOCAL | HOST/BACKUP01 | Yes (Backup Ops) | 730 days | Critical |

## Unconstrained Delegation

| Computer | OS | Domain Controller | Risk |
|---|---|---|---|
| WEB01.CORP.LOCAL | Server 2019 | No | Critical |
| PRINT01.CORP.LOCAL | Server 2016 | No | Critical |

## ACL Misconfigurations

| Source | Edge | Target | Risk |
|---|---|---|---|
| HELPDESK@CORP.LOCAL | GenericAll | IT_ADMINS@CORP.LOCAL | High |
| SVC_DEPLOY@CORP.LOCAL | WriteDACL | SERVER_ADMINS@CORP.LOCAL | High |
| HR_USERS@CORP.LOCAL | AddMember | VPN_USERS@CORP.LOCAL | Medium |

## Remediation Priorities

### Immediate (0-7 days)
1. Remove unconstrained delegation from WEB01, PRINT01
2. Reset passwords on Kerberoastable privileged accounts (25+ chars)
3. Remove GenericAll permission from HELPDESK on IT_ADMINS

### Short-Term (7-30 days)
1. Migrate service accounts to Group Managed Service Accounts (gMSA)
2. Enable AES-only Kerberos encryption for service accounts
3. Add privileged accounts to Protected Users group
4. Implement LAPS for local administrator passwords

### Long-Term (30-90 days)
1. Implement Active Directory Tier Model
2. Deploy Privileged Access Workstations (PAWs)
3. Enable Advanced Audit Policy for Kerberos events
4. Conduct quarterly BloodHound assessments
