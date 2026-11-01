# Validating Tpm Measured Boot Attestation

## API Reference

## Discovery
| Command | Description |
|---------|-------------|
| `tpm2_getcap properties-fixed` | TPM manufacturer / fixed properties. |
| `tpm2_getcap pcrs` | Supported PCR banks (sha1, sha256, ...). |
| `tpm2_pcrread sha256` | Read all sha256 PCRs. |
| `tpm2_pcrread sha256:0,7` | Read specific PCRs (here firmware + Secure Boot policy). |

## Event log
| Command | Description |
|---------|-------------|
| `tpm2_eventlog /sys/kernel/security/tpm0/binary_bios_measurements` | Parse + replay the firmware event log; output includes calculated PCRs. |

## Attestation key
| Command | Description |
|---------|-------------|
| `tpm2_createprimary -C e -g sha256 -G rsa -c primary.ctx` | Create an endorsement-hierarchy primary key. |
| `tpm2_create -C primary.ctx -G rsa -u ak.pub -r ak.priv -a 'fixedtpm\|fixedparent\|sensitivedataorigin\|userwithauth\|restricted\|sign'` | Create a restricted signing AK. |
| `tpm2_load -C primary.ctx -u ak.pub -r ak.priv -c ak.ctx` | Load the AK into the TPM. |
| `tpm2_readpublic -c ak.ctx -o ak.pem -f pem` | Export the AK public key (PEM) for the verifier. |

## Quote / verify
| Command | Description |
|---------|-------------|
| `tpm2_quote -c ak.ctx -l sha256:0,1,...,9 -q <nonce> -m quote.msg -s quote.sig -o quote.pcrs -g sha256` | Produce a nonce-bound signed quote. |
| `tpm2_checkquote -u ak.pem -m quote.msg -s quote.sig -f quote.pcrs -q <nonce> -g sha256` | Verify signature, nonce, and PCR digest (verifier side). |

## Sealing to PCR policy
| Command | Description |
|---------|-------------|
| `tpm2_createpolicy --policy-pcr -l sha256:7 -L pcr7.policy -f pcr7.dat` | Build a PCR-bound auth policy. |
| `tpm2_create -C primary.ctx -L pcr7.policy -i - -u sealed.pub -r sealed.priv` | Seal a secret to the policy. |
| `tpm2_unseal -c sealed.ctx -p pcr:sha256:7` | Release the secret only if PCRs match. |

## IMA (PCR 10)
| Command | Description |
|---------|-------------|
| `tpm2_pcrread sha256:10` | Read the IMA aggregate PCR. |
| `cat /sys/kernel/security/ima/ascii_runtime_measurements` | View the IMA runtime measurement list. |

## TCG PCR index meanings (PC Client profile)
| PCR | Measures |
|-----|----------|
| 0 | UEFI firmware code (CRTM, boot block). |
| 1 | UEFI firmware configuration / host platform config. |
| 2–3 | Option ROM code and config. |
| 4 | Boot manager / MBR code. |
| 5 | Boot manager config / GPT. |
| 6 | Platform-specific events. |
| 7 | Secure Boot policy (PK/KEK/db/dbx state). |
| 8–9 | Bootloader-measured kernel/initrd. |
| 10 | Linux IMA runtime measurements. |

---

## Standards and Controls

## MITRE ATT&CK

| ID | Name | Rationale |
|----|------|-----------|
| T1542 | Pre-OS Boot | Measured boot detects the pre-OS tampering this technique relies on. |
| T1542.001 | Pre-OS Boot: System Firmware | PCR 0–7 drift reveals unauthorized firmware modification. |
| T1542.003 | Pre-OS Boot: Bootkit | Bootloader/kernel measurements (PCR 8–10) expose bootkit changes. |
| T1014 | Rootkit | Quote verification and IMA measurements surface concealed tampering. |
| T1601.001 | Modify System Image: Patch System Image | Attestation against golden values flags unauthorized image patches. |

## NIST Cybersecurity Framework 2.0

| ID | Name | Rationale |
|----|------|-----------|
| PR.PS-01 | Configuration management practices are established and applied | Measured-boot baselining and attestation enforce and verify the approved firmware/kernel configuration of platforms. |

## Supporting Standards and References

- **TCG TPM 2.0 Library Specification.** Defines PCRs, extend semantics, quotes, and attestation keys.
- **TCG PC Client Platform Firmware Profile.** Assigns PCR index meanings (PCR 0–7 firmware, PCR 7 Secure Boot, PCR 8–10 OS/IMA).
- **RFC 9683 — Remote Integrity Verification of Network Devices Containing TPMs.** Standardizes TPM-based remote attestation.
- **NIST SP 800-155 — BIOS Integrity Measurement Guidelines.** Measured-boot and integrity reporting guidance.
- **NSA UEFI/Boot Security guidance.** Recommends measured boot + attestation alongside Secure Boot.
