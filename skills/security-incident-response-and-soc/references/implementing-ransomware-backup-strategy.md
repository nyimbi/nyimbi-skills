# Implementing Ransomware Backup Strategy

## API Reference

## Libraries Used

| Library | Purpose |
|---------|---------|
| `boto3` | AWS SDK for S3, AWS Backup, and IAM auditing |
| `json` | Parse backup policies and compliance data |
| `subprocess` | Run local backup verification commands |
| `datetime` | Calculate backup age and RPO/RTO compliance |

## Installation

```bash
pip install boto3
```

## Authentication

```python
import boto3
import os

session = boto3.Session(
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    region_name=os.environ.get("AWS_REGION", "us-east-1"),
)

s3 = session.client("s3")
backup = session.client("backup")
iam = session.client("iam")
```

## AWS S3 Backup Audit

### Check Bucket Versioning (Ransomware Recovery)
```python
def audit_s3_versioning():
    findings = []
    buckets = s3.list_buckets()["Buckets"]
    for bucket in buckets:
        name = bucket["Name"]
        versioning = s3.get_bucket_versioning(Bucket=name)
        status = versioning.get("Status", "Disabled")
        mfa_delete = versioning.get("MFADelete", "Disabled")

        if status != "Enabled":
            findings.append({
                "bucket": name,
                "issue": "Versioning not enabled",
                "severity": "high",
                "remediation": "Enable versioning for ransomware recovery",
            })
        if mfa_delete != "Enabled":
            findings.append({
                "bucket": name,
                "issue": "MFA Delete not enabled",
                "severity": "medium",
                "remediation": "Enable MFA Delete to prevent bulk deletion",
            })
    return findings
```

### Check Object Lock (Immutable Backups)
```python
def check_object_lock(bucket_name):
    try:
        config = s3.get_object_lock_configuration(Bucket=bucket_name)
        lock = config["ObjectLockConfiguration"]
        rule = lock.get("Rule", {}).get("DefaultRetention", {})
        return {
            "bucket": bucket_name,
            "object_lock_enabled": lock.get("ObjectLockEnabled") == "Enabled",
            "retention_mode": rule.get("Mode", "NONE"),
            "retention_days": rule.get("Days", 0),
        }
    except s3.exceptions.ClientError:
        return {"bucket": bucket_name, "object_lock_enabled": False}
```

### Check Cross-Region Replication
```python
def check_cross_region_replication(bucket_name):
    try:
        repl = s3.get_bucket_replication(Bucket=bucket_name)
        rules = repl["ReplicationConfiguration"]["Rules"]
        return {
            "bucket": bucket_name,
            "replication_enabled": True,
            "destinations": [
                r["Destination"]["Bucket"] for r in rules if r["Status"] == "Enabled"
            ],
        }
    except s3.exceptions.ClientError:
        return {"bucket": bucket_name, "replication_enabled": False}
```

## AWS Backup Service

### List Backup Plans
```python
def list_backup_plans():
    plans = backup.list_backup_plans()["BackupPlansList"]
    result = []
    for plan in plans:
        detail = backup.get_backup_plan(BackupPlanId=plan["BackupPlanId"])
        rules = detail["BackupPlan"]["Rules"]
        result.append({
            "name": plan["BackupPlanName"],
            "id": plan["BackupPlanId"],
            "rules": [
                {
                    "name": r["RuleName"],
                    "schedule": r.get("ScheduleExpression"),
                    "lifecycle_delete_days": r.get("Lifecycle", {}).get("DeleteAfterDays"),
                    "lifecycle_cold_days": r.get("Lifecycle", {}).get("MoveToColdStorageAfterDays"),
                    "target_vault": r["TargetBackupVaultName"],
                }
                for r in rules
            ],
        })
    return result
```

### Audit Backup Vault Access Policy
```python
def audit_vault_access(vault_name):
    try:
        policy = backup.get_backup_vault_access_policy(BackupVaultName=vault_name)
        policy_doc = json.loads(policy["Policy"])
        # Check for overly permissive policies
        findings = []
        for stmt in policy_doc.get("Statement", []):
            if stmt.get("Effect") == "Allow" and stmt.get("Principal") == "*":
                findings.append({
                    "vault": vault_name,
                    "issue": "Vault policy allows public access",
                    "severity": "critical",
                })
        return findings
    except backup.exceptions.ClientError:
        return [{"vault": vault_name, "issue": "No access policy set", "severity": "medium"}]
```

