# Detecting Container Escape Attempts

## API Reference

## Common Escape Vectors (MITRE ATT&CK)

| Vector | Technique | MITRE ID |
|--------|-----------|----------|
| Privileged container | Mount host FS, load modules | T1611 |
| Docker socket mount | Create privileged container | T1610 |
| Kernel exploits | CVE-2022-0185, Dirty Pipe | T1068 |
| Capability abuse | SYS_ADMIN, SYS_PTRACE | T1548 |
| Sensitive mounts | /proc/sysrq-trigger, cgroup release_agent | T1611 |
| Namespace escape | nsenter, unshare | T1611 |

## Docker CLI Inspection

```bash
# Check if container is privileged
docker inspect --format='{{.HostConfig.Privileged}}' <container>

# Check added capabilities
docker inspect --format='{{.HostConfig.CapAdd}}' <container>

# Check PID namespace mode
docker inspect --format='{{.HostConfig.PidMode}}' <container>

# Check volume mounts
docker inspect --format='{{range .Mounts}}{{.Source}}:{{.Destination}} {{end}}' <container>
```

## Falco JSON Alert Format

```json
{
  "time": "2024-01-15T10:30:00.000Z",
  "rule": "Container Escape via Privileged Mode",
  "priority": "Critical",
  "output": "Container escape attempt...",
  "output_fields": {
    "container.name": "attacker-pod",
    "container.image.repository": "alpine",
    "proc.cmdline": "nsenter -t 1 -m -u -i -n"
  },
  "tags": ["container", "escape", "T1611"]
}
```

## Linux Audit Rules for Escape Detection

```bash
# /etc/audit/rules.d/container-escape.rules
-a always,exit -F arch=b64 -S setns -S unshare -k container_escape
-a always,exit -F arch=b64 -S mount -S umount2 -k container_mount
-a always,exit -F arch=b64 -S init_module -S finit_module -k kernel_module
-w /var/run/docker.sock -p rwxa -k docker_socket
```

## Dangerous Linux Capabilities

| Capability | Escape Risk |
|------------|-------------|
| CAP_SYS_ADMIN | Mount filesystems, manage cgroups |
| CAP_SYS_PTRACE | Trace/debug any process |
| CAP_NET_ADMIN | Network namespace manipulation |
| CAP_SYS_MODULE | Load/unload kernel modules |
| CAP_DAC_READ_SEARCH | Bypass file read permissions |

## CLI Usage

```bash
python agent.py --falco-log /var/log/falco/events.json
python agent.py --audit-log /var/log/audit/audit.log
python agent.py --check-containers
python agent.py --container-id abc123
```

---

## Standards and Controls

## MITRE ATT&CK for Containers

### T1611 - Escape to Host
- **Tactic**: Privilege Escalation
- **Description**: Adversaries may escape container isolation and gain access to the host
- **Sub-techniques**: Privileged container, nsenter, cgroup escape, kernel exploit
- **Detection**: Monitor for namespace manipulation, sensitive path access, privilege changes

### T1610 - Deploy Container
- **Tactic**: Execution
- **Description**: Deploy a new container using Docker socket access from within a container

### T1068 - Exploitation for Privilege Escalation
- **Tactic**: Privilege Escalation
- **Description**: Exploit kernel vulnerabilities for container escape (Dirty Pipe, runc CVEs)

### T1548 - Abuse Elevation Control Mechanism
- **Sub-technique**: T1548.004 - Elevated Execution with Prompt
- **Description**: Abuse Linux capabilities like CAP_SYS_ADMIN for escape

## Known Container Escape CVEs

| CVE | Component | Description | CVSS |
|-----|-----------|-------------|------|
| CVE-2024-21626 | runc | Working directory escape via /proc/self/fd leak | 8.6 |
| CVE-2022-0185 | Linux kernel | fsconfig heap overflow, namespace escape | 8.4 |
| CVE-2022-0847 | Linux kernel | Dirty Pipe - arbitrary file overwrite | 7.8 |
| CVE-2021-22555 | Linux kernel | Netfilter heap OOB, container escape | 7.8 |
| CVE-2020-15257 | containerd | Abstract socket namespace escape | 5.2 |
| CVE-2019-5736 | runc | Binary overwrite, host code execution | 8.6 |

## NIST SP 800-190 - Application Container Security Guide

