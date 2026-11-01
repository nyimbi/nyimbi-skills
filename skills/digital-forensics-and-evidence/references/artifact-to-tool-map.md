# Artifact-to-Tool Map

Purpose: translate an investigative question into the artifacts that
answer it and the parser that extracts them, so no question is attacked
with the wrong artifact.

## Question → artifact → parser

| Investigative question | Artifacts to pull | Parser / tool | Technique file |
|---|---|---|---|
| What programs ran, and when? | Prefetch, Amcache, ShimCache, BAM/DAM, SRUM | PECmd, AmcacheParser, AppCompatCacheParser, KAPE modules | [analyzing-prefetch-files-for-execution-history](analyzing-prefetch-files-for-execution-history.md) · [analyzing-windows-amcache-artifacts](analyzing-windows-amcache-artifacts.md) |
| How does it survive reboots? | Run keys, services, scheduled tasks, WMI subscriptions, startup folders, SSH keys/cron (Linux) | RegRipper, Autoruns, RECmd | [analyzing-windows-registry-for-artifacts](analyzing-windows-registry-for-artifacts.md) · [performing-malware-persistence-investigation](performing-malware-persistence-investigation.md) |
| What files did the user open or browse to? | LNK, Jump Lists, Shellbags, RecentDocs, UserAssist | LECmd, JLECmd, SBECmd, RegRipper | [analyzing-lnk-file-and-jump-list-artifacts](analyzing-lnk-file-and-jump-list-artifacts.md) · [analyzing-windows-shellbag-artifacts](analyzing-windows-shellbag-artifacts.md) |
| What was deleted? | $MFT, $UsnJrnl, $LogFile, Recycle Bin, slack, unallocated | MFTECmd, analyzeMFT, LogFileParser, RBCmd, Foremost/PhotoRec | [analyzing-mft-for-deleted-file-recovery](analyzing-mft-for-deleted-file-recovery.md) · [performing-file-carving-with-foremost](performing-file-carving-with-foremost.md) |
| Did a removable device connect, and who used it? | USBSTOR, MountedDevices, MountPoints2, SetupAPI, event 6416 | RegRipper/RECmd + Python parsers | [analyzing-usb-device-connection-history](analyzing-usb-device-connection-history.md) |
| What accounts logged on, and from where? | Security EVTX (4624/4625/4648), auth.log, journal | Hayabusa, Chainsaw, EvtxECmd, journalctl exports | [extracting-windows-event-logs-artifacts](extracting-windows-event-logs-artifacts.md) · [performing-linux-log-forensics-investigation](performing-linux-log-forensics-investigation.md) |
| What web activity happened? | Chromium/Firefox history, cookies, cache, downloads | Hindsight, browser native exports | [analyzing-browser-forensics-with-hindsight](analyzing-browser-forensics-with-hindsight.md) · [extracting-browser-history-artifacts](extracting-browser-history-artifacts.md) |
| Which email, and was it spoofed? | EML headers, PST/OST, message trace | Python email lib, libpff, SPF/DKIM/DMARC checks | [analyzing-email-headers-for-phishing-investigation](analyzing-email-headers-for-phishing-investigation.md) · [analyzing-outlook-pst-for-email-forensics](analyzing-outlook-pst-for-email-forensics.md) |
| What was in RAM at capture time? | Memory dump | Volatility 3 (+ symbols) | [performing-memory-forensics-with-volatility3](performing-memory-forensics-with-volatility3.md) |
| What crossed the network? | PCAP/PCAPNG | Wireshark/tshark, NetworkMiner | [performing-network-packet-capture-analysis](performing-network-packet-capture-analysis.md) |
| What happened inside an app's database? | SQLite DB + WAL + freelists | sqlite3, forensic SQLite tools | [performing-sqlite-database-forensics](performing-sqlite-database-forensics.md) |
| What did the cloud account do? | CloudTrail/Activity/Audit logs, snapshots, S3 access logs | Athena, vendor CLI, snapshot + forensic VPC | [performing-cloud-forensics-investigation](performing-cloud-forensics-investigation.md) |
| What did the phone do? | Logical / file-system / physical extraction | Cellebrite UFED, ALEAPP, iLEAPP | [performing-mobile-device-forensics-with-cellebrite](performing-mobile-device-forensics-with-cellebrite.md) |
| Put every source in one narrative | All of the above, normalized | log2timeline/psort → Timesketch or Hayabusa | [performing-timeline-reconstruction-with-plaso](performing-timeline-reconstruction-with-plaso.md) |
| Is there hidden data in a file? | Alternate data streams, stego in media | TSK tools, steganalysis utilities | [analyzing-slack-space-and-file-system-artifacts](analyzing-slack-space-and-file-system-artifacts.md) · [performing-steganography-detection](performing-steganography-detection.md) |

## Ordering rules

- **Triage before deep analysis:** targeted collection (KAPE/VELO) and
  a first-pass timeline usually answer scope questions before full
  manual parsing of every hive.
- **Cross-validate:** a conclusion needs two artifact classes where
  possible — prefetch execution corroborated by Amcache or EVTX,
  deletion shown in both MFT flags and `$LogFile`.
- **Timestamps:** prefer artifacts with absolute timestamps and note
  the timezone; `MACB` ordering alone is not a timeline.
- **Missing artifacts are findings:** absence of prefetch (disabled
  logging, live response only, or cleared) changes what can be proven
  and must be stated.
