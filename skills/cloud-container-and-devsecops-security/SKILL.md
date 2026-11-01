---
name: cloud-container-and-devsecops-security
description: >-
  Secure the path from commit to running workload: secrets and SAST/SCA in CI,
  infrastructure-as-code scanning, container image hardening and vulnerability
  scanning, SBOM and signing, Kubernetes admission control and network policy,
  cloud posture management, and runtime workload protection. Use when the user
  asks to "scan my Docker image", "add Trivy to the pipeline", "why is this S3
  bucket public", "block privileged pods", "sign images with Cosign", "set up a
  default-deny NetworkPolicy", "CSPM vs CWP", or "harden our GitHub Actions" —
  or to write a Checkov rule for Terraform and stop secrets reaching git. This skill
  owns pipeline gate design and cloud/container control implementation. Do not
  use for prioritizing, SLA-tracking, or mapping vulnerabilities to frameworks
  (see vulnerability-management-and-compliance), for human IAM, conditional
  access, PAM, or endpoint agents (see
  identity-zero-trust-and-endpoint-security), for authorized attack execution
  (see offensive-security-and-red-teaming), or for web/API/mobile test
  methodology (see application-api-mobile-and-ai-security).
license: Apache-2.0
---

# Cloud, Container, and DevSecOps Security

Most cloud breaches in this domain are not novel attacks: they are a public
bucket, a privileged pod, a secret in git history, an image pulled by mutable
tag, or a cluster RBAC grant nobody reviewed. The value of this skill is closing
each of those with a gate that actually blocks, at the earliest stage where the
fact is visible, and knowing which stage that is.

A control you cannot verify by injecting a bad artifact and watching it fail is
not implemented. Treat every "configured" claim in this skill as unproven until
a deliberately malicious input has been rejected by it.

## When to use

- Adding or tuning security stages in a CI/CD pipeline (SAST, SCA, secrets, DAST, container scan)
- Scanning container images, Dockerfiles, Kubernetes manifests, or Helm charts
- Scanning Terraform, CloudFormation, or Pulumi before provisioning
- Signing images, generating SBOMs, or enforcing provenance at deploy time
- Writing admission policy (OPA Gatekeeper, Kyverno, Pod Security Admission, Binary Authorization)
- Segmenting pod traffic with network policies, or hardening cluster RBAC
- Standing up CSPM/CIS compliance monitoring, or runtime workload protection
- Investigating why a cloud or container control is not holding

**Do not use for** — `vulnerability-management-and-compliance` when the question
is how severe a CVE is, when it must be fixed by, or how a finding maps to PCI
or NIST (this skill detects and gates; that skill prioritizes and tracks);
`identity-zero-trust-and-endpoint-security` when the subject is human identity —
conditional access, MFA rollout, PAM/JIT, directory tiering, EDR, disk
encryption (workload identity, cloud IAM policies, and Kubernetes RBAC stay
here); `application-api-mobile-and-ai-security` when the ask is how to test an
application for XSS, BOLA, or prompt injection rather than whether the pipeline
blocks a bad build; `offensive-security-and-red-teaming` when the goal is to
gain access in an authorized engagement rather than to build the control that
prevents it.

## Workflow

1. **Inventory before you gate.** Enumerate cloud accounts/projects/subscriptions,
   repositories, registries, and clusters with an asset-and-relationship inventory
   (Cartography, CloudFox, or provider native inventory), then tag each with an
   owner. Output: a list where every repo, cluster, and bucket has a nameable
   owner — gates without an owner cannot be enforced.

2. **Harden the source and the runner.** Pin third-party actions to full SHA
   digests, set workflow `permissions: read-all` by default, move user-controlled
   input out of `${{ }}` expressions into environment variables, and protect
   `.github/workflows`/`.gitlab-ci.yml` with CODEOWNERS review. Run gitleaks
   (`protect --staged` locally, full history in CI) plus trufflehog with live
   verification; a verified secret fails the build *and* triggers rotation —
   blocking without rotating leaves the credential in git history.

3. **Gate IaC before provision.** Run Checkov plus one Terraform-native scanner
   (tfsec) on source, and again on `terraform plan -out` → `terraform show -json`
   so resolved module values are evaluated; add KICS for cross-framework coverage.
   Encode the organization's non-negotiables as custom Checkov checks or Rego.
   Output: a PR check that blocks on Critical/High outside a committed baseline,
   every baseline entry carrying owner, reason, and expiry.

4. **Build minimal, then scan the image.** Multi-stage build onto a distroless or
   slim base pinned by digest, non-root user, no package manager in the final
   stage. Scan once with Trivy — it covers OS and language CVEs, Dockerfile and
   manifest misconfiguration, secrets, licenses, and SBOM generation in one run
   (`trivy image --format sarif --exit-code 1 --severity HIGH,CRITICAL
   --ignore-unfixed`). Add Grype only as a second matcher or to re-scan an
   SBOM you already hold. Output: an image that cannot be pushed with a fixable
   High/Critical.

