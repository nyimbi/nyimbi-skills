# Implementing RBAC Hardening For kubernetes

## API Reference

## Libraries Used

| Library | Purpose |
|---------|---------|
| `kubernetes` | Official Kubernetes Python client for RBAC API |
| `json` | Parse and format RBAC audit results |
| `yaml` | Read Kubernetes RBAC manifest files |

## Installation

```bash
pip install kubernetes pyyaml
```

## Authentication

```python
from kubernetes import client, config

# Local kubeconfig
config.load_kube_config()

# In-cluster
# config.load_incluster_config()

rbac_api = client.RbacAuthorizationV1Api()
core_api = client.CoreV1Api()
```

## RBAC API Methods

| Method | Description |
|--------|-------------|
| `list_cluster_role()` | List all ClusterRoles |
| `list_cluster_role_binding()` | List all ClusterRoleBindings |
| `list_namespaced_role(namespace)` | List Roles in a namespace |
| `list_namespaced_role_binding(namespace)` | List RoleBindings in a namespace |
| `read_cluster_role(name)` | Get specific ClusterRole details |
| `read_cluster_role_binding(name)` | Get specific ClusterRoleBinding |

## Core Audit Operations

### Detect Wildcard Permissions
```python
def find_wildcard_permissions():
    """Find ClusterRoles with wildcard (*) verbs, resources, or apiGroups."""
    findings = []
    roles = rbac_api.list_cluster_role()
    for role in roles.items:
        if not role.rules:
            continue
        for rule in role.rules:
            wildcards = []
            if rule.verbs and "*" in rule.verbs:
                wildcards.append("verbs")
            if rule.resources and "*" in rule.resources:
                wildcards.append("resources")
            if rule.api_groups and "*" in rule.api_groups:
                wildcards.append("apiGroups")
            if wildcards:
                findings.append({
                    "role": role.metadata.name,
                    "wildcards": wildcards,
                    "severity": "critical" if len(wildcards) >= 2 else "high",
                })
    return findings
```

### Find Subjects Bound to cluster-admin
```python
def find_cluster_admin_bindings():
    """Identify all subjects with cluster-admin privileges."""
    bindings = rbac_api.list_cluster_role_binding()
    admin_subjects = []
    for binding in bindings.items:
        if binding.role_ref.name == "cluster-admin":
            for subject in binding.subjects or []:
                admin_subjects.append({
                    "binding": binding.metadata.name,
                    "subject_kind": subject.kind,
                    "subject_name": subject.name,
                    "namespace": subject.namespace or "cluster-wide",
                    "severity": "high",
                })
    return admin_subjects
```

### Detect Privilege Escalation Risks
```python
ESCALATION_VERBS = {"bind", "escalate", "impersonate"}
DANGEROUS_RESOURCES = {"secrets", "pods/exec", "serviceaccounts/token"}

def find_escalation_risks():
    findings = []
    roles = rbac_api.list_cluster_role()
    for role in roles.items:
        for rule in (role.rules or []):
            dangerous_verbs = set(rule.verbs or []) & ESCALATION_VERBS
            dangerous_resources = set(rule.resources or []) & DANGEROUS_RESOURCES
            if dangerous_verbs:
                findings.append({
                    "role": role.metadata.name,
                    "issue": f"Escalation verbs: {dangerous_verbs}",
                    "severity": "critical",
                })
            if dangerous_resources and "get" in (rule.verbs or []):
                findings.append({
                    "role": role.metadata.name,
                    "issue": f"Access to sensitive resources: {dangerous_resources}",
                    "severity": "high",
                })
    return findings
```

### Audit Service Account Token Auto-Mount
```python
def find_automount_service_tokens():
    """Find pods with automountServiceAccountToken enabled."""
    findings = []
    namespaces = core_api.list_namespace()
    for ns in namespaces.items:
        pods = core_api.list_namespaced_pod(ns.metadata.name)
        for pod in pods.items:
            automount = pod.spec.automount_service_account_token
            if automount is None or automount is True:
                sa = pod.spec.service_account_name or "default"
                if sa != "default":
                    findings.append({
                        "namespace": ns.metadata.name,
                        "pod": pod.metadata.name,
                        "service_account": sa,
                        "issue": "automountServiceAccountToken not disabled",
                    })
    return findings
```

