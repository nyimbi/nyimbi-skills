# Implementing RSA Key Pair Management

## API Reference

## Libraries Used

| Library | Purpose |
|---------|---------|
| `cryptography` | RSA key generation, signing, verification, serialization |
| `os` | Secure random bytes, file permissions |
| `datetime` | Certificate validity periods and key rotation schedules |
| `json` | Export key metadata and audit reports |

## Installation

```bash
pip install cryptography
```

## Key Generation

### Generate RSA Key Pair
```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

def generate_rsa_keypair(key_size=4096):
    """Generate an RSA key pair. Use 2048 minimum, 4096 recommended."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
    )
    return private_key
```

### Serialize Private Key (PEM, encrypted)
```python
def save_private_key(private_key, filepath, passphrase):
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(
            passphrase.encode()
        ),
    )
    with open(filepath, "wb") as f:
        f.write(pem)
    os.chmod(filepath, 0o600)  # Restrict permissions
```

### Serialize Public Key
```python
def save_public_key(private_key, filepath):
    public_key = private_key.public_key()
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    with open(filepath, "wb") as f:
        f.write(pem)
```

### Load Existing Key
```python
def load_private_key(filepath, passphrase=None):
    with open(filepath, "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=passphrase.encode() if passphrase else None,
        )
    return private_key

def load_public_key(filepath):
    with open(filepath, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())
    return public_key
```

## Signing and Verification

### Sign Data
```python
def sign_data(private_key, data):
    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    return signature
```

### Verify Signature
```python
from cryptography.exceptions import InvalidSignature

def verify_signature(public_key, data, signature):
    try:
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return True
    except InvalidSignature:
        return False
```

## Encryption and Decryption

### Encrypt with RSA-OAEP
```python
def encrypt_data(public_key, plaintext):
    ciphertext = public_key.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return ciphertext
```

### Decrypt with RSA-OAEP
```python
def decrypt_data(private_key, ciphertext):
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return plaintext
```

## Key Audit and Rotation

### Inspect Key Properties
```python
def audit_key(filepath, passphrase=None):
    key = load_private_key(filepath, passphrase)
    pub = key.public_key()
    numbers = pub.public_numbers()
    return {
        "key_size": key.key_size,
        "compliant": key.key_size >= 2048,
        "recommended": key.key_size >= 4096,
        "public_exponent": numbers.e,
        "modulus_bits": numbers.n.bit_length(),
        "format": "PKCS8-PEM",
        "encrypted": passphrase is not None,
    }
```

### Check Key Strength
```python
def check_key_strength(key_path, passphrase=None):
    key = load_private_key(key_path, passphrase)
    findings = []
    if key.key_size < 2048:
        findings.append({
            "issue": f"Key size {key.key_size} bits is below minimum (2048)",
            "severity": "critical",
        })
    elif key.key_size < 4096:
        findings.append({
            "issue": f"Key size {key.key_size} bits — 4096 recommended",
            "severity": "low",
        })
    return {"key_size": key.key_size, "findings": findings}
```

## Self-Signed Certificate Generation

```python
from cryptography import x509
from cryptography.x509.oid import NameOID
from datetime import datetime, timedelta, timezone

def create_self_signed_cert(private_key, common_name, days_valid=365):
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Security Audit"),
    ])
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.now(timezone.utc))
        .not_valid_after(datetime.now(timezone.utc) + timedelta(days=days_valid))
        .sign(private_key, hashes.SHA256())
    )
    return cert
```

## Output Format

```json
{
  "key_path": "/etc/pki/private/server.key",
  "key_size": 4096,
  "public_exponent": 65537,
  "compliant": true,
  "encrypted": true,
  "certificate": {
    "common_name": "server.example.com",
    "not_before": "2025-01-15T00:00:00Z",
    "not_after": "2026-01-15T00:00:00Z",
    "serial_number": "ABC123..."
  },
  "findings": []
}
```

---

## Standards and Controls

## Primary Standards

### NIST FIPS 186-5 - Digital Signature Standard (DSS)
- **URL**: https://csrc.nist.gov/publications/detail/fips/186/5/final
- **Description**: Specifies RSA digital signature generation and verification
- **RSA minimum**: 2048-bit keys

### RFC 8017 - PKCS #1: RSA Cryptography Specifications Version 2.2
- **URL**: https://www.rfc-editor.org/rfc/rfc8017
- **Description**: Defines RSA key formats, OAEP encryption, and PSS signatures
- **Key operations**: RSAEP, RSADP, RSASP1, RSAVP1

### RFC 5958 - Asymmetric Key Packages (PKCS#8 v2)
- **URL**: https://www.rfc-editor.org/rfc/rfc5958
- **Description**: Private key information syntax for storage

