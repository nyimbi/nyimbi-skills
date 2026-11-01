---
name: network-and-wireless-security
description: >-
  Secure and monitor network infrastructure: segmentation with VLANs, firewall
  zones and ACLs; IDS/IPS with Suricata and Snort; traffic analysis with Zeek,
  Arkime, Wireshark, tshark, Scapy and NetFlow; NAC and 802.1X; next-generation
  firewall policy; DNS tunneling, C2 and exfiltration detection;
  lateral-movement detection; wireless assessment and hardening; DDoS
  mitigation; TLS inspection. Use when the user asks to "segment the network",
  "deploy Suricata/Zeek", "detect DNS exfiltration", "set up 802.1X",
  "baseline our network traffic", "find rogue access points", "stop lateral
  movement over SMB", or to validate a control with an authorized ARP spoofing,
  MITM, VLAN hopping or packet-injection simulation. Defensive by default:
  attack simulations exist here to prove a control works, under written
  authorization — not to compromise a target. Do not use for adversary
  emulation or gaining access (offensive-security-and-red-teaming), for
  hypothesis-driven hunting across endpoint and log sources
  (threat-hunting-and-detection), for TLS and cipher configuration
  (cryptography-and-key-management), or for industrial control networks
  (ot-ics-and-firmware-security).
license: Apache-2.0
---

# Network and Wireless Security

Network controls are the only layer that can enforce boundaries between things
you do not own (workloads, users, devices) — and they are the layer most often
configured as a diagram rather than tested as a control. This skill treats
every segmentation rule, IDS rule and NAC policy as a claim that must be
verified from both sides of the boundary it draws.

Simulation techniques in this skill (ARP spoofing, MITM, SSL stripping, VLAN
hopping, packet injection, IPv6 abuse, bandwidth throttling) are **validation
tests for controls you are authorized to test**. When the objective shifts to
emulating an adversary or gaining access, that is
`offensive-security-and-red-teaming`.

## When to use

- Designing or auditing network segmentation: VLANs, zones, ACLs, microsegmentation
- Deploying or tuning IDS/IPS: Suricata, Snort, custom rules, ET rulesets, EVE JSON
- Building network traffic analysis: Zeek logs, full packet capture (Arkime), NetFlow baselines
- Detecting scanning, ARP poisoning, lateral movement, DNS tunneling/exfiltration, and C2 beaconing from network data
- Enforcing identity at the port: 802.1X, RADIUS, MAB, dynamic VLAN assignment, posture assessment
- Hardening wireless: rogue AP detection, WPA2/WPA3 handshake and PSK strength, enterprise vs PSK decisions
- Validating controls with authorized attack simulations (MITM, SSL strip, VLAN hopping, packet injection, IPv6)
- Edge resilience: NGFW policy, TLS inspection, DDoS mitigation, BGP/RPKI, browser isolation

**Do not use for** — `offensive-security-and-red-teaming` when the goal is to
compromise a target or emulate a threat actor rather than verify a control;
`threat-hunting-and-detection` when the question is how to hunt across
endpoint, identity and log sources rather than what the network stack can see;
`cryptography-and-key-management` when the question is TLS protocol/cipher
configuration rather than whether to inspect traffic; `ot-ics-and-firmware-security`
for industrial protocols (Modbus, DNP3, S7) and plant networks.

## Workflow

1. **Fix scope, authorization, and change control.** Input: the request and
   the production network it will touch. Output: an agreed scope statement.
   For configuration work: name the change window, rollback plan, and the
   device owner. For any attack simulation (ARP spoofing, MITM, VLAN hopping,
   injection): obtain written authorization with target list, time box and
   stop conditions first. Confirm which links, VLANs, and SSIDs are in scope
   and which are explicitly excluded.

2. **Map what exists before changing it.** Input: diagrams (if any), switch
   and firewall configs, and a span-port capture. Output: an architecture map
   — zones/VLANs, subnets, inter-zone flows actually observed, choke points,
   existing controls, and IPv6/dual-stack reality. Where documentation
   disagrees with the traffic, the traffic wins; record the discrepancy as a
   finding.

