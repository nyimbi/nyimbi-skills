# Power, Battery, and Thermals

## Read the state first

```bash
pmset -g              # active settings
pmset -g custom      # AC and battery settings
pmset -g assertions  # what is preventing sleep
pmset -g batt        # charge and power source
pmset -g therm       # thermal pressure
system_profiler SPPowerDataType
```

Never change a setting without recording the current values. `mac_power.py --apply`
writes a timestamped backup of `pmset -g custom` first.

## Settings that matter

| Key | Meaning | Sensible default |
|---|---|---|
| `displaysleep` | Minutes before display sleeps | 5–10 |
| `disksleep` | Minutes before idle disk sleeps | 10 |
| `sleep` | Minutes before system sleep | 10–30 |
| `womp` | Wake on network access | 1 on desktop, 0 on battery |
| `powernap` | Background maintenance while asleep | 1 on AC, 0 on battery |
| `standby` | Deep standby after sleep | leave default |
| `hibernatemode` | Sleep image behaviour | leave default |
| `autopoweroff` | Auto power-off after standby | leave default |

Do not set `sleep 0` permanently to “optimize performance.” It hides thermal problems,
drains battery, and collects dust. Use a bounded `caffeinate` for a render or download.

## Profiles

`mac_power.py --recommend` prints these; `--profile <name> --apply --yes` applies one.

- **desktop** — plugged-in machine: display 10 min, disk 10, system 30, wake-on-network
  on, Power Nap on.
- **laptop** — battery: display 5, disk 10, system 10, Power Nap off. AC settings are
  unchanged.

Profiles are not “better.” They are starting points for a stated problem: the machine
sleeps during a long job, or the battery drains overnight.

## Sleep assertions

`pmset -g assertions` lists processes preventing sleep. Read the owner, PID, and reason
before acting. Common legitimate holders: backups, media playback, a VM, a render, a
database. `caffeinate` itself appears there.

To find the process:

```bash
ps -o pid,ppid,user,lstart,etime,command -p <pid>
```

Do not kill a process that predates the session or belongs to another user. Ask the app
to quit, or wait for the job to finish.

## Battery

- **Cycle count** is cumulative; 1,000 cycles is a typical modern rating, not a failure
  threshold.
- **Condition: Normal** is the meaningful field. `Service Recommended` means book a
  battery service.
- **Maximum capacity** below ~80% with poor runtime is a service signal.
- A swollen battery (trackpad lifting, case bulge) is a safety issue: stop using it,
  back up, and get it serviced. Do not press it back into place.

## Thermals

`pmset -g therm` reports CPU speed limits and thermal pressure. Sustained pressure plus
fan noise usually means:

- a runaway process (`ps -Ao pid,pcpu,etime,comm -r | head`);
- blocked vents or a dusty fan;
- a charging battery in a hot room;
- an app using the GPU unnecessarily.

Fix the cause, not the fan curve. Third-party fan controllers can mask a failing thermal
system.

## Temporary keep-awake

```bash
caffeinate -dimsu -t 14400   # 4 hours; releases automatically
```

Use it for a bounded job. Record why it is running and when it ends. Do not leave an
unbounded `caffeinate` behind.

## Rejected

- `sudo purge` as routine maintenance.
- `sudo pmset ... sleep 0` permanently.
- `killall` on `mDNSResponder`, `powerd`, or `WindowServer` to “refresh” power.
- Disabling sleep to “speed up” a laptop on battery.
- Fan-control apps that override thermal protection.
