# Building Red Team C2 Infrastructure With Havoc

## API Reference

> For authorized penetration testing and lab environments only.

## Havoc Teamserver API
```
Base URL: https://{teamserver}:{port}/api/
Authorization: Bearer {token}
```

## Listener Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/listeners` | List active listeners |
| POST | `/api/listeners` | Create new listener |
| DELETE | `/api/listeners/{name}` | Remove listener |

## Agent (Demon) Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/agents` | List connected agents |
| POST | `/api/agents/{id}/command` | Task agent |
| GET | `/api/agents/{id}/output` | Get task output |

## HTTPS Listener Config
```json
{
  "name": "https-c2",
  "protocol": "Https",
  "host": "0.0.0.0",
  "port": 443,
  "hosts": ["c2.example.com"],
  "secure": true,
  "user_agent": "Mozilla/5.0 ..."
}
```

## SMB Listener Config
```json
{
  "name": "smb-pivot",
  "protocol": "Smb",
  "pipe_name": "\\\\.\\pipe\\mojo_ipc"
}
```

## Payload Generation
```json
POST /api/payloads/generate
{
  "listener": "https-c2",
  "arch": "x64",
  "format": "exe",
  "config": {
    "sleep": 5,
    "jitter": 20,
    "indirect_syscalls": true,
    "sleep_technique": "WaitForSingleObjectEx"
  }
}
```

## Payload Formats
| Format | Description |
|--------|-------------|
| `exe` | Windows PE executable |
| `dll` | DLL side-loading |
| `shellcode` | Raw shellcode |
| `service_exe` | Windows service binary |

## Agent Properties
| Field | Description |
|-------|-------------|
| `agent_id` | Unique identifier |
| `hostname` | Target hostname |
| `username` | Running user context |
| `os` | Operating system |
| `process_name` | Host process |
| `pid` | Process ID |
| `sleep` | Callback interval (seconds) |
| `last_callback` | Last check-in time |

---

## Standards and Controls

## MITRE ATT&CK Techniques

### Resource Development (TA0042)
- **T1583.001** - Acquire Infrastructure: Domains
- **T1583.003** - Acquire Infrastructure: Virtual Private Server
- **T1583.006** - Acquire Infrastructure: Web Services
- **T1587.001** - Develop Capabilities: Malware
- **T1587.003** - Develop Capabilities: Digital Certificates
- **T1608.001** - Stage Capabilities: Upload Malware
- **T1608.005** - Stage Capabilities: Link Target

### Command and Control (TA0011)
- **T1071.001** - Application Layer Protocol: Web Protocols (HTTP/HTTPS)
- **T1573.001** - Encrypted Channel: Symmetric Cryptography
- **T1573.002** - Encrypted Channel: Asymmetric Cryptography
- **T1090.001** - Proxy: Internal Proxy
- **T1090.002** - Proxy: External Proxy
- **T1090.004** - Proxy: Domain Fronting
- **T1105** - Ingress Tool Transfer
- **T1132.001** - Data Encoding: Standard Encoding
- **T1001** - Data Obfuscation
- **T1568.002** - Dynamic Resolution: Domain Generation Algorithms
- **T1571** - Non-Standard Port
- **T1572** - Protocol Tunneling

### Defense Evasion (TA0005)
- **T1055** - Process Injection
- **T1055.012** - Process Hollowing
- **T1620** - Reflective Code Loading
- **T1027** - Obfuscated Files or Information
- **T1497** - Virtualization/Sandbox Evasion
- **T1140** - Deobfuscate/Decode Files or Information

### Execution (TA0002)
- **T1059.001** - PowerShell
- **T1106** - Native API
- **T1129** - Shared Modules

## NIST References

- **NIST SP 800-115** - Section 4.3: Penetration Testing (authorized C2 usage)
- **NIST SP 800-53 Rev. 5** - CA-8: Penetration Testing controls
- **NIST SP 800-53 Rev. 5** - SI-4: Information System Monitoring (detection of C2)

## Havoc-Specific Detection Signatures

