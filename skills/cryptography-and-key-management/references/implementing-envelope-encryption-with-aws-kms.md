# Implementing Envelope Encryption With AWS Kms

## API Reference

## Libraries Used
- **boto3**: AWS SDK for KMS key management and data key generation
- **cryptography**: AES-256-GCM for local data encryption with generated data keys

## CLI Interface

```
python agent.py --region us-east-1 encrypt --input <file> --output <out> --key-id <kms_key>
python agent.py --region us-east-1 decrypt --input <encrypted> --output <out>
python agent.py --region us-east-1 list-keys
python agent.py --region us-east-1 audit --key-id <kms_key>
```

## Core Functions

### `generate_data_key(kms_key_id, region)`
Generates a data encryption key (DEK) using AWS KMS.
- `kms.generate_data_key(KeyId=key_id, KeySpec="AES_256")`
- Returns plaintext key (for local encryption) and encrypted key (for storage).

### `encrypt_data(plaintext_bytes, kms_key_id, region)`
Performs envelope encryption: generates DEK via KMS, encrypts data locally with AES-256-GCM, stores encrypted DEK alongside ciphertext.

### `decrypt_data(envelope, region)`
Decrypts envelope: calls `kms.decrypt(CiphertextBlob=encrypted_key)` to recover DEK, then decrypts data locally.

### `list_kms_keys(region)`
Lists KMS keys with metadata using `kms.list_keys()` and `kms.describe_key()`.

### `audit_key_policy(key_id, region)`
Audits KMS key policy for overly permissive principals (`Principal: "*"`).
- `kms.get_key_policy(KeyId=key_id, PolicyName="default")`

## boto3 KMS API Calls

| Method | Purpose |
|--------|---------|
| `kms.generate_data_key(KeyId, KeySpec)` | Generate plaintext + encrypted DEK |
| `kms.decrypt(CiphertextBlob)` | Decrypt encrypted DEK back to plaintext |
| `kms.list_keys()` | List all KMS keys in the account |
| `kms.describe_key(KeyId)` | Get key metadata (state, usage, origin) |
| `kms.get_key_policy(KeyId, PolicyName)` | Get key resource policy JSON |

## Dependencies
```
pip install boto3>=1.28 cryptography>=41.0
```

---

## Standards and Controls

## AWS Documentation

### AWS KMS Developer Guide
- **URL**: https://docs.aws.amazon.com/kms/latest/developerguide/
- **Envelope Encryption**: https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#enveloping

### AWS KMS API Reference
- **GenerateDataKey**: https://docs.aws.amazon.com/kms/latest/APIReference/API_GenerateDataKey.html
- **Decrypt**: https://docs.aws.amazon.com/kms/latest/APIReference/API_Decrypt.html
- **ReEncrypt**: https://docs.aws.amazon.com/kms/latest/APIReference/API_ReEncrypt.html

### AWS Encryption SDK
- **URL**: https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/
- **Python**: https://aws-encryption-sdk-python.readthedocs.io/

## Cryptographic Standards

### NIST SP 800-57 Part 1 - Key Management
- **URL**: https://csrc.nist.gov/publications/detail/sp/800-57-part-1/rev-5/final
- **Relevance**: Key hierarchy and key wrapping concepts

### NIST SP 800-38F - Key Wrap
- **URL**: https://csrc.nist.gov/publications/detail/sp/800-38f/final
- **Description**: AES Key Wrap specification used by KMS internally

### FIPS 140-2 Level 2 (KMS HSMs)
- **Description**: KMS HSMs are validated at FIPS 140-2 Level 2 (Level 3 for CloudHSM)

## Compliance Frameworks

### PCI DSS v4.0 Requirement 3
- Key management with separation of DEK and KEK
- KMS satisfies key management requirements

### SOC 2 Type II
- AWS KMS is SOC 2 compliant
- Encryption controls map to CC6.1 (logical access controls)

### HIPAA
- KMS encryption satisfies encryption requirements for ePHI
- BAA required with AWS

## Python Libraries

### boto3 (AWS SDK for Python)
- **URL**: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html
- **PyPI**: https://pypi.org/project/boto3/

### aws-encryption-sdk
- **URL**: https://pypi.org/project/aws-encryption-sdk/
- **Description**: High-level envelope encryption with caching

---

## Workflows

## Workflow 1: Encrypt Data with Envelope Encryption