### Container Runtime Security
- Monitor containers for anomalous behavior
- Detect attempts to access host namespaces
- Alert on kernel module loading from containers
- Implement syscall filtering with seccomp

## Linux Capabilities Required for Escape

| Capability | Escape Risk | Description |
|-----------|------------|-------------|
| CAP_SYS_ADMIN | Critical | Mount filesystems, namespace manipulation |
| CAP_SYS_PTRACE | Critical | ptrace processes, inspect memory |
| CAP_NET_ADMIN | High | Network namespace manipulation |
| CAP_SYS_MODULE | Critical | Load kernel modules |
| CAP_SYS_RAWIO | High | Raw I/O access, iopl/ioperm |
| CAP_DAC_OVERRIDE | High | Bypass file read/write permission |
| CAP_DAC_READ_SEARCH | Medium | Bypass file read permission |
| CAP_MKNOD | Medium | Create device files |

---

## Workflows

## Workflow 1: Real-Time Detection Pipeline

```
[Container Syscall] --> [eBPF/Kernel Module] --> [Falco Engine]
        |                                             |
        v                                             v
  Syscall captured                          Rule evaluation
  (setns, mount,                                  |
   ptrace, etc.)                    +-------------+-------------+
                                    |                           |
                                    v                           v
                              Match found                No match
                                    |                     (normal)
                                    v
                          [Alert Generated]
                                    |
                          +---------+---------+
                          |         |         |
                          v         v         v
                       Slack    SIEM     PagerDuty
                       Alert    Log      Incident
```

## Workflow 2: Escape Attempt Investigation

```
Step 1: Triage alert
  - Identify container, image, namespace
  - Check if container is privileged
  - Determine escape vector attempted

Step 2: Immediate containment
  - kubectl delete pod <pod-name> -n <namespace> (if active escape)
  - kubectl cordon <node> (if node compromised)
  - Network isolate the node

Step 3: Forensic collection
  - Capture container filesystem: docker export <id> > container.tar
  - Collect Falco events for timeline
  - Dump process tree: ps auxf
  - Check for new processes on host
  - Audit logs: ausearch -k container_escape

Step 4: Root cause analysis
  - Was the container privileged?
  - What capabilities were granted?
  - Was Docker socket mounted?
  - Which vulnerability was exploited?

Step 5: Remediation
  - Patch kernel/runtime vulnerability
  - Remove excessive capabilities
  - Apply PSS restricted profile
  - Update seccomp profiles
```

## Workflow 3: Proactive Escape Surface Audit

```
[Inventory all containers] --> [Check for escape risk factors]
                                        |
                            +-----------+-----------+
                            |           |           |
                            v           v           v
                     Privileged?   Docker sock?  Host NS?
                     CAP_SYS_ADMIN? mounted?     hostPID?
                            |           |           |
                            +-----------+-----------+
                                        |
                                        v
                            [Risk Score per container]
                                        |
                              +---------+---------+
                              |                   |
                              v                   v
                        HIGH risk            LOW risk
                        Remediate            Monitor
                        immediately          continuously
```

---

## Working Template

## Environment Information

| Field | Value |
|-------|-------|
| Cluster Name | |
| Container Runtime | Docker / containerd / CRI-O |
| Kernel Version | |
| Runtime Detection Tool | Falco / Sysdig / Tetragon |
| Assessment Date | |

## Escape Surface Inventory

| Container | Privileged | Capabilities | Host NS | Docker Socket | Risk Score |
|-----------|-----------|-------------|---------|--------------|------------|
| | | | | | /10 |

## Detection Rules Deployed

| Rule | Tool | Detects | Status |
|------|------|---------|--------|
| Namespace manipulation | Falco | setns/unshare from container | |
| Docker socket access | Falco | /var/run/docker.sock read/write | |
| Kernel module loading | Falco | modprobe/insmod from container | |
| Sensitive proc access | Falco | /proc/sysrq-trigger, /proc/kcore | |
| Cgroup escape | Falco | release_agent write | |
| Mount operations | auditd | mount/umount2 syscalls | |
| Binary replacement | FIM | runc/containerd binary changes | |

## Findings

| Priority | Container | Risk Factor | Score | Remediation |
|----------|-----------|------------|-------|-------------|
| P1 | | | | |
| P2 | | | | |

## Remediation Tracking

| Finding | Action Required | Owner | Status | Verified |
|---------|----------------|-------|--------|----------|
| | | | | |