### Find Unused Roles
```python
def find_unused_roles():
    """Detect Roles with no corresponding RoleBindings."""
    namespaces = core_api.list_namespace()
    unused = []
    for ns in namespaces.items:
        roles = rbac_api.list_namespaced_role(ns.metadata.name)
        bindings = rbac_api.list_namespaced_role_binding(ns.metadata.name)
        bound_roles = {b.role_ref.name for b in bindings.items}
        for role in roles.items:
            if role.metadata.name not in bound_roles:
                unused.append({
                    "namespace": ns.metadata.name,
                    "role": role.metadata.name,
                    "issue": "Role has no bindings — candidate for removal",
                })
    return unused
```

## kubectl Equivalents

```bash
# List all ClusterRoleBindings for cluster-admin
kubectl get clusterrolebindings -o json | \
  jq '.items[] | select(.roleRef.name=="cluster-admin") | .subjects[]'

# Find roles with wildcard permissions
kubectl get clusterroles -o json | \
  jq '.items[] | select(.rules[]?.verbs[]? == "*") | .metadata.name'

# Audit RBAC with rakkess (kubectl plugin)
kubectl krew install access-matrix
kubectl access-matrix --namespace production
```

## Output Format

```json
{
  "cluster": "production",
  "audit_date": "2025-01-15",
  "cluster_admin_subjects": 5,
  "wildcard_roles": 3,
  "escalation_risks": 2,
  "unused_roles": 8,
  "findings": [
    {
      "role": "custom-admin",
      "issue": "Wildcard verbs and resources",
      "severity": "critical",
      "remediation": "Replace * with explicit verb and resource lists"
    }
  ]
}
```

---

## Standards and Controls

## CIS Kubernetes Benchmark v1.9
- 5.1.1: Ensure cluster-admin role is only used where required
- 5.1.2: Minimize access to secrets
- 5.1.3: Minimize wildcard use in Roles and ClusterRoles
- 5.1.4: Minimize access to create pods
- 5.1.5: Ensure default service accounts are not actively used
- 5.1.6: Ensure Service Account Tokens are only mounted where necessary

## NIST SP 800-190
- Section 3.4: Orchestrator security -- access control hardening
- Section 4.4: Countermeasures for orchestrator vulnerabilities

## MITRE ATT&CK
- T1078.004: Valid Accounts: Cloud Accounts -- compromised service accounts
- T1098: Account Manipulation -- RBAC escalation
- T1069: Permission Groups Discovery -- enumerating RBAC bindings

---

## Workflows

## Hardening Workflow
1. Audit all existing ClusterRoleBindings and RoleBindings
2. Identify overprivileged accounts (cluster-admin sprawl)
3. Create namespace-scoped Roles with minimum required permissions
4. Migrate workloads to dedicated service accounts
5. Disable automountServiceAccountToken on default service accounts
6. Integrate OIDC for user authentication
7. Deploy RBAC monitoring and alerting
8. Schedule quarterly RBAC reviews

## Continuous Compliance
- Weekly: automated RBAC audit with rbac-lookup
- Monthly: review new RoleBindings created in past 30 days
- Quarterly: full access review with stakeholder sign-off
- Annually: penetration test RBAC boundaries

---

## Working Template

## Cluster Information
| Field | Value |
|-------|-------|
| Cluster Name | |
| Kubernetes Version | |
| Assessment Date | |

## RBAC Audit Results
| Metric | Count |
|--------|-------|
| ClusterRoleBindings | |
| cluster-admin bindings | |
| Wildcard permissions | |
| Default SA bindings | |

## Hardening Checklist
- [ ] Removed unnecessary cluster-admin bindings
- [ ] All workloads use dedicated service accounts
- [ ] automountServiceAccountToken disabled on default SAs
- [ ] OIDC integration configured
- [ ] RBAC monitoring and alerting active
- [ ] Quarterly review process established

## Sign-Off
| Role | Name | Date |
|------|------|------|
| Security Engineer | | |
| Platform Lead | | |
