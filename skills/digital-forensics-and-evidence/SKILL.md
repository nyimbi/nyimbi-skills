---
name: digital-forensics-and-evidence
description: >-
  Acquire, preserve, and interpret digital evidence so the result
  survives scrutiny: forensically sound disk and memory imaging with
  hash verification and chain of custody, Windows/Linux/Mac artifact
  parsing (registry, MFT, prefetch, Amcache, shellbags, LNK, USB
  history, browser, email, SQLite), file carving and deleted-file
  recovery, super-timeline reconstruction with Plaso and Timesketch,
  network PCAP analysis, cloud and container evidence acquisition, and
  mobile device extraction. Use when the user asks to "image this
  drive", "recover deleted files", "build a timeline of what happened
  on this host", "extract browser history", "preserve evidence before
  we reimage", "acquire the cloud snapshot", "analyze this memory dump",
  or "prove who plugged in this USB". Do not use for responding to and
  containing a live compromise (see security-incident-response-and-soc),
  for proactive searching before an event is alleged (see
  threat-hunting-and-detection), or for dissecting a malware sample (see
  malware-analysis-and-reverse-engineering).
license: Apache-2.0
---

# Digital Forensics and Evidence

Evidence fails in court and in post-mortems for procedural reasons far
more often than analytical ones: an unhashed image, a write-blocker
never verified, a workstation wiped before the legal hold, a timeline
built on local timestamps with no timezone recorded. This skill treats
acquisition discipline as the first-class deliverable and analysis as
the second — a brilliant finding from a broken chain of custody is
worthless.

Analyze copies, never originals. Record what you did, when, and with
which hash, while you do it — reconstructing custody afterwards is the
one task that cannot be done later.

## When to use

- Acquiring a disk, container, or memory image before reimaging,
  remediation, or return of a device to the user
- Establishing what happened on a host: execution, file access,
  logins, USB connections, browsing, and deletions
- Recovering deleted or hidden content from MFT slack, unallocated
  space, recycle bin, shadow copies, SQLite freelists/WAL, or carved
  fragments
- Building a defensible super-timeline across file system, event logs,
  registry, and application artifacts
- Parsing Windows artifacts (registry hives, prefetch, Amcache,
  shellbags, LNK/jump lists, EVTX) or Linux artifacts (auth logs,
  cron, journal, auditd)
- Analyzing network packet captures for exfiltration, C2, or data
  transfers
- Collecting evidence from cloud accounts, object storage, Docker
  containers, or mobile devices where data is ephemeral
- Answering "did the user actually do this?" with artifact-level
  citations rather than recollection

**Do not use for** — `security-incident-response-and-soc` when the
compromise is active and the priority is containment and recovery
(that skill captures volatile evidence in-flight, then hands deep
analysis here); `threat-hunting-and-detection` when no event is alleged
and the job is proactive searching or detection authoring;
`malware-analysis-and-reverse-engineering` when a sample has been
seized and the question is what the sample does rather than what the
host did. Mobile-device extraction in a corporate HR matter also needs
`identity-zero-trust-and-endpoint-security` for the access policy side.

## Workflow

1. **Establish authority, scope, and the legal hold.** Confirm written
   authorization, the systems and date range in scope, privacy and
   jurisdiction constraints (especially cross-border cloud data), and
   issue a legal hold that suspends normal destruction. Output: case
   file with scope, authority reference, and evidence log opened.

2. **Capture volatile state first, in order of volatility.** Before
   touching disk: memory (winpmem/DumpIt/LiME), network connections,
   running processes, open files, mounted shares, logged-on users,
   captured on the live system. Output: memory image plus a live
   triage bundle, each hashed at capture.

3. **Acquire forensically sound images.** Write-block (hardware or
   verified software), hash the source before imaging, image with
   `dcfldd`/`dd` (or KAPE/FTK Imager for targeted collection),
   hash the image and re-hash the source after, and verify all three
   match. Output: bit-for-bit image or verified triage collection with
   matching SHA-256 values recorded.

4. **Record chain of custody for every item.** For each artifact:
   who collected it, when, from where, hash, current storage location,
   and every transfer of possession. Output: custody entries that
   close with the hashes from step 3.

5. **Parse artifacts against the question.** Choose parsers by
   question, not habit — execution → prefetch/Amcache/shimcache;
   persistence → registry hives and task/WMI artifacts; user activity
   → shellbags, LNK, jump lists, UserAssist, browser history; USB →
   USBSTOR/MountedDevices/SetupAPI; deleted content → MFT, USN journal,
   `$LogFile`, carving. Work on copies; hash parser inputs and
   outputs. Output: extracted artifact set with source paths.