### List Recovery Points (Check Backup Freshness)
```python
from datetime import datetime, timezone

def check_backup_freshness(vault_name, max_age_hours=24):
    recovery_points = backup.list_recovery_points_by_backup_vault(
        BackupVaultName=vault_name, MaxResults=100
    )["RecoveryPoints"]

    stale = []
    for rp in recovery_points:
        age = datetime.now(timezone.utc) - rp["CreationDate"]
        if age.total_seconds() > max_age_hours * 3600:
            stale.append({
                "resource": rp["ResourceArn"],
                "last_backup": rp["CreationDate"].isoformat(),
                "age_hours": round(age.total_seconds() / 3600),
                "status": rp["Status"],
            })
    return stale
```

## 3-2-1 Backup Rule Audit

```python
def audit_321_rule(bucket_name):
    """Verify the 3-2-1 backup rule: 3 copies, 2 media types, 1 offsite."""
    versioning = s3.get_bucket_versioning(Bucket=bucket_name)
    replication = check_cross_region_replication(bucket_name)
    object_lock = check_object_lock(bucket_name)

    score = {
        "three_copies": versioning.get("Status") == "Enabled",
        "two_media": replication["replication_enabled"],
        "one_offsite": replication["replication_enabled"],
        "immutable": object_lock["object_lock_enabled"],
    }
    score["compliant"] = all([score["three_copies"], score["two_media"], score["one_offsite"]])
    return score
```

## Output Format

```json
{
  "audit_date": "2025-01-15",
  "backup_strategy": {
    "total_buckets": 15,
    "versioning_enabled": 12,
    "object_lock_enabled": 5,
    "cross_region_replication": 8,
    "three_two_one_compliant": 4
  },
  "backup_plans": 3,
  "recovery_points_stale": 2,
  "findings": [
    {
      "resource": "critical-data-bucket",
      "issue": "No Object Lock — vulnerable to ransomware deletion",
      "severity": "high",
      "remediation": "Enable S3 Object Lock in COMPLIANCE mode"
    }
  ]
}
```

---

## Standards and Controls

## Industry Standards

### NIST SP 800-209: Security Guidelines for Storage Infrastructure
- Defines security controls for storage systems including backup infrastructure
- Covers access control, encryption, integrity verification, and audit logging for storage
- Section 5.3: Backup and recovery security controls

### NIST IR 8374: Ransomware Risk Management
- Identifies backup as a critical control in the Recover function
- Recommends maintaining offline, encrypted backups with regular testing
- Emphasizes credential separation for backup administration

### CISA #StopRansomware Guide (2023, updated 2025)
- Prescribes 3-2-1 backup rule as baseline, recommends extending to 3-2-1-1-0
- Mandates backup credential isolation from production domains
- Requires documented and tested recovery procedures

### CIS Controls v8
- Control 11: Data Recovery
  - 11.1: Establish and maintain a data recovery process
  - 11.2: Perform automated backups
  - 11.3: Protect recovery data (encryption, access control)
  - 11.4: Establish and maintain an isolated instance of recovery data (air-gapped/immutable)
  - 11.5: Test data recovery

### ISO 27001:2022
- A.8.13: Information backup
- A.8.14: Redundancy of information processing facilities

## Regulatory Requirements

### PCI DSS v4.0
- Requirement 9.4.1: Backup media physically secured
- Requirement 12.10.1: Incident response plan includes recovery procedures

### HIPAA Security Rule
- 45 CFR 164.308(a)(7): Contingency plan including data backup, disaster recovery, emergency mode operation
- 45 CFR 164.312(a)(2)(ii): Emergency access procedure

### SOX
- Section 302/404: Internal controls over financial reporting must include IT controls for data backup and recovery

## Vendor Documentation

### Veeam
- Hardened Repository Guide: https://helpcenter.veeam.com/docs/backup/vsphere/hardened_repository.html
- SureBackup: https://helpcenter.veeam.com/docs/backup/vsphere/surebackup_job.html
- Immutability: https://helpcenter.veeam.com/docs/backup/vsphere/immutability.html

