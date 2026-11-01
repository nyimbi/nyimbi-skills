# Active Directory Attack-Path Selection

Purpose: choose the AD technique that matches the precondition you actually
have, instead of running the full toolchain and hoping. Tool flags and command
detail live in the linked per-technique files.

## Precondition → technique

| You have | Target condition | Technique | Tooling | Detail |
|---|---|---|---|---|
| Any domain user | Accounts with SPNs and weak passwords | Kerberoasting | Impacket `GetUserSPNs`, Rubeus, hashcat `-m 13100` | [exploiting-kerberoasting-with-impacket](exploiting-kerberoasting-with-impacket.md) |
| Any domain user | Accounts without Kerberos pre-auth | AS-REP roasting | Impacket `GetNPUsers`, hashcat `-m 18200` | [performing-kerberoasting-attack](performing-kerberoasting-attack.md) |
| Any domain user | Reachable NTLM service without signing | NTLM relay | `ntlmrelayx`; targets include SMB, LDAP, ADCS web enrollment | [relaying-ntlm-for-adcs-esc8](relaying-ntlm-for-adcs-esc8.md) |
| Any domain user, relay ready | No natural authentication to relay | Auth coercion (MS-EFSR, MS-RPRN, MS-DFSNM, MS-FSRVP) | PetitPotam, Coercer | [coercing-authentication-with-coercer-petitpotam](coercing-authentication-with-coercer-petitpotam.md) |
| Any domain user | Vulnerable certificate template / CA flags | ADCS abuse (ESC1–ESC16, golden certificates) | Certipy `find`/`req`/`relay`/`shadow` | [exploiting-adcs-with-certipy](exploiting-adcs-with-certipy.md) |
| Domain user | Computer with unconstrained delegation | TGT capture from memory; force DC authentication | PrinterBug/SpoolSample + memory dumping | [performing-active-directory-penetration-test](performing-active-directory-penetration-test.md) |
| Domain user | Constrained delegation configured | S4U2self/S4U2proxy impersonation | Impacket `getST`, Rubeus | [exploiting-constrained-delegation-abuse](exploiting-constrained-delegation-abuse.md) |
| Low-priv user | Write access to a target's `msDS-KeyCredentialLink` | Shadow Credentials → PKINIT auth | pyWhisker, Whisker, Certipy | [abusing-shadow-credentials-for-privesc](abusing-shadow-credentials-for-privesc.md) |
| Stolen TGT or TGS | Ticket in hand, no password | Pass-the-ticket | Impacket `psexec`/`wmiexec` with `-k`, Rubeus | [conducting-pass-the-ticket-attack](conducting-pass-the-ticket-attack.md) |
| Any domain user | No privileged precondition — need the map first | Attack-path discovery | BloodHound CE (SharpHound/AzureHound collection + Cypher) | [mapping-attack-paths-with-bloodhound-ce](mapping-attack-paths-with-bloodhound-ce.md) |
| Replication rights (or path to them) | Domain dominance / persistence | DCSync → KRBTGT extraction → golden ticket | Impacket `secretsdump`, `ticketer`, Mimikatz | [conducting-domain-persistence-with-dcsync](conducting-domain-persistence-with-dcsync.md) |
| Local admin on one host | Next hop or better credentials | Lateral movement (SMB/WinRM/WMI/MSSQL) | NetExec, Impacket `wmiexec`, evil-winrm | [moving-laterally-with-netexec](moving-laterally-with-netexec.md) |
| Credentialed domain user | Forest trust boundary | Trust key extraction, SID history, cross-realm tickets | Impacket | [performing-active-directory-forest-trust-attack](performing-active-directory-forest-trust-attack.md) |
| Compromised Windows endpoint | Stored secrets in user context | DPAPI / browser / vault extraction | Mimikatz, LaZagne | [abusing-dpapi-for-credential-access](abusing-dpapi-for-credential-access.md) |

## Ordering rules

1. **Map before you move.** Run BloodHound collection first; a five-minute
   Cypher query routinely beats three hours of spraying. Mark owned principals
   and re-run shortest-path queries after each new credential.
2. **Coercion before guessing.** When relay is viable, coerce authentication
   rather than spray — fewer failed-logon events, no lockout risk.
3. **Kerberos over NTLM where both work.** NTLM relay leaves noisy, well-signaled
   events; Kerberoasting and ticket use blend with normal traffic.
4. **Certificates over passwords at the end.** ESC1/ESC8 and shadow-credential
   paths produce durable access that survives password resets — document the
   issued certificates for cleanup.
5. **Stop at the objective.** Domain dominance is a means; extract only the
   proof required by the ROE and record (do not export) everything else.

## Cleanup obligations

Every technique above leaves artifacts: service tickets, issued certificates,
DCSync-ed hashes, added SPNs or `msDS-KeyCredentialLink` values, created
accounts, and relayed sessions. Record each one as it is created and reverse
it during the cleanup step of the engagement, verifying with a re-enumeration
pass.
