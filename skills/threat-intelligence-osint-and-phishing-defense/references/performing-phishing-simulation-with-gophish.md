# Performing Phishing Simulation With Gophish

## API Reference

## Libraries Used
- **requests**: HTTP client for GoPhish REST API

## CLI Interface
```
python agent.py --url https://gophish.local:3333 --api-key <key> campaigns
python agent.py --url <url> --api-key <key> metrics --id 1
python agent.py --url <url> --api-key <key> resources
python agent.py --url <url> --api-key <key> report --id 1
python agent.py --url <url> --api-key <key> launch --name "Q1 Test" --template-id 1 --page-id 1 --smtp-id 1 --group-ids 1 2 --phish-url https://phish.local
```

## GoPhishClient API Endpoints

### `GET /api/campaigns/` — List all campaigns
### `GET /api/campaigns/{id}` — Campaign details with results
### `POST /api/campaigns/` — Create and launch campaign
### `GET /api/groups/` — List target groups
### `GET /api/templates/` — List email templates
### `GET /api/smtp/` — List sending profiles

## Core Functions

### `get_campaign_metrics(...)` — Campaign performance analysis
Tracks: sent, opened, clicked, submitted, reported. Calculates percentage rates.

### `generate_report(...)` — Risk assessment with recommendations
Risk levels: CRITICAL (>10% credential submission), HIGH (>20% click rate), MEDIUM.

### `list_resources(...)` — Enumerate available GoPhish configurations

## Campaign Status Tracking
| Status | Description |
|--------|-------------|
| Email Sent | Email delivered to target |
| Email Opened | Tracking pixel loaded |
| Clicked Link | Target clicked phishing URL |
| Submitted Data | Target entered credentials |
| Reported | Target reported phishing email |

## Dependencies
```
pip install requests
```

---

## Standards and Controls

## Legal & Compliance Framework
- **Computer Fraud and Abuse Act (CFAA)**: Ensure written authorization before conducting simulations
- **GDPR (EU)**: Data protection requirements for handling employee email addresses and click data
- **CCPA (California)**: Employee data privacy considerations
- **Company Acceptable Use Policy**: Must align simulation with organizational policies

## Industry Standards
- **NIST SP 800-50**: Building an Information Technology Security Awareness and Training Program
- **NIST SP 800-16**: Information Technology Security Training Requirements
- **SANS Security Awareness Maturity Model**: Five levels from non-existent to metrics framework
- **ISO 27001:2022**: A.6.3 - Information security awareness, education and training

## MITRE ATT&CK References
- **T1566.001**: Phishing: Spearphishing Attachment
- **T1566.002**: Phishing: Spearphishing Link
- **T1598**: Phishing for Information
- **T1204.001**: User Execution: Malicious Link
- **T1204.002**: User Execution: Malicious File

## GoPhish Technical Reference

### API Endpoints
| Endpoint | Method | Description |
|---|---|---|
| `/api/campaigns/` | GET | List all campaigns |
| `/api/campaigns/` | POST | Create new campaign |
| `/api/campaigns/{id}` | GET | Get campaign details |
| `/api/campaigns/{id}/results` | GET | Get campaign results |
| `/api/campaigns/{id}/summary` | GET | Get campaign summary |
| `/api/templates/` | GET/POST | Manage email templates |
| `/api/pages/` | GET/POST | Manage landing pages |
| `/api/smtp/` | GET/POST | Manage sending profiles |
| `/api/groups/` | GET/POST | Manage user groups |
| `/api/import/email` | POST | Import email template |
| `/api/import/site` | POST | Import/clone website |

### Campaign Event Types
| Event | Description |
|---|---|
| Email Sent | Email delivered to target |
| Email Opened | Tracking pixel loaded |
| Clicked Link | User clicked phishing URL |
| Submitted Data | User entered credentials |
| Email Reported | User reported via plugin |

## Phishing Simulation Best Practices
1. **Always obtain written authorization** from executive management
2. **Coordinate with IT/security teams** to whitelist simulation infrastructure
3. **Start with easier-to-identify phishing** and increase difficulty gradually
4. **Never punish employees** for failing - focus on education
5. **Provide immediate training** after user interaction
6. **Run campaigns regularly** (monthly/quarterly) for sustained awareness
7. **Vary scenarios** across campaign types (credential harvesting, attachment, link)
8. **Respect opt-outs** where legally required
9. **Protect campaign data** - treat click/submit data as sensitive
10. **Report metrics anonymously** when possible at department level

---

## Workflows

## Workflow 1: End-to-End Campaign Execution

```
Phase 1: Authorization & Planning
  |
  +-- Obtain written authorization from management
  +-- Define campaign objectives and success criteria
  +-- Select target groups (by department, role, risk level)
  +-- Choose phishing scenario (credential harvest, link click, attachment)
  +-- Set campaign timeline
  |
Phase 2: Infrastructure Setup
  |
  +-- Deploy GoPhish server (Docker or bare metal)
  +-- Configure SSL/TLS certificate for landing page
  +-- Set up SMTP sending profile
  +-- Whitelist GoPhish IP in email gateway
  +-- Configure DNS for phishing domain
  +-- Test email deliverability
  |
Phase 3: Content Creation
  |
  +-- Design email template with GoPhish variables
  +-- Create or clone landing page
  +-- Set up redirect to training page
  +-- Configure credential capture (if authorized)
  +-- Test with internal team first
  |
Phase 4: Target Preparation
  |
  +-- Import user list (CSV: first,last,email,position)
  +-- Segment into groups if needed
  +-- Verify email addresses are valid
  |
Phase 5: Campaign Launch
  |
  +-- Set send schedule (staggered over hours/days)
  +-- Launch campaign
  +-- Monitor real-time dashboard
  +-- Handle any delivery issues
  |
Phase 6: Analysis & Reporting
  |
  +-- Wait for campaign duration to complete
  +-- Export results via API
  +-- Generate analytics report
  +-- Present findings to stakeholders
  +-- Identify high-risk groups for targeted training
```

