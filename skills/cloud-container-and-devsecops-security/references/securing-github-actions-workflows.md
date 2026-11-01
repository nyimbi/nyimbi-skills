# Securing Github Actions Workflows

## API Reference

## Security Checks

| Check | Risk | Severity |
|-------|------|----------|
| Unpinned actions (mutable tags) | Supply chain attack via tag overwrite | Medium |
| Missing permissions block | Inherits overly broad defaults | Medium |
| write-all permissions | Excessive token scope | High |
| Script injection in run steps | Code execution via PR title/body | High |
| pull_request_target trigger | Fork code runs with base permissions | High |
| Secrets in workflow logs | Credential exposure | Critical |

## Dangerous Expression Contexts

| Context | Risk |
|---------|------|
| `github.event.pull_request.title` | Attacker-controlled PR title |
| `github.event.pull_request.body` | Attacker-controlled PR body |
| `github.event.issue.title` | Attacker-controlled issue title |
| `github.event.comment.body` | Attacker-controlled comment |
| `github.head_ref` | Attacker-controlled branch name |

## SHA Pinning Format

| Format | Security |
|--------|----------|
| `actions/checkout@v4` | Insecure - mutable tag |
| `actions/checkout@b4ffde65f...` | Secure - immutable SHA |

## Permission Scopes

| Scope | Values |
|-------|--------|
| contents | read, write |
| actions | read, write |
| deployments | read, write |
| id-token | write (for OIDC) |
| security-events | write |
| pull-requests | read, write |

## Python Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| `yaml` | PyYAML >=6.0 | Parse workflow YAML |
| `re` | stdlib | Pattern matching |
| `json` | stdlib | Report output |
| `pathlib` | stdlib | File discovery |

## References

- GitHub Actions Security Hardening: https://docs.github.com/en/actions/security-guides
- StepSecurity Harden Runner: https://github.com/step-security/harden-runner
- actionlint: https://github.com/rhysd/actionlint

---

## Standards and Controls

## NIST SSDF (SP 800-218)

### PS.1: Protect All Forms of Code
- Workflows are code and must be reviewed and protected
- Pin action dependencies to SHA digests
- Minimize GITHUB_TOKEN permissions

## CIS Software Supply Chain Security

- BD-1: Define security requirements for build processes
- BD-2: Automate security validation of build configurations
- BD-3: Pin all external dependencies to immutable references

## OWASP CI/CD Top 10 Risks

| Risk | GitHub Actions Mitigation |
|------|--------------------------|
| CICD-SEC-1: Insufficient Flow Control | Environment protection rules, CODEOWNERS |
| CICD-SEC-3: Dependency Chain Abuse | SHA pinning of actions |
| CICD-SEC-4: Poisoned Pipeline Execution | Restrict pull_request_target, input sanitization |
| CICD-SEC-6: Credential Hygiene | OIDC federation, minimal GITHUB_TOKEN scope |
| CICD-SEC-9: Artifact Integrity | Sign artifacts in workflows |

## SLSA Framework

- Level 2: Hosted build service (GitHub Actions qualifies)
- Level 3: Hardened build platform with isolation guarantees
- Workflow hardening prevents provenance falsification

---

## Workflows

## Hardening Checklist

1. Pin all actions to SHA digests
2. Set restrictive default permissions
3. Sanitize all user-controlled inputs
4. Never use pull_request_target with PR checkout
5. Enable environment protection for production
6. Configure CODEOWNERS for workflow files
7. Enable Dependabot for github-actions
8. Audit third-party actions quarterly
9. Use OIDC instead of long-lived cloud credentials
10. Add harden-runner for network monitoring

## Permission Scoping Reference

| Permission | Use Case |
|-----------|----------|
| contents: read | Checkout code |
| contents: write | Create releases, push tags |
| security-events: write | Upload SARIF results |
| packages: write | Push container images |
| deployments: write | Create deployment status |
| id-token: write | OIDC cloud authentication |
| pull-requests: write | Comment on PRs |

## Script Injection Prevention

```yaml
# DANGEROUS patterns to avoid:
run: echo "${{ github.event.issue.title }}"
run: echo "${{ github.event.comment.body }}"
run: echo "${{ github.head_ref }}"

# SAFE alternatives:
env:
  TITLE: ${{ github.event.issue.title }}
run: echo "${TITLE}"
```

---

## Working Template

## Hardened Workflow Template

```yaml
name: Secure CI Pipeline
permissions: {}

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11  # v4.1.1
      - uses: step-security/harden-runner@17d0e2bd7d51742c71671bd19fa12bdc9d40a3d6  # v2.8.1
        with:
          egress-policy: audit
      - name: Build
        run: make build
      - name: Test
        run: make test
```

## Dependabot for Actions

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    commit-message:
      prefix: "ci"
```

## CODEOWNERS for Workflow Protection

```
# .github/CODEOWNERS
.github/workflows/ @org/security-team @org/platform-team
.github/actions/ @org/security-team
.github/dependabot.yml @org/platform-team
```
