# Implementing Runtime Security With Tetragon

## API Reference

## TracingPolicy CRD

```yaml
apiVersion: cilium.io/v1alpha1
kind: TracingPolicy
metadata:
  name: monitor-sensitive-files
spec:
  kprobes:
    - call: fd_install
      args:
        - index: 1
          type: file
      selectors:
        - matchArgs:
            - index: 1
              operator: Prefix
              values: ["/etc/shadow", "/etc/passwd"]
```

## Tetra CLI Commands

| Command | Description |
|---------|-------------|
| `tetra status` | Tetragon health |
| `tetra getevents` | Stream events |
| `tetra tracingpolicy list` | List policies |

## Event Types

| Type | Description |
|------|-------------|
| `process_exec` | Process execution |
| `process_exit` | Process termination |
| `process_kprobe` | Kernel probe trigger |

## Key Libraries

| Library | Use |
|---------|-----|
| `kubernetes` | K8s API client |
| `subprocess` | kubectl/tetra CLI |
| `grpc` | Tetragon gRPC API |

---

## Standards and Controls

## Industry Standards

### NIST SP 800-190: Application Container Security Guide
- Section 4.2: Runtime monitoring and anomaly detection for containers
- Section 4.4: Container-level network monitoring requirements
- Recommends kernel-level security monitoring for container environments

### CIS Kubernetes Benchmark v1.9
- Control 5.7.1: Create administrative boundaries between resources using namespaces
- Control 5.7.3: Apply Security Context to pods and containers
- Control 5.7.4: The default namespace should not be used

### MITRE ATT&CK for Containers
- T1611: Escape to Host -- Tetragon detects namespace manipulation attempts
- T1059.004: Command and Scripting Interpreter: Unix Shell -- process execution monitoring
- T1053.007: Container Orchestration Job -- detects unauthorized job creation
- T1496: Resource Hijacking -- crypto-miner detection and blocking

## CNCF Landscape Positioning

Tetragon is positioned in the CNCF Runtime Security category alongside:
- Falco (audit-log and syscall-based detection)
- KubeArmor (LSM-based enforcement)
- Tracee (eBPF-based tracing)

### Key Differentiators
- Kernel-level filtering reduces event volume before reaching user space
- Native enforcement (Sigkill/Override) without requiring separate enforcement engine
- Deep integration with Cilium for combined network + runtime security
- TracingPolicy CRD for Kubernetes-native policy management

## Compliance Mapping

| Requirement | Framework | Tetragon Capability |
|-------------|-----------|-------------------|
| Runtime threat detection | PCI DSS 11.5 | TracingPolicy with file integrity monitoring |
| Unauthorized process detection | SOC 2 CC6.8 | Process execution monitoring with namespace context |
| Container isolation enforcement | NIST 800-190 4.2 | Namespace escape detection and blocking |
| Audit trail generation | ISO 27001 A.12.4 | JSON event export to SIEM systems |
| Incident response automation | NIST CSF DE.AE | Real-time Sigkill enforcement on policy violations |

---

## Workflows

## Deployment Workflow

### Phase 1: Observation Mode
1. Install Tetragon with default TracingPolicies (no enforcement)
2. Collect baseline process execution data for 7-14 days
3. Analyze event patterns to identify normal vs anomalous behavior
4. Document expected processes per namespace and workload type

### Phase 2: Detection Policies
1. Create TracingPolicies for known attack patterns (container escape, privilege escalation)
2. Configure event export to SIEM (Elasticsearch, Splunk, or Datadog)
3. Build alerting rules based on TracingPolicy matches
4. Validate detection accuracy with red team exercises

### Phase 3: Enforcement
1. Enable Sigkill actions for high-confidence threats (known malware binaries)
2. Enable Override actions for dangerous syscalls in non-privileged containers
3. Implement graduated response -- alert first, block after confirmation
4. Monitor enforcement actions for false positives

## TracingPolicy Development Workflow

```
1. Identify Threat -> Map to MITRE ATT&CK technique
2. Determine Kernel Hook -> kprobe, tracepoint, or LSM hook
3. Define Selectors -> Binary, namespace, capability filters
4. Set Action -> Post (observe), Sigkill (block), Override (deny)
5. Test in Staging -> Deploy to non-production namespace first
6. Validate with Attack Simulation -> Confirm detection
7. Deploy to Production -> Apply via GitOps
8. Monitor False Positives -> Tune selectors as needed
```

