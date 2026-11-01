# Monitoring Stack Selection

Purpose: decide which network sensors to deploy, where to place them, and what
each one cannot see — before buying or building anything.

## Tool roles

| Tool | What it produces | Best placement | Blind spots |
|---|---|---|---|
| Zeek | Structured session/protocol logs (`conn`, `dns`, `ssl`, `smb_mapping`, `dce_rpc`, `kerberos`, `ntlm`, custom scripts → `notice.log`) | SPAN/tap on internal core + IT/OT boundaries | no payloads for deep inspection; encrypted SMB3 file contents invisible; sees only what the tap carries |
| Suricata | Signature alerts + EVE JSON (http/dns/tls/files/flow/netflow), optional inline blocking, JA3/HASSH | Internet egress, DMZ, internal choke points | signature-dependent; needs tuning to survive production traffic; drops under-sized at peak |
| Snort 3 | Signature alerts, preprocessors, alert plugins | Where an existing Snort ops model exists | same signature/tuning economics as Suricata, single-threaded heritage in older deployments |
| Arkime (Moloch) | Indexed sessions + full PCAP retrieval | Span of high-value segments where PCAP retention is affordable | storage-heavy; content still encrypted without TLS interception |
| NetFlow/IPFIX | Flow records for baselines and volumetric anomalies | Everywhere packet capture is impossible (wan links, SPAN exhaustion) | no payload, no protocol depth; sampling loses low-and-slow |
| Wireshark / tshark | Ad-hoc dissection, field extraction, protocol stats | Investigation, validation tests, one-off captures | operator-driven; not a continuous sensor |
| Scapy | Craft/send/sniff custom packets | Validation tests, protocol experimentation | needs authorization; not a monitoring platform |
| Fail2ban | Host-level auto-ban on log patterns | Individual exposed hosts (SSH, scanners) | host-local view only |

## Placement decision

1. **Put a full-visibility sensor where you enforce.** The choke point that
   carries filtered traffic (NGFW span, core trunk) sees both what was allowed
   and what was attempted — enforcement and detection then correlate.
2. **Separate metadata from payloads.** Zeek answers "who talked to whom, when,
   how often"; Suricata answers "did this match a known bad pattern"; Arkime
   answers "show me the bytes". Design for all three questions or accept which
   ones you cannot answer.
3. **One span, many consumers.** Where SPAN ports are scarce, tap once and
   fan out; never let sensor outages compete for the same oversubscribed span.
4. **Baseline before alerting.** Volume and threshold rules derived from a
   1–2 week baseline (see [implementing-network-traffic-baselining](implementing-network-traffic-baselining.md))
   survive contact with production; imported thresholds do not.
5. **Enable Community ID** across Suricata/Zeek/PCAP tools so one flow can be
   correlated across stacks without manual IP translation.

## Capability ↔ technique file

| Question to answer | Primary tool | Technique file |
|---|---|---|
| Who connected where, and is it anomalous? | Zeek / NetFlow | [detecting-network-anomalies-with-zeek](detecting-network-anomalies-with-zeek.md), [analyzing-network-flow-data-with-netflow](analyzing-network-flow-data-with-netflow.md) |
| Is someone scanning us right now? | Suricata/Snort thresholds | [detecting-network-scanning-with-ids-signatures](detecting-network-scanning-with-ids-signatures.md) |
| Did an internal host move laterally? | Zeek SMB/DCE/RPC/NTLM logs | [detecting-lateral-movement-with-zeek](detecting-lateral-movement-with-zeek.md) |
| Is DNS being used for C2 or exfiltration? | Zeek dns.log + Suricata rules | [detecting-command-and-control-over-dns](detecting-command-and-control-over-dns.md), [detecting-exfiltration-over-dns-with-zeek](detecting-exfiltration-over-dns-with-zeek.md) |
| What exactly was in that session? | Arkime / PCAP | [implementing-network-traffic-analysis-with-arkime](implementing-network-traffic-analysis-with-arkime.md) |
| Do we block it, or just alert? | Suricata inline / NGFW | [implementing-network-intrusion-prevention-with-suricata](implementing-network-intrusion-prevention-with-suricata.md) |

## Non-negotiable deployment checks

- NIC offloading (GRO/LRO/TSO/GSO) disabled on every capture interface;
  incorrect checksums silently defeat signatures.
- `kernel_drops` (Suricata stats) and Zeek packet loss watched at peak, not
  just at install time.
- Ruleset inventory owned and version-controlled; disabled rules documented
  with a reason, not deleted.
- Every sensor's clock NTP-synced — correlation across tools fails otherwise.
