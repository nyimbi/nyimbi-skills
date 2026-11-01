# Auditing Uefi Firmware With Chipsec

## API Reference

## chipsec_main (test suite)

| Command / Flag | Purpose |
|----------------|---------|
| `chipsec_main` | Run all applicable security modules for the platform |
| `-m, --module <name>` | Run a specific module, e.g. `-m common.bios_wp` |
| `-m common` | Run the whole OEM-independent module group |
| `-mx <modules>` | Exclude listed modules |
| `-a, --module_args` | Pass arguments to a module (e.g. `-a modify`) |
| `-p, --platform <code>` | Force platform code when auto-detect fails |
| `-n, --no_driver` | Skip checks requiring the kernel driver |
| `-l, --log <file>` | Write output to a log file |
| `-j, --json <file>` | JSON results output |
| `-x, --xml <file>` | JUnit-style XML results output |
| `-v / -vv / -d` | Verbose / very verbose / debug logging |

## Key security modules

| Module | Checks |
|--------|--------|
| `common.bios_wp` | BIOS_CNTL BLE / SMM_BWP and SPI Protected Ranges |
| `common.spi_lock` | SPI flash descriptor FLOCKDN lock |
| `common.spi_access` | SPI flash region access permissions |
| `common.smrr` | SMRR programming (SMRAM cache protection) |
| `common.smm` | SMM BIOS write protection |
| `common.secureboot.variables` | Secure Boot variable protection (`-a modify` to test writes) |
| `common.uefi.s3bootscript` | S3 resume boot-script protection |

## chipsec_util (manual access)

| Command | Purpose |
|---------|---------|
| `chipsec_util spi info` | Report SPI flash regions/descriptor/permissions |
| `chipsec_util spi dump rom.bin` | Dump entire SPI flash to file |
| `chipsec_util spi read <addr> <len> out.bin` | Read SPI flash range |
| `chipsec_util decode rom.bin` | Decode dumped image into volumes/files/variables |
| `chipsec_util uefi var-list` | List UEFI variables (runtime) |
| `chipsec_util uefi var-find <name>` | Find a UEFI variable |
| `chipsec_util uefi var-read <name> <GUID> out.bin` | Read a variable |
| `chipsec_util uefi decode rom.bin` | Decode UEFI firmware structure from image |
| `chipsec_util platform` | Show detected platform info |

## Result interpretation

| Result | Meaning |
|--------|---------|
| PASSED | Protection is correctly enabled |
| FAILED | Protection missing/misconfigured — exploitable |
| WARNING | Potential issue / needs manual review |
| INFORMATION | Informational, no pass/fail |

---

## Standards and Controls

## MITRE ATT&CK

| Technique ID | Name | Tactic | Rationale |
|--------------|------|--------|-----------|
| T1542.001 | Pre-OS Boot: System Firmware | Persistence / Defense Evasion | CHIPSEC verifies the SPI flash and BIOS write-protection locks whose absence enables adversaries to modify system firmware for stealthy, OS-survivable persistence. |

## NIST Cybersecurity Framework 2.0

| ID | Name | Rationale |
|----|------|-----------|
| ID.AM-02 | Inventories of software, services, and systems managed by the organization are maintained | Firmware version, SPI flash image, and platform-security configuration are part of the asset/software inventory that CHIPSEC enumerates and baselines. |

## Official Resources

- CHIPSEC project: https://github.com/chipsec/chipsec
- CHIPSEC documentation: https://chipsec.github.io/
- Running CHIPSEC: https://chipsec.github.io/usage/Running-Chipsec.html
- common.bios_wp module: https://chipsec.github.io/modules/
- common.secureboot.variables module docs
- UEFITool: https://github.com/LongSoft/UEFITool
- Binarly fwhunt-scan: https://github.com/binarly-io/fwhunt-scan

## Key Research

- Intel ATR: original CHIPSEC framework and BlackHat arsenal presentations
- "Exploring Your System Deeper with CHIPSEC" (CSW)
- NSA UEFI Secure Boot Customization / firmware hardening guidance
