# Conducting Social Engineering Penetration Test

## API Reference

## Libraries

| Library | Install | Purpose |
|---------|---------|---------|
| requests | `pip install requests` | GoPhish REST API client |
| gophish | `pip install gophish` | Official GoPhish Python client |

## GoPhish API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/campaigns/` | List all campaigns |
| GET | `/api/campaigns/{id}/results` | Campaign results and metrics |
| POST | `/api/campaigns/` | Create new campaign |
| POST | `/api/templates/` | Create email template |
| POST | `/api/groups/` | Create target group |
| POST | `/api/smtp/` | Create sending profile |
| POST | `/api/pages/` | Create landing page |

## Campaign Metrics

| Metric | Formula |
|--------|---------|
| Open Rate | emails_opened / emails_sent x 100 |
| Click Rate | links_clicked / emails_sent x 100 |
| Submit Rate | data_submitted / emails_sent x 100 |
| Report Rate | reported / emails_sent x 100 |

## Social Engineering Vectors

| Vector | Tools |
|--------|-------|
| Email Phishing | GoPhish, King Phisher |
| Vishing | Pretext scripts, VoIP tools |
| Physical | Badge cloning, tailgating |
| USB Drops | Rubber Ducky, USB armory |

## External References

- [GoPhish API Documentation](https://docs.getgophish.com/api-documentation/)
- [SANS Social Engineering Framework](https://www.social-engineer.org/framework/)
- [MITRE ATT&CK Phishing T1566](https://attack.mitre.org/techniques/T1566/)

---

## Standards and Controls

## Frameworks
- PTES Social Engineering Section: http://www.pentest-standard.org/index.php/Social_Engineering
- NIST SP 800-50: Building an Information Technology Security Awareness and Training Program
- SANS Security Awareness Maturity Model
- MITRE ATT&CK Initial Access: https://attack.mitre.org/tactics/TA0001/

## MITRE ATT&CK Techniques
| Technique | ID | Vector |
|-----------|----|--------|
| Phishing: Spear Phishing Link | T1566.002 | Email with malicious URL |
| Phishing: Spear Phishing Attachment | T1566.001 | Email with payload |
| Phishing: Spear Phishing via Service | T1566.003 | Social media / messaging |

## Legal Considerations
- Must have explicit written authorization
- Cannot target personal email or devices without consent
- GDPR compliance for EU employees
- Cannot use real malware or destructive payloads
- Results must be anonymized in reporting to protect individuals

---

## Workflows

## Campaign Lifecycle
```
Authorization & Scoping
    │
    ├── OSINT & Target Profiling
    │   ├── Email harvesting
    │   ├── LinkedIn/social media reconnaissance
    │   └── Target group selection
    │
    ├── Infrastructure Setup
    │   ├── Domain registration (lookalike)
    │   ├── GoPhish/Evilginx deployment
    │   ├── SMTP configuration (SPF/DKIM)
    │   └── Landing page creation
    │
    ├── Campaign Execution
    │   ├── Phishing emails (batched sends)
    │   ├── Vishing calls
    │   ├── Physical pretexting
    │   └── USB drops
    │
    ├── Monitoring & Data Collection
    │   ├── Email opens/clicks tracking
    │   ├── Credential captures
    │   ├── Call recordings/notes
    │   └── Physical access logs
    │
    └── Reporting & Training
        ├── Metrics compilation
        ├── Risk scoring
        ├── Executive report
        └── Targeted training recommendations
```

---

## Working Template

## Document Control
| Field | Value |
|-------|-------|
| Client | [Name] |
| Test Type | Social Engineering Assessment |
| Vectors Tested | Phishing, Vishing, Physical |
| Period | [Start] — [End] |
| Classification | CONFIDENTIAL |

## Executive Summary
[Overview of social engineering resilience, key success rates, highest risk groups]

## Campaign Results

### Phishing
| Metric | Value |
|--------|-------|
| Emails Sent | [N] |
| Open Rate | [N]% |
| Click Rate | [N]% |
| Credential Submit Rate | [N]% |
| Report Rate | [N]% |

### Vishing
| Metric | Value |
|--------|-------|
| Calls Made | [N] |
| Info Disclosed | [N]% |
| Credentials Provided | [N]% |

### Physical
| Metric | Value |
|--------|-------|
| Tailgate Success | [N/M] |
| Areas Accessed | [N] |

## Department Risk Matrix
| Department | Risk | Priority Action |
|-----------|------|----------------|
| [Dept] | [Level] | [Training type] |

## Recommendations
1. [Recommendation]
