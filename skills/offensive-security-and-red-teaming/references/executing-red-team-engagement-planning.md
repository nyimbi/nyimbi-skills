# Executing Red Team Engagement Planning

## API Reference

## MITRE ATT&CK Framework

### Tactics (Enterprise)
| ID | Tactic |
|----|--------|
| TA0043 | Reconnaissance |
| TA0042 | Resource Development |
| TA0001 | Initial Access |
| TA0002 | Execution |
| TA0003 | Persistence |
| TA0004 | Privilege Escalation |
| TA0005 | Defense Evasion |
| TA0006 | Credential Access |
| TA0007 | Discovery |
| TA0008 | Lateral Movement |
| TA0009 | Collection |
| TA0011 | Command and Control |
| TA0010 | Exfiltration |
| TA0040 | Impact |

### ATT&CK Navigator API
```http
GET https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json
```

## Red Team Tools API References

### Cobalt Strike — Teamserver
```
./teamserver <IP> <password> <malleable_c2_profile>
```

### GoPhish — Campaign API
```http
POST https://gophish-server:3333/api/campaigns/
Authorization: Bearer {api_key}

{
  "name": "Spearphishing Test",
  "template": {"name": "IT Support"},
  "url": "https://phish.example.com",
  "smtp": {"name": "smtp_config"},
  "groups": [{"name": "Target Group"}]
}
```

### BloodHound — Data Collection
```bash
# SharpHound collection
SharpHound.exe -c All --domain corp.local
# or via Python
bloodhound-python -d corp.local -u user -p pass -c all
```

## Engagement Plan Structure

### Key Sections
| Section | Content |
|---------|---------|
| Scope | IP ranges, domains, systems in/out |
| Rules of Engagement | Authorization, boundaries |
| Objectives | Goals mapped to business risk |
| Scenarios | Attack paths and techniques |
| Timeline | Phases with milestones |
| Communication | Deconfliction, reporting |
| Data Handling | Encryption, retention, destruction |

## PTES (Penetration Testing Execution Standard)

### Phases
1. Pre-engagement Interactions
2. Intelligence Gathering
3. Threat Modeling
4. Vulnerability Analysis
5. Exploitation
6. Post-Exploitation
7. Reporting

## Report Template Fields

| Field | Description |
|-------|-------------|
| Executive Summary | Business impact overview |
| Scope & Methodology | What was tested and how |
| Findings | Vulnerabilities with CVSS scores |
| Attack Narrative | Timeline of red team actions |
| Detection Gaps | What blue team missed |
| Recommendations | Prioritized remediation |

---

## Standards and Controls

## MITRE ATT&CK

- **Reconnaissance (TA0043)**: Pre-engagement intelligence gathering
  - T1595 - Active Scanning
  - T1592 - Gather Victim Host Information
  - T1589 - Gather Victim Identity Information
  - T1590 - Gather Victim Network Information
  - T1591 - Gather Victim Org Information
- **Resource Development (TA0042)**: Infrastructure and capability preparation
  - T1583 - Acquire Infrastructure
  - T1584 - Compromise Infrastructure
  - T1587 - Develop Capabilities
  - T1588 - Obtain Capabilities
  - T1608 - Stage Capabilities

## PTES (Penetration Testing Execution Standard)

### Pre-engagement Interactions
- Scope definition and boundaries
- Goals and objectives
- Rules of engagement
- Communication plan
- Emergency contacts
- Timeline and milestones
- Legal considerations
- Authorization documentation

### Intelligence Gathering
- OSINT requirements
- Threat actor identification
- Attack surface mapping
- Technology profiling

## OSSTMM (Open Source Security Testing Methodology Manual)

### Section 3: Rules of Engagement
- Test boundaries and limitations
- Test vectors classification
- Compliance requirements
- Reporting standards

### Section 4: Scope
- Physical security scope
- Wireless scope
- Telecommunications scope
- Data networks scope
- Social engineering scope

## NIST SP 800-115

### Technical Guide to Information Security Testing and Assessment
- Section 3: Review Techniques
- Section 4: Target Identification and Analysis
- Section 5: Target Vulnerability Validation
- Section 6: Security Assessment Planning

## CBEST Framework (Bank of England)

- Threat intelligence-led penetration testing
- Threat actor profile development
- Scenario-based adversary simulation
- Control validation and assessment

## TIBER-EU Framework

- European framework for threat intelligence-based ethical red teaming
- Phase 1: Generic Threat Landscape
- Phase 2: Threat Intelligence
- Phase 3: Red Team Testing
- Phase 4: Closure

## CREST STAR (Simulated Targeted Attack and Response)

- Intelligence-led red team testing standard
- Adversary simulation methodology
- Detection and response validation
- Structured reporting format

## Relevant CVE/CWE References

