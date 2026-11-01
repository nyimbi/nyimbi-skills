# Generating Forensic Timelines With Hayabusa

## API Reference

## Subcommands

| Command | Purpose |
|---------|---------|
| `csv-timeline` | Build a CSV forensic timeline |
| `json-timeline` | Build a JSON/JSONL timeline |
| `update-rules` | Sync the latest Sigma/Hayabusa rules |
| `search` | Keyword/regex search across event logs |
| `level-tuning` | Customize alert severity per rule |
| `computer-metrics` | Event counts per computer |
| `eid-metrics` | Event counts/percentages per Event ID |
| `log-metrics` | File metadata (timestamps, channels, providers) |
| `pivot-keywords-list` | Extract suspicious keywords for correlation |

## Common Timeline Flags

| Flag | Description |
|------|-------------|
| `-d, --directory <DIR>` | Directory of `.evtx` files |
| `-f, --file <FILE>` | Single `.evtx` file |
| `-l, --live-analysis` | Analyze local Windows event logs (admin) |
| `-o, --output <FILE>` | Output path |
| `-p, --profile <PROFILE>` | Output profile (see below) |
| `-m, --min-level <LEVEL>` | Minimum alert level |
| `-w, --no-wizard` | Skip interactive wizard (scripting) |
| `-U, --UTC` | Output timestamps in UTC |
| `-L` (json-timeline) | JSONL (one object per line) |

## Output Profiles

`minimal`, `standard` (default), `verbose`, `all-field-info`,
`all-field-info-verbose`, `super-verbose`, `timesketch-minimal`, `timesketch-verbose`

## Alert Levels

`informational`, `low`, `medium`, `high`, `critical`

## search Flags

| Flag | Description |
|------|-------------|
| `-k, --keyword <KW>` | Keyword to match |
| `-r, --regex <RE>` | Regex to match |
| `-i, --ignore-case` | Case-insensitive |
| `-d, --directory <DIR>` | Logs directory |

## Examples

```bash
hayabusa update-rules
hayabusa csv-timeline -d ./evtx -o tl.csv -p verbose -m high -U -w
hayabusa json-timeline -d ./evtx -L -o tl.jsonl -w
hayabusa search -d ./evtx -k "mimikatz" -i
hayabusa eid-metrics -d ./evtx -o eid.csv
hayabusa pivot-keywords-list -d ./evtx -m medium -o pivots
```

## External References

- Hayabusa Wiki: https://github.com/Yamato-Security/hayabusa/wiki
- Releases: https://github.com/Yamato-Security/hayabusa/releases

---

## Standards and Controls

## MITRE ATT&CK References

| Technique ID | Name | Tactic | Rationale |
|-------------|------|--------|-----------|
| T1059.001 | Command and Scripting Interpreter: PowerShell | Execution | Sigma rules over EID 4104/4103/Sysmon flag malicious PowerShell |
| T1059.003 | Command and Scripting Interpreter: Windows Command Shell | Execution | Process-creation rules surface suspicious cmd usage |
| T1078 | Valid Accounts | Defense Evasion / Persistence | Logon events (4624/4625/4672) reveal anomalous auth |
| T1547.001 | Boot or Logon Autostart Execution: Registry Run Keys / Startup Folder | Persistence | Registry-modification rules flag persistence |
| T1053.005 | Scheduled Task/Job: Scheduled Task | Execution / Persistence | EID 4698/106 rules surface task creation |
| T1003 | OS Credential Dumping | Credential Access | Rules flag LSASS access patterns |

## NIST Cybersecurity Framework 2.0

| ID | Name | Rationale |
|----|------|-----------|
| RS.AN-03 | Analysis is performed to establish what has taken place during an incident and the root cause | Hayabusa timelines reconstruct the sequence of events during IR analysis |

## Detection Standards

- Sigma generic signature format: https://github.com/SigmaHQ/sigma
- Hayabusa rules (Sigma + Hayabusa-native): https://github.com/Yamato-Security/hayabusa-rules

## Official Resources

- Hayabusa GitHub: https://github.com/Yamato-Security/hayabusa
- Usage Examples Wiki: https://github.com/Yamato-Security/hayabusa/wiki/Usage-Examples
- Timeline Output Wiki: https://github.com/Yamato-Security/hayabusa/wiki/Timeline-Output
- Takajō analyzer: https://github.com/Yamato-Security/takajo
- MITRE ATT&CK T1059.001: https://attack.mitre.org/techniques/T1059/001/

## Key Research

- Yamato Security: Hayabusa documentation and AnalysisWithJQ guide
- Timesketch integration via timesketch-minimal / timesketch-verbose profiles
