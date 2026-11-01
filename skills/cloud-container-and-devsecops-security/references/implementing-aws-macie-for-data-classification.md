# Implementing AWS Macie For Data Classification

## API Reference

## Dependencies

| Library | Version | Purpose |
|---------|---------|---------|
| boto3 | >=1.28 | AWS SDK for Macie2 sensitive data discovery |

## CLI Usage

```bash
python scripts/agent.py \
  --profile security-audit \
  --region us-east-1 \
  --output-dir /reports/ \
  --output macie_report.json
```

## Functions

### `get_macie_client(profile, region)`
Creates boto3 Macie2 client with optional named profile.

### `enable_macie(client) -> dict`
Calls `client.get_macie_session()` to check status, then `client.enable_macie()` if needed.

### `list_s3_buckets_summary(client) -> list`
Calls `client.describe_buckets()` to get bucket inventory with encryption, public access, and classifiable object counts.

### `create_classification_job(client, bucket_names, job_name) -> dict`
Calls `client.create_classification_job(jobType="ONE_TIME", s3JobDefinition={...})` for targeted sensitive data discovery.

### `get_finding_statistics(client) -> dict`
Calls `client.get_finding_statistics(groupBy=...)` for severity and type breakdowns.

### `list_findings(client, severity, max_results) -> list`
Calls `client.list_findings()` with severity criterion, then `client.get_findings(findingIds=[...])` for details.

### `generate_report(client) -> dict`
Orchestrates all functions and compiles summary with public bucket identification.

## boto3 Macie2 Methods Used

| Method | Purpose |
|--------|---------|
| `enable_macie(status)` | Enable Macie service |
| `describe_buckets(criteria)` | S3 bucket inventory |
| `create_classification_job(...)` | Start discovery job |
| `get_finding_statistics(groupBy)` | Finding aggregations |
| `list_findings(findingCriteria)` | Filter findings |
| `get_findings(findingIds)` | Detailed finding data |

## Output Schema

```json
{
  "summary": {"total_buckets": 45, "public_buckets": 2, "high_findings": 12},
  "bucket_inventory": [{"name": "my-bucket", "public_access": "NOT_PUBLIC"}],
  "high_findings": [{"type": "SensitiveData:S3Object/Personal", "bucket": "data-lake"}]
}
```

---

## Standards and Controls

## Compliance Frameworks Supported
- GDPR Article 30: Records of processing activities
- CCPA: California Consumer Privacy Act data discovery
- HIPAA: Protected health information identification
- PCI DSS 4.0: Cardholder data discovery (Requirement 3)
- SOC 2: Data classification and protection controls

## AWS Well-Architected Security Pillar
- SEC 8: Protect data at rest
- SEC 10: Prepare for security events

## NIST 800-53 Controls
- RA-5: Vulnerability Monitoring and Scanning
- SC-28: Protection of Information at Rest
- SI-4: System Monitoring
- MP-4: Media Storage

---

## Workflows

## Implementation Workflow
```
1. Enable Macie → Configure administrator account
2. Bucket Inventory → Review automated S3 inventory
3. Discovery Jobs → Create targeted classification jobs
4. Custom Identifiers → Add organization-specific patterns
5. Allow Lists → Suppress known false positives
6. Automation → EventBridge + Lambda for response
7. Reporting → Dashboard and Security Hub integration
```

## Remediation Workflow
```
1. Finding Generated → Macie detects sensitive data
2. Triage → Security team reviews severity and data type
3. Classify → Determine data classification level
4. Protect → Apply encryption, access controls, or relocate
5. Validate → Re-scan to confirm remediation
6. Document → Update data classification inventory
```

---

## Working Template

## Configuration

| Setting | Value |
|---------|-------|
| Administrator Account | |
| Regions Enabled | |
| Automated Discovery | Enabled / Disabled |
| Finding Publication | 15min / 1hr / 6hr |
| Export Bucket | |

## S3 Bucket Coverage

| Bucket | Classification Job | Sensitive Data Found | Action Taken |
|--------|-------------------|---------------------|-------------|
| | | | |

## Custom Data Identifiers

| Name | Regex Pattern | Severity Levels | Purpose |
|------|--------------|-----------------|---------|
| | | | |

## Findings Summary

| Severity | Count | Top Data Type | Remediation Status |
|----------|-------|--------------|-------------------|
| Critical | | | |
| High | | | |
| Medium | | | |
| Low | | | |
