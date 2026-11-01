# Scanning docker Images With Trivy

## API Reference

## Trivy Scanner Types

| Scanner | Flag | Detects |
|---------|------|---------|
| Vulnerability | `--scanners vuln` | CVEs in OS packages and libraries |
| Misconfiguration | `--scanners misconfig` | Dockerfile/K8s misconfigs |
| Secret | `--scanners secret` | Hardcoded passwords, API keys |
| License | `--scanners license` | License compliance issues |

## Core Commands

| Command | Description |
|---------|-------------|
| `trivy image <ref>` | Scan Docker image |
| `trivy image --input <tar>` | Scan saved tar archive |
| `trivy image --format json` | JSON output |
| `trivy image --format sarif` | SARIF for GitHub Security |
| `trivy image --format cyclonedx` | CycloneDX SBOM |
| `trivy image --format spdx-json` | SPDX SBOM |
| `trivy image --exit-code 1 --severity CRITICAL` | Fail on critical |
| `trivy image --list-all-pkgs` | List all detected packages |

## Vulnerability Database Sources

| Source | Coverage |
|--------|----------|
| NVD | All ecosystems |
| GitHub Advisory Database | Open source packages |
| Alpine SecDB | Alpine Linux |
| Debian Security Tracker | Debian packages |
| Red Hat Security Data | RHEL/CentOS |
| Ubuntu CVE Tracker | Ubuntu packages |

## Python Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| `subprocess` | stdlib | Execute trivy CLI |
| `json` | stdlib | Parse scan results |
| `pathlib` | stdlib | File path handling |

## References

- Trivy Documentation: https://trivy.dev/docs/
- Trivy GitHub: https://github.com/aquasecurity/trivy
- Aqua Security: https://www.aquasec.com/products/trivy/

---

## Standards and Controls

## NIST SP 800-190 - Application Container Security Guide

### Relevant Controls
- **Image Vulnerability Management**: Organizations should maintain a pipeline for scanning and remediating container image vulnerabilities
- **Image Provenance**: Use content trust and signing to verify image source and integrity
- **SBOM Generation**: Produce Software Bill of Materials for all container images

## CIS Docker Benchmark v1.8.0

### Section 4: Container Images and Build File
- 4.4: Ensure images are scanned and rebuilt to include security patches
- 4.5: Ensure Content trust for Docker is Enabled
- 4.8: Ensure setuid and setgid permissions are removed

## NIST SSDF (Secure Software Development Framework)

### PW.4 - Reuse Existing, Well-Secured Software
- PW.4.1: Verify third-party software components have no known vulnerabilities
- PW.4.4: Verify software components are obtained from trusted sources

### RV.1 - Identify and Confirm Vulnerabilities
- RV.1.1: Gather information from vulnerability notifications
- RV.1.2: Review, analyze, and/or test code to identify vulnerabilities

## OWASP Container Security Verification Standard

### V2: Image Security
- 2.1: Verify images are scanned for known vulnerabilities before deployment
- 2.2: Verify base images are from trusted sources
- 2.3: Verify images do not contain embedded secrets
- 2.4: Verify unnecessary packages are removed from images
- 2.5: Verify images use minimal base (distroless/Alpine)

## Executive Order 14028 - Improving the Nation's Cybersecurity

### SBOM Requirements
- Software producers must provide SBOMs for federal software
- SBOMs must follow NTIA minimum elements
- Supported formats: SPDX, CycloneDX
- Trivy supports both SPDX and CycloneDX SBOM generation

## Trivy Vulnerability Scoring

### CVSS v3.1 Severity Mapping
| Score Range | Severity | Trivy Flag |
|-------------|----------|-----------|
| 9.0 - 10.0 | CRITICAL | --severity CRITICAL |
| 7.0 - 8.9 | HIGH | --severity HIGH |
| 4.0 - 6.9 | MEDIUM | --severity MEDIUM |
| 0.1 - 3.9 | LOW | --severity LOW |
| N/A | UNKNOWN | --severity UNKNOWN |

### Vulnerability Data Sources
| Source | Coverage |
|--------|----------|
| NVD | All CVEs |
| GHSA | GitHub ecosystem packages |
| Red Hat OVAL | RHEL, CentOS |
| Debian Security Tracker | Debian |
| Ubuntu CVE Tracker | Ubuntu |
| Alpine SecDB | Alpine Linux |
| Amazon ALAS | Amazon Linux |
| SUSE OVAL | SUSE/openSUSE |
| Wolfi SecDB | Wolfi/Chainguard |

---

## Workflows

## Workflow 1: Developer Local Scan

```
[Developer builds image] --> [trivy image myapp:latest]
         |                            |
         v                            v
    Fix Dockerfile              Review findings
    Update deps                      |
         |                    +------+------+
         |                    |             |
         v                    v             v
    Rebuild image       CRITICAL/HIGH    MEDIUM/LOW
         |               found?           found?
         |                 |               |
         v                 v               v
    Re-scan          Fix immediately   Add to backlog
                     before commit     or .trivyignore
```

## Workflow 2: CI/CD Gate Scan

