#!/usr/bin/env python3
"""Audit and, only on explicit request, apply a macOS power profile.

    python3 scripts/mac_power.py --audit
    python3 scripts/mac_power.py --recommend
    python3 scripts/mac_power.py --profile laptop --apply --yes
    python3 scripts/mac_power.py --caffeinate 240

`--audit` and `--recommend` never change anything. `--apply` uses sudo and writes a
timestamped backup of `pmset -g custom` first.
"""
from __future__ import annotations

import argparse
import subprocess
from datetime import datetime

from mac_audit import HOME, run

POWER_DIR = HOME / ".mac-maintenance/power"

PROFILES = {
    "desktop": {
        "label": "Plugged-in desktop",
        "args": ["-a", "displaysleep", "10", "disksleep", "10", "sleep", "30", "womp", "1", "powernap", "1"],
        "note": "Display sleeps after 10 min, system after 30, wake-on-network on.",
    },
    "laptop": {
        "label": "Battery-conscious laptop",
        "args": ["-b", "displaysleep", "5", "disksleep", "10", "sleep", "10", "powernap", "0"],
        "note": "Battery only: display 5 min, system 10, Power Nap off.",
    },
}


def audit() -> str:
    settings, _, _ = run(["pmset", "-g"])
    custom, _, _ = run(["pmset", "-g", "custom"])
    assertions, _, _ = run(["pmset", "-g", "assertions"])
    batt, _, _ = run(["pmset", "-g", "batt"])
    therm, _, _ = run(["pmset", "-g", "therm"])
    profiler, _, _ = run(["system_profiler", "SPPowerDataType"], timeout=20)
    return "\n".join([
        "# Power audit",
        "",
        "## Current settings",
        "```text",
        settings or "unavailable",
        "```",
        "",
        "## Custom settings",
        "```text",
        custom or "unavailable",
        "```",
        "",
        "## Battery",
        "```text",
        batt or "no battery (desktop?)",
        "```",
        "",
        "## Thermal",
        "```text",
        therm or "no thermal warning",
        "```",
        "",
        "## Battery health",
        "```text",
        "\n".join(line for line in profiler.splitlines() if any(
            key in line for key in ("Cycle Count", "Condition", "Maximum Capacity", "Fully Charged")
        )) or "unavailable",
        "```",
        "",
        "## Sleep assertions",
        "```text",
        "\n".join(assertions.splitlines()[:80]) or "none",
        "```",
    ])


def recommend() -> str:
    settings, _, _ = run(["pmset", "-g"])
    lines = [
        "# Power recommendations",
        "",
        "Current settings:",
        "```text",
        settings,
        "```",
        "",
        "Do not change settings just because a profile exists. Pick one only if the current "
        "behaviour is causing a problem.",
        "",
    ]
    for key, profile in PROFILES.items():
        lines += [
            f"## {profile['label']} (`{key}`)",
            "",
            f"{profile['note']}",
            "",
            "```bash",
            "sudo pmset " + " ".join(profile["args"]),
            "```",
            "",
        ]
    lines += [
        "## Temporary keep-awake",
        "",
        "For a bounded render or download, do not set `sleep 0` permanently:",
        "",
        "```bash",
        "caffeinate -dimsu -t 14400   # 4 hours, then releases",
        "```",
        "",
        "## Reject",
        "",
        "- `sudo purge` — macOS manages inactive memory; purging causes churn and swap.",
        "- `sudo pmset ... sleep 0` as a permanent setting — it hides thermal and battery problems.",
        "- `killall` on power or network daemons to \"refresh\" them.",
        "",
    ]
    return "\n".join(lines)


def apply_profile(name: str, yes: bool) -> None:
    profile = PROFILES[name]
    POWER_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = POWER_DIR / f"pmset-{stamp}.txt"
    original, _, _ = run(["pmset", "-g", "custom"])
    backup.write_text(original + "\n")
    cmd = ["sudo", "pmset", *profile["args"]]
    print(f"Backup: {backup}")
    print("Command:", " ".join(cmd))
    if not yes:
        print("Dry run. Add --yes to execute.")
        return
    p = subprocess.run(cmd, check=False)
    if p.returncode != 0:
        raise SystemExit(f"pmset failed with {p.returncode}")
    print("Applied. Re-run --audit to verify.")


def caffeinate(minutes: int) -> None:
    seconds = max(1, minutes) * 60
    p = subprocess.Popen(["caffeinate", "-dimsu", "-t", str(seconds)])
    print(f"caffeinate started: pid {p.pid}, {minutes} minutes. It releases automatically.")


def main() -> None:
    ap = argparse.ArgumentParser(description="Audit or apply macOS power settings")
    ap.add_argument("--audit", action="store_true", help="Print current power state")
    ap.add_argument("--recommend", action="store_true", help="Print profiles and commands")
    ap.add_argument("--profile", choices=sorted(PROFILES), help="Profile to apply")
    ap.add_argument("--apply", action="store_true", help="Apply the profile")
    ap.add_argument("--yes", action="store_true", help="Confirm the change")
    ap.add_argument("--caffeinate", type=int, metavar="MINUTES", help="Keep awake for N minutes")
    args = ap.parse_args()

    if args.caffeinate:
        caffeinate(args.caffeinate)
    elif args.profile:
        if not args.apply:
            profile = PROFILES[args.profile]
            print(f"Profile: {profile['label']}")
            print("Command: sudo pmset", " ".join(profile["args"]))
            print(profile["note"])
            print("Dry run. Add --apply --yes to execute.")
        else:
            if not args.yes:
                raise SystemExit("Refusing to change power settings without --yes.")
            apply_profile(args.profile, args.yes)
    elif args.recommend:
        print(recommend())
    else:
        print(audit())


if __name__ == "__main__":
    main()