3. **Design segmentation as an explicit flow matrix.** Input: the architecture
   map and business flows. Output: a zone → zone allow/deny matrix plus the
   rules that implement it. Give every zone a purpose (corporate, servers, DMZ,
   guest, IoT, management, quarantine), default-deny between zones, and pair it
   with Layer 2 hardening — DTP disabled, unused native VLAN, explicit trunk
   allow-lists, DHCP snooping, dynamic ARP inspection, port security, BPDU
   guard. Detail and switch configuration:
   [configuring-network-segmentation-with-vlans](references/configuring-network-segmentation-with-vlans.md),
   [implementing-network-segmentation-with-firewall-zones](references/implementing-network-segmentation-with-firewall-zones.md).

4. **Choose and place the monitoring stack.** Input: the flow matrix and
   choke points. Output: a placement plan — what each sensor sees and what it
   logs. Split the job: Zeek for protocol metadata and session logs, Suricata/
   Snort for signatures and inline blocking, Arkime when you need full PCAP
   retrieval, NetFlow/IPFIX where packets cannot be retained, Wireshark/
   tshark/Scapy for ad-hoc dissection. Selection criteria and what each tool
   misses are in
   [`references/monitoring-stack-selection.md`](references/monitoring-stack-selection.md).

5. **Deploy, baseline, and tune.** Input: the placement plan. Output: sensors
   producing validated telemetry. Disable NIC offloading, confirm promiscuous
   capture, load rulesets (ET Open via `suricata-update`), write local rules
   for environment-specific gaps, and establish a traffic baseline (hourly/
   daily patterns, z-score thresholds) before enabling alert thresholds.
   Tune against the baseline — disable noisy rules rather than learning to
   ignore alerts. Watch `kernel_drops`: a sensor that drops packets is not a
   sensor.

6. **Enforce access at the edge and the port.** Input: the flow matrix and
   device inventory. Output: identity-driven access plus edge controls.
   Deploy 802.1X with a RADIUS server, MAB for devices without supplicants,
   dynamic VLAN assignment, posture checks, and — non-negotiable — guest,
   quarantine, and critical VLAN fallback so a RADIUS outage does not take the
   network down. Add NGFW application/user policy, TLS inspection with a
   documented exemption list, DDoS protections, and BGP origin validation where
   you announce prefixes.

7. **Validate by attacking the control you just built.** Input: deployed
   controls and in-scope test conditions. Output: pass/fail evidence per
   control. From each zone, run the positive and negative reachability tests;
   from an authorized position, run the matching simulation — VLAN hopping
   against trunk hardening, ARP spoofing against DAI, MITM/SSL strip against
   HSTS and certificate validation, packet injection against IPS rules, IPv6
   RA abuse against dual-stack policy, port scanning against IDS signatures.
   The test matrix and pass criteria are in
   [`references/segmentation-and-attack-validation.md`](references/segmentation-and-attack-validation.md).
   Every failed control is a finding with a fix, not a reason to widen the rule.

8. **Report and hand over.** Input: test results, alert data, baselines.
   Output: the deliverable described below, plus the operational artifacts —
   rule inventory with owners, baseline thresholds, change/rollback runbook,
   and the detection coverage map showing which attack technique each control
   or rule addresses.

## Quality bar

- [ ] Change window, rollback plan, and device owner named for every production configuration change; simulations carry written authorization
- [ ] Zone/flow matrix exists with default-deny between zones; no `any any` permit remains unreviewed and justified
- [ ] Segmentation verified from both sides — allowed flows succeed, denied flows fail — with the test output attached
- [ ] Layer 2 hardening present: `switchport nonegotiate`, unused native VLAN, restricted trunk allowed-VLAN list, DHCP snooping, DAI, port security
- [ ] IDS/IPS sensors have offloading disabled, drops monitored (≈0 at peak), rules tuned against a real baseline, and at least one synthetic test alert proven end-to-end into the SIEM
- [ ] Every detection claims a specific technique and has been validated with a known-good test, not assumed from rule presence
- [ ] NAC assigns authenticated/guest/quarantine correctly and critical-VLAN fallback was tested by killing the RADIUS server
- [ ] Wireless: enterprise 802.1X vs PSK decision documented; PSK strength verified by offline cracking of handshakes captured only on scoped SSIDs; rogue/unknown AP detection running
- [ ] TLS inspection has a documented exemption list (health, finance, legal) and privacy review sign-off
- [ ] IPv6 and IPv4 policy parity confirmed — no shadow IPv6 path bypasses an IPv4 control

