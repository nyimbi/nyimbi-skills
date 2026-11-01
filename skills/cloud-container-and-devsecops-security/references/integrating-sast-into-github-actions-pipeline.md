# Integrating Sast Into Github Actions Pipeline

## API Reference

## Semgrep CLI

### Installation
```bash
pip install semgrep
```

### Scan Commands
```bash
semgrep scan --config auto --json .           # Auto-detect rules
semgrep scan --config p/owasp-top-ten --json . # OWASP rules
semgrep scan --config p/ci --sarif .           # CI-optimized rules
```

### JSON Output Structure
```json
{"results": [{"check_id": "rule-id", "path": "file.py",
  "start": {"line": 10}, "extra": {"severity": "ERROR",
  "message": "...", "metadata": {"cwe": ["CWE-89"], "owasp": ["A03"]}}}]}
```

### Severity Levels
| Level | Action |
|-------|--------|
| ERROR | Block merge |
| WARNING | Require review |
| INFO | Advisory only |

## GitHub Actions Integration

### Semgrep Action
```yaml
- uses: returntocorp/semgrep-action@v1
  with:
    config: auto
    generateSarif: "1"
```

### SARIF Upload
```yaml
- uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: semgrep.sarif
```

### SARIF 2.1.0 Schema
| Field | Description |
|-------|-------------|
| `runs[].tool.driver.name` | Scanner name |
| `runs[].tool.driver.rules` | Rule definitions |
| `runs[].results` | Finding instances |
| `results[].ruleId` | Matching rule ID |
| `results[].level` | `error`, `warning`, `note` |

## References
- Semgrep: https://semgrep.dev/docs/
- GitHub Code Scanning: https://docs.github.com/en/code-security/code-scanning
- SARIF spec: https://docs.oasis-open.org/sarif/sarif/v2.1.0/

---

## Standards and Controls

## OWASP SAMM - Verification: Security Testing

### Maturity Level 1
- Perform automated SAST scanning with default rulesets on all application code
- Results are visible to development teams through IDE or CI/CD integration

### Maturity Level 2
- Customize SAST rules to reduce false positives below 20%
- Track and triage all findings with defined SLAs per severity
- Integrate SAST results into a centralized vulnerability management system

### Maturity Level 3
- Correlate SAST findings with DAST and SCA results for comprehensive coverage
- Measure and improve detection accuracy through benchmarking against known vulnerabilities
- Custom rules cover organization-specific vulnerability patterns and deprecated APIs

## NIST SSDF (SP 800-218) - Produce Well-Secured Software

### PW.7: Review and Analyze Code
- PW.7.1: Determine whether SAST tools should be used and select appropriate tools
- PW.7.2: Use SAST tools to analyze source code and identify vulnerabilities
- Configure tools to analyze code for compliance with secure coding standards

### PW.8: Test Executable Code
- Integration of SAST into CI/CD ensures code is tested before deployment
- Findings are tracked and remediated according to organizational policy

## CIS Software Supply Chain Security Guide

### Source Code (SC) Controls
- SC-2: Enforce branch protection requiring SAST checks to pass
- SC-3: Require code review in addition to automated scanning
- SC-4: Automate security testing in the build pipeline

### Build (BD) Controls
- BD-1: Define and enforce security requirements for build processes
- BD-2: Integrate multiple security testing tools for defense in depth

## OWASP Top 10 Coverage Matrix

| OWASP Category | CodeQL | Semgrep | Combined |
|----------------|--------|---------|----------|
| A01: Broken Access Control | Partial | Yes | Yes |
| A02: Cryptographic Failures | Yes | Yes | Yes |
| A03: Injection | Yes | Yes | Yes |
| A04: Insecure Design | No | Partial | Partial |
| A05: Security Misconfiguration | Partial | Yes | Yes |
| A06: Vulnerable Components | No | No | No (Use SCA) |
| A07: Auth Failures | Yes | Yes | Yes |
| A08: Software Integrity | No | Partial | Partial |
| A09: Logging Failures | Partial | Yes | Yes |
| A10: SSRF | Yes | Yes | Yes |

## PCI DSS v4.0 Mapping

- Requirement 6.2.4: Software engineering techniques or automated methods prevent or mitigate common software attacks
- Requirement 6.3.2: An inventory of bespoke and custom software and third-party software components is maintained
- Requirement 6.5.4: SAST tools are run as part of the software development lifecycle

## SOC 2 Trust Service Criteria

- CC7.1: Deploy detection and monitoring mechanisms for anomalies indicative of actual or attempted attacks
- CC8.1: Authorize, design, develop or acquire, configure, document, test, approve, and implement changes to infrastructure, data, software, and procedures

