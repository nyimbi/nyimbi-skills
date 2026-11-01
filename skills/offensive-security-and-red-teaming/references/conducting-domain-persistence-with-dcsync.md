# Conducting Domain Persistence With Dcsync

## API Reference

## Libraries

| Library | Install | Purpose |
|---------|---------|---------|
| ldap3 | `pip install ldap3` | LDAP directory queries for AD permission enumeration |
| impacket | `pip install impacket` | Network protocol toolkit — secretsdump.py for DCSync |
| pyad | `pip install pyad` | Windows Active Directory interface |

## Key ldap3 Methods

| Method | Description |
|--------|-------------|
| `Server(ip, get_info=ALL)` | Create LDAP server connection object |
| `Connection(server, user, password, authentication=NTLM)` | Bind to AD with NTLM auth |
| `conn.search(search_base, search_filter, attributes)` | Query directory objects |
| `conn.entries` | Access search result entries |
| `conn.unbind()` | Close LDAP connection |

## Critical GUIDs for DCSync Detection

| GUID | Right |
|------|-------|
| `1131f6aa-9c07-11d1-f79f-00c04fc2dcd2` | DS-Replication-Get-Changes |
| `1131f6ad-9c07-11d1-f79f-00c04fc2dcd2` | DS-Replication-Get-Changes-All |
| `89e95b76-444d-4c62-991a-0facbeda640c` | DS-Replication-Get-Changes-In-Filtered-Set |

## Windows Event IDs

| Event ID | Description |
|----------|-------------|
| 4662 | Directory service object accessed (replication GUIDs indicate DCSync) |
| 4624 | Logon event — correlate with replication activity from non-DC source |

## MITRE ATT&CK Mapping

| Technique | ID |
|-----------|----|
| OS Credential Dumping: DCSync | T1003.006 |

## External References

- [impacket secretsdump.py](https://github.com/fortra/impacket/blob/master/examples/secretsdump.py)
- [ldap3 Documentation](https://ldap3.readthedocs.io/)
- [Microsoft DCSync Detection](https://learn.microsoft.com/en-us/defender-for-identity/credential-access-alerts)

---

## Standards and Controls

## MITRE ATT&CK References

| Technique ID | Name | Tactic |
|-------------|------|--------|
| T1003.006 | OS Credential Dumping: DCSync | Credential Access |
| T1558.001 | Steal or Forge Kerberos Tickets: Golden Ticket | Credential Access |
| T1222.001 | File and Directory Permissions Modification | Defense Evasion |
| T1098 | Account Manipulation | Persistence |
| T1078.002 | Valid Accounts: Domain Accounts | Persistence |

## Key Research

- MITRE ATT&CK T1003.006: https://attack.mitre.org/techniques/T1003/006/
- Netwrix: DCSync Attack Using Mimikatz Detection
- JumpCloud: What Is DCSync? Critical AD Attack Explained
- The Hacker Recipes: DCSync technique documentation
- Atomic Red Team T1003.006 test procedures

## Threat Actor Usage

- APT28 (Fancy Bear) - DCSync for credential harvesting
- APT29 (Cozy Bear) - SolarWinds campaign used DCSync
- FIN6 - Financial cybercrime group
- Wizard Spider - Ryuk ransomware campaigns

---

## Workflows

## DCSync Attack Chain

```
1. Prerequisites
   ├── Domain Admin or account with replication rights
   ├── Network access to Domain Controller (TCP/135, dynamic RPC)
   └── Tool: Mimikatz (Windows) or secretsdump.py (Linux)

2. Credential Extraction
   ├── Extract KRBTGT hash (Golden Ticket capability)
   ├── Extract Administrator hash (immediate DA access)
   ├── Extract all domain hashes (comprehensive dump)
   └── Extract service account hashes (lateral movement)

3. Golden Ticket Persistence
   ├── Forge Golden Ticket with KRBTGT hash
   ├── Set arbitrary user, SID, and group memberships
   ├── Import ticket into current session
   └── Access any resource in the domain

4. DCSync Rights Persistence
   ├── Create low-profile account in AD
   ├── Grant DS-Replication-Get-Changes-All rights
   ├── Verify rights with ACL enumeration
   └── Account can now perform DCSync independently
```

## Golden Ticket Lifecycle

```
Creation: KRBTGT hash + Domain SID → Golden Ticket (10-year validity)
Usage: Import ticket → Access any service in domain
Survival: Persists through password resets (except double KRBTGT reset)
Detection: Anomalous TGT lifetime, non-existent users, impossible SIDs
Cleanup: Double KRBTGT password reset (with 10+ hour gap between resets)
```

---

## Working Template

## Target Domain

| Field | Value |
|-------|-------|
| Domain | |
| Domain SID | |
| DC Target | |
| Attack Source Account | |
| Tool Used | Mimikatz / secretsdump.py |

## Extracted Credentials

| Account | Type | NT Hash | Cleartext | Persistence Value |
|---------|------|---------|-----------|-------------------|
| krbtgt | Service | | No | Golden Ticket |
| Administrator | DA | | No | Direct DA access |

## Persistence Mechanisms

| Mechanism | Status | Details |
|-----------|--------|---------|
| Golden Ticket | Created / Not Created | |
| DCSync Rights Granted | Yes / No | Account: |
| Silver Tickets | Created / Not Created | Services: |

## Remediation

| Action | Priority |
|--------|----------|
| Double KRBTGT password reset (with 10h gap) | Critical |
| Audit accounts with replication rights | Critical |
| Enable Event 4662 logging for replication GUIDs | High |
| Deploy DRSUAPI traffic monitoring | High |
