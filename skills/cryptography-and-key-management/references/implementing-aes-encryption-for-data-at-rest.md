# Implementing AES Encryption For Data At REST

## API Reference

## cryptography Library - AESGCM

```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

key = AESGCM.generate_key(bit_length=256)
aesgcm = AESGCM(key)
nonce = os.urandom(12)  # 96-bit nonce, NEVER reuse

ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data)
plaintext = aesgcm.decrypt(nonce, ciphertext, associated_data)
```

## Key Derivation - PBKDF2

```python
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,               # 256-bit key
    salt=os.urandom(16),
    iterations=600_000,      # NIST 2024 recommendation
)
key = kdf.derive(password.encode())
```

## Encrypted File Format

```
[salt: 16 bytes][nonce: 12 bytes][ciphertext + tag: variable]
```

| Field | Size | Purpose |
|-------|------|---------|
| Salt | 16 bytes | PBKDF2 salt (random per file) |
| Nonce | 12 bytes | GCM nonce (random per encryption) |
| Ciphertext | Variable | Encrypted data + 16-byte auth tag |

## AES Modes Comparison

| Mode | AEAD | Nonce Size | Use Case |
|------|------|------------|----------|
| GCM | Yes | 12 bytes | File/network encryption |
| CBC | No | 16 bytes | Legacy, disk encryption |
| CTR | No | 16 bytes | Streaming |
| XTS | No | 16 bytes | Full disk encryption |

## Fernet (High-Level API)

```python
from cryptography.fernet import Fernet
key = Fernet.generate_key()
f = Fernet(key)
token = f.encrypt(b"data")
plaintext = f.decrypt(token)
```

### References

- cryptography AESGCM: https://cryptography.io/en/latest/hazmat/primitives/aead/
- NIST SP 800-38D (GCM): https://csrc.nist.gov/publications/detail/sp/800-38d/final
- NIST FIPS 197 (AES): https://csrc.nist.gov/publications/detail/fips/197/final

---

## Standards and Controls

## Primary Standards

### NIST FIPS 197 - Advanced Encryption Standard (AES)
- **URL**: https://csrc.nist.gov/publications/detail/fips/197/final
- **Description**: Defines the AES algorithm (Rijndael) with key sizes of 128, 192, and 256 bits
- **Block size**: 128 bits (16 bytes)
- **Key sizes**: 128, 192, or 256 bits
- **Rounds**: 10 (128-bit), 12 (192-bit), 14 (256-bit)

### NIST SP 800-38D - Recommendation for Block Cipher Modes: GCM and GMAC
- **URL**: https://csrc.nist.gov/publications/detail/sp/800-38d/final
- **Description**: Specifies Galois/Counter Mode (GCM) for authenticated encryption
- **IV length**: 96 bits recommended for GCM
- **Tag length**: 128 bits recommended (minimum 96 bits)
- **Max plaintext**: 2^39 - 256 bits per invocation

### NIST SP 800-132 - Recommendation for Password-Based Key Derivation
- **URL**: https://csrc.nist.gov/publications/detail/sp/800-132/final
- **Description**: Covers PBKDF2 for deriving cryptographic keys from passwords
- **Minimum iterations**: 600,000 (OWASP 2024 recommendation for PBKDF2-SHA256)
- **Salt length**: Minimum 128 bits (16 bytes)

### NIST SP 800-38A - Recommendation for Block Cipher Modes of Operation
- **URL**: https://csrc.nist.gov/publications/detail/sp/800-38a/final
- **Description**: Defines ECB, CBC, CFB, OFB, and CTR modes

### NIST SP 800-57 Part 1 Rev. 5 - Key Management
- **URL**: https://csrc.nist.gov/publications/detail/sp/800-57-part-1/rev-5/final
- **Description**: Recommendations for cryptographic key lengths and algorithms
- **AES-256 security strength**: 256 bits
- **Recommended until**: Beyond 2031

## RFC Standards

### RFC 5116 - An Interface and Algorithms for Authenticated Encryption
- **URL**: https://www.rfc-editor.org/rfc/rfc5116
- **Description**: Defines AEAD interface including AES-GCM

### RFC 5869 - HMAC-based Extract-and-Expand Key Derivation Function (HKDF)
- **URL**: https://www.rfc-editor.org/rfc/rfc5869
- **Description**: Key derivation from existing key material (not passwords)

### RFC 9106 - Argon2 Memory-Hard Function
- **URL**: https://www.rfc-editor.org/rfc/rfc9106
- **Description**: Argon2 password hashing / key derivation specification
- **Recommended variant**: Argon2id (hybrid of Argon2i and Argon2d)

## Compliance Frameworks

### PCI DSS v4.0 - Requirement 3
- Encrypt stored cardholder data with strong cryptography
- AES-256 meets the strong cryptography requirement
- Key management procedures required

### HIPAA Security Rule - 45 CFR 164.312(a)(2)(iv)
- Encryption of ePHI at rest is an addressable implementation specification
- AES-256 is an acceptable encryption method

### GDPR Article 32 - Security of Processing
- Encryption is listed as an appropriate technical measure
- AES-256 satisfies encryption requirements for personal data protection

## Python Library References

### cryptography (pyca/cryptography)
- **URL**: https://cryptography.io/en/latest/
- **PyPI**: https://pypi.org/project/cryptography/
- **AES-GCM**: `cryptography.hazmat.primitives.ciphers.aead.AESGCM`
- **PBKDF2**: `cryptography.hazmat.primitives.kdf.pbkdf2.PBKDF2HMAC`

### PyCryptodome
- **URL**: https://pycryptodome.readthedocs.io/
- **PyPI**: https://pypi.org/project/pycryptodome/
- **AES-GCM**: `Crypto.Cipher.AES` with `MODE_GCM`

