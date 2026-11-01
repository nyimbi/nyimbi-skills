# Implementing Code Signing For Artifacts

## API Reference

## Dependencies

| Library | Version | Purpose |
|---------|---------|---------|
| cryptography | >=41.0 | Ed25519 key generation, signing, and verification |

## CLI Usage

```bash
# Generate keypair
python scripts/agent.py --generate-keys --output-dir /keys/

# Sign artifact
python scripts/agent.py --sign build/app.tar.gz --private-key /keys/signing_key.pem

# Verify artifacts
python scripts/agent.py \
  --artifacts build/app.tar.gz build/lib.so \
  --public-key /keys/signing_key.pub \
  --output-dir /reports/
```

## Functions

### `generate_ed25519_keypair(output_dir) -> dict`
Calls `Ed25519PrivateKey.generate()`, serializes to PEM using `private_bytes()` and `public_bytes()`.

### `sign_artifact(file_path, private_key_path) -> dict`
Loads PEM key via `serialization.load_pem_private_key()`, calls `private_key.sign(data)`. Writes 64-byte signature to `.sig` file.

### `verify_signature(file_path, signature_path, public_key_path) -> dict`
Loads public key, calls `public_key.verify(signature, data)`. Catches `InvalidSignature`.

### `verify_cosign_signature(image) -> dict`
Runs `cosign verify <image>` via subprocess for container image signature verification.

### `batch_verify(artifacts, public_key_path) -> list`
Verifies multiple artifacts against the same public key.

## cryptography API Used

| Class/Method | Purpose |
|-------------|---------|
| `Ed25519PrivateKey.generate()` | Generate signing keypair |
| `private_key.sign(data)` | Sign data (returns 64 bytes) |
| `public_key.verify(signature, data)` | Verify signature |
| `serialization.load_pem_private_key()` | Load PEM private key |

## Output Schema

```json
{
  "summary": {"total": 3, "valid": 2, "invalid": 1},
  "verifications": [{"file": "app.tar.gz", "valid": true, "algorithm": "Ed25519"}]
}
```

---

## Standards and Controls

## SLSA Framework

### Level 1: Build Provenance
- Document the build process (source, builder, dependencies)
- Provenance metadata available for all artifacts

### Level 2: Signed Provenance
- Build provenance is signed by the build platform
- Signatures tied to authenticated builder identity

### Level 3: Hardened Build Platform
- Build process runs on a hardened, isolated platform
- Provenance is non-falsifiable by the build service

## NIST SSDF (SP 800-218)

### PS.2: Provide Mechanism for Verifying Software Release Integrity
- PS.2.1: Make integrity verification information available to consumers
- Code signing provides cryptographic proof of artifact integrity
- Transparency logs provide public auditability of signing events

### PW.4: Reuse Existing, Well-Secured Software
- Verify signatures of third-party dependencies before integration
- Establish trust anchors for acceptable signing identities

## CIS Software Supply Chain Security

### Artifacts (AR) Controls
- AR-1: Sign all build artifacts using cryptographic signatures
- AR-2: Verify artifact signatures before deployment
- AR-3: Use transparency logs for signing event auditability
- AR-4: Rotate signing keys on a defined schedule

## Executive Order 14028

- Section 4(e): Agencies shall employ tools and processes to maintain trusted source code supply chains
- SBOM and artifact signing required for federal software suppliers
- Sigstore adoption recommended by CISA for open-source supply chain security

---

## Workflows

## Signing Pipeline Flow

```
Build Artifacts
       │
       ▼
┌──────────────────┐
│ Generate          │
│ Checksums         │
└──────┬───────────┘
       │
       ├──────────────────────┐
       ▼                      ▼
┌──────────────┐    ┌──────────────┐
│ GPG Sign     │    │ Sigstore     │
│ (detached)   │    │ Keyless Sign │
└──────┬───────┘    └──────┬───────┘
       │                    │
       │                    ▼
       │            ┌──────────────┐
       │            │ Rekor Log    │
       │            │ Entry        │
       │            └──────┬───────┘
       │                    │
       └──────────┬─────────┘
                  ▼
       ┌──────────────────┐
       │ Publish Release  │
       │ + Signatures     │
       └──────────────────┘
```

## Signing Methods Comparison

| Method | Key Management | Identity | Verification | Best For |
|--------|---------------|----------|--------------|----------|
| GPG | Manual key lifecycle | Key fingerprint | gpg --verify | Traditional projects |
| Sigstore Keyless | No keys to manage | OIDC identity | cosign verify-blob | Modern CI/CD |
| Code Signing Cert | CA-issued certificate | Organization name | Platform-specific | Windows/macOS apps |
| npm Provenance | Automated | GitHub Actions OIDC | npm audit signatures | npm packages |

---

## Working Template

## GitHub Actions: Build, Sign, and Release

```yaml
name: Signed Release
on:
  push:
    tags: ['v*']

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: make build-all
      - uses: sigstore/cosign-installer@v3
      - name: Sign artifacts
        run: |
          for f in dist/*.tar.gz; do
            cosign sign-blob "$f" --output-signature "${f}.sig" --output-certificate "${f}.cert" --yes
          done
          sha256sum dist/*.tar.gz > dist/checksums.sha256
      - uses: softprops/action-gh-release@v2
        with:
          files: dist/*
```

## Verification Script

```bash
#!/bin/bash
set -euo pipefail
# verify-release.sh <artifact> <signature> <certificate>
ARTIFACT="$1"
SIGNATURE="$2"
CERTIFICATE="$3"

echo "Verifying: $ARTIFACT"
sha256sum "$ARTIFACT"

cosign verify-blob "$ARTIFACT" \
  --signature "$SIGNATURE" \
  --certificate "$CERTIFICATE" \
  --certificate-identity "https://github.com/org/repo/.github/workflows/release.yml@refs/tags/*" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com"

echo "Verification: PASSED"
```
