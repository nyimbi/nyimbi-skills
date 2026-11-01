# Detecting Container Drift At Runtime

## API Reference

## Docker SDK for Python

```python
import docker
client = docker.from_env()

# List running containers
containers = client.containers.list()

# Get container details
container = client.containers.get("container_id")
container.attrs         # full inspection dict
container.image.id      # image SHA256
container.image.tags    # ['app:v1.0']

# Filesystem diff (vs original image)
diff = container.diff()
# Returns: [{"Path": "/tmp/new_file", "Kind": 1}]
# Kind: 0=Modified, 1=Added, 2=Deleted

# Container inspection fields
container.attrs["HostConfig"]["Privileged"]       # bool
container.attrs["HostConfig"]["ReadonlyRootfs"]   # bool
container.attrs["Config"]["Image"]                # image reference
```

## Docker CLI Commands

```bash
# Filesystem changes since creation
docker diff <container>     # A=Added, C=Changed, D=Deleted

# Running processes
docker top <container> -eo pid,user,comm,args

# Image digest verification
docker inspect --format='{{.Image}}' <container>
```

## Falco Drift Detection Rules

```yaml
# Detect binary not in original image
condition: spawned_process and container and proc.is_exe_upper_layer = true

# Detect package manager usage
condition: spawned_process and container and proc.name in (apt, yum, pip, npm)

# Detect shell spawn
condition: spawned_process and container and proc.name in (bash, sh, dash)
```

## Kubernetes Security Context

```yaml
securityContext:
  readOnlyRootFilesystem: true     # prevent drift
  allowPrivilegeEscalation: false
  runAsNonRoot: true
  capabilities:
    drop: ["ALL"]
```

## Drift Severity Classification

| Indicator | Severity |
|-----------|----------|
| Privileged container | CRITICAL |
| Sensitive file modified (/etc/shadow) | CRITICAL |
| Binary added to system path | HIGH |
| Package manager executed | HIGH |
| Root shell active | MEDIUM |
| Mutable root filesystem | MEDIUM |

## CLI Usage

```bash
python agent.py --container my-app-container
python agent.py --container abc123 --all
```

---

## Standards and Controls

## Industry Standards

### NIST SP 800-190: Application Container Security Guide
- Section 3.3: Containers modified at runtime indicate compromise
- Section 4.2: Monitor containers for unauthorized changes
- Recommends treating containers as immutable infrastructure

### CIS Kubernetes Benchmark v1.9
- Control 5.2.8: Minimize container readOnlyRootFilesystem
- Control 5.7.3: Apply security contexts to pods
- Control 5.7.4: Default namespace restrictions

### MITRE ATT&CK for Containers
- T1610: Deploy Container -- unauthorized container deployment
- T1611: Escape to Host -- container boundary violation
- T1059.004: Unix Shell execution in containers
- T1105: Ingress Tool Transfer -- downloading tools into containers

## Compliance Mapping

| Requirement | Framework | Drift Detection Capability |
|-------------|-----------|--------------------------|
| Change detection | PCI DSS 11.5 | File integrity monitoring in containers |
| Unauthorized software | SOC 2 CC6.8 | Binary execution drift alerts |
| Configuration management | ISO 27001 A.12.1 | Image digest verification |
| Incident detection | NIST CSF DE.CM-7 | Runtime behavioral anomaly detection |

---

## Workflows

## Detection Workflow

1. Container image deployed with known-good state
2. Runtime monitor (Falco/Sysdig) tracks all process executions and file changes
3. Events compared against baseline: original image manifest + expected runtime behavior
4. Drift events classified by severity (binary drift = HIGH, config drift = MEDIUM)
5. Alerts sent to SIEM/SOC with full container context
6. Automated response: isolate pod network, capture forensics, evict pod

## Implementation Phases

### Phase 1: Visibility (Weeks 1-2)
- Deploy Falco with drift detection rules in alert-only mode
- Collect baseline of normal container behavior per workload
- Identify legitimate runtime changes (log files, temp files, caches)
- Create allowlists for expected runtime modifications

### Phase 2: Detection (Weeks 3-4)
- Enable drift detection alerts with tuned thresholds
- Integrate with SIEM for correlation and dashboarding
- Build runbooks for drift investigation
- Conduct tabletop exercises with container drift scenarios

### Phase 3: Prevention (Weeks 5-8)
- Enable readOnlyRootFilesystem on all production workloads
- Deploy Pod Security Standards in enforce mode
- Implement image digest pinning in all manifests
- Enable automated pod eviction for confirmed drift events

## Incident Response for Drift Events

1. **Triage**: Is the drift from a legitimate operation or potential compromise?
2. **Contain**: Apply NetworkPolicy deny-all to affected pod
3. **Collect**: Capture container filesystem diff, process tree, network connections
4. **Analyze**: Compare drifted files against malware signatures and IoCs
5. **Remediate**: Delete compromised pod, scan all pods in namespace
6. **Recover**: Deploy clean image, verify no persistence mechanisms

---

## Working Template

## Environment

| Field | Value |
|-------|-------|
| Cluster Name | |
| Namespaces Assessed | |
| Detection Tool | |
| Assessment Date | |

## Drift Detection Coverage

- [ ] Binary execution monitoring enabled
- [ ] File system change monitoring enabled
- [ ] Package manager usage detection enabled
- [ ] Image digest verification enabled
- [ ] ReadOnlyRootFilesystem enforced
- [ ] Pod Security Standards in enforce mode

## Findings Summary

| Severity | Count | Remediated |
|----------|-------|-----------|
| Critical | | |
| High | | |
| Medium | | |
| Low | | |

## Sign-Off

| Role | Name | Date |
|------|------|------|
| Security Engineer | | |
| Platform Lead | | |
