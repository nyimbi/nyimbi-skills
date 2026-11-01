# Performing Container Image Hardening

## API Reference

## Libraries Used

| Library | Purpose |
|---------|---------|
| `subprocess` | Execute Trivy, Docker, and hadolint CLI commands |
| `json` | Parse vulnerability scan and inspection results |
| `re` | Analyze Dockerfile instructions |
| `pathlib` | Handle Dockerfile and image paths |

## Installation

```bash
# Trivy vulnerability scanner
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin

# Hadolint Dockerfile linter
wget -O /usr/local/bin/hadolint https://github.com/hadolint/hadolint/releases/latest/download/hadolint-Linux-x86_64
chmod +x /usr/local/bin/hadolint

# Docker CLI (already installed in most environments)
```

## Trivy Image Scanning

### Scan Image for Vulnerabilities
```python
import subprocess
import json

def scan_image(image_name, severity="CRITICAL,HIGH"):
    cmd = [
        "trivy", "image",
        "--format", "json",
        "--severity", severity,
        "--exit-code", "0",
        image_name,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    return json.loads(result.stdout) if result.stdout else {}
```

### Scan for Secrets in Image
```python
def scan_secrets(image_name):
    cmd = [
        "trivy", "image",
        "--format", "json",
        "--scanners", "secret",
        image_name,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    return json.loads(result.stdout) if result.stdout else {}
```

### Scan for Misconfigurations
```python
def scan_misconfig(image_name):
    cmd = [
        "trivy", "image",
        "--format", "json",
        "--scanners", "misconfig",
        image_name,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    return json.loads(result.stdout) if result.stdout else {}
```

## Docker Image Inspection

### Inspect Image Metadata
```python
def inspect_image(image_name):
    cmd = ["docker", "inspect", image_name]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    data = json.loads(result.stdout)[0]
    config = data.get("Config", {})
    return {
        "image": image_name,
        "user": config.get("User", "root"),
        "exposed_ports": list(config.get("ExposedPorts", {}).keys()),
        "env_vars": config.get("Env", []),
        "entrypoint": config.get("Entrypoint"),
        "cmd": config.get("Cmd"),
        "labels": config.get("Labels", {}),
        "layers": len(data.get("RootFS", {}).get("Layers", [])),
        "size_mb": round(data.get("Size", 0) / 1048576, 1),
    }
```

### Check for Root User
```python
def check_non_root(image_name):
    inspection = inspect_image(image_name)
    user = inspection["user"]
    return {
        "image": image_name,
        "runs_as_root": user in ("", "root", "0"),
        "user": user or "root (default)",
        "severity": "high" if user in ("", "root", "0") else "pass",
    }
```

## Hadolint Dockerfile Linting

```python
def lint_dockerfile(dockerfile_path):
    cmd = [
        "hadolint",
        "--format", "json",
        str(dockerfile_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    findings = json.loads(result.stdout) if result.stdout else []
    return [
        {
            "line": f["line"],
            "code": f["code"],
            "level": f["level"],
            "message": f["message"],
        }
        for f in findings
    ]
```

## Hardening Checks

### Common Dockerfile Issues
```python
def audit_dockerfile(dockerfile_path):
    findings = []
    with open(dockerfile_path) as f:
        lines = f.readlines()

    has_user = False
    has_healthcheck = False

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("USER") and stripped.split()[-1] not in ("root", "0"):
            has_user = True
        if stripped.startswith("HEALTHCHECK"):
            has_healthcheck = True
        if stripped.startswith("FROM") and ":latest" in stripped:
            findings.append({
                "line": i, "severity": "medium",
                "issue": "Using :latest tag — pin specific version",
            })
        if "ADD" in stripped and ("http://" in stripped or "https://" in stripped):
            findings.append({
                "line": i, "severity": "high",
                "issue": "ADD with remote URL — use COPY + curl for verification",
            })

    if not has_user:
        findings.append({"line": 0, "severity": "high", "issue": "No USER instruction — runs as root"})
    if not has_healthcheck:
        findings.append({"line": 0, "severity": "low", "issue": "No HEALTHCHECK instruction"})

    return findings
```

## Output Format

