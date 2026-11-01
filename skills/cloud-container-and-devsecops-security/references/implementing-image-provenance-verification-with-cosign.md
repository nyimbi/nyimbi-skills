# Implementing Image Provenance Verification With Cosign

## API Reference

## Cosign CLI Commands

```bash
# Sign image (keyless with OIDC)
cosign sign --yes IMAGE_REF

# Sign with key
cosign sign --key cosign.key IMAGE_REF

# Verify (keyless)
cosign verify --certificate-identity USER --certificate-oidc-issuer ISSUER IMAGE_REF

# Verify with key
cosign verify --key cosign.pub IMAGE_REF

# Attach attestation
cosign attest --predicate sbom.json --type spdxjson IMAGE_REF

# Verify attestation
cosign verify-attestation --type spdxjson IMAGE_REF

# Get signature location
cosign triangulate IMAGE_REF
```

## Sigstore Components

| Component | Purpose |
|-----------|---------|
| Cosign | Sign and verify images |
| Fulcio | Short-lived certificate authority |
| Rekor | Transparency log |
| policy-controller | Kubernetes admission |

## Attestation Types

| Type | Predicate | Use Case |
|------|-----------|----------|
| `custom` | Custom JSON | General |
| `spdxjson` | SPDX SBOM | Software bill of materials |
| `cyclonedxjson` | CycloneDX SBOM | Alt SBOM format |
| `slsaprovenance` | SLSA Provenance | Build provenance |
| `vuln` | Vulnerability scan | Scan results |

## Kyverno Policy (Kubernetes Admission)

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: verify-images
spec:
  validationFailureAction: Enforce
  rules:
    - name: verify-cosign
      match:
        any:
          - resources: { kinds: [Pod] }
      verifyImages:
        - imageReferences: ["ghcr.io/org/*"]
          attestors:
            - entries:
                - keyless:
                    subject: "*@org.com"
                    issuer: "https://token.actions.githubusercontent.com"
```

### References

- Sigstore: https://sigstore.dev/
- Cosign Docs: https://docs.sigstore.dev/cosign/signing/overview/
- SLSA Framework: https://slsa.dev/
- Kyverno Image Verification: https://kyverno.io/docs/writing-policies/verify-images/

---

## Standards and Controls

## SLSA Framework (Supply-chain Levels for Software Artifacts)
- Level 1: Documentation of build process
- Level 2: Source version controlled + signed provenance
- Level 3: Hardened build platform, non-falsifiable provenance
- Level 4: Two-party review, hermetic reproducible builds

## NIST SP 800-190
- Section 4.1: Image vulnerabilities - Verify image integrity before deployment
- Section 5.1: Image security - Cryptographic signing and verification

## Executive Order 14028 (Improving the Nation's Cybersecurity)
- Section 4(e): SBOM requirements for software supply chain
- Section 4(g): Software supply chain security guidelines

## Sigstore Components

| Component | Purpose | URL |
|-----------|---------|-----|
| Cosign | Container signing/verification | https://github.com/sigstore/cosign |
| Fulcio | Free code signing CA | https://fulcio.sigstore.dev |
| Rekor | Transparency log | https://rekor.sigstore.dev |
| policy-controller | K8s admission enforcement | https://github.com/sigstore/policy-controller |

## Compliance Mappings

### PCI DSS v4.0
- Req 6.3.2: Develop software securely with integrity verification

### SOC 2
- CC8.1: Change management with cryptographic verification

### FedRAMP
- SA-12: Supply chain protection
- SI-7: Software, firmware, and information integrity

---

## Workflows

## Phase 1: Setup
1. Install cosign CLI
2. Choose signing method: keyless (recommended) or key-based
3. If key-based: generate keys, store private key in KMS
4. Configure CI/CD OIDC token for keyless signing

## Phase 2: Build Pipeline Integration
1. Build container image
2. Push to registry (by digest)
3. Sign image with cosign (keyless or key-based)
4. Generate SBOM with syft
5. Attach SBOM as attestation
6. Attach vulnerability scan as attestation

## Phase 3: Admission Enforcement
1. Deploy policy-controller or Kyverno
2. Create ClusterImagePolicy requiring signatures
3. Test with signed image (should pass)
4. Test with unsigned image (should be denied)
5. Enable enforcement in production namespaces

## Phase 4: Verification
```bash
# Manual verification
cosign verify --certificate-identity=CI_IDENTITY \
  --certificate-oidc-issuer=ISSUER \
  IMAGE@DIGEST

# Verify SBOM attestation
cosign verify-attestation --type cyclonedx \
  --certificate-identity=CI_IDENTITY \
  --certificate-oidc-issuer=ISSUER \
  IMAGE@DIGEST
```

## Phase 5: Monitoring
1. Check Rekor transparency log for audit trail
2. Monitor admission controller deny events
3. Alert on unsigned image deployment attempts

---

## Working Template

## Signing Requirements

| Environment | Signing Required | Attestations Required | Enforcement |
|-------------|-----------------|----------------------|-------------|
| Production | Yes (keyless) | SBOM + vuln scan | Deny unsigned |
| Staging | Yes (keyless) | SBOM | Warn unsigned |
| Development | Optional | None | Audit only |

## Trusted Identities

| Identity | OIDC Issuer | Registries |
|----------|-------------|------------|
| GitHub Actions CI | https://token.actions.githubusercontent.com | ghcr.io/myorg/* |
| Google Cloud Build | https://accounts.google.com | gcr.io/project/* |

## Image Inventory for Signing Audit

| Image | Registry | Signed | SBOM | Vuln Scan | Last Verified |
|-------|----------|--------|------|-----------|---------------|
| | | | | | |

## Key Management

| Key Type | Location | Rotation | Owner |
|----------|----------|----------|-------|
| Keyless (OIDC) | Fulcio CA | Ephemeral | CI/CD |
| Backup key pair | AWS KMS | Annual | Security |

## Verification Commands Reference

```bash
# Verify keyless signature
cosign verify \
  --certificate-identity=IDENTITY \
  --certificate-oidc-issuer=ISSUER \
  IMAGE@DIGEST

# Verify SBOM attestation
cosign verify-attestation --type cyclonedx \
  --certificate-identity=IDENTITY \
  --certificate-oidc-issuer=ISSUER \
  IMAGE@DIGEST
```
