# Conducting Post Incident Lessons Learned

## API Reference

## Libraries

| Library | Install | Purpose |
|---------|---------|---------|
| requests | `pip install requests` | API calls to ticketing/SIEM systems |
| jinja2 | `pip install Jinja2` | Report template rendering |
| matplotlib | `pip install matplotlib` | Timeline and metric visualization |

## Key Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| MTTD | Detection time - Incident start | < 30 minutes |
| MTTC | Containment time - Detection time | < 60 minutes |
| MTTR | Resolution time - Detection time | < 4 hours |
| Dwell Time | Detection time - Initial compromise | < 24 hours |

## NIST SP 800-61 Phases

| Phase | Activities |
|-------|-----------|
| Preparation | Playbooks, tools, training |
| Detection & Analysis | Alert triage, scoping, evidence collection |
| Containment | Short-term and long-term isolation |
| Eradication & Recovery | Root cause removal, system restoration |
| Post-Incident | Lessons learned, action items, metrics |

## Report Template Sections

| Section | Content |
|---------|---------|
| Executive Summary | Impact, scope, duration |
| Timeline | Chronological event sequence |
| Root Cause | 5-Whys or fishbone analysis |
| Action Items | Prioritized P1/P2/P3 with owners |

## External References

- [NIST SP 800-61 Rev. 2](https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final)
- [SANS Incident Handler's Handbook](https://www.sans.org/white-papers/33901/)
- [VERIS Framework](http://veriscommunity.net/)

---

## Standards and Controls

## NIST SP 800-61 Rev. 2 - Section 3.4 Post-Incident Activity
- 3.4.1: Lessons Learned meetings after each significant incident
- 3.4.2: Using Collected Incident Data for trending and metrics
- Recommends formal review within days of resolution

## NIST SP 800-61 Rev. 3 - Continuous Improvement
- Recover (RC) function: Learning from incidents
- RC.CO-03: Recovery activities and progress communicated
- Emphasis on continuous improvement of IR capabilities

## SANS PICERL - Lessons Learned Phase
- Phase 6: Final phase of incident handling
- Formal review with all stakeholders
- Document improvements and update procedures

## MITRE ATT&CK - Detection Gap Analysis
- Map incident techniques to ATT&CK framework
- Identify detection gaps in current monitoring
- Develop new detection rules based on observed TTPs

## ISO 27001 - Clause 10: Improvement
- 10.1: Nonconformity and corrective action
- 10.2: Continual improvement
- Requires organizations to learn from security incidents

## Google SRE Post-Mortem Culture
- Blameless approach to incident review
- Focus on systemic issues rather than human error
- Document and share learnings broadly

---

## Workflows

## Pre-Meeting Preparation (1-3 days before)
1. Compile complete incident timeline from all sources
2. Gather all communication logs (email, chat, phone)
3. Export incident metrics from ticketing system
4. Collect detection data from SIEM/EDR
5. Identify all participants and send calendar invites

## Meeting Facilitation Guide

### Ground Rules
1. Blameless discussion - focus on processes and systems
2. Everyone's perspective is valued equally
3. Objective review of facts, not opinions
4. All observations documented in real-time
5. Action items must have owners and deadlines

### Discussion Framework
1. What was the incident? (5 min) - Brief factual summary
2. Walk the timeline (20 min) - Chronological event review
3. What went well? (15 min) - Effective actions and decisions
4. What could improve? (15 min) - Gaps and failures
5. Root cause deep dive (15 min) - 5 Whys or fishbone diagram
6. Action items (10 min) - Assigned improvements
7. Playbook updates (10 min) - Procedural changes

## Key Metrics Framework

| Metric | Formula | Industry Benchmark |
|--------|---------|-------------------|
| Dwell Time | Detection - Initial Compromise | Median: 10 days (Mandiant) |
| MTTD | Triage Complete - First Alert | Target: < 15 min (P1) |
| MTTC | Containment Complete - Detection | Target: < 4 hours |
| MTTR | Recovery Complete - Eradication | Target: < 48 hours |
| Total Duration | Closure - Detection | Target: < 7 days |

## Action Item Categories

### Process
- Updated playbooks and runbooks
- Communication plan updates
- Escalation criteria changes

### Technology
- New detection rules
- Tool improvements
- Monitoring expansion
- Automation opportunities

### People
- Training needs
- Staffing gaps
- Cross-training requirements

## Follow-Up Schedule
- 1 week: Action items tracked in project system
- 1 month: First progress review
- 3 months: Validate improvements with tabletop
- 6 months: Re-evaluate metrics

---

## Working Template

## Incident Information
| Field | Value |
|-------|-------|
| Incident ID | |
| Incident Type | |
| Severity | |
| Date Detected | |
| Date Resolved | |
| Review Date | |
| Facilitator | |

## Incident Summary
[Brief factual description of the incident]

## Response Metrics
| Metric | Value | Target | Met Target |
|--------|-------|--------|------------|
| Dwell Time | | < 24 hours | Yes/No |
| MTTD (Detection to Triage) | | < 15 min | Yes/No |
| MTTC (Detection to Containment) | | < 4 hours | Yes/No |
| Eradication Duration | | < 24 hours | Yes/No |
| MTTR (Eradication to Recovery) | | < 48 hours | Yes/No |
| Total Incident Duration | | < 7 days | Yes/No |

## Timeline
| Date/Time (UTC) | Event | Actor |
|-----------------|-------|-------|
| | Initial compromise (estimated) | Threat actor |
| | First alert generated | SIEM/EDR |
| | Triage completed | SOC analyst |
| | Incident declared | IR lead |
| | Containment achieved | IR team |
| | Eradication completed | IR team |
| | Recovery completed | IT ops |
| | Incident closed | IR lead |

## What Worked Well
-
-
-

## What Needs Improvement
-
-
-

## Root Cause Analysis (5 Whys)
| Level | Question | Answer |
|-------|----------|--------|
| Why 1 | | |
| Why 2 | | |
| Why 3 | | |
| Why 4 | | |
| Why 5 | | |

**Root Cause:** [Summary]

## Action Items
| ID | Action | Owner | Priority | Deadline | Category | Status |
|----|--------|-------|----------|----------|----------|--------|
| 1 | | | High/Med/Low | | Process/Tech/People | Open |
| 2 | | | | | | |
| 3 | | | | | | |

## Playbook Updates Required
| Playbook | Change Description | Owner | Deadline |
|----------|--------------------|-------|----------|
| | | | |

## Detection Improvements
| Rule Name | Description | MITRE Technique | Priority |
|-----------|-------------|-----------------|----------|
| | | | |

## Participants
| Name | Role | Present |
|------|------|---------|
| | Incident Commander | Yes/No |
| | SOC Analyst | Yes/No |
| | IR Lead | Yes/No |
| | CISO | Yes/No |

## Meeting Notes
[Key discussion points and decisions]

## Approval
| Role | Name | Date |
|------|------|------|
| IR Lead | | |
| CISO | | |
