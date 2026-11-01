# Performing Ransomware Tabletop Exercise

## API Reference

## Scenario Framework

### Phase Structure
Each phase contains:

| Field | Type | Description |
|-------|------|-------------|
| `phase` | string | Phase name: detection, containment, escalation, eradication, recovery |
| `inject` | string | Narrative scenario inject read to participants |
| `expected_actions` | list | Correct response actions for scoring |
| `time_pressure_minutes` | int | Simulated time window for decisions |

### Exercise Variants

- **standard** - Normal time pressure, full scenario
- **accelerated** - Half time windows, tests rapid decision-making

## Scoring Algorithm

```
phase_score = (correct_actions / expected_actions) * 100
overall_score = mean(all_phase_scores)
```

Rating thresholds:
- >= 90%: Excellent
- >= 70%: Good
- >= 50%: Needs Improvement
- < 50%: Critical Gaps

## Expected Actions by Phase

### Detection
- `isolate_host` - Quarantine affected endpoint
- `preserve_evidence` - Capture memory dump and disk image
- `notify_ir_lead` - Escalate to incident response lead

### Containment
- `network_segmentation` - Restrict lateral movement paths
- `disable_compromised_accounts` - Lock affected credentials
- `block_c2_domains` - Update firewall/proxy deny lists
- `preserve_shadow_copies` - Protect backup snapshots

### Escalation
- `notify_executive_team` - Brief C-suite leadership
- `engage_legal_counsel` - Activate legal response team
- `contact_law_enforcement` - Report to FBI IC3 or local CIRT
- `activate_crisis_comms` - Prepare stakeholder communications

### Eradication
- `remove_persistence` - Clean scheduled tasks, registry keys, WMI subscriptions
- `reset_all_credentials` - Reset passwords domain-wide
- `rebuild_compromised_hosts` - Reimage from gold images
- `reset_krbtgt_twice` - Invalidate all Kerberos tickets

### Recovery
- `restore_from_backup` - Use verified clean backup sets
- `validate_restored_systems` - Run integrity checks
- `monitor_for_reinfection` - Enhanced monitoring for 72+ hours
- `staged_network_reconnection` - Reconnect systems in phases

## After-Action Report Schema

```json
{
  "report": "ransomware_tabletop_aar",
  "evaluation": {
    "overall_score_pct": 78.5,
    "rating": "good",
    "phase_scores": [{"phase": "detection", "score_pct": 66.7}]
  },
  "recommendations": [{"phase": "detection", "gap": "Missed: preserve_evidence"}]
}
```

## CLI Usage

```bash
python agent.py --mode demo --output aar.json
python agent.py --mode generate --variant accelerated --output scenario.json
python agent.py --mode score --responses-file responses.json --output aar.json
```

---

## Standards and Controls

## Exercise Standards

### FEMA HSEEP (Homeland Security Exercise and Evaluation Program)
- Standardized methodology for exercise design, conduct, and evaluation
- Defines exercise types: seminars, workshops, tabletops, drills, functional, full-scale
- Provides templates for exercise plans, evaluation guides, and AARs
- https://www.fema.gov/emergency-managers/national-preparedness/exercises/hseep

### NIST SP 800-84: Guide to Test, Training, and Exercise Programs
- Framework for developing IT plan test and exercise programs
- Section 4.3: Tabletop exercises for incident response testing
- Covers exercise scoping, objectives, scenario development, and evaluation

### CISA Tabletop Exercise Packages (CTEPs)
- Free downloadable exercise scenarios for critical infrastructure sectors
- Ransomware-specific scenarios updated to reflect current threat landscape
- https://www.cisa.gov/resources-tools/services/cisa-tabletop-exercise-packages

## Ransomware-Specific Guidance

### CISA #StopRansomware Guide
- Ransomware response checklist that exercises should validate
- Decision tree for ransom payment considerations
- Recovery priority guidance

### NIST IR 8374: Ransomware Risk Management
- Identifies exercise testing as a key control in the Recover function
- Recommends annual tabletop exercises with escalating complexity

### FBI/CISA Joint Advisories
- AA24-131A: Black Basta Ransomware
- AA23-136A: BianLian Ransomware Group
- AA23-158A: CL0P Ransomware Gang Exploiting MOVEit
- Use these as source material for realistic exercise scenarios

## Regulatory Notification Requirements (for Scenario Design)

| Regulation | Notification Timeline | Authority |
|-----------|----------------------|-----------|
| GDPR (EU) | 72 hours | Supervisory Authority |
| HIPAA (US Healthcare) | 60 days (individuals), ASAP (HHS if >500) | HHS OCR |
| SEC (US Public Companies) | 4 business days (Form 8-K) | SEC |
| PCI DSS | 72 hours | Card brands/acquiring bank |
| NY DFS (23 NYCRR 500) | 72 hours | NY DFS |
| CCPA (California) | "Expedient time" | California AG |
| NIS2 (EU) | 24 hours (early warning), 72 hours (full) | National CSIRT |

---

## Workflows

## Workflow 1: Exercise Planning (4-6 weeks before)

