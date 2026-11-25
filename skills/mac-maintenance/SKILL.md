---
name: mac-maintenance
description: >-
  Audit, plan, and safely maintain a macOS machine: disk space and APFS pressure,
  cache and log cleanup, project build artifacts, Xcode and simulator cruft, package
  manager and Docker caches, memory and CPU pressure, power and sleep settings,
  battery and thermal health, startup agents, updates, FileVault/Time Machine checks,
  and network listening ports. Read-only by default: audit and plan never use sudo,
  never delete, and never change a setting. Apply runs one allowlisted category at a
  time with --yes, moves user files to a timestamped quarantine, deletes only
  regenerable artifacts, and logs every change. Use when the user says "clean my Mac",
  "disk is full", "what is using space", "why is it slow", "fans are loud", "battery
  drains", "is my backup current", "what starts at login", "audit this machine", or
  "maintain this Mac". Do not use for Linux or Windows, for hardware repair, for
  reinstalling macOS, for deleting app data or media libraries, for malware response
  (see security-incident-response-and-soc), or for deleting Hugging Face model weights.
license: MIT
---

# Mac Maintenance

A read-only audit and an explicit, reversible maintenance workflow for the Mac this
bundle runs on. The goal is not “a clean Mac”; it is a machine with enough free space,
no runaway processes, sane power behaviour, a current backup, and no hidden security
regression.

## When to use

- Free space is low, a model download failed, or Xcode will not update.
- The fan is loud, the battery drains, or the machine is slow under a known workload.
- The user asks what is using disk, memory, CPU, startup, or network ports.
- A weekly or monthly maintenance pass is due.
- A machine is handed over, reinstalled, or recovered and needs a baseline audit.

## Operating principles

1. **Read-only default.** `mac_audit.py` and `mac_plan.py` never use `sudo`, delete, or
   change settings.
2. **One category per apply.** `mac_apply.py --category <id> --apply --yes`. There is no
   “clean everything” switch.
3. **Quarantine user files.** Downloads, logs, archives, and iOS backups move to
   `~/.mac-maintenance/quarantine/<timestamp>/`; space is freed only when that is
   emptied deliberately.
4. **Delete only regenerable artifacts.** Package caches, DerivedData, unavailable
   simulators, and project build outputs. When in doubt, move.
5. **Preserve the model stores.** `~/.cache/huggingface/hub`, ComfyUI models, film
   outputs, and `~/src` are never cleaned automatically.
6. **Whitelist wins.** `~/.config/mac-maintenance/whitelist` protects paths. A missing or
   unreadable whitelist is not permission to proceed.
7. **Guard running apps.** Skip Xcode while it runs, Simulator while it runs, and Docker
   when the daemon is unreachable.
8. **Log and verify.** Every change goes to `~/.mac-maintenance/changes.log`; re-audit
   after applying and compare free space and the affected category.

## Modes

| Mode | Command | Changes anything? |
|---|---|---|
| Audit | `python3 scripts/mac_audit.py` | No |
| Plan | `python3 scripts/mac_plan.py` | No |
| Apply | `python3 scripts/mac_apply.py --category <id> --apply --yes` | Yes, one category |
| Power audit | `python3 scripts/mac_power.py --audit` | No |
| Power apply | `python3 scripts/mac_power.py --profile laptop --apply --yes` | Yes, sudo; backs up first |
| Caffeinate | `python3 scripts/mac_power.py --caffeinate 240` | Bounded keep-awake |
| Schedule | `python3 scripts/mac_schedule.py --install --yes` | Weekly read-only audit |

## Workflow

### 1. Audit

```bash
python3 scripts/mac_audit.py
```

Writes `audit.json` and `report.md` under
`~/src/pjs/infra/local/mac-maintenance/<date>/`. The report covers:

- boot and Data volume free space, capacity, local snapshots;
- storage categories with bytes, risk, and whether they are whitelisted;
- home, Library, cache, Application Support, and Preferences top entries;
- project build artifacts under registered roots;
- large files and old installers;
- memory pressure, swap, load, top CPU and memory processes;
- power settings, sleep assertions, battery condition, thermal state;
- user and system LaunchAgents, non-Apple `launchctl` entries, Homebrew services;
- macOS, Homebrew, and App Store updates;
- FileVault, SIP, Gatekeeper, firewall, Time Machine;
- interfaces, DNS, default route, listening TCP ports.

### 2. Plan

```bash
python3 scripts/mac_plan.py
```

Writes `plan.json` and `plan.md`: every action, its size, risk, category, and command.
It marks safe, caution, and quarantine-only totals. It warns on low disk, memory
pressure, battery condition, FileVault, backup, updates, and startup count.

### 3. Approve

Show the user the plan and ask which **one** category to run. Do not bundle categories.
For any `caution` or `move` category, state exactly what will happen and where the
quarantine is.

### 4. Apply

