# Maintenance Runbook

## Weekly (5 minutes)

```bash
python3 scripts/mac_audit.py
python3 scripts/mac_plan.py
```

Read:

- free space and the warning state;
- safe reclaimable total;
- memory pressure and top processes;
- sleep assertions;
- Time Machine’s latest backup;
- pending updates;
- non-Apple startup items.

Do not clean on a schedule just because the number moved. Clean when free space is under
the reserve or a category is abnormal.

## Monthly (20 minutes)

1. Audit and plan.
2. Apply one safe category that is actually large:
   `mac_apply.py --category <id> --apply --yes`
3. Verify with a second audit.
4. Review `~/.mac-maintenance/changes.log`.
5. Check the quarantine and empty it deliberately if everything works.
6. Check battery condition and thermal pressure.
7. Check `brew outdated` and schedule updates.

## Quarterly

- Review startup items and Homebrew services.
- Review large Application Support entries and uninstalled-app leftovers manually.
- Check Time Machine restore, not just the last backup date.
- Check disk health if `smartctl` is available.
- Review the whitelist; add model caches, film outputs, and active project roots.
- Re-run the template and skill bundle integrity checks if they changed.

## Incident: disk nearly full

1. Stop large downloads and model pulls.
2. Audit; identify the largest safe category.
3. Apply one safe category at a time: Homebrew, package caches, DerivedData, project
   artifacts.
4. Quarantine old Downloads/installers; do not delete them in a panic.
5. Do not delete local snapshots or `/private/var/vm` as a first move.
6. Re-audit; if free space is still under 10 GB, move media to an external drive.

## Incident: fan noise and heat

1. `ps -Ao pid,pcpu,etime,comm -r | head -15`.
2. Identify the top process and its age.
3. Check `pmset -g therm`.
4. Quit the app normally; do not `kill -9` first.
5. Check vents, charger, and ambient temperature.
6. If idle load is high with no obvious process, check background agents and malware
   indicators; do not disable thermal protection.

## Incident: battery drains overnight

1. `pmset -g assertions` before sleeping.
2. `pmset -g log | tail -50` for wake reasons.
3. Check Power Nap, wake-on-network, and background agents.
4. Apply the laptop profile only if the current settings are the cause.
5. Check battery condition and cycle count.
6. A swollen battery is a stop-use safety issue.

## Incident: kernel panic or random restart

1. Note the time and what was running.
2. Check `~/Library/Logs/DiagnosticReports` and `/Library/Logs/DiagnosticReports`.
3. Run Apple Diagnostics (hold `D` at boot on Intel; hold power on Apple Silicon).
4. Boot in safe mode to isolate third-party login items.
5. Back up before any repair.
6. Do not “clean” caches as a fix for a panic.

## Incident: no network

1. Check the default route and DNS.
2. Try another network.
3. Renew DHCP, then check the VPN.
4. Flush DNS only if a stale record is confirmed; it is not a first-line fix.
5. Do not remove Wi-Fi profiles or change DNS without recording the original values.

## Incident: runaway process

1. Record `ps -o pid,ppid,user,lstart,etime,%cpu,%mem,command -p <pid>`.
2. Check whether it is yours and whether it has children.
3. Ask the app to quit.
4. `kill -TERM <pid>`; use `kill -KILL` only if it does not respond and you accept the
   data-loss risk.
5. Never kill a database, backup, or another user’s process to “free memory.”

## Escalation

- Hardware: Apple Diagnostics, Apple service.
- Filesystem: Disk Utility First Aid, then a backup.
- Data loss: stop writing, mount read-only, recover from Time Machine.
- Security incident: isolate the network, preserve logs, follow the security-incident
  runbook; do not clean evidence.