## Workflow 2: Progressive Difficulty Model

```
Quarter 1: Easy to Detect
  +-- Generic greeting, spelling errors
  +-- Unrelated external domain
  +-- Obvious call to action
  +-- Expected: < 20% click rate
  |
Quarter 2: Moderate Difficulty
  +-- Personalized with name/department
  +-- Look-alike domain
  +-- Relevant pretext (IT maintenance, HR policy)
  +-- Expected: < 15% click rate
  |
Quarter 3: Difficult
  +-- Highly targeted content
  +-- Convincing sender spoofing
  +-- Timely pretext (tax season, annual review)
  +-- Expected: < 10% click rate
  |
Quarter 4: Advanced
  +-- Spear-phishing with OSINT
  +-- Multi-step pretext
  +-- Mimics real vendor communication
  +-- Expected: < 5% click rate
```

## Workflow 3: Automated Campaign via API

```
[Python Script] --> GoPhish API
  |
  +-- POST /api/smtp/ (create sending profile)
  +-- POST /api/templates/ (create email template)
  +-- POST /api/pages/ (create landing page)
  +-- POST /api/groups/ (import target users)
  +-- POST /api/campaigns/ (launch campaign)
  |
  [Wait for campaign duration]
  |
  +-- GET /api/campaigns/{id}/summary
  +-- GET /api/campaigns/{id}/results
  |
  [Generate report with metrics]
  |
  +-- Calculate: open rate, click rate, submit rate, report rate
  +-- Compare against baseline and industry benchmarks
  +-- Export to PDF/HTML report
```

## Workflow 4: Post-Campaign Remediation

```
Campaign Results Available
  |
  v
[Identify users who submitted credentials]
  |
  +-- Immediately: Force password reset
  +-- Within 24h: Send targeted training content
  +-- Within 1 week: Manager notification (aggregate only)
  |
  v
[Identify users who clicked but did not submit]
  |
  +-- Send phishing awareness micro-training
  +-- Include specific red flags they missed
  |
  v
[Identify users who reported the email]
  |
  +-- Send positive reinforcement
  +-- Recognize in security champions program
  |
  v
[Aggregate department-level metrics]
  |
  +-- Present to leadership
  +-- Identify highest-risk departments
  +-- Plan targeted training interventions
  +-- Schedule next campaign
```

---

## Working Template

## Campaign Information
- **Campaign Name**: [e.g., Q1-2026 Password Reset Simulation]
- **Campaign Owner**: [Security Awareness Team Lead]
- **Authorization Date**: [YYYY-MM-DD]
- **Authorized By**: [CISO / VP of Security]
- **Campaign Period**: [Start Date] to [End Date]

## Authorization Checklist
- [ ] Written authorization from executive management
- [ ] Legal review completed
- [ ] HR notification and approval
- [ ] IT operations notified (email gateway whitelisting)
- [ ] Privacy impact assessment completed
- [ ] Data handling procedures documented

## Campaign Objectives
| Objective | Target Metric |
|---|---|
| Measure click susceptibility | Click rate < 10% |
| Measure credential submission | Submit rate < 5% |
| Measure reporting behavior | Report rate > 50% |
| Identify high-risk departments | Department-level breakdown |

## Scenario Design
- **Pretext**: [Password reset / IT maintenance / HR policy update]
- **Sender**: [it-support@company-domain.com]
- **Subject Line**: [Urgent: Password Expiration Notice]
- **Call to Action**: [Click link to reset password]
- **Landing Page**: [Fake login page mimicking internal portal]
- **Post-Interaction**: [Redirect to training page]

## Target Audience
| Group | Count | Department | Difficulty Level |
|---|---|---|---|
| Group A | | | |
| Group B | | | |

## GoPhish Configuration
### Sending Profile
```json
{
  "name": "Campaign SMTP Profile",
  "host": "smtp.server.com:587",
  "from_address": "IT Support <it-support@domain.com>",
  "username": "service-account",
  "ignore_cert_errors": false
}
```

### Email Template Variables
- `{{.FirstName}}` - Recipient first name
- `{{.LastName}}` - Recipient last name
- `{{.Position}}` - Recipient job title
- `{{.Email}}` - Recipient email
- `{{.From}}` - Sender address
- `{{.URL}}` - Phishing URL (tracked)
- `{{.Tracker}}` - Tracking pixel
- `{{.TrackingURL}}` - Full tracking URL
- `{{.RId}}` - Unique recipient ID

## Success Criteria
| Metric | Poor | Fair | Good | Excellent |
|---|---|---|---|---|
| Click Rate | >25% | 15-25% | 5-15% | <5% |
| Submit Rate | >15% | 8-15% | 3-8% | <3% |
| Report Rate | <10% | 10-30% | 30-60% | >60% |

## Post-Campaign Actions
- [ ] Generate campaign report
- [ ] Force password reset for credential submitters
- [ ] Send targeted training to clickers
- [ ] Send positive reinforcement to reporters
- [ ] Present aggregate findings to leadership
- [ ] Update training curriculum based on results
- [ ] Plan next campaign with adjusted difficulty