```bash
python3 scripts/mac_apply.py --category homebrew-cache --apply --yes
python3 scripts/mac_apply.py --category xcode-derived --apply --yes
python3 scripts/mac_apply.py --category project-artifacts --root ~/src/project --apply --yes
python3 scripts/mac_apply.py --category downloads --days 90 --apply --yes
```

Dry-run is the default: omit `--apply` to see the scope. `--yes` is mandatory for a
change. `trash-empty` is irreversible and should be used only on explicit request.

### 5. Verify

```bash
python3 scripts/mac_audit.py
```

Compare free bytes, the category size, and the application or project. If a cleanup
reclaims nothing, read the skip reason before trying again. If the machine behaves worse,
restore from quarantine or the `pmset` backup.

## Storage policy

| State | Threshold | Response |
|---|---|---|
| Critical | free < 10 GB or < 2% | Clear one safe category before installing or pulling models |
| Warning | free < 20 GB or < 5% | Plan a cleanup before the next large download |
| Adequate | free ≥ 20 GB | Keep 20 GB reserve; review monthly |

Safe: Homebrew downloads, npm/Yarn/pnpm/Bun/pip/uv/Go caches, RubyGems, DerivedData,
unavailable simulators, project build artifacts.
Caution: whole user caches, Playwright browsers, Conda packages, iOS backups, Xcode
archives, Trash.
Never: Hugging Face weights, Application Support, Preferences, Mail, Messages, Photos,
`~/src`, documents, swap, system caches.

A 4 TB disk with 132 GB free is 3.6% but has ample absolute headroom. Use the absolute
number for the decision and the percentage as context.

## Power policy

Audit first. The machine may already be configured correctly.

- Desktop profile: display 10 min, disk 10, system 30, wake-on-network on, Power Nap on.
- Laptop profile: on battery, display 5, disk 10, system 10, Power Nap off.
- Long render or download: `caffeinate -dimsu -t <seconds>`, not permanent `sleep 0`.
- Battery condition, cycle count, maximum capacity, and thermal pressure are reported,
  not “optimized.”
- `mac_power.py --apply` uses sudo, backs up `pmset -g custom`, and prints the reverse.

## What this skill refuses

- `sudo purge` as a memory routine.
- `killall` on `mDNSResponder`, `powerd`, or `WindowServer`.
- `docker system prune -a --volumes`.
- `sudo rm -rf` on caches or `/var/log`.
- Force-empty Trash by default.
- Deleting model weights, app data, documents, mail, messages, or photos.
- Disabling SIP, Gatekeeper, FileVault, Spotlight, or Time Machine to “speed up” a Mac.
- Killing a process because it looks stuck, without checking age, owner, and parent.

## Quality bar

- [ ] The audit ran before any change; the report path is stated.
- [ ] The plan names one category, its size, its risk, and its destination.
- [ ] `--apply --yes` was used only after the user approved that category.
- [ ] User files went to quarantine, not deletion.
- [ ] Whitelisted paths and model stores are untouched.
- [ ] Xcode, Simulator, and Docker guards were respected.
- [ ] Every change has a `changes.log` entry.
- [ ] A second audit verifies the result.
- [ ] Power changes have a timestamped `pmset` backup and a reverse command.
- [ ] No rejected command from the list above was run.

## Reference map

| Situation | Open |
|---|---|
| Hard rules, never-touch list, quarantine, whitelist, process discipline | [safety.md](references/safety.md) |
| Disk thresholds, cache categories, APFS snapshots, project artifacts | [storage.md](references/storage.md) |
| pmset keys, profiles, sleep assertions, battery, thermals, caffeinate | [power.md](references/power.md) |
| Memory pressure, CPU, startup agents, updates, security, backup, network | [system-health.md](references/system-health.md) |
| Weekly/monthly/quarterly routines and incident playbooks | [runbook.md](references/runbook.md) |
| Mole review, what was adopted and rejected, GPL boundary | [mole-review.md](references/mole-review.md) |

## Output format

After an audit:

```markdown
# Mac maintenance — YYYY-MM-DD

## Bottom line
- Free: X GB of Y GB (Z%)
- Safe reclaimable: X GB
- Attention: <disk / memory / battery / backup / updates>

## Report
`~/src/pjs/infra/local/mac-maintenance/YYYY-MM-DD/report.md`

## Recommended next action
One category, why, expected bytes, risk, command.
```

After an apply:

```markdown
# Applied — <category>

- Path/command:
- Measured reclaim: X GB
- Quarantine: <path> (if any)
- Verification: <second audit result>
- Residual issues:
```

## Scripts

| Script | Purpose |
|---|---|
| `scripts/mac_audit.py` | Read-only audit; `audit.json`, `report.md` |
| `scripts/mac_plan.py` | Read-only plan; `plan.json`, `plan.md` |
| `scripts/mac_apply.py` | One allowlisted category; dry-run default; quarantine and log |
| `scripts/mac_power.py` | Power audit, profiles, bounded caffeinate |
| `scripts/mac_schedule.py` | Weekly read-only audit via launchd |
