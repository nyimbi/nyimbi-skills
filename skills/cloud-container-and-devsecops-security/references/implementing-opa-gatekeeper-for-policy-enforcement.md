# Implementing Opa Gatekeeper For Policy Enforcement

## API Reference

## OPA REST API (localhost:8181)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/data/{path}` | GET/POST | Query policy |
| `/v1/policies/{id}` | PUT | Create/update policy |
| `/v1/data` | POST | Evaluate input against policy |

## Gatekeeper CRDs

| CRD | Description |
|-----|-------------|
| `ConstraintTemplate` | Define policy schema + Rego |
| `Constraint` | Instantiate a template |
| `Config` | Audit/sync configuration |

## ConstraintTemplate Example
```yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredLabels
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels
        violation[{"msg": msg}] {
          not input.review.object.metadata.labels["app"]
          msg := "Missing required label: app"
        }
```

## Key Libraries

| Library | Use |
|---------|-----|
| `kubernetes` | K8s API client |
| `requests` | OPA REST queries |
| `subprocess` | kubectl commands |

---

## Standards and Controls

## Industry Standards

### NIST SP 800-190
- Section 4.1: Image vulnerabilities - Enforce image registry restrictions
- Section 4.2: Image configuration defects - Enforce security context requirements
- Section 5.2: Registry security - Restrict allowed image sources

### CIS Kubernetes Benchmark v1.8
- 5.2.1: Ensure Pods cannot run with privileged containers
- 5.2.2: Ensure Pods cannot share host PID namespace
- 5.2.3: Ensure Pods cannot share host IPC namespace
- 5.2.4: Ensure Pods cannot share host network namespace
- 5.2.5: Ensure containers do not allow privilege escalation
- 5.2.6: Ensure containers do not run as root
- 5.2.7: Ensure Pods use seccomp profile
- 5.2.8: Ensure Pods restrict volume types
- 5.2.9: Ensure Pods restrict host path volumes
- 5.7.1: Create administrative boundaries using namespaces
- 5.7.2: Ensure seccomp profile is set
- 5.7.3: Apply security context to pods

### NSA/CISA Kubernetes Hardening Guide
- Section 2: Pod Security - Admission control enforcement
- Recommends admission controllers to enforce security baselines

## Gatekeeper Policy Library

| Template | Purpose | CIS Mapping |
|----------|---------|-------------|
| K8sPSPPrivilegedContainer | Block privileged containers | 5.2.1 |
| K8sPSPHostNamespace | Block host PID/IPC/Network | 5.2.2-5.2.4 |
| K8sPSPAllowPrivilegeEscalation | Prevent privilege escalation | 5.2.5 |
| K8sPSPRunAsNonRoot | Require non-root | 5.2.6 |
| K8sPSPSeccomp | Require seccomp profiles | 5.2.7 |
| K8sPSPVolumeTypes | Restrict volume types | 5.2.8 |
| K8sPSPHostFilesystem | Restrict hostPath | 5.2.9 |
| K8sAllowedRepos | Restrict image registries | 5.1.1 |
| K8sRequiredLabels | Enforce labeling standards | Organizational |
| K8sContainerLimits | Enforce resource limits | Operational |

## Compliance Mappings

### PCI DSS v4.0
- Req 2.2: Secure system components per configuration standards
- Req 6.3.2: Develop software securely with automated controls

### SOC 2
- CC6.1: Logical access to system components is restricted
- CC8.1: Changes to infrastructure are controlled

---

## Workflows

## Phase 1: Install Gatekeeper

```bash
helm repo add gatekeeper https://open-policy-agent.github.io/gatekeeper/charts
helm repo update
helm install gatekeeper gatekeeper/gatekeeper \
  --namespace gatekeeper-system --create-namespace \
  --set replicas=3 --set audit.replicas=1

kubectl -n gatekeeper-system rollout status deployment/gatekeeper-controller-manager
```

## Phase 2: Deploy ConstraintTemplates