```json
{
  "image": "myapp:v1.2.3",
  "vulnerabilities": {
    "critical": 2,
    "high": 8,
    "medium": 15,
    "low": 23
  },
  "runs_as_root": false,
  "size_mb": 142.5,
  "layers": 12,
  "dockerfile_issues": 3,
  "secrets_found": 0,
  "findings": [
    {
      "type": "vulnerability",
      "package": "openssl",
      "installed": "3.0.2",
      "fixed": "3.0.13",
      "severity": "CRITICAL",
      "cve": "CVE-2024-0727"
    }
  ]
}
```

---

## Standards and Controls

## CIS Docker Benchmark v1.6.0 - Image Controls

- 4.1: Create a user for the container
- 4.2: Use trusted base images
- 4.3: Do not install unnecessary packages
- 4.4: Scan and rebuild images for security patches
- 4.6: Add HEALTHCHECK instruction
- 4.7: Do not use update instructions alone
- 4.9: Use COPY instead of ADD
- 4.10: Do not store secrets in Dockerfiles
- 4.11: Install verified packages only

## NIST SP 800-190 Application Container Security Guide

### Image Hardening (Section 4.1)
- Use minimal base images to reduce attack surface
- Remove unnecessary tools, shells, and package managers
- Scan images for vulnerabilities before deployment
- Sign images for integrity verification

## OWASP Docker Security Cheat Sheet

- Use multi-stage builds
- Run as non-root user
- Use read-only root filesystem
- Pin base images to digests
- Drop all Linux capabilities
- Enable seccomp profile

---

## Workflows

## Hardening Pipeline

```
Base Image Selection
       │
       ▼
┌──────────────────┐
│ Multi-Stage Build │
│ (builder + prod)  │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Remove Packages  │
│ + Set User/Perms │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Trivy Scan       │
│ + Hadolint       │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ CIS Benchmark    │
│ Validation       │
└──────────────────┘
```

## Base Image Selection Guide

| Base Image | Size | Use Case | Packages |
|------------|------|----------|----------|
| scratch | 0 MB | Static Go/Rust binaries | None |
| distroless/static | 2 MB | Static binaries + CA certs | ca-certificates |
| distroless/base | 20 MB | Dynamic binaries | glibc, libssl |
| alpine:3.19 | 7 MB | General minimal | musl, busybox |
| debian:bookworm-slim | 80 MB | Debian ecosystem | apt, glibc |
| ubuntu:24.04 | 78 MB | Ubuntu ecosystem | apt, glibc |

## Dockerfile Hardening Checklist

- [ ] Multi-stage build separates build and runtime
- [ ] Minimal base image selected
- [ ] Non-root USER instruction present
- [ ] HEALTHCHECK instruction defined
- [ ] Base image pinned by digest
- [ ] COPY used instead of ADD
- [ ] No secrets in ENV or ARG
- [ ] Package cache cleaned (rm -rf /var/lib/apt/lists/*)
- [ ] Unnecessary packages removed
- [ ] setuid/setgid bits cleared
- [ ] Shell removed (if not needed)

---

## Working Template

## Hardened Python Dockerfile

```dockerfile
FROM python:3.12-slim-bookworm AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim-bookworm AS production
RUN apt-get update && apt-get install -y --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/* && \
    groupadd -r appuser && useradd -r -g appuser -s /sbin/nologin appuser && \
    find / -perm /6000 -type f -exec chmod a-s {} + 2>/dev/null || true
COPY --from=builder /install /usr/local
COPY --chown=appuser:appuser src/ /app/src/
USER appuser
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1
EXPOSE 8080
ENTRYPOINT ["python", "-m", "src.main"]
```

## Hardened Go Dockerfile (Distroless)

```dockerfile
FROM golang:1.22 AS builder
WORKDIR /app
COPY go.* ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o /server .

FROM gcr.io/distroless/static-debian12:nonroot
COPY --from=builder /server /server
USER nonroot:nonroot
ENTRYPOINT ["/server"]
```

## Hadolint Configuration

```yaml
# .hadolint.yaml
ignored:
  - DL3008  # Pin versions in apt-get (use --no-install-recommends instead)
trustedRegistries:
  - docker.io
  - gcr.io
  - ghcr.io
```
