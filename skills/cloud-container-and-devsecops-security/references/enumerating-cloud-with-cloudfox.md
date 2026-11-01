# Enumerating Cloud With Cloudfox

## API Reference

## Global Invocation

```
cloudfox <provider> [global-flags] <command>
```

| Flag | Description |
|------|-------------|
| `--profile <name>` | AWS named profile to use |
| `-o, --outdir <dir>` | Output directory for results/loot |
| `--region <region>` | Restrict to a region (where applicable) |
| `-v` | Verbosity level |
| `AWS_PROFILE` (env) | Alternative to `--profile` |

## AWS Commands (selection)

| Command | Description |
|---------|-------------|
| `all-checks` | Run all AWS enumeration commands with defaults |
| `inventory` | Account size / resource counts by region |
| `endpoints` | Internet-reachable service endpoints |
| `instances` | EC2 instances with IPs and instance-profile roles |
| `principals` | IAM users and roles |
| `permissions` | Effective IAM permissions per principal |
| `iam-simulator` | Simulate whether principals can perform actions |
| `role-trusts` | Who can assume which roles (assume-role paths) |
| `access-keys` | Active IAM access keys |
| `secrets` | Secrets from Secrets Manager and SSM Parameter Store |
| `buckets` | S3 buckets |
| `ecr` | Elastic Container Registry repositories/images |
| `lambda` | Lambda functions and configuration |
| `route53` | Hosted zones and records |
| `ram` | Resource Access Manager shares |
| `sns` / `sqs` | Messaging resources |
| `env-vars` | Environment variables across services |

## Azure Commands

| Command | Description |
|---------|-------------|
| `inventory` | Resource inventory by location/subscription |
| `rbac` | Role-based access control assignments |
| `storage` | Storage accounts and access data |
| `vms` | Virtual machines |

## Output Layout

CloudFox writes to `<outdir>/cloudfox-output/<provider>/<account-or-sub>/`:
- `table/` and `csv/` — per-command findings
- `loot/` — ready-to-run follow-up commands (e.g., `aws s3 ls`, `ssm start-session`)
- A combined log of the run

---

## Standards and Controls

## NIST Cybersecurity Framework 2.0

| ID | Name | Rationale |
|----|------|-----------|
| ID.AM-03 | Organizational communication and data flows are mapped (asset/inventory management) | CloudFox builds an attacker-centric inventory of cloud assets, identities, and trust relationships, informing asset-management gaps. |

## MITRE ATT&CK (Enterprise / Cloud)

| ID | Name | Rationale |
|----|------|-----------|
| T1526 | Cloud Service Discovery | CloudFox enumerates available cloud services and resources. |
| T1580 | Cloud Infrastructure Discovery | Inventory/instances/buckets map the infrastructure footprint. |
| T1087.004 | Account Discovery: Cloud Account | `principals`/`access-keys` enumerate cloud identities. |
| T1069.003 | Permission Groups Discovery: Cloud Groups | `permissions`/`role-trusts` reveal cloud entitlements. |
| T1538 | Cloud Service Dashboard | Aggregated cross-service situational awareness. |

## Supporting References

- BishopFox CloudFox — https://github.com/BishopFox/cloudfox
- NIST CSF 2.0 — https://www.nist.gov/cyberframework
