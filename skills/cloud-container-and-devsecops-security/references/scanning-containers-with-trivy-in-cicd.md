# Scanning Containers With Trivy In CICD

## API Reference

## Trivy CLI Commands

| Command | Description |
|---------|-------------|
| `trivy image <ref>` | Scan container image for vulnerabilities |
| `trivy config <path>` | Scan Dockerfiles/IaC for misconfigurations |
| `trivy fs <path>` | Scan filesystem for vulnerabilities |
| `trivy sbom <file>` | Scan existing SBOM for vulnerabilities |
| `trivy image --format sarif` | SARIF output for GitHub Security |
| `trivy image --format cyclonedx` | CycloneDX SBOM generation |
| `trivy image --exit-code 1` | Non-zero exit on findings |

## Scan Options

| Flag | Description |
|------|-------------|
| `--severity CRITICAL,HIGH` | Filter by severity level |
| `--ignore-unfixed` | Skip CVEs without patches |
| `--scanners vuln,misconfig,secret` | Select scanner types |
| `--format json/sarif/cyclonedx` | Output format |
| `--exit-code 1` | Fail pipeline on findings |
| `--skip-db-update` | Use cached vulnerability DB |
| `--cache-dir <path>` | Set database cache directory |

## CI/CD Integration

| Platform | Method |
|----------|--------|
| GitHub Actions | `aquasecurity/trivy-action@v0.28.0` |
| GitLab CI | `aquasec/trivy:latest` Docker image |
| Jenkins | Trivy CLI in pipeline script |
| Azure DevOps | Trivy CLI task |

## Quality Gate Severities

| Level | CVSS Range | Default Gate Action |
|-------|-----------|-------------------|
| CRITICAL | 9.0 - 10.0 | Block deployment |
| HIGH | 7.0 - 8.9 | Block deployment |
| MEDIUM | 4.0 - 6.9 | Warn |
| LOW | 0.1 - 3.9 | Allow |

## Python Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| `subprocess` | stdlib | Execute trivy CLI |
| `json` | stdlib | Parse scan results |
| `pathlib` | stdlib | Output file management |

## References

- Trivy Documentation: https://trivy.dev/docs/
- Trivy GitHub Action: https://github.com/aquasecurity/trivy-action
- Trivy GitHub: https://github.com/aquasecurity/trivy

---

## Standards and Controls

## NIST SP 800-190 - Application Container Security Guide

### Image Vulnerabilities (Section 3.1)
- Scan all container images for known vulnerabilities before deployment
- Establish organizational policies for maximum acceptable vulnerability severity
- Monitor images in registries for newly discovered vulnerabilities
- Maintain an up-to-date vulnerability database for scanning tools

### Image Configuration Defects (Section 3.2)
- Verify images follow CIS Docker Benchmark configuration guidelines
- Ensure images run as non-root users unless operationally required
- Remove unnecessary packages, shells, and utilities from production images

## CIS Docker Benchmark v1.6.0

### Image Level Controls
- 4.1: Ensure a user for the container has been created (maps to Trivy DS002)
- 4.2: Ensure containers use trusted base images
- 4.3: Ensure unnecessary packages are not installed in the container
- 4.6: Ensure HEALTHCHECK instructions have been added (maps to Trivy DS026)
- 4.7: Ensure update instructions are not used alone in the Dockerfile
- 4.9: Ensure COPY is used instead of ADD in Dockerfiles (maps to Trivy DS005)

## OWASP Docker Security Cheat Sheet

### Vulnerability Management
- Scan images in the CI/CD pipeline before pushing to registries
- Use `--ignore-unfixed` to focus on actionable vulnerabilities
- Implement SBOM generation for full component visibility
- Re-scan images on a schedule to catch newly published CVEs

### Dockerfile Security
- Use minimal base images (distroless, Alpine, slim variants)
- Pin base image versions with digest for reproducibility
- Run containers as non-root with explicit USER instruction
- Use multi-stage builds to exclude build tools from production images

## NIST SSDF (SP 800-218)

