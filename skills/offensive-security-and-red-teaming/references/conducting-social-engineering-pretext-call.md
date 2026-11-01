# Conducting Social Engineering Pretext Call

## API Reference

## Libraries

| Library | Install | Purpose |
|---------|---------|---------|
| requests | `pip install requests` | API integration with tracking platforms |
| twilio | `pip install twilio` | Programmatic phone call management |
| jinja2 | `pip install Jinja2` | Pretext script template rendering |

## Pretext Call Phases

| Phase | Description |
|-------|-------------|
| Reconnaissance | Research target name, role, department, reporting chain |
| Pretext Development | Create believable scenario and script |
| Call Execution | Make the call, follow script, adapt to responses |
| Documentation | Record outcome, information obtained, duration |
| Analysis | Calculate success rates, identify vulnerable departments |

## Success Criteria Categories

| Category | Description |
|----------|-------------|
| Full Success | Target provided credentials, access, or completed action |
| Partial Success | Target revealed organizational info but not credentials |
| Failed | Target refused or became suspicious |
| Reported | Target reported the call to security team |

## Key Metrics

| Metric | Formula |
|--------|---------|
| Success Rate | successful_calls / total_calls x 100 |
| Report Rate | calls_reported_to_security / total_calls x 100 |
| Avg Call Duration | total_duration / total_calls |
| Dept Vulnerability | dept_successes / dept_total x 100 |

## Legal Considerations

| Requirement | Description |
|-------------|-------------|
| Written Authorization | Signed Rules of Engagement from client |
| Recording Consent | Follow state/jurisdiction recording laws |
| Scope Boundaries | Only call authorized targets |
| Data Handling | Securely store any obtained credentials, delete after report |

## External References