### RFC 7468 - Textual Encodings of PKIX, PKCS, and CMS Structures
- **URL**: https://www.rfc-editor.org/rfc/rfc7468
- **Description**: PEM encoding format specification

### NIST SP 800-57 Part 1 Rev. 5 - Key Management
- **URL**: https://csrc.nist.gov/publications/detail/sp/800-57-part-1/rev-5/final
- **Description**: Key length recommendations and lifecycle management
- **RSA 2048**: Acceptable through 2030
- **RSA 3072+**: Recommended for beyond 2030

### NIST SP 800-131A Rev. 2 - Transitioning Cryptographic Algorithms
- **URL**: https://csrc.nist.gov/publications/detail/sp/800-131a/rev-2/final
- **Description**: Transition guidance for algorithm selection
- **PKCS#1 v1.5 signatures**: Legacy use only
- **RSA-PSS**: Recommended for all new applications

## Python Library References

### cryptography (pyca/cryptography)
- **RSA Key Generation**: `cryptography.hazmat.primitives.asymmetric.rsa`
- **Serialization**: `cryptography.hazmat.primitives.serialization`
- **Signatures**: `cryptography.hazmat.primitives.asymmetric.padding`
- **Documentation**: https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/

---

## Workflows

## Workflow 1: Key Pair Generation

```
[Select Key Size] (3072 or 4096 bits)
      |
[Generate RSA Key Pair]
(public_exponent=65537)
      |
[Serialize Private Key]
(PEM/PKCS#8 with AES-256-CBC passphrase)
      |
[Extract and Serialize Public Key]
(PEM/SubjectPublicKeyInfo)
      |
[Compute Key Fingerprint]
(SHA-256 of DER-encoded public key)
      |
[Store Keys with Metadata]
(key_id, creation_date, algorithm, size)
```

## Workflow 2: Digital Signature (RSA-PSS)

```
[Document/Data to Sign]
      |
[Hash Data] (SHA-256)
      |
[Load Private Key] (decrypt with passphrase)
      |
[RSA-PSS Sign]
(padding=PSS, mgf=MGF1(SHA256), salt_length=PSS.MAX_LENGTH)
      |
[Output Signature] (DER or Base64)
```

## Workflow 3: Signature Verification

```
[Document + Signature + Public Key]
      |
[Load Public Key]
      |
[RSA-PSS Verify]
(same padding parameters as signing)
      |
[Valid?]
  YES --> Accept
  NO  --> Reject (data or signature tampered)
```

## Workflow 4: Key Rotation

```
[Current Key Pair (version N)]
      |
[Generate New Key Pair (version N+1)]
      |
[Update Active Key Reference]
      |
[Archive Old Key Pair]
(mark as "decrypt/verify only")
      |
[After Grace Period: Destroy Old Private Key]
(keep public key for verification)
```

## Workflow 5: RSA Encryption (OAEP)

```
[Plaintext] (max size depends on key and padding)
      |
[Load Recipient's Public Key]
      |
[RSA-OAEP Encrypt]
(padding=OAEP, mgf=MGF1(SHA256), algorithm=SHA256)
      |
[Ciphertext]
```

---

## Working Template

## Key Generation Checklist

- [ ] Select key size (minimum 3072 bits for new deployments)
- [ ] Generate key pair using secure random number generator
- [ ] Protect private key with strong passphrase (AES-256)
- [ ] Compute and record key fingerprint (SHA-256)
- [ ] Set restrictive file permissions on private key
- [ ] Store public key in accessible location
- [ ] Document key metadata (size, algorithm, creation date)

## Key Metadata Template

```json
{
  "key_id": "rsa-prod-001",
  "algorithm": "RSA",
  "key_size": 4096,
  "public_exponent": 65537,
  "fingerprint_sha256": "<hex-digest>",
  "created_at": "2024-01-01T00:00:00Z",
  "expires_at": "2025-01-01T00:00:00Z",
  "usage": ["sign", "verify"],
  "owner": "security-team",
  "version": 1
}
```

## Key Rotation Schedule

| Environment | Rotation Frequency | Grace Period |
|------------|-------------------|--------------|
| Production | 12 months | 30 days |
| Staging    | 6 months  | 14 days |
| Development| 3 months  | 7 days  |

## Quick Reference

```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

# Generate
key = rsa.generate_private_key(public_exponent=65537, key_size=4096)

# Sign (RSA-PSS)
signature = key.sign(data, padding.PSS(
    mgf=padding.MGF1(hashes.SHA256()),
    salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())

# Verify
key.public_key().verify(signature, data, padding.PSS(
    mgf=padding.MGF1(hashes.SHA256()),
    salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
```
