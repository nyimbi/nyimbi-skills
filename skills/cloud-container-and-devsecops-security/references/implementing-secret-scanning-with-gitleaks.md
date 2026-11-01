# Implementing Secret Scanning With Gitleaks

## API Reference

## Libraries Used

| Library | Purpose |
|---------|---------|
| `subprocess` | Execute gitleaks CLI commands |
| `json` | Parse gitleaks JSON report output |
| `pathlib` | Handle repository and report file paths |
| `os` | Read `GITLEAKS_CONFIG` environment variable |

## Installation

```bash
# Install gitleaks binary
# macOS
brew install gitleaks

# Linux
curl -sSfL https://github.com/gitleaks/gitleaks/releases/latest/download/gitleaks_linux_x64 -o gitleaks
chmod +x gitleaks && sudo mv gitleaks /usr/local/bin/

# Docker
docker pull ghcr.io/gitleaks/gitleaks:latest
```

## CLI Commands

### Scan a Git Repository
```bash
gitleaks git --source=/path/to/repo --report-format=json --report-path=results.json
```

### Scan a Directory (Non-Git)
```bash
gitleaks dir --source=/path/to/code --report-format=json --report-path=results.json
```

### Scan from stdin
```bash
echo "aws_secret_access_key=AKIAIOSFODNN7EXAMPLE" | gitleaks stdin
```

### Key CLI Flags

| Flag | Description |
|------|-------------|
| `--source` | Path to repository or directory to scan |
| `--config`, `-c` | Path to custom gitleaks.toml config |
| `--report-format`, `-f` | Output format: `json`, `csv`, `junit`, `sarif` |
| `--report-path`, `-r` | Path to write the report file |
| `--baseline-path` | Ignore known findings from baseline file |
| `--exit-code` | Exit code when leaks found (default: 1) |
| `--redact` | Redact secrets in output (percent: 0-100) |
| `--verbose`, `-v` | Show verbose scan output |
| `--no-git` | Treat source as plain directory |
| `--log-level` | Log level: trace, debug, info, warn, error |
| `--max-target-megabytes` | Skip files larger than this size |

## Custom Configuration (.gitleaks.toml)

```toml
title = "Custom Gitleaks Config"

[extend]
useDefault = true  # Extend the default ruleset

[[rules]]
id = "custom-internal-token"
description = "Internal API token pattern"
regex = '''(?i)internal[_-]?token\s*[:=]\s*['"]?([a-zA-Z0-9]{32,})'''
tags = ["internal", "token"]
keywords = ["internal_token", "internal-token"]

[[rules]]
id = "custom-db-password"
description = "Database password in config"
regex = '''(?i)(db|database|mysql|postgres)[_-]?pass(word)?\s*[:=]\s*['"]?[^\s'"]{8,}'''
tags = ["database", "password"]

[rules.allowlist]
paths = ['''test/.*''', '''mock/.*''']
regexTarget = "line"
regexes = ['''(?i)example|placeholder|changeme|test''']

[[allowlist.paths]]
regex = '''vendor/.*'''

[[allowlist.commits]]
sha = "abc123def456"
```

## Python Integration

### Run Gitleaks and Parse Results
```python
import subprocess
import json
from pathlib import Path

def scan_repository(repo_path, config_path=None):
    cmd = [
        "gitleaks", "git",
        "--source", str(repo_path),
        "--report-format", "json",
        "--report-path", "/tmp/gitleaks-report.json",
        "--exit-code", "0",
    ]
    if config_path:
        cmd.extend(["--config", str(config_path)])

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

    report_path = Path("/tmp/gitleaks-report.json")
    if report_path.exists():
        with open(report_path) as f:
            findings = json.load(f)
        return findings
    return []
```

