# Performing Service Account Credential Rotation

## API Reference

## AWS IAM CLI Key Rotation

| Command | Description |
|---------|-------------|
| `aws iam create-access-key --user-name <user>` | Create new access key |
| `aws iam list-access-keys --user-name <user>` | List existing keys |
| `aws iam update-access-key --access-key-id <id> --status Inactive` | Deactivate old key |
| `aws iam delete-access-key --access-key-id <id> --user-name <user>` | Delete old key |

## Azure AD CLI Credential Rotation

| Command | Description |
|---------|-------------|
| `az ad app credential reset --id <app-id> --years 1` | Generate new client secret |
| `az ad app credential list --id <app-id>` | List current credentials |
| `az ad app credential delete --id <app-id> --key-id <key-id>` | Remove old credential |

## HashiCorp Vault Database Secrets Engine

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/database/creds/{role}` | GET | Generate dynamic database credentials |
| `/v1/database/config/{name}` | POST | Configure database connection |
| `/v1/database/roles/{name}` | POST | Create dynamic credential role |
| `/v1/sys/leases/revoke` | PUT | Revoke a dynamic credential lease |

### Vault Request Headers

| Header | Value |
|--------|-------|
| `X-Vault-Token` | Vault authentication token |
| `Content-Type` | `application/json` |

## GCP Service Account Key Rotation

| Command | Description |
|---------|-------------|
| `gcloud iam service-accounts keys create` | Create new key |
| `gcloud iam service-accounts keys list --iam-account <sa>` | List keys |
| `gcloud iam service-accounts keys delete <key-id>` | Delete old key |

## Python Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| `subprocess` | stdlib | Execute AWS/Azure/GCP CLI commands |
| `requests` | >=2.28 | HashiCorp Vault HTTP API calls |
| `hvac` | >=2.1 | HashiCorp Vault Python client |
| `boto3` | >=1.26 | AWS IAM programmatic key rotation |

## References

- AWS Secrets Manager Rotation: https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html
- HashiCorp Vault Database Engine: https://developer.hashicorp.com/vault/docs/secrets/databases
- Azure Key Vault Rotation: https://learn.microsoft.com/en-us/azure/key-vault/secrets/tutorial-rotation
- GCP Key Rotation: https://cloud.google.com/iam/docs/key-rotation

---

## Standards and Controls

## Compliance Requirements

### NIST SP 800-63B - Digital Identity Guidelines
- Authenticator lifecycle management
- Credential rotation for compromised or expired secrets
- Automated mechanisms for credential management preferred

### PCI DSS v4.0
- 8.3.9: Passwords/passphrases for application and system accounts changed periodically (at least every 90 days)
- 8.6.1: Interactive use of system and application accounts managed
- 8.6.3: Passwords for application and system accounts protected against misuse

### SOC 2 - CC6.1
- Logical access controls restrict access to information assets
- Credentials are managed throughout their lifecycle
- Service account credentials rotated per policy

### CIS Controls v8
- 5.2: Use unique passwords
- 5.4: Restrict admin privileges to dedicated accounts
- 5.5: Establish and maintain inventory of service accounts

## Rotation Frequency Standards

| Account Type | NIST Guideline | PCI DSS | CIS Benchmark | Recommended |
|-------------|----------------|---------|---------------|-------------|
| Domain Admin | 60 days | 90 days | 90 days | 30 days |
| Service Account (AD) | gMSA auto | 90 days | 90 days | gMSA (auto 30 days) |
| Cloud Access Keys | 90 days | 90 days | 90 days | 90 days or eliminate |
| Database Admin | 60 days | 90 days | 90 days | Dynamic secrets (per-session) |
| API Keys | 90 days | N/A | 90 days | 90 days or short-lived tokens |

## Technology Standards

### gMSA (Group Managed Service Accounts)
- Windows Server 2012+ domain functional level
- KDS Root Key required (one per forest)
- 240-byte cryptographically random passwords
- Automatic rotation every 30 days by default
- Multiple hosts can share same gMSA

### PKCS#12 / X.509 Certificate Rotation
- Certificate-based authentication preferred over passwords
- Auto-renewal via ACME protocol or internal CA
- Certificate pinning considerations for service-to-service auth

---

## Workflows

## Automated Rotation Workflow

```
Rotation Scheduler (cron/secrets manager)
    │
    ├── Pre-Rotation Checks:
    │   ├── Verify service account exists and is active
    │   ├── Verify all dependent services are healthy
    │   ├── Confirm change window (maintenance window)
    │   └── Notify operations team of pending rotation
    │
    ├── Generate New Credential:
    │   ├── Create new password/key with required complexity
    │   ├── Store new credential in secrets vault
    │   └── Maintain old credential as backup
    │
    ├── Update Source System:
    │   ├── AD: Set-ADAccountPassword
    │   ├── AWS: CreateAccessKey
    │   ├── Azure: Add client secret to service principal
    │   ├── GCP: Create new service account key
    │   └── DB: ALTER USER ... PASSWORD ...
    │
    ├── Propagate to Consumers:
    │   ├── Update application config (env vars, config files)
    │   ├── Update Kubernetes secrets
    │   ├── Update CI/CD pipeline secrets
    │   ├── Restart dependent services if required
    │   └── Wait for propagation
    │
    ├── Post-Rotation Verification:
    │   ├── Health check all dependent services
    │   ├── Test authentication with new credentials
    │   ├── Verify old credential no longer works
    │   └── Log rotation success/failure
    │
    └── Cleanup:
        ├── Deactivate old credential after grace period
        ├── Delete old credential after confirmation
        └── Update rotation audit log
