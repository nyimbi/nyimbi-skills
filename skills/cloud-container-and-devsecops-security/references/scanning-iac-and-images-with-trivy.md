# Scanning IAC And Images With Trivy

## API Reference

## Scan Targets (subcommands)

| Command | Target | Example |
|---------|--------|---------|
| `trivy image` | Container image (registry/tar) | `trivy image alpine:3.19` |
| `trivy fs` | Local filesystem / project dir | `trivy fs ./` |
| `trivy repository` (`repo`) | Git repository (local or remote URL) | `trivy repo https://github.com/org/repo` |
| `trivy config` | IaC / config misconfiguration | `trivy config ./infra` |
| `trivy sbom` | Existing SBOM (CycloneDX/SPDX) | `trivy sbom sbom.cdx.json` |
| `trivy kubernetes` (`k8s`) | Live Kubernetes cluster | `trivy k8s --report summary cluster` |
| `trivy vm` | VM image (AMI/EBS/VMDK) | `trivy vm ami:ami-0123` |
| `trivy rootfs` | Extracted root filesystem | `trivy rootfs /mnt/rootfs` |

## Key Flags

| Flag | Description |
|------|-------------|
| `--scanners vuln,misconfig,secret,license` | Select which scanners to run |
| `--severity LOW,MEDIUM,HIGH,CRITICAL` | Filter results by severity |
| `--exit-code <n>` | Exit code when matching results are found (gating) |
| `--ignore-unfixed` | Suppress vulnerabilities with no fixed version |
| `--format table\|json\|sarif\|cyclonedx\|spdx-json` | Output format |
| `--output <file>` | Write report to file |
| `--input <file>` | Scan an image tar instead of a registry ref |
| `--vuln-type os,library` | Limit vulnerability detection scope |
| `--image-config-scanners misconfig,secret` | Scan image build config/history |
| `--config-policy <dir>` | Custom Rego misconfig policy directory |
| `--policy-namespaces <ns>` | Rego policy namespaces to evaluate |
| `--download-db-only` | Pre-download vulnerability DB (caching/air-gap) |
| `--download-java-db-only` | Pre-download Java index DB |
| `--skip-dirs` / `--skip-files` | Exclude paths from scan |
| `--ignorefile <path>` | Path to `.trivyignore` (default `.trivyignore`) |

## Output Formats

| Format | Use |
|--------|-----|
| `table` | Human-readable console (default) |
| `json` | Programmatic gating / parsing |
| `sarif` | GitHub code scanning / IDE ingestion |
| `cyclonedx` | CycloneDX SBOM |
| `spdx-json` | SPDX SBOM (JSON) |
| `github` | GitHub dependency snapshot |

## `.trivyignore` Format

```
# One ID per line; supports CVE, AVD (misconfig), and secret rule IDs
CVE-2023-12345
AVD-AWS-0089
generic-api-key
```

## GitHub Actions (trivy-action)

```yaml
- uses: aquasecurity/trivy-action@master
  with:
    scan-type: 'image'      # image | fs | config | repo | sbom
    image-ref: 'myorg/app:1.4.0'
    format: 'sarif'
    output: 'trivy-results.sarif'
    severity: 'HIGH,CRITICAL'
    ignore-unfixed: true
    exit-code: '1'
```

## External References

- Trivy Docs: https://trivy.dev/latest/docs/
- Configuration reference: https://trivy.dev/latest/docs/configuration/
- Misconfiguration scanning: https://trivy.dev/latest/docs/scanner/misconfiguration/
- SBOM: https://trivy.dev/latest/docs/supply-chain/sbom/

---

## Standards and Controls

## NIST CSF 2.0

| ID | Name | Rationale |
|----|------|-----------|
| ID.RA-01 | Asset vulnerabilities are identified and recorded | Trivy enumerates CVEs, misconfigurations, and embedded secrets across images, IaC, and SBOMs, recording them for risk assessment and remediation tracking. |

## MITRE ATT&CK

| Technique ID | Name | Tactic | Rationale |
|--------------|------|--------|-----------|
| T1525 | Implant Internal Image | Persistence | Scanning images and SBOMs before they reach a registry detects vulnerable, secret-laden, or malicious layers an adversary could implant to persist across deployments. |

## Supporting Frameworks and Standards

- **CIS Benchmarks** — Trivy `misconfig` checks align with CIS Docker/Kubernetes hardening guidance.
- **CycloneDX / SPDX** — SBOM output formats supported for supply-chain transparency.
- **SARIF** — Static Analysis Results Interchange Format for code-scanning dashboards.
- **OWASP Top 10 (A06: Vulnerable and Outdated Components)** — Trivy directly addresses outdated/vulnerable dependency detection.

## Official Resources

- Trivy: https://github.com/aquasecurity/trivy
- Trivy Docs: https://trivy.dev/latest/docs/
- Trivy DB: https://github.com/aquasecurity/trivy-db
- trivy-action: https://github.com/aquasecurity/trivy-action
- Aqua Security: https://www.aquasec.com/products/trivy/