---

## Workflows

## End-to-End SAST Integration Workflow

```
Developer Push/PR
       │
       ▼
┌──────────────────┐
│ GitHub Actions    │
│ Trigger           │
└──────┬───────────┘
       │
       ├──────────────────────┐
       ▼                      ▼
┌──────────────┐    ┌──────────────┐
│ CodeQL Init  │    │ Semgrep CI   │
│ + Autobuild  │    │ + Custom     │
│ + Analyze    │    │   Rules      │
└──────┬───────┘    └──────┬───────┘
       │                    │
       ▼                    ▼
┌──────────────┐    ┌──────────────┐
│ SARIF Upload │    │ SARIF Upload │
│ (CodeQL)     │    │ (Semgrep)    │
└──────┬───────┘    └──────┬───────┘
       │                    │
       └──────────┬─────────┘
                  ▼
       ┌──────────────────┐
       │ GitHub Security  │
       │ Tab / Dashboard  │
       └──────┬───────────┘
              │
              ▼
       ┌──────────────────┐
       │ Branch Protection│
       │ Quality Gate     │
       └──────┬───────────┘
              │
    ┌─────────┴──────────┐
    ▼                    ▼
 PASS: Merge          FAIL: Block
 Permitted            + Notify Dev
```

## CodeQL Analysis Deep Dive

