---
name: ot-ics-and-firmware-security
description: >-
  Secure industrial control systems and the firmware beneath them: Purdue model
  and IEC 62443 zone/conduit segmentation, OT asset discovery and safe
  vulnerability assessment (Claroty, passive monitoring, Tenable OT), SCADA/DCS
  monitoring with Dragos and Nozomi, Modbus/DNP3/S7comm anomaly detection,
  historian protection, OT patch management and incident response, NERC CIP,
  sector assessments (power grid, oil and gas), and firmware/boot-chain
  analysis — binwalk extraction, PLC firmware review, UEFI and CHIPSEC
  auditing, EFI System Partition hunting, Secure Boot bypass detection, TPM
  measured boot attestation. Use when the user asks to "segment the plant
  network", "scan OT without breaking anything", "detect Modbus anomalies",
  "build an IEC 62443 zone model", "analyze this firmware dump", "is Secure
  Boot actually enforcing", or to assess a SCADA, HMI, substation, or pipeline
  environment. Safety outranks confidentiality: no active scanning, writes,
  logic changes, or denial-of-service against running process control without
  change-control approval and a rollback plan; safety instrumented systems are
  off-limits. Do not use for enterprise network controls
  (network-and-wireless-security), IT vulnerability management programs
  (vulnerability-management-and-compliance), or enterprise incident response
  (security-incident-response-and-soc).
license: Apache-2.0
---

# OT/ICS and Firmware Security

Two trust bottoms, one discipline: the physical process and the boot chain.
Both fail differently from IT — a wrong write can stop a plant or a patient
support system, and a compromised boot loader defeats every control above it.
Both therefore share the same working rule: **verify before you touch, prefer
passive evidence, and never trade safety for confidentiality.**

This skill covers plant/SCADA/DCS security and firmware analysis. IT/enterprise
network controls are `network-and-wireless-security`; enterprise vulnerability
programs are `vulnerability-management-and-compliance`.

## When to use

- Designing or auditing OT segmentation: Purdue levels, IEC 62443 zones and conduits, data diodes, industrial firewalls
- OT asset inventory and vulnerability assessment done safely: passive discovery, native-protocol queries, controlled scanning (Claroty, Nozomi, Tenable OT)
- SCADA/DCS monitoring: Dragos, Nozomi Guardian, Zeek/Suricata with OT rules, Modbus/DNP3/S7comm anomaly detection, historian attack detection
- Assessing control-system environments: SCADA HMI, substation/power grid, oil and gas pipelines, process control networks
- OT-specific operations: patch management with vendor testing, remote-access conduits, incident response playbooks, NERC CIP controls
- Firmware analysis: binwalk extraction, embedded credential hunting, PLC firmware review, UEFI/CHIPSEC platform audit, ESP forensics, Secure Boot and TPM attestation

**Do not use for** — `network-and-wireless-security` when the target is
enterprise IT network controls (VLANs, 802.1X, IDS for corporate traffic) even
though the tooling overlaps; `vulnerability-management-and-compliance` for
enterprise-wide CVE/SLA programs and audit reporting; `security-incident-response-and-soc`
for IT SOC triage and enterprise IR; `malware-analysis-and-reverse-engineering`
when the artifact is a standalone malware sample rather than device firmware
in situ.

## Workflow

1. **Pass the safety and authorization gate.** Input: the request and the
   environment it will touch. Output: a signed-off test plan. Before any
   active traffic: name the change window, the responsible operator, the
   rollback procedure, and the stop signal. Passive monitoring and lab/test-bed
   analysis are preferred by default. Safety instrumented systems (SIS),
   emergency stops, and life-safety equipment are out of scope for active
   testing, always. Denial-of-service, protocol fuzzing, CPU stop commands,
   and logic writes run only against lab replicas or vendor-approved test
   fixtures. Record this gate first — it is the difference between an
   assessment and an incident. Method detail:
   [performing-ot-vulnerability-scanning-safely](references/performing-ot-vulnerability-scanning-safely.md)
   and [`references/ot-safety.md`](references/ot-safety.md).

2. **Inventory from passive evidence.** Input: a span port or passive sensor
   at the IT/OT boundary and inside the plant. Output: an asset register —
   PLCs, RTUs, HMIs, historians, engineering workstations, network devices —
   each with Purdue level, IP/MAC, protocol (Modbus, DNP3, S7comm, EtherNet/IP,
   OPC UA), firmware version where observable, and vendor/CVE correlation.
   Passive discovery first; active queries only with native protocol reads
   approved in step 1.
   [performing-ics-asset-discovery-with-claroty](references/performing-ics-asset-discovery-with-claroty.md).

