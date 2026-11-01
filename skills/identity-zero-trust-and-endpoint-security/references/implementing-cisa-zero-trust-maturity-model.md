# Implementing Cisa Zero Trust Maturity Model

## API Reference

## Dependencies

| Library | Version | Purpose |
|---------|---------|---------|
| (stdlib only) | Python 3.8+ | JSON processing, assessment logic |

## CLI Usage

```bash
python scripts/agent.py \
  --data /assessments/zt_responses.json \
  --output-dir /reports/ \
  --output ztmm_report.json
```

## Functions

### `assess_control(control, implemented, maturity) -> dict`
Scores a single control: 0 (Traditional) to 3 (Optimal).

### `assess_pillar(pillar, responses) -> dict`
Evaluates all controls within a CISA ZT pillar. Returns score, percentage, and maturity level.

### `compute_overall_maturity(pillar_results) -> dict`
Aggregates pillar scores into overall maturity: Traditional/Initial/Advanced/Optimal.

### `generate_recommendations(pillar_results) -> list`
Identifies unimplemented controls, prioritizes by pillar weakness.

### `generate_report(data_path) -> dict`
Full assessment pipeline: load data, assess 5 pillars, compute maturity, generate recommendations.

## CISA ZT Pillars

| Pillar | Controls Assessed |
|--------|-------------------|
| Identity | MFA, phishing-resistant MFA, JIT access, PAM |
| Devices | Inventory, EDR, health attestation, posture |
| Networks | Microsegmentation, encrypted DNS, SDP |
| Applications | Inventory, access controls, API security |
| Data | Classification, DLP, encryption at rest |

## Input Data Format

```json
{
  "Identity": {
    "MFA enforced for all users": {"implemented": true, "maturity": "Advanced"},
    "Phishing-resistant MFA (FIDO2/PIV)": {"implemented": false, "maturity": "Traditional"}
  }
}
```

## Output Schema

```json
{
  "overall_maturity": {"percentage": 52.3, "maturity_level": "Advanced"},
  "pillars": [{"pillar": "Identity", "percentage": 66.7, "maturity_level": "Advanced"}],
  "recommendations": [{"pillar": "Devices", "control": "EDR deployed", "priority": "HIGH"}]
}
```

---

## Standards and Controls

## Primary Standards

### CISA Zero Trust Maturity Model v2.0 (April 2023)
- **Source**: Cybersecurity and Infrastructure Security Agency
- **Scope**: Federal agencies and organizations implementing zero trust
- **Five Pillars**: Identity, Devices, Networks, Applications & Workloads, Data
- **Four Maturity Stages**: Traditional, Initial, Advanced, Optimal
- **Cross-Cutting**: Visibility & Analytics, Automation & Orchestration, Governance

### NIST SP 800-207: Zero Trust Architecture
- **Published**: August 2020
- **Tenets**: Never trust, always verify; assume breach; least privilege access
- **Deployment Models**: Device agent/gateway, enclave, resource portal
- **Key Requirement**: Policy decision point (PDP) and policy enforcement point (PEP)

### Executive Order 14028: Improving the Nation's Cybersecurity
- **Signed**: May 12, 2021
- **Mandate**: Federal agencies must adopt zero trust architecture
- **Timeline**: Agencies required to develop zero trust implementation plans

### OMB Memorandum M-22-09: Federal Zero Trust Strategy
- **Published**: January 2022
- **Requirements per pillar**:
  - Identity: Phishing-resistant MFA for all staff
  - Devices: EDR deployed across federal endpoints
  - Networks: DNS traffic encrypted, HTTP traffic encrypted
  - Applications: Application security testing in CI/CD
  - Data: Data categorization and automated classification

## Supporting Standards

### NSA Zero Trust Pillar Guidance Series (2024)
- User Pillar (February 2024)
- Device Pillar (March 2024)
- Data Pillar (April 2024)
- Application & Workload Pillar (April 2024)
- Network & Environment Pillar (May 2024)
- Visibility & Analytics Pillar (May 2024)
- Automation & Orchestration Pillar (June 2024)

### DISA Zero Trust Reference Architecture
- Department of Defense specific implementation
- Aligns with NIST 800-207 and CISA ZTMM
- Covers DoD-specific compliance requirements

### FedRAMP Zero Trust Requirements
- Cloud service providers must support zero trust
- Continuous monitoring requirements
- Identity federation standards

---

## Workflows

