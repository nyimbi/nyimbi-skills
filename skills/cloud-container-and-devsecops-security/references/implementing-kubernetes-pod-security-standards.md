# Implementing kubernetes Pod Security Standards

## API Reference

## PSA Namespace Labels

```bash
# Apply restricted enforcement
kubectl label namespace production \
  pod-security.kubernetes.io/enforce=restricted \
  pod-security.kubernetes.io/audit=restricted \
  pod-security.kubernetes.io/warn=restricted --overwrite
```

## Pod Security Standard Levels

| Level | Description | Blocks |
|-------|-------------|--------|
| Privileged | Unrestricted | Nothing |
| Baseline | Minimally restrictive | hostNetwork, privileged, hostPID/IPC |
| Restricted | Heavily restricted | + runAsNonRoot, drop ALL caps, seccomp |

## PSA Modes

| Mode | Behavior |
|------|----------|
| enforce | Reject violating pods |
| audit | Log violations (allow pod) |
| warn | Warn user (allow pod) |

## Baseline Violations

| Field | Forbidden Value |
|-------|----------------|
| `spec.hostNetwork` | true |
| `spec.hostPID` | true |
| `spec.hostIPC` | true |
| `containers[*].securityContext.privileged` | true |
| `containers[*].securityContext.capabilities.add` | Non-default |

## Restricted Violations (adds to Baseline)

| Field | Required |
|-------|----------|
| `runAsNonRoot` | true |
| `allowPrivilegeEscalation` | false |
| `capabilities.drop` | ["ALL"] |
| `seccompProfile.type` | RuntimeDefault or Localhost |

### References

- K8s PSS: https://kubernetes.io/docs/concepts/security/pod-security-standards/
- PSA: https://kubernetes.io/docs/concepts/security/pod-security-admission/
- Migrate from PSP: https://kubernetes.io/docs/tasks/configure-pod-container/migrate-from-psp/

---

## Standards and Controls

## Kubernetes Pod Security Standards (PSS) v1.31

### Privileged Profile
- No restrictions applied
- Used for: kube-system, monitoring agents, CNI plugins, storage drivers

### Baseline Profile Controls
| Control | Policy |
|---------|--------|
| HostProcess | Must be false |
| Host Namespaces | hostNetwork, hostPID, hostIPC must be false |
| Privileged Containers | Must be false |
| Capabilities | Cannot add beyond: AUDIT_WRITE, CHOWN, DAC_OVERRIDE, FOWNER, FSETID, KILL, MKNOD, NET_BIND_SERVICE, SETFCAP, SETGID, SETPCAP, SETUID, SYS_CHROOT |
| HostPath Volumes | Must not be used |
| Host Ports | Must not define hostPort |
| AppArmor | Must not set to unconfined |
| SELinux | type must be container_t, container_init_t, or container_kvm_t; user/role must not be set |
| /proc Mount Type | Must be Default |
| Seccomp | Must not set to Unconfined |
| Sysctls | Must only use safe sysctls |

### Restricted Profile Controls (in addition to Baseline)
| Control | Policy |
|---------|--------|
| Volume Types | Only: configMap, csi, downwardAPI, emptyDir, ephemeral, persistentVolumeClaim, projected, secret |
| Privilege Escalation | allowPrivilegeEscalation must be false |
| Running as Non-root | runAsNonRoot must be true |
| Running as Non-root User | runAsUser must be non-zero |
| Seccomp | Must be RuntimeDefault or Localhost |
| Capabilities | Must drop ALL; may only add NET_BIND_SERVICE |

## CIS Kubernetes Benchmark v1.8

### Section 5: Policies
- 5.1: RBAC and Service Accounts
- 5.2: Pod Security Standards
  - 5.2.1: Ensure PSA is not set to Privileged on non-system namespaces
  - 5.2.2: Minimize admission of privileged containers
  - 5.2.3: Minimize admission of containers wanting to share host process ID namespace
  - 5.2.4: Minimize admission of containers wanting to share host IPC namespace
  - 5.2.5: Minimize admission of containers wanting to share host network namespace
  - 5.2.6: Minimize admission of containers with allowPrivilegeEscalation
  - 5.2.7: Minimize admission of root containers
  - 5.2.8: Minimize admission of containers with NET_RAW capability
  - 5.2.9: Minimize admission of containers with added capabilities
  - 5.2.10: Minimize admission of containers with capabilities assigned
  - 5.2.11: Minimize admission of containers with HostProcess
  - 5.2.12: Minimize admission of HostPath volumes
  - 5.2.13: Minimize admission of containers with unrestricted Seccomp profile

## NSA/CISA Kubernetes Hardening Guide

### Pod Security Recommendations
- Use PSA in enforce mode for production namespaces
- Set restricted profile as default for all non-system namespaces
- Require seccomp profiles on all pods
- Prevent privileged containers in all workload namespaces
- Require non-root user for all containers
- Drop all capabilities and only add NET_BIND_SERVICE if needed

## MITRE ATT&CK for Containers

