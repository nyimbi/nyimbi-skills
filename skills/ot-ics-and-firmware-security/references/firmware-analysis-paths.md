# Firmware Analysis Paths

Purpose: pick the right firmware analysis path from the inputs you have —
a vendor image, a dumped image, a live device, or a suspect boot chain — and
know what each path can and cannot prove.

## Path selection

| You have | Question | Path | Technique files |
|---|---|---|---|
| Vendor firmware file (`.bin`, `.img`, `.rom`) | What's inside; embedded secrets? | Extract → enumerate → search | [performing-firmware-extraction-with-binwalk](performing-firmware-extraction-with-binwalk.md) |
| Extracted filesystem | Hardcoded credentials, config, keys? | String/entropy/config sweep | [performing-firmware-extraction-with-binwalk](performing-firmware-extraction-with-binwalk.md) |
| PLC/controller firmware image | Backdoors, weak update mechanisms, debug interfaces? | Platform-specific static review + baseline diff | [performing-plc-firmware-security-analysis](performing-plc-firmware-security-analysis.md) |
| Live PC/UEFI machine | Is platform firmware properly locked down? | CHIPSEC platform audit | [auditing-uefi-firmware-with-chipsec](auditing-uefi-firmware-with-chipsec.md) |
| Machine suspected compromised at boot | Is there a bootkit or implanted firmware? | ESP forensics → bootkit persistence analysis | [hunting-bootkits-in-efi-system-partition](hunting-bootkits-in-efi-system-partition.md), [analyzing-uefi-bootkit-persistence](analyzing-uefi-bootkit-persistence.md) |
| Boot behavior question (BlackLotus-class) | Is Secure Boot actually enforcing? | DBX / bypass-binary detection | [detecting-secure-boot-bypass](detecting-secure-boot-bypass.md) |
| Need measured-boot proof | Can we attest the boot chain from hardware? | TPM PCR attestation | [validating-tpm-measured-boot-attestation](validating-tpm-measured-boot-attestation.md) |

## Standard static path (vendor image)

1. **Record provenance** — source URL/vendor, exact SHA-256, acquisition date.
   Everything downstream is only credible if the artifact is pinned.
2. **Binwalk scan** — `binwalk` for signatures, entropy plot first: high
   entropy regions are compressed or encrypted (expect filesystems), flat
   regions are plaintext or padding.
3. **Recursive extraction** — `-e` for squashfs/cramfs/jffs2/ubi and nested
   archives; mount extracted images read-only where possible.
4. **Strings and config sweep** — credentials (`root:`, `password=`, SSH
   keys), hardcoded API tokens, default certificates, busybox configuration,
   update endpoints and signature-check presence.
5. **Cross-check findings** — a credential string proves it is *in the image*;
   confirm account existence/usage before claiming "default password works".

Firmware extraction detail, including encrypted-image handling:
[performing-firmware-extraction-with-binwalk](performing-firmware-extraction-with-binwalk.md).

## PC/UEFI path (live machine)

1. **CHIPSEC audit** — SPI flash write protection, BIOS lock, SMM/SMRR,
   Secure Boot variable state, platform configuration vs baseline.
2. **ESP inventory** — mount the EFI System Partition, hash boot loaders,
   YARA-scan binaries, flag non-EFI files and unexpected loaders.
3. **Known-bootkit comparison** — check persistence patterns for BlackLotus,
   LoJax, MosaicRegressor, MoonBounce, CosmicStrand, ESPecter, Bootkitty.
4. **Secure Boot bypass check** — validate DBX contains known-vulnerable
   revocations; detect bypass binaries and unsigned/downlevel load paths.
5. **Attestation** — if TPM available, extend to measured-boot attestation:
   compare quoted PCRs against known-good measurements.

## What each path can prove

| Evidence | Proves | Does not prove |
|---|---|---|
| Strings hit in extracted image | The value exists in shipped firmware | That the credential is active on a given device |
| CHIPSEC report | Current platform configuration state | Whether firmware was previously tampered with |
| ESP hash mismatch vs vendor baseline | This device's ESP differs from baseline | Which of the two images is malicious |
| DBX missing a revocation | Bootkit-class bypasses are possible here | That a bootkit is present |
| TPM PCR quote matches golden | This boot chain measured as expected | Post-boot runtime integrity |

## Safety note

All firmware paths are lab/offline by default. Dumping SPI flash from a
running production machine requires change control; flashing anything back to
a device that controls a physical process follows the safety gate in
[ot-safety](ot-safety.md) and is lab-only unless a vendor procedure says
otherwise.
