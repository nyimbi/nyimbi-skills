# Building Devsecops Pipeline With Gitlab Ci

## API Reference

## GitLab Security Templates
| Template | Stage |
|----------|-------|
| `Security/SAST.gitlab-ci.yml` | Static analysis |
| `Security/DAST.gitlab-ci.yml` | Dynamic testing |
| `Security/Dependency-Scanning.gitlab-ci.yml` | Dependency audit |
| `Security/Container-Scanning.gitlab-ci.yml` | Container scan |
| `Security/Secret-Detection.gitlab-ci.yml` | Secret detection |
| `Security/IaC-Scanning.gitlab-ci.yml` | IaC security |

## .gitlab-ci.yml Structure
```yaml
include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Secret-Detection.gitlab-ci.yml
stages:
  - build
  - test
  - security
  - deploy
variables:
  SECURE_LOG_LEVEL: info
```

## GitLab CI Lint API
```
POST /api/v4/projects/:id/ci/lint
PRIVATE-TOKEN: your-token
Body: {"content": "yaml-string"}
```

## Security Variables
| Variable | Description |
|----------|-------------|
| `SAST_DEFAULT_ANALYZERS` | Comma-separated analyzer list |
| `SAST_EXCLUDED_ANALYZERS` | Analyzers to skip |
| `CS_IMAGE` | Container image to scan |
| `DAST_WEBSITE` | Target URL for DAST |
| `SECRET_DETECTION_HISTORIC_SCAN` | Scan full history |

## Vulnerability Report API
```
GET /api/v4/projects/:id/vulnerability_findings
```

## Security Scanning Tools
| Tool | Type | Language |
|------|------|----------|
| Semgrep | SAST | Multi-language |
| Bandit | SAST | Python |
| Trivy | Container | Container images |
| Gitleaks | Secret | Git history |
| KICS | IaC | Terraform/CloudFormation |
| ZAP | DAST | Web applications |

---

## Standards and Controls

## OWASP DevSecOps Pipeline Maturity Model

| Level | SAST | DAST | SCA | Container | Secrets | License |
|-------|------|------|-----|-----------|---------|---------|
| Level 1 (Basic) | Manual runs | None | Manual dependency check | None | Pre-commit hooks | None |
| Level 2 (Integrated) | CI-triggered on MR | Scheduled scans | CI-triggered | Image scan on build | CI scan on commits | CI-triggered |
| Level 3 (Enforced) | Required for merge | Gate before deploy | Block on critical CVE | Block vulnerable images | Push protection | Policy enforcement |
| Level 4 (Optimized) | Custom rules, tuned FP | Authenticated full scan | Auto-remediation PRs | Signed images only | Auto-rotation | SBOM generation |

## NIST SP 800-218 (SSDF) Mapping

| SSDF Practice | GitLab Feature | Pipeline Stage |
|---------------|----------------|----------------|
| PO.1 Define security requirements | Security policies | Policy configuration |
| PW.1 Design software securely | Threat modeling integration | Pre-build |
| PW.4 Reuse well-secured software | Dependency scanning | Security stage |
| PW.5 Create source code securely | SAST, secret detection | Security stage |
| PW.7 Review and test code | MR security widget | Merge request |
| PW.8 Test executable code | DAST | Post-deploy staging |
| PW.9 Configure software securely | Container scanning | Security stage |
| RV.1 Identify vulnerabilities | Vulnerability report | Dashboard |
| RV.2 Assess and prioritize | Severity classification | Triage workflow |
| RV.3 Remediate vulnerabilities | Issue tracking integration | Sprint planning |

## CIS Software Supply Chain Security

- **SCS-1**: Secure source code management with protected branches and signed commits
- **SCS-2**: Secure build pipelines with pinned template versions and runner isolation
- **SCS-3**: Verified dependencies through dependency scanning and license compliance
- **SCS-4**: Secure artifacts with container scanning and signed images
- **SCS-5**: Deployment security with manual gates and environment approvals

## GitLab Scanner Coverage Matrix

