# Hardening docker Containers For Production

## API Reference

## Docker CLI

### List Containers
```bash
docker ps --format '{{json .}}'
```

### Inspect Container
```bash
docker inspect <container_id>
```

### Key Inspect Fields
| Path | Description |
|------|-------------|
| `.HostConfig.Privileged` | Privileged mode |
| `.HostConfig.NetworkMode` | Network namespace |
| `.HostConfig.CapAdd` | Added capabilities |
| `.HostConfig.ReadonlyRootfs` | Read-only filesystem |
| `.HostConfig.Memory` | Memory limit (bytes) |
| `.Config.User` | Container user |

## CIS Docker Benchmark Checks

| Check | Description | Severity |
|-------|-------------|----------|
| 4.1 | Non-root user | HIGH |
| 5.3 | Restrict capabilities | HIGH |
| 5.4 | No privileged containers | CRITICAL |
| 5.5 | No sensitive host mounts | HIGH |
| 5.10 | No host network | HIGH |
| 5.12 | Read-only root FS | MEDIUM |
| 5.13 | CPU limits set | LOW |
| 5.14 | Memory limits set | MEDIUM |

## Secure Dockerfile Practices

### Non-Root User
```dockerfile
FROM alpine:3.18
RUN adduser -D appuser
USER appuser
```

### Read-Only Filesystem
```bash
docker run --read-only --tmpfs /tmp:rw,noexec,nosuid myimage
```

### Drop Capabilities
```bash
docker run --cap-drop ALL --cap-add NET_BIND_SERVICE myimage
```

### Resource Limits
```bash
docker run --memory=512m --cpus=1.0 myimage
```

## Docker Bench Security

### Run Audit
```bash
docker run --rm --net host --pid host --userns host \
    --cap-add audit_control \
    -v /var/lib:/var/lib \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /etc:/etc \
    docker/docker-bench-security
```

## Seccomp and AppArmor

### Custom Seccomp Profile
```bash
docker run --security-opt seccomp=profile.json myimage
```

### AppArmor Profile
```bash
docker run --security-opt apparmor=docker-default myimage
```

---

## Standards and Controls

## CIS Docker Benchmark v1.8.0

### Section 1: Host Configuration
- 1.1.1: Ensure a separate partition for containers has been created
- 1.1.2: Ensure only trusted users are allowed to control Docker daemon
- 1.1.3-1.1.18: Ensure Docker daemon audit configuration

### Section 2: Docker Daemon Configuration
- 2.1: Run the Docker daemon as non-root user (rootless mode)
- 2.2: Ensure network traffic is restricted between containers (--icc=false)
- 2.3: Ensure logging level is set to info
- 2.4: Ensure Docker is allowed to make changes to iptables
- 2.5: Ensure insecure registries are not used
- 2.6: Ensure aufs storage driver is not used
- 2.7: Ensure TLS authentication for Docker daemon is configured
- 2.8: Ensure default ulimit is configured appropriately
- 2.9: Enable user namespace support
- 2.10: Ensure default cgroup usage has been confirmed
- 2.11: Ensure base device size is not changed until needed
- 2.12: Ensure centralized and remote logging is configured
- 2.13: Ensure live restore is enabled
- 2.14: Ensure Userland Proxy is disabled
- 2.15: Ensure daemon-wide custom seccomp profile is applied
- 2.16: Ensure experimental features are not used in production
- 2.17: Ensure containers are restricted from acquiring new privileges

### Section 4: Container Images and Build Files
- 4.1: Ensure that a user for the container has been created
- 4.2: Ensure containers use trusted base images
- 4.3: Ensure unnecessary packages are not installed
- 4.4: Ensure images are scanned for vulnerabilities
- 4.5: Ensure Content trust for Docker is enabled
- 4.6: Ensure HEALTHCHECK instructions have been added to container images
- 4.7: Ensure update instructions are not used alone in the Dockerfile
- 4.8: Ensure setuid and setgid permissions are removed
- 4.9: Ensure COPY is used instead of ADD
- 4.10: Ensure secrets are not stored in Dockerfiles
- 4.11: Ensure only verified packages are installed