### Categorize Findings by Severity
```python
HIGH_SEVERITY_RULES = {
    "aws-access-key", "aws-secret-key", "gcp-api-key",
    "github-pat", "private-key", "generic-api-key",
}

def categorize_findings(findings):
    high, medium, low = [], [], []
    for f in findings:
        rule = f.get("RuleID", "")
        if rule in HIGH_SEVERITY_RULES:
            high.append(f)
        elif "password" in rule or "token" in rule:
            medium.append(f)
        else:
            low.append(f)
    return {"high": high, "medium": medium, "low": low}
```

## GitHub Actions Integration

```yaml
name: Gitleaks Secret Scan
on: [push, pull_request]
jobs:
  gitleaks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Output Format

```json
[
  {
    "Description": "Detected a Generic API Key",
    "StartLine": 42,
    "EndLine": 42,
    "StartColumn": 15,
    "EndColumn": 55,
    "Match": "REDACTED",
    "Secret": "REDACTED",
    "File": "config/settings.py",
    "Commit": "a1b2c3d4e5f6",
    "Author": "developer@example.com",
    "Date": "2025-01-15T10:30:00Z",
    "RuleID": "generic-api-key",
    "Tags": ["api", "key"],
    "Fingerprint": "a1b2c3d4:config/settings.py:generic-api-key:42"
  }
]
```

---

## Standards and Controls

## OWASP Top 10 - A07:2021 Identification and Authentication Failures

- Hardcoded credentials in source code enable unauthorized access
- Gitleaks detects API keys, passwords, tokens, and private keys before they reach repositories
- CWE-798: Use of Hard-coded Credentials is a direct mapping

## NIST SSDF (SP 800-218)

### PW.1: Design Software to Meet Security Requirements
- PW.1.1: Identify security requirements including credential management
- Secrets should never be stored in source code; use environment variables or secrets managers

### PS.1: Protect All Forms of Code
- PS.1.1: Store code securely with access controls and secret scanning
- Implement pre-commit hooks to prevent secrets from entering version control

### PS.2: Provide a Mechanism for Verifying Software Release Integrity
- Code signing and secret scanning ensure software releases do not contain embedded credentials

## CIS Software Supply Chain Security Guide

### Source Code Controls
- SC-1: Automated secret scanning on all commits
- SC-5: No hardcoded credentials in source repositories
- SC-6: Secrets detection integrated into CI/CD pipeline

## OWASP SAMM - Secure Build

### Maturity Level 1
- Scan repositories for common secret patterns using default rulesets
- Alert developers when secrets are detected in pull requests

### Maturity Level 2
- Custom rules for organization-specific secret patterns
- Pre-commit hooks prevent secrets from entering history
- Baseline management for legacy codebases

### Maturity Level 3
- Automated secret rotation workflow triggered by detection
- Correlation with secrets management systems for validation
- Historical scanning with git-filter-repo remediation

## PCI DSS v4.0

- Requirement 6.3.1: Security vulnerabilities identified through a defined process including code analysis
- Requirement 8.6.1: Secrets stored in code or configuration files must be protected
- Requirement 8.6.3: Passwords/passphrases for application and system accounts are protected against misuse

## SOC 2 Trust Service Criteria

- CC6.1: Logical access security over protected information assets including credential management
- CC6.7: Restrict transmission of data to authorized external parties (prevent credential leakage)

---

## Workflows

## Secret Detection Pipeline

```
Developer Workstation          CI/CD Pipeline              Security Response
     │                              │                           │
     ▼                              │                           │
┌──────────────┐                    │                           │
│ Pre-commit   │                    │                           │
│ Hook (local) │                    │                           │
└──────┬───────┘                    │                           │
       │                            │                           │
  ┌────┴────┐                       │                           │
  │         │                       │                           │
PASS      FAIL                      │                           │
  │     (blocked)                   │                           │
  ▼                                 │                           │
