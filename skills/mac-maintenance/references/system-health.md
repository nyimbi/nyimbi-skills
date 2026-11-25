# Memory, CPU, Startup, Updates, Security, Network

## Memory

macOS uses available RAM for cache; “free” memory is not the goal. Read:

- **Memory pressure** (`memory_pressure -Q`): the percentage of system-wide free memory
  and whether the system is under pressure.
- **Swap** (`sysctl -n vm.swapusage`): used vs total. Small swap use is normal; sustained
  growth with high pressure is the signal.
- **Compressed memory** (`vm_stat`): pages compressed. High compression plus swap plus
  slow app switching means the workload exceeds RAM.

Do not run `sudo purge` to “free” memory. It evicts useful cache and causes re-reads and
swap. If pressure is sustained, find the process or reduce concurrency.

## CPU and load

- Load average across `hw.ncpu`: sustained load above the core count means a queue.
- `ps -Ao pid,pcpu,pmem,etime,comm -r | head -15` shows the top CPU consumers.
- Check elapsed time and parent. A long-running compiler, render, or model download is
  not a leak.
- Thermal pressure plus high CPU means cooling or workload, not a cache problem.

## Startup and background

Audit:

- `~/Library/LaunchAgents` — per-user agents.
- `/Library/LaunchAgents` and `/Library/LaunchDaemons` — system-wide; read-only.
- `launchctl list` — non-Apple labels.
- `brew services list` — Homebrew-managed services.

Flag, do not disable. A launch agent may belong to an installed app, a backup tool, a
VPN, or a security agent. Check the program path and the app it belongs to before
removing a plist. To stop a user agent temporarily:

```bash
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/<label>.plist
```

Re-enable with `bootstrap`. Do not unload system daemons.

## Updates

- `softwareupdate -l --no-scan` — pending macOS updates.
- `brew outdated --quiet` — outdated formulae.
- `mas outdated` — App Store apps, if `mas` is installed.
- Xcode command-line tools: `xcode-select -p` and `pkgutil --pkg-info=com.apple.pkg.CLTools_Executables`.

Updates are not cleanup. Schedule them; do not install during a deadline. A macOS major
upgrade needs a backup and a free-space check first.

## Security and backup

| Check | Command | Good state |
|---|---|---|
| FileVault | `fdesetup status` | On |
| SIP | `csrutil status` | enabled |
| Gatekeeper | `spctl --status` | assessments enabled |
| Firewall | `socketfilterfw --getglobalstate` | enabled or deliberately managed |
| Time Machine | `tmutil latestbackup` | recent successful backup |

Do not disable SIP or Gatekeeper to make a tool run. If a developer workflow needs it,
that is a separate, explicit decision with a rollback plan.

A backup older than a week is a finding. Check the destination has space and that the
last backup completed, not just that Time Machine is “on.”

## Network

- Interfaces and addresses: `ifconfig -a`.
- DNS: `scutil --dns`.
- Default route: `netstat -rn -f inet`.
- Listening ports: `lsof -nP -iTCP -sTCP:LISTEN`.

For “slow network,” measure before flushing anything: DNS resolution, packet loss,
Wi-Fi signal, VPN, and the actual throughput. DNS cache flushing is a manual remedy for
a confirmed stale record, not a routine.

Do not remove Wi-Fi profiles or change DNS automatically. A stale profile is a manual
review item; a corporate DNS profile may be required.

## Disk health

`smartctl` is not installed by default. If available:

```bash
smartctl -a disk0
```

Check reallocated sectors, pending sectors, and SMART overall status. A failing disk is
a backup-and-replace decision, not a cleanup decision.