### AWS
- S3 Object Lock: https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html
- AWS Backup Vault Lock: https://docs.aws.amazon.com/aws-backup/latest/devguide/vault-lock.html

### Azure
- Immutable Blob Storage: https://learn.microsoft.com/en-us/azure/storage/blobs/immutable-storage-overview
- Azure Backup Immutable Vault: https://learn.microsoft.com/en-us/azure/backup/backup-azure-immutable-vault-concept

---

## Workflows

## Workflow 1: Initial Backup Architecture Design

```
Start
  |
  v
[Inventory all systems and data] --> Classify into Tier 1/2/3 by business impact
  |
  v
[Define RPO/RTO per tier] --> Document in recovery plan
  |
  v
[Select backup platform] --> Veeam / Rubrik / Commvault / Cohesity
  |
  v
[Design 3-2-1-1-0 architecture]
  |-- Copy 1: Local repository (fast restore)
  |-- Copy 2: Secondary site/cloud (different media)
  |-- Copy 3: Offsite (geographic separation)
  |-- +1: Immutable or air-gapped copy
  |-- +0: Automated restore verification
  |
  v
[Isolate backup credentials]
  |-- Remove from production AD
  |-- Deploy MFA for backup admin access
  |-- Segment backup network
  |
  v
[Configure immutable storage]
  |-- Linux Hardened Repository (XFS immutability)
  |-- S3 Object Lock / Azure Immutable Blob
  |-- Tape air-gap rotation
  |
  v
[Set backup schedules per tier]
  |
  v
[Configure automated restore testing]
  |-- SureBackup / SureReplica
  |-- Verify boot, network, application health
  |
  v
[Document recovery runbook]
  |
  v
End
```

## Workflow 2: Restore Verification Process

```
Start (Scheduled - Weekly for Tier 1, Monthly for Tier 2)
  |
  v
[SureBackup job triggers VM restore to isolated sandbox]
  |
  v
[VM boots in isolated network segment]
  |
  v
[Heartbeat check] -- Fail --> Alert backup team
  |
  Pass
  |
  v
[Network ping check] -- Fail --> Alert backup team
  |
  Pass
  |
  v
[Application-specific check]
  |-- AD: LDAP query test
  |-- SQL: Database consistency check
  |-- Web: HTTP 200 response
  |-- Email: SMTP handshake
  |
  Fail --> Alert backup team with diagnostic details
  |
  Pass
  |
  v
[Log successful restore] --> Update compliance dashboard
  |
  v
[Clean up sandbox VMs]
  |
  v
End
```

## Workflow 3: Emergency Ransomware Recovery

```
Ransomware Incident Declared
  |
  v
[Isolate affected systems from network]
  |
  v
[Verify backup integrity]
  |-- Check immutable copies are unaffected
  |-- Validate backup timestamps predate infection
  |-- Scan backup files for ransomware artifacts
  |
  v
[Determine recovery scope]
  |-- Full environment rebuild vs. selective restore
  |-- Prioritize by tier: AD/DNS first, then Tier 1, then Tier 2/3
  |
  v
[Rebuild infrastructure in clean environment]
  |-- Deploy clean OS images
  |-- Restore AD from immutable backup
  |-- Validate AD integrity with ADRestore/DSInternals
  |
  v
[Restore applications in dependency order]
  |-- Database servers before application servers
  |-- Internal services before external-facing
  |
  v
[Validate restored systems]
  |-- Application functionality testing
  |-- Data integrity verification
  |-- Security control validation
  |
  v
[Reconnect to network in phases]
  |-- Monitor for re-infection indicators
  |-- Validate no persistence mechanisms in restored systems
  |
  v
[Post-recovery documentation and lessons learned]
  |
  v
End
```

## Workflow 4: Backup Health Monitoring

```
Daily Automated Check
  |
  v
[Query backup job status via API/PowerShell]
  |
  v
[Check for failed or warning jobs]
  |-- Failed --> Create P1 ticket, alert backup team
  |-- Warning --> Create P3 ticket, investigate within 24hr
  |-- Success --> Log and continue
  |
  v
[Verify backup repository capacity]
  |-- >85% utilization --> Alert for capacity planning
  |-- >95% utilization --> Critical alert, backup jobs at risk
  |
  v
[Check immutable copy synchronization]
  |-- Verify last immutable copy is within RPO window
  |-- Alert if immutable copy is stale
  |
  v
[Generate weekly backup health report]
  |-- Success rate percentage
  |-- Data protected volume
  |-- Restore test results
  |-- Capacity forecast
  |
  v
End
```

