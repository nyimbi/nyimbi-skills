---
name: threat-hunting-and-detection
description: >-
  Proactively search the environment for adversary activity that no alert
  fired on, then turn what you find into durable detection content.
  Covers hypothesis-driven hunting, C2 beaconing and DNS-tunneling
  analysis, persistence and credential-abuse hunts (Kerberoasting,
  DCSync, pass-the-ticket, process injection, LOLBins), fleet-wide
  hunting with Velociraptor and Chainsaw, YARA and Sigma rule authoring,
  ATT&CK coverage gap analysis, UEBA baselines, and deception tripwires
  (honeytokens, canary tokens, MITRE Engage). Use when the user asks to
  "hunt for C2 beaconing", "find persistence across our Windows fleet",
  "write a Sigma rule for", "detect lateral movement", "how covered are
  we against ATT&CK", "deploy honeytokens", "is there a webshell on our
  servers", or "build detection content for Kerberoasting". Do not use
  for responding to alerts or containing a live compromise (see
  security-incident-response-and-soc), for acquiring evidence and
  building timelines (see digital-forensics-and-evidence), or for
  dissecting a malware sample (see malware-analysis-and-reverse-
  engineering).
license: Apache-2.0
---

# Threat Hunting and Detection

Hunting earns its keep only when it closes a loop: a testable hypothesis
becomes queries, queries become validated findings, and findings become
detections that fire without a human. A hunt that ends with "nothing
found" and no recorded hypothesis, data sources, and time window is
indistinguishable from not having hunted — document it anyway, because
coverage you have proven absent is coverage you no longer need to worry
about.

Two failure modes dominate this discipline: hunting with no hypothesis
(boiling the ocean until a hit appears by luck) and promoting findings to
detections without validating them (manufacturing tomorrow's false
positives). Both are quality-bar failures below.

## When to use

- Turning threat intel, an ATT&CK coverage gap, or an anomaly into a
  testable hunt with a defined data source and time window
- Searching for C2 beaconing, DNS tunneling, domain fronting, or
  unusual outbound connections in network metadata
- Hunting Windows/Linux persistence: registry run keys, scheduled
  tasks, WMI subscriptions, services, startup folders, DNS persistence
- Hunting credential abuse and directory attacks: Kerberoasting,
  DCSync, golden/silver tickets, pass-the-hash/ticket, NTLM relay,
  credential dumping, service-account abuse
- Hunting LOLBin and living-off-the-cloud execution, process injection,
  process hollowing, privilege escalation, timestomping, web shells,
  and data staging or exfiltration before it completes
- Fleet-scale hunting with Velociraptor VQL, Chainsaw over collected
  EVTX, or YARA over files and memory
- Authoring and validating Sigma/YARA detection rules, measuring ATT&CK
  coverage, and building UEBA baselines for insider threats
- Seeding or operating deception — honeytokens, canary tokens, honeypots
  — as high-fidelity detection tripwires

**Do not use for** — `security-incident-response-and-soc` when an alert
or incident already exists and the job is to classify, contain, and
recover — hunting stops at validated findings and hands off rather than
containing; `digital-forensics-and-evidence` when the job is
forensically sound acquisition, artifact parsing, or timeline
reconstruction of a known event; `malware-analysis-and-reverse-
engineering` when a sample has been handed to you and the question is
what it does. Detection content for application, API, or cloud
misconfiguration belongs to `application-api-mobile-and-ai-security` and
`cloud-container-and-devsecops-security`.

## Workflow

1. **Frame a falsifiable hypothesis.** Input: threat intel, an ATT&CK
   technique gap, an anomaly from UEBA, or a sector-wide campaign.
   Write it as: *<actor or technique> is doing <activity> on <data
   source> in <scope> within <window>, evidenced by <observable>; the
   hypothesis is refuted if <condition>.* Output: a hunt record with
   ID, technique IDs, scope, and success/refutation criteria.

