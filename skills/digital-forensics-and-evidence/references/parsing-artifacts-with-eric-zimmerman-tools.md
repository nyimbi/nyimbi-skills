# Parsing Artifacts With Eric Zimmerman Tools

## API Reference

All tools are .NET CLI parsers that emit CSV/JSON. Common flags: `-f` (single file), `-d` (directory recurse), `--csv` (output dir), `--csvf` (output filename), `--json` (JSON output dir).

## MFTECmd

| Flag | Purpose |
|------|---------|
| `-f` | Path to `$MFT`, `$J`, `$Boot`, `$SDS`, or `$LogFile` |
| `--csv` / `--csvf` | CSV output dir / filename |
| `--json` | JSON output dir |
| `--de <entry>` | Dump a specific MFT entry |

```cmd
MFTECmd.exe -f "C:\$MFT" --csv "C:\out" --csvf MFT.csv
MFTECmd.exe -f "C:\$Extend\$J" --csv "C:\out" --csvf UsnJrnl.csv
```

## PECmd (Prefetch)

| Flag | Purpose |
|------|---------|
| `-f` / `-d` | Single `.pf` / directory |
| `--csv` / `--csvf` / `--json` | Outputs |
| `-k <keywords>` | Highlight keywords |

```cmd
PECmd.exe -d "C:\Windows\Prefetch" --csv "C:\out" --csvf Prefetch.csv --json "C:\out\json"
```

## RECmd (Registry)

| Flag | Purpose |
|------|---------|
| `-f` / `-d` | Single hive / directory of hives |
| `--bn <file>` | Batch file (.reb), e.g. `Kroll_Batch.reb` |
| `--sk <value>` | Search keys/values |
| `--csv` / `--csvf` | Outputs |

```cmd
RECmd.exe -d "C:\config" --bn "RECmd\BatchExamples\Kroll_Batch.reb" --csv "C:\out"
```

## SBECmd (ShellBags)

```cmd
SBECmd.exe -d "C:\Users\jsmith" --csv "C:\out"
```

## AmcacheParser

| Flag | Purpose |
|------|---------|
| `-f` | Path to `Amcache.hve` |
| `-i` | Include unassociated file entries |
| `--csv` | Output dir |

```cmd
AmcacheParser.exe -f "C:\Windows\AppCompat\Programs\Amcache.hve" --csv "C:\out" -i
```

## AppCompatCacheParser (ShimCache)

```cmd
AppCompatCacheParser.exe -f "C:\Windows\System32\config\SYSTEM" --csv "C:\out"
```

## LECmd / JLECmd (LNK / Jump Lists)

```cmd
LECmd.exe  -d "C:\Users\jsmith\AppData\Roaming\Microsoft\Windows\Recent" --csv "C:\out"
JLECmd.exe -d "...\Recent\AutomaticDestinations" --csv "C:\out"
```

## EvtxECmd (EVTX)

```cmd
EvtxECmd.exe -d "C:\Windows\System32\winevt\Logs" --csv "C:\out" --csvf EventLogs.csv
```

## Get-ZimmermanTools (downloader)

```powershell
.\Get-ZimmermanTools.ps1 -Dest C:\Tools\EZ
```

## Timeline Explorer

GUI CSV viewer: `TimelineExplorer.exe`. Loads EZ Tools CSVs; supports column filters, conditional formatting, and tagging for cross-artifact correlation on UTC timestamps.

---

## Standards and Controls

## NIST Cybersecurity Framework 2.0

| ID | Name | Rationale |
|----|------|-----------|
| RS.AN-03 | Analysis is performed to establish what has taken place during an incident and the root cause of the incident | EZ Tools parse Windows artifacts (MFT, prefetch, registry, shellbags, amcache) into structured evidence that establishes attacker execution, access, and persistence during incident analysis. |

## MITRE ATT&CK

| ID | Name | Rationale |
|----|------|-----------|
| T1112 | Modify Registry | RECmd, AmcacheParser, and AppCompatCacheParser parse registry artifacts where adversary registry modifications (persistence, evasion) are recorded and recovered. |

## Supporting References

- Eric Zimmerman's Tools: https://ericzimmerman.github.io/
- Get-ZimmermanTools: https://github.com/EricZimmerman/Get-ZimmermanTools
- SANS — Running EZ Tools Natively on Linux: https://www.sans.org/blog/running-ez-tools-natively-on-linux-a-step-by-step-guide
- NIST SP 800-86 Guide to Integrating Forensic Techniques into Incident Response
- NIST SP 800-101r1 Guidelines on Mobile Device Forensics (artifact methodology reference)