```yaml
# Pipeline stages
Build --> Scan --> Gate Decision --> Deploy/Block

# Gate policy
CRITICAL: Block deployment, fail pipeline (exit-code 1)
HIGH: Block deployment to production
MEDIUM: Warn, allow deployment to staging
LOW: Informational only
```

## Workflow 3: Registry Continuous Scanning

```
[Images in Registry]
        |
        v
[Scheduled Trivy Scan (daily/weekly)]
        |
        +--> [New CVE detected in existing image]
        |            |
        |            v
        |     [Create JIRA/GitHub issue]
        |            |
        |            v
        |     [Rebuild and push patched image]
        |
        +--> [No new CVEs]
                     |
                     v
              [Log clean scan result]
```

## Workflow 4: Full SBOM + Vulnerability Pipeline

```bash
#!/bin/bash
IMAGE="myapp:v1.0.0"

# Step 1: Generate SBOM
trivy image --format cyclonedx --output sbom.cdx.json "$IMAGE"

# Step 2: Vulnerability scan
trivy image --format json --output vuln-report.json "$IMAGE"

# Step 3: License scan
trivy image --scanners license --format json --output license-report.json "$IMAGE"

# Step 4: Secret scan
trivy image --scanners secret --format json --output secret-report.json "$IMAGE"

# Step 5: Config scan (if Dockerfile available)
trivy config --format json --output config-report.json Dockerfile

# Step 6: Generate HTML report
trivy image --format template \
  --template "@contrib/html.tpl" \
  --output report.html "$IMAGE"

# Step 7: Upload to dependency tracking (e.g., Dependency-Track)
curl -X POST "https://dtrack.example.com/api/v1/bom" \
  -H "X-Api-Key: $DTRACK_API_KEY" \
  -F "project=$PROJECT_UUID" \
  -F "bom=@sbom.cdx.json"
```

## Workflow 5: Multi-Image Fleet Scanning

```bash
#!/bin/bash
# Scan all images in a Kubernetes cluster

# Get unique images
IMAGES=$(kubectl get pods --all-namespaces -o jsonpath='{range .items[*]}{range .spec.containers[*]}{.image}{"\n"}{end}{end}' | sort -u)

echo "Scanning $(echo "$IMAGES" | wc -l) unique images..."

for IMAGE in $IMAGES; do
  echo "=== Scanning: $IMAGE ==="
  trivy image --severity CRITICAL,HIGH --exit-code 0 \
    --format json --output "scan_$(echo $IMAGE | tr '/:' '_').json" \
    "$IMAGE" 2>/dev/null
done

# Aggregate results
echo "Generating aggregate report..."
python3 aggregate_trivy_results.py scan_*.json > fleet_report.json
```

## Workflow 6: Trivy Operator for Kubernetes

```yaml
# Install Trivy Operator via Helm
# helm install trivy-operator aquasecurity/trivy-operator \
#   --namespace trivy-system --create-namespace

# VulnerabilityReport is created automatically for each workload
apiVersion: aquasecurity.github.io/v1alpha1
kind: VulnerabilityReport
metadata:
  name: pod-myapp-myapp
  namespace: default
spec:
  scanner:
    name: Trivy
    version: 0.50.0
report:
  summary:
    criticalCount: 2
    highCount: 5
    mediumCount: 12
    lowCount: 8
```

---

## Working Template

## Scan Information

| Field | Value |
|-------|-------|
| Image | |
| Tag/Digest | |
| Scan Date | |
| Trivy Version | |
| DB Version | |
| Scanners Used | vuln / misconfig / secret / license |

## Vulnerability Summary

| Severity | Count | Threshold | Status |
|----------|-------|-----------|--------|
| CRITICAL | | 0 | PASS/FAIL |
| HIGH | | 5 | PASS/FAIL |
| MEDIUM | | 20 | PASS/FAIL |
| LOW | | N/A | INFO |
| UNKNOWN | | N/A | INFO |

## Critical Findings

| CVE ID | Package | Installed | Fixed | CVSS | Description |
|--------|---------|-----------|-------|------|-------------|
| | | | | | |

## High Findings

| CVE ID | Package | Installed | Fixed | CVSS | Description |
|--------|---------|-----------|-------|------|-------------|
| | | | | | |

## Secrets Detected

| Rule ID | Category | Severity | File | Match (redacted) |
|---------|----------|----------|------|------------------|
| | | | | |

## Misconfigurations

| ID | Type | Severity | Title | Resolution |
|----|------|----------|-------|------------|
| | | | | |

## SBOM Summary

| Package Type | Count |
|-------------|-------|
| OS packages | |
| Python packages | |
| Node.js packages | |
| Go modules | |
| Java libraries | |

## Policy Decision

- [ ] APPROVED for deployment
- [ ] BLOCKED - requires remediation
- [ ] EXCEPTION GRANTED (see risk acceptance below)

## Risk Acceptance (if applicable)

| CVE ID | Justification | Expiry Date | Approved By |
|--------|--------------|-------------|-------------|
| | | | |

## Remediation Actions

| Priority | CVE/Finding | Action | Owner | ETA |
|----------|-------------|--------|-------|-----|
| P1 | | | | |
| P2 | | | | |
