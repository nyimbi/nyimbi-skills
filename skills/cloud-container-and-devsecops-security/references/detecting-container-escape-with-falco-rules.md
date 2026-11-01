# Detecting Container Escape With Falco Rules

## API Reference

## Falco CLI

```bash
falco --version                           # check version
falco --validate /path/to/rules.yaml      # validate rules syntax
falco -r /etc/falco/rules.d/escape.yaml   # load specific rules
falco --list                              # list all available fields
falco --list-events                       # list supported syscalls
```

## Falco Rule Syntax

```yaml
- rule: <name>
  desc: <description>
  condition: <filter expression>
  output: <alert message with fields>
  priority: <Emergency|Alert|Critical|Error|Warning|Notice|Informational|Debug>
  tags: [tag1, tag2]
  enabled: true
```

## Key Falco Filter Fields

| Field | Description |
|-------|-------------|
| `container` | True if event is from a container |
| `spawned_process` | True if new process spawned |
| `proc.name` | Process name |
| `proc.cmdline` | Full command line |
| `proc.pname` | Parent process name |
| `fd.name` | File descriptor name/path |
| `container.name` | Container name |
| `container.image.repository` | Image repository |
| `container.privileged` | True if privileged |
| `proc.is_exe_upper_layer` | Binary not in original image |
| `evt.type` | Syscall type (setns, unshare, mount) |

## Falco JSON Output Format

```json
{
  "time": "2024-01-15T10:30:00.000Z",
  "rule": "Container Escape Binary Execution",
  "priority": "Critical",
  "source": "syscall",
  "output": "Escape binary in container...",
  "output_fields": {
    "user.name": "root",
    "proc.cmdline": "nsenter -t 1 -m -u -i -n",
    "container.name": "attacker-pod"
  },
  "tags": ["container", "escape", "T1611"]
}
```

## Falcosidekick Alert Routing

```yaml
config:
  slack:
    webhookurl: "https://hooks.slack.com/services/XXX"
    minimumpriority: "critical"
  elasticsearch:
    hostport: "https://es:9200"
    index: "falco-alerts"
```

## Helm Deployment

```bash
helm repo add falcosecurity https://falcosecurity.github.io/charts
helm install falco falcosecurity/falco \
  --namespace falco --create-namespace \
  --set driver.kind=ebpf \
  --set falcosidekick.enabled=true
```

## CLI Usage

```bash
python agent.py --check-status
python agent.py --validate-rules /etc/falco/rules.d/escape.yaml
python agent.py --parse-alerts /var/log/falco/events.json --min-priority Warning
python agent.py --generate-rules > escape-rules.yaml
```

---

## Standards and Controls

## Industry Standards

### NIST SP 800-190: Application Container Security Guide
- Section 4.3: Container Runtime - Monitor containers for anomalous behavior at runtime
- Section 5.4: Container Runtime Security - Implement runtime monitoring and alerting
- Recommends syscall-level monitoring for escape detection

### CIS Kubernetes Benchmark v1.8
- 5.7.1: Create administrative boundaries between resources using namespaces
- 5.7.2: Ensure that the seccomp profile is set to docker/default
- 5.7.3: Apply Security Context to pods and containers
- 5.7.4: The default namespace should not be used

### MITRE ATT&CK for Containers

| Technique ID | Name | Falco Detection |
|-------------|------|-----------------|
| T1611 | Escape to Host | nsenter, mount, chroot detection |
| T1610 | Deploy Container | Privileged container launch detection |
| T1003 | OS Credential Dumping | /etc/shadow access from container |
| T1005 | Data from Local System | Sensitive file read detection |
| T1059 | Command and Scripting Interpreter | Shell spawn in container |
| T1068 | Exploitation for Privilege Escalation | Kernel exploit indicators |

### NSA/CISA Kubernetes Hardening Guide v1.2
- Section 5: Audit Logging and Threat Detection
  - Enable runtime security monitoring
  - Detect anomalous container behavior in real-time
  - Monitor for privilege escalation attempts

## Falco Rule Maturity Levels

| Level | Description | Count |
|-------|-------------|-------|
| maturity_stable | Production-ready, low false positives | 25 rules |
| maturity_incubating | Proven useful, may need tuning | ~30 rules |
| maturity_sandbox | Experimental, high false positive rate | ~38 rules |
| maturity_deprecated | Scheduled for removal | Variable |

## Known Container Escape CVEs

| CVE | Description | Falco Rule |
|-----|-------------|------------|
| CVE-2024-21626 | runc process.cwd container breakout | Detect use of /proc/self/fd to access host |
| CVE-2022-0492 | cgroup v1 release_agent escape | Write to Cgroup Release Agent |
| CVE-2022-0185 | File system context exploit | Detect unshare in container |
| CVE-2020-15257 | containerd-shim API access | Detect abstract socket connections |
| CVE-2019-5736 | runc overwrite host binary | Detect writes to /proc/self/exe |

## Compliance Mappings

### PCI DSS v4.0
- Requirement 10.6.1: Review logs for anomalies at least daily
- Requirement 11.5: Deploy change-detection mechanisms

### SOC 2 Type II
- CC7.2: Monitor system components for anomalies
- CC7.3: Evaluate security events to determine impact

