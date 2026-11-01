# Designing Adversary Engagement With Mitre Engage

## Standards and Controls

## Primary framework
### MITRE Engage™ v1.0
- **Publisher**: The MITRE Corporation
- **Version**: 1.0, last updated 2022-02-28
- **Home**: https://engage.mitre.org
- **Live Matrix**: https://engage.mitre.org/matrix/ (authoritative source for all Goal/Approach/Activity names and IDs)
- **Starter Kit**: https://engage.mitre.org/starter-kit/ (10-Step Process, planning worksheets, whitepapers)
- **Predecessor**: MITRE Shield (Engage supersedes and restructures Shield).
- **Note**: Engage is a framework for *planning and discussing* denial, deception, and adversary engagement. It is not a tool; it provides a shared language across defenders, vendors, and decision-makers.

## Engage Matrix structure
Five columns (Goals): **Prepare · Expose · Affect · Elicit · Understand**
- **Prepare** and **Understand** are *strategic* bookends (operation inputs and outputs).
- **Expose**, **Affect**, **Elicit** are the three *Engagement* goals; together they form the default **Operate** view and are mapped to MITRE ATT&CK.

### ID prefixes (verified from engage.mitre.org)
| Component | Strategic prefix | Engagement prefix |
|---|---|---|
| Goals | SGO | EGO |
| Approaches | SAP | EAP |
| Activities | SAC | EAC |

Always resolve specific numeric IDs (e.g., the EAC for "Decoy Credentials") against the live matrix rather than from memory.

### Engagement Approaches (EAP) by Goal
- **Expose** → Collection, Detection
- **Affect** → Prevention, Direction, Disruption
- **Elicit** → Reassurance, Motivation

### Representative Engagement Activities (EAC), by name
Decoy Credentials · Decoy Content · Decoy Account · Decoy Diversity · Lures · Pocket Litter ·
Persona Creation · Artifact Diversity · Network Diversity · Application Diversity ·
Email Manipulation · Network Manipulation · Software Manipulation · Hardware Manipulation ·
Security Controls · Isolation · Attack Vector Migration · Peripheral Management · Baseline ·
Network Monitoring · System Activity Monitoring · API Monitoring · Malware Detonation ·
Burn-In · Introduced Vulnerabilities.

> The matrix maps each Activity to the ATT&CK techniques whose execution exposes an adversary weakness. Use the Navigator overlay to confirm current mappings.

## Operating principle: Affect is defender-network-only
All Affect Activities are constrained to infrastructure the defender owns and controls. Acting on adversary or third-party infrastructure is out of scope and creates legal exposure.

## Complementary frameworks

### MITRE ATT&CK
- https://attack.mitre.org — the technique catalog used to model the target adversary. Engagement Activities exist to exploit the weaknesses adversary techniques create.

