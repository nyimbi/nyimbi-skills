# Implementing Infrastructure As Code Security Scanning

## API Reference

## Checkov CLI

```bash
# Scan Terraform directory
checkov -d /path/to/tf --framework terraform --output json
# Scan specific file
checkov -f main.tf
# Scan CloudFormation
checkov -d . --framework cloudformation
# Scan Kubernetes manifests
checkov -d . --framework kubernetes
# Skip specific checks
checkov -d . --skip-check CKV_AWS_18,CKV_AWS_21
```

## tfsec CLI

```bash
# Scan directory
tfsec /path/to/tf --format json
# Exclude specific rules
tfsec . --exclude aws-s3-enable-bucket-logging
# Minimum severity
tfsec . --minimum-severity HIGH
```

## Common IaC Security Checks

| Check ID | Description | Severity |
|----------|-------------|----------|
| CKV_AWS_18 | S3 bucket logging | MEDIUM |
| CKV_AWS_19 | S3 bucket encryption | HIGH |
| CKV_AWS_23 | Security group open to 0.0.0.0/0 | HIGH |
| CKV_AWS_41 | RDS encryption | HIGH |
| CKV_AWS_145 | KMS key rotation | MEDIUM |
| CKV_K8S_1 | Pod privileged container | CRITICAL |

## GitHub Actions Integration

```yaml
- uses: bridgecrewio/checkov-action@master
  with:
    directory: .
    framework: terraform
    output_format: sarif
    soft_fail: false
```

### References

- Checkov: https://www.checkov.io/
- tfsec: https://aquasecurity.github.io/tfsec/
- KICS: https://kics.io/
- Bridgecrew: https://www.bridgecrew.io/

---

## Standards and Controls

## CIS Cloud Benchmarks

### CIS AWS Foundations Benchmark v3.0
- Maps directly to Checkov CKV_AWS_* checks
- Covers IAM, logging, monitoring, networking, and storage security
- Automated scanning validates 100+ benchmark controls

### CIS Azure Foundations Benchmark v2.1
- Maps to Checkov CKV_AZURE_* checks
- Covers identity, security center, storage, database, and network controls

### CIS GCP Foundations Benchmark v2.0
- Maps to Checkov CKV_GCP_* checks
- Covers IAM, logging, networking, VM, storage, and database controls

## NIST SP 800-53 Mapping

| NIST Control | IaC Check | Checkov ID |
|-------------|-----------|------------|
| AC-3 Access Enforcement | S3 bucket public access | CKV_AWS_18, CKV_AWS_20 |
| AU-2 Audit Events | CloudTrail enabled | CKV_AWS_35 |
| SC-8 Transmission Confidentiality | HTTPS/TLS enforcement | CKV_AWS_2 |
| SC-28 Protection at Rest | Encryption at rest | CKV_AWS_19, CKV_AWS_17 |
| SI-4 System Monitoring | CloudWatch/logging | CKV_AWS_24, CKV_AWS_66 |

## OWASP SAMM - Secure Architecture

### Security Architecture Level 2
- Validate infrastructure configurations against security standards before deployment
- Use automated tools to enforce architecture security requirements

### Security Architecture Level 3
- Custom policies encode organization-specific architecture requirements
- Continuous validation prevents configuration drift from approved patterns

## NIST SSDF (SP 800-218)

### PO.1: Define Security Requirements
- IaC security policies translate security requirements into enforceable checks
- Custom policies capture organization-specific requirements

### PW.5: Configure Software Securely
- PW.5.1: Configure software to have secure settings by default
- IaC scanning enforces secure defaults in infrastructure provisioning

---

## Workflows

## IaC Scanning Pipeline

