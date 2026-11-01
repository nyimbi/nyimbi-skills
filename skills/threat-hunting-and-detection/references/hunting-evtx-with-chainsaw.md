# Hunting EVTX With Chainsaw

## API Reference

## Subcommands

| Command | Purpose |
|---------|---------|
| `hunt` | Detect threats using Sigma and Chainsaw rules |
| `search` | Keyword/regex/Tau search across artifacts |
| `analyse` | shimcache / srum / gaps artifact analysis |
| `dump` | Dump raw artifact content |
| `lint` | Validate rule files |

## hunt Flags

| Flag | Description |
|------|-------------|
| `-s, --sigma <DIR>` | SigmaHQ rules directory |
| `-r, --rule <DIR>` | Chainsaw rules directory |
| `-m, --mapping <FILE>` | Sigma->event field mapping (e.g. `mappings/sigma-event-logs-all.yml`) |
| `--level <LEVEL>` | Filter by Sigma rule level |
| `--status <STATUS>` | Filter by rule status (e.g. `stable`) |
| `--kind <KIND>` | Filter by detection kind (e.g. `evtx`) |
| `--json` / `--csv` | Output format |
| `-o, --output <PATH>` | Output file/directory |

```bash
chainsaw hunt ./evtx -s ./sigma/rules \
  --mapping ./mappings/sigma-event-logs-all.yml --level high --json
```

## search Flags

| Flag | Description |
|------|-------------|
| `-e, --regex <RE>` | Regex pattern |
| `-i, --ignore-case` | Case-insensitive |
| `-t, --tau <EXPR>` | Tau expression query |
| `--from` / `--to` | Timestamp bounds |
| `--json` | JSON output |

```bash
chainsaw search "mimikatz" -i ./evtx
chainsaw search -e "-enc\s+[A-Za-z0-9+/=]{20,}" ./evtx --json
chainsaw search ./evtx -t 'Event.System.EventID: =4624'
```

## analyse Subcommands

```bash
# Shimcache with Amcache timestamp pairing
chainsaw analyse shimcache ./SYSTEM --regexfile ./patterns.txt \
  --amcache ./Amcache.hve --tspair --output ./out.csv

# SRUM database
chainsaw analyse srum --software ./SOFTWARE ./SRUDB.dat -o srum.json

# Event-log gaps
chainsaw analyse gaps ./Logs/ --min-time-gap-minutes 30 --json
```

## dump / lint

```bash
chainsaw dump ./SOFTWARE --json --output dump.json
chainsaw lint -r ./rules --kind sigma
```

## Install

```bash
git clone https://github.com/WithSecureLabs/chainsaw.git
cd chainsaw && cargo build --release
# or: nix profile install github:WithSecureLabs/chainsaw
```

## External References

- Chainsaw: https://github.com/WithSecureLabs/chainsaw
- Sigma: https://github.com/SigmaHQ/sigma

---

## Standards and Controls

## MITRE ATT&CK References

| Technique ID | Name | Tactic | Rationale |
|-------------|------|--------|-----------|
| T1059.001 | Command and Scripting Interpreter: PowerShell | Execution | Sigma rules over EID 4104/4103 and search flag malicious PowerShell |
| T1059.003 | Command and Scripting Interpreter: Windows Command Shell | Execution | Process-creation Sigma rules surface suspicious cmd usage |
| T1547.001 | Boot or Logon Autostart Execution: Registry Run Keys / Startup Folder | Persistence | Registry-event Sigma rules flag persistence |
| T1053.005 | Scheduled Task/Job: Scheduled Task | Execution / Persistence | Rules over EID 4698/106 detect task creation |
| T1070.006 | Indicator Removal: Timestomp | Defense Evasion | `analyse gaps` and shimcache reveal time tampering |
| T1204.002 | User Execution: Malicious File | Execution | Shimcache analysis shows executed binaries |

## NIST Cybersecurity Framework 2.0

| ID | Name | Rationale |
|----|------|-----------|
| DE.AE-02 | Potentially adverse events are analyzed to better understand associated activities | Chainsaw hunts/searches analyze event-log activity to characterize threats |

## Detection Standards

- Sigma generic signature format: https://github.com/SigmaHQ/sigma
- Chainsaw mappings (Sigma->EVTX): https://github.com/WithSecureLabs/chainsaw/tree/master/mappings

## Official Resources

- Chainsaw GitHub: https://github.com/WithSecureLabs/chainsaw
- WithSecure Labs research: https://labs.withsecure.com/
- MITRE ATT&CK T1059.001: https://attack.mitre.org/techniques/T1059/001/

## Key Research

- WithSecure Labs: Chainsaw release announcements (shimcache, SRUM, gaps analysers)
- SigmaHQ community detection rule corpus