### MITRE D3FEND — `Deceive` tactic
D3FEND (https://d3fend.mitre.org) provides defensive-technique naming that pairs with Engage. The `Deceive` tactic includes:
- **Decoy Environment**: Connected Honeynet, Integrated Honeynet, Standalone Honeynet
- **Decoy Object**: Decoy File, Decoy Network Resource, Decoy Persona, Decoy Public Release, Decoy Session Token, Decoy User Credential

Use D3FEND honeynet types when documenting environment isolation in the operation plan:
- **Standalone Honeynet** — fully isolated; safest; least realistic to a sophisticated adversary.
- **Connected Honeynet** — bridged to production paths to appear reachable; moderate risk.
- **Integrated Honeynet** — decoys interleaved with production assets; most realistic; highest operational risk and tightest gating required.

## NIST CSF 2.0 alignment
| CSF 2.0 ID | Relevance to adversary engagement |
|---|---|
| GV.RM-01 | Risk management objectives established — anchors the strategic Prepare goal |
| ID.RA-01 | Vulnerabilities identified — informs which weaknesses to expose |
| ID.IM-02 | Security testing / improvement — engagement operations validate detections |
| DE.CM-01 | Networks monitored to find adverse events — Expose Activities feed monitoring |
| DE.AE-02 | Potentially adverse events analyzed — triage of decoy alerts |

## Legal & ethical references
- Engagement operations interact with live adversaries; obtain written legal review before deployment.
- Preserve evidence per the organization's incident-response and forensics procedures (chain of custody).
- Coordinate with law enforcement engagement policy where applicable.
- Document rules of engagement and gating criteria before any Activity is deployed.

---

## Working Template

> Worked example. Replace bracketed values. Do not deploy any Activity before legal sign-off and approved gating criteria.

## 1. Strategic context
- **Operation name:** Crown-Jewel Repo Watch
- **Strategic goal (Prepare):** Reduce dwell time of unauthorized access around the source-code repository and produce first-party CTI on whoever reaches it.
- **Where DD&AE fits the strategy:** Additive layer behind EDR + network segmentation; activates only if a primary control is bypassed.
- **Executive sponsor:** [CISO name]
- **Legal sign-off reference:** [Legal ticket / memo ID] — REQUIRED before deployment

## 2. Engagement Goals + Operational Objectives
| Goal (EGO) | Operational Objective (falsifiable, time-bound) |
|---|---|
| Expose | Alert the SOC within 5 minutes of any touch on a decoy repo credential or decoy commit. |
| Affect | Redirect lateral-movement attempts away from 2 unpatchable build servers for the duration of the operation. |
| Elicit | Obtain ≥10 new indicators and, if possible, one second-stage tool sample within 30 days. |

## 3. Threat model
- **Target adversary:** Suspected initial-access broker reselling dev-environment footholds.
- **Prioritized ATT&CK techniques:** T1078 (Valid Accounts), T1552 (Unsecured Credentials), T1083 (File & Directory Discovery), T1021 (Remote Services), T1046 (Network Service Discovery).

## 4. Activity selection matrix
| ATT&CK | Weakness exposed | Engage Activity (resolve EAC on live matrix) | Deployment owner | Tactical skill |
|---|---|---|---|---|
| T1078 | Must test credentials | Decoy Credentials, Lures | [Detection eng.] | deploying-active-directory-honeytokens |
| T1552 | Harvests secrets | Decoy Credentials, Artifact Diversity | [Detection eng.] | implementing-honeytokens-for-breach-detection |
| T1083 | Enumerates files | Decoy Content, Pocket Litter | [Blue team] | deploying-decoy-files-for-ransomware-detection |
| T1021 | Moves laterally | Network Manipulation, Decoy Systems | [Network eng.] | implementing-network-deception-with-honeypots |
| T1046 | Scans the network | Network Diversity | [Network eng.] | implementing-network-deception-with-honeypots |

## 5. Engagement environment design
- **Honeynet type:** Connected honeynet (reachable from the dev VLAN, isolated from prod data).
- **Realism / artifact plan:** Decoy repo with believable Pocket Litter (fake CI tokens, stale branches), Persona Creation for a fake "build-bot" account, Application Diversity to mimic the real toolchain.

## 6. Gating criteria & rules of engagement
- **Max blast radius:** Decoy VLAN only; no route to production data stores.
- **Tear-down / IR hand-off trigger:** Any attempt to pivot toward a real prod subnet, OR collection of the second-stage sample, whichever first.
- **Evidence handling:** Full pcap + host telemetry preserved to WORM storage; chain-of-custody log maintained.
- **Escalation authority:** [IR lead] may halt the operation at any time.
- **Affect Activities restricted to defender-owned network.** (Hard constraint — never act on infrastructure you do not own.)

## 7. Measurement plan
| Objective | Metric | Baseline | Result |
|---|---|---|---|
| Expose latency | Minutes from decoy touch to SOC alert | n/a (new) | [fill post-op] |
| Affect redirect | Lateral attempts steered from build servers | 0 | [fill post-op] |
| Elicit intel | New indicators / samples obtained | 0 | [fill post-op] |

## 8. After-action report (complete post-operation)
- **Objectives met/missed:** [ ]
- **Intel produced (indicators, samples, TTPs):** [ ]
- **Detections promoted to production:** [ ]
- **Threat-model updates for next cycle:** [ ]
