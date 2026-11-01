# Performing AWS Account Enumeration With Scout Suite

## API Reference

## Libraries Used

| Library | Purpose |
|---------|---------|
| `subprocess` | Execute Scout Suite CLI scans |
| `json` | Parse Scout Suite JSON report output |
| `boto3` | AWS SDK for supplementary API calls |
| `os` | Read AWS credentials from environment |

## Installation

```bash
pip install scoutsuite boto3

# Or from source
git clone https://github.com/nccgroup/ScoutSuite
cd ScoutSuite
pip install -r requirements.txt
python scout.py --help
```

## Authentication

Scout Suite uses standard AWS credential chain:

```python
import os

# Option 1: Environment variables
os.environ["AWS_ACCESS_KEY_ID"] = "AKIA..."
os.environ["AWS_SECRET_ACCESS_KEY"] = "..."
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

# Option 2: AWS CLI profile
# scout aws --profile my-profile

# Option 3: IAM Role (EC2 instance profile / ECS task role)
# Automatically detected by boto3
```

## CLI Reference

### Full AWS Account Scan
```bash
scout aws --report-dir ./scout-report
```

### Scan Specific Services
```bash
scout aws --services iam s3 ec2 rds lambda --report-dir ./scout-report
```

### Scan Specific Regions
```bash
scout aws --regions us-east-1 us-west-2 eu-west-1 --report-dir ./scout-report
```

### Use Named Profile
```bash
scout aws --profile production-readonly --report-dir ./scout-report
```

### Key CLI Flags

| Flag | Description |
|------|-------------|
| `--provider` | Cloud provider: `aws`, `azure`, `gcp` |
| `--profile` | AWS CLI named profile |
| `--regions` | Specific AWS regions to scan |
| `--services` | Specific services to audit |
| `--report-dir` | Output directory for HTML report |
| `--no-browser` | Don't open report in browser |
| `--max-workers` | Number of parallel API threads |
| `--result-format` | Output format: `json`, `csv` |
| `--exceptions` | Path to exceptions file (known acceptable findings) |
| `--ruleset` | Custom ruleset file for scoring |

## Python Integration

### Run Scout Suite and Parse Results
```python
import subprocess
import json
from pathlib import Path

def run_scout(services=None, regions=None, profile=None, report_dir="/tmp/scout"):
    cmd = ["scout", "aws", "--report-dir", report_dir, "--no-browser"]
    if services:
        cmd.extend(["--services"] + services)
    if regions:
        cmd.extend(["--regions"] + regions)
    if profile:
        cmd.extend(["--profile", profile])

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
    if result.returncode != 0:
        raise RuntimeError(f"Scout Suite failed: {result.stderr}")

    # Parse the JSON results
    report_path = Path(report_dir) / "scoutsuite-results" / "scoutsuite_results.json"
    if report_path.exists():
        with open(report_path) as f:
            return json.load(f)
    return None
```

### Extract High-Risk Findings
```python
def extract_findings(report, min_severity="warning"):
    severity_order = {"danger": 3, "warning": 2, "info": 1}
    min_level = severity_order.get(min_severity, 1)
    findings = []

    for service_name, service_data in report.get("services", {}).items():
        for rule_name, rule_data in service_data.get("findings", {}).items():
            level = severity_order.get(rule_data.get("level", "info"), 0)
            if level >= min_level:
                findings.append({
                    "service": service_name,
                    "rule": rule_name,
                    "severity": rule_data.get("level"),
                    "description": rule_data.get("description"),
                    "flagged_items": rule_data.get("flagged_items", 0),
                    "checked_items": rule_data.get("checked_items", 0),
                })
    return sorted(findings, key=lambda x: severity_order.get(x["severity"], 0), reverse=True)
```

## Common Findings Categories

| Service | Common Findings |
|---------|----------------|
| IAM | Root account MFA, access key rotation, overly permissive policies |
| S3 | Public buckets, missing encryption, no versioning |
| EC2 | Security groups with 0.0.0.0/0, unencrypted EBS, public IPs |
| RDS | Public access, no encryption at rest, no multi-AZ |
| Lambda | Overly permissive roles, environment variable secrets |
| CloudTrail | Logging disabled, no log file validation |
| VPC | Default VPC in use, missing flow logs |

## Output Format

```json
{
  "provider_code": "aws",
  "account_id": "123456789012",
  "last_run": {
    "time": "2025-01-15T10:30:00Z",
    "ruleset_name": "default",
    "run_parameters": {"services": ["iam", "s3", "ec2"]}
  },
  "services": {
    "iam": {
      "findings": {
        "iam-root-account-no-mfa": {
          "level": "danger",
          "description": "Root account does not have MFA enabled",
          "flagged_items": 1,
          "checked_items": 1
        }
      }
    },
    "s3": {
      "findings": {
        "s3-bucket-no-default-encryption": {
          "level": "warning",
          "description": "S3 bucket does not have default encryption",
          "flagged_items": 3,
          "checked_items": 15
        }
      }
    }
  }
}
```

---

## Standards and Controls

## Industry Standards

### CIS AWS Foundations Benchmark v3.0
- Section 1: Identity and Access Management
- Section 2: Logging
- Section 3: Monitoring
- Section 4: Networking
- Section 5: Storage

### AWS Well-Architected Framework - Security Pillar
- SEC 1: Securely operate your workload
- SEC 2: Manage identities for people and machines
- SEC 3: Manage permissions for people and machines
- SEC 6: Protect compute resources
- SEC 8: Protect data at rest
- SEC 9: Protect data in transit

### NIST 800-53 Mapped Controls
- AC-2: Account Management
- AU-2: Audit Events
- AU-6: Audit Review, Analysis, and Reporting
- CM-6: Configuration Settings
- SC-7: Boundary Protection

