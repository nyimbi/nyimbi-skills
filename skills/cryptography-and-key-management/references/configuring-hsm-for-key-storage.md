# Configuring HSM For Key Storage

## API Reference

## Libraries

| Library | Install | Purpose |
|---------|---------|---------|
| boto3 | `pip install boto3` | AWS CloudHSM and KMS API |
| python-pkcs11 | `pip install python-pkcs11` | PKCS#11 interface for HSM operations |

## Key boto3 CloudHSMv2 Methods

| Method | Description |
|--------|-------------|
| `describe_clusters()` | List CloudHSM clusters |
| `describe_backups()` | List cluster backups |
| `create_cluster(HsmType, SubnetIds)` | Create new cluster |
| `create_hsm(ClusterId, AvailabilityZone)` | Add HSM to cluster |
| `initialize_cluster(ClusterId, SignedCert, TrustAnchor)` | Initialize cluster |

## Key boto3 KMS Methods (Custom Key Store)

| Method | Description |
|--------|-------------|
| `create_custom_key_store()` | Create KMS custom key store backed by CloudHSM |
| `describe_key(KeyId)` | Get key metadata including CustomKeyStoreId |
| `create_key(Origin="AWS_CLOUDHSM", CustomKeyStoreId=)` | Create key in HSM |

## PKCS#11 Operations

| Function | Description |
|----------|-------------|
| `C_Initialize` | Initialize PKCS#11 library |
| `C_OpenSession` | Open session with HSM |
| `C_Login` | Authenticate with HSM PIN |
| `C_GenerateKeyPair` | Generate asymmetric key pair |
| `C_Sign / C_Verify` | Cryptographic signing operations |

## HSM Types

| Type | Use Case |
|------|----------|
| AWS CloudHSM | Cloud-native FIPS 140-2 Level 3 |
| Thales Luna | On-premises enterprise HSM |
| nCipher nShield | High-assurance code signing |

## External References