| Detection | Source | Rule |
|---|---|---|
| Default Havoc HTTP Headers | Network IDS | `alert http any any -> any any (msg:"Havoc C2 Default Headers"; content:"X-Havoc"; sid:1000001;)` |
| Demon Sleep Patterns | EDR | Periodic beaconing with consistent intervals +/- jitter |
| Named Pipe Patterns | Sysmon | EventID 17/18 with `\\.\pipe\` matching Havoc defaults |
| Default Teamserver Port | Firewall | TCP 40056 outbound |

## Compliance Context

Havoc C2 usage is only authorized under:
- Signed Rules of Engagement (RoE) documents
- Authorized penetration testing under PCI DSS 11.4, SOC 2 CC7.1
- TIBER-EU / CBEST threat-led penetration testing frameworks
- Bug bounty programs with explicit C2 authorization

---

## Workflows

## Infrastructure Deployment Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│              HAVOC C2 DEPLOYMENT WORKFLOW                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. DOMAIN & INFRASTRUCTURE PREPARATION (Week -4)                │
│     ├── Register domain names (aged 30+ days)                    │
│     ├── Submit domains for categorization (Bluecoat, Fortiguard) │
│     ├── Provision VPS instances (Teamserver + Redirector)        │
│     ├── Obtain SSL certificates (Let's Encrypt)                  │
│     └── Configure DNS A records                                  │
│                                                                  │
│  2. TEAMSERVER SETUP (Day 1)                                     │
│     ├── Install dependencies on Ubuntu VPS                       │
│     ├── Clone and build Havoc from source                        │
│     ├── Create teamserver profile (havoc.yaotl)                  │
│     │   ├── Configure operator credentials                       │
│     │   ├── Define listeners (HTTPS, SMB)                        │
│     │   ├── Set Demon agent parameters                           │
│     │   └── Configure malleable traffic profiles                 │
│     ├── Harden teamserver (iptables, fail2ban)                   │
│     └── Start teamserver with verbose logging                    │
│                                                                  │
│  3. REDIRECTOR CONFIGURATION (Day 1-2)                           │
│     ├── Install Nginx on redirector VPS                          │
│     ├── Configure SSL termination                                │
│     ├── Set up reverse proxy rules                               │
│     │   ├── Forward C2 URIs to teamserver                        │
│     │   └── Redirect non-matching traffic to legit site          │
│     ├── Configure access logging                                 │
│     └── Test end-to-end connectivity                             │
│                                                                  │
│  4. PAYLOAD DEVELOPMENT (Day 2-3)                                │
│     ├── Generate Demon shellcode via Havoc Client                │
│     ├── Develop custom loader (C/Rust/Nim)                       │
│     │   ├── AES-encrypt shellcode                                │
│     │   ├── Implement sleep obfuscation                          │
│     │   ├── Add sandbox checks                                   │
│     │   └── Use indirect syscalls                                │
│     ├── Test against AV/EDR in lab                               │
│     └── Package for delivery vector                              │
│                                                                  │
│  5. OPERATIONAL TESTING (Day 3-4)                                │
│     ├── Test beacon callback through full chain                  │
│     ├── Verify redirector filtering                              │
│     ├── Test sleep/jitter behavior                               │
│     ├── Validate post-exploitation modules                       │
│     └── Confirm kill switch functionality                        │
│                                                                  │
│  6. OPERATIONAL USE (Engagement period)                          │
│     ├── Deploy payloads via approved vectors                     │
│     ├── Manage sessions through Havoc Client                     │
│     ├── Execute post-exploitation tasks                          │
│     ├── Maintain operator logs                                   │
│     └── Monitor infrastructure health                            │
│                                                                  │
│  7. TEAR-DOWN (Post-engagement)                                  │
│     ├── Remove all implants from target systems                  │
│     ├── Archive engagement logs                                  │
│     ├── Destroy VPS instances                                    │
│     ├── Release domain names                                     │
│     └── Provide IOCs to client for deconfliction                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Havoc Listener Configuration Decision Tree

```
Select Listener Type
│
├── External (Internet-facing targets)?
│   ├── HTTPS Listener
│   │   ├── Use valid SSL certificate
│   │   ├── Configure malleable URIs
│   │   ├── Set User-Agent to match target
│   │   └── Route through redirector
│   └── HTTP Listener (lab only)
│       └── Never use in production operations
│
├── Internal (post-initial access)?
│   ├── SMB Listener (named pipe)
│   │   ├── For workstation-to-workstation pivoting
│   │   └── No direct internet connectivity needed
│   └── TCP Listener
│       └── For direct internal connections
│
└── Advanced?
    └── External C2 Listener
        ├── Custom protocol over DNS
        ├── Domain fronting via CDN
        └── Third-party service channels
```

## Terraform Deployment Template

```hcl
# main.tf - Automated Havoc C2 Infrastructure
provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "teamserver" {
  ami           = "ami-0c7217cdde317cfec"  # Ubuntu 22.04
  instance_type = "t3.medium"
  key_name      = var.ssh_key_name

  vpc_security_group_ids = [aws_security_group.teamserver_sg.id]

  user_data = file("scripts/install_havoc.sh")

  tags = {
    Name = "havoc-teamserver"
  }
}

resource "aws_instance" "redirector" {
  ami           = "ami-0c7217cdde317cfec"
  instance_type = "t3.micro"
  key_name      = var.ssh_key_name

  vpc_security_group_ids = [aws_security_group.redirector_sg.id]

  user_data = file("scripts/install_redirector.sh")

  tags = {
    Name = "havoc-redirector"
  }
}

resource "aws_security_group" "teamserver_sg" {
  name = "havoc-teamserver-sg"

  ingress {
    from_port   = 40056
    to_port     = 40056
    protocol    = "tcp"
    cidr_blocks = [var.operator_ip]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [aws_instance.redirector.public_ip]
  }
}

