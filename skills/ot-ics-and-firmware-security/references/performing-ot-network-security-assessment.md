# Performing OT Network Security Assessment

## API Reference

## Libraries Used
- **csv**: Parse asset inventories and firewall rule exports
- **subprocess**: Execute nmap for OT protocol scanning
- **xml.etree.ElementTree**: Parse nmap XML output

## CLI Interface
```
python agent.py assets --csv ot_inventory.csv
python agent.py segmentation --csv firewall_rules.csv
python agent.py protocols --subnet 192.168.1.0/24
python agent.py report --assets inventory.csv [--firewall fw_rules.csv]
```

## Core Functions

### `assess_asset_inventory(csv_file)` — Purdue model zone analysis
Groups assets by Purdue level. Flags end-of-life and unknown firmware.

### `assess_network_segmentation(csv_file)` — Firewall rule audit
Detects: direct IT-to-OT access (CRITICAL), allow-any-protocol rules (HIGH).

### `scan_ot_protocols(target_subnet)` — OT protocol discovery
Scans ports: 102 (S7), 502 (Modbus), 4840 (OPC-UA), 44818 (EtherNet/IP),
47808 (BACnet), 20000 (DNP3).

### `generate_assessment_report(...)` — Comprehensive report

## OT Protocol Ports
| Port | Protocol | Usage |
|------|----------|-------|
| 102 | S7Comm | Siemens S7 PLCs |
| 502 | Modbus TCP | Industrial automation |
| 4840 | OPC-UA | Industrial data exchange |
| 44818 | EtherNet/IP | Allen-Bradley PLCs |
| 47808 | BACnet | Building automation |
| 20000 | DNP3 | SCADA/utility |

## Dependencies
System: nmap (optional, for protocol scanning)
No Python packages required.

---

## Standards and Controls

## IEC 62443 (ISA/IEC 62443)

### IEC 62443-1-1: Terminology, Concepts, and Models
- Defines foundational concepts including zones, conduits, security levels, and the IACS reference architecture
- Establishes the vocabulary used across all parts of the standard

### IEC 62443-2-1: Security Management System Requirements
- Requirements for an IACS security management system (SMS)
- Covers risk assessment, security policies, organization, staff competence, and awareness

### IEC 62443-3-2: Security Risk Assessment for System Design
- Defines the process for partitioning an IACS into zones and conduits
- Establishes Security Level targets (SL-T) for each zone based on risk assessment
- Zone characteristics: assets, access points, communication channels, data flows
- Conduit characteristics: connected zones, protocols, security countermeasures

### IEC 62443-3-3: System Security Requirements and Security Levels
- Foundational requirements (FR) mapped to security levels (SL 1-4):
  - FR 1: Identification and Authentication Control (IAC)
  - FR 2: Use Control (UC)
  - FR 3: System Integrity (SI)
  - FR 4: Data Confidentiality (DC)
  - FR 5: Restricted Data Flow (RDF)
  - FR 6: Timely Response to Events (TRE)
  - FR 7: Resource Availability (RA)

### Security Levels
| Level | Description |
|-------|-------------|
| SL 1 | Protection against casual or coincidental violation |
| SL 2 | Protection against intentional violation using simple means |
| SL 3 | Protection against sophisticated attack with moderate resources |
| SL 4 | Protection against state-sponsored attack with extensive resources |

## NIST SP 800-82 Revision 3

### Guide to Operational Technology (OT) Security
- Published September 2023, replacing the ICS-focused Rev. 2
- Expanded scope covers: ICS/SCADA, building automation, transportation, physical access control, physical environment monitoring
- Provides OT overlay for NIST SP 800-53r5 security controls
- Tailored security control baselines for low/moderate/high-impact OT systems

### Key Sections for Network Assessment
- Section 3: OT Overview and Architectures (Purdue Model reference)
- Section 4: OT Risk Management
- Section 5: OT Security Architecture (network segmentation, DMZ design)
- Section 6: Applying Security Controls to OT (overlay guidance)