```bash
# Clone Gatekeeper policy library
git clone https://github.com/open-policy-agent/gatekeeper-library.git

# Apply common templates
kubectl apply -f gatekeeper-library/library/pod-security-policy/privileged-containers/template.yaml
kubectl apply -f gatekeeper-library/library/pod-security-policy/host-namespaces/template.yaml
kubectl apply -f gatekeeper-library/library/pod-security-policy/allow-privilege-escalation/template.yaml
kubectl apply -f gatekeeper-library/library/general/allowedrepos/template.yaml
kubectl apply -f gatekeeper-library/library/general/requiredlabels/template.yaml
kubectl apply -f gatekeeper-library/library/general/containerlimits/template.yaml
```

## Phase 3: Deploy Constraints in Dryrun Mode

```bash
kubectl apply -f - <<EOF
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sPSPPrivilegedContainer
metadata:
  name: block-privileged-dryrun
spec:
  enforcementAction: dryrun
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
    excludedNamespaces:
      - kube-system
      - gatekeeper-system
EOF
```

## Phase 4: Review Audit Violations

```bash
# Check violations for each constraint
kubectl get constraints -o json | jq '.items[] | {
  name: .metadata.name,
  enforcement: .spec.enforcementAction,
  violations: (.status.violations // [] | length),
  total_violations: .status.totalViolations
}'

# Get detailed violations
kubectl get k8spsprivilegedcontainer block-privileged-dryrun -o json | jq '.status.violations[]'
```

## Phase 5: Switch to Enforcement

```bash
# After reviewing violations and remediating, switch to deny
kubectl patch k8spsprivilegedcontainer block-privileged-dryrun \
  --type=merge -p '{"spec":{"enforcementAction":"deny"}}'
```

## Phase 6: Test Enforcement

```bash
# This should be denied
kubectl run test-priv --image=nginx --overrides='{"spec":{"containers":[{"name":"test","image":"nginx","securityContext":{"privileged":true}}]}}'
# Expected: Error from server (Forbidden): admission webhook denied the request

kubectl delete pod test-priv --ignore-not-found
```

## Phase 7: Monitor and Maintain

```bash
# Regular audit check
kubectl get constraints -o wide

# Check Gatekeeper health
kubectl get pods -n gatekeeper-system
kubectl logs -n gatekeeper-system -l control-plane=controller-manager --tail=20
```

---

## Working Template

## Policy Rollout Plan

### Pre-Deployment
- [ ] Policy reviewed and approved by security team
- [ ] Rego logic tested with `opa test`
- [ ] ConstraintTemplate syntax validated
- [ ] Exempt namespaces identified

### Deployment Steps
1. [ ] Deploy ConstraintTemplate to cluster
2. [ ] Verify CRD created: `kubectl get crd`
3. [ ] Deploy Constraint in `dryrun` mode
4. [ ] Wait 24 hours for audit results
5. [ ] Review violations and remediate/exempt
6. [ ] Switch to `warn` mode
7. [ ] Wait 7 days, monitor for issues
8. [ ] Switch to `deny` mode

### Post-Deployment
- [ ] Verify enforcement is active
- [ ] Test with known-bad resource (should be denied)
- [ ] Update documentation
- [ ] Alert engineering teams

## Policy Registry

| Policy Name | Kind | Mode | Namespaces | Owner |
|-------------|------|------|------------|-------|
| block-privileged | K8sBlockPrivileged | deny | all except kube-system | Security |
| require-labels | K8sRequiredLabels | deny | all | Platform |
| allowed-repos | K8sAllowedRepos | deny | production, staging | Security |
| block-latest | K8sBlockLatestTag | warn | production | DevOps |
| require-limits | K8sRequireLimits | deny | production | SRE |

## Exemption Request Form

| Field | Value |
|-------|-------|
| Constraint Name | |
| Resource | |
| Namespace | |
| Reason | |
| Duration | |
| Compensating Control | |
| Approved By | |
| Expiry Date | |
