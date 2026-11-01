# Hardening docker Daemon Configuration

## API Reference

## daemon.json Location
- Linux: `/etc/docker/daemon.json`
- Windows: `C:\ProgramData\docker\config\daemon.json`

## Recommended daemon.json
```json
{
  "icc": false,
  "live-restore": true,
  "userland-proxy": false,
  "no-new-privileges": true,
  "userns-remap": "default",
  "log-driver": "json-file",
  "log-opts": {"max-size": "10m", "max-file": "3"},
  "tls": true,
  "tlsverify": true,
  "tlscacert": "/etc/docker/ca.pem",
  "tlscert": "/etc/docker/server-cert.pem",
  "tlskey": "/etc/docker/server-key.pem"
}
```

## CIS Docker Benchmark — Daemon Settings

| CIS # | Setting | Recommendation |
|-------|---------|---------------|
| 2.1 | `icc` | Set to `false` |
| 2.2 | `live-restore` | Set to `true` |
| 2.3 | `userland-proxy` | Set to `false` |
| 2.4 | `no-new-privileges` | Set to `true` |
| 2.6 | TLS | Enable with certificates |
| 2.8 | `userns-remap` | Set to `default` |
| 2.12 | Logging | Configure centralized logging |

## File Permission Checks

| File | Permissions |
|------|------------|
| `/etc/docker/daemon.json` | 644 |
| `/var/run/docker.sock` | 660 |
| `/etc/docker/certs.d/` | 444 |
| Docker service files | 644 |

## Docker Socket Security

### Check permissions
```bash
ls -la /var/run/docker.sock
# srw-rw---- 1 root docker 0 ... /var/run/docker.sock
```

### Restrict group access
```bash
chmod 660 /var/run/docker.sock
chown root:docker /var/run/docker.sock
```

## Content Trust (Image Signing)

### Enable globally
```bash
export DOCKER_CONTENT_TRUST=1
```

### In daemon.json
```json
{"content-trust": {"mode": "enforced"}}
```

## Docker Info Command
```bash
docker info --format '{{json .}}'
```

### Key Fields
| Field | Description |
|-------|-------------|
| `SecurityOptions` | seccomp, apparmor, userns |
| `LiveRestoreEnabled` | Live restore status |
| `RegistryConfig.InsecureRegistryCIDRs` | Insecure registries |
| `ServerVersion` | Docker version |

---

## Standards and Controls

## CIS Docker Benchmark v1.6

### Section 2: Docker Daemon Configuration

| Rule | Description | Status |
|------|-------------|--------|
| 2.1 | Run the Docker daemon as a non-root user | Rootless mode |
| 2.2 | Ensure network traffic is restricted between containers | icc: false |
| 2.3 | Ensure the logging level is set to info | log-level: info |
| 2.4 | Ensure Docker is allowed to make changes to iptables | iptables: true |
| 2.5 | Ensure insecure registries are not used | No --insecure-registry |
| 2.6 | Ensure aufs storage driver is not used | overlay2 driver |
| 2.7 | Ensure TLS authentication for Docker daemon is configured | tlsverify: true |
| 2.8 | Ensure the default ulimit is configured appropriately | default-ulimits set |
| 2.9 | Enable user namespace support | userns-remap: default |
| 2.10 | Ensure the default cgroup usage has been confirmed | cgroup-parent |
| 2.11 | Ensure base device size is not changed until needed | Default 10G |
| 2.12 | Ensure that authorization for Docker client commands is enabled | AuthZ plugin |
| 2.13 | Ensure centralized and remote logging is configured | log-driver |
| 2.14 | Ensure containers are restricted from acquiring new privileges | no-new-privileges |
| 2.15 | Ensure live restore is enabled | live-restore: true |
| 2.16 | Ensure Userland Proxy is disabled | userland-proxy: false |
| 2.17 | Ensure daemon-wide custom seccomp profile is applied | seccomp-profile |

## NIST SP 800-190
- Section 4.1.4: Configuration defects in container images
- Section 5.1: Image security - Content trust enforcement
- Section 5.3: Daemon hardening recommendations

## OWASP Docker Security Cheat Sheet
- Rule 0: Keep host and Docker up to date
- Rule 1: Do not expose the Docker daemon socket
- Rule 2: Set a user
- Rule 3: Limit capabilities
- Rule 4: Add no-new-privileges flag
- Rule 5: Disable inter-container communication
- Rule 6: Use Linux Security Module
- Rule 7: Limit resources
- Rule 8: Set filesystem and volumes to read-only
- Rule 9: Use static analysis tools
- Rule 10: Set log level to info

## Compliance Mappings

### PCI DSS v4.0
- Req 2.2: Develop configuration standards for all system components
- Req 2.2.1: System hardening procedures

### SOC 2
- CC6.1: Logical and physical access controls
- CC8.1: Change management

### FedRAMP
- CM-6: Configuration Settings
- CM-7: Least Functionality

---

## Workflows

## Phase 1: Baseline Assessment