### OT-Specific Control Tailoring
- AC-4 (Information Flow Enforcement): Implement data diodes for unidirectional flows from Level 3 to Level 3.5
- SC-7 (Boundary Protection): Industrial firewalls with protocol-aware deep packet inspection
- AU-6 (Audit Record Review): Correlate OT network events with process alarms

## NERC CIP Standards (Power Sector)

### CIP-002-5.1a: BES Cyber System Categorization
- Identify and categorize Bulk Electric System (BES) cyber systems as high, medium, or low impact

### CIP-005-7: Electronic Security Perimeters
- Define Electronic Security Perimeters (ESP) around BES cyber systems
- Require Electronic Access Points (EAP) at all ESP boundaries
- 2025 update requires MFA for remote access to medium and high-impact systems

### CIP-007-6: System Security Management
- Port and service management, security patch management
- Malicious code prevention, security event monitoring
- System access controls and authentication

### CIP-010-4: Configuration Change Management and Vulnerability Assessments
- Baseline configurations for BES cyber systems
- Transient cyber asset and removable media management
- Active vulnerability assessments at least every 15 months

## Purdue Reference Model (ISA-95)

### Level Architecture
| Level | Name | Examples |
|-------|------|----------|
| Level 0 | Physical Process | Sensors, actuators, analyzers |
| Level 1 | Basic Control | PLCs, RTUs, safety controllers |
| Level 2 | Area Supervisory Control | HMI, engineering workstations, local historian |
| Level 3 | Site Operations | OPC servers, site historian, MES |
| Level 3.5 | DMZ | Data diodes, jump servers, patch servers |
| Level 4 | Enterprise | ERP, email, corporate IT |
| Level 5 | Internet/Cloud | Remote access, cloud services |

---

## Workflows

## Assessment Lifecycle

```
Phase 1: Scoping          Phase 2: Discovery       Phase 3: Analysis
+-----------------+       +-----------------+      +-----------------+
| Define scope    |       | Passive capture |      | Protocol review |
| Safety limits   | ----> | Asset inventory | ---> | Zone evaluation |
| Authorization   |       | Traffic mapping |      | Firewall audit  |
+-----------------+       +-----------------+      +-----------------+
                                                          |
Phase 6: Verify           Phase 5: Remediate       Phase 4: Report
+-----------------+       +-----------------+      +-----------------+
| Validate fixes  |       | Segmentation    |      | Risk scoring    |
| Re-assessment   | <---- | FW rule changes | <--- | Finding detail  |
| Compliance map  |       | Protocol harden |      | Prioritization  |
+-----------------+       +-----------------+      +-----------------+
```

## Phase 1: Scoping and Authorization

### Inputs
- Facility type and industry vertical
- Regulatory requirements (NERC CIP, IEC 62443, NIST CSF)
- Existing network diagrams and asset inventories
- Maintenance window schedules

### Activities
1. Meet with operations, engineering, and IT security teams
2. Define Purdue levels in scope and safety-critical exclusions
3. Obtain written authorization specifying permitted assessment activities
4. Identify SPAN/TAP points for passive monitoring deployment
5. Review prior assessment reports and known issues

### Outputs
- Signed Rules of Engagement document
- Assessment scope matrix (Purdue levels vs. activity types)
- SPAN/TAP deployment plan
- Emergency contact list and escalation procedures

## Phase 2: Passive Network Discovery

### Inputs
- SPAN port access on OT network switches
- Assessment scope document

### Activities
1. Deploy passive monitoring sensors on SPAN ports at each Purdue level boundary
2. Capture network traffic for minimum 2 weeks to observe full operational cycle
3. Build asset inventory from observed traffic (MAC, IP, protocols, firmware versions)
4. Map all communication flows with source, destination, protocol, and frequency
5. Identify industrial protocols in use (Modbus, DNP3, OPC UA, EtherNet/IP, S7comm)
6. Detect unauthorized devices and rogue connections

