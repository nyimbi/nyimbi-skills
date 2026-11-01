# Performing Access Recertification With Saviynt

## API Reference

## Saviynt EIC REST API v5

### Authentication
```python
POST /ECM/api/login
Body: {"username": "admin", "password": "pass"}
Returns: {"access_token": "...", "token_type": "Bearer"}
```

### Certification Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/ECM/api/v5/listCertification` | List campaigns |
| POST | `/ECM/api/v5/getCertificationDetails` | Campaign statistics |
| POST | `/ECM/api/v5/getCertificationItems` | Get review items |
| POST | `/ECM/api/v5/certifyItems` | Certify/revoke items |

### listCertification Payload
| Field | Description |
|-------|-------------|
| `certificationstatus` | `active`, `completed`, `expired` |
| `max` | Maximum results per page |
| `offset` | Pagination offset |

### Certification Item Fields
| Field | Description |
|-------|-------------|
| `username` | Identity under review |
| `entitlement_value` | Access being reviewed |
| `risk_score` | Computed risk (0-10) |
| `last_used_date` | Last access usage date |
| `peer_group_match` | Whether peers have same access |

### certifyItems Actions
| Action | Description |
|--------|-------------|
| `certify` | Approve continued access |
| `revoke` | Remove access |
| `consult` | Request additional reviewer input |

### Campaign Types
| Type | Trigger |
|------|---------|
| User Manager | Manager reviews direct reports |
| Application Owner | App owner reviews all users |
| Entitlement Owner | Entitlement owner reviews holders |
| Event-Based | Triggered by role/department change |

## References
- Saviynt REST API: https://docs.saviyntcloud.com/
- Saviynt Certification: https://docs.saviyntcloud.com/bundle/EIC-Admin-v24x/

---

## Standards and Controls

## Compliance Requirements for Access Reviews

### SOX Section 404 (Sarbanes-Oxley)
- Quarterly access reviews for financially significant applications
- Evidence of review decisions with justification
- Remediation of revoked access within defined SLA
- Separation of duties validation during certification

### SOC 2 Type II
- CC6.1: Logical access controls
- CC6.2: User registration and authorization
- CC6.3: Access modification and removal
- Semi-annual certification campaigns required for trust service criteria

### PCI DSS v4.0
- 7.2.4: User accounts and access reviewed at least every 6 months
- 7.2.5: Application and system accounts reviewed every 6 months
- Evidence of review decisions required

### HIPAA Security Rule
- 164.312(a)(1): Access control standard
- 164.308(a)(3)(ii)(A): Workforce clearance procedure
- 164.308(a)(4): Information access management
- Annual access reviews for PHI-accessing systems

### GDPR Article 5(1)(f)
- Appropriate security of personal data
- Regular access reviews ensure only authorized personnel access PII
- Documentation of access review decisions

## Saviynt Campaign Configuration Standards

### Campaign Frequency by Compliance

| Framework | Minimum Frequency | Scope |
|-----------|------------------|-------|
| SOX | Quarterly | Financial applications |
| SOC 2 | Semi-annually | All in-scope systems |
| PCI DSS | Semi-annually | Cardholder data systems |
| HIPAA | Annually | PHI-accessing systems |
| ISO 27001 | Annually | All systems |
| NIST CSF | Per risk assessment | Risk-based |

### Risk-Based Certification

| Risk Level | Review Frequency | Certifier | Auto-Revoke |
|-----------|-----------------|-----------|-------------|
| Critical | Monthly | CISO + App Owner | 7 days |
| High | Quarterly | Manager + App Owner | 14 days |
| Medium | Semi-annually | Manager | 21 days |
| Low | Annually | Manager | 30 days |

---

## Workflows

## Campaign Execution Workflow

