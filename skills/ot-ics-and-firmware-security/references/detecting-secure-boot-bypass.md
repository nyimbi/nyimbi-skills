# Detecting Secure Boot Bypass

## API Reference

## mokutil (Linux Secure Boot state)

| Command | Description |
|---------|-------------|
| `mokutil --sb-state` | Report whether Secure Boot is enabled. |
| `mokutil --list-enrolled` | List enrolled MOK (Machine Owner Keys). |
| `mokutil --db` | Show platform db entries (via shim). |
| `mokutil --dbx` | Show dbx (revoked) entries via shim. |

## efitools

| Command | Description |
|---------|-------------|
| `efi-readvar` | Dump PK, KEK, db, dbx. |
| `efi-readvar -v dbx -o dbx.esl` | Export dbx to an EFI signature list file. |

## dbxtool

| Command | Description |
|---------|-------------|
| `dbxtool --list` | List current dbx entries and count. |
| `dbxtool --dbx DBXUpdate.bin --apply --dry-run` | Show revocations a given update would add (no write). |
| `dbxtool --dbx DBXUpdate.bin --apply` | Apply a dbx update (write — caution). |

## CHIPSEC

| Command | Description |
|---------|-------------|
| `chipsec_main -m common.secureboot.variables` | Verify SB key variables are authenticated/protected. |
| `chipsec_main -m common.secureboot.variables -a modify` | Attempt to write/corrupt SB vars (destructive test). |
| `chipsec_main -m common.uefi.s3bootscript` | Check S3 resume boot-script protections. |
| `chipsec_util spi dump rom.bin` | Dump SPI flash for offline analysis. |

## Signature verification

| Command | Description |
|---------|-------------|
| `sbverify --list <file.efi>` | List signatures on an EFI binary. |
| `sbverify --cert db.crt <file.efi>` | Verify a binary against a db cert. |
| `pesign -S -i <file.efi>` | Show signatures (RHEL family). |

## Windows PowerShell

| Cmdlet | Description |
|--------|-------------|
| `Confirm-SecureBootUEFI` | Returns `$true` if Secure Boot is enabled. |
| `Get-SecureBootUEFI dbx` | Retrieve the raw dbx variable bytes. |
| `Get-SecureBootUEFI db` | Retrieve the allowed-signatures database. |

## TPM corroboration

| Command | Description |
|---------|-------------|
| `tpm2_pcrread sha256:7` | Read PCR[7] (Secure Boot policy measurement). |

## Key references

- UEFI revocation list files: https://uefi.org/revocationlistfile
- Microsoft KB5025885 (CVE-2023-24932): https://support.microsoft.com/topic/kb5025885

---

## Standards and Controls

## MITRE ATT&CK

| ID | Name | Rationale |
|----|------|-----------|
| T1542.003 | Pre-OS Boot: Bootkit | Core technique — bootkit subverts the boot chain below the OS to persist. |
| T1542 | Pre-OS Boot | Parent technique for firmware/boot-component tampering. |
| T1542.001 | Pre-OS Boot: System Firmware | Firmware modification used to weaken or bypass Secure Boot. |
| T1014 | Rootkit | Bootkits deliver rootkit-level stealth and persistence. |
| T1562.001 | Impair Defenses: Disable or Modify Tools | Post-bypass, BlackLotus disables BitLocker/HVCI/Defender. |

## NIST Cybersecurity Framework 2.0

| ID | Name | Rationale |
|----|------|-----------|
| DE.CM-01 | Networks and network services are monitored to find potentially adverse events | Applied here to boot-chain/firmware integrity monitoring — verifying Secure Boot, dbx, and EFI binaries surfaces tampering. |

## Supporting Standards and References

- **CVE-2022-21894 (Baton Drop).** Vulnerable signed Windows boot manager abused by BlackLotus to bypass Secure Boot.
- **CVE-2023-24932.** Secure Boot Security Feature Bypass; remediated via phased dbx revocation rollout (Microsoft KB5025885).
- **NSA UEFI Secure Boot Customization guidance.** Hardening and verification of the UEFI Secure Boot trust chain.
- **NIST SP 800-147 / 800-193 — Platform Firmware Resiliency.** Protection, detection, and recovery requirements for firmware integrity.
- **UEFI Specification — Secure Boot (db/dbx/KEK/PK).** Authoritative source for the variable model checked in this skill.
