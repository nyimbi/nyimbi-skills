# Detecting AWS Guardduty Findings Automation

## API Reference

## Libraries

| Library | Install | Purpose |
|---------|---------|---------|
| boto3 | `pip install boto3` | AWS SDK for GuardDuty API |

## Key boto3 GuardDuty Methods

| Method | Description |
|--------|-------------|
| `list_detectors()` | List GuardDuty detector IDs |
| `get_detector(DetectorId=)` | Get detector configuration |
| `list_findings(DetectorId=, FindingCriteria=)` | Query finding IDs |
| `get_findings(DetectorId=, FindingIds=[])` | Get finding details |
| `get_findings_statistics(DetectorId=)` | Finding counts by severity |
| `archive_findings(DetectorId=, FindingIds=[])` | Archive processed findings |
| `list_members(DetectorId=)` | List member accounts (multi-account) |
| `create_sample_findings(DetectorId=)` | Generate sample findings for testing |

## Finding Severity Levels

| Range | Level | Description |
|-------|-------|-------------|
| 7.0-8.9 | High | Compromised resource, active threat |
| 4.0-6.9 | Medium | Suspicious activity, potential threat |
| 1.0-3.9 | Low | Attempted suspicious activity |

## GuardDuty Finding Types

| Type Prefix | Category |
|-------------|----------|
| `Recon:` | Reconnaissance activity |
| `UnauthorizedAccess:` | Unauthorized access attempt |
| `CryptoCurrency:` | Crypto mining activity |
| `Trojan:` | Malware communication |
| `Stealth:` | Logging/monitoring evasion |
| `Policy:` | Policy violation |
| `Persistence:` | Persistence mechanism |

## GuardDuty Protection Features

| Feature | Description |
|---------|-------------|
| S3_DATA_EVENTS | S3 data plane monitoring |
| EKS_AUDIT_LOGS | EKS control plane monitoring |
| EBS_MALWARE_PROTECTION | EBS volume malware scanning |
| RDS_LOGIN_EVENTS | RDS login activity monitoring |
| LAMBDA_NETWORK_LOGS | Lambda function network monitoring |
| RUNTIME_MONITORING | EC2/ECS/EKS runtime threat detection |

## FindingCriteria Filter

```python
criteria = {
    "Criterion": {
        "severity": {"Gte": 7.0},
        "service.archived": {"Eq": ["false"]},
        "type": {"Eq": ["UnauthorizedAccess:EC2/SSHBruteForce"]},
    }
}
```

## External References

- [GuardDuty API Reference](https://docs.aws.amazon.com/guardduty/latest/APIReference/)
- [GuardDuty Finding Types](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_finding-types-active.html)
- [GuardDuty Multi-Account](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_accounts.html)

---

## Standards and Controls

## MITRE ATT&CK Mapping
- TA0001 Initial Access: UnauthorizedAccess findings
- TA0003 Persistence: Persistence:IAMUser findings
- TA0005 Defense Evasion: Stealth findings
- TA0006 Credential Access: CredentialAccess findings
- TA0010 Exfiltration: Exfiltration findings
- TA0040 Impact: CryptoCurrency/Trojan findings

## NIST 800-53
- IR-4: Incident Handling
- IR-5: Incident Monitoring
- SI-4: System Monitoring
- AU-6: Audit Record Review

## AWS Security Best Practices
- Enable GuardDuty in all regions
- Configure multi-account with Organizations
- Publish findings every 15 minutes
- Integrate with Security Hub

---

## Workflows

## Automated Response Workflow
```
1. GuardDuty detects threat → Generates finding
2. EventBridge receives finding event
3. EventBridge routes to Lambda based on severity/type
4. Lambda executes automated response:
   - EC2: Quarantine instance, snapshot volumes
   - IAM: Deactivate keys, apply deny policy
   - S3: Block public access, enable versioning
5. SNS notifies security team
6. Finding synced to Security Hub
7. Analyst reviews and confirms actions
```

## Triage Workflow
```
1. HIGH (7-8.9): Immediate auto-response + page on-call
2. MEDIUM (4-6.9): Auto-notify + queue for review
3. LOW (1-3.9): Log and batch review weekly
```

---

## Working Template

## Configuration
| Setting | Value |
|---------|-------|
| Detector ID | |
| Publishing Frequency | 15min / 1hr / 6hr |
| Multi-Account | Yes / No |
| Security Hub Integration | Enabled / Disabled |

## EventBridge Rules
| Rule Name | Severity Threshold | Target | Status |
|-----------|-------------------|--------|--------|
| guardduty-critical | >= 8.0 | Lambda + PagerDuty | |
| guardduty-high | >= 7.0 | Lambda + SNS | |
| guardduty-medium | >= 4.0 | SNS | |

## Auto-Response Actions
| Finding Type | Action | Lambda Function | Tested |
|-------------|--------|----------------|--------|
| EC2 Compromise | Quarantine + Snapshot | [ ] | |
| IAM Credential | Deactivate + Deny | [ ] | |
| S3 Exfiltration | Block Public Access | [ ] | |