```
Start
  |
  v
[Define exercise objectives] --> What gaps are we testing?
  |
  v
[Select scenario type]
  |-- Double extortion (data theft + encryption)
  |-- Supply chain ransomware (vendor compromise)
  |-- Cloud ransomware (SaaS/IaaS targeted)
  |-- Critical infrastructure disruption
  |
  v
[Choose threat actor model] --> LockBit / ALPHV / Cl0p / Rhysida
  |
  v
[Identify participants]
  |-- Executive leadership (CEO, CFO, COO)
  |-- IT/Security (CISO, SOC, IR team)
  |-- Legal (General Counsel, external counsel)
  |-- Communications (PR, media relations)
  |-- Operations (business unit leaders)
  |-- HR (employee communications)
  |-- External partners (IR firm, insurance)
  |
  v
[Develop scenario with 4 phases and injects]
  |
  v
[Prepare materials: SITREPs, inject cards, evaluation scorecard]
  |
  v
[Schedule 3-4 hour block, distribute pre-reading]
  |
  v
End
```

## Workflow 2: Exercise Execution

```
Exercise Start
  |
  v
[Facilitator opening brief] (10 min)
  |-- Ground rules, objectives, scope
  |-- "This is discussion-based, no wrong answers"
  |
  v
[Phase 1: Initial Detection] (30 min)
  |-- Distribute SITREP 1
  |-- Discussion: Who, what, when, initial actions
  |-- Inject: Additional information changes situation
  |-- Document decisions on worksheet
  |
  v
[Phase 2: Escalation] (30 min)
  |-- Distribute SITREP 2
  |-- Discussion: Scope of impact, containment actions
  |-- Inject: Double extortion element introduced
  |-- Document decisions
  |
  v
[Break] (10 min)
  |
  v
[Phase 3: Critical Decision Points] (45 min)
  |-- Distribute SITREP 3
  |-- Discussion: Ransom payment, law enforcement, notification
  |-- Inject: Public pressure from media/customers
  |-- Document decisions with rationale
  |
  v
[Phase 4: Recovery and Communication] (45 min)
  |-- Distribute SITREP 4
  |-- Discussion: Recovery priority, timeline, customer comms
  |-- Inject: Recovery complication (infected backup, key system fails)
  |-- Document decisions
  |
  v
[Hot wash / Debrief] (20 min)
  |-- Each functional area shares top insight
  |-- Facilitator highlights key observations
  |-- Immediate gap identification
  |
  v
Exercise End
```

## Workflow 3: After-Action Report Development

```
Exercise Complete
  |
  v
[Collect all documentation within 24 hours]
  |-- Decision worksheets
  |-- Facilitator notes
  |-- Evaluation scorecards
  |-- Observer notes (if separate observers present)
  |
  v
[Score each evaluation area (1-5)]
  |
  v
[Identify strengths (what worked well)]
  |
  v
[Identify gaps with severity rating]
  |-- Critical: Would prevent effective response
  |-- High: Would significantly delay/complicate response
  |-- Medium: Would reduce response quality
  |-- Low: Minor improvement opportunity
  |
  v
[Develop remediation actions]
  |-- Each gap gets: action, owner, deadline, priority
  |-- Must be specific and measurable
  |
  v
[Draft AAR within 5 business days]
  |
  v
[Review AAR with exercise sponsor]
  |
  v
[Distribute AAR to participants]
  |
  v
[Track remediation actions quarterly]
  |
  v
End
```

---

## Working Template

## Exercise Overview

| Field | Value |
|-------|-------|
| Exercise Name | |
| Date | |
| Duration | 3-4 hours |
| Facilitator | |
| Scenario | [Threat Actor] ransomware attack |
| Industry | |

## Participants

| Name | Role | Department | Present (Y/N) |
|------|------|-----------|---------------|
| | CISO | Security | |
| | CIO | IT | |
| | General Counsel | Legal | |
| | VP Comms | PR | |
| | COO | Operations | |
| | CFO | Finance | |

## Phase 1: Detection SITREP

[Insert scenario text]

### Discussion Questions
1. Who declares the incident?
2. What is the immediate containment action?
3. Who is notified at this stage?

### Decisions Made
| Decision | Rationale | Owner |
|----------|-----------|-------|
| | | |

## Phase 2: Escalation SITREP

[Insert scenario text]

### Discussion Questions
1. What is the scope assessment process?
2. How do we maintain business operations?
3. Do we engage law enforcement?

### Decisions Made
| Decision | Rationale | Owner |
|----------|-----------|-------|
| | | |

## Phase 3: Critical Decisions SITREP

[Insert scenario text]

### Discussion Questions
1. Under what conditions do we pay?
2. What are notification obligations?
3. How do we respond to data leak?

### Decisions Made
| Decision | Rationale | Owner |
|----------|-----------|-------|
| | | |

## Phase 4: Recovery SITREP

[Insert scenario text]

### Discussion Questions
1. What is recovery priority order?
2. What do we tell customers?
3. What is the media statement?

### Decisions Made
| Decision | Rationale | Owner |
|----------|-----------|-------|
| | | |

## Evaluation Scorecard

| Area | Score (1-5) | Notes |
|------|-------------|-------|
| Detection & Escalation | | |
| Containment | | |
| Internal Communication | | |
| External Communication | | |
| Recovery Planning | | |
| Legal & Compliance | | |
| Business Continuity | | |
| Payment Decision | | |
| **Overall** | | |

## Key Findings

### Strengths
1.
2.
3.

### Gaps
| Gap | Severity | Owner | Remediation | Deadline |
|-----|----------|-------|-------------|----------|
| | Critical/High/Medium | | | |

## Sign-Off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Exercise Sponsor | | | |
| Facilitator | | | |