## Workflow 1: Initial Maturity Assessment

```
Step 1: Establish Assessment Team
  - Identify stakeholders from IT, security, compliance, and business units
  - Assign pillar owners for each of the five ZTMM pillars
  - Define assessment timeline and reporting cadence

Step 2: Inventory Current Capabilities
  - Identity: Catalog authentication methods, identity providers, MFA coverage
  - Devices: Enumerate all endpoints, document endpoint security tools
  - Networks: Map network architecture, segmentation, encryption status
  - Applications: List all applications, classify access controls
  - Data: Identify data repositories, classification, DLP status

Step 3: Map to ZTMM Stages
  - For each pillar, evaluate each function against the four maturity stages
  - Document evidence for current stage determination
  - Identify gaps between current and target maturity
  - Rate cross-cutting capabilities (visibility, automation, governance)

Step 4: Produce Assessment Report
  - Pillar-by-pillar maturity scores
  - Gap analysis with prioritized recommendations
  - Quick wins vs. long-term transformation items
  - Resource requirements and estimated timelines
```

## Workflow 2: Identity Pillar Advancement (Traditional to Advanced)

```
Phase A: MFA Deployment
  1. Inventory all user accounts (privileged, standard, service)
  2. Select phishing-resistant MFA solution (FIDO2/WebAuthn)
  3. Deploy MFA for privileged accounts first
  4. Extend MFA to all user accounts
  5. Implement MFA for service accounts and APIs
  6. Configure conditional access policies

Phase B: Identity Governance
  1. Implement identity lifecycle management
  2. Connect IAM to HR system for automated provisioning
  3. Establish access certification reviews
  4. Deploy identity threat detection
  5. Implement just-in-time access for elevated privileges

Phase C: Continuous Verification
  1. Integrate identity signals into access decisions
  2. Deploy risk-based authentication
  3. Implement session-level re-authentication for sensitive actions
  4. Enable behavioral analytics for identity anomalies
```

## Workflow 3: Cross-Pillar Integration

```
Step 1: Establish Unified Policy Engine
  - Define access policies that incorporate all five pillars
  - Implement Policy Decision Point (PDP) per NIST 800-207
  - Deploy Policy Enforcement Points (PEP) at all access boundaries

Step 2: Integrate Signal Sources
  - Identity signals -> trust score component
  - Device posture -> trust score component
  - Network context -> trust score component
  - Application risk -> trust score component
  - Data sensitivity -> access control component

Step 3: Implement Continuous Evaluation
  - Real-time trust scoring engine
  - Dynamic policy adjustment based on risk
  - Automated access revocation on policy violation
  - Audit logging for all access decisions

Step 4: Measure and Report
  - Track maturity progression per pillar quarterly
  - Report to leadership with ZTMM scorecard
  - Adjust roadmap based on threat landscape changes
  - Document lessons learned for continuous improvement
```

## Workflow 4: Governance and Compliance Reporting

```
Step 1: Establish Zero Trust Governance Board
  - Executive sponsor, CISO, pillar owners, compliance
  - Monthly review of zero trust maturity progress
  - Annual strategic review and roadmap adjustment

Step 2: Continuous Compliance Monitoring
  - Map ZTMM controls to OMB M-22-09 requirements
  - Automate evidence collection for each pillar
  - Generate compliance dashboards
  - Prepare for FISMA and other audit requirements

Step 3: Reporting to CISA
  - Submit agency zero trust implementation plan
  - Provide quarterly progress updates
  - Document deviations and remediation plans
```

---

## Working Template

## Organization Information
- **Organization Name**: _______________
- **Assessment Date**: _______________
- **Assessment Lead**: _______________
- **Pillar Owners**:
  - Identity: _______________
  - Devices: _______________
  - Networks: _______________
  - Applications: _______________
  - Data: _______________

## Pillar Assessment Worksheet

### Identity Pillar

| Function | Traditional | Initial | Advanced | Optimal | Current | Evidence |
|---|---|---|---|---|---|---|
| Authentication | [ ] | [ ] | [ ] | [ ] | ___ | |
| Identity Stores | [ ] | [ ] | [ ] | [ ] | ___ | |
| Risk Assessment | [ ] | [ ] | [ ] | [ ] | ___ | |
| Access Management | [ ] | [ ] | [ ] | [ ] | ___ | |
| Identity Lifecycle | [ ] | [ ] | [ ] | [ ] | ___ | |
| Visibility & Analytics | [ ] | [ ] | [ ] | [ ] | ___ | |
| Automation & Orchestration | [ ] | [ ] | [ ] | [ ] | ___ | |
| Governance | [ ] | [ ] | [ ] | [ ] | ___ | |