### Techniques Prevented by Restricted Profile
| Technique | PSS Control |
|-----------|------------|
| T1611 - Escape to Host | Blocks privileged, hostPID, hostNetwork |
| T1610 - Deploy Container | Blocks privileged containers |
| T1053 - Scheduled Task | Blocks host namespace access |
| T1548 - Abuse Elevation Control | Blocks allowPrivilegeEscalation |

---

## Workflows

## Workflow 1: PSS Migration from PodSecurityPolicy

```
[Identify PSP usage] --> [Map PSP to PSS levels] --> [Apply audit/warn labels]
        |                        |                           |
        v                        v                           v
  kubectl get psp          Privileged PSP -> baseline    Monitor audit logs
  List all namespaces      Restrictive PSP -> restricted  for 2-4 weeks
        |                        |                           |
        +------------------------+---------------------------+
                                 |
                                 v
                    [Enable enforce mode per namespace]
                                 |
                                 v
                    [Remove PodSecurityPolicy resources]
                                 |
                                 v
                    [Disable PSP admission controller]
```

## Workflow 2: New Namespace Onboarding

```
Step 1: Classify workload sensitivity
  - System/Infrastructure -> Privileged (only kube-system)
  - General workloads -> Baseline + Restricted warnings
  - Production/Sensitive -> Restricted enforce

Step 2: Create namespace with labels
  kubectl create namespace $NS
  kubectl label namespace $NS \
    pod-security.kubernetes.io/enforce=$LEVEL \
    pod-security.kubernetes.io/audit=restricted \
    pod-security.kubernetes.io/warn=restricted

Step 3: Test with dry-run
  kubectl run test --image=nginx -n $NS --dry-run=server

Step 4: Deploy workloads with compliant security contexts

Step 5: Validate enforcement
  kubectl get events -n $NS --field-selector reason=FailedCreate
```

## Workflow 3: CI/CD PSS Compliance Check

```yaml
# Pre-deployment validation
name: PSS Compliance Check
on: pull_request

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install kubescape
        run: curl -s https://raw.githubusercontent.com/kubescape/kubescape/master/install.sh | /bin/bash

      - name: Scan manifests for PSS restricted compliance
        run: |
          kubescape scan framework nsa \
            --controls-config controls.json \
            --format junit --output results.xml \
            k8s-manifests/

      - name: Validate security contexts
        run: |
          for file in k8s-manifests/*.yaml; do
            echo "Checking $file..."
            # Verify runAsNonRoot
            if ! grep -q "runAsNonRoot: true" "$file"; then
              echo "FAIL: Missing runAsNonRoot in $file"
              exit 1
            fi
            # Verify drop ALL
            if ! grep -q "drop:" "$file" || ! grep -A1 "drop:" "$file" | grep -q "ALL"; then
              echo "FAIL: Missing drop ALL capabilities in $file"
              exit 1
            fi
          done
```

## Workflow 4: Violation Response

```
[PSA Violation Detected]
        |
        +-- enforce mode --> Pod rejected --> Alert developer
        |                                         |
        |                                         v
        |                                   Fix security context
        |                                   Re-deploy
        |
        +-- audit mode --> Pod allowed, audit log entry
        |                         |
        |                         v
        |                   Weekly audit review
        |                   Create remediation ticket
        |
        +-- warn mode --> Pod allowed, user warning
                                |
                                v
                          Developer sees warning
                          Fix before enforce rollout
```

---

## Working Template

## Namespace Classification

| Namespace | Current PSS Level | Target PSS Level | Migration Status |
|-----------|------------------|------------------|------------------|
| kube-system | privileged | privileged | N/A |
| production | | restricted | |
| staging | | baseline | |
| development | | baseline | |

## PSS Label Configuration

| Namespace | enforce | audit | warn | Version |
|-----------|---------|-------|------|---------|
| | | | | latest |

## Workload Compliance Checklist

### Pod Security Context
- [ ] runAsNonRoot: true
- [ ] runAsUser: non-zero (e.g., 65534)
- [ ] runAsGroup: non-zero
- [ ] fsGroup: appropriate group ID
- [ ] seccompProfile.type: RuntimeDefault

### Container Security Context
- [ ] allowPrivilegeEscalation: false
- [ ] readOnlyRootFilesystem: true
- [ ] capabilities.drop: ["ALL"]
- [ ] capabilities.add: only NET_BIND_SERVICE if needed
- [ ] privileged: false (or not set)

### Pod Spec
- [ ] automountServiceAccountToken: false (unless needed)
- [ ] No hostNetwork, hostPID, hostIPC
- [ ] No hostPath volumes
- [ ] No hostPort in container specs
- [ ] Resource requests and limits defined

## Migration Plan

| Phase | Action | Timeline | Status |
|-------|--------|----------|--------|
| 1 | Apply audit+warn labels | Week 1 | |
| 2 | Review audit violations | Week 2-3 | |
| 3 | Fix workload security contexts | Week 4-6 | |
| 4 | Enable baseline enforce | Week 7 | |
| 5 | Enable restricted enforce | Week 8 | |

## Exceptions

| Namespace | Workload | Required Level | Justification | Approved By |
|-----------|----------|---------------|---------------|-------------|
| | | | | |
