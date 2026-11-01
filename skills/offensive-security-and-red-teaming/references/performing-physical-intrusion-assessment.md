# Performing Physical Intrusion Assessment

## API Reference

## Libraries Used
- **csv**: Generate and parse assessment checklists
- **pathlib**: File operations

## CLI Interface
```
python agent.py checklist [--categories perimeter access_control server_room social_engineering] [--output checklist.csv]
python agent.py score --csv completed_assessment.csv
python agent.py report --csv completed_assessment.csv
```

## Core Functions

### `generate_checklist(categories, output_file)` — Create assessment template
22 checks across 4 categories with severity ratings. Outputs to CSV.

### `score_assessment(results_csv)` — Calculate compliance score
Groups by category and severity. Identifies critical failures.

### `generate_report(results_csv)` — Executive summary with risk level

## Assessment Categories (22 checks)
| Category | Checks | Focus |
|----------|--------|-------|
| Perimeter Security | 5 | Fencing, CCTV, lighting, barriers |
| Access Control | 6 | Badge access, tailgating, visitor policy |
| Server Room | 6 | MFA, CCTV, environmental, access logs |
| Social Engineering | 5 | Visitor challenge, clean desk, shredding |

## Risk Classification
- **CRITICAL**: Critical control failures found
- **HIGH**: >5 failed checks
- **MEDIUM**: 1-5 failed checks
- **LOW**: All checks passed

## Dependencies
No external packages — Python standard library only.

---

## Standards and Controls

## MITRE ATT&CK Techniques
- **T1200** - Hardware Additions (rogue device deployment)
- **T1091** - Replication Through Removable Media (USB attacks)
- **T1199** - Trusted Relationship (tailgating, impersonation)
- **T1078** - Valid Accounts (cloned badges)
- **T1598** - Phishing for Information (in-person social engineering)

## NIST References
- **NIST SP 800-53 Rev. 5** - PE-1 through PE-20: Physical and Environmental Protection
- **NIST SP 800-53 Rev. 5** - PE-3: Physical Access Control
- **NIST SP 800-53 Rev. 5** - PE-6: Monitoring Physical Access
- **NIST SP 800-116 Rev. 1** - PIV Card credential management
- **NIST SP 800-46** - Remote access security

## Industry Standards
- **ASIS Physical Security Professional (PSP)** guidelines
- **ISO 27001:2022** - A.7: Physical controls
- **PCI DSS 4.0** - Requirement 9: Restrict physical access to cardholder data
- **ISACA Physical Penetration Testing** white paper (2023)
- **CPTED** - Crime Prevention Through Environmental Design

## Compliance Mapping
| Framework | Control | Description |
|---|---|---|
| PCI DSS 4.0 | 9.1-9.5 | Physical access controls |
| SOC 2 | CC6.4 | Physical access restrictions |
| ISO 27001 | A.7.1-7.4 | Physical security perimeters, controls |
| HIPAA | 164.310 | Physical safeguards |
| NIST CSF | PR.AC-2 | Physical access to assets |

---

## Workflows

## Assessment Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│           PHYSICAL INTRUSION ASSESSMENT WORKFLOW                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. RECONNAISSANCE (Day 1-2)                                     │
│     ├── External perimeter survey                                │
│     ├── Entry/exit point mapping                                 │
│     ├── Camera placement analysis                                │
│     ├── Guard patrol timing                                      │
│     ├── Employee behavior observation                            │
│     ├── Badge technology identification                          │
│     └── Loading dock / service entrance survey                   │
│                                                                  │
│  2. BADGE CAPTURE (Day 2-3)                                      │
│     ├── Position near badge readers / elevators                  │
│     ├── Capture RFID data from passing employees                 │
│     ├── Clone to blank cards                                     │
│     └── Test cloned badges on external readers first             │
│                                                                  │
│  3. INTRUSION ATTEMPTS (Day 3-5)                                 │
│     ├── Tailgating through main entrance                         │
│     ├── Badge cloning at restricted doors                        │
│     ├── Lock bypass on server room / network closet              │
│     ├── Social engineering at reception                          │
│     ├── Loading dock / service entrance access                   │
│     └── After-hours access attempts                              │
│                                                                  │
│  4. INTERNAL OBJECTIVES (Day 4-5)                                │
│     ├── Access server room / data center                         │
│     ├── Deploy rogue network device                              │
│     ├── Access unlocked workstations                             │
│     ├── Plug in USB device to exposed port                       │
│     ├── Photograph sensitive documents on desks                  │
│     └── Test dumpster diving                                     │
│                                                                  │
│  5. REPORTING (Day 6-7)                                          │
│     ├── Document all access attempts with evidence               │
│     ├── Map successful paths on facility diagram                 │
│     ├── Provide remediation for each finding                     │
│     └── Present findings to security team                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Entry Point Decision Tree

```
Select Entry Point
│
├── Main Entrance
│   ├── Tailgate during shift change
│   ├── Social engineer past reception
│   └── Use cloned badge at turnstile
│
├── Side/Emergency Doors
│   ├── Check for propped doors
│   ├── Use under-door tool on push-bar
│   └── Badge clone if reader present
│
├── Loading Dock
│   ├── Impersonate delivery driver
│   ├── Follow truck into dock area
│   └── Access internal doors from dock
│
├── Parking Garage
│   ├── Tailgate vehicle through gate
│   ├── Access stairwells to building
│   └── Check for unlocked access doors
│
└── Smoking Area
    ├── Wait for employees on break
    ├── Build rapport during conversation
    └── Follow group back inside
```

---

## Working Template

## Assessment Details

| Field | Value |
|---|---|
| Assessment ID | PHYS-YYYY-XXX |
| Client | [Organization] |
| Facility | [Address] |
| Assessment Dates | YYYY-MM-DD to YYYY-MM-DD |
| Assessor(s) | [Names] |
| Authorization | [RoE document reference] |

## Executive Summary

Physical security testing of [Facility] revealed [X] successful unauthorized entries out of [Y] attempts ([Z]% success rate). Critical findings include [summary of top findings].

## Facility Map

[Insert annotated facility map showing entry points, camera positions, and successful access paths]

## Results Summary

| Metric | Result |
|---|---|
| Total Access Attempts | XX |
| Successful Entries | XX |
| Success Rate | XX% |
| Detection Rate | XX% |
| Challenge Rate | XX% |
| Rogue Devices Deployed | XX |
| Restricted Areas Accessed | XX |

## Findings

### Finding 1: [Title]

| Field | Value |
|---|---|
| Severity | Critical/High/Medium/Low |
| Location | [Specific location] |
| Technique | [Method used] |
| Detected | Yes/No |
| Evidence | [Photo/video reference] |

**Description:** [What was found]
**Impact:** [Potential business impact]
**Remediation:** [Specific fix]

## Recommendations

### Immediate
1. [Critical remediation]

### Short-Term
1. [High-priority improvement]

### Long-Term
1. [Strategic enhancement]
