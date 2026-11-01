# Performing Cloud Incident Containment Procedures

## API Reference

## Libraries Used

| Library | Purpose |
|---------|---------|
| `boto3` | AWS SDK for EC2, IAM, Security Groups, and CloudTrail |
| `json` | Parse and log containment actions |
| `datetime` | Timestamp containment events |

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

ec2 = session.client("ec2")
iam = session.client("iam")
```

## Containment Actions

### Isolate EC2 Instance (Security Group Quarantine)
```python
def isolate_instance(instance_id):
    """Replace instance security groups with a quarantine SG that blocks all traffic."""
    # Create quarantine SG if it doesn't exist
    vpc_id = ec2.describe_instances(
        InstanceIds=[instance_id]
    )["Reservations"][0]["Instances"][0]["VpcId"]

    try:
        quarantine_sg = ec2.create_security_group(
            GroupName="quarantine-no-access",
            Description="IR Quarantine — blocks all inbound/outbound",
            VpcId=vpc_id,
        )
        sg_id = quarantine_sg["GroupId"]
        # Revoke default outbound rule
        ec2.revoke_security_group_egress(
            GroupId=sg_id,
            IpPermissions=[{"IpProtocol": "-1", "IpRanges": [{"CidrIp": "0.0.0.0/0"}]}],
        )
    except ec2.exceptions.ClientError:
        # SG already exists
        sgs = ec2.describe_security_groups(
            Filters=[{"Name": "group-name", "Values": ["quarantine-no-access"]}]
        )
        sg_id = sgs["SecurityGroups"][0]["GroupId"]

    # Apply quarantine SG (replaces all existing SGs)
    ec2.modify_instance_attribute(
        InstanceId=instance_id,
        Groups=[sg_id],
    )
    return {"instance_id": instance_id, "quarantine_sg": sg_id, "action": "isolated"}
```

### Disable IAM Access Keys
```python
def disable_user_access_keys(username):
    """Disable all access keys for a compromised IAM user."""
    keys = iam.list_access_keys(UserName=username)
    disabled = []
    for key in keys["AccessKeyMetadata"]:
        if key["Status"] == "Active":
            iam.update_access_key(
                UserName=username,
                AccessKeyId=key["AccessKeyId"],
                Status="Inactive",
            )
            disabled.append(key["AccessKeyId"])
    return {"username": username, "keys_disabled": disabled}
```

### Revoke IAM Role Sessions
```python
def revoke_role_sessions(role_name):
    """Revoke all active sessions for an IAM role."""
    iam.put_role_policy(
        RoleName=role_name,
        PolicyName="RevokeOlderSessions",
        PolicyDocument=json.dumps({
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Deny",
                "Action": "*",
                "Resource": "*",
                "Condition": {
                    "DateLessThan": {
                        "aws:TokenIssueTime": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
                    }
                }
            }]
        }),
    )
    return {"role": role_name, "action": "sessions_revoked"}
```

### Snapshot EBS Volume for Forensics
```python
def snapshot_instance_volumes(instance_id):
    """Create forensic snapshots of all attached EBS volumes."""
    instance = ec2.describe_instances(InstanceIds=[instance_id])
    volumes = instance["Reservations"][0]["Instances"][0].get("BlockDeviceMappings", [])
    snapshots = []
    for vol in volumes:
        vol_id = vol["Ebs"]["VolumeId"]
        snap = ec2.create_snapshot(
            VolumeId=vol_id,
            Description=f"IR forensic snapshot — {instance_id} — {vol_id}",
            TagSpecifications=[{
                "ResourceType": "snapshot",
                "Tags": [
                    {"Key": "Purpose", "Value": "incident-response"},
                    {"Key": "SourceInstance", "Value": instance_id},
                ]
            }],
        )
        snapshots.append({"volume_id": vol_id, "snapshot_id": snap["SnapshotId"]})
    return snapshots
```

### Stop Instance (Preserve State)
```python
def stop_instance(instance_id):
    """Stop instance without terminating to preserve memory and disk."""
    ec2.stop_instances(InstanceIds=[instance_id])
    return {"instance_id": instance_id, "action": "stopped"}
```

### Block Public S3 Bucket Access
```python
s3 = session.client("s3")

def block_public_bucket(bucket_name):
    s3.put_public_access_block(
        Bucket=bucket_name,
        PublicAccessBlockConfiguration={
            "BlockPublicAcls": True,
            "IgnorePublicAcls": True,
            "BlockPublicPolicy": True,
            "RestrictPublicBuckets": True,
        },
    )
    return {"bucket": bucket_name, "action": "public_access_blocked"}
