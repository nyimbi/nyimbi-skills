# Performing False Positive Reduction In SIEM

## API Reference

## Libraries Used
- **csv**: Parse SIEM alert export files (Splunk, QRadar, Sentinel)
- **collections.Counter**: Aggregate alert patterns by rule, source, severity

## CLI Interface
```
python agent.py analyze --csv alerts.csv [--threshold 5]
python agent.py tune --csv alerts.csv
python agent.py simulate --csv alerts.csv [--disable-rules "Rule A" "Rule B"] [--whitelist-sources 10.0.0.1]
```

## Core Functions

### `analyze_alerts(csv_file, threshold)` — Identify false positive patterns
Parses alert CSV, calculates per-rule FP rates, identifies noisy rules exceeding threshold.
Returns: total alerts, FP count/rate, noisy rules ranked by FP rate, top FP sources.

### `generate_tuning_recommendations(csv_file)` — Create tuning action plan
Maps FP rates to actions: DISABLE (>=90%), ADD_WHITELIST (>=70%), TUNE_THRESHOLD (>=50%), REVIEW (<50%).

### `simulate_tuning_impact(csv_file, rules_to_disable, sources_to_whitelist)` — Model tuning changes
Calculates alert volume reduction and new FP rate after applying proposed rule disables and source whitelists.

## Expected CSV Columns
- `rule_name` / `Rule` / `alert_name`: Detection rule identifier
- `src_ip` / `source_ip` / `Source`: Source IP address
- `status` / `Status` / `disposition`: Alert disposition (false_positive, fp, closed_fp, benign)
- `severity` / `Severity`: Alert severity level

## FP Status Keywords
`false_positive`, `fp`, `closed_fp`, `benign`

## Dependencies
No external packages — Python standard library only.

---

## Standards and Controls

## Detection Quality Metrics (Industry Standards)

| Metric | Excellent | Good | Needs Improvement | Critical |
|---|---|---|---|---|
| False Positive Rate | < 10% | 10-20% | 20-40% | > 40% |
| Rule Precision | > 0.90 | 0.80-0.90 | 0.60-0.80 | < 0.60 |
| Mean Triage Time | < 5 min | 5-10 min | 10-20 min | > 20 min |
| Alert-to-Incident Ratio | 1:5 | 1:10 | 1:20 | > 1:50 |

## Tuning Frameworks

### NIST Continuous Monitoring (SP 800-137)
- Requires regular assessment and adjustment of detection capabilities
- Defines metrics-based approach to monitoring effectiveness

### SANS Detection Maturity Model
- Level 1: Basic alerts with high FP rate
- Level 2: Tuned alerts with correlation
- Level 3: Behavioral analytics reducing noise
- Level 4: Automated tuning with ML feedback loops

## Allowlist Management Standards
- All exclusions require documented justification
- Expiry dates mandatory (90-day maximum default)
- Quarterly review of all active exclusions
- Approval from detection engineering lead required

---

## Workflows

## Tuning Cycle
```
Identify Noisy Rules --> Analyze FP Root Causes --> Tune Rules -->
Validate with Testing --> Measure Improvement --> Report --> Repeat
```

## FP Analysis Categorization
| Category | Action | Example |
|---|---|---|
| Known benign | Add to allowlist | Vulnerability scanner IPs |
| Threshold too low | Raise threshold | Login failure count from 5 to 20 |
| Missing context | Add correlation | PowerShell + network = suspicious |
| Missing enrichment | Add lookup | Asset criticality context |
| Rule outdated | Rewrite or retire | Legacy detection no longer relevant |

---

## Working Template

## Rule Tuning Request

| Field | Value |
|---|---|
| Rule Name | |
| Current FP Rate | |
| Target FP Rate | |
| Alert Volume (30 days) | |
| Root Cause Category | Threshold / Missing context / Known benign / Outdated |

## FP Root Cause Analysis

| Sample # | Source | Classification | Root Cause | Recommended Fix |
|---|---|---|---|---|
| 1 | | FP | | |
| 2 | | FP | | |
| 3 | | FP | | |

## Tuning Action Plan

- [ ] Adjust threshold from ___ to ___
- [ ] Add allowlist entries for: ___
- [ ] Add correlation with: ___
- [ ] Add enrichment lookup: ___
- [ ] Test with Atomic Red Team: ___
- [ ] Validate FP rate improvement after 7 days
