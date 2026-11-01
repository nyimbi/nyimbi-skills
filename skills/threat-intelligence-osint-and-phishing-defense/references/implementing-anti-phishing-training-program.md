# Implementing Anti Phishing Training Program

## API Reference

## KnowBe4 API

```python
import requests

headers = {"Authorization": "Bearer <API_KEY>"}
base = "https://us.api.knowbe4.com/v1"

# List users
users = requests.get(f"{base}/users", headers=headers).json()

# Get phishing campaign results
campaigns = requests.get(f"{base}/phishing/campaigns", headers=headers).json()

# Get training enrollments
enrollments = requests.get(f"{base}/training/enrollments", headers=headers).json()
```

## Key Metrics

| Metric | Target | Calculation |
|--------|--------|-------------|
| Click Rate | < 15% | Clicked / Total Recipients |
| Submit Rate | < 5% | Submitted Creds / Total |
| Report Rate | > 70% | Reported / Total Recipients |
| Completion Rate | > 90% | Completed / Enrolled |

## pandas Simulation Analysis

```python
import pandas as pd
df = pd.read_csv("simulation_results.csv", parse_dates=["timestamp"])

# Department click rates
dept = df.groupby("department").agg(
    click_rate=("clicked", "mean"),
    report_rate=("reported", "mean"),
)

# Monthly trend
monthly = df.set_index("timestamp").resample("M")["clicked"].mean()
```

## SANS Maturity Model Levels

| Level | Name | Description |
|-------|------|-------------|
| 1 | Non-existent | No program |
| 2 | Compliance | Annual checkbox |
| 3 | Awareness | Engaging, regular |
| 4 | Sustainment | Culture change |
| 5 | Metrics | Risk-based optimization |

## GoPhish (Open-Source Alternative)

```bash
# Launch campaign
curl -X POST https://gophish:3333/api/campaigns \
  -H "Authorization: <API_KEY>" \
  -d '{"name":"Q1-2025","template":{"name":"IT Alert"},"groups":[{"name":"All Staff"}]}'
```

### References

- KnowBe4 API: https://developer.knowbe4.com/
- GoPhish: https://getgophish.com/
- SANS Security Awareness: https://www.sans.org/security-awareness-training/

---

## Standards and Controls

## NIST Guidelines
- **NIST SP 800-50**: Building an Information Technology Security Awareness and Training Program
- **NIST SP 800-16**: Information Technology Security Training Requirements
- **NIST SP 800-53 Rev.5**: AT-1 through AT-6 - Awareness and Training family

## Regulatory Requirements
- **PCI DSS 4.0**: Requirement 12.6 - Security awareness training for all personnel
- **HIPAA**: 45 CFR 164.308(a)(5) - Security awareness and training
- **SOX**: Section 404 - Internal controls requiring security awareness
- **GDPR**: Article 39(1)(b) - Data protection awareness training
- **CMMC 2.0**: AT.L2-3.2.1/2/3 - Awareness and training practices
- **FFIEC**: Information Security Handbook - Security awareness training

## Industry Frameworks
- **SANS Security Awareness Maturity Model**: Five-level maturity assessment
- **AISA Phishing Resilience Protocol**: Australian standard for phishing testing
- **CISA Cybersecurity Awareness Program**: Federal awareness guidance

## MITRE ATT&CK Techniques Addressed by Training
- **T1566**: Phishing (all sub-techniques)
- **T1598**: Phishing for Information
- **T1204**: User Execution
- **T1534**: Internal Spearphishing

## Key Performance Indicators (KPIs)

| KPI | Description | Target |
|---|---|---|
| Phish-Prone Percentage | Users who click simulated phishing | < 5% |
| Training Completion Rate | Users completing assigned modules | > 95% |
| Report Rate | Users reporting simulated phishing | > 70% |
| Time to Report | Average time to report phishing | < 5 minutes |
| Repeat Offender Rate | Users failing multiple simulations | < 2% |
| Training Satisfaction | Post-training survey score | > 4/5 |
| Knowledge Assessment Score | Quiz/test average score | > 85% |

## Training Content Categories
1. Email phishing identification
2. Business email compromise (BEC)
3. Spearphishing and whaling
4. Vishing (voice phishing)
5. Smishing (SMS phishing)
6. QR code phishing (quishing)
7. Social media phishing
8. Credential harvesting
9. Malicious attachments
10. USB/physical social engineering

---

## Workflows

## Workflow 1: Annual Program Lifecycle

```
Q1: Baseline & Planning
  +-- Run baseline phishing simulation
  +-- Assess current awareness maturity level
  +-- Define annual targets and KPIs
  +-- Select/renew training platform
  +-- Design curriculum by role and department
  |
Q2: Foundation Training
  +-- Deploy core phishing awareness modules
  +-- Run monthly simulations (easy difficulty)
  +-- Launch phishing report button
  +-- Begin tracking metrics
  |
Q3: Advanced Training
  +-- Role-specific training (finance, IT, executives)
  +-- Increase simulation difficulty
  +-- Recognize security champions
  +-- Mid-year metrics review
  |
Q4: Assessment & Optimization
  +-- Run year-end assessment simulation
  +-- Compare against baseline
  +-- Generate annual report
  +-- Identify gaps for next year
  +-- Present ROI to leadership
```