3. **Model zones and conduits before drawing firewall rules.** Input: the
   asset register and process-dependency map. Output: a zone/conduit design
   with Security Level targets — Purdue L0–L5 partitioning, IT/OT boundary,
   engineering network, SIS isolated, historian treated as a boundary system,
   every conduit with a named control (firewall, data diode, jump server).
   [implementing-purdue-model-network-segmentation](references/implementing-purdue-model-network-segmentation.md),
   [implementing-iec-62443-security-zones](references/implementing-iec-62443-security-zones.md),
   [implementing-network-segmentation-for-ot](references/implementing-network-segmentation-for-ot.md).

4. **Place protocol-aware monitoring.** Input: the zone design and span
   points. Output: sensors producing OT-native telemetry. Deploy Dragos or
   Nozomi for asset/protocol visibility and detection analytics, or Zeek/
   Suricata with OT rules where platform coverage is not justified; baseline
   normal PLC polling, function codes, and register ranges so unauthorized
   writes, rogue clients, and timing deviations alert.
   [implementing-dragos-platform-for-ot-monitoring](references/implementing-dragos-platform-for-ot-monitoring.md),
   [implementing-ot-network-traffic-analysis-with-nozomi](references/implementing-ot-network-traffic-analysis-with-nozomi.md),
   [detecting-modbus-protocol-anomalies](references/detecting-modbus-protocol-anomalies.md),
   [detecting-dnp3-protocol-anomalies](references/detecting-dnp3-protocol-anomalies.md).

5. **Assess risk on OT terms.** Input: inventory plus platform findings.
   Output: a prioritized risk register where operational impact outranks CVSS.
   Correlate passive findings with ICS-CERT/vendor advisories, validate with
   approved native-protocol reads, and assess the human-facing control layer
   (SCADA HMI web stacks, thin clients, engineering tools) and protocol
   weaknesses (S7comm replay/download manipulation, Modbus injection paths).
   [performing-ot-vulnerability-assessment-with-claroty](references/performing-ot-vulnerability-assessment-with-claroty.md),
   [performing-scada-hmi-security-assessment](references/performing-scada-hmi-security-assessment.md),
   [performing-s7comm-protocol-security-analysis](references/performing-s7comm-protocol-security-analysis.md).
   For electric or pipeline environments, apply the sector overlay:
   [performing-power-grid-cybersecurity-assessment](references/performing-power-grid-cybersecurity-assessment.md),
   [performing-oil-gas-cybersecurity-assessment](references/performing-oil-gas-cybersecurity-assessment.md),
   [implementing-nerc-cip-compliance-controls](references/implementing-nerc-cip-compliance-controls.md).

6. **Remediate the way OT allows.** Input: the risk register. Output: fixes
   that are either applied or explicitly compensated. Patches follow vendor
   compatibility testing, staged deployment, and maintenance windows — never
   auto-rollout; where patching is impossible, document the compensating
   control (conduit restriction, monitoring rule, virtual patch) and its
   owner. Remote access moves to a recorded, MFA-gated conduit.
   [implementing-patch-management-for-ot-systems](references/implementing-patch-management-for-ot-systems.md),
   [implementing-conduit-security-for-ot-remote-access](references/implementing-conduit-security-for-ot-remote-access.md),
   [securing-remote-access-to-ot-environment](references/securing-remote-access-to-ot-environment.md),
   [securing-historian-server-in-ot-environment](references/securing-historian-server-in-ot-environment.md).

7. **When firmware or boot integrity is in scope, take the firmware path.**
   Input: a firmware image (vendor download or lab dump) or an endpoint whose
   boot chain is suspect. Output: an extraction report and verified findings.
   Extract with binwalk (entropy → nested filesystems → strings for
   credentials), analyze PLC firmware for hardcoded secrets and update
   weaknesses, and for PC/UEFI platforms audit SPI flash and Secure Boot
   state with CHIPSEC, hunt the EFI System Partition, verify against known
   bypasses (DBX revocations), and validate TPM measured-boot attestation.
   Path selection, tool order, and which finding each step can prove are in
   [`references/firmware-analysis-paths.md`](references/firmware-analysis-paths.md).

8. **Validate detection and hand over a response path.** Input: deployed
   controls and monitoring. Output: test evidence plus an OT incident
   playbook. Validate detections with known-good test traffic (replay captured
   benign frames, inject a controlled function-code anomaly on a lab link),
   not by asserting rule presence. Confirm the playbook coordinates the IT SOC,
   OT engineering, and plant operations with roles for shutdown decisions,
   and rehearse at tabletop level. Detection classes worth covering: SCADA
   attack patterns, Stuxnet-style logic modification with sensor spoofing,
   historian compromise, process anomalies against physics/protocol baselines.
   [implementing-ot-incident-response-playbook](references/implementing-ot-incident-response-playbook.md),
   [detecting-stuxnet-style-attacks](references/detecting-stuxnet-style-attacks.md),
   [detecting-attacks-on-historian-servers](references/detecting-attacks-on-historian-servers.md).