---

## Workflows

## Phase 1: Deploy Falco

### Install on Kubernetes
```bash
helm repo add falcosecurity https://falcosecurity.github.io/charts
helm repo update

helm install falco falcosecurity/falco \
  --namespace falco --create-namespace \
  --set driver.kind=ebpf \
  --set falcosidekick.enabled=true \
  --set falcosidekick.webui.enabled=true \
  --set collectors.containerd.enabled=true

kubectl -n falco rollout status daemonset/falco --timeout=120s
```

### Verify Deployment
```bash
kubectl get pods -n falco -o wide
kubectl logs -n falco -l app.kubernetes.io/name=falco --tail=10
```

## Phase 2: Deploy Custom Escape Detection Rules

### Create ConfigMap with Custom Rules
```bash
kubectl create configmap falco-escape-rules -n falco \
  --from-file=container-escape.yaml=/path/to/container-escape.yaml

# Restart Falco to load new rules
kubectl rollout restart daemonset/falco -n falco
```

### Validate Rules Loaded
```bash
kubectl exec -n falco $(kubectl get pod -n falco -l app.kubernetes.io/name=falco -o jsonpath='{.items[0].metadata.name}') -- \
  falco --list | grep -i escape
```

## Phase 3: Test Detection

### Test 1 - Privileged Container
```bash
kubectl run escape-test-priv --image=alpine --restart=Never \
  --overrides='{"spec":{"containers":[{"name":"test","image":"alpine","command":["sleep","30"],"securityContext":{"privileged":true}}]}}'

# Check alert
kubectl logs -n falco -l app.kubernetes.io/name=falco --tail=5 | grep -i privileged
kubectl delete pod escape-test-priv
```

### Test 2 - Sensitive File Access
```bash
kubectl run escape-test-shadow --image=alpine --restart=Never -- cat /etc/shadow
kubectl logs -n falco -l app.kubernetes.io/name=falco --tail=5 | grep -i shadow
kubectl delete pod escape-test-shadow
```

### Test 3 - Shell Spawn
```bash
kubectl exec -it deploy/some-app -- /bin/sh
# In Falco logs, should see "Terminal shell in container"
```

## Phase 4: Integrate Alerting

### Configure Falcosidekick Outputs
```yaml
# values-sidekick.yaml
config:
  slack:
    webhookurl: "https://hooks.slack.com/services/XXX/YYY/ZZZ"
    minimumpriority: "warning"
  elasticsearch:
    hostport: "https://elasticsearch:9200"
    index: "falco"
    minimumpriority: "notice"
  prometheus:
    enabled: true
```

```bash
helm upgrade falco falcosecurity/falco -n falco \
  -f values-sidekick.yaml
```

## Phase 5: Tune and Maintain

### Handle False Positives
```yaml
# Add exceptions to rules
- rule: Terminal shell in container
  append: true
  exceptions:
    - name: known_shell_spawners
      fields: [container.image.repository]
      comps: [in]
      values:
        - [my-debug-image, kubectl-debug]
```

### Regular Maintenance
1. Update Falco rules weekly: `falcoctl artifact install falco-rules`
2. Review new maturity_stable rules after each Falco release
3. Correlate Falco alerts with Kubernetes audit logs
4. Run escape simulation exercises monthly

---

## Working Template

## Alert Triage Template

### Alert Details
| Field | Value |
|-------|-------|
| Alert Time | |
| Rule Name | |
| Priority | |
| Container Name | |
| Container Image | |
| Pod Name | |
| Namespace | |
| Node | |
| User | |
| Process Command | |
| MITRE Technique | |

## Triage Steps

### Immediate Actions (0-5 minutes)
- [ ] Acknowledge alert in SIEM/SOAR
- [ ] Verify alert is not a false positive (check known exceptions list)
- [ ] Identify the affected pod and node
- [ ] Check if the container is still running

### Investigation (5-30 minutes)
- [ ] Capture pod spec: `kubectl get pod <name> -n <ns> -o yaml`
- [ ] Review container security context
- [ ] Check if container is privileged
- [ ] Review mounted volumes for host paths
- [ ] Examine process tree from Falco output
- [ ] Check for other alerts from same container/node
- [ ] Review Kubernetes audit logs for the same timeframe

### Containment (if confirmed)
- [ ] Isolate pod with network policy deny-all
- [ ] Cordon affected node: `kubectl cordon <node>`
- [ ] Capture forensic data from container
- [ ] Kill compromised container: `kubectl delete pod <name> -n <ns>`
- [ ] Review other pods on same node for compromise

### Recovery
- [ ] Scan node for rootkits
- [ ] Rebuild node if compromise confirmed
- [ ] Patch vulnerable container image
- [ ] Update network policies
- [ ] Uncordon node after verification

## False Positive Exceptions

| Container Image | Rule | Justification | Approved By | Date |
|----------------|------|---------------|-------------|------|
| | | | | |

## Escalation Matrix

| Priority | Response Time | Notify |
|----------|--------------|--------|
| CRITICAL | Immediate | Security On-Call + Engineering Lead |
| WARNING | 15 minutes | Security On-Call |
| NOTICE | 1 hour | Security Team queue |
| INFO | Next business day | Review in daily standup |
