# Implementing Aqua Security For Container Scanning

## API Reference

## Dependencies

| Library | Version | Purpose |
|---------|---------|---------|
| trivy CLI | >=0.50 | Container image scanning (invoked via subprocess) |

## CLI Usage

```bash
python scripts/agent.py \
  --images nginx:latest alpine:3.19 myapp:v1.2 \
  --severity CRITICAL,HIGH \
  --sbom \
  --output-dir /reports/ \
  --output trivy_report.json
```

## Functions

### `check_trivy_installed() -> bool`
Verifies Trivy CLI is available in PATH by running `trivy --version`.

### `scan_image(image, severity, ignore_unfixed) -> dict`
Runs `trivy image --format json --severity CRITICAL,HIGH <image>`. Returns parsed JSON output.

### `scan_image_misconfig(image) -> dict`
Runs `trivy image --scanners misconfig` to detect Dockerfile and config issues.

### `scan_image_secrets(image) -> dict`
Runs `trivy image --scanners secret` to find embedded secrets in image layers.

### `generate_sbom(image, output_path) -> bool`
Runs `trivy image --format cyclonedx` to produce CycloneDX SBOM.

### `parse_vuln_results(scan_data) -> list`
Extracts vulnerability details from Trivy JSON: VulnerabilityID, PkgName, InstalledVersion, FixedVersion, Severity.

### `compute_summary(vulns) -> dict`
Counts vulnerabilities by severity level (CRITICAL/HIGH/MEDIUM/LOW) and fixable count.

### `scan_multiple_images(images, severity) -> dict`
Orchestrates scanning of multiple images and aggregates results.

## Trivy CLI Commands Used

| Command | Purpose |
|---------|---------|
| `trivy image --format json` | Vulnerability scan with JSON output |
| `trivy image --scanners misconfig` | Misconfiguration detection |
| `trivy image --scanners secret` | Secret detection in layers |
| `trivy image --format cyclonedx` | SBOM generation |

## Output Schema

```json
{
  "images": [{"image": "nginx:latest", "summary": {"CRITICAL": 2, "HIGH": 5, "fixable": 4}}],
  "overall_summary": {"CRITICAL": 2, "HIGH": 5, "total": 7}
}
```

---

## Standards and Controls

## NIST SP 800-190: Application Container Security Guide

| Recommendation | Trivy Coverage |
|---------------|---------------|
| 4.1 Image vulnerabilities | CVE scanning of OS packages and app dependencies |
| 4.2 Image configuration defects | IaC misconfig scanning of Dockerfiles |
| 4.3 Embedded malware | Secret scanning detects embedded credentials |
| 4.4 Embedded cleartext secrets | Secret scanner with regex and entropy detection |
| 4.5 Use of untrusted images | Registry scanning and image provenance verification |

## CIS Docker Benchmark v1.6 Alignment

| CIS Control | Trivy Check |
|-------------|-------------|
| 4.1 Ensure image is created from a trusted base | Base image vulnerability scanning |
| 4.3 Ensure unnecessary packages are not installed | SBOM generation reveals full package inventory |
| 4.6 Add HEALTHCHECK instruction | Dockerfile misconfiguration check |
| 4.9 Ensure COPY instead of ADD | Dockerfile misconfiguration check |
| 4.10 Ensure secrets are not stored in Dockerfiles | Secret detection in filesystem scan |

## Vulnerability Database Sources

| Source | Coverage | Update Frequency |
|--------|----------|------------------|
| NVD (NIST) | All CVEs | Continuous |
| Alpine SecDB | Alpine Linux packages | Daily |
| Debian Security Tracker | Debian packages | Daily |
| Ubuntu CVE Tracker | Ubuntu packages | Daily |
| Red Hat OVAL | RHEL/CentOS packages | Daily |
| GitHub Advisory Database | Language packages | Continuous |
| Go Vulnerability Database | Go modules | Continuous |
| RustSec Advisory Database | Rust crates | Continuous |

---

## Workflows

## Workflow 1: CI/CD Image Gate

```
Developer commits code
       |
Docker image built in CI
       |
Trivy scans image for vulnerabilities
       |
[No Critical/High] --> Image pushed to registry
[Critical found] --> Pipeline fails, image rejected
       |
SBOM generated and stored alongside image
       |
Image tagged with scan metadata
       |
Kubernetes admission controller validates scan results
       |
Deployment proceeds only with scanned images
```

## Workflow 2: Registry Continuous Scanning

```
New image pushed to container registry
       |
Trivy Operator detects new image tag
       |
Scheduled scan triggered
       |
VulnerabilityReport CR created in cluster
       |
New CVE published in NVD
       |
Re-scan of all running images
       |
Alert generated for newly affected images
       |
Remediation ticket created automatically
```

## Workflow 3: SBOM-Based Vulnerability Tracking

```
Image scanned, SBOM generated (CycloneDX/SPDX)
       |
SBOM stored in artifact repository
       |
New CVE published
       |
SBOM re-scanned without rebuilding image
       |
Affected images identified across fleet
       |
Prioritized patching based on exposure and severity
```

---

## Working Template

## Image Registry Scanning Configuration

| Registry | URL | Auth Method | Auto-scan | Schedule |
|----------|-----|-------------|-----------|----------|
| | | | [ ] Yes | |

## Severity Threshold Policy

| Environment | Block Critical | Block High | Block Medium | Block Unfixable |
|-------------|---------------|------------|--------------|-----------------|
| Development | [ ] | [ ] | [ ] | [ ] |
| Staging | [x] | [ ] | [ ] | [ ] |
| Production | [x] | [x] | [ ] | [ ] |

## Accepted Risk Register (.trivyignore)

| CVE ID | Package | Reason | Accepted By | Expiry Date |
|--------|---------|--------|-------------|-------------|
| | | | | |

## SBOM Tracking

| Image | SBOM Format | Storage Location | Last Generated |
|-------|-------------|------------------|----------------|
| | [ ] CycloneDX [ ] SPDX | | |