Push to                             │                           │
Remote                              │                           │
  │                                 ▼                           │
  │                        ┌──────────────┐                     │
  └───────────────────────>│ Gitleaks CI  │                     │
                           │ Scan (PR)    │                     │
                           └──────┬───────┘                     │
                                  │                             │
                            ┌─────┴─────┐                      │
                            │           │                       │
                          PASS        FAIL                      │
                            │     ┌─────┴──────┐               │
                            │     │ Block PR   │               │
                            │     │ + Alert    │──────────────>│
                            │     └────────────┘    ┌──────────┴──────┐
                            │                       │ Rotate Secret   │
                            │                       │ Update Baseline │
                            │                       │ Clean History   │
                            │                       └─────────────────┘
                            ▼
                    Merge Permitted
```

## Gitleaks Rule Configuration Deep Dive

### Rule Anatomy
```toml
[[rules]]
id = "rule-unique-identifier"          # Unique rule ID
description = "Human-readable desc"     # What this rule detects
regex = '''pattern'''                   # Detection regex
entropy = 3.5                           # Minimum entropy threshold (optional)
secretGroup = 1                         # Regex capture group containing secret
keywords = ["key1", "key2"]             # Fast pre-filter keywords
tags = ["aws", "credential"]            # Categorization tags
path = '''\.env$'''                     # Path filter regex (optional)
```

### Built-in Rule Categories
| Category | Example Rules | Count |
|----------|--------------|-------|
| Cloud Provider Keys | aws-access-key-id, gcp-service-account | 15+ |
| API Tokens | github-pat, gitlab-pat, slack-token | 20+ |
| Private Keys | private-key, rsa-private-key | 5+ |
| Database Credentials | generic-password, connection-string | 10+ |
| Service Tokens | stripe-api-key, sendgrid-api-key | 30+ |

### Entropy Scoring
- Entropy measures string randomness (Shannon entropy)
- Random-looking strings (API keys) have entropy > 3.5
- Regular English text has entropy around 2.0-3.0
- Setting entropy threshold reduces false positives on non-random strings
- Combine entropy with regex for highest accuracy

## Remediation Process

### Secret Rotation Checklist
1. Identify the exposed secret type and associated service
2. Log into the service provider and revoke the exposed credential
3. Generate a new credential with the same permissions
4. Store the new credential in a secrets manager (Vault, AWS SM, etc.)
5. Update all consuming services to use the new credential
6. Verify service functionality with the new credential
7. Update the Gitleaks baseline to remove the resolved finding
8. Optionally clean git history with git-filter-repo

### History Cleanup Decision Matrix
| Factor | Clean History | Keep History |
|--------|--------------|--------------|
| Secret is rotated | Optional | Acceptable |
| Repo is public | Required | Never |
| Compliance mandate | Required | Not compliant |
| Active contributor count | < 10 preferred | > 10 difficult |
| Secret exposure duration | Long (high risk) | Short (lower risk) |

---

## Working Template

## Pre-Commit Configuration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.21.2
    hooks:
      - id: gitleaks
        name: Detect secrets with Gitleaks
        entry: gitleaks protect --staged --verbose --redact
        language: golang
        pass_filenames: false
```

## Organization Gitleaks Configuration

