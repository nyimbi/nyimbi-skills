# Performing Sca Dependency Scanning With Snyk

## API Reference

## Snyk CLI Commands

### snyk test
Scans project dependencies for known vulnerabilities.

```bash
snyk test --json --severity-threshold=high
snyk test --json --all-projects          # Monorepo support
snyk test --json --file=package-lock.json
```

Exit codes:
- 0: No vulnerabilities found
- 1: Vulnerabilities found
- 2: Failure (missing manifest, auth error)

### snyk monitor
Creates a project snapshot for continuous monitoring on snyk.io.

```bash
snyk monitor --json --project-name="my-app"
```

### snyk auth
Authenticate with Snyk API token.

```bash
snyk auth <API_TOKEN>
export SNYK_TOKEN=<API_TOKEN>
```

## JSON Output Structure

### Test Result Fields

| Field | Type | Description |
|-------|------|-------------|
| `vulnerabilities` | array | List of vulnerability objects |
| `ok` | boolean | True if no vulns found |
| `dependencyCount` | int | Total dependencies scanned |
| `packageManager` | string | npm, pip, maven, etc. |
| `uniqueCount` | int | Unique vulnerability count |

### Vulnerability Object

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Snyk vulnerability ID (e.g., `SNYK-JS-LODASH-590103`) |
| `title` | string | Human-readable title |
| `severity` | string | critical, high, medium, low |
| `cvssScore` | float | CVSS v3.1 score (0-10) |
| `packageName` | string | Affected package name |
| `version` | string | Installed version |
| `fixedIn` | array | Versions with fix available |
| `exploit` | string | Exploit maturity: Mature, Proof of Concept, Not Defined |
| `isUpgradable` | boolean | Can be fixed by upgrading direct dependency |
| `isPatchable` | boolean | Snyk patch available |
| `from` | array | Dependency path from root |

## SARIF Integration

Snyk results can be converted to SARIF 2.1.0 for GitHub Code Scanning. The SARIF schema is at:
`https://raw.githubusercontent.com/oasis-tcs/sarif-spec/main/sarif-2.1/schema/sarif-schema-2.1.0.json`

## Severity Mapping

| Snyk Severity | CVSS Range | SARIF Level |
|---------------|-----------|-------------|
| critical | 9.0 - 10.0 | error |
| high | 7.0 - 8.9 | error |
| medium | 4.0 - 6.9 | warning |
| low | 0.1 - 3.9 | warning |

## CLI Usage

```bash
python agent.py --project /app --severity high --max-critical 0 --max-high 5 --output report.json
```

---

## Standards and Controls

## OWASP Top 10 - A06:2021 Vulnerable and Outdated Components

- Applications using components with known vulnerabilities may be exploitable
- SCA tools like Snyk identify vulnerable versions and provide upgrade paths
- Includes both direct and transitive dependency scanning

## NIST SSDF (SP 800-218)

### PW.4: Reuse Existing, Well-Secured Software
- PW.4.1: Verify that acquired software meets security requirements
- PW.4.2: Review, analyze, and test software to identify vulnerabilities
- SCA scanning of all third-party components before integration

### PW.4.4: Maintain Provenance Data
- Track the origin and version of all third-party software components
- Snyk monitor provides continuous tracking of dependency versions

## CIS Software Supply Chain Security

### Dependencies (DP) Controls
- DP-1: Pin dependencies to specific versions
- DP-2: Automate dependency vulnerability scanning in CI/CD
- DP-3: Review and approve new dependency additions
- DP-4: Monitor deployed dependencies for newly disclosed vulnerabilities

## OWASP SAMM - Software Security

### Security Testing - Maturity Level 1
- Automated dependency scanning using default configurations
- Visibility of vulnerable components to development teams

### Security Testing - Maturity Level 2
- Custom policies for severity thresholds and license compliance
- Automated fix PRs for upgradable vulnerabilities
- Tracking of exploit maturity to prioritize remediation

### Security Testing - Maturity Level 3
- Reachability analysis to identify actually exploitable vulnerabilities
- Integration with vulnerability management for SLA tracking
- Correlation with runtime monitoring for risk-based prioritization

## PCI DSS v4.0

- 6.2.4: Use automated methods to prevent common software attacks
- 6.3.2: Maintain an inventory of custom and third-party software components
- 6.3.3: Software components not needed for operation removed or identified

## Executive Order 14028 (US Federal)

- Section 4(e): Agencies shall employ automated tools for continuous monitoring of vulnerabilities in software
- SBOM requirement: All software suppliers must provide SBOMs listing all components including open-source
- Aligns with Snyk's SBOM generation and continuous monitoring capabilities

## License Compliance Framework

| License Type | Risk Level | Policy | Examples |
|--------------|------------|--------|----------|
| Permissive | Low | Auto-approve | MIT, BSD-2, BSD-3, ISC, Apache-2.0 |
| Weak Copyleft | Medium | Review | LGPL-2.1, LGPL-3.0, MPL-2.0 |
| Strong Copyleft | High | Restrict | GPL-2.0, GPL-3.0, AGPL-3.0 |
| Unknown/Custom | High | Manual Review | Proprietary, SSPL, BSL |

---

## Workflows

## Dependency Scanning Pipeline