2. **Select data sources, baselines, and tripwires.** Map each
   observable to telemetry that actually exists (Sysmon 1/3/8/10/11/13
   and 19–21, Windows Security 4624/4648/4662/4768/4769/4771/5136/
   7045, Script Block 4104, Zeek conn.log/dns.log, proxy, DNS, cloud
   audit logs), establish the normal baseline (30-day per-user or
   per-host, plus peer groups), and note any deception token that would
   fire on this activity. Output: data-source list with coverage
   status and baseline definition.

3. **Execute queries at fleet scale.** Write the queries in the
   platform's language — SPL, KQL, VQL, Chainsaw search, YARA — and
   run them over the defined window; keep every query verbatim in the
   hunt record. Output: raw result set with counts.

4. **Triage and correlate.** Apply the technique's decision rules
   rather than eyeballing: beaconing needs ≥50 connections with
   coefficient of variation <0.20 and mean interval between 30s and
   24h; DNS tunneling needs query-name entropy and subdomain length
   outliers; LSASS access needs `GrantedAccess` 0x1010/0x1FFFFF from a
   non-standard caller; WMI persistence needs Sysmon 19→20→21 bindings
   that survive cross-referencing SCCM/AV-known-good subscriptions.
   Correlate endpoint, network, and identity evidence for each hit.
   Output: candidate findings ranked by confidence.

5. **Validate and scope.** For each candidate, confirm context (is the
   process/parent/user relationship actually abnormal for this asset?),
   test against a known-good population, and decide true positive /
   false positive / inconclusive. If confirmed, expand scope — fleet
   VQL hunt, wider time window, related hosts — to find the blast
   radius. Output: validated findings with scope and evidence.

6. **Promote to detection or close with rationale.** Confirmed findings
   become detection content: a Sigma or native rule with ATT&CK
   mapping, tuned thresholds, an allowlist for the false positives you
   just produced, and a retest (Atomic/purple-team technique) proving
   it fires. Refuted or inconclusive hunts are closed with the
   hypothesis, evidence, and coverage claim recorded. Output: deployed
   rule plus test result, or a closed hunt record.

7. **Report and update the knowledge base.** Output: hunt report with
   hypothesis outcome, queries, findings, IOCs, coverage delta, and
   recommended response actions handed to
   `security-incident-response-and-soc` where an active compromise is
   implied.

## Quality bar

- [ ] The hypothesis is testable: named technique, data source, scope,
      time window, and an explicit refutation condition
- [ ] Every query is preserved verbatim with its time window so the
      hunt can be rerun and audited
- [ ] Data-source coverage is stated — a hunt over missing telemetry is
      recorded as inconclusive, never as "clean"
- [ ] Each candidate finding is validated with asset/user/peer context
      and a known-good comparison before being called a true positive
- [ ] Thresholds are justified (e.g., CV <0.20 periodicity, ≥50
      connections) rather than unexplained magic numbers
- [ ] False positives are recorded with the tuning change that prevents
      them recurring
- [ ] Confirmed findings either ship as a tested detection rule with
      ATT&CK mapping or carry a documented reason they were not
      promoted
- [ ] The hunt report states the outcome as confirmed, refuted, or
      inconclusive — never left blank
- [ ] No containment or remediation action is taken from a hunt; active
      compromise is handed to `security-incident-response-and-soc`
- [ ] Deception tokens and honeypots are authorized, inventoried, and
      routed to a monitored alert channel before deployment

## Reference map

All 71 merged techniques, with descriptions, are catalogued in
[`references/technique-index.md`](references/technique-index.md).
Near-duplicate techniques keep their own reference files; each group
below is one topic.