## Reference map

The complete catalog of merged techniques is in
[`references/technique-index.md`](references/technique-index.md). Load the file
for the component you are working on rather than reading the index end to end.

| Situation | Open |
|---|---|
| Choosing sensors and placement (Zeek vs Suricata vs Arkime vs NetFlow) | [monitoring-stack-selection](references/monitoring-stack-selection.md) |
| Test matrix and pass criteria for validating segmentation and controls | [segmentation-and-attack-validation](references/segmentation-and-attack-validation.md) |
| VLAN design, trunk hardening, inter-VLAN ACLs | [configuring-network-segmentation-with-vlans](references/configuring-network-segmentation-with-vlans.md) |
| Firewall zones, trust levels, PCI segmentation requirements | [implementing-network-segmentation-with-firewall-zones](references/implementing-network-segmentation-with-firewall-zones.md) |
| pfSense rules, NAT, VPN tunnels | [configuring-pfsense-firewall-rules](references/configuring-pfsense-firewall-rules.md) |
| Palo Alto NGFW: App-ID, User-ID, decryption, threat profiles | [implementing-next-generation-firewall-with-palo-alto](references/implementing-next-generation-firewall-with-palo-alto.md) |
| Suricata deployment: suricata.yaml, AF_PACKET, EVE JSON, rule management | [configuring-suricata-for-network-monitoring](references/configuring-suricata-for-network-monitoring.md) |
| Suricata as inline IPS with custom blocking rules | [implementing-network-intrusion-prevention-with-suricata](references/implementing-network-intrusion-prevention-with-suricata.md) |
| Snort 3 rulesets, preprocessors, alert output | [configuring-snort-ids-for-intrusion-detection](references/configuring-snort-ids-for-intrusion-detection.md) |
| Detecting Nmap/Masscan/custom scans with signatures and thresholds | [detecting-network-scanning-with-ids-signatures](references/detecting-network-scanning-with-ids-signatures.md) |
| Auto-banning scanners and SSH brute force with Fail2ban | [detecting-port-scanning-with-fail2ban](references/detecting-port-scanning-with-fail2ban.md) |
| Zeek deployment, custom scripts, anomaly detection | [detecting-network-anomalies-with-zeek](references/detecting-network-anomalies-with-zeek.md) · [performing-network-traffic-analysis-with-zeek](references/performing-network-traffic-analysis-with-zeek.md) |
| Lateral movement from Zeek logs (SMB admin shares, DCE/RPC, NTLM spray) | [detecting-lateral-movement-with-zeek](references/detecting-lateral-movement-with-zeek.md) · [detecting-lateral-movement-in-network](references/detecting-lateral-movement-in-network.md) |
| DNS tunneling, DGA, DNS C2 detection (entropy, beaconing, Zeek/Suricata rules) | [detecting-command-and-control-over-dns](references/detecting-command-and-control-over-dns.md) |
| DNS exfiltration via query analysis | [detecting-dns-exfiltration-with-dns-query-analysis](references/detecting-dns-exfiltration-with-dns-query-analysis.md) · [detecting-exfiltration-over-dns-with-zeek](references/detecting-exfiltration-over-dns-with-zeek.md) |
| Flow records: parsing NetFlow/IPFIX and anomaly detection | [analyzing-network-flow-data-with-netflow](references/analyzing-network-flow-data-with-netflow.md) |
| Statistical traffic baselines and z-score alerting | [implementing-network-traffic-baselining](references/implementing-network-traffic-baselining.md) |
| Packet capture and dissection: Wireshark, tshark, Scapy | [analyzing-network-traffic-with-wireshark](references/analyzing-network-traffic-with-wireshark.md) · [performing-network-traffic-analysis-with-tshark](references/performing-network-traffic-analysis-with-tshark.md) · [analyzing-network-packets-with-scapy](references/analyzing-network-packets-with-scapy.md) |
| Full packet capture search (Arkime sessions, PCAP export) | [implementing-network-traffic-analysis-with-arkime](references/implementing-network-traffic-analysis-with-arkime.md) |
| 802.1X/RADIUS NAC with dynamic VLAN and posture | [implementing-network-access-control](references/implementing-network-access-control.md) · [implementing-network-access-control-with-cisco-ise](references/implementing-network-access-control-with-cisco-ise.md) |
| TLS/SSL inspection on security devices (certificates, exemptions) | [performing-ssl-tls-inspection-configuration](references/performing-ssl-tls-inspection-configuration.md) |
| Server TLS/cipher/HSTS assessment (sslyze) | [performing-ssl-tls-security-assessment](references/performing-ssl-tls-security-assessment.md) |
| DDoS mitigation with Cloudflare (rulesets, rate limiting, origin protection) | [implementing-ddos-mitigation-with-cloudflare](references/implementing-ddos-mitigation-with-cloudflare.md) |
| Remote browser isolation for zero trust web access | [implementing-browser-isolation-for-zero-trust](references/implementing-browser-isolation-for-zero-trust.md) |
| BGP hijack simulation and RPKI route-origin validation | [exploiting-bgp-hijacking-vulnerabilities](references/exploiting-bgp-hijacking-vulnerabilities.md) · [implementing-bgp-security-with-rpki](references/implementing-bgp-security-with-rpki.md) |
| DNS enumeration and zone-transfer exposure | [performing-dns-enumeration-and-zone-transfer](references/performing-dns-enumeration-and-zone-transfer.md) |
| Authorized scanning and NSE scripting (Nmap) | [scanning-network-with-nmap-advanced](references/scanning-network-with-nmap-advanced.md) |
| ARP spoofing: attack simulation and detection | [performing-arp-spoofing-attack-simulation](references/performing-arp-spoofing-attack-simulation.md) · [detecting-arp-poisoning-in-network-traffic](references/detecting-arp-poisoning-in-network-traffic.md) |
| MITM and SSL-stripping validation of HSTS/cert checks | [conducting-man-in-the-middle-attack-simulation](references/conducting-man-in-the-middle-attack-simulation.md) · [performing-ssl-stripping-attack](references/performing-ssl-stripping-attack.md) |
| VLAN hopping and packet injection tests | [performing-vlan-hopping-attack](references/performing-vlan-hopping-attack.md) · [performing-packet-injection-attack](references/performing-packet-injection-attack.md) |
| IPv6 dual-stack abuse (SLAAC, RA flooding, tunnels) | [exploiting-ipv6-vulnerabilities](references/exploiting-ipv6-vulnerabilities.md) |
| Bandwidth throttling / traffic-manipulation simulation | [performing-bandwidth-throttling-attack-simulation](references/performing-bandwidth-throttling-attack-simulation.md) |
| SMB exploitation against unpatched hosts (validation only) | [exploiting-smb-vulnerabilities-with-metasploit](references/exploiting-smb-vulnerabilities-with-metasploit.md) |
| Wireless survey: rogue APs, hidden SSIDs, weak encryption | [performing-wireless-security-assessment-with-kismet](references/performing-wireless-security-assessment-with-kismet.md) |
| WPA handshake capture and offline PSK cracking | [performing-wifi-password-cracking-with-aircrack](references/performing-wifi-password-cracking-with-aircrack.md) |
| Bluetooth/BLE assessment and attack detection | [performing-bluetooth-security-assessment](references/performing-bluetooth-security-assessment.md) · [detecting-bluetooth-low-energy-attacks](references/detecting-bluetooth-low-energy-attacks.md) |

Executable helpers for each technique live in `scripts/<technique-name>/` —
read the reference file first to learn what the script expects, then run it.

## Output format

For design, deployment, or validation work, deliver:

```markdown
# <Network / Segment> — Security Design and Validation

## Scope and authorization
In-scope segments, SSIDs, devices; change window and rollback plan; simulation
authorization if any test traffic was sent.

## Current state
Architecture map: zones, VLANs, subnets, observed inter-zone flows, controls in
place, documentation discrepancies found.

## Target design
Zone/flow matrix: from → to → allowed services → enforced by (rule/ACL/port).

## Implementation
Per-device changes with before/after config excerpts and rollback commands.

## Validation results
| Control | Test | Expected | Observed | Pass/Fail |

## Detection coverage
Attack technique → sensor/log source → rule → validated how (test evidence).

## Findings
Ordered by severity: what is exposed, where, and the concrete fix.

## Operations handover
Rule inventory with owners, baseline thresholds, tuning log, and monitoring
dashboard/alert references.
```

For a control-validation run, the validation-results table is the core of the
deliverable — every row must carry observed output, not an assertion.