6. **Build the super-timeline and correlate.** Normalize every
   timestamp to UTC with its source and timezone offset, run
   log2timeline/psort (or Hayabusa for EVTX), load into Timesketch or
   Timeline Explorer, and anchor the analysis on pivot points (first
   known malicious event) rather than reading chronologically from
   zero. Output: unified timeline with the incident window marked.

7. **Validate findings against independent artifacts.** Every
   conclusion must be corroborated by a second artifact class (e.g.,
   prefetch execution confirmed by Amcache or event logs; a deletion
   shown in both MFT flags and `$LogFile` redo/undo). Output:
   findings with evidence citations and confidence.

8. **Report with the custody trail attached.** Output: forensic report
   — scope, methods, hashes, timeline, findings (fact vs. inference
   labeled separately), and the evidence index.

## Quality bar

- [ ] Written authorization and legal hold exist before acquisition,
      and the scope (systems, date range, data categories) is recorded
- [ ] Volatile evidence was captured before shutdown, imaging, or
      remediation, with capture time logged
- [ ] Source hash before imaging, image hash, and source hash after
      imaging all match; the values are in the evidence log
- [ ] Write-blocking was verified (not assumed) and every analysis was
      performed on a copy, with the original untouched after sealing
- [ ] Chain of custody entries exist for every item: collector, time,
      source, hash, storage, transfers
- [ ] All timeline timestamps carry a timezone and are normalized to
      UTC; clock skew against a known reference is noted
- [ ] Each finding cites the artifact, parser, and file path that
      supports it, and separates observed fact from inference
- [ ] Deleted/carved content is validated (header/footer signature,
      sane size, known-good filtering) before being called evidence
- [ ] Ephemeral sources (cloud instances, containers, mobile devices)
      were preserved before they could be destroyed or rotated
- [ ] The report is reproducible: another examiner could re-run the
      documented commands and hashes and reach the same result

## Reference map

All 41 merged techniques, with descriptions, are catalogued in
[`references/technique-index.md`](references/technique-index.md).
Near-duplicate techniques keep their own reference files; each group
below is one topic.

