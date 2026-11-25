#!/usr/bin/env python3
"""Turn a read-only audit into an ordered, explicit maintenance plan.

    python3 scripts/mac_plan.py
    python3 scripts/mac_plan.py --audit ~/src/pjs/infra/local/mac-maintenance/2026-11-02/audit.json
    python3 scripts/mac_plan.py --json

Never changes anything. Every action names the category that mac_apply.py accepts.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from mac_audit import DEFAULT_OUT, GIB, human_bytes


def latest_audit() -> Path:
    candidates = sorted(DEFAULT_OUT.glob("*/audit.json"))
    if not candidates:
        raise SystemExit(f"No audit found under {DEFAULT_OUT}. Run mac_audit.py first.")
    return candidates[-1]


def category_command(cid: str) -> str:
    return {
        "homebrew-cache": "brew cleanup --prune=all -s",
        "npm-cache": "npm cache clean --force",
        "npx-cache": "remove ~/.npm/_npx",
        "yarn-cache": "yarn cache clean",
        "pnpm-cache": "pnpm store prune",
        "bun-cache": "bun pm cache rm",
        "pip-cache": "pip cache purge",
        "uv-cache": "uv cache clean",
        "go-build-cache": "go clean -cache",
        "gem-cache": "gem cleanup",
        "conda-cache": "conda clean --all",
        "xcode-derived": "remove ~/Library/Developer/Xcode/DerivedData/*",
        "xcode-archives": "quarantine ~/Library/Developer/Xcode/Archives",
        "simulators": "xcrun simctl delete unavailable",
        "docker": "docker system prune -f (no -a, no --volumes)",
        "installer-files": "quarantine Downloads installers older than 30 days",
        "logs": "quarantine ~/Library/Logs files older than 30 days",
        "downloads": "quarantine ~/Downloads files older than 90 days",
        "ios-backups": "quarantine MobileSync backups (explicit only)",
    }.get(cid, "")


def build_plan(audit: dict) -> dict:
    disk = audit["disk"]["data"] or audit["disk"]["root"] or {}
    total = disk.get("total_bytes") or 1
    free = disk.get("free_bytes") or 0
    free_pct = free / total * 100 if total else 0
    categories = audit["storage"]["categories"]
    protected = [c for c in categories if c.get("protected")]
    actions = []

    for c in categories:
        if c.get("protected") or not c.get("bytes"):
            continue
        if c["risk"] not in ("safe", "caution", "move"):
            continue
        if c["action"] in ("never", "review", "manual", "cache"):
            continue
        category = "installers" if c["id"] == "installer-files" else c["id"]
        actions.append({
            "id": c["id"],
            "label": c["label"],
            "category": category,
            "bytes": c["bytes"],
            "risk": c["risk"],
            "action": c["action"],
            "path": c["path"],
            "command": category_command(c["id"]),
            "note": c["note"],
        })

    projects = audit["storage"].get("project_artifacts", [])
    if projects:
        actions.append({
            "id": "project-artifacts",
            "label": "Project build artifacts",
            "category": "project-artifacts",
            "bytes": sum(p["bytes"] for p in projects),
            "risk": "safe",
            "action": "delete",
            "path": "registered project roots",
            "command": "remove node_modules, target, build, dist, caches in project roots",
            "note": f"{len(projects)} artifact directories; all regenerable.",
            "targets": [p["path"] for p in projects],
        })

    installers = audit["storage"].get("installers", [])
    if installers:
        actions.append({
            "id": "installers",
            "label": "Old installer files",
            "category": "installers",
            "bytes": sum(p["bytes"] for p in installers),
            "risk": "move",
            "action": "move",
            "path": str(Path.home() / "Downloads"),
            "command": "quarantine DMG/PKG/ZIP older than 30 days",
            "note": f"{len(installers)} installer files; quarantine, do not delete.",
            "targets": [p["path"] for p in installers],
        })

    actions.sort(key=lambda a: a["bytes"], reverse=True)
    warnings = []
    if free < 10 * GIB or (free_pct < 2 and free < 50 * GIB):
        warnings.append("critical-disk")
    elif free < 20 * GIB or (free_pct < 5 and free < 50 * GIB):
        warnings.append("warning-disk")
    mem = audit["memory"]
    if mem.get("free_percentage") is not None and mem["free_percentage"] < 20:
        warnings.append("memory-pressure")
    swap = mem.get("swap") or {}
    if swap.get("total_mb") and swap.get("used_mb", 0) / swap["total_mb"] > 0.75 and swap.get("used_mb", 0) > 4096:
        warnings.append("swap-pressure")
    bat = audit["power"]["battery"]
    condition = (bat.get("condition") or "").lower()
    if condition and condition != "normal":
        warnings.append("battery-condition")
    if "FileVault is Off" in audit["security"].get("filevault", ""):
        warnings.append("filevault-off")
    tm = (audit["security"].get("timemachine") or "").lower()
    if not tm:
        warnings.append("no-time-machine")
    elif "failed" in tm or "error" in tm:
        warnings.append("time-machine-error")
    if audit["updates"].get("brew_outdated"):
        warnings.append("brew-outdated")
    if len(audit["startup"].get("non_apple_launchctl", [])) > 25:
        warnings.append("startup-items")

    return {
        "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
        "audit": audit.get("out_dir"),
        "disk": {"free_bytes": free, "total_bytes": total, "free_pct": round(free_pct, 1)},
        "actions": actions,
        "warnings": warnings,
        "protected": [{"label": c["label"], "path": c["display_path"], "bytes": c["bytes"]} for c in protected],
        "safe_total": sum(a["bytes"] for a in actions if a["risk"] == "safe"),
        "caution_total": sum(a["bytes"] for a in actions if a["risk"] == "caution"),
        "move_total": sum(a["bytes"] for a in actions if a["risk"] == "move"),
    }


def render(plan: dict) -> str:
    disk = plan["disk"]
    lines = [
        f"# Maintenance plan — {plan['timestamp'][:10]}",
        "",
        f"Free: **{human_bytes(disk['free_bytes'])} of {human_bytes(disk['total_bytes'])} "
        f"({disk['free_pct']}%)**",
        "",
        "## Actions",
        "",
        "Run one category at a time; nothing here is automatic. `mac_apply.py --category <id> --apply --yes` "
        "executes only that category. User files are moved to quarantine, not deleted.",
        "",
        "| Category | Size | Risk | Command |",
        "|---|---:|---|---|",
    ]
    for action in plan["actions"]:
        lines.append(
            f"| `{action['category']}` — {action['label']} | {human_bytes(action['bytes'])} | "
            f"{action['risk']} | {action['command'] or action['note']} |"
        )
    lines += [
        "",
        f"Safe reclaimable: **{human_bytes(plan['safe_total'])}** · "
        f"Caution: **{human_bytes(plan['caution_total'])}** · "
        f"Quarantine-only: **{human_bytes(plan['move_total'])}**",
        "",
    ]
    if plan["protected"]:
        lines += ["## Protected by whitelist", ""]
        for item in plan["protected"]:
            lines.append(f"- {item['label']} — {human_bytes(item['bytes'])} — `{item['path']}`")
        lines.append("")
    if plan["warnings"]:
        lines += ["## Warnings", ""]
        for warning in plan["warnings"]:
            lines.append(f"- `{warning}`")
        lines.append("")
    lines += [
        "## Apply order",
        "",
        "1. Package-manager caches and project artifacts (safe, regenerable).",
        "2. Xcode DerivedData and unavailable simulators (skip while Xcode or Simulator is running).",
        "3. Old logs and Downloads/installers to quarantine.",
        "4. Review app support, iOS backups, and archives manually.",
        "5. Re-run the audit and compare free space.",
        "",
        "Never run `sudo purge`, `killall mDNSResponder`, `docker system prune -a --volumes`, "
        "or bulk-delete `~/Library/Application Support`.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description="Build a macOS maintenance plan from an audit")
    ap.add_argument("--audit", type=Path, help="Path to audit.json")
    ap.add_argument("--out", type=Path, help="Output directory (default: audit directory)")
    ap.add_argument("--json", action="store_true", help="Print JSON instead of markdown")
    args = ap.parse_args()
    audit_path = args.audit or latest_audit()
    audit = json.loads(audit_path.read_text())
    out_dir = args.out or Path(audit.get("out_dir") or audit_path.parent)
    out_dir.mkdir(parents=True, exist_ok=True)
    plan = build_plan(audit)
    (out_dir / "plan.json").write_text(json.dumps(plan, indent=2) + "\n")
    text = render(plan)
    (out_dir / "plan.md").write_text(text)
    if args.json:
        print(json.dumps(plan, indent=2))
    else:
        print(f"Plan: {out_dir / 'plan.md'}")
        print(f"Safe reclaimable: {human_bytes(plan['safe_total'])}")
        print(f"Caution: {human_bytes(plan['caution_total'])}")
        print(f"Quarantine-only: {human_bytes(plan['move_total'])}")


if __name__ == "__main__":
    main()