## ScoutSuite Rule Mappings

### IAM Rules
| Rule ID | Description | CIS Benchmark |
|---------|-------------|---------------|
| iam-root-account-no-mfa | Root account MFA not enabled | 1.5 |
| iam-user-no-mfa | IAM user without MFA | 1.10 |
| iam-password-policy-no-uppercase | Weak password policy | 1.5 |
| iam-unused-access-key | Access key unused > 90 days | 1.12 |
| iam-inline-policy | Inline policies attached to users | 1.16 |

### S3 Rules
| Rule ID | Description | CIS Benchmark |
|---------|-------------|---------------|
| s3-bucket-public-access | Bucket allows public access | 2.1.5 |
| s3-bucket-no-logging | Server access logging disabled | 2.1.3 |
| s3-bucket-no-versioning | Versioning not enabled | N/A |
| s3-bucket-no-encryption | Default encryption not set | 2.1.1 |

### EC2 Rules
| Rule ID | Description | CIS Benchmark |
|---------|-------------|---------------|
| ec2-security-group-opens-all-ports | Security group allows all traffic | 5.2 |
| ec2-instance-with-public-ip | Instance has public IP | N/A |
| ec2-ebs-volume-not-encrypted | EBS volume unencrypted | 2.2.1 |

## Compliance Framework Coverage
- SOC 2 Type II
- PCI DSS v4.0
- HIPAA Security Rule
- ISO 27001:2022
- GDPR (data protection controls)

---

## Workflows

## Standard Security Assessment Workflow

```
1. Preparation Phase
   ├── Define scope (accounts, regions, services)
   ├── Create read-only IAM role with SecurityAudit policy
   ├── Install and configure ScoutSuite
   └── Verify credentials and connectivity

2. Enumeration Phase
   ├── Run ScoutSuite against target AWS account
   ├── Monitor scan progress and address API errors
   ├── Collect results from all specified regions
   └── Generate HTML report

3. Analysis Phase
   ├── Review dashboard for severity distribution
   ├── Prioritize danger-level findings
   ├── Map findings to CIS Benchmarks
   ├── Identify patterns across services
   └── Document false positives

4. Reporting Phase
   ├── Create executive summary of findings
   ├── Detail remediation steps per finding
   ├── Assign priority and ownership
   └── Establish remediation timeline

5. Remediation Phase
   ├── Implement fixes per priority order
   ├── Re-scan to validate remediation
   ├── Update documentation
   └── Schedule recurring assessments
```

## Multi-Account Assessment Workflow

```
1. Setup Organization Scanning
   ├── Create cross-account IAM roles in each target account
   ├── Configure trust relationships to auditor account
   └── Prepare account list and scanning schedule

2. Execute Scans
   ├── Iterate through accounts using assume-role
   ├── Run ScoutSuite per account
   ├── Aggregate results into central location
   └── Generate per-account and aggregate reports

3. Consolidate Findings
   ├── Merge findings across accounts
   ├── Identify organization-wide patterns
   ├── Compare accounts against baseline
   └── Produce organization security scorecard
```

## CI/CD Integration Workflow

```
1. Pipeline Trigger
   ├── Infrastructure change detected (Terraform/CloudFormation)
   └── Scheduled nightly scan

2. Automated Scan
   ├── Run ScoutSuite with targeted service scope
   ├── Parse JSON results programmatically
   └── Evaluate against security baseline

3. Gate Decision
   ├── Danger findings → Block deployment, alert security team
   ├── Warning findings → Proceed with notification
   └── No findings → Continue pipeline
```

---

## Working Template

## Assessment Information

| Field | Value |
|-------|-------|
| Assessment Date | YYYY-MM-DD |
| AWS Account ID | |
| Assessor | |
| ScoutSuite Version | |
| Scan Scope | Full / Targeted Services |
| Regions Scanned | |

## Findings Summary

| Severity | Count | Remediated |
|----------|-------|------------|
| Critical (Danger) | | |
| Warning | | |
| Passing | | |

## Service-Level Findings

### IAM
- [ ] Root account MFA enabled
- [ ] Password policy meets CIS requirements
- [ ] No unused IAM users (>90 days)
- [ ] No unused access keys (>90 days)
- [ ] No inline policies on users
- [ ] No wildcard (*) permissions in policies

### S3
- [ ] No publicly accessible buckets
- [ ] Default encryption enabled on all buckets
- [ ] Server access logging enabled
- [ ] Versioning enabled on critical buckets
- [ ] Block Public Access settings enabled

### EC2
- [ ] No security groups allowing 0.0.0.0/0 on SSH (22)
- [ ] No security groups allowing 0.0.0.0/0 on RDP (3389)
- [ ] EBS volumes encrypted
- [ ] No instances with public IPs in private subnets
- [ ] IMDSv2 required on all instances

### RDS
- [ ] No publicly accessible databases
- [ ] Encryption at rest enabled
- [ ] Automated backups configured
- [ ] Multi-AZ for production databases

### CloudTrail
- [ ] CloudTrail enabled in all regions
- [ ] Log file validation enabled
- [ ] CloudTrail logs encrypted with KMS
- [ ] CloudTrail integrated with CloudWatch

### Lambda
- [ ] No functions with public access
- [ ] No secrets in environment variables
- [ ] Functions deployed in VPC where appropriate
- [ ] Execution roles follow least privilege

## Remediation Plan

| Priority | Finding | Service | Remediation | Owner | Due Date | Status |
|----------|---------|---------|-------------|-------|----------|--------|
| P1 | | | | | | |
| P2 | | | | | | |
| P3 | | | | | | |

## Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Security Assessor | | | |
| Account Owner | | | |
| CISO | | | |
