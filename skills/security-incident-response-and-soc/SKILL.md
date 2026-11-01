---
name: security-incident-response-and-soc
description: >-
  Run the full lifecycle of an active security incident — alert triage,
  severity and SLA assignment, containment, eradication, recovery, and
  post-incident review — plus the SOC machinery around it: playbooks,
  escalation matrices, SIEM detection use cases, SOAR automation, IOC
  enrichment, log-source onboarding, and MTTD/MTTR metrics. Use when the
  user says "we've been breached", "triage this alert", "contain the
  ransomware", "isolate the compromised host", "write an IR playbook",
  "build our SOC escalation matrix", "cut false positives in the SIEM",
  "run a lessons-learned", or asks how to respond to a phishing campaign,
  an Active Directory compromise, insider data theft, a cloud account
  takeover, or a ransomware demand. Do not use for proactive
  hypothesis-driven searching before any alert exists (see
  threat-hunting-and-detection), for forensically sound evidence
  acquisition and timeline reconstruction (see
  digital-forensics-and-evidence), or for working out what a suspicious
  sample does (see malware-analysis-and-reverse-engineering).
license: Apache-2.0
---

# Security Incident Response and SOC

Most incident damage is done between detection and decision, not by the
initial compromise. This skill exists to compress that gap: classify
fast, contain before the adversary expands, verify the containment
instead of trusting it, and feed every incident back into detection and
playbooks so the same attack costs less the next time.

Treat every response step as if it will be reconstructed later by an
investigator, an insurer, or a regulator. If an action was not logged
with a timestamp and an owner, it did not happen.

## When to use

- A SIEM, EDR, DLP, or user report produces an alert that needs human
  classification, prioritization, and a triage disposition
- An active breach must be stopped: host isolation, credential
  revocation, C2 blocking or sinkholing, cloud session termination
- Ransomware, phishing/BEC, email-account compromise, Active Directory
  compromise, insider theft, or a cloud identity takeover is in progress
- Writing or refreshing incident response playbooks, severity/SLA
  definitions, escalation matrices, and communication templates
- Standing up or tuning SOC operations: SIEM use cases and correlation
  rules, false-positive reduction, log-source onboarding, SOAR
  playbooks, alert dashboards, and SOC metrics
- Collecting, enriching, and sharing indicators of compromise from a
  live or closed incident
- Running tabletop, purple-team, or ransomware-readiness exercises
- Deciding recovery order, backup validation, and re-infection checks
  after an intrusion

**Do not use for** — `threat-hunting-and-detection` when no alert exists
and the task is a proactive hypothesis-driven search or authoring
endpoint/network detection content for its own sake;
`digital-forensics-and-evidence` when the ask is forensically sound
acquisition, artifact parsing, or a defensible super-timeline (this
skill captures volatile evidence in-flight, but deep imaging and
timeline reconstruction belong to that skill); and
`malware-analysis-and-reverse-engineering` when the question is what a
sample does rather than what to do about the compromise.
`offensive-security-and-red-teaming` owns simulating the attack, and
`cloud-container-and-devsecops-security` owns hardening the cloud and
pipeline infrastructure before anything is compromised.

Not a security event? A production or engineering incident with no breach, compromise, or security component (outage, capacity, deploy failure) belongs in the **incident-response** skill.


## Workflow

1. **Intake and classify.** Input: alert, user report, threat-intel
   match, or DLP hit. Record source, occurrence vs. detection time
   (dwell-time gap), affected hosts/users, detection fidelity, and raw
   evidence; map to an incident category (unauthorized access, malicious
   code, improper usage, recon, web attack, DoS); select the matching
   playbook, or flag that one must be written. Output: incident record
   with type, playbook, and named owner.

2. **Assign severity and start the SLA clock.** Score asset criticality
   × data sensitivity × scope × active-vs-historical × confirmed-vs-
   suspected into P1–P4. Record acknowledgement and containment
   deadlines, plus any automatic escalation trigger (ransomware,
   domain-admin compromise, or confirmed exfiltration = immediate P1 to
   Tier 3 and management). Output: severity, SLA deadlines, escalation
   path on the ticket.

3. **Enrich before escalating.** Check IOC reputation (VirusTotal,
   AbuseIPDB, MISP), asset owner and business criticality from the
   CMDB, the user's recent authentication and MFA state, related alerts
   on the same host or user in the past 30 days, and whether the
   endpoints are internal, partner, or external. Output: enriched
   triage note with TI matches, confidence, and a recommended action.

4. **Preserve volatile evidence, then contain.** Follow the order of
   volatility — memory, live connections, and running process state
   before disk or any remediation — then apply short-term containment:
   EDR network isolation, disabling compromised accounts, blocking or
   sinkholing attacker infrastructure, revoking cloud sessions and
   keys. Output: captured volatile evidence plus containment in effect.

