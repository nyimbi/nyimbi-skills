# Implementing Just In Time Access Provisioning

## API Reference

## Azure AD PIM API (JIT for Azure)

```python
import requests
headers = {"Authorization": "Bearer <token>"}
# Activate eligible role
requests.post(
    "https://graph.microsoft.com/v1.0/roleManagement/directory/roleAssignmentScheduleRequests",
    headers=headers,
    json={"action": "selfActivate", "roleDefinitionId": ROLE_ID,
          "directoryScopeId": "/", "justification": "Incident response",
          "scheduleInfo": {"expiration": {"type": "afterDuration", "duration": "PT4H"}}})
```

## JIT Risk-Based Approval

| Risk Level | Approval | Max Duration |
|-----------|----------|-------------|
| Low | Auto-approve | 4 hours |
| Medium | Manager | 8 hours |
| High | Manager + Security | 4 hours |
| Critical | CISO + Manager + Security | 2 hours |

## AWS IAM Access Analyzer

```bash
# Find unused permissions for JIT conversion
aws accessanalyzer list-findings --analyzer-arn ARN --filter '{"status": {"eq": ["ACTIVE"]}}'
```

## CyberArk PAS REST API (JIT Privileged Access)

```bash
# Request JIT access
curl -X POST "https://VAULT/PasswordVault/api/MyRequests" \
  -H "Authorization: $TOKEN" \
  -d '{"AccountId": "ACC_ID", "Reason": "Maintenance", "TicketingSystemName": "ServiceNow"}'
```

## Key Metrics

| Metric | Target |
|--------|--------|
| Avg approval time | < 15 min |
| Auto-approval rate | 40-60% (low risk) |
| Standing privilege reduction | > 80% |
| Expired access auto-revoked | 100% |

### References

- Azure PIM: https://learn.microsoft.com/en-us/azure/active-directory/privileged-identity-management/
- CyberArk JIT: https://docs.cyberark.com/
- NIST 800-53 AC-6: Least Privilege

---

## Standards and Controls

## NIST Standards
- **NIST SP 800-207**: Zero Trust Architecture - Section 3 (Logical Components)
- **NIST SP 800-53 Rev 5**:
  - AC-2(2): Automated Temporary and Emergency Account Management
  - AC-2(3): Disable Accounts
  - AC-6: Least Privilege
  - AC-6(5): Privileged Accounts
- **NIST SP 1800-35**: Implementing a Zero Trust Architecture

## Zero Trust Frameworks
- **CISA Zero Trust Maturity Model**: Identity pillar - dynamic access provisioning
- **DoD Zero Trust Reference Architecture**: JIT/JEA requirements
- **Forrester ZTX**: Extended Zero Trust with JIT access

## Tools and Platforms
- **Microsoft Entra PIM**: Privileged Identity Management with JIT elevation
- **CyberArk JIT**: Privileged access on-demand
- **SailPoint**: Identity governance with access request workflows
- **HashiCorp Boundary**: Just-in-time access to infrastructure
- **StrongDM**: Dynamic access management

## Compliance
- **SOX**: Least privilege for financial system access
- **PCI DSS 4.0**: Requirement 7.2 - Access based on need to know
- **HIPAA**: Minimum necessary standard for PHI access

---

## Workflows

## Workflow 1: Standard JIT Access Request

### Steps:
1. User submits access request via self-service portal
2. Request includes: target resource, duration, business justification
3. System calculates risk score based on resource sensitivity and user context
4. Risk-based routing:
   - Low risk (< 1 hr, non-privileged): Auto-approve
   - Medium risk: Route to resource owner for approval
   - High risk (privileged, production): Dual approval required
5. Approver notified via email/Slack/Teams
6. Approver reviews and approves/denies with comments
7. On approval: system provisions access with time-bound constraint
8. User notified of access grant with expiration time
9. At expiration: system automatically revokes access
10. All events logged for audit trail

## Workflow 2: Emergency JIT Access (Break-Glass)

### Steps:
1. User declares emergency and requests immediate access
2. System grants access immediately without pre-approval
3. Access limited to shorter maximum duration (e.g., 2 hours)
4. Security team notified of emergency access grant
5. User must provide justification within 24 hours
6. Manager and security team perform post-facto review
7. If review finds access unjustified: security incident opened
8. All emergency access events flagged in audit reports

## Workflow 3: Privileged Elevation with PAM Integration

### Steps:
1. User requests privilege elevation through JIT portal
2. Approval obtained per risk-based workflow
3. JIT system triggers PAM credential checkout
4. PSM session initiated with time-bound credential
5. User performs privileged operations via isolated session
6. Session recorded for audit
7. At expiration: session terminated, credential checked in, password rotated
8. JIT access record closed

## Workflow 4: Vendor/Third-Party JIT Access

### Steps:
1. Internal sponsor submits access request on behalf of vendor
2. Request includes: vendor identity, scope, duration, project reference
3. Dual approval required (sponsor manager + security)
4. Temporary account created with MFA enrollment
5. Access restricted to specified resources only
6. Network access limited to authorized segments
7. Session monitoring enabled
8. Account deactivated at expiration
9. Account deleted after 30-day retention period

---

## Working Template

## Resource Classification
| Resource Type | Risk Level | Max Duration | Auto-Approve | Approvals Required |
|---------------|------------|--------------|--------------|-------------------|
| Read-only access | Low | 1 hour | Yes | 0 |
| Standard application | Medium | 4 hours | No | 1 (manager) |
| Production server | High | 4 hours | No | 2 (manager + security) |
| Database admin | Critical | 2 hours | No | 2 (DBA lead + security) |
| Domain admin | Critical | 1 hour | No | 2 (security + CISO) |
| Cloud admin | Critical | 2 hours | No | 2 (cloud team + security) |

## Approval Workflow Matrix
| Risk Level | Standard Request | Emergency Request |
|------------|-----------------|-------------------|
| Low | Auto-approve | Auto-approve |
| Medium | 1 approval | Auto-approve + post-review |
| High | 2 approvals | Immediate grant + post-review |
| Critical | 2 approvals + MFA | Immediate grant + incident review |

## Request Form Fields
- Requester name and ID
- Target resource/system
- Access level requested
- Duration requested (within policy maximum)
- Business justification
- Related ticket/incident number
- Emergency flag (yes/no)

## SLA Targets
| Metric | Target |
|--------|--------|
| Mean time to access (low risk) | < 1 minute |
| Mean time to access (medium risk) | < 15 minutes |
| Mean time to access (high risk) | < 30 minutes |
| Emergency access grant | < 2 minutes |
| Access revocation at expiry | Immediate (< 1 minute) |
| Post-emergency review | Within 24 hours |

## Monitoring Alerts
- [ ] Emergency access granted
- [ ] Access duration extended
- [ ] Approved access not used within 30 minutes
- [ ] Unusual access patterns detected
- [ ] Approval SLA breached
- [ ] Revocation failure