```
Code Push / PR
       │
       ▼
┌──────────────────┐
│ Install Deps     │
│ (npm ci, pip     │
│  install, etc.)  │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Snyk Test        │──── Report JSON ───> Artifact Storage
│ (vuln scan)      │
└──────┬───────────┘
       │
  ┌────┴────┐
  │         │
PASS      FAIL ──────> PR Comment with vuln details
  │                     │
  │                     ▼
  │              ┌──────────────┐
  │              │ Snyk Fix PR  │
  │              │ (auto-gen)   │
  │              └──────────────┘
  ▼
┌──────────────────┐
│ Snyk Monitor     │
│ (continuous)     │
└──────┬───────────┘
       │
       ▼
  Ongoing alerts for
  new disclosures
```

## Snyk CLI Command Reference

### Scanning Commands
```bash
# Basic vulnerability test
snyk test

# Test with severity filter
snyk test --severity-threshold=high

# Test with exploit maturity filter
snyk test --severity-threshold=high

# Test specific manifest
snyk test --file=package-lock.json

# Test all projects in monorepo
snyk test --all-projects

# Test with dev dependencies excluded
snyk test --production

# Output in JSON
snyk test --json --json-file-output=results.json

# Output in SARIF
snyk test --sarif --sarif-file-output=results.sarif
```

### Monitoring Commands
```bash
# Monitor project for new vulnerabilities
snyk monitor --project-name="my-app-prod"

# Monitor specific branch
snyk monitor --target-reference=main

# Monitor with tags
snyk monitor --project-tags=env=production,team=platform
```

### Fix Commands
```bash
# Preview available fixes
snyk fix --dry-run

# Apply fixes to direct dependencies
snyk fix

# Apply fixes including dev dependencies
snyk fix --dev
```

## Vulnerability Prioritization Matrix

| Factor | Score Weight | Description |
|--------|-------------|-------------|
| CVSS Score | 30% | Base vulnerability severity |
| Exploit Maturity | 25% | Mature > POC > No Known Exploit |
| Reachability | 20% | Function called > Imported > Present |
| Fix Availability | 15% | Upgrade available > Patch > None |
| Dependency Depth | 10% | Direct > Transitive (1 hop) > Deep transitive |

## Snyk Integration Options

| Platform | Integration Method | Features |
|----------|--------------------|----------|
| GitHub | GitHub App | Auto-scan PRs, fix PRs, SARIF upload |
| GitLab | GitLab Integration | MR comments, dependency scanning |
| Jenkins | Snyk Plugin | Pipeline step, HTML reports |
| Azure DevOps | Extension | Pipeline task, dashboard widget |
| Bitbucket | Bitbucket App | PR checks, fix PRs |
| CLI | npm/binary | Local scanning, CI/CD integration |

## Remediation Strategy by Vulnerability Type

### Direct Dependency Vulnerability
1. Check if upgrade is available: `snyk test --json | jq '.vulnerabilities[] | select(.isUpgradable)'`
2. If upgradable: run `snyk fix` or manually upgrade
3. Verify no breaking changes in the upgrade
4. If not upgradable: check for patch or accept risk with ignore

### Transitive Dependency Vulnerability
1. Identify the dependency chain: `snyk test --json | jq '.vulnerabilities[].from'`
2. Check if upgrading the direct dependency resolves it
3. If not: use version overrides in package manager
4. npm: `overrides` in package.json
5. Maven: `dependencyManagement` in pom.xml
6. Gradle: `constraints` in build.gradle
7. Poetry: `tool.poetry.extras` or constraint resolution

---

## Working Template

## GitHub Actions: Multi-Language SCA Pipeline

```yaml
# .github/workflows/sca-scanning.yml
name: SCA Dependency Scan

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
    paths:
      - 'package*.json'
      - 'requirements*.txt'
      - 'Pipfile*'
      - 'pom.xml'
      - 'build.gradle*'
      - 'go.mod'
      - 'Gemfile*'

jobs:
  snyk-node:
    name: Snyk Node.js
    runs-on: ubuntu-latest
    if: hashFiles('package.json') != ''
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci
      - uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high --fail-on=upgradable

  snyk-python:
    name: Snyk Python
    runs-on: ubuntu-latest
    if: hashFiles('requirements.txt') != ''
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: pip install -r requirements.txt
      - uses: snyk/actions/python-3.10@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high

  monitor:
    name: Snyk Monitor
    needs: [snyk-node, snyk-python]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          command: monitor
          args: --all-projects
```

## Snyk Policy File

```yaml
# .snyk
version: v1.25.0
ignore:
  # Accepted risk with documented justification and expiry
  SNYK-JS-LODASH-1018905:
    - '*':
        reason: "Not exploitable: user input never reaches _.template()"
        expires: 2026-06-01T00:00:00.000Z
        created: 2026-02-23T00:00:00.000Z

patch: {}
```

## Snyk Configuration for License Compliance

```json
{
  "org_settings": {
    "license_policy": {
      "approved": ["MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "Unlicense", "0BSD"],
      "review_required": ["LGPL-2.1", "LGPL-3.0", "MPL-2.0", "CDDL-1.0"],
      "restricted": ["GPL-2.0", "GPL-3.0", "AGPL-3.0", "SSPL-1.0"],
      "severity_for_unknown": "high"
    }
  }
}
```

## OWASP Dependency-Check Alternative (Free)

```yaml
# .github/workflows/dependency-check.yml
name: OWASP Dependency Check

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 8 * * 1'

jobs:
  dependency-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run OWASP Dependency-Check
        uses: dependency-check/Dependency-Check_Action@main
        with:
          project: 'my-app'
          path: '.'
          format: 'HTML'
          args: >
            --failOnCVSS 7
            --enableRetired
      - name: Upload report
        uses: actions/upload-artifact@v4
        with:
          name: dependency-check-report
          path: reports/
```