Not directly applicable for planning phase - CVE/CWE references will be mapped during the attack execution phase based on selected TTPs and target environment.

## Compliance Frameworks Impacting Scope

| Framework | Impact on Red Team Scope |
|-----------|--------------------------|
| PCI DSS | Cardholder data environment must be tested |
| HIPAA | PHI handling requires special data protections |
| SOX | Financial systems require specific authorization |
| GDPR | Personal data handling restrictions apply |
| CMMC | DoD contractor supply chain considerations |

---

## Workflows

## Workflow 1: Scoping and Threat Modeling

### Step 1: Stakeholder Meeting
```
1. Schedule kickoff with CISO, CTO, legal counsel, and engagement sponsor
2. Present red team capabilities and engagement type options
3. Discuss organizational threat landscape and prior incidents
4. Identify crown jewels (DC, financial systems, PII stores, IP repositories)
5. Agree on engagement type: Full-scope / Assumed Breach / Objective-based
6. Document initial scope boundaries
```

### Step 2: Threat Intelligence Review
```
1. Pull industry-specific threat reports (Mandiant M-Trends, CrowdStrike Global Threat Report)
2. Query MITRE ATT&CK for relevant threat groups:
   - Financial: FIN7, FIN12, Carbanak
   - Healthcare: APT41, Lazarus
   - Government: APT29, APT28, Turla
   - Technology: APT10, Hafnium
3. Map threat actor TTPs to ATT&CK Navigator
4. Export ATT&CK Navigator layer as JSON for engagement tracking
5. Identify top 10-15 techniques for emulation
```

### Step 3: Attack Surface Analysis
```
1. Review external attack surface using passive reconnaissance
2. Map network topology from provided documentation
3. Identify remote access points (VPN, RDP, Citrix)
4. Catalog cloud services (AWS, Azure, GCP, SaaS)
5. Review physical locations and access controls
6. Identify human targets for social engineering vectors
```

## Workflow 2: Rules of Engagement Development

### Step 1: Draft ROE Document
```
Sections to include:
1. Executive Summary
2. Engagement Objectives
3. Scope Definition
   - In-scope IP ranges/domains
   - In-scope physical locations
   - In-scope personnel (for social engineering)
   - Out-of-scope systems (production DBs, medical devices, SCADA)
4. Authorized Techniques
   - Approved MITRE ATT&CK techniques
   - Prohibited techniques (e.g., DoS, data destruction)
5. Communication Plan
   - Primary POC: Name, phone, email
   - Secondary POC: Name, phone, email
   - Daily check-in schedule
   - Encrypted communication channel details
6. Emergency Procedures
   - Stop code word: [DEFINED]
   - Escalation matrix
   - Incident response coordination
7. Legal Authorization
   - Get-out-of-jail letter template
   - Signed authorization from executive sponsor
8. Data Handling
   - Sensitive data discovery procedures
   - Data retention and destruction policy
9. Timeline
   - Start date, end date
   - Blackout periods
   - Reporting deadline
```

### Step 2: Legal Review
```
1. Submit ROE to organization's legal counsel
2. Review liability and indemnification clauses
3. Ensure compliance with local laws (CFAA, Computer Misuse Act, etc.)
4. Verify insurance coverage for testing activities
5. Obtain signed legal authorization
```

### Step 3: Distribution and Acknowledgment
```
1. Distribute finalized ROE to all red team operators
2. Require written acknowledgment from each operator
3. Provide emergency contact cards to each operator
4. Brief operators on scope restrictions and prohibited actions
5. Archive signed copies in secure document management system
```

## Workflow 3: Operational Planning

### Step 1: Infrastructure Planning
```
1. Identify C2 framework requirements (Cobalt Strike, Sliver, Mythic)
2. Plan redirector architecture:
   - HTTPS redirectors for web traffic
   - DNS redirectors for DNS tunneling
   - SMTP redirectors for phishing
3. Register domains that match target organization's naming patterns
4. Obtain SSL certificates for phishing and C2 domains
5. Configure domain categorization for web filtering bypass
6. Set up VPN/jump boxes for operator access
```

### Step 2: Phased Attack Plan
```
Phase 1: Reconnaissance (Days 1-3)
- OSINT collection on target organization
- External attack surface enumeration
- Social media profiling of target personnel
- Technology stack identification

Phase 2: Initial Access (Days 4-7)
- Spearphishing campaign delivery
- External service exploitation attempts
- Physical access attempts (if in scope)
- Supply chain attack vectors

Phase 3: Establish Persistence (Days 8-10)
- Deploy persistent implants
- Establish backup C2 channels
- Create local admin accounts
- Install backdoor services

Phase 4: Lateral Movement (Days 11-15)
- Internal network enumeration
- Credential harvesting
- Privilege escalation
- Domain controller targeting

Phase 5: Objective Completion (Days 16-18)
- Access crown jewels
- Demonstrate data exfiltration capability
- Document evidence of access
- Capture screenshots and proof

Phase 6: Cleanup and Reporting (Days 19-20)
- Remove all implants and persistence mechanisms
- Delete created accounts
- Restore modified configurations
- Compile evidence and findings
```

