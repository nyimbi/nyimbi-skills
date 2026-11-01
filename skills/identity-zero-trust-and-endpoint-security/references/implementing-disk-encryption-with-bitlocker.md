# Implementing Disk Encryption With Bitlocker

## API Reference

## manage-bde CLI

```powershell
# Check status
manage-bde -status C:

# Enable BitLocker with TPM
manage-bde -on C: -RecoveryPassword -EncryptionMethod AES256

# Backup recovery key to AD
manage-bde -protectors -adbackup C: -ID {protector-id}

# Lock/unlock
manage-bde -lock D:
manage-bde -unlock D: -RecoveryPassword 123456-...
```

## PowerShell BitLocker Cmdlets

```powershell
# Get BitLocker volume
Get-BitLockerVolume -MountPoint "C:"

# Enable with TPM + PIN
Enable-BitLocker -MountPoint "C:" -EncryptionMethod Aes256 `
  -TpmAndPinProtector -Pin (ConvertTo-SecureString "1234" -AsPlainText -Force)

# Add recovery password
Add-BitLockerKeyProtector -MountPoint "C:" -RecoveryPasswordProtector

# Backup to AD
Backup-BitLockerKeyProtector -MountPoint "C:" -KeyProtectorId $id
```

## Compliance Checks

| Check | Severity | Requirement |
|-------|----------|-------------|
| BitLocker enabled | CRITICAL | All OS drives |
| AES-256 encryption | MEDIUM | FIPS/enterprise |
| TPM protector | HIGH | Hardware-backed |
| Recovery key escrowed | HIGH | AD DS or Azure AD |
| Full disk encrypted | MEDIUM | Not used-space only |

## Microsoft Graph API (Intune)

```python
import requests
headers = {"Authorization": "Bearer <token>"}
resp = requests.get(
    "https://graph.microsoft.com/v1.0/deviceManagement/managedDevices"
    "?$select=deviceName,isEncrypted",
    headers=headers)
```

### References

- BitLocker: https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/
- BitLocker PowerShell: https://learn.microsoft.com/en-us/powershell/module/bitlocker/

---

## Standards and Controls

## Primary Standards

### NIST SP 800-111 - Guide to Storage Encryption Technologies
- **Publisher**: NIST
- **URL**: https://csrc.nist.gov/publications/detail/sp/800-111/final
- **Scope**: Guidance on planning, implementing, and maintaining storage encryption solutions

### FIPS 140-2/3 - Security Requirements for Cryptographic Modules
- **Publisher**: NIST
- **Relevance**: BitLocker uses FIPS 140-2 validated cryptographic modules when configured in FIPS-compliant mode

## Compliance Mappings

| Framework | Requirement | BitLocker Coverage |
|-----------|------------|-------------------|
| PCI DSS 4.0 | 3.5.1 - Render PAN unreadable in storage | BitLocker full disk encryption |
| HIPAA | 164.312(a)(2)(iv) - Encryption/decryption | BitLocker protects ePHI at rest |
| GDPR | Article 32(1)(a) - Encryption of personal data | BitLocker for data-at-rest protection |
| NIST 800-53 | SC-28 Protection of Information at Rest | BitLocker encryption |
| NIST 800-171 | 3.13.16 - Confidentiality of CUI at rest | BitLocker on CUI systems |
| ISO 27001 | A.10.1.1 - Cryptographic controls policy | BitLocker implementation |

## Microsoft References

- **BitLocker Overview**: https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/
- **BitLocker Group Policy Reference**: https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/bitlocker-group-policy-settings
- **BitLocker Recovery Guide**: https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/bitlocker-recovery-guide-plan
- **TPM Recommendations**: https://learn.microsoft.com/en-us/windows/security/hardware-security/tpm/tpm-recommendations

---

## Workflows

## Workflow 1: Enterprise BitLocker Deployment

```
[Pre-deployment assessment]
    │
    ├── Verify TPM 2.0 across fleet
    ├── Confirm UEFI/Secure Boot
    ├── Plan recovery key escrow (AD DS or Azure AD)
    │
    ▼
[Configure GPO/Intune policy]
    │
    ├── Set encryption method (XTS-AES 256)
    ├── Configure key protectors (TPM + PIN for laptops, TPM for desktops)
    ├── Enable recovery key escrow
    │
    ▼
[Pilot deployment (test group)]
    │
    ├── Verify encryption completes without errors
    ├── Test recovery key retrieval
    ├── Verify no boot issues
    │
    ▼
[Production rollout (phased)]
    │
    ▼
[Monitor encryption status via Intune/SCCM reports]
    │
    ▼
[Verify 100% coverage, address failures]
```

## Workflow 2: BitLocker Recovery Process

```
[User locked out (BitLocker recovery screen)]
    │
    ▼
[User provides Recovery Key ID to helpdesk]
    │
    ▼
[Helpdesk retrieves recovery key]
    │
    ├── AD DS: RSAT BitLocker Recovery Password Viewer
    ├── Azure AD: Azure Portal → Devices → BitLocker keys
    ├── Intune: Intune Portal → Devices → Recovery keys
    │
    ▼
[User enters 48-digit recovery key]
    │
    ▼
[Investigate why recovery was triggered]
    │
    ├── BIOS/firmware update ──► [Expected, no action]
    ├── TPM failure ──► [Replace TPM or re-encrypt]
    ├── Boot configuration change ──► [Review change, re-seal TPM]
    └── Potential tampering ──► [Security investigation]
```

## Workflow 3: Key Rotation

```
[Quarterly key rotation policy]
    │
    ▼
[Generate new recovery password]
    │
    ▼
[Backup new key to AD/Azure AD]
    │
    ▼
[Remove old recovery password protector]
    │
    ▼
[Verify new key works in test recovery]
```

---

## Working Template

## Endpoint Information

| Field | Value |
|-------|-------|
| Hostname | |
| OS Version | |
| TPM Version | 2.0 |
| UEFI/Secure Boot | Enabled |
| Encryption Date | |

## Encryption Configuration

| Setting | OS Drive | Fixed Drives | Removable |
|---------|----------|-------------|-----------|
| Encryption Method | XTS-AES 256 | XTS-AES 256 | AES-CBC 256 |
| Key Protectors | TPM + PIN | Auto-unlock | Password |
| Recovery Key Escrow | AD DS / Azure AD | AD DS / Azure AD | N/A |
| Full/Used Space | Full disk | Used space only | Used space only |

## Recovery Key Register

| Volume | Key Protector ID | Escrowed To | Verified |
|--------|-----------------|-------------|----------|
| C: | | AD DS / Azure AD | Yes / No |
| D: | | AD DS / Azure AD | Yes / No |

## Compliance Checklist

- [ ] TPM 2.0 present and enabled
- [ ] Secure Boot enabled
- [ ] OS drive encrypted with XTS-AES 256
- [ ] Recovery key escrowed to AD/Azure AD
- [ ] PIN configured for laptop endpoints
- [ ] Fixed data drives encrypted
- [ ] Removable drive encryption policy active
- [ ] BitLocker cannot be disabled without admin

## Sign-Off

| Role | Name | Date |
|------|------|------|
| Endpoint Admin | | |
| Security Analyst | | |
