# Scanning Container Images With Grype

## API Reference

## Grype CLI Commands

| Command | Description |
|---------|-------------|
| `grype <image>` | Scan a container image |
| `grype <image> -o json` | JSON output for parsing |
| `grype <image> -o sarif` | SARIF output for GitHub Security |
| `grype <image> --fail-on critical` | Exit non-zero on severity |
| `grype <image> --only-fixed` | Show only fixable vulns |
| `grype sbom:<file>` | Scan a pre-generated SBOM |
| `grype dir:<path>` | Scan a local directory |
| `grype db status` | Check vulnerability DB status |
| `grype db update` | Update vulnerability database |

## Input Sources

| Source | Syntax | Description |
|--------|--------|-------------|
| Registry | `grype nginx:latest` | Pull from registry |
| Docker daemon | `grype docker:myapp:1.0` | Local Docker image |
| Archive | `grype docker-archive:image.tar` | Saved tar archive |
| OCI dir | `grype oci-dir:path/` | OCI layout directory |
| SBOM | `grype sbom:bom.json` | CycloneDX/SPDX SBOM |
| Directory | `grype dir:/path/` | Filesystem scan |

## Severity Levels

| Level | CVSS Range | Action |
|-------|-----------|--------|
| Critical | 9.0 - 10.0 | Immediate remediation |
| High | 7.0 - 8.9 | Fix before deployment |
| Medium | 4.0 - 6.9 | Plan remediation |
| Low | 0.1 - 3.9 | Accept or fix later |
| Negligible | 0.0 | Informational |

## Python Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| `subprocess` | stdlib | Execute grype CLI |
| `json` | stdlib | Parse JSON output |
| `pathlib` | stdlib | File path handling |

## References

- Grype GitHub: https://github.com/anchore/grype
- Anchore Scan Action: https://github.com/anchore/scan-action
- Syft SBOM Generator: https://github.com/anchore/syft

---

## Standards and Controls

## Industry Standards

### NIST SP 800-190: Application Container Security Guide
- Section 4.1: Image vulnerabilities - Recommends scanning images for known vulnerabilities before deployment
- Section 4.2: Image configuration defects - Covers misconfigurations in container images
- Recommends integrating vulnerability scanning into CI/CD pipelines

### CIS Docker Benchmark v1.6
- Rule 4.1: Ensure a user for the container has been created
- Rule 4.6: Add HEALTHCHECK instruction to the container image
- Rule 4.9: Ensure that COPY is used instead of ADD
- Rule 4.10: Ensure secrets are not stored in Dockerfiles

### NIST SP 800-53 Rev 5
- RA-5: Vulnerability Monitoring and Scanning
- SI-2: Flaw Remediation
- CM-6: Configuration Settings
- SA-11: Developer Security Testing and Evaluation

### OWASP Container Security
- VS-001: Vulnerability Scanning - Scan container images for known vulnerabilities
- VS-002: SBOM Generation - Generate and maintain software bill of materials
- VS-003: Base Image Selection - Use minimal, trusted base images

## Vulnerability Databases

| Database | URL | Update Frequency |
|----------|-----|-----------------|
| NVD (National Vulnerability Database) | https://nvd.nist.gov/ | Continuous |
| GitHub Advisory Database | https://github.com/advisories | Continuous |
| OSV (Open Source Vulnerabilities) | https://osv.dev/ | Continuous |
| Alpine SecDB | https://secdb.alpinelinux.org/ | Daily |
| Debian Security Tracker | https://security-tracker.debian.org/ | Daily |

## CVSS Scoring Reference

| Severity | CVSS v3.1 Score | Recommended Action |
|----------|-----------------|-------------------|
| Critical | 9.0 - 10.0 | Block deployment, immediate remediation |
| High | 7.0 - 8.9 | Block deployment in production |
| Medium | 4.0 - 6.9 | Track and remediate within SLA |
| Low | 0.1 - 3.9 | Accept risk or remediate in next cycle |
| None | 0.0 | Informational |

## Compliance Mappings

### PCI DSS v4.0
- Requirement 6.3.1: Identify and manage security vulnerabilities
- Requirement 6.3.3: Update system components to address known vulnerabilities

### SOC 2
- CC7.1: To meet its objectives, the entity uses detection and monitoring procedures to identify changes to configurations that result in the introduction of new vulnerabilities

### FedRAMP
- RA-5(2): Update the vulnerabilities scanned within every 30 days prior to a new scan
- RA-5(5): Implement privileged access authorization for vulnerability scanning activities

---

## Workflows

## Phase 1: Environment Setup

### Install Grype and Syft
```bash
# Install Grype
curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin

# Install Syft for SBOM generation
curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin

# Verify
grype version
syft version
```

### Configure Grype
```bash
# Create config directory
mkdir -p ~/.grype

# Create configuration file
cat > ~/.grype/.grype.yaml <<EOF
check-for-app-update: false
fail-on-severity: "high"
db:
  auto-update: true
  cache-dir: "/tmp/grype-db"
  max-allowed-built-age: 120h
ignore:
  # Add known false positives here
  []
EOF
```

## Phase 2: Image Scanning Workflow

### Step 1 - Generate SBOM
```bash
syft ${IMAGE_REF} -o spdx-json > sbom.spdx.json
syft ${IMAGE_REF} -o cyclonedx-json > sbom.cdx.json
```

