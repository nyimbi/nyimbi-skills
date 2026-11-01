# Analyzing MFT For Deleted File Recovery

## API Reference

## MFT Entry Structure (1024 bytes)
| Offset | Size | Field |
|--------|------|-------|
| 0 | 4 | Signature ("FILE") |
| 18 | 2 | Sequence number |
| 20 | 2 | First attribute offset |
| 22 | 2 | Flags (0x01=in use, 0x02=directory) |

## MFT Attribute Types
| Type ID | Name | Description |
|---------|------|-------------|
| 0x10 | $STANDARD_INFORMATION | Timestamps, flags, owner |
| 0x20 | $ATTRIBUTE_LIST | List of attributes in other entries |
| 0x30 | $FILE_NAME | Filename and parent reference |
| 0x40 | $OBJECT_ID | Unique object identifier |
| 0x50 | $SECURITY_DESCRIPTOR | ACL and ownership |
| 0x60 | $VOLUME_NAME | Volume label |
| 0x80 | $DATA | File content (resident or non-resident) |
| 0x90 | $INDEX_ROOT | Directory index root |
| 0xA0 | $INDEX_ALLOCATION | Directory index entries |
| 0xB0 | $BITMAP | Bitmap for index allocation |

## $STANDARD_INFORMATION Timestamps
| Offset | Size | Field |
|--------|------|-------|
| 0 | 8 | Creation time (FILETIME) |
| 8 | 8 | Modification time |
| 16 | 8 | MFT modification time |
| 24 | 8 | Access time |

## $FILE_NAME Structure
| Offset | Size | Field |
|--------|------|-------|
| 0 | 8 | Parent directory reference |
| 64 | 1 | Filename length (chars) |
| 65 | 1 | Namespace (0=POSIX, 1=Win32, 2=DOS) |
| 66 | var | Filename (UTF-16LE) |

## FILETIME Conversion
```python
FILETIME_EPOCH = datetime(1601, 1, 1)
dt = FILETIME_EPOCH + timedelta(microseconds=filetime // 10)
```

## Tools
```bash
# Extract MFT with FTK Imager or raw copy
icat /dev/sda1 0 > $MFT
# analyzeMFT
analyzeMFT.py -f $MFT -o mft.csv
# MFTECmd (Eric Zimmerman)
MFTECmd.exe -f $MFT --csv output/
```

---

## Standards and Controls

## Standards
- NIST SP 800-86: Guide to Integrating Forensic Techniques into Incident Response
- ISO/IEC 27037: Guidelines for identification, collection, acquisition and preservation of digital evidence
- SWGDE Best Practices for Computer Forensics

## Key Technical References
- NTFS Documentation (Microsoft): File system internals and MFT structure
- MFTECmd by Eric Zimmerman: Primary parsing tool for $MFT, $J, $LogFile, $Boot
- analyzeMFT (Python): Open-source MFT parser for cross-platform analysis
- ntfstool (GitHub): Forensics tool for NTFS parsing, MFT, BitLocker, deleted files

## MITRE ATT&CK Mappings
- T1070.004 - Indicator Removal: File Deletion
- T1070.006 - Indicator Removal: Timestomping
- T1485 - Data Destruction
- T1561 - Disk Wipe

## NTFS Specifications
- MFT Record Size: 1024 bytes (default)
- MFT Entry 0: $MFT (self-reference)
- MFT Entry 1: $MFTMirr (mirror of first 4 entries)
- MFT Entry 2: $LogFile (transaction log)
- MFT Entry 5: Root directory
- MFT Entry 6: $Bitmap (cluster allocation)
- MFT Entry 8: $BadClus (bad cluster list)
- MFT Entry 11: $Extend (extended metadata)

---

## Workflows

## Workflow 1: Basic Deleted File Discovery
```
Extract $MFT from forensic image
    |
Parse with MFTECmd to CSV
    |
Filter for InUse = False (deleted records)
    |
Analyze ParentPath, FileName, FileSize
    |
Cross-reference with USN Journal for deletion timestamps
    |
Document findings with original paths and timestamps
```

## Workflow 2: MFT Slack Space Recovery
```
Extract raw $MFT binary
    |
Parse each 1024-byte record
    |
Compare used_size vs allocated_size (1024)
    |
Extract slack bytes between used and allocated
    |
Search for attribute headers (0x10, 0x30, 0x80)
    |
Reconstruct partial file metadata from slack data
```

## Workflow 3: Timeline Reconstruction
```
Parse $MFT for all timestamps ($SI and $FN)
    |
Parse $J (USN Journal) for change records
    |
Parse $LogFile for transaction records
    |
Merge into unified timeline
    |
Identify file creation, modification, deletion sequences
    |
Flag timestomping indicators ($SI Created < $FN Created)
```

---

## Working Template

## Case Information
| Field | Value |
|-------|-------|
| Case Number | |
| Examiner | |
| Date | |
| Evidence Source | |
| MFT Hash (SHA-256) | |

## Summary Statistics
| Metric | Count |
|--------|-------|
| Total MFT Records | |
| Active Records | |
| Deleted Records | |
| Timestomped Records | |

## Deleted Files of Interest
| Entry # | Filename | Original Path | Size | Created | Modified |
|---------|----------|---------------|------|---------|----------|
| | | | | | |

## Timestomping Indicators
| Entry # | Filename | $SI Created | $FN Created | Delta |
|---------|----------|------------|------------|-------|
| | | | | |

## Conclusion
_(Summary of deleted file recovery findings)_