### Activities - Wireless Assessment
1. Scan for wireless access points in OT areas using spectrum analyzer
2. Identify wireless industrial protocols (WirelessHART, ISA100.11a, Zigbee)
3. Check for unauthorized Wi-Fi networks bridging IT and OT

### Outputs
- Complete asset inventory with Purdue level classification
- Network communication flow map
- Protocol distribution analysis
- Unauthorized device/connection list

## Phase 3: Analysis and Evaluation

### Inputs
- Asset inventory and traffic capture data
- Firewall rule exports
- Network architecture diagrams

### Activities
1. Evaluate zone architecture against IEC 62443-3-2 requirements
2. Analyze firewall rules for overly permissive or prohibited conduits
3. Assess industrial protocol security (authentication, encryption, access controls)
4. Review remote access architecture and authentication mechanisms
5. Evaluate patch levels of HMI, engineering workstations, and servers
6. Check for known vulnerabilities in discovered OT firmware versions
7. Assess physical security of network equipment in field locations

### Outputs
- Finding list with severity ratings
- Gap analysis against applicable standards
- Risk matrix mapping findings to operational/safety impact

## Phase 4: Reporting

### Report Structure
1. Executive Summary (1 page)
2. Scope and Methodology
3. Asset Inventory Summary
4. Network Architecture Assessment
5. Detailed Findings (Critical/High/Medium/Low)
6. Compliance Gap Analysis
7. Remediation Roadmap with Prioritization
8. Appendices (asset inventory, network diagrams, tool output)

## Phase 5: Remediation Support

### Priority Order
1. **Immediate**: Block unauthorized cross-zone paths (enterprise to field devices)
2. **30-day**: Implement DMZ between corporate IT and OT operations
3. **60-day**: Deploy industrial protocol-aware firewalls between zones
4. **90-day**: Harden remote access with MFA and jump servers
5. **6-month**: Full zone/conduit segmentation per IEC 62443 design

## Risk Scoring for OT Environments

OT risk scoring must account for safety impact beyond traditional CIA triad:

| Factor | Weight | Description |
|--------|--------|-------------|
| Safety Impact | 30% | Potential for physical harm to personnel or public |
| Operational Impact | 25% | Production disruption or equipment damage |
| Environmental Impact | 15% | Release of hazardous materials |
| Financial Impact | 15% | Direct costs and regulatory penalties |
| Reputational Impact | 15% | Public trust and regulatory scrutiny |

---

## Working Template

## Document Information

| Field | Value |
|-------|-------|
| Facility | [Facility Name and Location] |
| Assessment Date | YYYY-MM-DD to YYYY-MM-DD |
| Lead Assessor | [Name, Certification] |
| Standard | IEC 62443-3-3 / NIST SP 800-82r3 |
| Classification | [Confidential / Internal Use Only] |
| Report Version | 1.0 |

## Executive Summary

[2-3 paragraphs summarizing the assessment scope, methodology, key findings, and overall risk rating. Written for C-level and operations management audience.]

**Overall Risk Rating**: [Critical / High / Moderate / Low]

**Key Statistics**:
- Total OT assets discovered: [N]
- Critical findings: [N]
- High findings: [N]
- Unauthenticated protocol exposures: [N]
- Cross-zone violations: [N]

## 1. Scope and Methodology

### 1.1 Assessment Scope

| Purdue Level | In Scope | Activity Type |
|-------------|----------|---------------|
| Level 0-1 (Field) | Yes/No | Passive Only |
| Level 2 (Control) | Yes/No | Passive + Limited Active |
| Level 3 (Operations) | Yes/No | Active Permitted |
| Level 3.5 (DMZ) | Yes/No | Active Permitted |
| Level 4 (Enterprise) | Yes/No | Active Permitted |

### 1.2 Exclusions
- [List safety-critical systems excluded from assessment]
- [List maintenance windows utilized for active testing]

### 1.3 Methodology
- Passive network monitoring via SPAN ports ([duration])
- Industrial protocol deep packet inspection
- Firewall rule analysis
- [Other assessment activities performed]

