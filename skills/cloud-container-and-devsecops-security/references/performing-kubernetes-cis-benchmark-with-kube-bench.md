# Performing kubernetes Cis Benchmark With Kube Bench

## API Reference

## Libraries Used
- **subprocess**: Execute kube-bench, kubectl commands
- **json**: Parse kube-bench JSON output and kubectl resource data

## CLI Interface
```
python agent.py bench [--target master|node|etcd|policies] [--benchmark cis-1.8]
python agent.py pods [--namespace default]
python agent.py rbac
python agent.py netpol [--namespace default]
```

## Core Functions

### `run_kube_bench(target, benchmark)` — Execute CIS benchmark scan
Runs kube-bench with JSON output. Returns pass/fail/warn/info summary and compliance percentage.
Targets: master, controlplane, node, etcd, policies.

### `check_pod_security(namespace)` — Audit pod security contexts
Checks for: privileged containers, root user, writable root filesystem,
dangerous capabilities (SYS_ADMIN, NET_ADMIN, ALL), privilege escalation.

### `check_rbac_config()` — Audit cluster RBAC
Detects wildcard permissions (`*` verbs on `*` resources), pod creation rights,
and cluster-admin bindings to service accounts/users.

### `check_network_policies(namespace)` — Verify network segmentation
Flags namespaces with no NetworkPolicy. Lists policy coverage details.

## Pod Security Issues Detected
| Issue | Description |
|-------|-------------|
| PRIVILEGED_CONTAINER | Container runs in privileged mode |
| RUNS_AS_ROOT | No runAsNonRoot constraint |
| WRITABLE_ROOT_FS | readOnlyRootFilesystem not set |
| DANGEROUS_CAPABILITIES | SYS_ADMIN/NET_ADMIN/ALL added |
| PRIVILEGE_ESCALATION_ALLOWED | allowPrivilegeEscalation not false |

## Dependencies
System: kube-bench (Aqua Security), kubectl with cluster access
No Python packages required.

---

## Standards and Controls

## CIS Kubernetes Benchmark Versions

| Benchmark Version | Kubernetes Versions | Released |
|-------------------|-------------------|----------|
| CIS 1.8 | 1.27+ | 2023 |
| CIS 1.7 | 1.25-1.26 | 2022 |
| CIS 1.6 | 1.20-1.24 | 2021 |
| EKS 1.2.0 | EKS 1.23+ | 2023 |
| GKE 1.4.0 | GKE 1.25+ | 2023 |
| AKS 1.0 | AKS 1.24+ | 2023 |

## NIST SP 800-53 Rev 5 Mappings

| CIS Check | NIST Control | Description |
|-----------|-------------|-------------|
| 1.2.1 Anonymous auth | AC-14 | Permitted Actions without Authentication |
| 1.2.6 RBAC | AC-3 | Access Enforcement |
| 1.2.22 Audit logging | AU-2, AU-3 | Audit Events, Content of Audit Records |
| 2.1 etcd encryption | SC-28 | Protection of Information at Rest |
| 4.2.1 kubelet auth | IA-2 | Identification and Authentication |
| 5.1 RBAC policies | AC-6 | Least Privilege |
| 5.2 Pod security | CM-7 | Least Functionality |
| 5.3 Network policies | SC-7 | Boundary Protection |

## NSA/CISA Kubernetes Hardening Guide v1.2
- Section 1: Kubernetes Pod Security
- Section 2: Network Separation and Hardening
- Section 3: Authentication and Authorization
- Section 4: Audit Logging and Threat Detection

## Compliance Frameworks

### PCI DSS v4.0
- Req 2.2: Develop configuration standards for all system components
- Req 6.3.2: Develop software securely

### SOC 2
- CC6.1: Logical access security for system components
- CC8.1: Change management controls

---

## Workflows

## Phase 1: Initial Assessment

```bash
# Deploy kube-bench as Job
kubectl apply -f https://raw.githubusercontent.com/aquasecurity/kube-bench/main/job.yaml
kubectl wait --for=condition=complete job/kube-bench --timeout=300s
kubectl logs job/kube-bench > baseline-report.txt
kubectl delete job kube-bench
```

## Phase 2: Analyze Results

```bash
# Count results by status
PASS=$(grep -c "\[PASS\]" baseline-report.txt)
FAIL=$(grep -c "\[FAIL\]" baseline-report.txt)
WARN=$(grep -c "\[WARN\]" baseline-report.txt)
echo "PASS: $PASS | FAIL: $FAIL | WARN: $WARN"

# Extract failed checks with remediation
grep -A 2 "\[FAIL\]" baseline-report.txt
```

## Phase 3: Remediate Failures

### Priority order:
1. Control plane authentication (Section 1.2)
2. etcd security (Section 2)
3. Worker node kubelet (Section 4)
4. RBAC and policies (Section 5)

### Apply each remediation, then re-run affected section:
```bash
kube-bench run --targets master --check 1.2.1
```

## Phase 4: Continuous Monitoring

```yaml
# kube-bench-cronjob.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: kube-bench-scan
  namespace: security
spec:
  schedule: "0 6 * * 1"
  jobTemplate:
    spec:
      template:
        spec:
          hostPID: true
          containers:
          - name: kube-bench
            image: aquasec/kube-bench:v0.7.3
            command: ["kube-bench", "run", "--json"]
            volumeMounts:
            - name: var-lib-kubelet
              mountPath: /var/lib/kubelet
              readOnly: true
            - name: etc-kubernetes
              mountPath: /etc/kubernetes
              readOnly: true
          volumes:
          - name: var-lib-kubelet
            hostPath:
              path: /var/lib/kubelet
          - name: etc-kubernetes
            hostPath:
              path: /etc/kubernetes
          restartPolicy: Never
```

## Phase 5: Track Improvement

Compare PASS/FAIL/WARN counts across scans to measure security posture improvement over time.

---

## Working Template

## Scan Schedule

| Cluster | Environment | Frequency | Last Scan | Score |
|---------|-------------|-----------|-----------|-------|
| prod-us-east | Production | Weekly | YYYY-MM-DD | NN% |
| staging-us-east | Staging | Bi-weekly | YYYY-MM-DD | NN% |
| dev-cluster | Development | Monthly | YYYY-MM-DD | NN% |

## Remediation Tracking

| Check ID | Description | Severity | Status | Owner | Due Date |
|----------|-------------|----------|--------|-------|----------|
| 1.2.1 | Anonymous auth disabled | Critical | Open | | |
| 1.2.6 | RBAC authorization | Critical | Open | | |
| 4.2.1 | kubelet anonymous auth | High | Open | | |
| 5.1.1 | Cluster-admin role | High | Open | | |

## Accepted Risks

| Check ID | Description | Justification | Approved By | Expiry |
|----------|-------------|---------------|-------------|--------|
| | | | | |

## Score History

| Date | Pass | Fail | Warn | Score |
|------|------|------|------|-------|
| YYYY-MM-DD | | | | % |
