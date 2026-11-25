# Safety Rules

The skill's default is **read-only**. Every change is explicit, scoped, logged, and
reversible where the operating system allows.

## Hard rules

1. **Audit first.** `mac_audit.py` never uses `sudo`, never deletes, and never changes a
   setting. `mac_plan.py` is also read-only.
2. **One category per invocation.** `mac_apply.py --category <id> --apply --yes`.
   There is no `--all`.
3. **Quarantine user files, do not delete them.** Downloads, logs, archives, and iOS
   backups move to `~/.mac-maintenance/quarantine/<timestamp>/`. Space is freed only
   after the quarantine is emptied deliberately.
4. **Delete only regenerable artifacts.** Package caches, DerivedData, unavailable
   simulators, and project build artifacts. When in doubt, move.
5. **No sudo in audit.** `mac_power.py --apply` is the only sudo path; it backs up
   `pmset -g custom` first and requires `--yes`.
6. **Check the whitelist.** `~/.config/mac-maintenance/whitelist` is one absolute path
   per line. A protected path is never cleaned. A missing or unreadable whitelist is not
   permission to proceed; the default protected set still applies.
7. **Guard running apps.** Skip Xcode cleaning while Xcode is open, simulators while
   Simulator is open, and Docker pruning when the daemon is unreachable.
8. **Log every change.** `~/.mac-maintenance/changes.log` records timestamp, action,
   path, bytes, and result. A change with no log entry did not happen.
9. **Verify after.** Re-run `mac_audit.py` and compare free space and the affected
   category. A cleanup that reports success but reclaims nothing is a finding.

## Never touch automatically

- `~/.cache/huggingface/hub` and any model weights.
- `~/src`, `~/Documents`, `~/Desktop`, `~/Pictures`, `~/Movies`.
- `~/Library/Application Support`, `~/Library/Preferences` — app data, not cache.
- Mail, Messages, Photos, Calendar, Contacts, Keychains.
- `/private/var/vm`, swap, sleep image.
- System caches under `/Library/Caches` or `/System`.
- Time Machine local snapshots, unless the user explicitly asks and a recent backup
  exists.
- iOS backups, Xcode archives, and film/media outputs without explicit consent.
- Any path that resolves outside the user's home or a known cache location.

## Rejected commands

| Command | Why not |
|---|---|
| `sudo purge` | macOS manages inactive memory. Purging causes churn, swap, and slower re-access; it is not a maintenance routine. |
| `sudo killall -HUP mDNSResponder` | Flushing DNS is rarely the fix and briefly disrupts name resolution. Manual only, never scheduled. |
| `docker system prune -a --volumes` | `-a` removes images you may need; `--volumes` deletes data volumes. Use `docker system prune -f` without either. |
| `sudo rm -rf /Library/Caches/*` | System caches require sudo and can break running services. |
| `rm -rf ~/Library/Caches/*` | Logs users out of apps and forces re-downloads. Clean per app, or leave it. |
| Deleting `/var/log` | System logs are small and are the evidence when something breaks. |
| Force-empty Trash as a default | Irreversible. Only with an explicit `trash-empty` request. |
| `killall` on a process because it looks stuck | Check age, owner, parent, and what it is doing first. A process that predates the session is not yours. |
| Disabling SIP, Gatekeeper, FileVault, Spotlight, or Time Machine | Security and recovery controls are not performance knobs. |
| Third-party "cleaner" apps | They duplicate this skill with less transparency. |

## Process discipline

Before stopping anything, record:

```bash
ps -o pid,ppid,user,lstart,etime,%cpu,%mem,command -p <pid>
```

Ask: is it mine, is it older than this session, does it have children, is it holding a
file or a port? Prefer quitting the app normally; use `kill -TERM` before `kill -KILL`.
Never kill a shared service, database, or another user's process.

## Whitelist

```text
# ~/.config/mac-maintenance/whitelist
~/.cache/huggingface
~/src/pjs/infra/local/films
~/Library/Developer/Xcode/Archives/2025
```

Paths are resolved and matched by prefix. Use absolute paths or `~`. Changes take
effect on the next audit/apply run.

## Quarantine

```text
~/.mac-maintenance/
  quarantine/2026-11-02-143000/
    downloads/...
    logs/...
    installers/...
  changes.log
  power/pmset-2026-11-02-143000.txt
  logs/audit.log
```

Empty the quarantine only after reviewing it. There is no automatic purge.