### Step 3: Deconfliction Planning
```
1. Establish deconfliction channel with SOC (separate from normal SOC comms)
2. Define red team IP addresses for SOC whitelisting (trusted agent model only)
3. Create deconfliction log template for real-time tracking
4. Schedule daily deconfliction calls during engagement
5. Define escalation criteria for when SOC must be notified
6. Agree on evidence preservation procedures if real incident overlaps
```

## Workflow 4: Engagement Execution Tracking

### Step 1: Daily Operations
```
1. Morning briefing with red team operators
2. Review previous day's activities and findings
3. Assign daily objectives aligned to attack plan
4. Execute assigned techniques with OPSEC considerations
5. Document all activities in engagement log with timestamps
6. Evening debrief and progress assessment
7. Update attack graph with new access and findings
```

### Step 2: Decision Points
```
Go/No-Go criteria for each phase transition:
- Phase 1 → 2: Sufficient reconnaissance data collected
- Phase 2 → 3: Initial access achieved, no detection alerts
- Phase 3 → 4: Persistence established, C2 communications stable
- Phase 4 → 5: Sufficient privileges and network access obtained
- Phase 5 → 6: Objectives achieved or engagement time expired
```

### Step 3: Metrics Collection
```
Track throughout engagement:
- Time to Initial Access (TTIA)
- Time to Domain Admin (TTDA)
- Time to Objective (TTO)
- Number of detections triggered
- Mean Time to Detect (MTTD) for blue team
- Techniques executed vs. detected ratio
- Number of unique hosts compromised
- Credentials harvested count
```

---

## Working Template

## Document Control

| Field | Value |
|-------|-------|
| Document Title | Red Team Engagement Plan |
| Organization | [ORGANIZATION NAME] |
| Version | 1.0 |
| Classification | CONFIDENTIAL |
| Author | [RED TEAM LEAD] |
| Date Created | [DATE] |
| Last Modified | [DATE] |
| Engagement ID | RT-[ORG]-[YYYYMMDD] |

---

## 1. Engagement Overview

### 1.1 Purpose
[Describe the purpose of this red team engagement and the business drivers behind it]

### 1.2 Engagement Type
- [ ] Full Scope Red Team
- [ ] Assumed Breach
- [ ] Objective-Based
- [ ] Purple Team Collaborative

### 1.3 Key Stakeholders

| Role | Name | Department | Contact |
|------|------|------------|---------|
| Executive Sponsor | | | |
| Technical POC | | | |
| Legal Counsel | | | |
| SOC Manager | | | |
| Red Team Lead | | | |

---

## 2. Scope Definition

### 2.1 In-Scope Assets

#### Network Ranges
| CIDR Range | Description | Location |
|-----------|-------------|----------|
| | | |

#### Domains
| Domain | Description | Type |
|--------|-------------|------|
| | | External/Internal |

#### Cloud Environments
| Provider | Account/Subscription | Services |
|----------|---------------------|----------|
| | | |

#### Physical Locations
| Address | Building/Floor | Access Type |
|---------|---------------|-------------|
| | | |

### 2.2 Out-of-Scope

| Asset | Reason | Alternative |
|-------|--------|------------|
| | | |

### 2.3 Restrictions
- [ ] No Denial of Service
- [ ] No data destruction
- [ ] No production database access
- [ ] No social engineering of executives
- [ ] Custom: [SPECIFY]

---

## 3. Threat Profile

### 3.1 Selected Threat Actor
**Primary:** [THREAT ACTOR NAME]
**Aliases:** [LIST]
**Motivation:** [Financial/Espionage/Disruption]

### 3.2 Mapped MITRE ATT&CK Techniques

| Tactic | Technique ID | Technique Name | Priority |
|--------|-------------|----------------|----------|
| Initial Access | | | High/Medium/Low |
| Execution | | | |
| Persistence | | | |
| Privilege Escalation | | | |
| Defense Evasion | | | |
| Credential Access | | | |
| Discovery | | | |
| Lateral Movement | | | |
| Collection | | | |
| Exfiltration | | | |
| Command and Control | | | |

### 3.3 ATT&CK Navigator Layer
[Attach exported JSON layer file]

---

## 4. Attack Plan

### Phase 1: Reconnaissance
**Duration:** [X days]
**Objective:** [DESCRIBE]

| Activity | Tool/Method | Expected Outcome | Risk Level |
|----------|------------|-------------------|------------|
| | | | |

