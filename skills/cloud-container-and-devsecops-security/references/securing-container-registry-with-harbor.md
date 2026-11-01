# Securing Container Registry With Harbor

## API Reference

## Harbor REST API v2.0

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v2.0/projects` | List all projects |
| PUT | `/api/v2.0/projects/{name}` | Update project settings |
| GET | `/api/v2.0/configurations` | Get system config |
| PUT | `/api/v2.0/configurations` | Update system config |
| GET | `/api/v2.0/projects/{name}/members` | List project members |
| POST | `/api/v2.0/projects/{name}/members` | Add member |
| GET | `/api/v2.0/projects/{name}/immutabletagrules` | List tag rules |
| GET | `/api/v2.0/audit-logs` | Get audit logs |
| GET | `/api/v2.0/projects/{name}/repositories/{repo}/artifacts/{ref}/additions/vulnerabilities` | Get scan results |

## Harbor Roles

| Role ID | Name | Permissions |
|---------|------|------------|
| 1 | ProjectAdmin | Full project control |
| 2 | Maintainer | Push/pull/scan/sign |
| 3 | Developer | Push and pull images |
| 4 | Guest | Pull images only |
| 5 | LimitedGuest | Pull specific repos |

## Security Metadata Fields

| Field | Values | Description |
|-------|--------|-------------|
| `auto_scan` | true/false | Scan images on push |
| `prevent_vul` | true/false | Block vulnerable images |
| `severity` | critical/high/medium | Block threshold |
| `enable_content_trust` | true/false | Notary signing |
| `enable_content_trust_cosign` | true/false | Cosign verification |
| `public` | true/false | Public project access |

## Python Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| `requests` | >=2.28 | Harbor REST API calls |
| `json` | stdlib | Parse API responses |

## References

- Harbor Documentation: https://goharbor.io/docs/
- Harbor API Spec: https://editor.swagger.io/?url=https://raw.githubusercontent.com/goharbor/harbor/main/api/v2.0/swagger.yaml
- Harbor GitHub: https://github.com/goharbor/harbor

---

## Standards and Controls

## NIST SP 800-190 - Container Security
- Use private registries with TLS
- Scan all images for vulnerabilities before deployment
- Sign images and verify signatures
- Implement RBAC on registry access
- Enable audit logging

## CIS Docker Benchmark
- 2.5: Ensure insecure registries are not used
- 4.2: Ensure containers use trusted base images
- 4.4: Ensure images are scanned for vulnerabilities
- 4.5: Ensure Content trust for Docker is enabled

## Harbor Security Features
| Feature | Purpose |
|---------|---------|
| Trivy Scanner | Vulnerability detection in images |
| Content Trust | Image signing with Notary/Cosign |
| RBAC | Role-based project access control |
| Vulnerability Prevention | Block deployment of vulnerable images |
| Immutable Tags | Prevent tag overwriting |
| Audit Logs | Track all registry operations |
| Replication | Secure cross-registry replication |
| Retention Policies | Automated cleanup of old images |
| Robot Accounts | Service-to-service authentication |
| OIDC/LDAP | Enterprise identity integration |

---

## Workflows

## Workflow 1: Secure Image Pipeline
```
[Build Image] --> [Push to Harbor] --> [Auto-Scan (Trivy)] --> [Sign (Cosign)]
                                              |
                                    +---------+---------+
                                    |                   |
                                    v                   v
                            Vulnerabilities?     No vulnerabilities
                            Block deployment     Allow pull
```

## Workflow 2: Registry Hardening
```
Step 1: Enable HTTPS with valid TLS certificates
Step 2: Configure OIDC/LDAP authentication
Step 3: Create projects with auto-scan enabled
Step 4: Enable vulnerability prevention policy
Step 5: Configure content trust (Cosign)
Step 6: Set immutable tag rules for release tags
Step 7: Configure retention policies
Step 8: Enable audit logging
Step 9: Create robot accounts for CI/CD
Step 10: Test with vulnerability gate check
```

---

## Working Template

## Registry Information
| Field | Value |
|-------|-------|
| Harbor URL | |
| Harbor Version | |
| Auth Mode | DB / OIDC / LDAP |
| TLS Enabled | Yes / No |

## Project Security Checklist
| Project | Auto-Scan | Vuln Prevention | Content Trust | Private | Immutable Tags |
|---------|-----------|----------------|--------------|---------|---------------|
| | | | | | |

## Findings and Remediation
| Severity | Finding | Remediation | Status |
|----------|---------|-------------|--------|
| | | | |
