# Detecting Privilege Escalation In kubernetes Pods

## API Reference

## Security Context Checks

| Check | Risk | Description |
|-------|------|-------------|
| privileged: true | CRITICAL | Full host access |
| allowPrivilegeEscalation | HIGH | setuid escalation |
| runAsUser: 0 | HIGH | Running as root |
| hostPID: true | CRITICAL | Host PID namespace |
| hostNetwork: true | HIGH | Host network access |

## Dangerous Capabilities

| Capability | Risk |
|------------|------|
| SYS_ADMIN | Container escape |
| SYS_PTRACE | Process debugging |
| SYS_MODULE | Kernel module loading |
| NET_ADMIN | Network manipulation |

## kubectl Audit Commands

```bash
kubectl get pods -A -o json | jq '.items[] | select(.spec.containers[].securityContext.privileged==true)'
kubectl auth can-i --list --as=system:serviceaccount:ns:sa
```

## Pod Security Standards

```yaml
apiVersion: v1
kind: Namespace
metadata:
  labels:
    pod-security.kubernetes.io/enforce: restricted
```

## Falco Rules

```yaml
- rule: Pod with Privileged Container
  condition: kevt and kcreate and container.privileged=true
  priority: CRITICAL
```

## CLI Usage

```bash
python agent.py --namespace default
python agent.py --json-file pods.json
```

---

## Standards and Controls

## MITRE ATT&CK for Containers

| Technique | ID | Description |
|-----------|-----|-------------|
| Escape to Host | T1611 | Container breakout via privilege escalation |
| Exploitation for Privilege Escalation | T1068 | Kernel exploit from container |
| Abuse Elevation Control | T1548 | Setuid/setgid binary exploitation |
| Valid Accounts | T1078 | Service account token theft |
| Create Account | T1136 | Modify /etc/passwd in container |

## CIS Kubernetes Benchmark v1.8
- 5.2.1-5.2.9: Pod Security Standards
- 5.7.3: Apply security context to pods

## NIST SP 800-190
- Section 4.3: Container runtime vulnerabilities
- Section 5.4: Runtime monitoring for privilege escalation

## Pod Security Standards

| Profile | Level | Key Restrictions |
|---------|-------|-----------------|
| Privileged | Unrestricted | No restrictions |
| Baseline | Minimally restrictive | No privileged, no hostPID/hostNetwork |
| Restricted | Heavily restricted | Non-root, drop all caps, no privilege escalation |

---

## Workflows

## Phase 1: Assess Current State
```bash
# Find privileged pods
kubectl get pods -A -o json | jq '[.items[] | select(.spec.containers[].securityContext.privileged==true) | {name:.metadata.name, ns:.metadata.namespace}]'

# Find pods running as root
kubectl get pods -A -o json | jq '[.items[] | select(.spec.securityContext.runAsUser==0 or .spec.containers[].securityContext.runAsUser==0) | {name:.metadata.name, ns:.metadata.namespace}]'

# Find hostPath mounts
kubectl get pods -A -o json | jq '[.items[] | select(.spec.volumes[]?.hostPath!=null) | {name:.metadata.name, ns:.metadata.namespace}]'
```

## Phase 2: Deploy Prevention
1. Apply Pod Security Admission labels to namespaces
2. Deploy OPA Gatekeeper constraints
3. Test with non-compliant pods (should be rejected)

## Phase 3: Deploy Detection
1. Install Falco with privilege escalation rules
2. Enable Kubernetes audit logging
3. Configure alerts to SIEM

## Phase 4: Respond to Alerts
1. Identify compromised pod
2. Check container security context
3. Review process list and capabilities
4. Isolate with network policy
5. Capture forensic data
6. Delete compromised pod

---

## Working Template

## Prevention Controls
- [ ] Pod Security Admission set to restricted on production namespaces
- [ ] OPA Gatekeeper constraints block privileged containers
- [ ] Default security context enforced via mutation webhook
- [ ] Dangerous capabilities blocked at admission

## Detection Controls
- [ ] Falco rules deployed for privilege escalation patterns
- [ ] Kubernetes audit logging enabled
- [ ] Alerts configured for CRITICAL findings
- [ ] Regular cluster scans scheduled

## Dangerous Configurations to Block

| Configuration | Risk Level | PSA Profile |
|--------------|------------|-------------|
| privileged: true | CRITICAL | Baseline blocks |
| hostPID: true | CRITICAL | Baseline blocks |
| hostNetwork: true | HIGH | Baseline blocks |
| allowPrivilegeEscalation: true | HIGH | Restricted blocks |
| runAsUser: 0 | HIGH | Restricted blocks |
| capabilities.add: SYS_ADMIN | CRITICAL | Restricted blocks |
| hostPath volumes | HIGH | Restricted blocks |
| automountServiceAccountToken: true | MEDIUM | Manual |