### Section 5: Container Runtime
- 5.1: Ensure AppArmor profile is enabled
- 5.2: Ensure SELinux security options are set
- 5.3: Ensure Linux kernel capabilities are restricted
- 5.4: Ensure privileged containers are not used
- 5.5: Ensure sensitive host system directories are not mounted
- 5.6: Ensure sshd is not running within containers
- 5.7: Ensure privileged ports are not mapped within containers
- 5.8: Ensure only needed ports are open on the container
- 5.9: Ensure host network mode is not used
- 5.10: Ensure memory usage for container is limited
- 5.11: Ensure CPU priority is set appropriately
- 5.12: Ensure container root filesystem is mounted as read only
- 5.13: Ensure incoming container traffic is bound to a specific host interface
- 5.25: Ensure container is restricted from acquiring additional privileges

## NIST SP 800-190 - Application Container Security Guide

### Key Recommendations
- Use container-specific host OS (CoreOS, Flatcar, Bottlerocket)
- Segment container networks by sensitivity level
- Use container runtime with minimal attack surface
- Implement image signing and verification
- Harden container registries with access controls
- Monitor container runtime behavior for anomalies

## OWASP Docker Security Cheat Sheet

### Top Docker Security Risks
1. Unrestricted container access to host resources
2. Running containers in privileged mode
3. Running as root inside containers
4. Unverified or unscanned container images
5. Exposed Docker daemon socket
6. Insecure container networking
7. Secrets stored in images or environment variables
8. Missing resource limits
9. Outdated base images with known vulnerabilities
10. Insufficient logging and monitoring

---

## Workflows

## Workflow 1: New Container Hardening Pipeline

```
[Dockerfile Created] --> [Hadolint Lint] --> [Build Image] --> [Dockle Scan]
        |                      |                    |               |
        v                      v                    v               v
  Use multi-stage        Fix warnings         Tag with digest   Fix findings
  Non-root USER          No ADD, use COPY     Sign image        Remove setuid
  Minimal base           Pin versions         Push to registry  Drop caps
        |                      |                    |               |
        +----------+-----------+--------------------+               |
                   |                                                |
                   v                                                v
          [Trivy Vulnerability Scan] -----> [Docker Bench Assessment]
                   |                                    |
                   v                                    v
          Fix HIGH/CRITICAL CVEs              Remediate CIS failures
                   |                                    |
                   +------------------------------------+
                   |
                   v
          [Deploy to Production with Hardened Runtime Flags]
                   |
                   v
          [Continuous Monitoring with Falco]
```

## Workflow 2: Existing Container Remediation

```
Step 1: Assess Current State
  - Run docker-bench-security against host
  - Run Trivy scan against all running images
  - Audit all running containers for root users
  - Check daemon.json configuration

Step 2: Prioritize Remediation
  - Critical: Privileged containers, root users, exposed daemon socket
  - High: Missing seccomp profiles, no resource limits, capability escalation
  - Medium: Missing health checks, no content trust, excessive open ports
  - Low: Missing labels, audit rules, log rotation

Step 3: Apply Fixes
  - Update Dockerfiles with non-root users
  - Rebuild images with multi-stage builds
  - Update docker-compose or orchestrator configs
  - Configure daemon.json with TLS and security options

Step 4: Validate
  - Re-run docker-bench-security
  - Confirm score improvement
  - Document remaining accepted risks
```

## Workflow 3: CI/CD Integration

```yaml
# GitHub Actions hardening pipeline
name: Container Hardening Pipeline
on: [push]

jobs:
  lint-dockerfile:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hadolint/hadolint-action@v3.1.0
        with:
          dockerfile: Dockerfile

  build-and-scan:
    needs: lint-dockerfile
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build image
        run: docker build -t myapp:${{ github.sha }} .

      - name: Dockle lint
        uses: erzz/dockle-action@v1
        with:
          image: myapp:${{ github.sha }}
          failure-threshold: WARN

      - name: Trivy scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: myapp:${{ github.sha }}
          format: table
          exit-code: 1
          severity: CRITICAL,HIGH

      - name: Sign image with Cosign
        if: github.ref == 'refs/heads/main'
        uses: sigstore/cosign-installer@v3
        run: cosign sign --yes myapp:${{ github.sha }}
```

