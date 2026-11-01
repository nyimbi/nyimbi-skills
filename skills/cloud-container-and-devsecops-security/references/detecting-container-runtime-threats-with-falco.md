# Detecting Container Runtime Threats With Falco

## API Reference

## Rule Object Fields

| Field | Required | Purpose |
|-------|----------|---------|
| `rule` | yes | Unique rule name |
| `desc` | yes | Human description |
| `condition` | yes | Falco filter expression that triggers the rule |
| `output` | yes | Alert message (supports `%field` interpolation) |
| `priority` | yes | EMERGENCY, ALERT, CRITICAL, ERROR, WARNING, NOTICE, INFO, DEBUG |
| `tags` | no | Categorization (e.g. MITRE IDs) |
| `enabled` | no | Toggle a rule (true/false) |
| `source` | no | Event source (syscall, k8s_audit) |

## Macro and List Objects

| Object | Keys | Purpose |
|--------|------|---------|
| `macro` | `condition` | Reusable condition fragment |
| `list` | `items` | Named value set used with `in (...)` |

## Key CLI Commands

| Command | Purpose |
|---------|---------|
| `falco --validate <file>` | Validate rule syntax without running |
| `falco -r <file>` | Run with a specific rules file |
| `falco -L` | List loaded rules |
| `falco -l <rule>` | Describe a single rule |
| `falco --list` | List supported fields |
| `falcoctl driver config --type modern_ebpf` | Set driver type |
| `falcoctl artifact install <name>` | Install a rules/plugin artifact |
| `falcoctl artifact list` | List available artifacts |

## Driver Types

| Driver | `driver.kind` | Notes |
|--------|---------------|-------|
| Modern eBPF | `modern_ebpf` | Default; built into binary; kernel >= 5.8 |
| Legacy eBPF | `ebpf` | CO-RE eBPF probe |
| Kernel module | `kmod` | Loadable kernel module |
| Auto | `auto` | falcoctl picks best available |

## Important Filter Fields

| Field | Description |
|-------|-------------|
| `evt.type` | Syscall name |
| `evt.dir` | `>` enter, `<` exit |
| `evt.is_open_read` / `evt.is_open_write` | open() intent |
| `proc.name` / `proc.cmdline` / `proc.pname` | Process / cmdline / parent |
| `container.id` / `container.name` / `container.image.repository` | Container identity |
| `container.privileged` | Privileged flag |
| `fd.name` / `fd.type` / `fd.num` | FD path / type / number |
| `user.name` / `user.uid` | Acting user |
| `k8s.pod.name` / `k8s.ns.name` | Kubernetes context |

## Configuration (falco.yaml)

| Key | Purpose |
|-----|---------|
| `rules_files` | List of rule files / dirs to load |
| `json_output` | Emit JSON for SIEM ingest |
| `priority` | Minimum priority to log |
| `outputs` / `http_output` / `program_output` | Alert sinks |

## External References

- Supported fields: https://falco.org/docs/reference/rules/supported-fields/
- Rule examples: https://falco.org/docs/reference/rules/examples/
- Configuration: https://falco.org/docs/reference/daemon/config-options/

---

## Standards and Controls

## MITRE ATT&CK

| Technique ID | Name | Tactic | Rationale |
|--------------|------|--------|-----------|
| T1611 | Escape to Host | Privilege Escalation | Falco rules detect the syscalls/files used in container breakout (release_agent, setns, privileged mount). |
| T1059.004 | Command and Scripting Interpreter: Unix Shell | Execution | Reverse-shell rule detects shells wired to network sockets in containers. |
| T1610 | Deploy Container | Defense Evasion / Execution | docker.sock access rule detects daemon-API container spawning. |
| T1543 | Create or Modify System Process | Persistence | Anomalous process/service creation inside containers. |
| T1071.001 | Application Layer Protocol: Web Protocols | Command and Control | Unexpected outbound connections from containers. |

## NIST CSF 2.0

| ID | Name | Rationale |
|----|------|-----------|
| DE.CM-01 | Networks and network services are monitored to find potentially adverse events | Falco continuously monitors syscall and network behavior at runtime, surfacing adverse container activity. |

## Official Resources

- Falco documentation: https://falco.org/docs/
- Custom ruleset guide: https://falco.org/docs/concepts/rules/custom-ruleset/
- Default rules: https://falco.org/docs/reference/rules/default-rules/
- falcosecurity/rules repo: https://github.com/falcosecurity/rules/blob/main/rules/falco_rules.yaml
- Falco Helm chart README: https://github.com/falcosecurity/charts/blob/master/charts/falco/README.md
- falcoctl: https://github.com/falcosecurity/falcoctl
- Falcosidekick: https://github.com/falcosecurity/falcosidekick

## Key Research

- Sysdig: "Detecting CVE-2025-22224 with Falco"
- Falco supported fields reference: https://falco.org/docs/reference/rules/supported-fields/
