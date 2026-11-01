# Performing Linux Log Forensics Investigation

## API Reference

## Libraries Used
- **re**: Pattern matching for log entries (IPs, users, timestamps, suspicious commands)
- **gzip**: Read compressed log files (.gz)
- **pathlib**: File system operations
- **collections.Counter**: Aggregate brute force IPs, command tags

## CLI Interface
```
python agent.py auth --file /var/log/auth.log
python agent.py syslog --file /var/log/syslog
python agent.py history --file /home/user/.bash_history
python agent.py timeline --files /var/log/auth.log /var/log/syslog /var/log/kern.log
```

## Core Functions

### `analyze_auth_log(log_file)` — Authentication log analysis
Detects: failed logins, successful logins, sudo commands, SSH events.
Identifies brute force suspects (>=5 failed attempts from same IP).

### `analyze_syslog(log_file)` — System log anomaly detection
Flags: errors/critical messages, kernel anomalies (segfault, OOM, panic), cron jobs.

### `analyze_command_history(history_file)` — Suspicious command detection
12 patterns: remote code execution (curl|sh), reverse shells, base64 decode,
crontab modification, firewall flush, history clearing, destructive commands.

### `timeline_analysis(log_files)` — Multi-source timeline reconstruction
Merges events from multiple log files sorted by timestamp.
Supports syslog format (Mon DD HH:MM:SS) and ISO 8601.

## Suspicious Command Tags
| Tag | Pattern |
|-----|---------|
| REMOTE_CODE_EXECUTION | curl/wget piped to sh/bash |
| BASH_REVERSE_SHELL | /dev/tcp/ usage |
| NETCAT_LISTENER | nc -e/-l/-p |
| HISTORY_CLEAR | history -c |
| DESTRUCTIVE_COMMAND | rm -rf / |

## Dependencies
No external packages — Python standard library only.

---

## Standards and Controls

## Standards
- NIST SP 800-92: Guide to Computer Security Log Management
- NIST SP 800-86: Guide to Integrating Forensic Techniques
- RFC 5424: The Syslog Protocol
## Key Log Locations
- /var/log/auth.log (Debian) or /var/log/secure (RHEL): Authentication events
- /var/log/syslog (Debian) or /var/log/messages (RHEL): System messages
- /var/log/kern.log: Kernel messages
- /var/log/audit/audit.log: Linux Audit Framework
- /var/log/wtmp, /var/log/btmp, /var/log/lastlog: Login records (binary)
## Tools
- journalctl: Systemd journal query tool
- ausearch/aureport: Audit log analysis
- logwatch, lnav: Log analysis utilities

---

## Workflows

## Workflow 1: Authentication Investigation
```
Collect /var/log/auth.log and rotated copies
    |
Parse for successful and failed SSH logins
    |
Identify brute force sources (>10 failures per IP)
    |
Trace sudo command execution by user
    |
Detect account creation/modification events
    |
Correlate with wtmp/btmp login records
```
## Workflow 2: Full System Timeline
```
Collect all logs from /var/log/
    |
Export systemd journal (journalctl --output=json)
    |
Parse audit.log for security events
    |
Merge into unified timeline
    |
Identify unauthorized access and persistence
```

---

## Working Template

## Case Info
| Field | Value |
|-------|-------|
| Case Number | |
| System | |
## Authentication Summary
| Metric | Count |
|--------|-------|
| Successful Logins | |
| Failed Logins | |
| Sudo Commands | |
| Brute Force Sources | |
## Suspicious Activity
| Timestamp | Event | Source IP | User | Details |
|-----------|-------|----------|------|---------|
| | | | | |
