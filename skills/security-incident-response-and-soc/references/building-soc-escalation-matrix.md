# Building Soc Escalation Matrix

## API Reference

## Priority Tiers
| Tier | Response SLA | Update SLA | Resolution SLA |
|------|-------------|------------|----------------|
| P1 Critical | 15 min | 1 hour | 4 hours |
| P2 High | 30 min | 2 hours | 8 hours |
| P3 Medium | 1 hour | 4 hours | 24 hours |
| P4 Low | 4 hours | 8 hours | 72 hours |

## Alert Categories
| Category | Default Priority | Auto-Escalate Triggers |
|----------|-----------------|----------------------|
| Malware | P2 | ransomware, wiper, apt |
| Phishing | P3 | executive_target, credential_harvested |
| Unauthorized Access | P2 | admin_account, domain_controller |
| Data Exfiltration | P1 | pii, financial, classified |
| Insider Threat | P2 | privileged_user, data_staging |

## Escalation Chain
```
P1: SOC Analyst → SOC Lead → IR Manager → CISO
P2: SOC Analyst → SOC Lead → IR Manager
P3: SOC Analyst → SOC Lead
P4: SOC Analyst
```

## Notification Channels
| Tier | Channels |
|------|----------|
| P1 | Slack #critical-alerts, PagerDuty, Email CISO, SMS |
| P2 | Slack #soc-alerts, PagerDuty, Email IR Manager |
| P3 | Slack #soc-alerts, Email SOC Lead |
| P4 | Slack #soc-triage |

## PagerDuty Incident API
```
POST https://events.pagerduty.com/v2/enqueue
{
  "routing_key": "SERVICE_KEY",
  "event_action": "trigger",
  "payload": {
    "summary": "P1 Alert: Data exfiltration detected",
    "severity": "critical",
    "source": "SOC SIEM"
  }
}
```

## Slack Webhook Notification
```
POST https://hooks.slack.com/services/T.../B.../xxx
{
  "channel": "#critical-alerts",
  "text": "P1 Incident: ..."
}
```

## Auto-Escalation Rules
| Condition | Action |
|-----------|--------|
| Response SLA exceeded | Escalate to next in chain |
| >= 3 correlated alerts | Increase priority by 1 |
| VIP user affected | Auto-escalate to P1 |
| Critical asset impacted | Increase priority by 1 |

---

## Standards and Controls

## NIST SP 800-61 Rev 2 Incident Handling
- Defines incident categories and severity levels
- Recommends functional impact, information impact, and recoverability as factors
- Guides escalation based on incident classification

## ITIL Incident Management
- P1-P4 priority classification framework
- Impact x Urgency = Priority matrix
- SLA management for each priority level

## SOC-CMM (SOC Capability Maturity Model)
- Level 1: Ad-hoc escalation, no formal process
- Level 2: Defined escalation paths, documented SLAs
- Level 3: Automated escalation with SOAR integration
- Level 4: Context-driven escalation with risk scoring
- Level 5: AI-assisted prioritization and auto-escalation

## Response Time Standards

| Priority | Industry Standard | Best Practice |
|---|---|---|
| P1 | 15 min response, 4h resolution | 5 min response, 2h containment |
| P2 | 30 min response, 8h resolution | 15 min response, 4h containment |
| P3 | 4h response, 24h resolution | 2h response, 12h resolution |
| P4 | 8h response, 72h resolution | 4h response, 48h resolution |

---

## Workflows

## Escalation Flow

```
Alert Generated
    |
    v
Tier 1 Triage (15 min)
    |
    +-- P4/P3: Handle to resolution
    |
    +-- P2: Escalate to Tier 2
    |       |
    |       +-- Resolved: Close
    |       +-- Unresolved (4h): Escalate to Tier 3
    |
    +-- P1: Immediate escalation
            |
            v
        Tier 3 + Management Notified
            |
            v
        War Room / Bridge Activated
            |
            v
        Containment within SLA
            |
            v
        Resolution + Post-Incident Review
```

## Notification Matrix

| Priority | Tier 1 | Tier 2 | Tier 3 | SOC Mgr | CISO | Legal |
|---|---|---|---|---|---|---|
| P1 | Aware | Aware | Lead | Notified | Notified | Standby |
| P2 | Aware | Lead | Consulted | Informed | - | - |
| P3 | Lead | Consulted | - | - | - | - |
| P4 | Lead | - | - | - | - | - |

---

## Working Template

## Priority Definitions

| Priority | Response SLA | Resolution SLA | Assigned Tier | Mgmt Notification |
|---|---|---|---|---|
| P1 - Critical | 15 min | 4 hours | Tier 3 | 30 min |
| P2 - High | 30 min | 8 hours | Tier 2 | 2 hours |
| P3 - Medium | 4 hours | 24 hours | Tier 1 | As needed |
| P4 - Low | 8 hours | 72 hours | Tier 1 | Weekly |

## Escalation Contacts

| Role | Name | Phone | Email | Availability |
|---|---|---|---|---|
| Tier 1 Lead | | | | 24/7 |
| Tier 2 Lead | | | | 24/7 |
| Tier 3 Lead | | | | On-call |
| SOC Manager | | | | Business hours + on-call |
| CISO | | | | On-call for P1 |

## Auto-Escalation Rules

| Trigger | Priority | Action |
|---|---|---|
| Ransomware detected | P1 | Tier 3 + CISO |
| Domain admin compromise | P1 | Tier 3 + CISO |
| Active data exfiltration | P1 | Tier 3 + CISO |
| Executive account anomaly | P2 | Tier 2 + SOC Manager |
| SLA breach | +1 Tier | Notify SOC Manager |