```

## Output Format

```json
{
  "incident_id": "IR-2025-001",
  "containment_time": "2025-01-15T10:30:00Z",
  "actions_taken": [
    {"action": "isolate_instance", "target": "i-0abc123", "status": "success"},
    {"action": "disable_access_keys", "target": "compromised-user", "keys_disabled": 2},
    {"action": "snapshot_volumes", "target": "i-0abc123", "snapshots": 2},
    {"action": "stop_instance", "target": "i-0abc123", "status": "success"}
  ]
}
```

---

## Standards and Controls

## NIST SP 800-61 Rev 2 - Incident Handling Guide
- Containment strategies for cloud environments
- Evidence preservation in ephemeral infrastructure

## CSA Cloud Incident Response Framework
- Cloud Security Alliance incident response procedures
- Shared responsibility model for incident handling
- Multi-cloud containment strategies

## AWS Well-Architected Framework - Security Pillar
- Incident response automation with AWS services
- CloudTrail, GuardDuty, and Security Hub integration
- Reference: https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/

## Microsoft Cloud Security Benchmark
- Azure Defender incident response procedures
- Sentinel playbook automation
- Reference: https://learn.microsoft.com/en-us/security/benchmark/azure/mcsb-incident-response

## GCP Security Best Practices
- Cloud Armor and VPC Service Controls
- Security Command Center integration
- Chronicle SIEM for cloud forensics

## MITRE ATT&CK Cloud Matrix
- Cloud-specific tactics, techniques, and procedures
- Containment mapping to ATT&CK techniques
- Reference: https://attack.mitre.org/matrices/enterprise/cloud/

---

## Workflows

## Workflow 1: AWS Credential Compromise Response

```
START: Compromised AWS Credentials Detected
  |
  v
[Identify Scope]
  |-- Which IAM user/role is compromised?
  |-- What permissions does it have?
  |-- Review CloudTrail for unauthorized actions
  |
  v
[Immediate Containment]
  |-- Disable all access keys
  |-- Attach deny-all inline policy
  |-- Revoke active sessions (date condition)
  |-- Update role trust policy if needed
  |
  v
[Evidence Preservation]
  |-- Export CloudTrail logs to S3 with Object Lock
  |-- Snapshot any accessed resources
  |-- Document all API calls by compromised identity
  |
  v
[Impact Assessment]
  |-- What resources were accessed?
  |-- Was data exfiltrated?
  |-- Were new resources created?
  |-- Were other accounts compromised?
  |
  v
[Remediation]
  |-- Rotate all credentials
  |-- Remove unauthorized resources
  |-- Update IAM policies
  |-- Enable MFA enforcement
  |
  v
END: Containment Complete
```

## Workflow 2: Cloud VM Compromise Response

```
START: Compromised Cloud VM Detected
  |
  v
[Preserve Evidence First]
  |-- Create disk snapshot immediately
  |-- Capture instance metadata
  |-- Export relevant logs
  |
  v
[Network Isolation]
  |-- Apply quarantine security group/NSG
  |-- Remove public IP addresses
  |-- Block outbound traffic
  |-- Maintain forensic access only
  |
  v
[Assess Blast Radius]
  |-- Check lateral movement indicators
  |-- Review IAM role attached to instance
  |-- Check for data access to other services
  |
  v
[Forensic Analysis]
  |-- Mount snapshot to forensic workstation
  |-- Analyze disk for malware/tools
  |-- Review instance logs
  |
  v
[Recovery]
  |-- Rebuild from known-good image
  |-- Apply security hardening
  |-- Restore from clean backup
  |
  v
END: VM Contained and Rebuilt
```

## Workflow 3: Multi-Cloud Containment

```
START: Multi-Cloud Incident
  |
  v
[Identify Affected Cloud Platforms]
  |-- AWS accounts affected?
  |-- Azure subscriptions affected?
  |-- GCP projects affected?
  |
  v
[Parallel Containment]
  |-- AWS: SecurityHub + GuardDuty response
  |-- Azure: Defender + Sentinel playbooks
  |-- GCP: SCC + Chronicle response
  |
  v
[Cross-Cloud Credential Check]
  |-- Shared credentials between platforms?
  |-- Federated identity compromise?
  |-- Third-party integrations affected?
  |
  v
[Unified Evidence Collection]
  |-- Centralize logs from all platforms
  |-- Normalize timestamps to UTC
  |-- Build cross-cloud timeline
  |
  v
END: Multi-Cloud Containment Complete
```

---

## Working Template

## Case Information
| Field | Details |
|-------|---------|
| Case ID | |
| Cloud Platform(s) | AWS / Azure / GCP |
| Incident Type | |
| Containment Start | |
| Containment End | |
| IR Lead | |

## Affected Resources
| Resource | Type | Account/Subscription | Region | Status |
|----------|------|---------------------|--------|--------|
| | | | | |

## Pre-Containment Evidence
- [ ] Disk snapshots created
- [ ] Log exports completed
- [ ] Configuration state captured
- [ ] Network flow logs preserved

## Containment Actions Taken
| # | Time (UTC) | Action | Resource | Result | Executed By |
|---|------------|--------|----------|--------|-------------|
| 1 | | | | | |

## Credential Actions
| Identity | Action | Timestamp | Verified |
|----------|--------|-----------|----------|
| | Keys disabled | | |
| | Sessions revoked | | |
| | Password reset | | |

## Network Isolation
| Resource | Previous SG/NSG | Quarantine SG/NSG | Verified |
|----------|----------------|-------------------|----------|
| | | | |

## Verification Results
- [ ] Compromised resource cannot reach internet
- [ ] Compromised credentials are non-functional
- [ ] Forensic access still available
- [ ] No new unauthorized activity detected

## Next Steps
1. [ ] Eradication planning
2. [ ] Root cause analysis
3. [ ] Recovery procedures
4. [ ] Post-incident review