| Situation | Open |
|---|---|
| Bit-for-bit disk imaging with dd/dcfldd and hash verification | [acquiring-disk-image-with-dd-and-dcfldd](references/acquiring-disk-image-with-dd-and-dcfldd.md) |
| Targeted Windows triage collection and module parsing | [triaging-windows-with-kape](references/triaging-windows-with-kape.md) |
| EZ Tools suite across registry, prefetch, LNK, MFT (near-duplicate pair — one topic) | [performing-windows-artifact-analysis-with-eric-zimmerman-tools](references/performing-windows-artifact-analysis-with-eric-zimmerman-tools.md) · [parsing-artifacts-with-eric-zimmerman-tools](references/parsing-artifacts-with-eric-zimmerman-tools.md) |
| Registry hives: persistence, UserAssist, MRU, system config | [analyzing-windows-registry-for-artifacts](references/analyzing-windows-registry-for-artifacts.md) |
| $MFT, USN journal, `$LogFile`, slack space, deleted-file metadata | [analyzing-mft-for-deleted-file-recovery](references/analyzing-mft-for-deleted-file-recovery.md) · [analyzing-slack-space-and-file-system-artifacts](references/analyzing-slack-space-and-file-system-artifacts.md) |
| Carving files from images or unallocated space | [performing-file-carving-with-foremost](references/performing-file-carving-with-foremost.md) · [recovering-deleted-files-with-photorec](references/recovering-deleted-files-with-photorec.md) |
| Program execution history: prefetch and Amcache | [analyzing-prefetch-files-for-execution-history](references/analyzing-prefetch-files-for-execution-history.md) · [analyzing-windows-prefetch-with-python](references/analyzing-windows-prefetch-with-python.md) · [analyzing-windows-amcache-artifacts](references/analyzing-windows-amcache-artifacts.md) |
| File access evidence: LNK, jump lists, shellbags | [analyzing-lnk-file-and-jump-list-artifacts](references/analyzing-lnk-file-and-jump-list-artifacts.md) · [analyzing-windows-lnk-files-for-artifacts](references/analyzing-windows-lnk-files-for-artifacts.md) · [analyzing-windows-shellbag-artifacts](references/analyzing-windows-shellbag-artifacts.md) |
| USB device connection history and user association | [analyzing-usb-device-connection-history](references/analyzing-usb-device-connection-history.md) |
| Super-timeline generation and collaborative review | [performing-timeline-reconstruction-with-plaso](references/performing-timeline-reconstruction-with-plaso.md) · [building-super-timelines-with-plaso](references/building-super-timelines-with-plaso.md) · [generating-forensic-timelines-with-hayabusa](references/generating-forensic-timelines-with-hayabusa.md) |
| Memory dump analysis, credential recovery, rootkit detection | [performing-memory-forensics-with-volatility3](references/performing-memory-forensics-with-volatility3.md) · [extracting-credentials-from-memory-dump](references/extracting-credentials-from-memory-dump.md) · [analyzing-linux-kernel-rootkits](references/analyzing-linux-kernel-rootkits.md) |
| Windows event log extraction and triage | [extracting-windows-event-logs-artifacts](references/extracting-windows-event-logs-artifacts.md) |
| Network PCAP analysis (near-duplicate pair — one topic; second file owned by network-and-wireless-security) | [performing-network-forensics-with-wireshark](references/performing-network-forensics-with-wireshark.md) · [analyzing-network-traffic-with-wireshark](../network-and-wireless-security/references/analyzing-network-traffic-with-wireshark.md) |
| Packet capture collection and file extraction from PCAP | [performing-network-packet-capture-analysis](references/performing-network-packet-capture-analysis.md) |
| Cloud and container evidence: snapshots, API logs, storage | [performing-cloud-forensics-investigation](references/performing-cloud-forensics-investigation.md) · [performing-cloud-storage-forensic-acquisition](references/performing-cloud-storage-forensic-acquisition.md) · [analyzing-docker-container-forensics](references/analyzing-docker-container-forensics.md) |
| Mobile device acquisition and analysis | [performing-mobile-device-forensics-with-cellebrite](references/performing-mobile-device-forensics-with-cellebrite.md) |
| Linux log and system artifact analysis | [performing-linux-log-forensics-investigation](references/performing-linux-log-forensics-investigation.md) · [analyzing-linux-system-artifacts](references/analyzing-linux-system-artifacts.md) |
| Browser artifacts and browsing history | [analyzing-browser-forensics-with-hindsight](references/analyzing-browser-forensics-with-hindsight.md) · [extracting-browser-history-artifacts](references/extracting-browser-history-artifacts.md) |
| Email evidence: headers, spoofing, PST/OST mailboxes | [analyzing-email-headers-for-phishing-investigation](references/analyzing-email-headers-for-phishing-investigation.md) · [analyzing-outlook-pst-for-email-forensics](references/analyzing-outlook-pst-for-email-forensics.md) |
| Recovering deleted rows from SQLite databases and WAL files | [performing-sqlite-database-forensics](references/performing-sqlite-database-forensics.md) |
| Ransomware artifacts: variant, scope, encryption footprint | [investigating-ransomware-attack-artifacts](references/investigating-ransomware-attack-artifacts.md) |
| How malware survives reboots on a seized host | [performing-malware-persistence-investigation](references/performing-malware-persistence-investigation.md) |
| Hidden data in media files | [performing-steganography-detection](references/performing-steganography-detection.md) |
| Custody, hashing, and order-of-volatility rules that bind every acquisition | [evidence-handling-and-chain-of-custody](references/evidence-handling-and-chain-of-custody.md) |
| Choose the artifact and parser for a specific question | [artifact-to-tool-map](references/artifact-to-tool-map.md) |

Executable helpers for each technique live in
`scripts/<technique-name>/` — read the reference file first to learn
what the script expects, then run it.

## Output format

For any forensic request, deliver:

```markdown
# Case <ID> — Forensic Report

## Authority and scope
Authorization | Legal hold | Systems and date range | Data categories

## Acquisition
Item | Source | Method (tool, options) | Write-block verified |
SHA-256 before / image / after | Collector | Time (UTC)

## Chain of custody
Time (UTC) | Item | Action (collected, transferred, analyzed) | By whom
| Location | Hash

## Method
Parsers and commands run, with inputs and outputs.

## Timeline
Time (UTC) | Event | Source artifact | Significance
(pivot points marked; clock skew noted)

## Findings
Number | Statement | Supporting artifact(s) + path | Fact or inference
| Confidence

## Evidence index
Exhibit | Description | Hash | Storage location

## Limitations
Gaps in telemetry, unrecovered data, and what could not be proven.
```

For acquisition-only requests, the deliverable is the acquisition record
plus custody log — no findings.