| Situation | Open |
|---|---|
| Structure a hunt hypothesis, choose data sources, write the report | [building-threat-hunt-hypothesis-framework](references/building-threat-hunt-hypothesis-framework.md) |
| Beaconing / C2 frequency and jitter analysis (near-duplicate pair — one topic) | [hunting-for-beaconing-with-frequency-analysis](references/hunting-for-beaconing-with-frequency-analysis.md) · [hunting-for-command-and-control-beaconing](references/hunting-for-command-and-control-beaconing.md) |
| Cobalt Strike beacons: JA3, certificates, profiles | [hunting-for-cobalt-strike-beacons](references/hunting-for-cobalt-strike-beacons.md) |
| DNS tunneling and DNS-based persistence | [hunting-for-dns-tunneling-with-zeek](references/hunting-for-dns-tunneling-with-zeek.md) · [hunting-for-dns-based-persistence](references/hunting-for-dns-based-persistence.md) |
| LOLBin / living-off-the-land execution (near-duplicate trio — one topic) | [hunting-for-living-off-the-land-binaries](references/hunting-for-living-off-the-land-binaries.md) · [hunting-for-lolbins-execution-in-endpoint-logs](references/hunting-for-lolbins-execution-in-endpoint-logs.md) · [detecting-living-off-the-land-with-lolbas](references/detecting-living-off-the-land-with-lolbas.md) |
| Credential dumping: LSASS, SAM, NTDS.dit, comsvcs.dll | [detecting-credential-dumping-techniques](references/detecting-credential-dumping-techniques.md) · [detecting-t1003-credential-dumping-with-edr](references/detecting-t1003-credential-dumping-with-edr.md) · [detecting-mimikatz-execution-patterns](references/detecting-mimikatz-execution-patterns.md) |
| Kerberos abuse: Kerberoasting, pass-the-ticket, golden ticket, DCSync | [detecting-kerberoasting-attacks](references/detecting-kerberoasting-attacks.md) · [detecting-pass-the-ticket-attacks](references/detecting-pass-the-ticket-attacks.md) · [detecting-golden-ticket-attacks-in-kerberos-logs](references/detecting-golden-ticket-attacks-in-kerberos-logs.md) · [hunting-for-dcsync-attacks](references/hunting-for-dcsync-attacks.md) |
| NTLM relay and NTLM downgrade | [detecting-ntlm-relay-with-event-correlation](references/detecting-ntlm-relay-with-event-correlation.md) · [hunting-for-ntlm-relay-attacks](references/hunting-for-ntlm-relay-attacks.md) |
| Lateral movement via SMB, RDP, WMI, DCOM | [detecting-lateral-movement-with-splunk](references/detecting-lateral-movement-with-splunk.md) · [hunting-for-dcom-lateral-movement](references/hunting-for-dcom-lateral-movement.md) · [hunting-for-lateral-movement-via-wmi](references/hunting-for-lateral-movement-via-wmi.md) |
| Windows persistence sweep: registry, tasks, services, WMI, startup | [hunting-for-persistence-mechanisms-in-windows](references/hunting-for-persistence-mechanisms-in-windows.md) · [detecting-wmi-persistence](references/detecting-wmi-persistence.md) · [hunting-for-scheduled-task-persistence](references/hunting-for-scheduled-task-persistence.md) · [hunting-for-unusual-service-installations](references/hunting-for-unusual-service-installations.md) |
| Linux persistence: cron, systemd, LD_PRELOAD, authorized_keys | [analyzing-persistence-mechanisms-in-linux](references/analyzing-persistence-mechanisms-in-linux.md) |
| Process injection and hollowing telemetry | [hunting-for-process-injection-techniques](references/hunting-for-process-injection-techniques.md) · [detecting-t1055-process-injection-with-sysmon](references/detecting-t1055-process-injection-with-sysmon.md) · [detecting-process-hollowing-technique](references/detecting-process-hollowing-technique.md) |
| Fileless / memory-only execution (near-duplicate pair — one topic; files owned by identity-zero-trust-and-endpoint-security and malware-analysis-and-reverse-engineering) | [detecting-fileless-attacks-on-endpoints](../identity-zero-trust-and-endpoint-security/references/detecting-fileless-attacks-on-endpoints.md) · [detecting-fileless-malware-techniques](../malware-analysis-and-reverse-engineering/references/detecting-fileless-malware-techniques.md) |
| Suspicious and obfuscated PowerShell (incl. Empire artifacts) | [hunting-for-anomalous-powershell-execution](references/hunting-for-anomalous-powershell-execution.md) · [detecting-suspicious-powershell-execution](references/detecting-suspicious-powershell-execution.md) · [analyzing-powershell-empire-artifacts](references/analyzing-powershell-empire-artifacts.md) |
| Data staging and exfiltration hunts | [hunting-for-data-exfiltration-indicators](references/hunting-for-data-exfiltration-indicators.md) · [hunting-for-data-staging-before-exfiltration](references/hunting-for-data-staging-before-exfiltration.md) · [hunting-for-unusual-network-connections](references/hunting-for-unusual-network-connections.md) |
| Fleet-wide hunting and offline EVTX searching | [fleet-hunting-with-velociraptor](references/fleet-hunting-with-velociraptor.md) · [hunting-evtx-with-chainsaw](references/hunting-evtx-with-chainsaw.md) |
| YARA hunting across files and memory | [performing-threat-hunting-with-yara-rules](references/performing-threat-hunting-with-yara-rules.md) |
| Privilege escalation and elevation-service abuse | [detecting-privilege-escalation-attempts](references/detecting-privilege-escalation-attempts.md) · [detecting-t1548-abuse-elevation-control-mechanism](references/detecting-t1548-abuse-elevation-control-mechanism.md) |
| Insider threat baselines and UEBA scoring | [detecting-insider-threat-with-ueba](references/detecting-insider-threat-with-ueba.md) · [detecting-insider-threat-behaviors](references/detecting-insider-threat-behaviors.md) |
| Web shells, supply chain, living off the cloud | [hunting-for-webshell-activity](references/hunting-for-webshell-activity.md) · [hunting-for-supply-chain-compromise](references/hunting-for-supply-chain-compromise.md) · [hunting-for-living-off-the-cloud-techniques](references/hunting-for-living-off-the-cloud-techniques.md) |
| Deploy honeytokens, cloud decoys, honeypots | [deploying-honeytokens-and-canarytokens](references/deploying-honeytokens-and-canarytokens.md) · [deploying-cloud-deception-with-decoy-resources](references/deploying-cloud-deception-with-decoy-resources.md) · [implementing-network-deception-with-honeypots](references/implementing-network-deception-with-honeypots.md) |
| Give deception a strategy and measurable objectives (MITRE Engage) | [designing-adversary-engagement-with-mitre-engage](references/designing-adversary-engagement-with-mitre-engage.md) |
| Pick the data source, platform, and tool for a hunt | [hunt-data-source-and-tool-matrix](references/hunt-data-source-and-tool-matrix.md) |

Executable helpers for each technique live in
`scripts/<technique-name>/` — read the reference file first to learn
what the script expects, then run it.

## Output format

For any hunt, deliver:

```markdown
# Hunt <TH-YYYYMMDD-NN> — <Title>

## Hypothesis
One falsifiable sentence: actor/technique, activity, data source, scope,
window, observable, refutation condition.

## Coverage
Data sources queried | Known gaps | Baseline definition

## Queries executed
Query (verbatim) | Platform | Window | Result count

## Findings
Finding | Evidence (events, processes, connections) | Confidence |
ATT&CK technique | True/false positive rationale

## Scope of confirmed activity
Hosts, users, and time range affected; IOCs (defanged).

## Outcome
Confirmed | Refuted | Inconclusive — with the reason.

## Detection promotion
Rule (Sigma/native) | Thresholds and allowlists | Retest result |
Coverage delta. Or: why no rule was written.

## Handoff
Recommended response actions and the incident skill to run if activity
is live.
```

For deception work, additionally deliver the engagement goal
(Expose/Affect/Elicit), the measurable operational objective, the
technique → activity selection matrix, gating criteria, and the alert
routing path.