## Quality bar

- [ ] **Safety gate passed before any active traffic**: change control, rollback, stop signal, and scope signed off; SIS/life-safety explicitly excluded; passive or lab-first method chosen and justified
- [ ] No denial-of-service, fuzzing, CPU stop, logic write, or firmware flash was attempted against production — lab evidence cited where such tests exist
- [ ] Asset register covers every discovered device with Purdue level, protocol, firmware version, and owner; unmanaged/unknown devices are findings, not silent gaps
- [ ] Zone/conduit design maps each IT/OT crossing to a named control; historian and engineering workstations are treated as boundary systems; every conduit has an enforcement point
- [ ] Vulnerability findings carry operational impact and compensating controls — CVSS alone never drives an OT remediation priority
- [ ] Patch decisions document vendor compatibility testing, maintenance window, and rollback; unpatched items name their compensating control and review date
- [ ] Remote access runs through the conduit (MFA, session recording, approval workflow) — no direct VPN-to-plant path remains
- [ ] Detection rules were validated with known-good test traffic and alert output captured; rule presence without test evidence does not count
- [ ] Firmware findings are reproducible: image hash, extraction output, and the exact evidence (config, string, binary diff) recorded; Secure Boot/TPM claims cite current DBX/PCR state
- [ ] OT incident playbook exists, names shutdown-decision authority, and has been walked through with OT engineering and plant operations

## Reference map

The complete catalog of merged techniques is in
[`references/technique-index.md`](references/technique-index.md). Load the file
for the component you are working on rather than reading the index end to end.

