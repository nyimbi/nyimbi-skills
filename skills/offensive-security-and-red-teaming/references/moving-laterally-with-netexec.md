# Moving Laterally With Netexec

## API Reference

## General Syntax

```
nxc [runtime options] <protocol> <target> [auth] [actions] [-M module] [-o KEY=val]
```

Supported protocols: `smb winrm mssql ldap ssh ftp wmi rdp vnc nfs`.

## Authentication Flags

| Flag | Description |
|------|-------------|
| `-u USER` | Username (or file of usernames) |
| `-p PASS` | Password (or file of passwords) |
| `-H HASH` | NT hash or `LM:NT` for pass-the-hash |
| `-d DOMAIN` | Target domain |
| `--local-auth` | Authenticate against the local SAM, not the domain |
| `-k` / `--use-kcache` | Kerberos auth using ccache (`KRB5CCNAME`) |
| `--continue-on-success` | Keep testing after a valid login (spraying) |
| `--no-bruteforce` | Pair user[i] with pass[i] instead of full matrix |

## SMB Actions

| Flag | Description |
|------|-------------|
| `--shares` | List accessible shares and permissions |
| `--users` / `--groups` | Enumerate domain users / groups |
| `--pass-pol` | Dump password / lockout policy |
| `--rid-brute [N]` | Enumerate accounts by RID cycling |
| `--loggedon-users` / `--sessions` | Show logged-on users / active sessions |
| `-x CMD` / `-X PS` | Execute shell / PowerShell command |
| `--exec-method M` | `smbexec`, `wmiexec`, `atexec`, `mmcexec` |
| `--sam` / `--lsa` | Dump SAM hashes / LSA secrets |
| `--ntds [vss\|drsuapi]` | Dump the domain NTDS.dit |
| `-M MODULE` | Run a module (e.g. `lsassy`, `spider_plus`) |

## LDAP Actions

| Flag | Description |
|------|-------------|
| `--kerberoasting FILE` | Request and save Kerberoastable hashes |
| `--asreproast FILE` | Request and save AS-REP roastable hashes |
| `--bloodhound --collection All` | Collect BloodHound data |
| `--trusted-for-delegation` | Find delegation-enabled accounts |
| `-M laps` | Read LAPS passwords |

## WinRM / MSSQL Actions

| Flag | Description |
|------|-------------|
| `winrm ... -X 'PScmd'` | Execute PowerShell over WinRM (5985/5986) |
| `mssql ... -q 'SQL'` | Run a SQL query |
| `mssql ... -x 'cmd'` | Execute OS command via xp_cmdshell |

## Modules and Workspace

```bash
nxc smb -L            # list SMB modules
nxc smb -M lsassy --options   # show module options
ls ~/.nxc/workspaces/         # SQLite result store
nxc smb <t> ... --log out.log # tee output to file
```

## External References

- NetExec Wiki: https://www.netexec.wiki/
- SMB protocol docs: https://www.netexec.wiki/smb-protocol/authentication
- Module list: https://www.netexec.wiki/

---

## Standards and Controls

## MITRE ATT&CK References

| Technique ID | Name | Tactic | Rationale |
|-------------|------|--------|-----------|
| T1021.002 | Remote Services: SMB/Windows Admin Shares | Lateral Movement | NetExec authenticates to `ADMIN$`/`C$` and runs code on remote hosts |
| T1110.003 | Brute Force: Password Spraying | Credential Access | `--continue-on-success` sprays one password across many accounts |
| T1003.002 | OS Credential Dumping: Security Account Manager | Credential Access | `--sam` extracts local account hashes |
| T1003.004 | OS Credential Dumping: LSA Secrets | Credential Access | `--lsa` extracts LSA secrets and cached domain creds |
| T1003.006 | OS Credential Dumping: DCSync | Credential Access | `--ntds` replicates the domain database via DRSUAPI |
| T1558.003 | Steal or Forge Kerberos Tickets: Kerberoasting | Credential Access | `ldap --kerberoasting` requests crackable service tickets |
| T1087.002 | Account Discovery: Domain Account | Discovery | `--users` / `--rid-brute` enumerate domain accounts |
| T1135 | Network Share Discovery | Discovery | `--shares` enumerates accessible SMB shares |

## NIST Cybersecurity Framework 2.0

| ID | Name | Rationale |
|----|------|-----------|
| DE.CM-01 | Networks and network services are monitored to find potentially adverse events | NetExec activity (mass auth, exec, dumping) is the adverse behavior defenders must detect; this skill informs detection coverage |

## Official Resources

- NetExec GitHub: https://github.com/Pennyw0rth/NetExec
- NetExec Wiki: https://www.netexec.wiki/
- Selecting a protocol: https://www.netexec.wiki/getting-started/selecting-and-using-a-protocol
- Impacket: https://github.com/fortra/impacket
- MITRE ATT&CK T1021.002: https://attack.mitre.org/techniques/T1021/002/

## Key Research

- Black Hills InfoSec: Getting Started with NetExec
- StationX: NetExec Cheat Sheet (2026 Guide)
- Vaadata: NetExec, the Tool for Auditing an Internal Network
