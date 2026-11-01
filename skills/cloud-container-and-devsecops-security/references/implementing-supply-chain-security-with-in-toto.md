# Implementing Supply Chain Security With In Toto

## API Reference

## Libraries Used

| Library | Purpose |
|---------|---------|
| `in_toto` | Python reference implementation for supply chain verification |
| `securesystemslib` | Cryptographic key management and signing |
| `subprocess` | Execute `in-toto-run` and `in-toto-verify` CLI commands |
| `json` | Parse link metadata and layout files |

## Installation

```bash
pip install in-toto securesystemslib[crypto]
```

## CLI Commands

### Record a Supply Chain Step
```bash
# Record a build step (creates a link metadata file)
in-toto-run --step-name build \
    --key functionary-key \
    --materials src/ \
    --products dist/ \
    -- make build

# Record a test step
in-toto-run --step-name test \
    --key tester-key \
    --materials dist/ \
    --products test-results/ \
    -- pytest tests/
```

### Verify the Supply Chain
```bash
# Verify all steps match the layout
in-toto-verify --layout root.layout \
    --layout-keys project-owner-pub.key
```

### Generate Signing Keys
```bash
# Generate an Ed25519 keypair
in-toto-keygen --type ed25519 --output functionary-key
```

## Python API

### Create a Supply Chain Layout
```python
from in_toto.models.layout import Layout, Step, Inspection
from in_toto.models.metadata import Metadata
from securesystemslib.interface import import_ed25519_privatekey_from_file

# Load the project owner's private key
owner_key = import_ed25519_privatekey_from_file("owner-key")

# Define the supply chain layout
layout = Layout()
layout.expires = "2026-01-01T00:00:00Z"

# Step 1: Source code checkout
step_clone = Step(name="clone")
step_clone.expected_materials = []
step_clone.expected_products = [["CREATE", "src/*"]]
step_clone.pubkeys = [functionary_keyid]
step_clone.expected_command = ["git", "clone", "https://github.com/org/repo.git"]

# Step 2: Build
step_build = Step(name="build")
step_build.expected_materials = [
    ["MATCH", "src/*", "WITH", "PRODUCTS", "FROM", "clone"]
]
step_build.expected_products = [["CREATE", "dist/*"]]
step_build.pubkeys = [functionary_keyid]

# Step 3: Test
step_test = Step(name="test")
step_test.expected_materials = [
    ["MATCH", "dist/*", "WITH", "PRODUCTS", "FROM", "build"]
]
step_test.expected_products = [["CREATE", "test-results/*"]]
step_test.pubkeys = [tester_keyid]

layout.steps = [step_clone, step_build, step_test]

# Add an inspection (run at verification time)
inspection = Inspection(name="verify-checksums")
inspection.expected_materials = [
    ["MATCH", "dist/*", "WITH", "PRODUCTS", "FROM", "build"]
]
inspection.run = ["sha256sum", "dist/*"]
layout.inspect = [inspection]

# Sign and write the layout
metadata = Metadata(signed=layout)
metadata.sign(owner_key)
metadata.dump("root.layout")
```

### Record a Step Programmatically
```python
from in_toto.runlib import in_toto_run

# Record a step with materials and products
link = in_toto_run(
    name="build",
    material_list=["src/"],
    product_list=["dist/"],
    signing_key=functionary_key,
    record_streams=True,
    command=["make", "build"],
)
# Saves build.{keyid-prefix}.link
```

### Verify the Supply Chain
```python
from in_toto.verifylib import in_toto_verify

# Verify all steps and inspections
summary = in_toto_verify(
    metadata=layout_metadata,
    layout_key_dict={owner_keyid: owner_pubkey},
)
# Raises an exception if verification fails
```

### Inspect Link Metadata
```python
from in_toto.models.metadata import Metadata

link_metadata = Metadata.load("build.abc123.link")
link = link_metadata.signed
print(f"Step: {link.name}")
print(f"Command: {link.command}")
print(f"Materials: {list(link.materials.keys())}")
print(f"Products: {list(link.products.keys())}")
print(f"Return value: {link.byproducts.get('return-value')}")
```

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Layout** | Defines the expected supply chain steps, who performs them, and material/product rules |
| **Step** | A single supply chain operation (clone, build, test, package) |
| **Link** | Metadata recorded when a step is actually performed (materials, products, command) |
| **Inspection** | Verification commands run at verification time |
| **Functionary** | A person or CI system authorized to perform a step |
| **Materials** | Input files consumed by a step |
| **Products** | Output files produced by a step |

## Output Format

### Link Metadata
```json
{
  "signatures": [{"keyid": "abc123...", "sig": "..."}],
  "signed": {
    "_type": "link",
    "name": "build",
    "command": ["make", "build"],
    "materials": {
      "src/main.py": {"sha256": "a1b2c3..."}
    },
    "products": {
      "dist/app.tar.gz": {"sha256": "d4e5f6..."}
    },
    "byproducts": {
      "return-value": 0,
      "stdout": "Build successful",
      "stderr": ""
    }
  }
}
```

---

## Standards and Controls

## Industry Standards

### SLSA (Supply chain Levels for Software Artifacts)
- in-toto provides the attestation framework that SLSA builds upon
- SLSA provenance attestations use in-toto attestation format
- Graduated to v1.0 specification with clear level requirements

### NIST SSDF (Secure Software Development Framework) SP 800-218
- PO.1.1: Define and document security requirements for software
- PS.1.1: Verify third-party software components
- PW.4.1: Review and analyze source code for security vulnerabilities

