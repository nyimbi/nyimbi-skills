#!/usr/bin/env python3
"""Install, inspect or remove a weekly read-only audit via launchd.

    python3 scripts/mac_schedule.py --status
    python3 scripts/mac_schedule.py --install --yes
    python3 scripts/mac_schedule.py --remove --yes
"""
from __future__ import annotations

import argparse
import os
import plistlib
import subprocess
import sys
from pathlib import Path

from mac_audit import DEFAULT_OUT, HOME

LABEL = "com.nyimbi.mac-maintenance.audit"
PLIST = HOME / "Library/LaunchAgents" / f"{LABEL}.plist"
LOG_DIR = HOME / ".mac-maintenance/logs"


def status() -> str:
    uid = os.getuid()
    p = subprocess.run(
        ["launchctl", "print", f"gui/{uid}/{LABEL}"],
        capture_output=True, text=True, check=False,
    )
    if p.returncode == 0:
        return "installed\n" + "\n".join(p.stdout.splitlines()[:25])
    return "not installed"


def install(yes: bool) -> None:
    if not yes:
        print(f"Would write {PLIST} and load {LABEL}.")
        print("Dry run. Add --yes to install.")
        return
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    PLIST.parent.mkdir(parents=True, exist_ok=True)
    audit = Path(__file__).resolve().parent / "mac_audit.py"
    payload = {
        "Label": LABEL,
        "ProgramArguments": [sys.executable, str(audit), "--quiet"],
        "StartCalendarInterval": {"Weekday": 0, "Hour": 9, "Minute": 0},
        "RunAtLoad": False,
        "StandardOutPath": str(LOG_DIR / "audit.log"),
        "StandardErrorPath": str(LOG_DIR / "audit.err.log"),
        "ProcessType": "Background",
        "LowPriorityIO": True,
    }
    PLIST.write_bytes(plistlib.dumps(payload))
    uid = os.getuid()
    subprocess.run(["launchctl", "bootout", f"gui/{uid}", str(PLIST)], capture_output=True, check=False)
    p = subprocess.run(["launchctl", "bootstrap", f"gui/{uid}", str(PLIST)], capture_output=True, text=True, check=False)
    if p.returncode != 0:
        raise SystemExit(f"launchctl bootstrap failed: {p.stderr.strip()}")
    print(f"Installed {PLIST}")
    print(f"Audit output: {DEFAULT_OUT}/<date>/report.md")
    print("Read-only: the scheduled job never calls mac_apply.py.")


def remove(yes: bool) -> None:
    if not yes:
        print(f"Would unload and remove {PLIST}.")
        print("Dry run. Add --yes to remove.")
        return
    uid = os.getuid()
    subprocess.run(["launchctl", "bootout", f"gui/{uid}", str(PLIST)], capture_output=True, check=False)
    if PLIST.exists():
        PLIST.unlink()
    print(f"Removed {PLIST}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Weekly read-only audit schedule")
    ap.add_argument("--install", action="store_true")
    ap.add_argument("--remove", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--yes", action="store_true")
    args = ap.parse_args()
    if args.install:
        install(args.yes)
    elif args.remove:
        remove(args.yes)
    else:
        print(status())


if __name__ == "__main__":
    main()