---

## Working Template

## Organization Information

| Field | Value |
|-------|-------|
| Organization Name | |
| Assessment Date | |
| Assessor Name | |
| Backup Solution | |
| Number of Servers | |
| Total Data Volume | |

## Current Backup Architecture

### Backup Copies Inventory

| Copy # | Location | Media Type | Offsite? | Immutable? | Air-Gapped? | Retention | Encrypted? | Last Successful |
|--------|----------|------------|----------|------------|-------------|-----------|------------|-----------------|
| 1 | | | | | | | | |
| 2 | | | | | | | | |
| 3 | | | | | | | | |

### 3-2-1-1-0 Compliance Checklist

- [ ] **3 Copies**: At least 3 copies of data exist
- [ ] **2 Media Types**: Backups stored on at least 2 different media types
- [ ] **1 Offsite**: At least 1 copy stored offsite or in a different geographic location
- [ ] **1 Immutable/Air-Gapped**: At least 1 copy is immutable or physically air-gapped
- [ ] **0 Errors**: Automated restore testing passes with zero errors

## Recovery Tier Classification

### Tier 1 - Critical Systems

| System | RPO Target | RTO Target | Backup Frequency | Dependencies |
|--------|-----------|-----------|-------------------|--------------|
| | | | | |

### Tier 2 - Important Systems

| System | RPO Target | RTO Target | Backup Frequency | Dependencies |
|--------|-----------|-----------|-------------------|--------------|
| | | | | |

### Tier 3 - Standard Systems

| System | RPO Target | RTO Target | Backup Frequency | Dependencies |
|--------|-----------|-----------|-------------------|--------------|
| | | | | |

## Credential Isolation Assessment

| Control | Status | Evidence |
|---------|--------|----------|
| Backup servers removed from production AD | Yes / No | |
| Dedicated backup admin accounts | Yes / No | |
| MFA enabled for backup console | Yes / No | |
| Backup network segmented | Yes / No | |
| RDP disabled on backup servers | Yes / No | |
| Backup encryption keys stored separately | Yes / No | |

## Restore Testing History

| Date | Tier | Systems Tested | Result | RTO Achieved | Issues |
|------|------|---------------|--------|-------------|--------|
| | | | | | |

## Gap Analysis

| Control | Current State | Target State | Gap | Priority | Effort |
|---------|--------------|-------------|-----|----------|--------|
| Immutable backup | | | | | |
| Credential isolation | | | | | |
| Restore testing | | | | | |
| Offsite copy | | | | | |
| Encryption | | | | | |

## Recommendations

### Critical Priority

1. **[Finding]**: [Recommendation] - Estimated effort: [X days/weeks]

### High Priority

1. **[Finding]**: [Recommendation] - Estimated effort: [X days/weeks]

### Medium Priority

1. **[Finding]**: [Recommendation] - Estimated effort: [X days/weeks]

## Recovery Runbook Checklist

### Pre-Recovery
- [ ] Incident declared and scope determined
- [ ] Affected systems isolated from network
- [ ] Backup integrity verified (immutable copies confirmed clean)
- [ ] Backup timestamps verified to predate infection
- [ ] Recovery environment prepared (clean network, fresh OS images)

### Recovery Execution
- [ ] Phase 1: Identity infrastructure (AD, DNS, DHCP)
- [ ] Phase 2: Tier 1 critical systems
- [ ] Phase 3: Tier 2 important systems
- [ ] Phase 4: Tier 3 standard systems
- [ ] Each restored system validated before connecting to network

### Post-Recovery
- [ ] All restored systems scanned for persistence mechanisms
- [ ] Security controls validated (EDR, firewall rules, MFA)
- [ ] Users notified and credentials reset
- [ ] Recovery time documented against RTO targets
- [ ] Lessons learned documented

## Sign-Off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| IT Director | | | |
| CISO | | | |
| Backup Admin | | | |