- [AWS CloudHSM Docs](https://docs.aws.amazon.com/cloudhsm/)
- [boto3 CloudHSMv2](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2.html)
- [PKCS#11 Standard](https://docs.oasis-open.org/pkcs11/pkcs11-base/v2.40/pkcs11-base-v2.40.html)

---

## Standards and Controls

## Primary Standards

### PKCS#11 v3.0 (Cryptoki)
- **URL**: https://docs.oasis-open.org/pkcs11/pkcs11-base/v3.0/pkcs11-base-v3.0.html
- **Description**: Standard API for cryptographic token interface

### FIPS 140-2 / FIPS 140-3
- **URL**: https://csrc.nist.gov/publications/detail/fips/140/3/final
- **Description**: Security requirements for cryptographic modules
- **CMVP**: https://csrc.nist.gov/projects/cryptographic-module-validation-program

### NIST SP 800-57 Part 1 Rev. 5
- **URL**: https://csrc.nist.gov/publications/detail/sp/800-57-part-1/rev-5/final
- **Description**: Key management recommendations (HSM storage for high-value keys)

## HSM Products

### SoftHSM2 (Development/Testing)
- **URL**: https://www.opendnssec.org/softhsm/
- **GitHub**: https://github.com/opendnssec/SoftHSMv2
- **Description**: Software-only PKCS#11 implementation for testing

### AWS CloudHSM
- **URL**: https://docs.aws.amazon.com/cloudhsm/
- **FIPS**: 140-2 Level 3
- **PKCS#11**: https://docs.aws.amazon.com/cloudhsm/latest/userguide/pkcs11-library.html

### Azure Dedicated HSM
- **URL**: https://docs.microsoft.com/en-us/azure/dedicated-hsm/
- **FIPS**: 140-2 Level 3 (Thales Luna)

### Thales Luna HSM
- **URL**: https://cpl.thalesgroup.com/encryption/hardware-security-modules
- **FIPS**: 140-2 Level 3

## Python Libraries

### python-pkcs11
- **URL**: https://python-pkcs11.readthedocs.io/
- **PyPI**: https://pypi.org/project/python-pkcs11/

### PyKCS11
- **URL**: https://github.com/LudovicRousseau/PyKCS11
- **PyPI**: https://pypi.org/project/PyKCS11/

---

## Workflows

## Workflow 1: SoftHSM2 Initialization

```bash
# Install SoftHSM2
# Ubuntu: apt install softhsm2
# macOS: brew install softhsm

# Initialize a token
softhsm2-util --init-token --slot 0 --label "MyToken" --pin 1234 --so-pin 5678

# List tokens
softhsm2-util --show-slots
```

## Workflow 2: Key Generation via PKCS#11

```
[Connect to HSM]
(open session, login with PIN)
      |
[Generate Key]:
  Symmetric: AES-256 (CKM_AES_KEY_GEN)
  Asymmetric: RSA-4096 (CKM_RSA_PKCS_KEY_PAIR_GEN)
  Asymmetric: EC P-256 (CKM_EC_KEY_PAIR_GEN)
      |
[Set Key Attributes]:
  CKA_EXTRACTABLE = False
  CKA_SENSITIVE = True
  CKA_TOKEN = True (persistent)
  CKA_LABEL = "my-key-001"
      |
[Key Stored in HSM]
(returns handle, not key material)
```

## Workflow 3: Cryptographic Operations

```
[Application Request]
      |
[Open PKCS#11 Session]
      |
[Find Key by Label/ID]
      |
[Perform Operation on HSM]:
  Sign:    C_SignInit + C_Sign
  Verify:  C_VerifyInit + C_Verify
  Encrypt: C_EncryptInit + C_Encrypt
  Decrypt: C_DecryptInit + C_Decrypt
      |
[Return Result to Application]
(key never leaves HSM)
      |
[Close Session]
```

## Workflow 4: HSM Key Ceremony (Root CA)

```
[Prepare Air-Gapped HSM Station]
      |
[Multi-Person Authentication]
(M-of-N key custodians present)
      |
[Generate Root CA Key in HSM]
(CKA_EXTRACTABLE=False)
      |
[Sign Root CA Certificate]
(self-signed, 20-year validity)
      |
[Export Root CA Certificate]
(public certificate only)
      |
[Secure HSM in Safe/Vault]
(offline until next signing ceremony)
```

---

## Working Template

## HSM Selection Matrix

| HSM | FIPS Level | Cloud | On-Premise | Cost |
|-----|-----------|-------|-----------|------|
| SoftHSM2 | N/A (dev) | N/A | Yes | Free |
| AWS CloudHSM | 140-2 L3 | Yes | No | ~$1.60/hr |
| Azure Dedicated HSM | 140-2 L3 | Yes | No | ~$5,500/mo |
| Thales Luna | 140-2 L3 | Both | Yes | License |
| YubiHSM 2 | 140-2 L3 | No | Yes | ~$650 |

## PKCS#11 Key Attributes

```
CKA_TOKEN = True          # Persistent storage
CKA_PRIVATE = True        # Requires login
CKA_SENSITIVE = True      # Cannot be revealed in clear
CKA_EXTRACTABLE = False   # Cannot be exported
CKA_MODIFIABLE = False    # Cannot change attributes
CKA_LABEL = "my-key"      # Human-readable label
CKA_ID = <byte_string>    # Unique identifier
```

## Key Ceremony Checklist

- [ ] Prepare air-gapped workstation with HSM
- [ ] Assemble M-of-N key custodians (quorum)
- [ ] Initialize HSM and set SO/User PINs
- [ ] Generate root CA key in HSM (non-extractable)
- [ ] Generate and sign root CA certificate
- [ ] Export root CA certificate (public only)
- [ ] Verify certificate independently
- [ ] Secure HSM in physical vault
- [ ] Document ceremony in audit log
- [ ] Distribute key custodian tokens/smart cards
