# Scanning kubernetes Manifests With Kubesec

## API Reference

## Kubesec CLI Commands

| Command | Description |
|---------|-------------|
| `kubesec scan <file>` | Scan a manifest file |
| `kubesec scan -o json <file>` | JSON output |
| `kubesec http --port 8080` | Start local API server |
| `kubesec version` | Show version info |

## Kubesec HTTP API

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `https://v2.kubesec.io/scan` | Public scan API |
| POST | `http://localhost:8080/scan` | Local scan API |

## Critical Checks (Negative Score)

| Check | Selector | Risk |
|-------|----------|------|
| Privileged | `securityContext.privileged == true` | Full host access |
| HostPID | `spec.hostPID == true` | Process namespace escape |
| HostNetwork | `spec.hostNetwork == true` | Network namespace escape |
| SYS_ADMIN | `capabilities.add contains SYS_ADMIN` | Near-root capability |

## Best Practice Checks (Positive Score)

| Check | Points | Description |
|-------|--------|-------------|
| ReadOnlyRootFilesystem | +1 | Prevents filesystem writes |
| RunAsNonRoot | +1 | Non-root execution |
| RunAsUser > 10000 | +1 | High UID |
| LimitsCPU | +1 | CPU limits set |
| LimitsMemory | +1 | Memory limits set |
| ServiceAccountName | +3 | Explicit service account |
| AppArmor annotation | +3 | MAC enforcement |
| Seccomp profile | +4 | Syscall filtering |

## Python Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| `subprocess` | stdlib | Execute kubesec CLI |
| `requests` | >=2.28 | HTTP API fallback |
| `json` | stdlib | Parse scan results |

## References

- Kubesec GitHub: https://github.com/controlplaneio/kubesec
- Kubesec Online: https://kubesec.io/
- CIS Kubernetes Benchmark: https://www.cisecurity.org/benchmark/kubernetes

---

## Standards and Controls

## Industry Standards

### CIS Kubernetes Benchmark v1.9
- Section 5.2: Pod Security Standards -- Kubesec validates privileged mode, host namespaces
- Section 5.7: General Policies -- Service account configuration, resource limits
- Maps directly to kubesec scoring checks for container security contexts

### NIST SP 800-190: Application Container Security Guide
- Section 3.1: Image vulnerabilities and configuration defects
- Section 3.4: Orchestrator security -- manifest validation before deployment
- Section 4.1: Countermeasures for image vulnerabilities

### Kubernetes Pod Security Standards (PSS)
- **Privileged**: No restrictions (kubesec score = lowest)
- **Baseline**: Prevents known privilege escalation (kubesec validates hostPID, hostNetwork, privileged)
- **Restricted**: Best practices enforcement (kubesec validates all recommended controls)

## Compliance Mapping

| Kubesec Check | CIS Control | NIST 800-190 | PCI DSS |
|---------------|-------------|--------------|---------|
| Privileged containers | 5.2.1 | 3.4.4 | 2.2 |
| Host PID namespace | 5.2.2 | 3.4.2 | 2.2 |
| Host network | 5.2.4 | 3.4.3 | 1.3 |
| Root execution | 5.2.6 | 3.4.1 | 7.1 |
| ReadOnlyRootFilesystem | 5.2.8 | 4.1.2 | 2.2 |
| Resource limits | 5.4.1 | 4.3.1 | 2.2 |
| Service accounts | 5.1.5 | 3.4.5 | 7.2 |

## Tool Ecosystem

### Complementary Scanning Tools
- **Kubescape**: NSA/CISA framework compliance scanning
- **Checkov**: Infrastructure-as-code security scanning (covers Kubernetes)
- **Datree**: Policy enforcement with custom rules
- **OPA/Gatekeeper**: Runtime policy enforcement as admission controller

### Integration Points
- Pre-commit hooks for developer feedback
- CI/CD pipeline gates to prevent insecure deployments
- Admission webhooks for runtime enforcement
- IDE plugins for shift-left security

---

## Workflows

## Scanning Workflow

### Pre-Commit Scanning
1. Developer writes Kubernetes manifest locally
2. Pre-commit hook runs `kubesec scan` on changed YAML files
3. If score < 0 (critical issues), commit is blocked with remediation guidance
4. Developer fixes issues and retries commit

### CI/CD Pipeline Integration
1. Pull request created with manifest changes
2. CI job runs kubesec scan on all manifests in PR
3. Results posted as PR comment with score breakdown
4. Gate: PR blocked if any manifest scores below threshold
5. Merge allowed only after all manifests pass minimum score

### Admission Control
1. Developer applies manifest via kubectl or GitOps
2. ValidatingWebhook intercepts the API request
3. Kubesec webhook scans the manifest in real-time
4. If critical issues found, admission is denied with explanation
5. Clean manifests are admitted to the cluster

## Remediation Workflow

### Scoring Improvement Process
```
1. Run kubesec scan on target manifest
2. Review "advise" section for point-earning improvements
3. Review "critical" section for must-fix issues
4. Apply fixes in priority order:
   a. Remove critical issues (privileged, hostPID, hostNetwork)
   b. Add seccomp profile (+4 points)
   c. Add AppArmor annotation (+3 points)
   d. Set readOnlyRootFilesystem (+1 point)
   e. Set runAsNonRoot (+1 point)
   f. Add resource limits (+1 point each)
5. Re-scan to verify improved score
6. Commit and push hardened manifest
```

## Continuous Monitoring Workflow

### Scheduled Cluster Scanning
1. CronJob runs daily scan of all deployed resources
2. Extracts manifests from live cluster: `kubectl get deploy -o yaml`
3. Runs kubesec scan on each resource
4. Compares scores against previous scan results
5. Alerts on score regressions or new critical findings
6. Generates weekly security posture report

### Score Trending
```
Week 1: Average score 2.3  (baseline)
Week 2: Average score 3.1  (+0.8 improvement)
Week 3: Average score 4.5  (+1.4 improvement)
Week 4: Average score 5.2  (+0.7 improvement -- target: 6.0)
```

---

## Working Template

## Scan Configuration

| Field | Value |
|-------|-------|
| Scan Date | |
| Kubesec Version | |
| Manifests Scanned | |
| Minimum Score Threshold | |
| Scan Mode (CLI/API/Webhook) | |
| Assessed By | |

## Scan Results Summary

| Metric | Value |
|--------|-------|
| Total Resources Scanned | |
| Critical Findings (score < 0) | |
| Warnings (score < 5) | |
| Passed (score >= 5) | |
| Average Score | |

## Critical Findings

| Resource | File | Score | Critical Check | Remediation |
|----------|------|-------|---------------|-------------|
| | | | | |

## Top Remediation Actions

| # | Check ID | Affected Resources | Points Gain | Effort |
|---|----------|--------------------|-------------|--------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

## CI/CD Gate Configuration

- [ ] Minimum score threshold configured
- [ ] PR comment integration enabled
- [ ] Admission webhook deployed
- [ ] Weekly full-cluster scan scheduled
- [ ] Score trending dashboard configured

## Sign-Off

| Role | Name | Date |
|------|------|------|
| Security Engineer | | |
| DevOps Lead | | |