resource "aws_security_group" "redirector_sg" {
  name = "havoc-redirector-sg"

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

## OPSEC Checklist

- [ ] Domains aged 30+ days before use
- [ ] Domains categorized in web proxies
- [ ] Valid SSL certificates installed
- [ ] Teamserver port (40056) firewalled to operator IPs only
- [ ] Redirector configured to filter non-C2 traffic
- [ ] Malleable C2 profile customized (URIs, headers, user-agent)
- [ ] Demon sleep set to 10+ seconds with 30%+ jitter
- [ ] Payload tested against target AV/EDR in lab
- [ ] Kill date set on all payloads
- [ ] Operator logs enabled and encrypted
- [ ] Emergency deconfliction process documented

---

## Working Template

## Engagement Details

| Field | Value |
|---|---|
| Engagement ID | RT-YYYY-XXX |
| Client | [Organization] |
| Operators | [Names] |
| Start Date | YYYY-MM-DD |
| End Date | YYYY-MM-DD |
| Kill Date | YYYY-MM-DD |

## Infrastructure Inventory

### Teamserver

| Field | Value |
|---|---|
| Provider | [AWS/DigitalOcean/Linode] |
| IP Address | X.X.X.X |
| OS | Ubuntu 22.04 LTS |
| Port | 40056 |
| Havoc Version | 0.7 |
| Access | SSH Key: [key name] |

### Redirector(s)

| Name | Provider | IP | Domain | SSL Cert | Status |
|---|---|---|---|---|---|
| Redirector-1 | [Provider] | X.X.X.X | c2.domain.com | Let's Encrypt | Active |
| Redirector-2 | [Provider] | X.X.X.X | cdn.domain2.com | Let's Encrypt | Standby |

### Domains

| Domain | Purpose | Registered | Aged | Categorized | SSL |
|---|---|---|---|---|---|
| c2.domain.com | Primary C2 | YYYY-MM-DD | Yes (45 days) | Business | Yes |
| cdn.domain2.com | Backup C2 | YYYY-MM-DD | Yes (60 days) | Technology | Yes |
| phish.domain3.com | Phishing | YYYY-MM-DD | Yes (30 days) | Uncategorized | Yes |

## Havoc Profile Configuration

```yaml
Teamserver:
  Host: "0.0.0.0"
  Port: 40056

Operators:
  - Username: operator1
    Password: [REDACTED]
  - Username: operator2
    Password: [REDACTED]

Listeners:
  - Name: "Primary HTTPS"
    Type: HTTPS
    Host: c2.domain.com
    Port: 443
    URIs: ["/api/v2/auth", "/api/v2/status", "/content/images/gallery"]
    User-Agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    Jitter: 30%

  - Name: "SMB Pivot"
    Type: SMB
    PipeName: "\\ntsvcs"

Demon:
  Sleep: 10
  Jitter: 30
  Spawn64: "C:\\Windows\\System32\\notepad.exe"
  Spawn32: "C:\\Windows\\SysWOW64\\notepad.exe"
```

## Payload Inventory

| Payload | Format | Listener | Arch | Hash (SHA256) | Delivery |
|---|---|---|---|---|---|
| stage1.bin | Shellcode | Primary HTTPS | x64 | [hash] | Custom loader |
| beacon.dll | DLL | Primary HTTPS | x64 | [hash] | DLL sideloading |
| pivot.exe | Service EXE | SMB Pivot | x64 | [hash] | Lateral movement |

## OPSEC Checklist

### Pre-Engagement
- [ ] Domains registered 30+ days before engagement start
- [ ] Domains categorized in Bluecoat, Fortiguard, Palo Alto
- [ ] SSL certificates obtained from trusted CA (not self-signed)
- [ ] Teamserver hardened (SSH keys only, fail2ban, UFW)
- [ ] Redirector filtering non-C2 traffic to legitimate site
- [ ] Malleable profile customized (URIs, headers, user-agent)
- [ ] Payloads tested against target AV/EDR in isolated lab
- [ ] Kill date configured on all payloads
- [ ] Operator logs enabled and encrypted at rest

### During Engagement
- [ ] Beacon sleep/jitter appropriate for operation phase
- [ ] No default Havoc indicators in network traffic
- [ ] Post-exploitation tools loaded in-memory only
- [ ] Named pipes and service names randomized
- [ ] Token manipulation used instead of credential replay where possible

### Post-Engagement
- [ ] All Demon sessions terminated
- [ ] All persistence mechanisms removed from target
- [ ] All payloads removed from target systems
- [ ] Teamserver logs archived and encrypted
- [ ] VPS instances destroyed
- [ ] Domains released or parked
- [ ] IOC list provided to client

## Emergency Procedures

| Scenario | Action |
|---|---|
| Burned domain | Switch to backup redirector |
| Detected implant | Sleep beacon to 24h, assess exposure |
| Teamserver compromise | Kill all sessions, rotate infrastructure |
| Client emergency stop | Execute `killall` on all active Demons |
| Legal escalation | Contact [Legal Contact] at [phone] |

## Operator Communication

| Channel | Purpose |
|---|---|
| Signal Group | Real-time coordination |
| Encrypted Email | Reports and documentation |
| Havoc Chat | In-tool session coordination |
| Emergency Phone | [Phone number] for critical issues |