## Incident Response Integration

### When Tetragon Detects a Threat
1. Event is generated with full context (pod, namespace, binary, args, capabilities)
2. Event exported to SIEM via JSON log export or Prometheus metric
3. SOAR platform receives alert and triggers playbook
4. Automated actions: isolate pod network (via Cilium NetworkPolicy), capture forensic data
5. Security team receives enriched alert with Kubernetes context

### Forensic Data Collection
```bash
# Export recent events for a specific pod
tetra getevents --namespace <ns> --pod <pod-name> \
  --since 1h -o json > /forensics/tetragon-events.json

# Get process tree for suspicious activity
tetra getevents --process-pid <pid> --ancestors 5 -o compact
```

## Operational Runbook

### Daily Checks
- Review `tetragon_missed_events_total` metric for event buffer overflows
- Check Tetragon DaemonSet health across all nodes
- Review new TracingPolicy match counts

### Weekly Checks
- Analyze top 10 most frequent event types
- Review enforcement action logs for false positives
- Update TracingPolicies based on new threat intelligence

### Monthly Checks
- Performance impact assessment (CPU/memory overhead per node)
- TracingPolicy effectiveness review with red team
- Update Tetragon to latest stable release

---

## Working Template

## Cluster Information

| Field | Value |
|-------|-------|
| Cluster Name | |
| Kubernetes Version | |
| Node Count | |
| Tetragon Version | |
| Kernel Version | |
| Assessment Date | |
| Assessed By | |

## Pre-Deployment Checklist

- [ ] Linux kernel version >= 5.4 (5.10+ preferred)
- [ ] BTF (BPF Type Format) enabled in kernel
- [ ] Helm 3.x installed and configured
- [ ] kubectl access with cluster-admin privileges
- [ ] SIEM/log aggregation endpoint configured
- [ ] Alerting channels established (PagerDuty, Slack, etc.)

## Deployment Configuration

### Helm Values

```yaml
tetragon:
  enableProcessCred: true
  enableProcessNs: true
  grpc:
    address: "localhost:54321"
  export:
    mode: "json"
  resources:
    limits:
      cpu: "1"
      memory: "1Gi"
    requests:
      cpu: "250m"
      memory: "256Mi"
```

## TracingPolicy Inventory

| Policy Name | Type | Hooks | Action | Target Namespaces |
|-------------|------|-------|--------|------------------|
| | kprobe/tracepoint | | Post/Sigkill/Override | |
| | | | | |
| | | | | |

## Baseline Metrics

| Metric | Value | Date Captured |
|--------|-------|--------------|
| Average events/sec per node | | |
| CPU overhead per node (%) | | |
| Memory usage per node (MB) | | |
| Event buffer miss rate | | |

## Detection Validation Results

| Attack Scenario | MITRE ATT&CK ID | Detected | Action Taken | Notes |
|----------------|------------------|----------|-------------- |-------|
| Container escape via nsenter | T1611 | Yes/No | | |
| Crypto-miner execution | T1496 | Yes/No | | |
| Sensitive file read (/etc/shadow) | T1552.001 | Yes/No | | |
| Shell in non-shell container | T1059.004 | Yes/No | | |
| Privilege escalation via sudo | T1548.003 | Yes/No | | |
| Network reconnaissance (nmap) | T1046 | Yes/No | | |

## Risk Findings

### Critical

| Finding | Namespace | Pod | Recommended Action |
|---------|-----------|-----|-------------------|
| | | | |

### High

| Finding | Namespace | Pod | Recommended Action |
|---------|-----------|-----|-------------------|
| | | | |

### Medium

| Finding | Namespace | Pod | Recommended Action |
|---------|-----------|-----|-------------------|
| | | | |

## Recommendations

1. **Immediate Actions**
   - [ ]

2. **Short-term (30 days)**
   - [ ]

3. **Long-term (90 days)**
   - [ ]

## Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Security Engineer | | | |
| Platform Engineer | | | |
| Security Manager | | | |