```toml
# .gitleaks.toml
title = "Organization Secret Scanning Rules"

[extend]
useDefault = true

# ─── Custom Rules ───

[[rules]]
id = "internal-service-token"
description = "Internal service-to-service authentication token"
regex = '''(?i)(service[_-]?token|internal[_-]?key)["\s:=]+["']?([A-Za-z0-9_\-]{36,})["']?'''
entropy = 3.5
keywords = ["service_token", "service-token", "internal_key", "internal-key"]

[[rules]]
id = "database-url-with-password"
description = "Database connection URL with embedded password"
regex = '''(?i)(DATABASE_URL|DB_URL|SQLALCHEMY_DATABASE_URI)\s*=\s*["']?(postgres|mysql|mongodb)\+?[a-z]*://[^:]+:[^@]+@'''
keywords = ["DATABASE_URL", "DB_URL", "SQLALCHEMY_DATABASE_URI"]

[[rules]]
id = "encryption-key-hex"
description = "Encryption key in hexadecimal format"
regex = '''(?i)(encryption[_-]?key|aes[_-]?key|secret[_-]?key)\s*=\s*["']?([0-9a-fA-F]{32,64})["']?'''
entropy = 3.0
keywords = ["encryption_key", "aes_key", "secret_key"]

# ─── Allowlist ───

[allowlist]
description = "Global allowlist for false positive reduction"
paths = [
  '''(^|/)test(s)?/''',
  '''(^|/)spec(s)?/''',
  '''\.test\.(js|ts|py|go|rb)$''',
  '''\.spec\.(js|ts|py|go|rb)$''',
  '''(^|/)__tests__/''',
  '''(^|/)__mocks__/''',
  '''(^|/)fixtures/''',
  '''(^|/)testdata/''',
  '''(^|/)vendor/''',
  '''(^|/)node_modules/''',
  '''\.md$''',
  '''CHANGELOG'''
]
regexes = [
  '''(?i)EXAMPLE''',
  '''(?i)PLACEHOLDER''',
  '''(?i)CHANGEME''',
  '''(?i)your[-_]?(api[-_]?key|secret|token|password)''',
  '''(?i)test[-_]?(key|secret|token|password|credential)''',
  '''example\.com''',
  '''localhost''',
  '''0{8,}''',
  '''x{8,}'''
]

# Per-rule allowlists
[[rules.allowlist]]
description = "Allow AWS example keys"
regexes = ["AKIAIOSFODNN7EXAMPLE"]
```

## GitHub Actions Workflow

```yaml
# .github/workflows/secret-scanning.yml
name: Secret Scanning

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 6 * * *'

jobs:
  gitleaks:
    name: Gitleaks
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Install Gitleaks
        run: |
          GITLEAKS_VERSION="8.21.2"
          wget -qO- "https://github.com/gitleaks/gitleaks/releases/download/v${GITLEAKS_VERSION}/gitleaks_${GITLEAKS_VERSION}_linux_x64.tar.gz" | tar xz
          sudo mv gitleaks /usr/local/bin/

      - name: Run scan
        run: |
          if [ "${{ github.event_name }}" == "pull_request" ]; then
            gitleaks detect \
              --source . \
              --log-opts="${{ github.event.pull_request.base.sha }}..${{ github.sha }}" \
              --report-format sarif \
              --report-path gitleaks.sarif \
              --exit-code 1 \
              --verbose
          else
            gitleaks detect \
              --source . \
              --baseline-path .gitleaks-baseline.json \
              --report-format sarif \
              --report-path gitleaks.sarif \
              --exit-code 1 \
              --verbose
          fi

      - name: Upload SARIF
        if: always()
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: gitleaks.sarif
          category: gitleaks
```

## Incident Response Template for Exposed Secrets

```markdown
## Secret Exposure Incident Report

**Date Detected**: YYYY-MM-DD
**Detected By**: Gitleaks CI scan / Pre-commit hook / Manual review
**Repository**: org/repo-name
**Severity**: Critical / High

### Exposed Credential Details
- **Type**: [AWS Access Key | GitHub PAT | Database Password | etc.]
- **Rule ID**: [gitleaks rule that detected it]
- **File**: [path/to/file:line]
- **Commit**: [short SHA]
- **Author**: [email]
- **Date Committed**: [date]
- **Exposure Duration**: [time from commit to detection]

### Remediation Actions
- [ ] Credential revoked at service provider
- [ ] New credential generated and stored in secrets manager
- [ ] Consuming services updated to use new credential
- [ ] Service functionality verified
- [ ] Git history cleaned (if required)
- [ ] Baseline updated
- [ ] Root cause documented

### Root Cause
[Why was the secret committed? Missing pre-commit hook? Developer education gap?]

### Preventive Measures
[What changes prevent recurrence? Hook enforcement? Rule addition?]
```