```
WEEK 1: PREPARATION
    ├── Review and update certifier assignments
    ├── Verify identity data freshness (HR sync)
    ├── Validate entitlement data accuracy
    ├── Configure campaign template
    └── Schedule campaign launch

WEEK 2: LAUNCH AND REVIEW
    ├── Launch campaign (auto-notifications sent)
    ├── Certifiers receive email with review link
    ├── Certifiers review each line item:
    │   ├── Check user's current role
    │   ├── Review risk score
    │   ├── Check last access date
    │   ├── Compare with peer group
    │   └── Make certify/revoke decision
    └── Day 7: First reminder sent

WEEK 3: FOLLOW-UP
    ├── Day 10: Second reminder sent
    ├── Day 13: Final reminder (escalation warning)
    ├── Security team contacts non-responsive certifiers
    └── Campaign manager reviews progress dashboard

WEEK 4: CLOSE AND REMEDIATE
    ├── Day 14: Campaign due date
    ├── Day 15: Auto-revoke for non-certified items (if configured)
    ├── Revocation tasks created automatically
    ├── Remediation tickets sent to provisioning team
    ├── Access removed from target systems
    └── Campaign report generated for compliance
```

## Certifier Decision Workflow

```
Certifier opens Saviynt certification inbox
    │
    ├── For each user-entitlement pair:
    │
    │   ├── Review Context:
    │   │   ├── User's name, title, department
    │   │   ├── Entitlement name and application
    │   │   ├── Risk score (1-10)
    │   │   ├── Last access: 3 days ago / 180 days ago / Never
    │   │   ├── Peer analysis: 85% of peers have this access
    │   │   └── SoD violation: None / Conflict detected
    │   │
    │   ├── Decision Logic:
    │   │   ├── Active user + Used recently + Peers have it → CERTIFY
    │   │   ├── Active user + Not used in 90+ days → INVESTIGATE
    │   │   ├── User changed department → LIKELY REVOKE
    │   │   ├── SoD violation detected → REVOKE or ESCALATE
    │   │   └── Cannot determine → DELEGATE to app owner
    │   │
    │   └── Record decision with justification
    │
    └── Submit all decisions
```

## Event-Based Certification Workflow

```
User attribute changes in HR system (e.g., department transfer)
    │
    ├── Saviynt detects change via HR connector sync
    │
    ├── User update rule triggers micro-certification:
    │   ├── Scope: All entitlements for this user
    │   ├── Certifier: New manager
    │   └── Due date: 7 days
    │
    ├── New manager reviews all access:
    │   ├── Certify access relevant to new role
    │   ├── Revoke access specific to old role
    │   └── Request new access if needed
    │
    └── Remediation executes for revoked items
```

## Remediation Tracking Workflow

```
Campaign completes with revoked items
    │
    ├── Saviynt creates provisioning tasks for each revocation
    │
    ├── For each revoked entitlement:
    │   ├── Create deprovisioning request
    │   ├── Route to target system connector
    │   ├── Execute removal (API/connector)
    │   ├── Verify removal succeeded
    │   └── Update audit log
    │
    ├── If automated removal fails:
    │   ├── Create manual remediation ticket (ServiceNow)
    │   ├── Assign to application admin
    │   ├── Track SLA compliance
    │   └── Escalate if overdue
    │
    └── Post-remediation verification:
        ├── Re-scan target systems
        ├── Confirm revoked access no longer present
        └── Archive compliance evidence
```

---

## Working Template

## Campaign Details

| Field | Value |
|-------|-------|
| Campaign Name | |
| Campaign Type | User Manager / Entitlement Owner / Application |
| Scope | All users / Department / Application |
| Launch Date | |
| Due Date | |
| Certifier | Manager / App Owner / Data Owner |

## Campaign Results

| Metric | Count | Percentage |
|--------|-------|------------|
| Total Items | | 100% |
| Certified (Approved) | | |
| Revoked | | |
| Conditionally Certified | | |
| Pending (Not Reviewed) | | |
| Delegated | | |

## Remediation Tracking

| User | Entitlement | Decision | Remediation Status | Completed Date |
|------|------------|----------|-------------------|----------------|
| | | Revoke | Pending/In Progress/Done | |

## Compliance Evidence

- [ ] Campaign configured with appropriate scope
- [ ] All certifiers received notifications
- [ ] Reminder schedule executed (Day 7, 10, 13)
- [ ] Completion rate > 95% before due date
- [ ] Revocation tasks created for all denied items
- [ ] Remediation completed within SLA
- [ ] Campaign report exported and archived
- [ ] Non-responsive certifiers escalated
- [ ] Auto-revoke executed for overdue items

## Sign-Off

| Role | Name | Date |
|------|------|------|
| Campaign Manager | | |
| Compliance Officer | | |
| IT Security Lead | | |