## Workflow 2: Just-in-Time Training Flow

```
User interacts with simulated phishing email
  |
  v
[Did user click the link?]
  |
  +-- NO (ignored or reported) --> Positive outcome tracked
  |     |
  |     +-- [Did user report it?]
  |           +-- YES --> Send congratulations, award points
  |           +-- NO --> No action (not a failure)
  |
  +-- YES (clicked link)
       |
       v
  [Landing page shows "This was a test"]
       |
       v
  [Immediate micro-training module (2-3 min)]
       +-- What red flags were present
       +-- How to identify similar emails
       +-- How to report suspicious emails
       |
       v
  [Auto-enroll in refresher course within 7 days]
       |
       v
  [Manager receives aggregate report (not individual names)]
       |
       v
  [User included in next simulation cycle]
```

## Workflow 3: Repeat Offender Escalation

```
User fails first simulation
  |
  +-- Standard just-in-time training
  +-- Auto-enrolled in awareness module
  |
User fails second simulation (within 6 months)
  |
  +-- Enhanced training assignment
  +-- One-on-one coaching session offered
  +-- Manager notification (private)
  |
User fails third simulation
  |
  +-- Mandatory extended training
  +-- Access restrictions considered (additional MFA, restricted permissions)
  +-- HR involvement per policy
  +-- Monthly targeted simulations
  |
User passes subsequent simulation
  |
  +-- Return to normal simulation schedule
  +-- Positive reinforcement
```

## Workflow 4: Metrics-Driven Optimization

```
Monthly Data Collection
  |
  +-- Simulation results (click, submit, report rates)
  +-- Training completion rates
  +-- User-reported real phishing volume
  +-- Help desk phishing tickets
  |
  v
[Analyze by dimensions]
  +-- Department breakdown
  +-- Role/seniority breakdown
  +-- Location breakdown
  +-- Trend over time
  |
  v
[Identify patterns]
  +-- Which departments are improving?
  +-- Which scenarios are most effective?
  +-- Are repeat offenders decreasing?
  +-- Is report rate increasing?
  |
  v
[Adjust program]
  +-- Increase difficulty for high-performing groups
  +-- More training for struggling departments
  +-- New scenario types for common gaps
  +-- Update content for new threat trends
```

---

## Working Template

## Program Overview
- **Organization**: [Company Name]
- **Program Owner**: [CISO / Security Awareness Manager]
- **Start Date**: [YYYY-MM-DD]
- **Review Cycle**: [Quarterly / Semi-annual]

## Baseline Metrics
| Metric | Current Value | 6-Month Target | 12-Month Target |
|---|---|---|---|
| Phish Click Rate | % | % | <5% |
| Submit Rate | % | % | <2% |
| Report Rate | % | % | >60% |
| Training Completion | % | 90% | 95% |
| Repeat Offenders | % | % | <3% |

## Training Curriculum
| Module | Audience | Duration | Frequency | Platform |
|---|---|---|---|---|
| Phishing Basics | All employees | 15 min | Annual + new hire | |
| BEC/Wire Fraud | Finance | 20 min | Quarterly | |
| Executive Threats | C-suite/VPs | 10 min | Quarterly | |
| IT-Targeted Phishing | IT Staff | 20 min | Quarterly | |
| Credential Protection | All employees | 10 min | Semi-annual | |
| Mobile Threats (Smishing) | All employees | 10 min | Annual | |

## Simulation Schedule
| Month | Scenario Type | Difficulty | Target Group |
|---|---|---|---|
| Jan | Password reset | Easy | All employees |
| Feb | Vendor invoice | Medium | Finance |
| Mar | IT notification | Easy | All employees |
| Apr | Package delivery | Easy | All employees |
| May | Executive request | Hard | Finance + Admin |
| Jun | Cloud storage share | Medium | All employees |
| Jul | HR policy update | Easy | All employees |
| Aug | Tax document | Medium | All employees |
| Sep | Conference invite | Medium | All employees |
| Oct | Security alert | Hard | IT Staff |
| Nov | Benefits enrollment | Medium | All employees |
| Dec | Holiday promotion | Hard | All employees |

## Escalation Policy for Repeat Offenders
| Offense | Action | Responsible |
|---|---|---|
| First click | Just-in-time training + auto-enroll in module | Automated |
| Second click | Enhanced training + coaching offer | Security team |
| Third click | Mandatory training + manager notification | HR + Security |
| Fourth+ click | Access review + remediation plan | HR + IT + Security |

## Budget
| Item | Annual Cost |
|---|---|
| Training platform license | $ |
| Simulation platform | $ |
| Content development | $ |
| Program administration | $ |
| Rewards/recognition | $ |
| **Total** | **$** |

## Reporting Schedule
- **Monthly**: Simulation results to security team
- **Quarterly**: Department-level report to leadership
- **Annually**: Full program assessment and ROI report to board
