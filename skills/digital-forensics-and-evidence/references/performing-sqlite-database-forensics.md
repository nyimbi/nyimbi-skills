# Performing Sqlite Database Forensics

## API Reference

## SQLite File Header (First 100 Bytes)

| Offset | Size | Description |
|--------|------|-------------|
| 0 | 16 | Magic: `SQLite format 3\000` |
| 16 | 2 | Page size (512-65536; 1 means 65536) |
| 24 | 4 | File change counter |
| 28 | 4 | Database size in pages |
| 32 | 4 | First freelist trunk page |
| 36 | 4 | Total freelist pages |
| 52 | 4 | Text encoding (1=UTF-8, 2=UTF-16le, 3=UTF-16be) |

## Page Types

| Type Byte | Description |
|-----------|-------------|
| `0x02` | Index interior (B-tree) |
| `0x05` | Table interior (B-tree) |
| `0x0A` | Index leaf (B-tree) |
| `0x0D` | Table leaf (B-tree) |

## Timestamp Decoders

| Format | Epoch | Conversion |
|--------|-------|------------|
| Unix | 1970-01-01 | `datetime.utcfromtimestamp(val)` |
| Chrome/WebKit | 1601-01-01 | `(val / 1e6) - 11644473600` seconds since Unix epoch |
| Mac Absolute | 2001-01-01 | `datetime(2001,1,1) + timedelta(seconds=val)` |
| Mozilla PRTime | 1970-01-01 | `val / 1e6` seconds since Unix epoch |

## Common Forensic Databases

| Application | File | Key Tables |
|------------|------|------------|
| Chrome | `History` | `urls`, `visits`, `downloads` |
| Firefox | `places.sqlite` | `moz_places`, `moz_historyvisits` |
| WhatsApp | `msgstore.db` | `messages`, `chat_list` |
| iMessage | `sms.db` | `message`, `handle`, `chat` |
| Android SMS | `mmssms.db` | `sms`, `threads` |

## Python Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| `sqlite3` | stdlib | Query database tables |
| `struct` | stdlib | Parse binary header and page structures |
| `os` / `pathlib` | stdlib | File size and path operations |

## References

- SQLite File Format: https://www.sqlite.org/fileformat2.html
- SQLite WAL Format: https://www.sqlite.org/wal.html
- Belkasoft SQLite Analysis: https://belkasoft.com/sqlite-analysis
- Sanderson Forensics SQLite: https://sqliteforensictoolkit.com/

---

## Standards and Controls

## Standards
- NIST SP 800-86: Guide to Integrating Forensic Techniques
- SQLite File Format Specification: https://www.sqlite.org/fileformat2.html
- SWGDE Best Practices for Mobile Device Forensics

## Tools
- DB Browser for SQLite: Open-source GUI editor
- sqlcipher: Encrypted SQLite database handling
- Belkasoft Evidence Center: Commercial SQLite forensic analysis
- Exponent SQLite Explorer: Forensic SQLite viewer with timestamp auto-detection
- FORC (Forensic Operations for Recognizing SQLite Content): Automated Android extraction

## Key Database Locations
- Chrome History: %LOCALAPPDATA%\Google\Chrome\User Data\Default\History
- Firefox places.sqlite: %APPDATA%\Mozilla\Firefox\Profiles\*.default\places.sqlite
- Android SMS: /data/data/com.android.providers.telephony/databases/mmssms.db
- iOS SMS: /private/var/mobile/Library/SMS/sms.db
- WhatsApp: /data/data/com.whatsapp/databases/msgstore.db

---

## Workflows

## Workflow 1: Complete Database Analysis
```
Identify SQLite databases in evidence
    |
Create forensic copies (preserve WAL and journal files)
    |
Analyze database header (page size, encoding, freelist)
    |
Query active tables for evidence
    |
Analyze freelist pages for deleted records
    |
Parse WAL file for transaction history
    |
Examine unallocated space within pages
    |
Decode timestamps (Chrome, Unix, Mac Absolute, Mozilla)
    |
Document and export findings
```

## Workflow 2: Deleted Record Recovery
```
Open database in hex editor
    |
Identify freelist trunk/leaf pages from header
    |
Extract raw page data from freelist
    |
Parse B-tree cell format to decode records
    |
Check WAL for pre-deletion snapshots
    |
Examine unallocated space between cell pointers and content area
    |
Carve recoverable records
```

---

## Working Template

## Case Information
| Field | Value |
|-------|-------|
| Case Number | |
| Database File | |
| File Hash (SHA-256) | |
| Examiner | |

## Database Summary
| Property | Value |
|----------|-------|
| Page Size | |
| Total Pages | |
| Freelist Pages | |
| Text Encoding | |
| WAL Present | |

## Tables and Record Counts
| Table Name | Row Count | Columns |
|-----------|-----------|---------|
| | | |

## Recovered Deleted Records
| Source | Record Data | Recovery Method |
|--------|------------|----------------|
| | | |

## Findings
_(Summary of forensic analysis)_
