# Performing kubernetes Penetration Testing

## API Reference

## Libraries Used
- **subprocess**: Execute kubectl commands for cluster reconnaissance and testing
- **json**: Parse Kubernetes API JSON output

## CLI Interface
```
python agent.py recon
python agent.py sa-perms [--namespace default]
python agent.py dashboards
python agent.py escape [--namespace default]
```

## Core Functions

### `enumerate_cluster_info()` — Cluster reconnaissance
Gathers: K8s version, node info (OS, kubelet), namespaces, services with types/ports.

### `test_service_account_permissions(namespace)` — RBAC permission testing
Tests 8 permissions via `kubectl auth can-i`:
get pods, list/get secrets, create pods, exec into pods, get nodes, list namespaces, create clusterroles.

### `scan_exposed_dashboards()` — Find management interfaces
Searches for: dashboard, grafana, prometheus, kibana, jaeger, argocd, rancher, lens.
Flags LoadBalancer/NodePort services as externally accessible.

### `check_pod_escape_vectors(namespace)` — Container escape analysis
Detects: privileged mode, CAP_SYS_ADMIN/SYS_PTRACE, hostPath mounts (/, /etc, docker.sock, /proc, /sys),
hostPID namespace, hostNetwork.

## Dangerous Permissions (CRITICAL)
- `list secrets` / `get secrets --all-namespaces`
- `create pods` (pod creation with escalation)
- `create pods/exec` (remote code execution)
- `create clusterroles` (RBAC escalation)

## Dependencies
System: kubectl with cluster access
No Python packages required.

---

## Standards and Controls

## MITRE ATT&CK for Containers

### Relevant Techniques
| ID | Technique | Phase |
|----|-----------|-------|
| T1609 | Container Administration Command | Execution |
| T1610 | Deploy Container | Execution |
| T1611 | Escape to Host | Privilege Escalation |
| T1613 | Container and Resource Discovery | Discovery |
| T1612 | Build Image on Host | Defense Evasion |
| T1552.007 | Container API | Credential Access |

## CIS Kubernetes Benchmark v1.8

### Master Node Checks
- 1.1: Control Plane Configuration Files
- 1.2: API Server (anonymous auth, RBAC, audit logging)
- 1.3: Controller Manager
- 1.4: Scheduler

### Worker Node Checks
- 4.1: Worker Node Configuration Files
- 4.2: Kubelet (anonymous auth, authorization mode)

### Policies
- 5.1: RBAC and Service Accounts
- 5.2: Pod Security Standards
- 5.3: Network Policies
- 5.4: Secrets Management

## NSA/CISA Kubernetes Hardening Guide

### Key Areas
- Scan containers and pods for vulnerabilities
- Run containers as non-root users
- Use network policies to restrict traffic
- Encrypt secrets at rest
- Audit logging for all API calls
- Scan for misconfigurations regularly

## OWASP Kubernetes Top 10

1. K01: Insecure Workload Configurations
2. K02: Supply Chain Vulnerabilities
3. K03: Overly Permissive RBAC
4. K04: Lack of Centralized Policy Enforcement
5. K05: Inadequate Logging and Monitoring
6. K06: Broken Authentication
7. K07: Missing Network Segmentation
8. K08: Secrets Management Failures
9. K09: Misconfigured Cluster Components
10. K10: Outdated and Vulnerable Kubernetes Components

---

## Workflows

## Workflow 1: External Kubernetes Pentest

```
[Scope Definition] --> [Reconnaissance] --> [Service Discovery]
        |                     |                    |
        v                     v                    v
  Define targets        DNS, OSINT,          nmap 6443,8443
  Rules of engagement   cloud metadata       10250,2379,30000+
        |                     |                    |
        +---------------------+--------------------+
                              |
                              v
                    [Automated Scanning]
                    kube-hunter --remote
                    kubescape scan
                    kube-bench (if access)
                              |
                    +---------+---------+
                    |                   |
                    v                   v
            [API Server Tests]   [Kubelet Tests]
            Anonymous auth       Unauthenticated access
            RBAC enumeration     Command execution
            Token theft          Pod listing
                    |                   |
                    +-------------------+
                              |
                              v
                    [Exploitation]
                    Deploy privileged pod
                    Extract secrets
                    Pivot to other namespaces
                              |
                              v
                    [Report and Remediate]
```

## Workflow 2: Internal/Assumed-Breach Testing

```
Step 1: Initial Pod Access
  - Deploy test pod in target namespace
  - Collect service account token
  - Enumerate permissions: kubectl auth can-i --list

Step 2: Internal Reconnaissance
  - List namespaces, pods, services
  - Discover internal services via DNS
  - Check metadata endpoints (cloud IMDS)
  - Identify NetworkPolicy gaps

Step 3: Privilege Escalation
  - Check for wildcard RBAC roles
  - Test service account token from other pods
  - Attempt to create privileged pods
  - Check for vulnerable admission controllers

Step 4: Lateral Movement
  - Access services in other namespaces
  - Extract secrets and configmaps
  - Attempt container escape
  - Access cloud provider metadata

Step 5: Impact Assessment
  - Demonstrate data access (secrets, PVCs)
  - Show cluster-wide compromise path
  - Document attack chain
```

## Workflow 3: Pentest Cleanup

```
[Testing Complete]
        |
        v
[Remove all pentest pods]
kubectl delete pods -l purpose=pentest -A
        |
        v
[Remove test RBAC resources]
kubectl delete rolebinding pentest-rb
kubectl delete serviceaccount pentest-sa
        |
        v
[Verify cleanup]
kubectl get all -l purpose=pentest -A
        |
        v
[Document findings and hand off report]
```

---

## Working Template

## Engagement Details

| Field | Value |
|-------|-------|
| Client | |
| Cluster | |
| Test Type | External / Internal / Assumed-Breach |
| Tester | |
| Date Range | |
| Scope | |

## Executive Summary

[Brief overview of findings and overall cluster security posture]

## Findings Summary

| Severity | Count |
|----------|-------|
| CRITICAL | |
| HIGH | |
| MEDIUM | |
| LOW | |

## Detailed Findings

### Finding 1: [Title]
- **Severity**: CRITICAL / HIGH / MEDIUM / LOW
- **Category**: Authentication / RBAC / Secrets / Network / Pod Security
- **MITRE ATT&CK**: T1xxx
- **Description**:
- **Evidence**:
- **Impact**:
- **Remediation**:
- **References**:

## Attack Paths Identified

### Path 1: [Description]
```
[Initial Access] --> [Step 2] --> [Step 3] --> [Impact]
```

## Recommendations (Priority Order)

| Priority | Recommendation | Effort | Impact |
|----------|---------------|--------|--------|
| 1 | | Low/Med/High | |
| 2 | | | |

## Cleanup Confirmation

- [ ] All test pods removed
- [ ] All test RBAC resources removed
- [ ] All test namespaces cleaned up
- [ ] No persistent backdoors remain