```

## Emergency Rotation Workflow (Credential Compromise)

```
Credential compromise detected
    │
    ├── IMMEDIATE (within 15 minutes):
    │   ├── Disable compromised credential
    │   ├── Generate new credential
    │   ├── Update source system
    │   └── Notify incident response team
    │
    ├── SHORT-TERM (within 1 hour):
    │   ├── Propagate new credential to all consumers
    │   ├── Verify service health
    │   ├── Review audit logs for unauthorized use
    │   └── Assess blast radius of compromise
    │
    └── FOLLOW-UP (within 24 hours):
        ├── Complete incident report
        ├── Review rotation procedures
        ├── Update dependent service configurations
        └── Rotate any related credentials
```

## gMSA Migration Workflow

```
Identify service accounts eligible for gMSA migration
    │
    ├── For each eligible service account:
    │   ├── Create gMSA in Active Directory
    │   ├── Add target servers to PrincipalsAllowedToRetrieve
    │   ├── Install gMSA on each target server
    │   ├── Test gMSA retrieval (Test-ADServiceAccount)
    │   │
    │   ├── During maintenance window:
    │   │   ├── Stop the service
    │   │   ├── Change service logon account to gMSA
    │   │   ├── Update file/folder permissions if needed
    │   │   ├── Start the service
    │   │   └── Verify service functionality
    │   │
    │   └── Post-migration:
    │       ├── Disable old service account
    │       ├── Monitor service for 2 weeks
    │       └── Delete old account after confirmation
    │
    └── Update service account inventory
```

---

## Working Template

## Rotation Campaign

| Field | Value |
|-------|-------|
| Campaign Date | |
| Rotation Window | |
| Operator | |
| Change Ticket | |

## Service Account Inventory

| Account Name | Platform | Type | Last Rotated | Dependent Services | Status |
|-------------|----------|------|-------------|-------------------|--------|
| | AD/AWS/GCP/Azure/DB | Password/Key/Cert | | | Pending/Done/Failed |

## Rotation Results

| Account | New Credential Stored | Source Updated | Consumers Updated | Health Check | Result |
|---------|----------------------|---------------|-------------------|-------------|--------|
| | Yes/No | Yes/No | Yes/No | Pass/Fail | Success/Failed |

## Post-Rotation Verification

- [ ] All new credentials stored in secrets vault
- [ ] All source systems updated with new credentials
- [ ] All consumer applications restarted/reconfigured
- [ ] Health checks passing for all dependent services
- [ ] Old credentials deactivated/deleted
- [ ] Audit log exported and archived
- [ ] Operations team notified of completion