### Devices Pillar

| Function | Traditional | Initial | Advanced | Optimal | Current | Evidence |
|---|---|---|---|---|---|---|
| Policy Enforcement | [ ] | [ ] | [ ] | [ ] | ___ | |
| Asset Management | [ ] | [ ] | [ ] | [ ] | ___ | |
| Device Compliance | [ ] | [ ] | [ ] | [ ] | ___ | |
| Device Threat Protection | [ ] | [ ] | [ ] | [ ] | ___ | |
| Visibility & Analytics | [ ] | [ ] | [ ] | [ ] | ___ | |
| Automation & Orchestration | [ ] | [ ] | [ ] | [ ] | ___ | |
| Governance | [ ] | [ ] | [ ] | [ ] | ___ | |

### Networks Pillar

| Function | Traditional | Initial | Advanced | Optimal | Current | Evidence |
|---|---|---|---|---|---|---|
| Network Segmentation | [ ] | [ ] | [ ] | [ ] | ___ | |
| Threat Protection | [ ] | [ ] | [ ] | [ ] | ___ | |
| Encryption | [ ] | [ ] | [ ] | [ ] | ___ | |
| Network Resilience | [ ] | [ ] | [ ] | [ ] | ___ | |
| Visibility & Analytics | [ ] | [ ] | [ ] | [ ] | ___ | |
| Automation & Orchestration | [ ] | [ ] | [ ] | [ ] | ___ | |
| Governance | [ ] | [ ] | [ ] | [ ] | ___ | |

### Applications & Workloads Pillar

| Function | Traditional | Initial | Advanced | Optimal | Current | Evidence |
|---|---|---|---|---|---|---|
| Access Authorization | [ ] | [ ] | [ ] | [ ] | ___ | |
| Threat Protection | [ ] | [ ] | [ ] | [ ] | ___ | |
| Accessibility | [ ] | [ ] | [ ] | [ ] | ___ | |
| Application Security | [ ] | [ ] | [ ] | [ ] | ___ | |
| Visibility & Analytics | [ ] | [ ] | [ ] | [ ] | ___ | |
| Automation & Orchestration | [ ] | [ ] | [ ] | [ ] | ___ | |
| Governance | [ ] | [ ] | [ ] | [ ] | ___ | |

### Data Pillar

| Function | Traditional | Initial | Advanced | Optimal | Current | Evidence |
|---|---|---|---|---|---|---|
| Data Inventory | [ ] | [ ] | [ ] | [ ] | ___ | |
| Data Categorization | [ ] | [ ] | [ ] | [ ] | ___ | |
| Data Availability | [ ] | [ ] | [ ] | [ ] | ___ | |
| Data Access | [ ] | [ ] | [ ] | [ ] | ___ | |
| Data Encryption | [ ] | [ ] | [ ] | [ ] | ___ | |
| Visibility & Analytics | [ ] | [ ] | [ ] | [ ] | ___ | |
| Automation & Orchestration | [ ] | [ ] | [ ] | [ ] | ___ | |
| Governance | [ ] | [ ] | [ ] | [ ] | ___ | |

## Gap Analysis Summary

| Pillar | Current Stage | Target Stage | Gap | Priority |
|---|---|---|---|---|
| Identity | ___ | Advanced | ___ | ___ |
| Devices | ___ | Advanced | ___ | ___ |
| Networks | ___ | Advanced | ___ | ___ |
| Applications | ___ | Advanced | ___ | ___ |
| Data | ___ | Advanced | ___ | ___ |

## OMB M-22-09 Compliance Checklist

- [ ] Phishing-resistant MFA deployed for all agency staff
- [ ] Complete device inventory with EDR coverage
- [ ] DNS and HTTP traffic encrypted
- [ ] Applications treated as internet-connected with regular testing
- [ ] Data categorization and automated discovery implemented

## Roadmap Priorities

### Quick Wins (0-3 months)
1. _______________
2. _______________
3. _______________

### Short-term (3-6 months)
1. _______________
2. _______________
3. _______________

### Medium-term (6-12 months)
1. _______________
2. _______________
3. _______________

### Long-term (12-24 months)
1. _______________
2. _______________
3. _______________
