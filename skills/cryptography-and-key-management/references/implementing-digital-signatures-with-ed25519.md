# Implementing Digital Signatures With Ed25519

## API Reference

## Dependencies

| Library | Version | Purpose |
|---------|---------|---------|
| cryptography | >=41.0 | Ed25519 key generation, signing, verification |

## CLI Usage

```bash
# Generate keypair
python scripts/agent.py --generate-keys --output-dir /keys/

# Sign a file
python scripts/agent.py --sign release.tar.gz --private-key /keys/ed25519_private.pem

# Verify files
python scripts/agent.py --verify release.tar.gz --public-key /keys/ed25519_public.pem
```

## Functions

### `generate_keypair(output_dir, key_name) -> dict`
`Ed25519PrivateKey.generate()`, serializes with `private_bytes(PEM, PKCS8, NoEncryption)` and `public_bytes(PEM, SubjectPublicKeyInfo)`.

### `sign_message(private_key_path, message) -> dict`
Loads key via `load_pem_private_key()`, calls `key.sign(message)`. Returns base64 and hex signature.

### `sign_file(private_key_path, file_path) -> dict`
Signs file contents, writes `.ed25519.sig` JSON containing signature, hash, timestamp.

### `verify_message(public_key_path, message, signature_b64) -> dict`
Calls `key.verify(signature, message)`. Catches `InvalidSignature`.

### `verify_file(public_key_path, file_path, sig_path) -> dict`
Verifies file against `.ed25519.sig` JSON, checks hash match.

## cryptography API

| Method | Purpose |
|--------|---------|
| `Ed25519PrivateKey.generate()` | Generate 32-byte private key |
| `private_key.sign(data)` | Create 64-byte signature |
| `public_key.verify(signature, data)` | Verify signature |
| `load_pem_private_key(data, password)` | Load PEM key |

## Output Schema

```json
{
  "verifications": [{"file": "release.tar.gz", "valid": true}],
  "valid": 3, "invalid": 0
}
```

---

## Standards and Controls

## Primary Standards

### RFC 8032 - Edwards-Curve Digital Signature Algorithm (EdDSA)
- **URL**: https://www.rfc-editor.org/rfc/rfc8032
- **Description**: Defines Ed25519 and Ed448 signature algorithms

### RFC 8709 - Ed25519 and Ed448 Public Key Algorithms for SSH
- **URL**: https://www.rfc-editor.org/rfc/rfc8709
- **Description**: SSH key format for Ed25519

### NIST FIPS 186-5 - Digital Signature Standard
- **URL**: https://csrc.nist.gov/publications/detail/fips/186/5/final
- **Description**: Includes EdDSA as approved signature algorithm

### RFC 7748 - Elliptic Curves for Security
- **URL**: https://www.rfc-editor.org/rfc/rfc7748
- **Description**: Defines Curve25519 and Curve448

## Python Libraries

### cryptography (pyca/cryptography)
- **Ed25519**: `cryptography.hazmat.primitives.asymmetric.ed25519`
- **Docs**: https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ed25519/

### PyNaCl (libsodium)
- **URL**: https://pynacl.readthedocs.io/
- **Ed25519**: `nacl.signing`
- **Docs**: https://pynacl.readthedocs.io/en/latest/signing/

## Related

### Daniel J. Bernstein et al. - High-speed high-security signatures
- **URL**: https://ed25519.cr.yp.to/
- **Description**: Original Ed25519 paper and reference implementation

---

## Workflows

## Workflow 1: Key Generation and Storage

```
[Generate Ed25519 Key Pair]
(32-byte private seed -> 32-byte public key)
      |
[Serialize Private Key (PKCS#8 PEM)]
[Serialize Public Key (SubjectPublicKeyInfo PEM)]
      |
[Encrypt Private Key with Passphrase]
      |
[Store with Metadata]
(key_id, fingerprint, creation_date)
```

## Workflow 2: Sign Document

```
[Document to Sign]
      |
[Load Private Key (decrypt passphrase)]
      |
[Ed25519 Sign]
(deterministic: SHA-512 internal hash)
      |
[Output: 64-byte Signature]
      |
[Create Signature File]
(signature + public key reference + metadata)
```

## Workflow 3: Verify Signature

```
[Document + Signature + Public Key]
      |
[Load Public Key]
      |
[Ed25519 Verify]
      |
[Valid?]
  YES -> Accept document as authentic
  NO  -> Reject (tampering detected)
```

## Workflow 4: Code Signing System

```
[Build Artifact] (binary, package, container)
      |
[Hash Artifact] (SHA-256)
      |
[Create Signing Manifest]
(artifact_name, hash, timestamp, signer_id)
      |
[Sign Manifest with Ed25519]
      |
[Distribute: Artifact + Manifest + Signature + Public Key]
      |
[Recipient Verifies]:
  1. Verify signature on manifest
  2. Hash artifact and compare to manifest
  3. Check signer identity against trust store
```

---

## Working Template

## Quick Reference

```python
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

# Generate
private_key = Ed25519PrivateKey.generate()
public_key = private_key.public_key()

# Sign
signature = private_key.sign(b"message data")

# Verify
public_key.verify(signature, b"message data")  # raises InvalidSignature on failure
```

## Key Formats

| Format | Private Key Size | Public Key Size | Signature Size |
|--------|-----------------|-----------------|----------------|
| Raw | 32 bytes | 32 bytes | 64 bytes |
| PEM (PKCS#8) | ~119 bytes | ~90 bytes | N/A |
| SSH | ~83 bytes | ~51 bytes | ~83 bytes |

## Use Cases

- API request authentication (sign request body)
- Software/code signing
- Document signing
- Git commit signing (ssh-ed25519)
- JWT signing (EdDSA algorithm)
- Certificate signing (X.509 with Ed25519)