## Workflow 4: Runtime Hardening Checklist

```
Pre-deployment:
  [ ] Image built from minimal base (distroless/Alpine)
  [ ] Non-root USER specified in Dockerfile
  [ ] No secrets in image layers
  [ ] Image signed and verified
  [ ] Vulnerability scan shows no CRITICAL/HIGH CVEs
  [ ] Hadolint and Dockle pass with zero errors

Runtime configuration:
  [ ] --read-only flag enabled
  [ ] --cap-drop ALL with minimum cap-add
  [ ] --security-opt no-new-privileges:true
  [ ] --security-opt seccomp=<profile>
  [ ] --memory and --cpus limits set
  [ ] --pids-limit configured
  [ ] --user flag set to non-root UID
  [ ] --tmpfs for writable directories only
  [ ] Health check configured
  [ ] Restart policy set (on-failure with max retries)

Host configuration:
  [ ] Docker daemon TLS enabled
  [ ] Inter-container communication disabled (icc=false)
  [ ] User namespace remapping enabled
  [ ] Audit rules for Docker binaries and directories
  [ ] Docker socket not exposed to containers
```

---

## Working Template

## Project Information

| Field | Value |
|-------|-------|
| Application Name | |
| Docker Image | |
| Base Image | |
| Environment | Development / Staging / Production |
| Assessment Date | |
| Assessor | |

## Pre-Hardening Checklist

### Dockerfile Security
- [ ] Using minimal base image (distroless, Alpine, scratch)
- [ ] Specific image tag with digest pinning (not :latest)
- [ ] Multi-stage build implemented
- [ ] Non-root USER instruction present
- [ ] COPY used instead of ADD
- [ ] No secrets in Dockerfile or image layers
- [ ] HEALTHCHECK instruction present
- [ ] Unnecessary packages removed
- [ ] setuid/setgid binaries removed

### Daemon Configuration (/etc/docker/daemon.json)
- [ ] icc set to false
- [ ] TLS authentication enabled (tlsverify: true)
- [ ] Live restore enabled
- [ ] Userland proxy disabled
- [ ] no-new-privileges enabled
- [ ] Log rotation configured (max-size, max-file)
- [ ] Default ulimits configured
- [ ] Seccomp profile specified

### Runtime Security Flags
- [ ] --read-only enabled
- [ ] --cap-drop ALL applied
- [ ] Minimum --cap-add for required capabilities only
- [ ] --security-opt no-new-privileges:true
- [ ] --security-opt seccomp=<profile>
- [ ] --memory limit set
- [ ] --cpus limit set
- [ ] --pids-limit set
- [ ] --user set to non-root UID:GID
- [ ] --tmpfs for writable directories
- [ ] --network set to custom bridge (not host)
- [ ] --restart on-failure with max retries

### Host Security
- [ ] Separate partition for /var/lib/docker
- [ ] Docker group membership restricted
- [ ] Audit rules configured for Docker files
- [ ] Docker socket not exposed to containers
- [ ] Content Trust enabled (DOCKER_CONTENT_TRUST=1)

## Vulnerability Scan Results

### Trivy Scan
```
trivy image <image-name>
```

| Severity | Count | Action Required |
|----------|-------|----------------|
| CRITICAL | | Immediate fix |
| HIGH | | Fix before production |
| MEDIUM | | Plan remediation |
| LOW | | Accept or fix |

### Docker Bench Score
```
docker run --rm docker/docker-bench-security
```

| Section | Score | Notes |
|---------|-------|-------|
| Host Configuration | /10 | |
| Daemon Configuration | /10 | |
| Container Images | /10 | |
| Container Runtime | /10 | |
| Docker Security Ops | /10 | |

## Risk Acceptance

| Finding | Severity | Justification | Approved By | Date |
|---------|----------|---------------|-------------|------|
| | | | | |

## Remediation Plan

| Priority | Finding | Action | Owner | Target Date | Status |
|----------|---------|--------|-------|-------------|--------|
| P1 | | | | | |
| P2 | | | | | |
| P3 | | | | | |

## Sign-Off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Security Engineer | | | |
| DevOps Lead | | | |
| Application Owner | | | |