### Step 2 - Run Vulnerability Scan
```bash
# Scan directly
grype ${IMAGE_REF} -o json > vulnerability-report.json

# Or scan from SBOM (faster for repeated scans)
grype sbom:sbom.spdx.json -o json > vulnerability-report.json
```

### Step 3 - Evaluate Results
```bash
# Count by severity
cat vulnerability-report.json | jq '.matches | group_by(.vulnerability.severity) | map({severity: .[0].vulnerability.severity, count: length})'

# List critical and high findings
cat vulnerability-report.json | jq '[.matches[] | select(.vulnerability.severity == "Critical" or .vulnerability.severity == "High") | {id: .vulnerability.id, severity: .vulnerability.severity, package: .artifact.name, version: .artifact.version, fix: .vulnerability.fix.versions}]'
```

### Step 4 - Gate Decision
```bash
# Automated gate check
grype ${IMAGE_REF} --fail-on high
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo "GATE FAILED: High or Critical vulnerabilities found"
    exit 1
fi
```

## Phase 3: CI/CD Integration

### GitHub Actions Complete Workflow
```yaml
name: Container Security Scan
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build image
        run: docker build -t myapp:${{ github.sha }} .

      - name: Generate SBOM
        uses: anchore/sbom-action@v0
        with:
          image: myapp:${{ github.sha }}
          format: spdx-json
          output-file: sbom.spdx.json

      - name: Scan for vulnerabilities
        uses: anchore/scan-action@v4
        id: scan
        with:
          image: myapp:${{ github.sha }}
          fail-build: true
          severity-cutoff: high
          output-format: sarif

      - name: Upload SARIF to GitHub Security
        uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: ${{ steps.scan.outputs.sarif }}

      - name: Upload SBOM artifact
        uses: actions/upload-artifact@v4
        with:
          name: sbom
          path: sbom.spdx.json
```

## Phase 4: Reporting and Remediation

### Generate Human-Readable Report
```bash
# Table output with full details
grype ${IMAGE_REF} -o table > scan-report.txt

# Generate custom HTML report using template
grype ${IMAGE_REF} -o template -t report.tmpl > report.html
```

### Remediation Workflow
1. Review critical/high findings from scan output
2. Check if fix versions are available (`fix.versions` in JSON output)
3. Update base image to latest patched version
4. Update application dependencies
5. Rebuild and rescan to verify remediation
6. Add accepted risks to `.grype.yaml` ignore list with documented justification

## Phase 5: Continuous Monitoring

### Scheduled Rescans
```yaml
# GitHub Actions scheduled scan
name: Scheduled Vulnerability Scan
on:
  schedule:
    - cron: '0 6 * * 1'  # Every Monday at 6 AM

jobs:
  rescan:
    runs-on: ubuntu-latest
    steps:
      - name: Scan production images
        run: |
          for image in $(cat image-inventory.txt); do
            grype ${image} --fail-on critical -o json > "report-$(echo $image | tr '/:' '-').json"
          done
```

---

## Working Template

## Scan Policy Configuration

### Severity Thresholds

| Environment | Block On | Alert On | Accept |
|-------------|----------|----------|--------|
| Production | Critical, High | Medium | Low, Negligible |
| Staging | Critical | High, Medium | Low, Negligible |
| Development | None | Critical, High | Medium, Low, Negligible |

### Scan Triggers

- [ ] On image build (CI pipeline)
- [ ] On image push to registry
- [ ] Before deployment to production
- [ ] Scheduled weekly rescan of deployed images
- [ ] On new vulnerability database update

### Image Inventory

| Image | Registry | Tag Policy | Last Scanned | Status |
|-------|----------|------------|--------------|--------|
| `app/frontend` | ghcr.io | Immutable digest | YYYY-MM-DD | Pass/Fail |
| `app/backend` | ghcr.io | Immutable digest | YYYY-MM-DD | Pass/Fail |
| `app/worker` | ghcr.io | Immutable digest | YYYY-MM-DD | Pass/Fail |

## Grype Configuration Template

```yaml
# .grype.yaml - Place in repository root
check-for-app-update: false
fail-on-severity: "high"
output: "json"
scope: "squashed"
quiet: false

ignore:
  # Template: Add accepted risks below
  # - vulnerability: CVE-YYYY-NNNNN
  #   reason: "Justification for accepting this risk"
  #   expires: "YYYY-MM-DD"  # Optional expiration for risk acceptance

db:
  auto-update: true
  cache-dir: "/tmp/grype-db"
  max-allowed-built-age: 120h

match:
  java:
    using-cpes: true
  python:
    using-cpes: true
  javascript:
    using-cpes: false
  stock:
    using-cpes: true
```

## Risk Acceptance Form

### Vulnerability Risk Acceptance

| Field | Value |
|-------|-------|
| CVE ID | |
| Severity | |
| Affected Package | |
| Image(s) Affected | |
| Justification | |
| Compensating Controls | |
| Approved By | |
| Approval Date | |
| Expiration Date | |

## Remediation SLA

| Severity | Remediation Timeline | Escalation |
|----------|---------------------|------------|
| Critical | 24 hours | Security Lead + Engineering VP |
| High | 7 days | Security Lead |
| Medium | 30 days | Team Lead |
| Low | 90 days | Tracked in backlog |
| Negligible | Best effort | No escalation |
