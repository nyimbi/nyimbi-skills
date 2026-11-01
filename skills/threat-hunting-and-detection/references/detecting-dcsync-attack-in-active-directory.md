# Detecting Dcsync Attack In Active Directory

## API Reference

## DCSync Replication GUIDs

| GUID | Right |
|------|-------|
| 1131f6aa-9c07-11d1-f79f-00c04fc2dcd2 | DS-Replication-Get-Changes |
| 1131f6ad-9c07-11d1-f79f-00c04fc2dcd2 | DS-Replication-Get-Changes-All |
| 89e95b76-444d-4c62-991a-0facbeda640c | DS-Replication-Get-Changes-In-Filtered-Set |

## Windows Event ID 4662 Fields

```xml
<EventID>4662</EventID>
<Data Name="SubjectUserName">attacker</Data>
<Data Name="SubjectDomainName">CORP</Data>
<Data Name="Properties">{1131f6ad-9c07-11d1-f79f-00c04fc2dcd2}</Data>
<Data Name="ObjectName">DC=corp,DC=local</Data>
```

## python-evtx Usage

```python
import Evtx.Evtx as evtx
with evtx.Evtx("Security.evtx") as log:
    for record in log.records():
        xml = record.xml()
        # Filter for EventID 4662 with replication GUIDs
```

## Splunk SPL Detection Query

```spl
index=wineventlog EventCode=4662
| where Properties IN ("*1131f6aa*", "*1131f6ad*", "*89e95b76*")
| where NOT match(SubjectUserName, ".*\\$$")
| stats count values(Properties) by SubjectUserName Computer
```

## KQL (Microsoft Sentinel)

```kql
SecurityEvent
| where EventID == 4662
| where Properties has "1131f6ad-9c07-11d1-f79f-00c04fc2dcd2"
| where SubjectUserName !endswith "$"
| project TimeGenerated, SubjectUserName, Computer, Properties
```

## PowerShell - Audit Replication Permissions

```powershell
$domain = (Get-ADDomain).DistinguishedName
$acl = Get-Acl "AD:\$domain"
$acl.Access | Where-Object {
    $_.ObjectType -in @(
        '1131f6aa-9c07-11d1-f79f-00c04fc2dcd2',
        '1131f6ad-9c07-11d1-f79f-00c04fc2dcd2'
    )
} | Select IdentityReference, ObjectType
```

## Attack Tools Reference

| Tool | Command |
|------|---------|
| Mimikatz | `lsadump::dcsync /user:krbtgt /domain:corp.local` |
| Impacket | `secretsdump.py corp/admin:pass@dc-ip` |
| DSInternals | `Get-ADReplAccount -SamAccountName krbtgt` |

## CLI Usage

```bash
python agent.py --security-log Security.evtx --dc-accounts known_dcs.txt
python agent.py --generate-sigma
python agent.py --check-perms
```

---

## Standards and Controls

## MITRE ATT&CK Credential Access (TA0006)

| Technique | Name | Relevance |
|-----------|------|-----------|
| T1003.006 | OS Credential Dumping: DCSync | Primary technique |
| T1003.001 | LSASS Memory | Often combined with DCSync for complete credential theft |
| T1003.003 | NTDS | Alternative to DCSync using ntdsutil or volume shadow copy |
| T1078.002 | Valid Accounts: Domain Accounts | Using dumped credentials |
| T1558.001 | Steal or Forge Kerberos Tickets: Golden Ticket | Primary goal of KRBTGT hash extraction |
| T1222.001 | File and Directory Permissions Modification | Granting replication rights |

## Critical Replication GUIDs

| GUID | Permission Name | Risk |
|------|----------------|------|
| 1131f6aa-9c07-11d1-f79f-00c04fc2dcd2 | DS-Replication-Get-Changes | Required for DCSync |
| 1131f6ad-9c07-11d1-f79f-00c04fc2dcd2 | DS-Replication-Get-Changes-All | Includes confidential attributes (passwords) |
| 89e95b76-444d-4c62-991a-0facbeda640c | DS-Replication-Get-Changes-In-Filtered-Set | Partial replication rights |

## Windows Event IDs for DCSync Detection

| Event ID | Source | Description |
|----------|--------|-------------|
| 4662 | Security | Directory Service Object Access (primary detection) |
| 4624 | Security | Successful logon (correlate source of replication) |
| 4672 | Security | Special privileges assigned (admin logon) |
| 4738 | Security | User account changed (permission grants) |
| 5136 | Security | Directory Service Object modified (ACL changes) |

## Known Threat Actors Using DCSync

| Actor | Context |
|-------|---------|
| APT29 (Cozy Bear) | Used DCSync in SolarWinds campaign |
| FIN6 | DCSync for credential harvesting in retail/hospitality |
| Wizard Spider | TrickBot/Conti ransomware using DCSync pre-encryption |
| APT28 (Fancy Bear) | DCSync in government network intrusions |
| LAPSUS$ | DCSync after AD compromise for data theft |

## Legitimate Replication Sources

| Source | Reason | How to Distinguish |
|--------|--------|--------------------|
| Domain Controllers | Normal AD replication | Computer account ends with $ |
| Azure AD Connect | Hybrid identity sync | MSOL_ service account |
| Backup Software | AD backup operations | Documented service accounts |
| Migration Tools | Cross-forest migrations | Temporary, documented operations |

---

