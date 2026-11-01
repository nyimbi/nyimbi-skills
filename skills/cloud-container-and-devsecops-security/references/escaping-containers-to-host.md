# Escaping Containers To Host

## API Reference

## Enumeration Commands

| Command | Purpose |
|---------|---------|
| `amicontained` | Print capabilities, namespaces, seccomp mode, AppArmor profile |
| `grep CapEff /proc/self/status` | Read effective capability bitmask |
| `capsh --decode=<hex>` | Decode capability bitmask to names |
| `mount` / `findmnt` | List mounts; spot `docker.sock`, `hostPath`, `/host` |
| `ls -la /var/run/docker.sock` | Detect mounted Docker socket |
| `ls -la /proc/1/root` | Detect shared host PID namespace |
| `./deepce.sh` | Automated Docker enumeration + escape checks |
| `./cdk evaluate` | CDK automated container/K8s posture eval |

## Docker Daemon REST API (via /var/run/docker.sock)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/version` | GET | Confirm daemon reachability/version |
| `/containers/create?name=<n>` | POST | Create container (set `Binds`, `Privileged`) |
| `/containers/<id>/start` | POST | Start the created container |
| `/images/create?fromImage=alpine` | POST | Pull a base image |
| `/containers/<id>/logs?stdout=1` | GET | Read command output |

Create-container JSON keys of interest: `Image`, `Cmd`, `Binds` (`["/:/host"]`), `Privileged` (`true`), `HostConfig.PidMode` (`host`), `HostConfig.NetworkMode` (`host`).

## runC / Runtime Version Checks

| Command | Vulnerable Range | Patched |
|---------|------------------|---------|
| `runc --version` | 1.0.0-rc93 .. 1.1.11 (CVE-2024-21626) | >= 1.1.12 |
| `runc --version` | <= 1.2.7 / 1.3.2 / 1.4.0-rc.2 (2025 CVEs) | 1.2.8 / 1.3.3 / 1.4.0-rc.3 |
| `docker version --format '{{.Server.Version}}'` | < 25.0.2 | >= 25.0.2 |
| `containerd --version` | < 1.6.28 / 1.7.13 | >= 1.6.28 / 1.7.13 |

## Key Privileged-Escape Primitives

| File / Path | Use |
|-------------|-----|
| `/sys/fs/cgroup/.../release_agent` | Host command execution on cgroup empty (needs CAP_SYS_ADMIN) |
| `/proc/self/fd/7`, `/proc/self/fd/8` | Leaked host-cwd fd for CVE-2024-21626 |
| `/proc/sys/kernel/core_pattern` | `|/path/to/handler` runs as root on host on core dump |
| `/proc/sysrq-trigger` | Host kernel actions (DoS proof for 2025 CVEs) |
| `/etc/kubernetes/manifests/` | Drop a static pod manifest kubelet auto-runs |

## External References

- runC repo: https://github.com/opencontainers/runc
- amicontained: https://github.com/genuinetools/amicontained
- deepce: https://github.com/stealthcopter/deepce
- CDK: https://github.com/cdk-team/CDK
- Docker Engine API: https://docs.docker.com/engine/api/

---

## Standards and Controls

## MITRE ATT&CK

| Technique ID | Name | Tactic | Rationale |
|--------------|------|--------|-----------|
| T1611 | Escape to Host | Privilege Escalation | The core technique: breaking container isolation to execute on the host kernel/namespace. |
| T1610 | Deploy Container | Defense Evasion / Execution | Docker-socket escapes spawn a new privileged container mounting host root. |
| T1613 | Container and Resource Discovery | Discovery | Enumerating caps, namespaces, mounts to find a viable escape path. |
| T1068 | Exploitation for Privilege Escalation | Privilege Escalation | runC CVE exploitation (CVE-2024-21626, CVE-2025-31133/52565/52881). |

## NIST CSF 2.0

| ID | Name | Rationale |
|----|------|-----------|
| PR.PS-01 | Configuration management practices are established and applied | Hardening container runtime/pod config (no `--privileged`, no socket mount, no hostPath `/`) and keeping runC patched is the primary control against breakout. |

## Real CVEs Covered

| CVE | Runtime | Fixed In | Note |
|-----|---------|----------|------|
| CVE-2024-21626 | runC <=1.1.11 | runC 1.1.12, containerd 1.6.28/1.7.13, Docker 25.0.2 | "Leaky Vessels" host-cwd fd leak |
| CVE-2025-31133 | runC <=1.2.7/1.3.2/1.4.0-rc.2 | runC 1.2.8/1.3.3/1.4.0-rc.3 | `/dev/null` masked-path race |
| CVE-2025-52565 | runC <=1.2.7/1.3.2/1.4.0-rc.2 | runC 1.2.8/1.3.3/1.4.0-rc.3 | `/dev/console` bind-mount race |
| CVE-2025-52881 | runC <=1.2.7/1.3.2/1.4.0-rc.2 | runC 1.2.8/1.3.3/1.4.0-rc.3 | Arbitrary procfs write redirection |

## Official Resources

- runC security advisories: https://github.com/opencontainers/runc/security/advisories
- GHSA-cgrx-mc8f-2prm (2025 write gadgets): https://github.com/opencontainers/runc/security/advisories/GHSA-cgrx-mc8f-2prm
- GHSA-9493-h29p-rfm2 (2025 masked-path): https://github.com/opencontainers/runc/security/advisories/GHSA-9493-h29p-rfm2
- Palo Alto Leaky Vessels: https://www.paloaltonetworks.com/blog/cloud-security/leaky-vessels-vulnerabilities-container-escape/
- Sysdig runc 2025 escape blog: https://www.sysdig.com/blog/runc-container-escape-vulnerabilities
- HackTricks Docker Breakout: https://book.hacktricks.xyz/linux-hardening/privilege-escalation/docker-security/docker-breakout-privilege-escalation
