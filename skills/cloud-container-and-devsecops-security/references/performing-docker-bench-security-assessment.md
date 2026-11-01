# Performing docker Bench Security Assessment

## API Reference

## Libraries Used
- **subprocess**: Run docker-bench-security container and docker inspect commands
- **json**: Parse docker inspect JSON output

## CLI Interface

```
python agent.py bench        # Run full docker-bench-security
python agent.py containers   # Check running container configurations
```

## Core Functions

### `run_docker_bench()`
Runs the docker/docker-bench-security container with host access for CIS benchmark checks.

### `parse_bench_output(output)`
Parses [WARN], [PASS], [NOTE] lines into structured findings with sections.

### `check_container_configs()`
Inspects all running containers for CIS Docker Benchmark violations.

### CIS Checks Performed on Containers

| Check | CIS ID | Severity |
|-------|--------|----------|
| Privileged mode | 5.4 | CRITICAL |
| Host PID namespace | 5.15 | HIGH |
| Host network namespace | 5.13 | HIGH |
| Dangerous capabilities | 5.3 | HIGH |
| Running as root | 4.1 | MEDIUM |
| Sensitive host mounts | 5.5 | HIGH |

## Dependencies
Docker must be installed and accessible. No Python packages required beyond stdlib.

---

## Standards and Controls

## CIS Docker Benchmark v1.8.0 Sections
| Section | Area | Checks |
|---------|------|--------|
| 1 | Host Configuration | Partition, users, audit rules |
| 2 | Docker Daemon | ICC, TLS, logging, seccomp, privileges |
| 3 | Docker Daemon Config Files | File permissions and ownership |
| 4 | Container Images | Non-root user, scanning, trusted images |
| 5 | Container Runtime | Capabilities, rootfs, resources, privileges |
| 6 | Docker Security Operations | Monitoring, CVE scanning |

## Scoring
- PASS: Check meets CIS recommendation
- FAIL: Check does not meet recommendation (remediation required)
- WARN: Check requires manual verification
- INFO: Informational, no scoring impact

---

## Workflows

## Assessment Workflow
```
[Run Docker Bench] --> [Parse Results] --> [Prioritize FAIL findings]
        |                    |                      |
        v                    v                      v
  Initial baseline    Export JSON           Group by section
  assessment          for tracking          and severity
        |                    |                      |
        +--------------------+----------------------+
                             |
                             v
                [Create Remediation Plan]
                             |
                             v
                [Apply Fixes] --> [Re-run Assessment] --> [Compare Scores]
```

---

## Working Template

## Host Information
| Field | Value |
|-------|-------|
| Hostname | |
| Docker Version | |
| OS | |
| Assessment Date | |

## Results Summary
| Status | Count |
|--------|-------|
| PASS | |
| FAIL | |
| WARN | |
| Score | % |

## Failed Checks Remediation
| Check ID | Description | Remediation | Owner | Status |
|----------|-------------|-------------|-------|--------|
| | | | | |