### PW.4: Reuse Existing, Well-Secured Software
- PW.4.1: Use automated tools to check for known vulnerabilities in dependencies
- Map to Trivy's OS package and language dependency scanning capabilities

### PS.1: Protect All Forms of Code
- PS.1.1: Store all forms of code in a code repository protected by access controls
- Container images in registries should be scanned and signed before use

## SLSA Framework Alignment

### Source Level
- Trivy filesystem scanning validates source dependencies before build
- Git repository scanning detects secrets and vulnerable dependencies in source

### Build Level
- Trivy image scanning validates the build output for vulnerabilities
- SBOM generation creates a verifiable bill of materials for the built artifact

### Deployment Level
- Admission controllers can verify Trivy scan results before pod scheduling
- Harbor registry integration enforces scan-before-pull policies

---

## Workflows

## Container Security Scanning Pipeline

```
Source Code Push
       │
       ▼
┌──────────────────┐
│ Build Docker      │
│ Image             │
└──────┬───────────┘
       │
       ├──────────────────────┐
       ▼                      ▼
┌──────────────┐    ┌──────────────┐
│ Trivy Image  │    │ Trivy Config │
│ Vuln Scan    │    │ Misconfig    │
└──────┬───────┘    └──────┬───────┘
       │                    │
       ▼                    ▼
┌──────────────┐    ┌──────────────┐
│ SARIF/JSON   │    │ Table/JSON   │
│ Output       │    │ Output       │
└──────┬───────┘    └──────┬───────┘
       │                    │
       └──────────┬─────────┘
                  ▼
       ┌──────────────────┐
       │ Quality Gate     │
       │ Evaluation       │
       └──────┬───────────┘
              │
    ┌─────────┴──────────┐
    ▼                    ▼
 PASS: Push to         FAIL: Block
 Registry + Tag        + Alert Team
       │
       ▼
┌──────────────┐
│ Generate     │
│ SBOM + Sign  │
└──────────────┘
```

## Trivy Scan Types Reference

### Image Scanning
```bash
# Full scan (OS + language packages)
trivy image --severity CRITICAL,HIGH --exit-code 1 myimage:tag

# OS packages only
trivy image --vuln-type os myimage:tag

# Language-specific packages only
trivy image --vuln-type library myimage:tag

# From Docker archive
trivy image --input image.tar
```

### Filesystem Scanning
```bash
# Scan project directory for vulnerable dependencies
trivy fs --severity HIGH,CRITICAL /path/to/project

# Scan specific lockfile
trivy fs --severity HIGH,CRITICAL requirements.txt
```

### Repository Scanning
```bash
# Scan remote git repository
trivy repo https://github.com/org/repo

# Scan specific branch
trivy repo --branch develop https://github.com/org/repo
```

### Configuration Scanning
```bash
# Scan Dockerfile and Kubernetes manifests
trivy config .

# Scan Terraform files
trivy config --tf-vars terraform.tfvars ./terraform/

# Scan Helm charts
trivy config ./charts/myapp/
```

## Output Format Options

| Format | Use Case | Flag |
|--------|----------|------|
| table | Human-readable terminal output | `--format table` |
| json | Programmatic processing and storage | `--format json` |
| sarif | GitHub Security tab upload | `--format sarif` |
| cyclonedx | SBOM generation (CycloneDX) | `--format cyclonedx` |
| spdx-json | SBOM generation (SPDX) | `--format spdx-json` |
| template | Custom report format | `--format template --template @template.tpl` |
| cosign-vuln | Cosign attestation format | `--format cosign-vuln` |

## Severity Threshold Matrix

| Environment | Block On | Ignore Unfixed | Rationale |
|-------------|----------|----------------|-----------|
| Development | CRITICAL | Yes | Fast feedback, focus on worst issues |
| Staging | CRITICAL, HIGH | Yes | Catch more issues before production |
| Production | CRITICAL, HIGH | No | Full visibility even for unfixed CVEs |
| Compliance | ALL | No | Complete audit trail required |

## Database Management