| Situation | Open |
|---|---|
| Safety rules, pre-test checklist, lab vs production decision | [ot-safety](references/ot-safety.md) |
| Which firmware analysis path to take (image vs device vs boot chain) | [firmware-analysis-paths](references/firmware-analysis-paths.md) |
| Safe scanning method: passive first, native reads, controlled active | [performing-ot-vulnerability-scanning-safely](references/performing-ot-vulnerability-scanning-safely.md) |
| OT asset discovery and visibility (Claroty xDome, Edge queries) | [performing-ics-asset-discovery-with-claroty](references/performing-ics-asset-discovery-with-claroty.md) |
| Passive vulnerability assessment and risk scoring | [performing-ot-vulnerability-assessment-with-claroty](references/performing-ot-vulnerability-assessment-with-claroty.md) |
| Full OT network assessment methodology (Purdue, IT/OT convergence, protocol audit) | [performing-ot-network-security-assessment](references/performing-ot-network-security-assessment.md) |
| Purdue-level segmentation design and migration from flat networks | [implementing-purdue-model-network-segmentation](references/implementing-purdue-model-network-segmentation.md) |
| IEC 62443 zones/conduits with Security Level targets | [implementing-iec-62443-security-zones](references/implementing-iec-62443-security-zones.md) |
| OT segmentation with VLANs, diodes, SDN and OT-aware firewalls | [implementing-network-segmentation-for-ot](references/implementing-network-segmentation-for-ot.md) |
| Industrial firewall deployment for Modbus/EtherNet/IP/OPC/S7comm | [implementing-ics-firewall-with-tofino](references/implementing-ics-firewall-with-tofino.md) |
| OT monitoring platform (Dragos analytics, threat-group playbooks) | [implementing-dragos-platform-for-ot-monitoring](references/implementing-dragos-platform-for-ot-monitoring.md) |
| Passive OT traffic analysis (Nozomi Guardian sensors) | [implementing-ot-network-traffic-analysis-with-nozomi](references/implementing-ot-network-traffic-analysis-with-nozomi.md) |
| Modbus function-code/register baselines and anomaly detection | [detecting-modbus-protocol-anomalies](references/detecting-modbus-protocol-anomalies.md) · [monitoring-scada-modbus-traffic-anomalies](references/monitoring-scada-modbus-traffic-anomalies.md) |
| Detecting unauthorized Modbus write/command injection | [detecting-modbus-command-injection-attacks](references/detecting-modbus-command-injection-attacks.md) |
| DNP3 control-command and protocol-violation detection | [detecting-dnp3-protocol-anomalies](references/detecting-dnp3-protocol-anomalies.md) |
| SCADA attack detection: MITM, command injection, HMI compromise, DoS | [detecting-attacks-on-scada-systems](references/detecting-attacks-on-scada-systems.md) |
| ML/physics-based ICS anomaly detection and process correlation | [detecting-anomalies-in-industrial-control-systems](references/detecting-anomalies-in-industrial-control-systems.md) |
| Stuxnet-pattern detection: PLC logic modification + sensor spoofing | [detecting-stuxnet-style-attacks](references/detecting-stuxnet-style-attacks.md) |
| Historian attack detection (data manipulation, unauthorized queries) | [detecting-attacks-on-historian-servers](references/detecting-attacks-on-historian-servers.md) |
| Hardening the historian at the IT/OT boundary | [securing-historian-server-in-ot-environment](references/securing-historian-server-in-ot-environment.md) |
| SCADA HMI assessment (web stacks, thin clients, HMI↔PLC channels) | [performing-scada-hmi-security-assessment](references/performing-scada-hmi-security-assessment.md) |
| S7comm/S7CommPlus analysis: replay, integrity bypass, CPU stop, download manipulation | [performing-s7comm-protocol-security-analysis](references/performing-s7comm-protocol-security-analysis.md) |
| Patch management with vendor testing, staging, rollback, compensating controls | [implementing-patch-management-for-ot-systems](references/implementing-patch-management-for-ot-systems.md) |
| Secure remote access: conduits, jump servers, MFA, session recording | [implementing-conduit-security-for-ot-remote-access](references/implementing-conduit-security-for-ot-remote-access.md) · [securing-remote-access-to-ot-environment](references/securing-remote-access-to-ot-environment.md) |
| OT incident response playbook (PICERL, IT SOC ↔ OT engineering ↔ ops) | [implementing-ot-incident-response-playbook](references/implementing-ot-incident-response-playbook.md) |
| NERC CIP controls (CIP-002/005/007/010/013, MFA for remote access) | [implementing-nerc-cip-compliance-controls](references/implementing-nerc-cip-compliance-controls.md) |
| Power grid assessment (substations, IEC 61850, PMU, Industroyer-class threats) | [performing-power-grid-cybersecurity-assessment](references/performing-power-grid-cybersecurity-assessment.md) |
| Oil and gas assessment (pipelines, RTUs, API 1164, TSA directives) | [performing-oil-gas-cybersecurity-assessment](references/performing-oil-gas-cybersecurity-assessment.md) |
| Firmware extraction: entropy, nested filesystems, embedded secrets | [performing-firmware-extraction-with-binwalk](references/performing-firmware-extraction-with-binwalk.md) |
| PLC firmware review (hardcoded credentials, update flaws, debug interfaces) | [performing-plc-firmware-security-analysis](references/performing-plc-firmware-security-analysis.md) |
| Platform firmware audit: SPI flash, BIOS lock, SMM, Secure Boot state | [auditing-uefi-firmware-with-chipsec](references/auditing-uefi-firmware-with-chipsec.md) |
| UEFI bootkit persistence analysis (BlackLotus, LoJax, MoonBounce…) | [analyzing-uefi-bootkit-persistence](references/analyzing-uefi-bootkit-persistence.md) |
| EFI System Partition baseline and bootkit hunting | [hunting-bootkits-in-efi-system-partition](references/hunting-bootkits-in-efi-system-partition.md) |
| Secure Boot bypass detection (DBX, known bypass binaries) | [detecting-secure-boot-bypass](references/detecting-secure-boot-bypass.md) |
| TPM measured boot attestation validation | [validating-tpm-measured-boot-attestation](references/validating-tpm-measured-boot-attestation.md) |

Executable helpers for each technique live in `scripts/<technique-name>/` —
read the reference file first to learn what the script expects, then run it.

## Output format

For OT assessments, designs, and firmware reviews, deliver:

```markdown
# <Facility / Device / Firmware> — <Assessment|Design|Analysis>

## Authorization and safety record
Change-control reference, maintenance window, rollback plan, stop signal,
SIS/life-safety exclusions, passive-first justification.

## Scope and method
In-scope zones/levels/devices; methods used (passive / native read / active)
and methods deliberately not used, with reason.

## Asset and architecture view
Asset register (device, vendor/model, firmware, Purdue level, protocol) and
zone/conduit map of what exists today.

## Findings
Ordered by safety impact first, then exploitability, then compliance:
observation → evidence (log line, capture, hash, extracted artifact) →
process/safety consequence → remediation or compensating control → owner.

## Detection coverage
Technique → sensor/log source → rule/analytics → validated how (test evidence).

## Validation results
| Control | Test | Expected | Observed | Pass/Fail |

## Remediation plan by window
What ships in the next maintenance window, what needs vendor coordination,
what stays compensated — each with a review date.

## Response handover
Playbook reference, shutdown-decision authority, contacts, tabletop findings.
```

For firmware-only work, the safety record is replaced by provenance: source
of the image, exact SHA-256, extraction environment, and the tool versions
used, so every finding can be re-derived by the next analyst.
