# Hunt Data Source and Tool Matrix

Purpose: choose the telemetry that can prove or refute a hypothesis,
and the tool that queries it fastest, before writing any query.

## Telemetry → question → tool

| Telemetry | Questions it can answer | Collection | Query tool | Technique files |
|---|---|---|---|---|
| Windows Security EVTX (4624/4625/4648/4662/4688/4768/4769/4771/5136/7045) | Who logged on where, with what credential type; directory changes; service installs | WEF, Splunk UF, Defender | Splunk SPL, KQL, Chainsaw, Hayabusa | [detecting-lateral-movement-with-splunk](detecting-lateral-movement-with-splunk.md) · [hunting-evtx-with-chainsaw](hunting-evtx-with-chainsaw.md) |
| Sysmon (1/3/7/8/10/11/13/19/20/21) | Process lineage, network mapping, cross-process access, registry writes, WMI subscriptions | Sysmon + WEF | Splunk, Elastic EQL, Velociraptor VQL | [detecting-t1055-process-injection-with-sysmon](detecting-t1055-process-injection-with-sysmon.md) · [detecting-wmi-persistence](detecting-wmi-persistence.md) |
| PowerShell Script Block / Module logging (4103/4104) | Encoded commands, AMSI bypass, download cradles, Empire artifacts | GPO + WEF | Splunk, Chainsaw search | [hunting-for-anomalous-powershell-execution](hunting-for-anomalous-powershell-execution.md) · [analyzing-powershell-empire-artifacts](analyzing-powershell-empire-artifacts.md) |
| EDR process telemetry | Fleet-wide process, file, and registry events with lineage | CrowdStrike / MDE / SentinelOne | KQL advanced hunting, Falcon queries, VQL | [detecting-credential-dumping-techniques](detecting-credential-dumping-techniques.md) |
| Zeek conn.log / dns.log / ssl.log | Beaconing regularity, DNS tunneling, JA3/JA4, rare destinations | Zeek sensor | RITA, Python/pandas, Splunk | [hunting-for-beaconing-with-frequency-analysis](hunting-for-beaconing-with-frequency-analysis.md) · [hunting-for-dns-tunneling-with-zeek](hunting-for-dns-tunneling-with-zeek.md) |
| Proxy / firewall logs | Domain fronting (SNI vs Host), cloud-storage uploads, non-standard ports | Forwarder | Splunk, Elastic | [hunting-for-domain-fronting-c2-traffic](hunting-for-domain-fronting-c2-traffic.md) · [hunting-for-data-exfiltration-indicators](hunting-for-data-exfiltration-indicators.md) |
| AD replication / Kerberos events | DCSync, golden ticket, pass-the-ticket, Kerberoasting | DC event logs | Splunk, Elastic, Impacket checks | [hunting-for-dcsync-attacks](hunting-for-dcsync-attacks.md) · [detecting-golden-ticket-attacks-in-kerberos-logs](detecting-golden-ticket-attacks-in-kerberos-logs.md) |
| Cloud audit logs (CloudTrail, Entra/Graph, GCP Audit) | Living off the cloud, token abuse, recon, privilege changes | Native + SIEM ingest | KQL, Splunk, Athena | [hunting-for-living-off-the-cloud-techniques](hunting-for-living-off-the-cloud-techniques.md) · [detecting-entra-offensive-tools-in-graph-logs](../../security-incident-response-and-soc/references/detecting-entra-offensive-tools-in-graph-logs.md) |
| Files on disk / shares / memory images | Known-bad content, packing, injected code, family matching | Agent sweep, share mount, memdump | YARA, yara-python | [performing-threat-hunting-with-yara-rules](performing-threat-hunting-with-yara-rules.md) |
| Email gateway and mailbox audit | Campaign scope, forwarding rules, token abuse | Message trace, Graph audit | Splunk, Graph API | [hunting-for-spearphishing-indicators](hunting-for-spearphishing-indicators.md) · [detecting-email-forwarding-rules-attack](detecting-email-forwarding-rules-attack.md) |
| Deception tokens (honeyfiles, honey credentials, canary buckets) | Did anyone touch something no legitimate user should? | Canarytokens, Thinkst, cloud decoys | Webhook/SIEM alert | [deploying-honeytokens-and-canarytokens](deploying-honeytokens-and-canarytokens.md) · [deploying-cloud-deception-with-decoy-resources](deploying-cloud-deception-with-decoy-resources.md) |
| UEBA / identity baselines | Deviation from a user's or peer group's norm | SIEM analytics | Elastic aggregations, Splunk | [detecting-insider-threat-with-ueba](detecting-insider-threat-with-ueba.md) |

## Live vs offline routing

| Situation | Use | Why |
|---|---|---|
| Fleet-wide hunt across managed endpoints | Velociraptor VQL | Parallel collection with query-at-endpoint results |
| Collected EVTX folder, air-gapped VM, no SIEM | Chainsaw + SigmaHQ rules | Single binary, offline, seconds to results |
| Historical search over months of normalized data | Splunk / Elastic / Sentinel | Data is already ingested and indexed |
| Files, shares, quarantine, memory dumps | YARA | Pattern matching without execution |
| Correlating many sources into one narrative | Timeline tools (Plaso, Timesketch) | Cross-source ordering — see ../digital-forensics-and-evidence/references/performing-timeline-reconstruction-with-plaso.md |

## Rules

- Verify the data source is actually collecting (source count over the
  window) before trusting a negative result; log the gap instead.
- Baseline first: peer group or rolling 30-day window per user/host,
  then score deviation — never flag on a single event where a baseline
  exists.
- One hypothesis, one time window, one scope; widen only after the
  first pass returns a candidate.
- Thresholds travel with the query: record the exact values (jitter,
  entropy, count floors) in the hunt record so results reproduce.