```
[Application]
      |
[Call KMS GenerateDataKey]
(KeyId=CMK ARN, KeySpec=AES_256)
      |
[KMS Returns]:
  - Plaintext DEK (32 bytes)
  - Encrypted DEK (ciphertext blob)
      |
[Encrypt Data Locally]
(AES-256-GCM with plaintext DEK)
      |
[Store]:
  - Encrypted DEK (ciphertext blob)
  - Encrypted data (nonce + ciphertext + tag)
  - Encryption context metadata
      |
[Wipe Plaintext DEK from Memory]
```

## Workflow 2: Decrypt Data

```
[Read Stored Data]
  - Encrypted DEK
  - Encrypted data
  - Encryption context
      |
[Call KMS Decrypt]
(CiphertextBlob=Encrypted DEK, EncryptionContext)
      |
[KMS Returns Plaintext DEK]
      |
[Decrypt Data Locally]
(AES-256-GCM with plaintext DEK)
      |
[Return Plaintext Data]
      |
[Wipe Plaintext DEK from Memory]
```

## Workflow 3: Key Rotation

```
[Enable Automatic Key Rotation on CMK]
(KMS rotates backing key annually)
      |
[New GenerateDataKey calls use new backing key]
      |
[Old encrypted DEKs still decrypt]
(KMS tracks all backing key versions)
      |
[Optional: Re-encrypt old DEKs]
[Call KMS ReEncrypt to update DEK encryption]
```

## Workflow 4: Multi-Region Encryption

```
[Primary Region (us-east-1)]
  |
  [Create Multi-Region CMK]
  [Replicate to us-west-2, eu-west-1]
  |
  [Encrypt with Regional Endpoint]
  |
[Secondary Region (us-west-2)]
  |
  [Same Key ID works for Decrypt]
  [No cross-region API calls needed]
```

---

## Working Template

## Prerequisites Checklist

- [ ] AWS account with KMS access
- [ ] IAM policy allows kms:GenerateDataKey, kms:Decrypt, kms:ReEncrypt
- [ ] KMS Customer Managed Key (CMK) created
- [ ] CloudTrail logging enabled for KMS events
- [ ] boto3 and cryptography Python libraries installed

## IAM Policy Template

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "kms:GenerateDataKey",
        "kms:Decrypt",
        "kms:ReEncrypt*",
        "kms:DescribeKey"
      ],
      "Resource": "arn:aws:kms:us-east-1:123456789012:key/your-key-id"
    }
  ]
}
```

## KMS Key Policy Template

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowKeyAdministration",
      "Effect": "Allow",
      "Principal": {"AWS": "arn:aws:iam::123456789012:role/KeyAdmin"},
      "Action": [
        "kms:Create*", "kms:Describe*", "kms:Enable*", "kms:List*",
        "kms:Put*", "kms:Update*", "kms:Revoke*", "kms:Disable*",
        "kms:Get*", "kms:Delete*", "kms:ScheduleKeyDeletion",
        "kms:CancelKeyDeletion"
      ],
      "Resource": "*"
    },
    {
      "Sid": "AllowKeyUsage",
      "Effect": "Allow",
      "Principal": {"AWS": "arn:aws:iam::123456789012:role/AppRole"},
      "Action": ["kms:Decrypt", "kms:GenerateDataKey", "kms:ReEncrypt*"],
      "Resource": "*"
    }
  ]
}
```

## Quick Reference

```python
import boto3
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

kms = boto3.client('kms')

# Encrypt
resp = kms.generate_data_key(KeyId='alias/my-key', KeySpec='AES_256')
plaintext_key = resp['Plaintext']
encrypted_key = resp['CiphertextBlob']

nonce = os.urandom(12)
ciphertext = AESGCM(plaintext_key).encrypt(nonce, data, None)
# Store: encrypted_key + nonce + ciphertext

# Decrypt
resp = kms.decrypt(CiphertextBlob=encrypted_key)
plaintext_key = resp['Plaintext']
data = AESGCM(plaintext_key).decrypt(nonce, ciphertext, None)
```

## Cost Estimation

| Operation | Price | Notes |
|-----------|-------|-------|
| KMS API requests | $0.03 per 10,000 | GenerateDataKey, Decrypt |
| CMK storage | $1.00 per month | Per customer managed key |
| Key rotation | Free | Automatic annual rotation |