5. **Verify containment rather than assuming it.** Prove no adversary
   access remains: look for persistence and attacker-created accounts,
   keys, or resources (all cloud regions included), confirm C2 is dead,
   and check for lateral spread to hosts touched by the same campaign.
   Repeat steps 4–5 until verification passes. Output: a written
   containment-verification statement, or a new containment action.

6. **Eradicate and recover.** Remove every persistence mechanism
   (autoruns, scheduled tasks, WMI subscriptions, services, web shells,
   malicious GPO changes), reset every exposed credential — twice for
   `krbtgt` at least 12 hours apart where Kerberos ticket forgery is
   possible, plus cloud tokens and API secrets — patch the entry-point
   vulnerability, then restore from a backup proven to predate the
   compromise: scan it first, rebuild identity infrastructure first,
   and reconnect in phases with re-infection checks. Output: clean,
   validated systems returned to production.

7. **Communicate on the severity cadence.** Update the ticket for every
   action; brief stakeholders and executives at the cadence the severity
   defines; trigger legal, regulatory, insurance, and law-enforcement
   notifications when thresholds are met. Output: communication log and
   a stakeholder brief.

8. **Run the post-incident review.** Rebuild the timeline from ticket
   and log data, calculate MTTD/MTTA/MTTC/MTTR and alert disposition
   rates, run a blameless 5-Whys to root cause, assign action items
   with owners and dates, and update the playbook and detection rules
   (Sigma, correlation searches, ATT&CK coverage gaps) — then retest
   them. Output: PIR report, tracked action items, and new or tuned
   detections.

## Quality bar

- [ ] Severity comes from the matrix (asset criticality × threat
      status), with SLA deadlines and escalation trigger recorded at
      intake, not after the incident escalates itself
- [ ] Volatile evidence was captured before any remediation that would
      destroy it, and the collection is timestamped on the ticket
- [ ] Containment is *verified* — residual access, attacker-created
      identities, and active C2 are checked for, not assumed gone
- [ ] Every responder action has a timestamp and an owner in the
      incident ticket; collected artifacts have custody recorded
- [ ] Recovery uses only backups verified to predate the compromise and
      scanned before restore; `krbtgt` was reset twice where ticket
      forgery was possible
- [ ] Alert dispositions are explicit — true positive, benign true
      positive, false positive, or undetermined — with a tuning action
      recorded for every false positive
- [ ] Notifications (stakeholder, executive, regulatory, legal) were
      made inside the severity cadence and are evidenced in the log
- [ ] The PIR contains measured MTTD/MTTR, a root cause (not a symptom),
      and dated action items with owners
- [ ] Playbook and detection updates from the incident are written,
      deployed, and retested — an action item without a retest is open
- [ ] Automated SOAR actions above the approval threshold ran only
      behind a human approval gate, and every automated action is logged

## Reference map

All 102 merged techniques, with descriptions, are catalogued in
[`references/technique-index.md`](references/technique-index.md). Load
the file for the situation you are in rather than reading the index.

