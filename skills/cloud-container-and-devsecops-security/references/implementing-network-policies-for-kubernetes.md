# Implementing Network Policies For kubernetes

## API Reference

## Default Deny-All Policy

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
  namespace: production
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]
```

## Allow Specific Ingress

```yaml
spec:
  podSelector:
    matchLabels: { app: backend }
  ingress:
    - from:
        - podSelector: { matchLabels: { app: frontend } }
      ports:
        - port: 8080
```

## kubectl Commands

```bash
# List all network policies
kubectl get networkpolicy --all-namespaces
# Describe policy
kubectl describe networkpolicy default-deny -n production
# Apply policy
kubectl apply -f netpol.yaml
```

## Policy Types

| Type | Behavior when present |
|------|-----------------------|
| Ingress | Restrict inbound traffic |
| Egress | Restrict outbound traffic |
| Both empty | Default deny all |

## Common Patterns

| Pattern | Description |
|---------|-------------|
| Default deny | Empty podSelector, no rules |
| Allow DNS | Egress to kube-system:53 |
| Allow same namespace | namespaceSelector match |
| Allow from ingress controller | Label-based ingress |

### References

- K8s NetworkPolicy: https://kubernetes.io/docs/concepts/services-networking/network-policies/
- Network Policy Editor: https://editor.networkpolicy.io/
- CNI Comparison: https://kubernetes.io/docs/concepts/cluster-administration/networking/

---

## Standards and Controls

## CIS Kubernetes Benchmark v1.8 - Section 5.3
- 5.3.1: Ensure CNI supports Network Policies
- 5.3.2: Ensure default deny NetworkPolicy for all namespaces

## NSA/CISA Kubernetes Hardening Guide
- Implement network segmentation between namespaces
- Apply default-deny network policies
- Restrict pod-to-pod communication to required paths only
- Block access to cloud metadata endpoints

## MITRE ATT&CK Mitigations
| Technique | Mitigation via Network Policy |
|-----------|------------------------------|
| T1046 - Network Service Scanning | Limit reachable services |
| T1021 - Remote Services | Block lateral movement |
| T1552 - Credentials from IMDS | Block 169.254.169.254 |

---

## Workflows

## Workflow 1: Network Policy Deployment
```
[Identify communication paths] --> [Create default-deny] --> [Add allow rules per service]
         |                                |                           |
         v                                v                           v
  Map pod-to-pod traffic         Apply to all namespaces    Test with connectivity checks
  Document required flows        Verify DNS still works     Monitor for broken connections
```

## Workflow 2: Progressive Enforcement
```
Step 1: Deploy in audit mode (Calico: log-only)
Step 2: Monitor traffic patterns for 1 week
Step 3: Create policies matching observed traffic
Step 4: Apply default-deny in non-production
Step 5: Validate application functionality
Step 6: Roll out to production namespaces
```

---

## Working Template

## Namespace Policy Matrix
| Namespace | Default-Deny Ingress | Default-Deny Egress | DNS Allowed | Metadata Blocked |
|-----------|---------------------|---------------------|-------------|-----------------|
| | | | | |

## Service Communication Map
| Source | Destination | Port | Protocol | Policy Name |
|--------|-------------|------|----------|-------------|
| | | | | |

## Remediation
| Namespace | Missing Policy | Action | Status |
|-----------|---------------|--------|--------|
| | | | |
