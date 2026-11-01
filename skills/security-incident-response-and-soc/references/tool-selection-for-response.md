# Tool Selection for Response

Purpose: route a response action to the concrete platform, API, or CLI
that performs it, so an responder does not have to open 100 technique
files to find the right interface.

## Action → tool matrix

| Response action | Primary tooling | Fallback / alternate | Detail |
|---|---|---|---|
| Case intake, tasks, SLAs | TheHive, ServiceNow, Jira | SIRP, TheHive Cortex | [building-incident-response-playbook](building-incident-response-playbook.md) |
| Alert correlation and triage queue | Splunk ES notable events | Elastic Security signals, QRadar offenses, Sentinel incidents | [triaging-security-alerts-in-splunk](triaging-security-alerts-in-splunk.md) · [performing-alert-triage-with-elastic-siem](performing-alert-triage-with-elastic-siem.md) · [correlating-security-events-in-qradar](correlating-security-events-in-qradar.md) |
| Host network isolation | CrowdStrike `devices/actions/contain` | Defender `IsolateMachine`, EDR quarantine, Velociraptor response | [containing-active-breach](containing-active-breach.md) |
| Account disable / password reset | Entra ID / AD `Set-ADUser`, IAM console | Local admin, service accounts via PAM | [containing-active-breach](containing-active-breach.md) |
| Session and token revocation | Entra sign-out, AWS `GetSigninToken`/key disable, OAuth token revoke | Gateway session kill | [conducting-cloud-incident-response](conducting-cloud-incident-response.md) |
| Network blocking / sinkhole | NGFW policy, DNS sinkhole (Unbound/CoreDNS), `iptables` | Proxy block, host firewall | [containing-active-breach](containing-active-breach.md) |
| Cloud resource isolation | AWS SG replace-with-forensic-SG + EBS snapshot, Azure NSG deny-all, GCP firewall | Snapshot-then-terminate | [performing-cloud-incident-containment-procedures](performing-cloud-incident-containment-procedures.md) |
| Mass email quarantine / purge | M365 Compliance Search + Purge, Google Vault | Gateway bulk release | [investigating-phishing-email-incident](investigating-phishing-email-incident.md) |
| Endpoint artifact collection | Velociraptor VQL hunts | KAPE, native EDR RTR | [implementing-velociraptor-for-ir-collection](implementing-velociraptor-for-ir-collection.md) |
| IOC enrichment | VirusTotal, AbuseIPDB, Shodan, MISP via SOAR | Manual lookups | [performing-ioc-enrichment-automation](performing-ioc-enrichment-automation.md) |
| Automation / orchestration | Splunk SOAR (Phantom), Cortex XSOAR | Custom scripts + webhooks | [implementing-soar-automation-with-phantom](implementing-soar-automation-with-phantom.md) · [implementing-soar-playbook-with-palo-alto-xsoar](implementing-soar-playbook-with-palo-alto-xsoar.md) |
| Paging and escalation | PagerDuty, Opsgenie, Slack/Teams webhooks | Phone tree | [building-soc-escalation-matrix](building-soc-escalation-matrix.md) |
| Metrics and dashboards | Splunk ES risk/alert tables, Elastic, Grafana | CSV export | [building-soc-metrics-and-kpi-tracking](building-soc-metrics-and-kpi-tracking.md) |
| Log pipeline intake | rsyslog (TLS), Fluentd/Fluent Bit, Wazuh agent | Vendor agent | [performing-log-source-onboarding-in-siem](performing-log-source-onboarding-in-siem.md) · [implementing-log-forwarding-with-fluentd](implementing-log-forwarding-with-fluentd.md) |

## Automation vs approval gate

| Class of action | Automation posture |
|---|---|
| Read-only: enrichment, searches, reputation lookups, log pulls | Fully automated, no gate |
| Reversible, low blast radius: tag alert, add observable, block a URL | Automated with rollback logged |
| High impact: host isolation, account disable, mailbox purge, firewall change | Automated only behind a human approval gate |
| Irreversible or legally significant: wipe, restore over evidence, ransom payment steps | Human decision only, with legal/management sign-off |

## Platform selection rules

- Choose the SIEM already carrying the log sources; detection logic
  written once in Sigma ports across Splunk, Elastic, and Sentinel —
  author in Sigma first when portability matters.
- Choose SOAR only where a playbook repeats ≥ weekly; below that
  threshold a documented runbook is cheaper to maintain.
- Prefer EDR-native containment over network isolation when the
  adversary is credential-based — network isolation does not stop
  valid-session abuse.
- Every tool invocation used during an incident must be recorded on
  the ticket with time, operator, and parameters.