```
Terraform/IaC Code Change
       │
       ▼
┌──────────────────┐
│ PR Created       │
└──────┬───────────┘
       │
       ├──────────────────────┐
       ▼                      ▼
┌──────────────┐    ┌──────────────┐
│ Checkov      │    │ tfsec        │
│ (2500+ rules)│    │ (Terraform)  │
└──────┬───────┘    └──────┬───────┘
       │                    │
       └──────────┬─────────┘
                  ▼
       ┌──────────────────┐
       │ SARIF Upload     │
       │ to GitHub        │
       └──────┬───────────┘
              │
              ▼
       ┌──────────────────┐
       │ Quality Gate     │
       │ (Block on HIGH+) │
       └──────┬───────────┘
              │
    ┌─────────┴──────────┐
    ▼                    ▼
 PASS                  FAIL
 terraform apply      Block merge
 permitted            + Fix required
```

## Checkov Command Reference

| Command | Purpose |
|---------|---------|
| `checkov -d ./terraform/` | Scan directory |
| `checkov -f main.tf` | Scan single file |
| `checkov -f tfplan.json --framework terraform_plan` | Scan Terraform plan |
| `checkov --list` | List all available checks |
| `checkov -d . --check CKV_AWS_18` | Run specific check |
| `checkov -d . --skip-check CKV_AWS_145` | Skip specific check |
| `checkov -d . --bc-api-key KEY` | Upload to Bridgecrew |
| `checkov -d . --create-baseline` | Create baseline file |
| `checkov -d . --baseline BASELINE` | Scan against baseline |
| `checkov -d . --external-checks-dir ./custom/` | Use custom checks |
| `checkov -d . --compact` | Compact output |
| `checkov -d . --output sarif` | SARIF format output |

## Common Misconfigurations by Cloud Provider

### AWS Top 10 IaC Misconfigurations
1. S3 bucket public access enabled (CKV_AWS_18, CKV_AWS_20)
2. Security group with open ingress 0.0.0.0/0 (CKV_AWS_23)
3. RDS instance not encrypted (CKV_AWS_16)
4. CloudTrail not enabled (CKV_AWS_35)
5. EBS volume not encrypted (CKV_AWS_3)
6. IAM policy with wildcard actions (CKV_AWS_1)
7. ALB not using HTTPS (CKV_AWS_2)
8. CloudWatch logs not encrypted (CKV_AWS_24)
9. IMDSv2 not required (CKV_AWS_79)
10. VPC flow logs not enabled (CKV_AWS_9)

### Kubernetes Top Misconfigurations
1. Container running as root (CKV_K8S_6)
2. Privileged container (CKV_K8S_16)
3. No resource limits (CKV_K8S_11, CKV_K8S_13)
4. No readiness/liveness probes (CKV_K8S_9)
5. hostNetwork enabled (CKV_K8S_19)

---

## Working Template

## Checkov Configuration File

```yaml
# .checkov.yaml
branch: main
compact: true
directory:
  - terraform/
  - cloudformation/
  - k8s/
framework:
  - terraform
  - cloudformation
  - kubernetes
output:
  - cli
  - sarif
skip-check:
  - CKV_AWS_145   # CMK encryption for S3 (SSE-S3 acceptable)
  - CKV2_AWS_6    # S3 request logging (CloudTrail covers this)
soft-fail: false
```

## GitHub Actions Pipeline

```yaml
# .github/workflows/iac-security.yml
name: IaC Security

on:
  pull_request:
    paths: ['terraform/**', 'k8s/**', 'cloudformation/**']

jobs:
  checkov:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: bridgecrewio/checkov-action@v12
        with:
          directory: terraform/
          framework: terraform
          output_format: cli,sarif
          output_file_path: console,checkov.sarif
          soft_fail: false
      - uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: checkov.sarif
```

## Secure Terraform Module Template

```hcl
# modules/secure-s3-bucket/main.tf
resource "aws_s3_bucket" "this" {
  bucket = var.bucket_name
  tags   = var.tags
}

resource "aws_s3_bucket_versioning" "this" {
  bucket = aws_s3_bucket.this.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "this" {
  bucket = aws_s3_bucket.this.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "aws:kms"
      kms_master_key_id = var.kms_key_id
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_public_access_block" "this" {
  bucket = aws_s3_bucket.this.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_logging" "this" {
  bucket        = aws_s3_bucket.this.id
  target_bucket = var.logging_bucket
  target_prefix = "s3-access-logs/${var.bucket_name}/"
}
```
