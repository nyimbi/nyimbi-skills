# Performing Threat Modeling With Owasp Threat Dragon

## API Reference

## Threat Dragon JSON Model Structure

| Field | Description |
|-------|-------------|
| `version` | Threat Dragon version (e.g., "2.2.0") |
| `summary.title` | Threat model name |
| `summary.owner` | Model owner |
| `detail.diagrams[]` | Array of DFD diagrams |
| `detail.diagrams[].cells[]` | DFD elements within a diagram |
| `detail.diagrams[].diagramType` | Methodology (STRIDE, LINDDUN, CIA) |

## DFD Element Types

| Type | Threat Dragon Class | STRIDE Categories |
|------|--------------------|--------------------|
| Process | `tm.Process` | S, T, R, I, D, E |
| Data Store | `tm.Store` | T, I, D |
| Data Flow | `tm.Flow` | T, I, D |
| External Entity | `tm.Actor` | S, R |
| Trust Boundary | `tm.Boundary` | N/A |

## STRIDE Categories

| Letter | Threat | Mitigation |
|--------|--------|------------|
| S | Spoofing | Strong authentication, MFA |
| T | Tampering | Integrity checks, HMAC |
| R | Repudiation | Audit logging |
| I | Information Disclosure | Encryption, least privilege |
| D | Denial of Service | Rate limiting, auto-scaling |
| E | Elevation of Privilege | RBAC, authorization checks |

## Threat Status Values

| Status | Description |
|--------|-------------|
| Open | Threat needs mitigation |
| Mitigated | Controls address the threat |
| Not Applicable | Threat does not apply |

## Docker Deployment

```bash
docker run -p 3000:3000 \
  -e ENCRYPTION_JWT_SIGNING_KEY=$(openssl rand -hex 32) \
  -e ENCRYPTION_JWT_REFRESH_SIGNING_KEY=$(openssl rand -hex 32) \
  owasp/threat-dragon:latest
```

## Python Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| `json` | stdlib | Threat Dragon model serialization |
| `uuid` | stdlib | Generate unique element IDs |

## References

- OWASP Threat Dragon: https://owasp.org/www-project-threat-dragon/
- Threat Dragon GitHub: https://github.com/OWASP/threat-dragon
- STRIDE Model: https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats
- LINDDUN: https://www.linddun.org/

---

## Standards and Controls

## OWASP Threat Modeling Process

1. **Decompose the application**: Create DFDs showing data flows, trust boundaries, entry points
2. **Determine and rank threats**: Apply STRIDE per element, rank by DREAD or risk matrix
3. **Determine countermeasures and mitigations**: Map threats to controls
4. **Review and validate**: Peer review the model, validate against architecture

## NIST SP 800-154: Guide to Data-Centric System Threat Modeling

- Identify data assets and their sensitivity levels
- Map data flows through system components
- Identify threat actors and attack vectors targeting data
- Assess risk based on data exposure and impact
- Document countermeasures protecting data at rest, in transit, and in use

## ISO 27005 Risk Assessment Alignment

| ISO 27005 Step | Threat Dragon Activity |
|----------------|----------------------|
| Context establishment | Define system scope and trust boundaries |
| Risk identification | STRIDE threat enumeration per DFD element |
| Risk analysis | Severity rating and likelihood assessment |
| Risk evaluation | Prioritize threats by risk score |
| Risk treatment | Define mitigations (mitigate, accept, transfer, avoid) |

## STRIDE-per-Element Mapping

| DFD Element | S | T | R | I | D | E |
|-------------|---|---|---|---|---|---|
| External Entity | x | | x | | | |
| Process | x | x | x | x | x | x |
| Data Store | | x | | x | x | |
| Data Flow | | x | | x | x | |

## Threat Severity Rating Scale

| Rating | Score | Description |
|--------|-------|-------------|
| Critical | 9-10 | Immediate exploitation possible, severe business impact |
| High | 7-8 | Likely exploitation, significant business impact |
| Medium | 4-6 | Possible exploitation, moderate business impact |
| Low | 1-3 | Unlikely exploitation or minimal impact |

---

## Workflows

## Workflow 1: Feature-Level Threat Modeling

```
Product team proposes new feature
       |
Security champion schedules threat modeling session
       |
Gather architecture docs, API specs, DFDs
       |
Workshop session (60-90 min):
  - Review DFD for new feature
  - Apply STRIDE to each element
  - Identify threats and rank by severity
  - Document mitigations needed
       |
Threats documented in Threat Dragon
       |
Mitigation tasks created in backlog
       |
Security acceptance criteria added to user stories
       |
Feature development includes mitigations
       |
Threat model updated during code review
```

## Workflow 2: Architecture Review Threat Model

```
New system or major refactor proposed
       |
Create Level 0 DFD (context diagram)
       |
Identify trust boundaries and data sensitivity
       |
Decompose into Level 1 DFDs per subsystem
       |
Apply STRIDE per element in each diagram
       |
Auto-generate threats using Threat Dragon rule engine
       |
Review and refine auto-generated threats
       |
Assign severity ratings
       |
Document existing controls as mitigations
       |
Identify gaps (open threats without mitigations)
       |
Generate PDF report for architecture review board
       |
Remediation plan approved and tracked
```

## Workflow 3: Continuous Threat Modeling in Agile

```
Sprint planning identifies security-relevant stories
       |
Pull existing threat model from version control
       |
Update DFD to reflect planned changes
       |
Quick STRIDE review (30 min) focused on changes
       |
New threats added, mitigations defined
       |
Threat model committed alongside code changes
       |
Sprint retrospective reviews threat model accuracy
       |
Quarterly full threat model review cycle
```

---

## Working Template

## System Information

| Field | Value |
|-------|-------|
| System Name | |
| Version/Release | |
| Owner | |
| Date | |
| Participants | |
| Methodology | [ ] STRIDE [ ] LINDDUN [ ] CIA [ ] DIE |

## Scope Definition

**Assets to Protect:**
1.
2.
3.

**Trust Boundaries:**
1.
2.

**External Dependencies:**
1.
2.

## Threat Register

| ID | Element | STRIDE Category | Threat Description | Severity | Status | Mitigation | Owner |
|----|---------|-----------------|-------------------|----------|--------|------------|-------|
| T-001 | | | | | [ ] Open [ ] Mitigated [ ] N/A | | |
| T-002 | | | | | [ ] Open [ ] Mitigated [ ] N/A | | |

## Action Items

| Item | Description | Owner | Due Date | Status |
|------|-------------|-------|----------|--------|
| | | | | |

## Review Schedule

- [ ] Initial threat model created
- [ ] Peer review completed
- [ ] Architecture review board sign-off
- [ ] Quarterly review scheduled
- [ ] Model updated for last architecture change
