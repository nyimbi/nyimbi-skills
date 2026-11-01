# Detecting Malicious Npm Packages

## API Reference

## GuardDog (DataDog/guarddog)

Install: `pip install guarddog`  |  Docker: `ghcr.io/datadog/guarddog`

### Subcommands
| Command | Description |
|---------|-------------|
| `guarddog npm scan <pkg>` | Scan latest version from registry. |
| `guarddog npm scan <pkg> --version X.Y.Z` | Scan a specific version. |
| `guarddog npm scan <path.tgz \| dir>` | Scan a local tarball or extracted directory. |
| `guarddog npm verify <package.json>` | Scan every dependency in a manifest. |
| `guarddog pypi scan <pkg>` | Same for PyPI. |
| `guarddog go scan <module>` / `guarddog go verify go.mod` | Go modules. |
| `guarddog rubygems scan <gem>` | RubyGems. |

### Common flags
| Flag | Description |
|------|-------------|
| `--output-format=json` | Machine-readable JSON. |
| `--output-format=sarif` | SARIF for GitHub code scanning. |
| `--rules <rule>` (repeatable) | Run only the named rule(s). |
| `--exclude-rules <rule>` | Exclude the named rule(s). |
| `--log-level debug` | Verbose diagnostics. |

### Key npm heuristics
| Rule | Detects |
|------|---------|
| `npm-install-script` | preinstall/install/postinstall lifecycle scripts. |
| `npm-serialize-environment` | Exfiltration of environment variables. |
| `npm-exec-base64` | eval of base64-decoded payloads. |
| `npm-silent-process-execution` | Silent child-process execution. |
| `npm-obfuscation` | Common obfuscation patterns. |
| `shady-links` | Suspicious URLs in code. |
| `typosquatting` | Name similar to a popular package. |
| `potentially_compromised_email_domain` | Maintainer email on a lapsed domain. |

## OSV-Scanner

| Command | Description |
|---------|-------------|
| `osv-scanner --lockfile=package-lock.json` | Match pinned versions to OSV advisories incl. `MAL-` malicious entries. |
| `osv-scanner -r <dir>` | Recursively scan a directory. |
| `osv-scanner --format json` | JSON output. |

## npm acquisition (no execution)

| Command | Description |
|---------|-------------|
| `npm pack <pkg>@<ver>` | Download tarball without installing. |
| `npm view <pkg>@<ver> dist.tarball` | Print the tarball URL. |
| `npm install --ignore-scripts` | Install while skipping lifecycle scripts. |
| `jq '.scripts' package/package.json` | List lifecycle hooks. |

---

## Standards and Controls

## MITRE ATT&CK

| ID | Name | Rationale |
|----|------|-----------|
| T1195.002 | Supply Chain Compromise: Compromise Software Supply Chain | Core technique — trojanized package shipped through the npm registry. |
| T1059.007 | Command and Scripting Interpreter: JavaScript | Install scripts and module code run attacker JavaScript on the victim. |
| T1552.001 | Unsecured Credentials: Credentials In Files | Packages harvest `.npmrc`, `.env`, SSH keys, and cloud credential files. |
| T1041 | Exfiltration Over C2 Channel | Stolen data is POSTed to attacker HTTP(S) endpoints. |
| T1027 | Obfuscated Files or Information | base64/eval/hex obfuscation conceals the payload. |

## NIST Cybersecurity Framework 2.0

| ID | Name | Rationale |
|----|------|-----------|
| DE.CM-09 | Computing hardware and software, runtime environments, and their data are monitored to find potentially adverse events | Static + dynamic triage of npm packages and lockfiles is the monitoring control that surfaces malicious dependencies. |

## Supporting Standards

- **OWASP Top 10 CI/CD Security Risks — CICD-SEC-03: Dependency Chain Abuse.** Malicious package ingestion is a primary dependency-chain abuse vector.
- **NIST SP 800-218 (SSDF) — PW.4 / PS.3.** Reuse and verify the integrity of acquired software components; triaging packages satisfies the verification practice.
- **SLSA provenance.** Verifying build provenance reduces the chance of consuming a tampered or republished package.
