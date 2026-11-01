# Implementing Mitre Attack Coverage Mapping

## API Reference

## ATT&CK Enterprise STIX Data

```bash
# Download latest ATT&CK STIX bundle
curl -sL "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json" -o attack.json
```

## ATT&CK Navigator Layer Format

```json
{
  "name": "Detection Coverage",
  "domain": "enterprise-attack",
  "versions": {"attack": "14", "navigator": "4.9.1"},
  "techniques": [
    {"techniqueID": "T1566", "score": 3, "color": "#80b1d3"}
  ]
}
```

## ATT&CK Tactics (Enterprise)

| ID | Tactic | Example Technique |
|----|--------|------------------|
| TA0001 | Initial Access | T1566 Phishing |
| TA0002 | Execution | T1059 Command Interpreter |
| TA0003 | Persistence | T1053 Scheduled Task |
| TA0004 | Privilege Escalation | T1078 Valid Accounts |
| TA0005 | Defense Evasion | T1027 Obfuscation |
| TA0006 | Credential Access | T1003 OS Credential Dumping |
| TA0008 | Lateral Movement | T1021 Remote Services |
| TA0011 | Command and Control | T1071 Application Layer Protocol |

## Coverage Score

| Score | Meaning | Color |
|-------|---------|-------|
| 0 | No detection | White |
| 1 | Single rule | Yellow |
| 2 | Multiple rules | Green |
| 3 | Good coverage | Blue |
| 4+ | Excellent | Red |

### References

- MITRE ATT&CK: https://attack.mitre.org/
- ATT&CK Navigator: https://mitre-attack.github.io/attack-navigator/
- ATT&CK STIX Data: https://github.com/mitre/cti

---

## Standards and Controls

## MITRE ATT&CK Framework

- Current version: v18.1 (December 2025)
- 14 Tactics, 200+ Techniques, 400+ Sub-Techniques
- Domains: Enterprise, Mobile, ICS

### Tactics (Kill Chain Order)
1. Reconnaissance (TA0043)
2. Resource Development (TA0042)
3. Initial Access (TA0001)
4. Execution (TA0002)
5. Persistence (TA0003)
6. Privilege Escalation (TA0004)
7. Defense Evasion (TA0005)
8. Credential Access (TA0006)
9. Discovery (TA0007)
10. Lateral Movement (TA0008)
11. Collection (TA0009)
12. Command and Control (TA0011)
13. Exfiltration (TA0010)
14. Impact (TA0040)

## Detection Maturity Model

| Level | Description |
|---|---|
| L0 | No detection capability for the technique |
| L1 | Basic log collection for relevant data sources |
| L2 | Detection rule deployed but not validated |
| L3 | Validated detection with known false positive rate |
| L4 | Automated testing and continuous validation |
| L5 | Behavioral detection with ML-based anomaly detection |

## Related Frameworks
- MITRE D3FEND (Defensive techniques)
- MITRE ATT&CK Data Sources
- NIST CSF Detection function
- SANS Detection Maturity Level model

---

## Workflows

## Quarterly Coverage Assessment Workflow

```
1. Export all active SIEM detection rules
   |
   v
2. Map each rule to MITRE ATT&CK technique(s)
   |
   v
3. Score each technique (0-100)
   |
   v
4. Generate ATT&CK Navigator heatmap
   |
   v
5. Identify top 10 gap techniques
   |
   v
6. Prioritize based on threat landscape
   |
   v
7. Create detection engineering backlog
   |
   v
8. Build and deploy new rules
   |
   v
9. Validate with adversary emulation
   |
   v
10. Update coverage map
```

## Continuous Improvement Cycle

```
Assess Coverage --> Identify Gaps --> Prioritize -->
Build Rules --> Test Rules --> Deploy --> Validate -->
Measure --> Report --> Repeat
```

## Gap Closure Tracking

| Week | New Rules | Techniques Covered | Coverage Delta |
|---|---|---|---|
| 1 | 3 | T1059, T1055, T1003 | +1.5% |
| 2 | 2 | T1053, T1547 | +1.0% |
| 3 | 3 | T1071, T1105, T1048 | +1.5% |
| 4 | 2 | T1218, T1036 | +1.0% |

---

## Working Template

## Assessment Metadata

| Field | Value |
|---|---|
| Organization | |
| Assessment Date | |
| Assessor | |
| ATT&CK Version | v18.1 |
| SIEM Platform | |
| Total Active Rules | |

## Coverage Summary

| Metric | Value |
|---|---|
| Total Techniques Evaluated | |
| Techniques with Detection | |
| Coverage Percentage | |
| Average Detection Score | |
| Critical Gaps (Score 0) | |

## Top 10 Gap Techniques

| Priority | Technique ID | Name | Tactic | Current Score | Remediation Plan |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

## Detection Roadmap

### Q1 Goals
- [ ] Close top 5 critical gaps
- [ ] Enable missing data sources for priority techniques
- [ ] Validate top 10 existing rules with adversary emulation

### Q2 Goals
- [ ] Improve partial coverage techniques to score > 75
- [ ] Add enrichment to existing detection rules
- [ ] Implement detection-as-code pipeline