### Database Update Strategy
```bash
# Download DB only (for caching)
trivy image --download-db-only --cache-dir /shared/trivy-cache

# Skip DB update (use cached)
trivy image --skip-db-update --cache-dir /shared/trivy-cache myimage:tag

# Java DB for JAR scanning
trivy image --download-java-db-only --cache-dir /shared/trivy-cache
```

### Cache Locations
- Default: `~/.cache/trivy/`
- CI override: `TRIVY_CACHE_DIR=/tmp/trivy-cache`
- GitHub Actions: Use `actions/cache` with key based on date

---

## Working Template

## GitHub Actions: Full Container Security Pipeline

```yaml
# .github/workflows/container-security.yml
name: Container Security

on:
  push:
    branches: [main]
  pull_request:
    paths: ['Dockerfile', 'docker-compose*.yml', 'src/**']

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-scan-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
      security-events: write

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build image
        uses: docker/build-push-action@v6
        with:
          context: .
          load: true
          tags: ${{ env.IMAGE_NAME }}:scan
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Cache Trivy DB
        uses: actions/cache@v4
        with:
          path: /tmp/trivy
          key: trivy-db-${{ github.run_id }}
          restore-keys: trivy-db-

      - name: Trivy vulnerability scan
        uses: aquasecurity/trivy-action@0.28.0
        with:
          image-ref: ${{ env.IMAGE_NAME }}:scan
          format: sarif
          output: trivy-vuln.sarif
          severity: CRITICAL,HIGH
          exit-code: '1'
          ignore-unfixed: true
          cache-dir: /tmp/trivy

      - name: Upload vulnerability SARIF
        if: always()
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: trivy-vuln.sarif
          category: trivy-vulnerabilities

      - name: Trivy misconfiguration scan
        uses: aquasecurity/trivy-action@0.28.0
        with:
          scan-type: config
          scan-ref: .
          format: sarif
          output: trivy-config.sarif
          severity: CRITICAL,HIGH
          exit-code: '1'

      - name: Upload config SARIF
        if: always()
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: trivy-config.sarif
          category: trivy-misconfigurations

      - name: Generate SBOM
        uses: aquasecurity/trivy-action@0.28.0
        with:
          image-ref: ${{ env.IMAGE_NAME }}:scan
          format: cyclonedx
          output: sbom.cdx.json

      - name: Upload SBOM artifact
        uses: actions/upload-artifact@v4
        with:
          name: sbom
          path: sbom.cdx.json

      - name: Login to GHCR
        if: github.event_name == 'push'
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Push image
        if: github.event_name == 'push'
        uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: |
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
```

## Trivy Ignore File Template

```yaml
# .trivyignore.yaml
vulnerabilities:
  # Accepted risk: mitigated at infrastructure level
  - id: CVE-YYYY-NNNNN
    statement: "Mitigated by WAF rules. Risk accepted by security team."
    expires: 2026-12-31

misconfigurations:
  # Init containers require root
  - id: DS002
    paths:
      - "docker/init/*.Dockerfile"
    statement: "Init containers need root for volume permissions"
```

## Secure Dockerfile Template

```dockerfile
# syntax=docker/dockerfile:1

# Build stage
FROM python:3.12-slim-bookworm AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Production stage
FROM python:3.12-slim-bookworm AS production

# Security: Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser -s /bin/false appuser

# Security: Install only runtime dependencies, remove cache
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application code
WORKDIR /app
COPY --chown=appuser:appuser src/ ./src/

# Security: Run as non-root
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1

EXPOSE 8080
ENTRYPOINT ["python", "-m", "src.main"]
```

## Trivy Operator for Kubernetes

```yaml
# Install Trivy Operator via Helm
# helm repo add aqua https://aquasecurity.github.io/helm-charts/
# helm install trivy-operator aqua/trivy-operator \
#   --namespace trivy-system --create-namespace \
#   --set trivy.severity=CRITICAL,HIGH

# Sample VulnerabilityReport CRD
apiVersion: aquasecurity.github.io/v1alpha1
kind: ClusterComplianceReport
metadata:
  name: cis-benchmark
spec:
  cron: "0 */6 * * *"
  compliance:
    id: cis
    title: CIS Kubernetes Benchmark
    platform: k8s
```