---

## Workflows

## Workflow 1: Single File Encryption

```
[Input File] --> [Read File Bytes]
                      |
              [Derive Key from Password]
              (PBKDF2 / Argon2id + random salt)
                      |
              [Generate Random Nonce]
              (12 bytes from CSPRNG)
                      |
              [AES-256-GCM Encrypt]
              (key + nonce + plaintext --> ciphertext + tag)
                      |
              [Write Encrypted File]
              (salt || nonce || ciphertext || tag)
```

## Workflow 2: Single File Decryption

```
[Encrypted File] --> [Parse Header]
                     (extract salt, nonce)
                          |
                  [Derive Key from Password]
                  (same PBKDF2 / Argon2id params + extracted salt)
                          |
                  [AES-256-GCM Decrypt]
                  (key + nonce + ciphertext + tag)
                          |
                  [Verify Authentication Tag]
                  (reject if tag invalid)
                          |
                  [Write Decrypted File]
```

## Workflow 3: Streaming Encryption for Large Files

```
[Large Input File]
      |
[Read in Chunks] (e.g., 64KB chunks)
      |
[For Each Chunk]:
  - [Encrypt chunk with AES-256-CTR]
  - [Update HMAC with ciphertext chunk]
  - [Write encrypted chunk to output]
      |
[Finalize HMAC]
[Append HMAC tag to output]
```

## Workflow 4: Directory Tree Encryption

```
[Source Directory]
      |
[Walk Directory Tree]
      |
[For Each File]:
  - [Derive unique file key from master key + file path]
  - [Generate random nonce]
  - [AES-256-GCM encrypt file]
  - [Write encrypted file preserving directory structure]
      |
[Create Manifest File]
(maps original paths to encrypted paths with metadata)
```

## Workflow 5: Key Derivation Pipeline

```
[User Password]
      |
[Generate Random Salt] (16 bytes)
      |
[PBKDF2-SHA256]
  - iterations: 600,000+
  - dkLen: 32 bytes (256 bits)
      |
[Derived Key (256-bit)]
      |
[Optional: HKDF Expand]
  - Derive multiple subkeys from single derived key
  - info="encryption" --> encryption key
  - info="authentication" --> HMAC key
```

## Workflow 6: Envelope Encryption Pattern

```
[Master Key] (stored in HSM/KMS)
      |
[Generate Random Data Encryption Key (DEK)]
(32 bytes from CSPRNG)
      |
[Encrypt DEK with Master Key] --> [Encrypted DEK]
      |
[Encrypt Data with DEK] --> [Ciphertext]
      |
[Store: Encrypted DEK + Ciphertext]
[Securely Wipe DEK from Memory]
```

## Error Handling Workflow

```
[Decryption Attempt]
      |
  [Parse Header] --FAIL--> [Return: Corrupt/invalid file format]
      |
  [Derive Key] --FAIL--> [Return: KDF parameter error]
      |
  [Decrypt + Verify Tag]
      |
  [Tag Valid?]
    YES --> [Return plaintext]
    NO  --> [Return: Authentication failed - data tampered]
            [DO NOT return partial plaintext]
```

---

## Working Template

## Pre-Implementation Checklist

- [ ] Identify data classification level and regulatory requirements
- [ ] Determine key management strategy (local, HSM, KMS)
- [ ] Select AES mode (GCM recommended for authenticated encryption)
- [ ] Define key derivation parameters (algorithm, iterations)
- [ ] Plan nonce/IV generation strategy
- [ ] Determine encrypted file format and metadata storage
- [ ] Review compliance requirements (PCI-DSS, HIPAA, GDPR)

## Configuration Parameters

```yaml
encryption:
  algorithm: AES-256-GCM
  key_length: 256
  nonce_length: 96  # bits
  tag_length: 128   # bits

key_derivation:
  algorithm: PBKDF2-SHA256
  iterations: 600000
  salt_length: 128  # bits

file_format:
  magic_bytes: "AES256GCM"
  version: 1
  header: "magic || version || salt || nonce"
  body: "ciphertext || tag"
```

## Integration Code Template

```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import os

def encrypt_data(plaintext: bytes, password: str) -> bytes:
    """Encrypt data with AES-256-GCM."""
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600_000,
    )
    key = kdf.derive(password.encode())
    nonce = os.urandom(12)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    return salt + nonce + ciphertext

def decrypt_data(data: bytes, password: str) -> bytes:
    """Decrypt AES-256-GCM encrypted data."""
    salt = data[:16]
    nonce = data[16:28]
    ciphertext = data[28:]
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600_000,
    )
    key = kdf.derive(password.encode())
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, None)
```

## Testing Checklist

- [ ] Encrypt and decrypt a small text file
- [ ] Encrypt and decrypt a large binary file (>100MB)
- [ ] Verify wrong password raises authentication error
- [ ] Verify tampered ciphertext raises authentication error
- [ ] Verify nonce uniqueness across multiple encryptions
- [ ] Measure encryption throughput (MB/s)
- [ ] Test with empty files and edge cases

## Common Pitfalls

| Pitfall | Impact | Mitigation |
|---------|--------|------------|
| Nonce reuse with same key | Complete loss of confidentiality in GCM | Always generate random nonce per encryption |
| Low PBKDF2 iterations | Brute-force password attacks | Use minimum 600,000 iterations |
| ECB mode usage | Pattern leakage in ciphertext | Always use GCM or CBC (never ECB) |
| No authentication | Undetected ciphertext modification | Use AEAD modes (GCM, CCM) |
| Hardcoded keys | Key compromise | Use KMS, HSM, or environment variables |
| No key rotation | Extended exposure window | Implement periodic key rotation policy |