### Phase 2: Initial Access
**Duration:** [X days]
**Objective:** [DESCRIBE]

| Activity | Tool/Method | Expected Outcome | Risk Level |
|----------|------------|-------------------|------------|
| | | | |

### Phase 3: Establish Persistence
**Duration:** [X days]
**Objective:** [DESCRIBE]

| Activity | Tool/Method | Expected Outcome | Risk Level |
|----------|------------|-------------------|------------|
| | | | |

### Phase 4: Lateral Movement
**Duration:** [X days]
**Objective:** [DESCRIBE]

| Activity | Tool/Method | Expected Outcome | Risk Level |
|----------|------------|-------------------|------------|
| | | | |

### Phase 5: Privilege Escalation
**Duration:** [X days]
**Objective:** [DESCRIBE]

| Activity | Tool/Method | Expected Outcome | Risk Level |
|----------|------------|-------------------|------------|
| | | | |

### Phase 6: Objective Completion
**Duration:** [X days]
**Objective:** [DESCRIBE]

| Activity | Tool/Method | Expected Outcome | Risk Level |
|----------|------------|-------------------|------------|
| | | | |

### Phase 7: Cleanup and Reporting
**Duration:** [X days]
**Objective:** [DESCRIBE]

| Activity | Tool/Method | Expected Outcome | Risk Level |
|----------|------------|-------------------|------------|
| | | | |

---

## 5. Infrastructure Requirements

### 5.1 C2 Infrastructure
| Component | Provider | Domain/IP | Purpose |
|-----------|---------|-----------|---------|
| C2 Server | | | Primary command and control |
| Redirector | | | Traffic redirection |
| Phishing Server | | | Email delivery |
| Payload Host | | | Stage delivery |

### 5.2 Operator Equipment
| Item | Specification | Assigned To |
|------|-------------|-------------|
| Laptop | | |
| USB Devices | | |
| WiFi Adapter | | |
| Lock Pick Set | | |

---

## 6. Communication Plan

### 6.1 Channels
- **Primary:** [METHOD]
- **Secondary:** [METHOD]
- **Emergency:** [METHOD]

### 6.2 Check-in Schedule
| Frequency | Method | Participants | Time |
|-----------|--------|-------------|------|
| Daily | | | |
| Weekly | | | |

### 6.3 Emergency Stop Procedure
- **Code Word:** [WORD]
- **Activation Method:** [DESCRIBE]
- **Response Time:** [X minutes]

---

## 7. Legal Authorization

### 7.1 Authorization Statement
I hereby authorize [RED TEAM COMPANY/TEAM] to conduct the red team engagement
as described in this document against [ORGANIZATION NAME] assets.

**Signature:** ___________________________
**Name:** ___________________________
**Title:** ___________________________
**Date:** ___________________________

### 7.2 Attached Documents
- [ ] Signed Rules of Engagement
- [ ] Master Services Agreement
- [ ] Non-Disclosure Agreement
- [ ] Get-Out-of-Jail Letters (physical testing)
- [ ] Insurance Certificate

---

## 8. Reporting

### 8.1 Deliverables
| Deliverable | Due Date | Format | Recipients |
|------------|----------|--------|------------|
| Daily Status Update | Daily | Email | Technical POC |
| Interim Report | Mid-engagement | PDF | Sponsor, CISO |
| Final Report | [DATE] | PDF | Full distribution |
| Executive Summary | [DATE] | PDF/PPT | Executive team |
| Technical Debrief | [DATE] | Presentation | Security team |

### 8.2 Report Sections
1. Executive Summary
2. Engagement Overview and Scope
3. Methodology
4. Attack Narrative (Timeline)
5. Findings and Observations
6. Risk Ratings and Impact Assessment
7. Recommendations
8. Appendices (Evidence, Tool List, IOCs)

---

## Appendix A: Engagement Checklist

### Pre-Engagement
- [ ] Scope defined and approved
- [ ] ROE signed by all parties
- [ ] Legal authorization obtained
- [ ] Insurance verified
- [ ] Infrastructure deployed and tested
- [ ] Operators briefed on ROE
- [ ] Emergency contacts distributed
- [ ] Deconfliction channel established
- [ ] Threat profile selected and mapped

### During Engagement
- [ ] Daily check-ins conducted
- [ ] Activity log maintained
- [ ] Evidence collected and secured
- [ ] Deconfliction matrix updated
- [ ] Phase transition approvals obtained

### Post-Engagement
- [ ] All implants and persistence removed
- [ ] Created accounts deleted
- [ ] Modified configurations restored
- [ ] Final report delivered
- [ ] Technical debrief completed
- [ ] Lessons learned session conducted
- [ ] Evidence securely archived
- [ ] Infrastructure decommissioned
