# Triaging Windows With Kape

## API Reference

KAPE has two execution phases: **Target** (collection) and **Module** (processing). Switches use `--` prefix. `kape.exe` is the CLI; `gkape.exe` is the GUI.

## Target (collection) switches

| Switch | Required | Description |
|--------|----------|-------------|
| `--tsource` | yes | Source drive/volume to copy from (e.g. `C:`, `D:`, `F:\`) |
| `--target` | yes | Target/compound target name(s), comma-separated (e.g. `KapeTriage`, `!SANS_Triage`, `RegistryHives,EventLogs`) |
| `--tdest` | yes | Destination directory for collected files |
| `--tflush` | no | Delete contents of `--tdest` before copy |
| `--vss` | no | Process all Volume Shadow Copies on `--tsource` (default false) |
| `--vhdx <name>` | no | Create a VHDX container from `--tdest`; value is a base identifier, not a filename |
| `--vhd <name>` | no | Create a VHD container instead of VHDX |
| `--zip <name>` | no | Create a ZIP of the collection |
| `--zv` | no | Add `--tdest` to container then delete originals (true/false) |

## Module (processing) switches

| Switch | Required | Description |
|--------|----------|-------------|
| `--module` | yes | Module/compound module name(s) (e.g. `!EZParser`, `PECmd`, `MFTECmd`) |
| `--mdest` | yes | Destination for parsed module output (CSV/JSON/HTML) |
| `--msource` | no | Source data for processing (defaults to `--tdest` if collecting+processing) |
| `--mflush` | no | Delete contents of `--mdest` before processing |
| `--mef` | no | Module export format override |

## Global / utility switches

| Switch | Description |
|--------|-------------|
| `--sync` | Update Targets and Modules from the KapeFiles GitHub repo |
| `--tlist` | List all available Targets |
| `--mlist` | List all available Modules |
| `--gui` | Open progress in GUI window when launched from CLI |
| `--debug` | Verbose debug logging |
| `--trace` | Even more verbose tracing |

## Example command lines

```cmd
REM Triage collection
kape.exe --tsource C: --target KapeTriage --tdest E:\out\tdest --tflush

REM Collection with VSS + VHDX container
kape.exe --tsource C: --target !SANS_Triage --tdest E:\out\tdest --vss --vhdx HOST01 --tflush

REM Process an existing collection with all EZ Tools
kape.exe --msource E:\out\tdest\C --mdest E:\out\mdest --module !EZParser --mflush

REM Collect and parse in one run
kape.exe --tsource C: --target KapeTriage --tdest E:\out\tdest --mdest E:\out\mdest --module !EZParser --tflush --mflush
```

## Batch mode

Place a `_kape.cli` file beside `kape.exe`. Each non-comment line is one full argument set; run `kape.exe` with no args to execute all lines.
Variables: `%d` = KAPE directory, `%m` = machine name.

```
--tsource C: --target KapeTriage --tdest %d\Disk\%m --vhdx %m
```

## Config file types

| Extension | Purpose |
|-----------|---------|
| `.tkape` | Target definition (what to collect) |
| `.mkape` | Module definition (how to process) |
| `_kape.cli` | Batch command file |

## Output logs (chain of custody)

- `<timestamp>_CopyLog.csv` — every file copied with source/dest and SHA-1
- `<timestamp>_ConsoleLog.txt` — full console output
- `<timestamp>_SkipLog.csv` — files skipped and why

---

## Standards and Controls

## NIST Cybersecurity Framework 2.0

| ID | Name | Rationale |
|----|------|-----------|
| RS.AN-03 | Analysis is performed to establish what has taken place during an incident and the root cause of the incident | KAPE rapidly collects and parses host artifacts (execution, persistence, account, file-system) that establish the sequence of attacker activity and root cause during incident response. |

## MITRE ATT&CK

| ID | Name | Rationale |
|----|------|-----------|
| T1005 | Data from Local System | KAPE acquires forensic data directly from the local file system; this same data source is what adversaries target with T1005 and what responders must preserve and analyze. |

## Supporting References

- KAPE Documentation (Eric Zimmerman / Kroll): https://ericzimmerman.github.io/KapeDocs/
- KapeFiles Targets/Modules: https://github.com/EricZimmerman/KapeFiles
- SANS DFIR — KAPE: https://www.sans.org/tools/kape/
- NIST SP 800-86 Guide to Integrating Forensic Techniques into Incident Response
- NIST SP 800-61r2 Computer Security Incident Handling Guide
