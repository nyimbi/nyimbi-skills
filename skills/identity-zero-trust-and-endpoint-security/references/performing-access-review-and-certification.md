# Performing Access Review And Certification

## API Reference

## CSV Input Format
```csv
username,entitlement,application,manager,status,last_used,risk_score
jsmith,Admin,SAP,mjones,active,2025-01-15T00:00:00Z,8
```

## SoD Rules JSON Format
```json
[{"name": "Finance SoD", "role_a": "AP_Approver", "role_b": "AP_Creator"}]
```

## Key Review Checks
| Check | Description | Severity |
|-------|-------------|----------|
| Orphaned accounts | No manager or terminated status | HIGH |
| SoD violations | Conflicting entitlements held | CRITICAL |
| Excessive access | Entitlement count above threshold | MEDIUM |
| Stale entitlements | Unused beyond retention period | MEDIUM |

## Compliance Frameworks
| Framework | Requirement |
|-----------|-------------|
| SOX Section 404 | Periodic access reviews for financial systems |
| SOC 2 CC6.1 | Logical access controls and reviews |
| HIPAA 164.312(a) | Access authorization and review |
| PCI DSS 7.2 | Restrict access based on need-to-know |

## Review Campaign Design
| Parameter | Best Practice |
|-----------|---------------|
| Frequency | Quarterly for privileged, semi-annual for standard |
| Reviewer | Direct manager + application owner |
| Escalation | Auto-revoke if no response within 14 days |
| Evidence | Export decisions with timestamps and reviewer ID |

## References
- NIST SP 800-53 AC-6: https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final
- ISACA Access Review: https://www.isaca.org/

---

## Standards and Controls

## NIST Standards
- **NIST SP 800-53 Rev 5**:
  - AC-2: Account Management (periodic review requirement)
  - AC-2(3): Disable accounts after inactivity period
  - AC-5: Separation of Duties
  - AC-6: Least Privilege
  - AC-6(7): Review of User Privileges
  - AU-6: Audit Record Review, Analysis, and Reporting
- **NIST SP 800-171**: 3.1.1 Authorized Access Control, 3.1.2 Transaction Control

## Compliance Requirements
- **SOX Section 404**: Quarterly access reviews for financial systems
- **PCI DSS 4.0**: Requirement 7.2.5 - Review all access at least every six months
- **HIPAA Security Rule**: 45 CFR 164.312(a)(1) - Access control review
- **ISO 27001**: A.9.2.5 Review of user access rights
- **GDPR Article 5(1)(f)**: Integrity and confidentiality of processing

## Industry Frameworks
- **CIS Controls v8**: Control 6.2 - Establish an Access Revoking Process
- **COBIT 2019**: DSS05.04 - Manage user identity and logical access
- **IGA Market**: SailPoint, Saviynt, One Identity, Omada

---

## Workflows

## Workflow 1: Quarterly Access Review Campaign

### Timeline:
- Week 1: Data collection and campaign configuration
- Week 2-4: Active review period
- Week 5: Escalation for non-responsive reviewers
- Week 6: Hard close and remediation initiation
- Week 7-8: Remediation execution and verification
- Week 8: Campaign closure and reporting

### Steps:
1. Extract entitlement data from all in-scope systems
2. Correlate with HR data for active/inactive status
3. Calculate risk scores for each user-entitlement pair
4. Assign reviewers based on reviewer model
5. Launch campaign with notifications
6. Monitor completion daily, send reminders at 50% and 75% of timeline
7. Escalate to VP level at deadline for incomplete reviews
8. Force-close with auto-revoke or manager-override at hard deadline
9. Process revocations through ticketing system
10. Verify revocations completed in target systems
11. Generate compliance report and evidence package

## Workflow 2: Triggered Access Review (Role Change)

### Steps:
1. HR system notifies of employee role change (transfer, promotion)
2. System identifies current access vs. new role entitlements
3. Birthright access for new role automatically provisioned
4. Legacy access flagged for new manager review
5. New manager certifies which legacy access to retain/revoke
6. Retained access documented with justification
7. Revoked access removed within SLA

## Workflow 3: Privileged Access Micro-Certification

### Steps:
1. Weekly extraction of privileged entitlements
2. Privileged access grouped by system owner
3. System owner reviews new privileged access grants since last certification
4. Each privileged entitlement requires explicit approval with justification
5. Non-certified privileged access auto-revoked after 48 hours
6. Results forwarded to security team for trending

## Workflow 4: SOD Violation Detection and Resolution

### Steps:
1. Define SOD rule matrix (e.g., AP create vs. AP approve)
2. Scan entitlements against SOD rules
3. Flag violations with risk level
4. Route violations to compliance team
5. Compliance team evaluates: revoke access or approve compensating control
6. If compensating control: document control, set review frequency, assign monitor
7. If revoke: process access removal and verify

---

## Working Template

## Campaign Information
| Field | Value |
|-------|-------|
| Campaign ID | |
| Campaign Name | |
| Review Period | Q_ 20__ |
| Start Date | |
| End Date | |
| Review Model | [ ] Manager [ ] App Owner [ ] Hybrid |
| Auto-Revoke on Non-Response | [ ] Yes [ ] No |

## In-Scope Applications
| Application | Risk Level | Review Frequency | App Owner | Reviewer |
|-------------|------------|------------------|-----------|----------|
| | | | | |

## Timeline
| Milestone | Date | Status |
|-----------|------|--------|
| Data extraction complete | | [ ] |
| Campaign launched | | [ ] |
| First reminder (50%) | | [ ] |
| Second reminder (75%) | | [ ] |
| Escalation to management | | [ ] |
| Hard close deadline | | [ ] |
| Remediation complete | | [ ] |
| Report delivered to audit | | [ ] |

## SOD Rules Matrix
| Rule ID | Conflict Description | App A | Entitlement A | App B | Entitlement B | Severity |
|---------|---------------------|-------|---------------|-------|---------------|----------|
| | | | | | | |

## Campaign Results Summary
| Metric | Value |
|--------|-------|
| Total entitlements reviewed | |
| Completion rate | |
| Approved | |
| Revoked | |
| Exceptions documented | |
| SOD violations found | |
| Stale access identified | |
| Orphaned accounts found | |
