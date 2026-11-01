# Implementing kubernetes Network Policy With Calico

## API Reference

## Kubernetes NetworkPolicy

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]
```

## Calico GlobalNetworkPolicy

```yaml
apiVersion: projectcalico.org/v3
kind: GlobalNetworkPolicy
metadata:
  name: deny-external
spec:
  order: 100
  selector: app == "backend"
  types: [Ingress]
  ingress:
    - action: Deny
      source:
        nets: ["0.0.0.0/0"]
```

## calicoctl CLI

```bash
# Apply policy
calicoctl apply -f policy.yaml
# Get policies
calicoctl get globalnetworkpolicy -o yaml
# Get host endpoints
calicoctl get hostendpoint
```

## Policy Types

| Type | Scope | Ordering |
|------|-------|----------|
| NetworkPolicy | Namespace | Additive (OR) |
| GlobalNetworkPolicy | Cluster-wide | Ordered by `order` field |

## Common Policy Patterns

| Pattern | Description |
|---------|-------------|
| Default deny | Empty podSelector, no rules |
| Allow DNS | Egress to kube-system UDP/TCP 53 |
| Allow ingress from namespace | namespaceSelector match |
| Allow to external CIDR | ipBlock in egress |

### References

- Calico Docs: https://docs.tigera.io/calico/
- K8s NetworkPolicy: https://kubernetes.io/docs/concepts/services-networking/network-policies/
- Calico Policy Tutorial: https://docs.tigera.io/calico/latest/network-policy/

---

## Standards and Controls

## Industry Standards

### NIST SP 800-190: Application Container Security Guide
- Section 4.4: Container Networking - Isolate container network traffic using network policies
- Section 5.3: Network Security - Implement micro-segmentation between containers
- Recommends default-deny policies with explicit allowlisting

### CIS Kubernetes Benchmark v1.8
- 5.3.1: Ensure that the CNI in use supports Network Policies
- 5.3.2: Ensure that all Namespaces have Network Policies defined
- 5.3.3: Ensure that the default namespace does not contain any pods

### NIST SP 800-53 Rev 5
- SC-7: Boundary Protection - Implement network segmentation controls
- AC-4: Information Flow Enforcement - Control network traffic between pods
- SC-7(5): Deny by Default / Allow by Exception

### NSA/CISA Kubernetes Hardening Guide v1.2
- Section 3: Network Separation and Hardening
  - Use network policies to isolate workloads
  - Implement default deny ingress and egress policies
  - Limit pod-to-pod communication to minimum required

## Calico Documentation References

| Resource | URL |
|----------|-----|
| Calico NetworkPolicy | https://docs.tigera.io/calico/latest/network-policy/get-started/calico-policy/calico-network-policy |
| Kubernetes Policy Tutorial | https://docs.tigera.io/calico/latest/network-policy/get-started/kubernetes-policy/kubernetes-policy-basic |
| GlobalNetworkPolicy | https://docs.tigera.io/calico/latest/reference/resources/globalnetworkpolicy |
| Policy Tiers | https://docs.tigera.io/calico-enterprise/latest/network-policy/policy-tiers/tiered-policy |
| Calico eBPF Dataplane | https://docs.tigera.io/calico/latest/operations/ebpf/enabling-ebpf |

## Zero Trust Network Model

### Principles Applied
1. **Never trust, always verify** - Default deny all traffic between pods
2. **Least privilege access** - Only allow specific required communication paths
3. **Micro-segmentation** - Isolate workloads at pod-to-pod granularity
4. **Identity-based policies** - Use service accounts and labels for policy selection
5. **Continuous monitoring** - Log and alert on denied traffic patterns

## Compliance Mappings

### PCI DSS v4.0
- Requirement 1.2.1: Restrict inbound and outbound traffic to that which is necessary
- Requirement 1.3.1: Inbound traffic is restricted to that which is necessary
- Requirement 1.3.2: Outbound traffic is restricted to that which is necessary

### SOC 2 Type II
- CC6.1: Logical access security - Network isolation between components
- CC6.6: Network boundaries - Restrict access at network boundaries

### HIPAA
- 164.312(e)(1): Transmission Security - Protect data in transit between services

---

## Workflows

## Phase 1: Discovery and Planning

### Map Application Communication Flows
```bash
# Identify all namespaces
kubectl get namespaces

# List all services per namespace
kubectl get svc --all-namespaces -o wide

# Identify pod labels
kubectl get pods --all-namespaces --show-labels

# Check existing network policies
kubectl get networkpolicy --all-namespaces
```

### Document Required Traffic Flows
Create a traffic matrix documenting:
- Source pod/namespace -> Destination pod/namespace
- Protocol and port
- Business justification

## Phase 2: Install and Verify Calico

```bash
# Install Tigera operator
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.27.0/manifests/tigera-operator.yaml

# Wait for operator
kubectl wait --for=condition=Available deployment/tigera-operator -n tigera-operator --timeout=120s

# Install Calico custom resources
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.27.0/manifests/custom-resources.yaml