```bash
# Check current Docker daemon configuration
docker info
docker system info --format '{{json .SecurityOptions}}'

# Check existing daemon.json
cat /etc/docker/daemon.json 2>/dev/null || echo "No daemon.json found"

# Run Docker Bench Security for baseline
docker run --rm --net host --pid host \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /etc:/etc:ro \
  docker/docker-bench-security 2>&1 | tee docker-bench-baseline.txt
```

## Phase 2: Apply Hardened Configuration

### Step 1 - Backup Current Config
```bash
sudo cp /etc/docker/daemon.json /etc/docker/daemon.json.bak 2>/dev/null
```

### Step 2 - Deploy Hardened daemon.json
```bash
sudo tee /etc/docker/daemon.json <<'EOF'
{
  "icc": false,
  "userns-remap": "default",
  "no-new-privileges": true,
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "5"
  },
  "storage-driver": "overlay2",
  "live-restore": true,
  "userland-proxy": false,
  "default-ulimits": {
    "nofile": { "Name": "nofile", "Hard": 65536, "Soft": 32768 },
    "nproc": { "Name": "nproc", "Hard": 4096, "Soft": 2048 }
  },
  "experimental": false,
  "metrics-addr": "127.0.0.1:9323"
}
EOF
```

### Step 3 - Restart Docker Daemon
```bash
sudo systemctl restart docker
sudo systemctl status docker
```

### Step 4 - Verify Settings
```bash
docker info | grep -E "(Remap|ICC|Live Restore|Security)"
```

## Phase 3: TLS Configuration

```bash
# Generate certificates (see SKILL.md for full commands)
# Deploy to /etc/docker/tls/

# Add TLS to daemon.json
sudo jq '. + {
  "tls": true,
  "tlsverify": true,
  "tlscacert": "/etc/docker/tls/ca.pem",
  "tlscert": "/etc/docker/tls/server-cert.pem",
  "tlskey": "/etc/docker/tls/server-key.pem",
  "hosts": ["unix:///var/run/docker.sock", "tcp://0.0.0.0:2376"]
}' /etc/docker/daemon.json | sudo tee /etc/docker/daemon.json.new
sudo mv /etc/docker/daemon.json.new /etc/docker/daemon.json

sudo systemctl restart docker
```

## Phase 4: Post-Hardening Validation

```bash
# Run Docker Bench again
docker run --rm --net host --pid host \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /etc:/etc:ro \
  docker/docker-bench-security 2>&1 | tee docker-bench-hardened.txt

# Compare results
diff docker-bench-baseline.txt docker-bench-hardened.txt
```

## Phase 5: Ongoing Monitoring

```bash
# Setup auditd rules for Docker
sudo auditctl -w /var/run/docker.sock -k docker
sudo auditctl -w /etc/docker -p wa -k docker-config
sudo auditctl -w /usr/bin/docker -k docker-binary
sudo auditctl -w /var/lib/docker -k docker-data

# Monitor Docker metrics
curl -s http://127.0.0.1:9323/metrics | head -20
```

---

## Working Template

## Pre-Hardening

- [ ] Document current daemon.json configuration
- [ ] Run Docker Bench Security baseline
- [ ] Identify running containers that may be affected
- [ ] Schedule maintenance window
- [ ] Backup existing /etc/docker/daemon.json

## CIS Docker Benchmark v1.6 - Daemon Checks

### Critical
- [ ] 2.2 - Disable inter-container communication (`"icc": false`)
- [ ] 2.9 - Enable user namespace remapping (`"userns-remap": "default"`)
- [ ] 2.14 - Restrict new privileges (`"no-new-privileges": true`)
- [ ] 2.7 - Configure TLS authentication (if remote access needed)

### High
- [ ] 2.6 - Use overlay2 storage driver
- [ ] 2.16 - Disable userland proxy
- [ ] 2.13 - Configure centralized logging
- [ ] 2.8 - Set default ulimits
- [ ] 2.17 - Apply custom seccomp profile

### Medium
- [ ] 2.15 - Enable live restore
- [ ] 2.1 - Consider rootless mode
- [ ] Docker socket permissions set to 660

## Post-Hardening Verification

- [ ] Docker daemon restarts successfully
- [ ] All containers start correctly
- [ ] Docker Bench shows improved score
- [ ] TLS connection works (if configured)
- [ ] Monitoring endpoints accessible
- [ ] Log rotation working

## Recommended daemon.json

```json
{
  "icc": false,
  "userns-remap": "default",
  "no-new-privileges": true,
  "log-driver": "json-file",
  "log-opts": { "max-size": "10m", "max-file": "5" },
  "storage-driver": "overlay2",
  "live-restore": true,
  "userland-proxy": false,
  "experimental": false
}
```

## Rollback Plan

1. Stop Docker daemon: `sudo systemctl stop docker`
2. Restore backup: `sudo cp /etc/docker/daemon.json.bak /etc/docker/daemon.json`
3. Start Docker daemon: `sudo systemctl start docker`
4. Verify containers: `docker ps`