| Vulnerability Type | Primary Scanner | Secondary Scanner |
|--------------------|-----------------|-------------------|
| SQL Injection | SAST (Semgrep) | DAST |
| XSS | SAST | DAST |
| SSRF | SAST | DAST |
| Command Injection | SAST | DAST |
| Insecure Deserialization | SAST | N/A |
| Known CVE in dependency | Dependency Scanning | Container Scanning |
| Hardcoded credentials | Secret Detection | SAST |
| License violation | License Scanning | N/A |
| OS-level CVE in image | Container Scanning | N/A |
| Authentication flaws | DAST | SAST |

---

## Workflows

## Workflow 1: Merge Request Security Review

```
Developer creates merge request
           |
   Pipeline triggers security scanners in parallel:
   [SAST] [Secret Detection] [Dependency Scanning] [License Scanning]
           |
   MR Security Widget displays results:
   - New vulnerabilities introduced
   - Existing vulnerabilities fixed
   - Comparison with target branch
           |
   [No Critical/High] --> Reviewers can approve and merge
   [Critical/High found] --> MR blocked by approval policy
           |
   Security team reviews findings
           |
   [Confirmed] --> Developer remediates and re-pushes
   [False Positive] --> Dismissed with documented reason
           |
   All findings resolved --> MR eligible for merge
```

## Workflow 2: Container Image Security Gate

```
Docker image built in CI
           |
   Container scanning (Trivy) analyzes image layers
           |
   Findings categorized by severity
           |
   [Below threshold] --> Image pushed to registry with metadata
   [Above threshold] --> Pipeline fails, image not pushed
           |
   Registry stores scan results as artifact
           |
   Deployment pulls only scanned/approved images
```

## Workflow 3: DAST Against Staging Environment

```
Application deployed to staging
           |
   DAST browser scan initiated against staging URL
           |
   Authenticated scan crawls application pages
           |
   Active testing for XSS, SQLi, CSRF, etc.
           |
   Results added to vulnerability report
           |
   [Pass] --> Manual deploy-to-production gate enabled
   [Fail on critical] --> Staging deployment rolled back
           |
   Production deploy requires manual approval
```

## Workflow 4: Vulnerability Lifecycle Management

```
Scanner detects vulnerability
           |
   Status: "Detected" in vulnerability report
           |
   Security analyst triages finding
           |
   [Confirmed vulnerability]        [False positive]
           |                              |
   Status: "Confirmed"              Status: "Dismissed"
   Issue created automatically      Reason documented
           |
   Developer assigned fix
           |
   Fix merged, scanner re-runs
           |
   Vulnerability no longer detected
           |
   Status: "Resolved"
```

---

## Working Template

## Pipeline Security Scanner Checklist

| Scanner | Enabled | Template Included | Threshold Set | Blocking |
|---------|---------|-------------------|---------------|----------|
| SAST | [ ] | [ ] | Severity: _____ | [ ] |
| DAST | [ ] | [ ] | Severity: _____ | [ ] |
| Container Scanning | [ ] | [ ] | Severity: _____ | [ ] |
| Dependency Scanning | [ ] | [ ] | Severity: _____ | [ ] |
| Secret Detection | [ ] | [ ] | N/A | [ ] |
| License Scanning | [ ] | [ ] | Policy: _____ | [ ] |

## Security Policy Configuration

| Policy Type | Name | Scope | Enforcement |
|-------------|------|-------|-------------|
| Scan Execution | | [ ] All branches [ ] Default only | [ ] Required |
| MR Approval | | Severity trigger: _____ | Approvers: _____ |

## Environment-Specific DAST Targets

| Environment | URL | Auth Method | Scan Type | Schedule |
|-------------|-----|-------------|-----------|----------|
| Staging | | [ ] None [ ] Token [ ] Cookie | [ ] Passive [ ] Full | |
| Pre-production | | [ ] None [ ] Token [ ] Cookie | [ ] Passive [ ] Full | |

## Vulnerability SLA Targets

| Severity | Detection to Triage | Triage to Fix | Total SLA |
|----------|--------------------|--------------|-----------|
| Critical | 4 hours | 24 hours | 48 hours |
| High | 24 hours | 5 days | 7 days |
| Medium | 48 hours | 14 days | 30 days |
| Low | 1 week | 30 days | 90 days |