### Database Creation Phase
1. CodeQL extracts source code into a relational database
2. For compiled languages (Java, C++, C#, Go), the build process is intercepted
3. For interpreted languages (Python, JavaScript, Ruby), source files are parsed directly
4. The database captures the full AST, data flow, and control flow of the program

### Query Execution Phase
1. Security queries analyze the database for known vulnerability patterns
2. Taint tracking follows data from untrusted sources to dangerous sinks
3. Dataflow analysis tracks variable assignments across method boundaries
4. Results are deduplicated and ranked by confidence and severity

### Query Suites
- **default**: Core security queries with high precision and low false positive rate
- **security-extended**: Additional queries covering more vulnerability types
- **security-and-quality**: All security queries plus code quality checks

## Semgrep Rule Authoring Process

### Rule Development Lifecycle
1. Identify a vulnerability pattern from a recent security incident or code review
2. Write the pattern using Semgrep syntax with `pattern`, `pattern-either`, `pattern-not`
3. Test the rule against known vulnerable and safe code samples
4. Add metadata: CWE ID, OWASP category, severity, remediation guidance
5. Deploy via `.semgrep/` directory or Semgrep App registry
6. Monitor false positive rate and refine patterns

### Pattern Operators Reference
| Operator | Purpose |
|----------|---------|
| `pattern` | Match a single code pattern |
| `pattern-either` | Match any of multiple patterns (OR) |
| `pattern-not` | Exclude specific patterns from matches |
| `pattern-inside` | Match only within a containing pattern |
| `pattern-not-inside` | Exclude matches within a containing pattern |
| `metavariable-regex` | Constrain metavariable values with regex |
| `metavariable-comparison` | Compare metavariable values numerically |

## SARIF Processing Pipeline

### SARIF Structure
```json
{
  "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/main/sarif-2.1/schema/sarif-schema-2.1.0.json",
  "version": "2.1.0",
  "runs": [
    {
      "tool": {
        "driver": {
          "name": "Semgrep",
          "rules": []
        }
      },
      "results": [
        {
          "ruleId": "hardcoded-database-url",
          "level": "error",
          "message": { "text": "..." },
          "locations": [
            {
              "physicalLocation": {
                "artifactLocation": { "uri": "src/config.py" },
                "region": { "startLine": 42 }
              }
            }
          ]
        }
      ]
    }
  ]
}
```

## Triage and Remediation Workflow

### Severity-Based SLA
| Severity | Triage SLA | Remediation SLA | Escalation |
|----------|-----------|-----------------|------------|
| Critical | 1 business day | 3 business days | Security Lead + VP Eng |
| High | 3 business days | 10 business days | Security Lead |
| Medium | 5 business days | 30 business days | Team Lead |
| Low | 10 business days | 90 business days | Backlog |

### Finding States
1. **Open**: New finding not yet reviewed
2. **Confirmed**: Finding validated as true positive
3. **False Positive**: Finding dismissed with justification
4. **Fixed**: Remediation committed and verified by rescan
5. **Won't Fix**: Accepted risk with documented justification and risk owner

---

## Working Template

## GitHub Actions: Combined CodeQL + Semgrep Workflow

```yaml
# .github/workflows/sast-pipeline.yml
name: "SAST Security Pipeline"

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 3 * * 1'

concurrency:
  group: sast-${{ github.ref }}
  cancel-in-progress: true

jobs:
  # ─────────────── CodeQL Analysis ───────────────
  codeql:
    name: CodeQL (${{ matrix.language }})
    runs-on: ubuntu-latest
    permissions:
      actions: read
      contents: read
      security-events: write
    strategy:
      fail-fast: false
      matrix:
        language: ['javascript', 'python']
    steps:
      - uses: actions/checkout@v4

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: ${{ matrix.language }}
          queries: security-extended
          config-file: .github/codeql/codeql-config.yml

      - name: Autobuild
        uses: github/codeql-action/autobuild@v3

      - name: Perform Analysis
        uses: github/codeql-action/analyze@v3
        with:
          category: "/language:${{ matrix.language }}"

  # ─────────────── Semgrep Scan ───────────────
  semgrep:
    name: Semgrep Scan
    runs-on: ubuntu-latest
    permissions:
      security-events: write
      contents: read
    container:
      image: semgrep/semgrep:latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Semgrep
        run: |
          semgrep ci \
            --config auto \
            --config p/owasp-top-ten \
            --config p/cwe-top-25 \
            --config .semgrep/ \
            --sarif --output semgrep.sarif \
            --severity ERROR \
            --error
        env:
          SEMGREP_APP_TOKEN: ${{ secrets.SEMGREP_APP_TOKEN }}

      - name: Upload SARIF
        if: always()
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: semgrep.sarif
          category: semgrep

  # ─────────────── Quality Gate ───────────────
  security-gate:
    name: Security Quality Gate
    needs: [codeql, semgrep]
    runs-on: ubuntu-latest
    if: always()
    steps:
      - name: Check SAST Results
        run: |
          if [ "${{ needs.codeql.result }}" == "failure" ] || [ "${{ needs.semgrep.result }}" == "failure" ]; then
            echo "::error::SAST security gate failed. Review findings in the Security tab."
            exit 1
          fi
          echo "Security gate passed."
```

## CodeQL Custom Configuration

```yaml
# .github/codeql/codeql-config.yml
name: "Organization CodeQL Config"

queries:
  - uses: security-extended
  - uses: security-and-quality

paths-ignore:
  - '**/test/**'
  - '**/tests/**'
  - '**/spec/**'
  - '**/vendor/**'
  - '**/node_modules/**'
  - '**/__mocks__/**'
  - '**/*.test.js'
  - '**/*.test.ts'
  - '**/*.spec.py'
  - '**/migrations/**'

query-filters:
  - exclude:
      id: js/unused-local-variable
  - exclude:
      id: py/unused-import
```

## Semgrep Ignore File

```
# .semgrepignore
# Test files
*_test.go
*_test.py
*.test.js
*.test.ts
*.spec.js
*.spec.ts
test/
tests/
__tests__/
spec/

# Generated code
*_generated.go
*.pb.go
**/generated/**

# Vendored dependencies
vendor/
node_modules/
third_party/

# Build artifacts
dist/
build/
out/
```

## Branch Protection Configuration (Terraform)

```hcl
# branch-protection.tf
resource "github_branch_protection" "main" {
  repository_id = github_repository.app.node_id
  pattern       = "main"

  required_status_checks {
    strict   = true
    contexts = [
      "CodeQL (javascript)",
      "CodeQL (python)",
      "Semgrep Scan",
      "Security Quality Gate"
    ]
  }

  required_pull_request_reviews {
    required_approving_review_count = 1
    dismiss_stale_reviews           = true
  }

  enforce_admins = true

  allows_deletions    = false
  allows_force_pushes = false
}
```

## SARIF Report Aggregation Script

```bash
#!/bin/bash
# aggregate-sarif.sh - Merge multiple SARIF files for unified upload
set -euo pipefail

OUTPUT="merged-results.sarif"
SARIF_FILES=($(find . -name "*.sarif" -type f))

if [ ${#SARIF_FILES[@]} -eq 0 ]; then
  echo "No SARIF files found"
  exit 0
fi

# Use jq to merge SARIF runs
jq -s '{
  "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/main/sarif-2.1/schema/sarif-schema-2.1.0.json",
  "version": "2.1.0",
  "runs": [.[].runs[]]
}' "${SARIF_FILES[@]}" > "$OUTPUT"

echo "Merged ${#SARIF_FILES[@]} SARIF files into $OUTPUT"
TOTAL=$(jq '[.runs[].results | length] | add' "$OUTPUT")
echo "Total findings: $TOTAL"
```