# Verify all Calico pods are running
kubectl get pods -n calico-system -w

# Install calicoctl as a pod
kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.27.0/manifests/calicoctl.yaml

# Verify node status
kubectl exec -n calico-system calicoctl -- calicoctl node status
```

## Phase 3: Apply Default Deny Policies

### Step 1 - Create DNS Allow Policy First
```bash
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Egress
  egress:
    - to: []
      ports:
        - protocol: UDP
          port: 53
        - protocol: TCP
          port: 53
EOF
```

### Step 2 - Apply Default Deny Ingress
```bash
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Ingress
EOF
```

### Step 3 - Apply Default Deny Egress
```bash
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-egress
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Egress
EOF
```

### Step 4 - Apply Allow Rules per Traffic Flow
```bash
# Allow frontend to backend
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend
      ports:
        - protocol: TCP
          port: 8080
EOF
```

## Phase 4: Validate Policies

### Connectivity Testing
```bash
# Test allowed path (should succeed)
kubectl exec -n production deploy/frontend -- wget -qO- --timeout=5 http://backend-svc:8080/health

# Test blocked path (should timeout/fail)
kubectl exec -n production deploy/frontend -- wget -qO- --timeout=5 http://database-svc:5432

# Test cross-namespace (should fail if denied)
kubectl exec -n staging deploy/test -- wget -qO- --timeout=5 http://backend-svc.production:8080/health
```

### Monitor Denied Connections
```bash
# Check Calico logs for denied connections
kubectl logs -n calico-system -l k8s-app=calico-node --tail=50 | grep -i deny

# Enable flow logs (Calico Enterprise)
kubectl exec -n calico-system calicoctl -- calicoctl get felixconfiguration default -o yaml
```

## Phase 5: Advanced Calico Policies

### Apply Global Security Baseline
```bash
kubectl exec -n calico-system calicoctl -- calicoctl apply -f - <<EOF
apiVersion: projectcalico.org/v3
kind: GlobalNetworkPolicy
metadata:
  name: security-baseline
spec:
  order: 100
  types:
    - Ingress
    - Egress
  egress:
    - action: Allow
      protocol: UDP
      destination:
        ports:
          - 53
    - action: Allow
      protocol: TCP
      destination:
        ports:
          - 53
  ingress:
    - action: Allow
      source:
        selector: "projectcalico.org/namespace in {'kube-system', 'monitoring'}"
EOF
```

## Phase 6: Ongoing Operations

### Regular Policy Audits
1. Review traffic flow matrix monthly
2. Validate policies match documented flows
3. Remove stale policies for decommissioned services
4. Update policies when new services are deployed

### Incident Response
1. If suspicious traffic detected, apply emergency deny policy
2. Analyze Calico flow logs for investigation
3. Identify compromised pod via workload endpoint
4. Isolate pod by applying targeted deny policy

---

## Working Template

## Application Traffic Flow Matrix

| Source | Destination | Port | Protocol | Justification |
|--------|-------------|------|----------|---------------|
| frontend | backend-api | 8080 | TCP | REST API calls |
| backend-api | postgres-db | 5432 | TCP | Database queries |
| backend-api | redis-cache | 6379 | TCP | Session caching |
| all pods | kube-dns | 53 | UDP/TCP | DNS resolution |
| ingress-nginx | frontend | 80 | TCP | External traffic |
| prometheus | all pods | 9090 | TCP | Metrics scraping |

## Namespace Policy Checklist

### Per Namespace
- [ ] Default deny ingress applied
- [ ] Default deny egress applied
- [ ] DNS egress allowed
- [ ] Required ingress rules created per traffic flow
- [ ] Required egress rules created per traffic flow
- [ ] Cross-namespace policies documented
- [ ] Policies tested with connectivity checks

### Cluster-Wide (GlobalNetworkPolicy)
- [ ] Block external access to non-ingress namespaces
- [ ] Allow monitoring namespace to scrape metrics
- [ ] Allow kube-system health checks
- [ ] Emergency isolation policy prepared

## Policy Naming Convention

```
{action}-{source}-to-{destination}-{port}
```

Examples:
- `allow-frontend-to-backend-8080`
- `deny-external-to-database-5432`
- `allow-monitoring-to-all-9090`

## Emergency Isolation Policy

```yaml
# Apply this to immediately isolate a compromised namespace
apiVersion: projectcalico.org/v3
kind: GlobalNetworkPolicy
metadata:
  name: emergency-isolate-NAMESPACE
spec:
  order: 1
  selector: "projectcalico.org/namespace == 'NAMESPACE'"
  types:
    - Ingress
    - Egress
  ingress:
    - action: Deny
  egress:
    - action: Deny
```

## Review Schedule

| Review Type | Frequency | Owner |
|-------------|-----------|-------|
| Policy audit | Monthly | Security Team |
| Traffic flow validation | After each deployment | DevOps |
| Compliance check | Quarterly | GRC Team |
| Emergency drill | Semi-annually | Security + SRE |