### 1.4 Tools Used
- [Tool 1]: [Purpose]
- [Tool 2]: [Purpose]

## 2. Asset Inventory

### 2.1 Asset Summary by Purdue Level

| Level | Device Type | Count | Key Vendors |
|-------|------------|-------|-------------|
| Level 0-1 | PLCs, RTUs, I/O | [N] | [Vendors] |
| Level 2 | HMI, EWS | [N] | [Vendors] |
| Level 3 | Historian, OPC | [N] | [Vendors] |
| Level 3.5 | DMZ systems | [N] | [Vendors] |
| Level 4 | Enterprise | [N] | [Vendors] |

### 2.2 Industrial Protocol Distribution

| Protocol | Port | Packet Count | Device Count | Auth Support |
|----------|------|-------------|-------------|-------------|
| Modbus/TCP | 502 | [N] | [N] | No |
| EtherNet/IP | 44818 | [N] | [N] | No |
| OPC UA | 4840 | [N] | [N] | Yes |
| S7comm | 102 | [N] | [N] | No |
| DNP3 | 20000 | [N] | [N] | Optional |

## 3. Network Architecture Assessment

### 3.1 Zone Architecture Evaluation
[Assessment of current zone/conduit architecture against IEC 62443-3-2]

### 3.2 Cross-Zone Communication Analysis
[Summary of authorized and unauthorized cross-zone communication flows]

### 3.3 Firewall Rule Analysis
[Summary of firewall rule review findings]

## 4. Findings

### 4.1 Finding Template

```
Finding ID: OT-[NNN]
Severity: [Critical / High / Medium / Low]
Title: [Finding Title]
Affected Assets: [Asset list]
IEC 62443 Reference: [Section reference]
NIST 800-82r3 Reference: [Section reference]

Description:
[Detailed technical description of the finding]

Evidence:
[Screenshots, packet captures, or tool output demonstrating the finding]

Operational Impact:
[Impact on process safety, availability, and operations]

Remediation:
[Specific technical steps to remediate the finding]

Compensating Controls:
[Interim measures if immediate remediation is not feasible]
```

### 4.2 Critical Findings
[List all critical findings using template above]

### 4.3 High Findings
[List all high findings]

### 4.4 Medium Findings
[List all medium findings]

### 4.5 Low Findings
[List all low findings]

## 5. Risk Matrix

| Finding ID | Likelihood | Safety Impact | Operational Impact | Overall Risk |
|-----------|-----------|---------------|-------------------|-------------|
| OT-001 | [H/M/L] | [H/M/L] | [H/M/L] | [Critical/High/Medium/Low] |

## 6. Remediation Roadmap

### Phase 1: Immediate (0-30 days)
- [Critical finding remediation items]

### Phase 2: Short-term (30-90 days)
- [High finding remediation items]

### Phase 3: Medium-term (90-180 days)
- [Medium finding remediation items]

### Phase 4: Long-term (6-12 months)
- [Architecture improvements and low findings]

## 7. Compliance Gap Analysis

### IEC 62443-3-3 Compliance

| Requirement | Status | Gap Description |
|------------|--------|----------------|
| SR 1.1 Human User IAC | [Met/Partial/Not Met] | [Gap detail] |
| SR 2.1 Authorization Enforcement | [Met/Partial/Not Met] | [Gap detail] |
| SR 3.1 Communication Integrity | [Met/Partial/Not Met] | [Gap detail] |
| SR 5.1 Network Segmentation | [Met/Partial/Not Met] | [Gap detail] |

## Appendices

### Appendix A: Complete Asset Inventory
[Detailed asset list with IPs, MACs, firmware versions, protocols]

### Appendix B: Network Diagrams
[Updated network topology diagrams showing discovered assets and flows]

### Appendix C: Firewall Rule Analysis Detail
[Complete firewall rule review with per-rule assessment]

### Appendix D: Tool Output
[Relevant tool output and packet captures]