5. **SBOM, sign, attest.** Generate an SBOM (Syft SPDX or CycloneDX) and attach it
   as an OCI artifact; sign the digest with Cosign — keyless OIDC in CI where the
   platform supports it (no key material in the pipeline), KMS/HSM-backed key
   where offline trust is required — and record in-toto/SLSA provenance links for
   clone → build → scan. Signing without a verification step somewhere is
   decoration; verification lands in step 6.

6. **Enforce at admission.** Label namespaces for Pod Security Admission and
   migrate `audit` → `warn` → `enforce`; stand up Gatekeeper or Kyverno
   constraints for registry allowlists, digest-pinned images, no
   privileged/hostPath/hostNetwork, required resources and labels; use GCP
   Binary Authorization where the platform offers it. Apply default-deny ingress
   *and* egress per namespace, explicitly allow DNS, then add per-workload allows
   (Calico NetworkPolicy for namespace scope, GlobalNetworkPolicy for
   cluster-wide). Replace static cloud keys with workload identity (IRSA, GKE
   Workload Identity, Azure Workload Identity) and scope RBAC to verbs actually
   used.

7. **Split posture from runtime.** CSPM answers "is the configuration wrong" —
   Prowler/ScoutSuite on a schedule plus Security Hub, Defender for Cloud, or SCC,
   against a pinned CIS benchmark version, with de-duplication on
   (resource, control) and auto-remediation only for the safe subset. CWP answers
   "is the behavior wrong" — Falco or Tetragon rules for escape, privileged mount,
   secret read, and reverse shell, plus drift of running containers from their
   image baseline. Output: two queues with two response playbooks, not one.

8. **Prove every gate, then document exceptions.** Inject one known-bad artifact
   per stage — a hardcoded AWS key, a public-bucket Terraform file, a privileged
   pod, an unsigned image — and confirm each stage blocks it. Record every
   suppression that survives with an approver and an expiry date.

## Quality bar

- [ ] Every gate has been proven to fail a known-bad artifact; "the config looks right" is not evidence
- [ ] Secrets are caught pre-commit and in history, and a verified leak triggers credential rotation, not just a red build
- [ ] IaC is scanned against plan output as well as source, with custom house rules for the org's non-negotiables
- [ ] No image reaches a registry unscanned, and no image reaches admission unsigned and unverified
- [ ] Ignore/baseline entries (`.trivyignore`, Checkov baseline, Gatekeeper exemptions) each carry owner, reason, and expiry
- [ ] Every namespace has default-deny ingress and egress with DNS explicitly allowed, and workload traffic flows only through documented allows
- [ ] Production namespaces run PSA/Gatekeeper in `enforce`; `warn`/`audit` appear only in named migration namespaces
- [ ] Workloads authenticate with workload identity, never long-lived static cloud keys; CI secrets come from the platform secret store, never the repository
- [ ] Runtime rules have been triggered in a test pod and observed firing, not merely validated as syntactically correct YAML
- [ ] CSPM findings are de-duplicated to one owner per (resource, control), tracked against a pinned benchmark version
- [ ] Every documented exception names an approver, a compensating control, and an expiry date

## Reference map

Every technique merged into this skill is catalogued in
[`references/technique-index.md`](references/technique-index.md). Open the index
when you need a technique that is not named below; open the specific file when it
is.

Two synthesized topic files cut across the pipeline:

| Situation | Open |
|---|---|
| Which stage owns which gate, tool, and fail condition; shift-left vs runtime boundary | [pipeline-gates.md](references/pipeline-gates.md) |
| Telling CSPM, CIEM, and CWP apart; CIS benchmark assessment pattern | [posture-management-cspm-vs-cwp.md](references/posture-management-cspm-vs-cwp.md) |

Per-technique detail:

| Situation | Open |
|---|---|
| Image scanning — Trivy, one topic with several entry points (local, CI, IaC+image, K8s manifests) | [scanning-docker-images-with-trivy](references/scanning-docker-images-with-trivy.md) · [scanning-containers-with-trivy-in-cicd](references/scanning-containers-with-trivy-in-cicd.md) · [scanning-iac-and-images-with-trivy](references/scanning-iac-and-images-with-trivy.md) · [performing-container-security-scanning-with-trivy](references/performing-container-security-scanning-with-trivy.md) |
| Second-opinion scan or SBOM-based matching | [scanning-container-images-with-grype](references/scanning-container-images-with-grype.md) |
| IaC scanning: Checkov, tfsec, Terrascan, custom policies, baselines | [auditing-terraform-infrastructure-for-security](references/auditing-terraform-infrastructure-for-security.md) · [implementing-infrastructure-as-code-security-scanning](references/implementing-infrastructure-as-code-security-scanning.md) |
| Pre-deploy review of Kubernetes manifests and Helm charts | [scanning-kubernetes-manifests-with-kubesec](references/scanning-kubernetes-manifests-with-kubesec.md) · [securing-helm-chart-deployments](references/securing-helm-chart-deployments.md) |
| Hardening the image and Dockerfile (multi-stage, distroless, non-root) | [performing-container-image-hardening](references/performing-container-image-hardening.md) · [implementing-container-image-minimal-base-with-distroless](references/implementing-container-image-minimal-base-with-distroless.md) · [hardening-docker-containers-for-production](references/hardening-docker-containers-for-production.md) |
| Docker daemon configuration and host benchmark | [hardening-docker-daemon-configuration](references/hardening-docker-daemon-configuration.md) · [performing-docker-bench-security-assessment](references/performing-docker-bench-security-assessment.md) |
| Signing images, SBOMs, and verifying at the registry | [implementing-image-provenance-verification-with-cosign](references/implementing-image-provenance-verification-with-cosign.md) · [securing-container-registry-images](references/securing-container-registry-images.md) · [implementing-code-signing-for-artifacts](references/implementing-code-signing-for-artifacts.md) |
| Pipeline step attestation, SLSA, in-toto layouts | [implementing-supply-chain-security-with-in-toto](references/implementing-supply-chain-security-with-in-toto.md) |
| Self-hosted registry with scanning, signing, and RBAC | [securing-container-registry-with-harbor](references/securing-container-registry-with-harbor.md) |
| Secrets scanning in CI and pre-commit; rotating what leaked | [implementing-secrets-scanning-in-ci-cd](references/implementing-secrets-scanning-in-ci-cd.md) · [implementing-secret-scanning-with-gitleaks](references/implementing-secret-scanning-with-gitleaks.md) · [detecting-aws-credential-exposure-with-trufflehog](references/detecting-aws-credential-exposure-with-trufflehog.md) |
| Central secrets store replacing hardcoded credentials | [implementing-secrets-management-with-vault](references/implementing-secrets-management-with-vault.md) |
| Hardening the CI runner and workflow definitions | [securing-github-actions-workflows](references/securing-github-actions-workflows.md) · [building-devsecops-pipeline-with-gitlab-ci](references/building-devsecops-pipeline-with-gitlab-ci.md) |
| SAST / SCA / DAST gates in the pipeline | [integrating-sast-into-github-actions-pipeline](references/integrating-sast-into-github-actions-pipeline.md) · [implementing-semgrep-for-custom-sast-rules](references/implementing-semgrep-for-custom-sast-rules.md) · [implementing-github-advanced-security-for-code-scanning](references/implementing-github-advanced-security-for-code-scanning.md) · [performing-sca-dependency-scanning-with-snyk](references/performing-sca-dependency-scanning-with-snyk.md) · [integrating-dast-with-owasp-zap-in-pipeline](references/integrating-dast-with-owasp-zap-in-pipeline.md) |
| Coverage-guided fuzzing wired into CI | [implementing-fuzz-testing-in-cicd-with-aflplusplus](references/implementing-fuzz-testing-in-cicd-with-aflplusplus.md) |
| Admission control: Gatekeeper/OPA constraints, PSA, Binary Authorization | [implementing-opa-gatekeeper-for-policy-enforcement](references/implementing-opa-gatekeeper-for-policy-enforcement.md) · [implementing-policy-as-code-with-open-policy-agent](references/implementing-policy-as-code-with-open-policy-agent.md) · [implementing-pod-security-admission-controller](references/implementing-pod-security-admission-controller.md) · [implementing-kubernetes-pod-security-standards](references/implementing-kubernetes-pod-security-standards.md) · [implementing-gcp-binary-authorization](references/implementing-gcp-binary-authorization.md) |
| Network policy — one topic across three merged techniques | [implementing-container-network-policies-with-calico](references/implementing-container-network-policies-with-calico.md) · [implementing-kubernetes-network-policy-with-calico](references/implementing-kubernetes-network-policy-with-calico.md) · [implementing-network-policies-for-kubernetes](references/implementing-network-policies-for-kubernetes.md) |
| Cluster hardening, workload identity, managed-Kubernetes specifics | [securing-kubernetes-on-cloud](references/securing-kubernetes-on-cloud.md) |
| Cluster CIS benchmark and etcd/API-server assessment | [benchmarking-kubernetes-with-kube-bench](references/benchmarking-kubernetes-with-kube-bench.md) · [performing-kubernetes-cis-benchmark-with-kube-bench](references/performing-kubernetes-cis-benchmark-with-kube-bench.md) · [performing-kubernetes-etcd-security-assessment](references/performing-kubernetes-etcd-security-assessment.md) |
| Kubernetes RBAC: wildcard grants, cluster-admin sprawl, escalation paths | [auditing-kubernetes-cluster-rbac](references/auditing-kubernetes-cluster-rbac.md) · [auditing-kubernetes-rbac-privilege-escalation](references/auditing-kubernetes-rbac-privilege-escalation.md) · [implementing-rbac-hardening-for-kubernetes](references/implementing-rbac-hardening-for-kubernetes.md) |
| Cloud posture: Prowler/ScoutSuite, Security Hub, Defender, CIS benchmarks | [implementing-cloud-security-posture-management](references/implementing-cloud-security-posture-management.md) · [auditing-cloud-with-cis-benchmarks](references/auditing-cloud-with-cis-benchmarks.md) · [implementing-aws-security-hub](references/implementing-aws-security-hub.md) · [implementing-azure-defender-for-cloud](references/implementing-azure-defender-for-cloud.md) |
| Runtime workload protection: Falco, Tetragon, drift detection | [detecting-container-runtime-threats-with-falco](references/detecting-container-runtime-threats-with-falco.md) · [implementing-runtime-security-with-tetragon](references/implementing-runtime-security-with-tetragon.md) · [implementing-cloud-workload-protection](references/implementing-cloud-workload-protection.md) · [detecting-container-drift-at-runtime](references/detecting-container-drift-at-runtime.md) |
| Container escape posture and detection | [performing-container-escape-detection](references/performing-container-escape-detection.md) · [detecting-container-escape-with-falco-rules](references/detecting-container-escape-with-falco-rules.md) |
| Cloud IAM: least privilege, permission boundaries, privilege-escalation paths | [securing-aws-iam-permissions](references/securing-aws-iam-permissions.md) · [auditing-gcp-iam-permissions](references/auditing-gcp-iam-permissions.md) · [detecting-aws-iam-privilege-escalation](references/detecting-aws-iam-privilege-escalation.md) |
| Serverless hardening: Lambda/Functions roles, injection surface | [securing-serverless-functions](references/securing-serverless-functions.md) · [securing-aws-lambda-execution-roles](references/securing-aws-lambda-execution-roles.md) · [performing-serverless-function-security-review](references/performing-serverless-function-security-review.md) |
| Public storage: bucket permissions and remediation | [auditing-aws-s3-bucket-permissions](references/auditing-aws-s3-bucket-permissions.md) · [remediating-s3-bucket-misconfiguration](references/remediating-s3-bucket-misconfiguration.md) · [detecting-azure-storage-account-misconfigurations](references/detecting-azure-storage-account-misconfigurations.md) |
| Cloud threat detection feeding the response pipeline | [detecting-cloud-threats-with-guardduty](references/detecting-cloud-threats-with-guardduty.md) · [analyzing-kubernetes-audit-logs](references/analyzing-kubernetes-audit-logs.md) · [detecting-aws-cloudtrail-anomalies](references/detecting-aws-cloudtrail-anomalies.md) |
| Cloud WAF and API gateway edge controls | [implementing-cloud-waf-rules](references/implementing-cloud-waf-rules.md) · [securing-api-gateway-with-aws-waf](references/securing-api-gateway-with-aws-waf.md) |
| Threat modeling before the pipeline exists | [performing-threat-modeling-with-owasp-threat-dragon](references/performing-threat-modeling-with-owasp-threat-dragon.md) |

Executable helpers for each technique live in `scripts/<technique-name>/` — read
the reference file first to learn what the script expects, then run it.

## Output format

For a pipeline design or audit, deliver:

```markdown
# <System> — Cloud/Container Security Pipeline

## Scope
Accounts, projects, clusters, registries, repositories in scope, each with an owner.

## Pipeline gates
Stage | Gate | Tool | Fail condition | Blocks (commit / PR / build / registry / admission / runtime)
Proven-by line: the bad artifact injected at each stage and the observed block.

## Control state
Control | Status (implemented / partial / absent) | Evidence | Reference file

## Findings
Severity | Finding | Exact location (file, policy, namespace, bucket) | Concrete fix

## Posture vs runtime
CSPM queue (configuration, owner, remediation path) · Runtime queue (behavior,
detection rule, response playbook)

## Exceptions
Finding | Owner | Compensating control | Approver | Expiry
```

Findings must cite the exact file path, policy name, or `kubectl` object that is
wrong, plus the command that reproduces the failure. "Consider hardening IAM" is
not a finding.
