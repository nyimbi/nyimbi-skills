# Implementing Github Advanced Security For Code Scanning

## API Reference

## GitHub Code Scanning API

```bash
# List code scanning alerts
gh api /repos/OWNER/REPO/code-scanning/alerts?state=open

# Get specific alert
gh api /repos/OWNER/REPO/code-scanning/alerts/ALERT_NUMBER

# List analyses
gh api /repos/OWNER/REPO/code-scanning/analyses

# Upload SARIF
gh api /repos/OWNER/REPO/code-scanning/sarifs -X POST \
  -f commit_sha=SHA -f ref=refs/heads/main -f sarif=@results.sarif.gz
```

## Secret Scanning API

```bash
# List secret alerts
gh api /repos/OWNER/REPO/secret-scanning/alerts?state=open

# Update alert state
gh api /repos/OWNER/REPO/secret-scanning/alerts/ALERT_NUMBER -X PATCH \
  -f state=resolved -f resolution=revoked
```

## CodeQL Query Suites

| Suite | Description | False Positive Rate |
|-------|-------------|-------------------|
| `default` | High-confidence security | Low |
| `security-extended` | Broader security coverage | Medium |
| `security-and-quality` | Security + code quality | Higher |

## CodeQL Workflow (GitHub Actions)

```yaml
- uses: github/codeql-action/init@v3
  with:
    languages: ${{ matrix.language }}
    queries: +security-extended
- uses: github/codeql-action/autobuild@v3
- uses: github/codeql-action/analyze@v3
```

## Supported Languages

| Language | Build Required | Query Pack |
|----------|---------------|-----------|
| Python | No | codeql/python-queries |
| JavaScript/TypeScript | No | codeql/javascript-queries |
| Java/Kotlin | Yes | codeql/java-queries |
| C/C++ | Yes | codeql/cpp-queries |
| C# | Yes | codeql/csharp-queries |
| Go | Yes | codeql/go-queries |
| Ruby | No | codeql/ruby-queries |
| Swift | Yes | codeql/swift-queries |

### References

- GHAS Docs: https://docs.github.com/en/code-security/code-scanning
- CodeQL: https://codeql.github.com/docs/
- CodeQL Queries: https://github.com/github/codeql
- SARIF Spec: https://sarifweb.azurewebsites.net/

---

## Standards and Controls

## OWASP Top 10 (2021) Coverage by CodeQL

| OWASP Category | CodeQL CWE Coverage | Query Suite |
|----------------|---------------------|-------------|
| A01 Broken Access Control | CWE-22, CWE-284, CWE-639 | security-extended |
| A02 Cryptographic Failures | CWE-259, CWE-327, CWE-328 | security-extended |
| A03 Injection | CWE-77, CWE-78, CWE-79, CWE-89 | default |
| A04 Insecure Design | CWE-209, CWE-256, CWE-501 | security-and-quality |
| A05 Security Misconfiguration | CWE-16, CWE-611 | security-extended |
| A06 Vulnerable Components | Dependency Review / Dependabot | N/A (separate feature) |
| A07 Auth Failures | CWE-287, CWE-798 | default |
| A08 Data Integrity Failures | CWE-502, CWE-829 | security-extended |
| A09 Logging Failures | CWE-117, CWE-778 | security-and-quality |
| A10 SSRF | CWE-918 | default |

## NIST SP 800-218 (SSDF) Alignment

- **PO.3**: Define security requirements --- CodeQL enforces security policies through query suites
- **PW.4**: Reuse existing, well-secured software --- Dependabot ensures dependencies are patched
- **PW.7**: Review and test code for vulnerabilities --- Automated code scanning on every PR
- **PW.8**: Test executable code --- SARIF integration enables combining SAST with DAST results
- **RV.1**: Identify and confirm vulnerabilities --- Security overview tracks alerts across the organization

## CIS Software Supply Chain Security Guide

- **SCS-1**: Source code management security --- Branch protection rules, required reviewers
- **SCS-2**: Build pipelines --- CodeQL runs in GitHub Actions with pinned action versions
- **SCS-5**: Artifact management --- Dependency review prevents vulnerable packages from merging

## ISO 27001 Control Mapping

| ISO 27001 Control | GHAS Feature |
|--------------------|--------------|
| A.8.25 Secure development lifecycle | CodeQL in CI/CD pipeline |
| A.8.26 Application security requirements | Custom query packs for org standards |
| A.8.28 Secure coding | Real-time scanning on pull requests |
| A.8.29 Security testing in dev and acceptance | Required status checks with severity gates |
| A.8.31 Separation of environments | Branch protection and deployment rules |

---

## Workflows

## Workflow 1: Organization-Wide Enablement