### NIST SP 800-204D: Strategies for Securing the Software Supply Chain
- Section 4: Build system integrity verification
- Section 5: Attestation-based supply chain verification
- Recommends cryptographic provenance tracking

### Executive Order 14028 (Improving the Nation's Cybersecurity)
- Requires SBOM generation for software sold to federal government
- Mandates supply chain security for critical software
- in-toto attestations satisfy provenance requirements

## Compliance Mapping

| Requirement | Framework | in-toto Capability |
|-------------|-----------|-------------------|
| Build provenance | SLSA L2+ | Signed link metadata per build step |
| Artifact integrity | NIST 800-204D | SHA-256 hash chaining between steps |
| Authorized builders | SLSA L3+ | Functionary key verification |
| SBOM generation | EO 14028 | Inspection step for SBOM validation |
| Code review | SLSA L4 | Threshold signing with multiple reviewers |
| Tamper detection | PCI DSS 6.5 | End-to-end verification before deployment |

## Ecosystem Integration

### Sigstore
- Keyless signing via Fulcio certificate authority
- Transparency log via Rekor for attestation persistence
- Cosign for container image signing and verification

### Witness / Archivista
- Witness: in-toto implementation focused on cloud-native CI/CD
- Archivista: Attestation storage and retrieval service
- Both used by SolarWinds for supply chain integrity post-breach

### OpenVEX
- Vulnerability Exploitability eXchange format
- Complements in-toto attestations with vulnerability status
- Allows marking CVEs as "not affected" for specific builds

---

## Workflows

## Implementation Workflow

### Phase 1: Layout Design
1. Map your CI/CD pipeline steps (source, build, test, scan, package, push)
2. Identify functionaries for each step (CI runner, scanner, reviewer)
3. Define artifact flow between steps (what inputs/outputs)
4. Generate signing keys for each functionary
5. Create and sign the supply chain layout

### Phase 2: Pipeline Integration
1. Wrap each CI/CD step with `in-toto-run` to generate link metadata
2. Configure key management (Vault, KMS, or Sigstore keyless)
3. Store link metadata alongside build artifacts
4. Verify supply chain at end of pipeline before push to registry
5. Attach attestations to container images via cosign

### Phase 3: Deployment Verification
1. Deploy admission webhook for in-toto verification
2. Configure policy engine to require valid attestations
3. Test with known-good and known-bad attestation chains
4. Enable enforcement mode to block unverified images
5. Monitor verification failures and alert on anomalies

## CI/CD Pipeline Integration

### GitHub Actions Example
```yaml
jobs:
  build:
    steps:
      - uses: actions/checkout@v4
      - name: Record checkout step
        run: |
          in-toto-run --step-name checkout \
            --key ${{ secrets.BUILDER_KEY }} \
            --products Dockerfile src/* \
            -- echo "checkout complete"
      - name: Build and record
        run: |
          in-toto-run --step-name build \
            --key ${{ secrets.BUILDER_KEY }} \
            --materials Dockerfile src/* \
            --products image-digest.txt \
            -- docker build -t app:${{ github.sha }} .
      - name: Scan and record
        run: |
          in-toto-run --step-name scan \
            --key ${{ secrets.SCANNER_KEY }} \
            --materials image-digest.txt \
            --products vuln-report.json sbom.json \
            -- trivy image app:${{ github.sha }}
      - name: Verify chain
        run: |
          in-toto-verify --layout root.layout \
            --layout-key keys/owner.pub
```

## Key Rotation Workflow

1. Generate new key pair for the functionary
2. Update the supply chain layout with new public key
3. Re-sign the layout with the owner key
4. Distribute new private key to the functionary (via secrets manager)
5. Revoke the old key after transition period
6. Verify builds use new key going forward

## Incident Response Workflow

### Supply Chain Compromise Detected
1. Identify which step's attestation is invalid or missing
2. Check if functionary key was compromised
3. Review link metadata for the affected step
4. Compare artifact hashes against known-good builds
5. If compromise confirmed: revoke affected keys, rebuild from verified source
6. Update layout to add additional verification requirements

---

## Working Template

## Project Information

| Field | Value |
|-------|-------|
| Project Name | |
| Repository | |
| Container Registry | |
| in-toto Version | |
| Assessment Date | |
| Assessed By | |

## Supply Chain Layout

### Pipeline Steps

| Step | Functionary | Key Type | Threshold | Artifacts |
|------|-------------|----------|-----------|-----------|
| checkout | | | | |
| build | | | | |
| test | | | | |
| scan | | | | |
| push | | | | |

### Key Management

- [ ] Signing keys generated for all functionaries
- [ ] Keys stored in secrets manager (Vault, KMS)
- [ ] Key rotation schedule defined
- [ ] Layout signed by project owner key
- [ ] Backup keys secured offline

## Verification Checklist

- [ ] All required steps produce link metadata
- [ ] Artifact hashes chain correctly between steps
- [ ] Signatures verified against trusted functionaries
- [ ] Inspections pass (no critical vulnerabilities)
- [ ] Layout expiration date is current

## SLSA Compliance

| Level | Requirement | Status |
|-------|-------------|--------|
| L1 | Build process documented | |
| L2 | Signed provenance from hosted build | |
| L3 | Hardened build platform | |
| L4 | Two-party review + hermetic build | |

## Sign-Off

| Role | Name | Date |
|------|------|------|
| Security Engineer | | |
| Release Manager | | |