| Situation | Open |
|---|---|
| Classify and prioritize a new incident (near-duplicate pair — one topic, two files) | [triaging-security-incident](references/triaging-security-incident.md) · [triaging-security-incident-with-ir-playbook](references/triaging-security-incident-with-ir-playbook.md) |
| Triage queued alerts in Splunk or Elastic; disposition taxonomy | [triaging-security-alerts-in-splunk](references/triaging-security-alerts-in-splunk.md) · [performing-alert-triage-with-elastic-siem](references/performing-alert-triage-with-elastic-siem.md) |
| Severity tiers, response SLAs, escalation triggers, notification cadence | [building-soc-escalation-matrix](references/building-soc-escalation-matrix.md) |
| Author IR playbooks, decision trees, and RACI | [building-incident-response-playbook](references/building-incident-response-playbook.md) |
| Contain a live breach: isolate, revoke, sinkhole, then verify | [containing-active-breach](references/containing-active-breach.md) |
| Cloud-native containment and evidence preservation (AWS/Azure/GCP) | [conducting-cloud-incident-response](references/conducting-cloud-incident-response.md) · [performing-cloud-incident-containment-procedures](references/performing-cloud-incident-containment-procedures.md) |
| Ransomware response end to end (near-duplicate pair — one topic, two files) | [performing-ransomware-response](references/performing-ransomware-response.md) · [building-soc-playbook-for-ransomware](references/building-soc-playbook-for-ransomware.md) · [building-ransomware-playbook-with-cisa-framework](references/building-ransomware-playbook-with-cisa-framework.md) |
| Recovery order, backup integrity, and re-infection validation | [recovering-from-ransomware-attack](references/recovering-from-ransomware-attack.md) · [validating-backup-integrity-for-recovery](references/validating-backup-integrity-for-recovery.md) · [implementing-ransomware-backup-strategy](references/implementing-ransomware-backup-strategy.md) |
| Phishing / BEC / email-account compromise response | [investigating-phishing-email-incident](references/investigating-phishing-email-incident.md) · [conducting-phishing-incident-response](references/conducting-phishing-incident-response.md) · [detecting-email-account-compromise](references/detecting-email-account-compromise.md) |
| Malware infection response and eradication | [conducting-malware-incident-response](references/conducting-malware-incident-response.md) · [eradicating-malware-from-infected-systems](references/eradicating-malware-from-infected-systems.md) |
| Active Directory compromise investigation | [performing-active-directory-compromise-investigation](references/performing-active-directory-compromise-investigation.md) |
| Insider threat case: allegation to evidence preservation | [performing-insider-threat-investigation](references/performing-insider-threat-investigation.md) · [investigating-insider-threat-indicators](references/investigating-insider-threat-indicators.md) |
| Automate triage and containment with SOAR, with approval gates | [implementing-soar-automation-with-phantom](references/implementing-soar-automation-with-phantom.md) · [implementing-soar-playbook-with-palo-alto-xsoar](references/implementing-soar-playbook-with-palo-alto-xsoar.md) |
| Build or tune SIEM detection use cases; cut false positives | [implementing-siem-use-cases-for-detection](references/implementing-siem-use-cases-for-detection.md) · [performing-false-positive-reduction-in-siem](references/performing-false-positive-reduction-in-siem.md) · [building-detection-rules-with-sigma](references/building-detection-rules-with-sigma.md) |
| Onboard a log source cleanly (parsers, TLS syslog, forwarding) | [performing-log-source-onboarding-in-siem](references/performing-log-source-onboarding-in-siem.md) · [implementing-syslog-centralization-with-rsyslog](references/implementing-syslog-centralization-with-rsyslog.md) · [implementing-log-forwarding-with-fluentd](references/implementing-log-forwarding-with-fluentd.md) |
| Analyze a specific log source during an investigation | [analyzing-windows-event-logs-in-splunk](references/analyzing-windows-event-logs-in-splunk.md) · [analyzing-web-server-logs-for-intrusion](references/analyzing-web-server-logs-for-intrusion.md) · [analyzing-dns-logs-for-exfiltration](references/analyzing-dns-logs-for-exfiltration.md) · [analyzing-linux-audit-logs-for-intrusion](references/analyzing-linux-audit-logs-for-intrusion.md) |
| Capture and analyze memory during a live investigation (in-flight, before remediation) | [conducting-memory-forensics-with-volatility](references/conducting-memory-forensics-with-volatility.md) · [analyzing-memory-forensics-with-lime-and-volatility](references/analyzing-memory-forensics-with-lime-and-volatility.md) |
| Collect and enrich IOCs during triage | [collecting-indicators-of-compromise](references/collecting-indicators-of-compromise.md) · [performing-ioc-enrichment-automation](references/performing-ioc-enrichment-automation.md) |
| Fleet-scale endpoint collection during response | [implementing-velociraptor-for-ir-collection](references/implementing-velociraptor-for-ir-collection.md) |
| Build the incident dashboard and SOC metrics | [building-incident-response-dashboard](references/building-incident-response-dashboard.md) · [building-soc-metrics-and-kpi-tracking](references/building-soc-metrics-and-kpi-tracking.md) |
| Post-incident review and collaborative timeline | [conducting-post-incident-lessons-learned](references/conducting-post-incident-lessons-learned.md) · [building-incident-timeline-with-timesketch](references/building-incident-timeline-with-timesketch.md) |
| Tabletop, purple-team, or ransomware readiness exercise | [performing-soc-tabletop-exercise](references/performing-soc-tabletop-exercise.md) · [performing-ransomware-tabletop-exercise](references/performing-ransomware-tabletop-exercise.md) · [performing-purple-team-exercise](references/performing-purple-team-exercise.md) |
| Choose platform and API tooling for a response action | [tool-selection-for-response](references/tool-selection-for-response.md) |

Executable helpers for each technique live in
`scripts/<technique-name>/` — read the reference file first to learn
what the script expects, then run it.

## Output format

For any incident request, deliver:

```markdown
# Incident <ID> — <Short Title>

## Classification
Type | Severity (P1–P4) | Confidence | MITRE ATT&CK techniques | Playbook used

## Timeline
Timestamp (UTC) | Event or responder action | Source | Actor

## Scope
Affected assets | Users | Data at risk | Business unit | Lateral spread status

## Containment and verification
Actions taken, and the evidence that adversary access is actually gone
(credentials revoked, C2 dead, persistence checked, cloud resources
audited across regions).

## Eradication and recovery
Persistence removed, credentials rotated, entry point patched, backup
provenance, restore order, re-infection checks.

## Metrics and root cause
MTTD / MTTA / MTTC / MTTR | Alert disposition | Root cause (5 Whys)

## Action items
Item | Owner | Due date | Detection or playbook change it produces

## Communications log
Stakeholder, executive, regulatory, legal notifications with timestamps
```

For alert triage alone, the deliverable is the triage record: source,
classification, severity, enrichment results, disposition, recommended
actions, escalation target, and SLA deadline.