```
1. Audit current repository inventory
   - List all repositories in the organization
   - Identify languages and build systems in use
   - Estimate active committer count for licensing
   |
2. Pilot phase (2-4 weeks)
   - Enable GHAS on 5-10 representative repositories
   - Use default setup for initial scanning
   - Collect baseline alert counts and false positive rates
   |
3. Triage pilot results
   - Review alerts by severity (Critical, High, Medium, Low)
   - Dismiss confirmed false positives with documented reasons
   - Create remediation issues for confirmed vulnerabilities
   |
4. Tune configuration
   - Adjust query suites based on false positive feedback
   - Write custom queries for organization-specific patterns
   - Configure alert dismissal policies
   |
5. Broad rollout
   - Enable default setup across remaining repositories
   - Configure organization-level security configurations
   - Set branch protection rules requiring code scanning checks
   |
6. Continuous monitoring
   - Review security overview dashboard weekly
   - Track MTTR for code scanning alerts
   - Report metrics to security leadership monthly
```

## Workflow 2: Pull Request Security Gate

```
Developer pushes code to feature branch
           |
   PR is created targeting main
           |
   CodeQL analysis triggers automatically
           |
   Dependency review checks for vulnerable dependencies
           |
   Secret scanning checks for hardcoded credentials
           |
   Results posted as PR check and inline annotations
           |
   [Pass] All checks pass --> PR is eligible for merge
   [Fail] Critical/High findings --> PR is blocked
           |
   Developer reviews findings and applies fixes
           |
   Re-push triggers re-analysis
           |
   Merge after all checks pass and reviewer approval
```

## Workflow 3: Custom CodeQL Query Development

```
1. Identify recurring vulnerability pattern not caught by default queries
   |
2. Set up CodeQL development environment
   - Install CodeQL CLI
   - Clone CodeQL standard library repository
   - Create workspace with target codebase database
   |
3. Author the query in QL language
   - Define source, sink, and taint-tracking configuration
   - Add metadata (@name, @description, @kind, @problem.severity, @security-severity, @precision, @id, @tags)
   |
4. Test the query
   - Create test cases with expected results
   - Run `codeql test run` against test database
   - Validate precision and recall
   |
5. Package the query
   - Create qlpack.yml with version and dependencies
   - Publish to GitHub Container Registry or internal package registry
   |
6. Deploy to scanning workflow
   - Reference the query pack in codeql-action/init step
   - Monitor results for the new query across repositories
```

## Workflow 4: SARIF Integration with External Tools

```
External SAST/DAST tool runs scan
           |
   Tool outputs results in SARIF 2.1.0 format
           |
   GitHub Actions uploads SARIF via codeql-action/upload-sarif
           |
   Results appear in Security tab alongside CodeQL findings
           |
   Unified triage workflow across all scanning tools
           |
   Alert deduplication based on location and rule ID
```

---

## Working Template

## Organization Security Configuration

| Setting | Value | Notes |
|---------|-------|-------|
| Organization | `_______________` | |
| GHAS License Seats | `_______________` | Active committers |
| Default Query Suite | [ ] default [ ] security-extended [ ] security-and-quality | |
| Branch Protection Enabled | [ ] Yes [ ] No | |
| Secret Scanning Enabled | [ ] Yes [ ] No | |
| Push Protection Enabled | [ ] Yes [ ] No | |
| Dependabot Enabled | [ ] Yes [ ] No | |

## Repository Enablement Tracker

| Repository | Languages | Setup Type | Scanning Active | Open Alerts | Date Enabled |
|------------|-----------|------------|-----------------|-------------|--------------|
| | | [ ] Default [ ] Advanced | [ ] Yes [ ] No | | |
| | | [ ] Default [ ] Advanced | [ ] Yes [ ] No | | |
| | | [ ] Default [ ] Advanced | [ ] Yes [ ] No | | |

## Custom Query Pack Registry

| Pack Name | Version | Description | Target Languages |
|-----------|---------|-------------|------------------|
| | | | |

## Alert Severity Gate Configuration

| Environment | Block on Critical | Block on High | Block on Medium | Block on Low |
|-------------|-------------------|---------------|-----------------|--------------|
| Production (main) | [x] Yes | [x] Yes | [ ] Yes | [ ] No |
| Staging (develop) | [x] Yes | [ ] Yes | [ ] No | [ ] No |
| Feature branches | [x] Yes | [ ] Yes | [ ] No | [ ] No |

## Secret Scanning Custom Patterns

| Pattern Name | Regex | Description | Alert Enabled | Push Protection |
|--------------|-------|-------------|---------------|-----------------|
| | | | [ ] Yes [ ] No | [ ] Yes [ ] No |

## Weekly Security Review Checklist

- [ ] Review new critical and high severity alerts
- [ ] Check alert dismissal reasons for quality
- [ ] Verify new repositories have scanning enabled
- [ ] Review Dependabot alerts and merge security updates
- [ ] Check secret scanning alerts for exposed credentials
- [ ] Update security overview dashboard metrics
- [ ] Review MTTR trends and identify bottlenecks

## Escalation Matrix

| Alert Severity | Response SLA | Escalation Contact | Action Required |
|----------------|-------------|--------------------|-----------------|
| Critical | 24 hours | Security Lead | Immediate remediation, potential incident |
| High | 72 hours | Team Lead | Prioritize in current sprint |
| Medium | 2 weeks | Developer | Schedule for next sprint |
| Low | 30 days | Developer | Add to backlog |