- [Social Engineering Framework](https://www.social-engineer.org/framework/)
- [PTES Pre-engagement Guidelines](http://www.pentest-standard.org/)
- [Twilio Voice API](https://www.twilio.com/docs/voice)

---

## Standards and Controls

## MITRE ATT&CK Techniques
- **T1566.004** - Phishing: Voice (Vishing)
- **T1598** - Phishing for Information
- **T1598.003** - Phishing for Information: Spearphishing Voice
- **T1589** - Gather Victim Identity Information
- **T1589.001** - Gather Victim Identity Information: Credentials
- **T1589.002** - Gather Victim Identity Information: Email Addresses
- **T1591** - Gather Victim Org Information
- **T1591.004** - Gather Victim Org Information: Identify Roles
- **T1593** - Search Open Websites/Domains

## NIST References
- **NIST SP 800-50** - Building an IT Security Awareness and Training Program
- **NIST SP 800-53 Rev. 5** - AT-2: Literacy Training and Awareness
- **NIST SP 800-53 Rev. 5** - AT-3: Role-Based Training
- **NIST SP 800-115** - Section 3.3: Social Engineering

## Legal Frameworks
- **Computer Fraud and Abuse Act (CFAA)** - Authorization requirements
- **GDPR Article 6** - Lawful basis for processing (if recording EU citizens)
- **State wiretapping laws** - One-party vs two-party consent states
- **Telecommunications Act** - Caller ID spoofing regulations (47 U.S.C. 227)

## Industry Standards
- **PTES** - Social Engineering section
- **OSSTMM** - Human Security Testing module
- **CREST** - Social Engineering guidelines
- **SE Code of Ethics** - Social engineering testing ethical standards

---

## Workflows

## Vishing Campaign Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│              VISHING CAMPAIGN WORKFLOW                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. AUTHORIZATION & SCOPING                                      │
│     ├── Obtain written authorization                             │
│     ├── Define target list (departments, roles)                  │
│     ├── Define boundaries (no C-suite, no threats)               │
│     ├── Agree on pretext scenarios                               │
│     ├── Confirm call recording legality                          │
│     └── Establish deconfliction process                          │
│                                                                  │
│  2. OSINT RECONNAISSANCE                                         │
│     ├── Employee enumeration (LinkedIn, website)                 │
│     ├── Organizational structure mapping                         │
│     ├── Technology stack identification                          │
│     ├── Internal terminology and process research                │
│     └── Target prioritization                                    │
│                                                                  │
│  3. PRETEXT DEVELOPMENT                                          │
│     ├── Select scenario(s) per target role                       │
│     ├── Draft call scripts with key phrases                      │
│     ├── Prepare objection handling responses                     │
│     ├── Set up caller ID spoofing (authorized)                   │
│     └── Rehearse delivery                                        │
│                                                                  │
│  4. CALL EXECUTION                                               │
│     ├── Execute calls according to schedule                      │
│     ├── Record calls (with legal authorization)                  │
│     ├── Document responses and disclosures                       │
│     ├── Note verification attempts by targets                    │
│     └── Track time-to-disclosure metrics                         │
│                                                                  │
│  5. ANALYSIS & REPORTING                                         │
│     ├── Calculate disclosure rates by department                 │
│     ├── Identify patterns (role, tenure, training)               │
│     ├── Compare against industry benchmarks                      │
│     ├── Generate remediation recommendations                     │
│     └── Present findings to stakeholders                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Pretext Selection Decision Tree

```
Select Pretext Based on Target Role
│
├── IT/Technical Staff
│   ├── Vendor support call (patch emergency)
│   ├── Cloud provider security alert
│   └── Penetration test notification (meta-pretext)
│
├── Finance/Accounting
│   ├── Wire transfer verification (CEO fraud)
│   ├── Vendor payment update
│   └── Audit compliance request
│
├── HR/Recruiting
│   ├── Benefits enrollment verification
│   ├── Background check follow-up
│   └── Payroll system update
│
├── Executive Assistants
│   ├── Executive impersonation (travel issue)
│   ├── Board meeting preparation
│   └── Urgent document request
│
├── General Employees
│   ├── IT Helpdesk (password reset/VPN update)
│   ├── Facilities (badge system update)
│   └── Survey/research call
│
└── Front Desk/Reception
    ├── Delivery/courier pretext
    ├── Visitor registration
    └── Employee directory request
```

---

## Working Template

## Engagement Details

| Field | Value |
|---|---|
| Campaign ID | VISH-YYYY-XXX |
| Client | [Organization] |
| Period | YYYY-MM-DD to YYYY-MM-DD |
| Total Targets | XX employees |
| Pretext(s) Used | [List of pretexts] |
| Assessor | [Name] |

## Executive Summary

[Organization] engaged [Company] to conduct a vishing assessment targeting XX employees across XX departments. The assessment measured employee susceptibility to social engineering pretext calls, specifically testing credential disclosure, verification procedures, and incident reporting behaviors.

## Results Summary

| Metric | Result | Benchmark | Status |
|---|---|---|---|
| Credential Disclosure Rate | XX% | <10% | Pass/Fail |
| Sensitive Info Disclosure Rate | XX% | <20% | Pass/Fail |
| Caller Verification Rate | XX% | >80% | Pass/Fail |
| Security Reporting Rate | XX% | >50% | Pass/Fail |

## Call Log

| # | Target | Dept | Pretext | Cred Disclosed | Verified | Reported |
|---|---|---|---|---|---|---|
| 1 | [Name] | [Dept] | [Pretext] | Yes/No | Yes/No | Yes/No |
| 2 | [Name] | [Dept] | [Pretext] | Yes/No | Yes/No | Yes/No |

## Department Risk Scores

| Department | Targets | Disclosure Rate | Risk Level |
|---|---|---|---|
| Finance | XX | XX% | Critical/High/Medium/Low |
| HR | XX | XX% | Critical/High/Medium/Low |
| IT | XX | XX% | Critical/High/Medium/Low |

## Recommendations

### Immediate (0-30 days)
1. Implement mandatory callback verification for credential requests
2. Issue security bulletin about vishing threats

### Short-Term (30-90 days)
1. Deploy role-based security awareness training
2. Establish easy suspicious-call reporting mechanism
3. Conduct targeted training for high-risk departments

### Long-Term (90+ days)
1. Implement quarterly vishing simulations
2. Integrate vishing metrics into security KPIs
3. Develop department-specific verification procedures