## Workflows

## Phase 1: Enumerate Legitimate Replication Accounts

### Step 1.1 - List All Domain Controllers
```powershell
Get-ADDomainController -Filter * | Select-Object Name, IPv4Address, OperatingSystem
```

### Step 1.2 - Find Accounts with Replication Rights
```powershell
# Find all accounts with Replicating Directory Changes
Import-Module ActiveDirectory
$rootDSE = Get-ADRootDSE
$domainDN = $rootDSE.defaultNamingContext
$acl = Get-Acl "AD:\$domainDN"
$acl.Access | Where-Object {
    $_.ObjectType -eq "1131f6ad-9c07-11d1-f79f-00c04fc2dcd2" -or
    $_.ObjectType -eq "1131f6aa-9c07-11d1-f79f-00c04fc2dcd2"
} | Select-Object IdentityReference, ActiveDirectoryRights, ObjectType
```

### Step 1.3 - BloodHound Query for DCSync Rights
```cypher
MATCH p=(n)-[:GetChanges|GetChangesAll]->(d:Domain)
WHERE NOT n:Domain
RETURN n.name, labels(n)
```

## Phase 2: Deploy Detection

### Step 2.1 - Enable Required Audit Policy
```cmd
auditpol /set /subcategory:"Directory Service Access" /success:enable /failure:enable
```

### Step 2.2 - Configure SACL on Domain Object
Apply SACL to the domain root object monitoring for:
- Control Access rights
- Access to Replication GUIDs
- By Everyone or Authenticated Users

## Phase 3: Active Monitoring

### Step 3.1 - Splunk Real-Time Detection
```spl
index=wineventlog source="WinEventLog:Security" EventCode=4662
| rex field=Properties "(?<guid>\{[0-9a-f-]+\})"
| where guid IN ("{1131f6aa-9c07-11d1-f79f-00c04fc2dcd2}",
    "{1131f6ad-9c07-11d1-f79f-00c04fc2dcd2}",
    "{89e95b76-444d-4c62-991a-0facbeda640c}")
| lookup dc_accounts SubjectUserName OUTPUT is_dc
| where is_dc!="true"
| eval alert_severity="CRITICAL"
| table _time SubjectUserName SubjectDomainName Computer guid alert_severity
```

### Step 3.2 - Network-Level Detection
```spl
index=zeek sourcetype=dce_rpc
| where operation="DRSGetNCChanges"
| lookup domain_controllers src_ip OUTPUT is_dc
| where is_dc!="true"
| table _time src_ip dst_ip operation
```

## Phase 4: Investigation

### Step 4.1 - Determine Source Machine
Correlate Event 4662 with Event 4624 to identify the source workstation:
```spl
index=wineventlog EventCode=4624 LogonType=3
| where TargetUserName=[suspected_account]
| table _time TargetUserName IpAddress WorkstationName LogonType
```

### Step 4.2 - Check for Subsequent Credential Abuse
```spl
index=wineventlog EventCode=4769
| where ServiceName="krbtgt"
| where TicketEncryptionType="0x17"
| table _time TargetUserName ServiceName IpAddress TicketEncryptionType
```

## Phase 5: Response

### Step 5.1 - Immediate Containment
1. Disable compromised account immediately
2. Rotate KRBTGT password (twice, 12 hours apart)
3. Reset all service account passwords
4. Block source IP at network level
5. Isolate source machine for forensics

### Step 5.2 - Remediation
1. Remove unauthorized replication rights
2. Review all accounts with DCSync-capable permissions
3. Implement tiered administration model
4. Enable Microsoft Defender for Identity DCSync alerts
5. Deploy Protected Users security group for admin accounts

---

## Working Template

## Hunt Metadata
| Field | Value |
|-------|-------|
| Hunt ID | TH-DCSYNC-YYYY-MM-DD-NNN |
| Analyst | |
| Date | |
| Status | [ ] In Progress / [ ] Complete |

## Hypothesis
> An adversary with elevated AD privileges is performing DCSync to extract password hashes from Active Directory by replicating directory data from a non-domain-controller machine.

## Pre-Hunt Checklist
- [ ] Event ID 4662 audit policy enabled on all DCs
- [ ] SACL configured on domain root object
- [ ] Domain controller inventory documented
- [ ] Known service accounts with replication rights documented
- [ ] Azure AD Connect accounts identified (if hybrid)

## DCSync Detection Findings

| # | Timestamp | Subject Account | Source Machine | Target DC | Replication Rights | Severity |
|---|-----------|-----------------|----------------|-----------|-------------------|----------|
| 1 | | | | | | |

## Accounts with Replication Rights Audit

| Account | Type | Rights | Legitimate | Justification |
|---------|------|--------|-----------|---------------|
| | User/Service/Computer | Get-Changes / Get-Changes-All | Yes/No | |

## Post-DCSync Impact Assessment

| Check | Status | Notes |
|-------|--------|-------|
| KRBTGT hash potentially compromised | | |
| Domain Admin hashes extracted | | |
| Service account credentials at risk | | |
| Golden Ticket creation possible | | |

## Response Actions
1. **Disable**: [Compromised accounts]
2. **Reset**: [KRBTGT password -- twice, 12 hours apart]
3. **Revoke**: [Unauthorized replication rights]
4. **Investigate**: [Source machine forensics]
5. **Monitor**: [Subsequent credential abuse attempts]
