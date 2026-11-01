# Pipeline gates — build → scan → sign → deploy → runtime

Every gate has one owner stage, one tool, one fail condition, and one place it
blocks. A gate that cannot block is a report, not a gate.

| Stage | Gate | Default tool | Fail condition | Blocks |
|---|---|---|---|---|
| Commit | Secret in staged files | gitleaks `protect --staged` | Any finding without an ignore entry | Local push |
| PR | Secret in history | gitleaks + trufflehog (verify mode) | High-confidence secret, verified live | Merge |
| PR | SAST | CodeQL + Semgrep | New High/Critical alert on changed lines | Merge |
| PR | Dependencies (SCA) | Snyk / Trivy fs | Fixable Critical/High with a patch available | Merge |
| PR | IaC | Checkov (source **and** `tfplan.json`) + tfsec/KICS | Critical/High outside baseline | Merge |
| PR | K8s manifest / Helm | Kubesec + Trivy config | Privileged, hostPath, no limits, `:latest` | Merge |
| Build | Dockerfile lint | hadolint + `trivy config` | Root user, `ADD` from URL, secrets in `ENV` | Image build |
| Build | Image vulnerability | Trivy image (then Grype for a second matcher) | Fixable High/Critical (`--ignore-unfixed`) | Push |
| Build | SBOM | Syft SPDX/CycloneDX | SBOM generation or upload fails | Push |
| Build | Signing | Cosign (keyless OIDC in CI, or KMS key) | Signature missing or unverifiable | Push |
| Registry | Registry policy | ECR scan-on-push + tag immutability; Harbor/Quay | Mutable tag, unscanned digest | Pull by tag |
| Deploy | Provenance / attestation | Cosign verify + in-toto/SLSA link check | No signature, wrong signer identity, missing build link | Admission |
| Deploy | Policy admission | OPA Gatekeeper / Kyverno / PSA / Binary Authorization | Constraint violated in `enforce` mode | Admission |
| Deploy | Network | Calico / CNI NetworkPolicy | Egress or ingress not covered by an allow rule | Traffic |
| Runtime | Drift from image baseline | Falco / Tetragon / CWP agent | Binary, file, or package change vs. image | Alert + isolate |
| Runtime | Escape / privilege | Falco rules | setns, cgroup release_agent, docker.sock, privileged mount | Alert + isolate |
| Runtime | Posture drift | Prowler + Security Hub / Defender / SCC | Control regressed vs. pinned CIS version | Ticket |

## Tool choice notes

- **One image scanner, chosen deliberately.** Trivy covers vulnerabilities,
  misconfiguration, secrets, licenses, and SBOM in a single invocation; use it as
  the gating scanner. Add Grype only when you want a second vulnerability matcher
  or when you must scan a pre-generated SBOM rather than the image.
- **Scan the plan, not just the source.** `checkov -f tfplan.json --framework
  terraform_plan` sees values resolved at apply time; source-only scans miss
  module variables and dynamic values.
- **Severity threshold + `--ignore-unfixed`** is the workable default. Failing
  builds on vulnerabilities no vendor has patched trains people to bypass the
  gate.
- **Ignore files are contracts.** `.trivyignore`, `.checkov`, and Gatekeeper
  exemptions need a comment with owner, reason, and an expiry date; an
  unexpiring ignore is a permanent hole.
- **Enforcement must migrate, not flip.** PSA and Gatekeeper go
  `audit` → `warn` → `enforce` per namespace; flipping straight to `enforce`
  in production blocks deploys, which ends with the controller disabled.

## Shift-left vs runtime boundary

Catch it at shift-left if the fact is visible before the workload runs: code
pattern, dependency CVE, IaC misconfiguration, missing label, bad image
reference, unsigned artifact. Catch it at runtime only if it exists solely once
running: a container escape, a reverse shell, a file mutated after start, a
cryptominer, an unexpected outbound connection. CSPM answers "is the
configuration wrong?"; CWP answers "is the behavior wrong?". Neither substitutes
for the other, and neither is an admission gate.
