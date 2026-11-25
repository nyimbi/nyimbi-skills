#!/usr/bin/env python3
"""Apply one approved macOS maintenance category.

Dry-run by default. Requires --apply --yes to change anything. User files are moved
to a timestamped quarantine; regenerable caches and build artifacts are deleted.
No sudo. No blanket deletion. One category per invocation.

    python3 scripts/mac_apply.py --list
    python3 scripts/mac_apply.py --category xcode-derived
    python3 scripts/mac_apply.py --category xcode-derived --apply --yes
    python3 scripts/mac_apply.py --category project-artifacts --apply --yes
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import time
from datetime import datetime
from pathlib import Path

from mac_audit import (
    ARTIFACT_NAMES,
    HOME,
    PROJECT_ROOTS,
    dir_size,
    human_bytes,
    installers,
    is_protected,
    project_artifacts,
    run,
    whitelist,
)

QUARANTINE = HOME / ".mac-maintenance/quarantine"
LOG = HOME / ".mac-maintenance/changes.log"

CATEGORIES: dict[str, dict] = {
    "homebrew-cache": {"label": "Homebrew downloads", "kind": "command", "cmd": ["brew", "cleanup", "--prune=all", "-s"], "path": HOME / "Library/Caches/Homebrew"},
    "npm-cache": {"label": "npm cache", "kind": "command", "cmd": ["npm", "cache", "clean", "--force"], "path": HOME / ".npm"},
    "npx-cache": {"label": "npx cache", "kind": "delete-dir", "path": HOME / ".npm/_npx"},
    "yarn-cache": {"label": "Yarn cache", "kind": "command", "cmd": ["yarn", "cache", "clean"], "path": HOME / "Library/Caches/Yarn"},
    "pnpm-cache": {"label": "pnpm store", "kind": "command", "cmd": ["pnpm", "store", "prune"], "path": HOME / "Library/pnpm/store"},
    "bun-cache": {"label": "Bun cache", "kind": "command", "cmd": ["bun", "pm", "cache", "rm"], "path": HOME / ".bun/install/cache"},
    "pip-cache": {"label": "pip cache", "kind": "command", "cmd": ["python3", "-m", "pip", "cache", "purge"], "path": HOME / "Library/Caches/pip"},
    "uv-cache": {"label": "uv cache", "kind": "command", "cmd": ["uv", "cache", "clean"], "path": HOME / "Library/Caches/uv"},
    "go-build-cache": {"label": "Go build cache", "kind": "command", "cmd": ["go", "clean", "-cache"], "path": HOME / "Library/Caches/go-build"},
    "gem-cache": {"label": "RubyGems cache", "kind": "command", "cmd": ["gem", "cleanup"], "path": HOME / ".gem"},
    "conda-cache": {"label": "Conda package cache", "kind": "command", "cmd": ["conda", "clean", "--all", "-y"], "path": HOME / "opt/anaconda3/pkgs"},
    "xcode-derived": {"label": "Xcode DerivedData", "kind": "delete-dir", "path": HOME / "Library/Developer/Xcode/DerivedData", "guard": "Xcode"},
    "xcode-archives": {"label": "Xcode archives", "kind": "quarantine-dir", "path": HOME / "Library/Developer/Xcode/Archives"},
    "xcode-device-support": {"label": "Xcode device support", "kind": "delete-dir", "path": HOME / "Library/Developer/Xcode/iOS DeviceSupport", "guard": "Xcode"},
    "simulators": {"label": "Unavailable simulators", "kind": "command", "cmd": ["xcrun", "simctl", "delete", "unavailable"], "guard": "Simulator"},
    "docker": {"label": "Docker dangling images and build cache", "kind": "command", "cmd": ["docker", "system", "prune", "-f"], "guard": "Docker"},
    "logs": {"label": "Old user logs", "kind": "quarantine-old", "path": HOME / "Library/Logs", "days": 30},
    "downloads": {"label": "Old Downloads", "kind": "quarantine-old", "path": HOME / "Downloads", "days": 90},
    "installers": {"label": "Old installer files", "kind": "quarantine-installers", "path": HOME / "Downloads", "days": 30},
    "ios-backups": {"label": "iOS backups", "kind": "quarantine-dir", "path": HOME / "Library/Application Support/MobileSync/Backup"},
    "project-artifacts": {"label": "Project build artifacts", "kind": "project-artifacts"},
    "trash-empty": {"label": "Empty Trash (irreversible)", "kind": "trash"},
}

REFUSED = {
    "user-caches": "Deleting the whole ~/Library/Caches can log you out or break running apps. Clean per-app caches manually.",
    "app-support": "Application Support is app data, not cache. Review manually.",
    "preferences": "Preferences are app settings. Review manually.",
    "mail": "Mail data is user data.",
    "messages": "Messages data is user data.",
    "hf-cache": "Hugging Face weights are preserved by policy.",
    "system-caches": "System caches require sudo and are not worth the risk.",
    "swap": "macOS manages swap and VM.",
}


def log(line: str) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as fh:
        fh.write(f"{datetime.now().isoformat(timespec='seconds')}\t{line}\n")


def process_running(name: str) -> bool:
    if name == "Docker":
        _, _, code = run(["docker", "info"], timeout=8)
        return code != 0
    out, _, code = run(["pgrep", "-x", name], timeout=5)
    if code == 0 and out:
        return True
    out, _, code = run(["pgrep", "-f", f"/{name}.app/"], timeout=5)
    return code == 0 and bool(out)


def guard(category: str) -> str | None:
    cfg = CATEGORIES[category]
    name = cfg.get("guard")
    if name and process_running(name):
        return f"{name} is running; close it before cleaning {category}."
    return None


def protected(path: Path, whitelist_entries: list[str]) -> bool:
    return is_protected(path, whitelist_entries)


def quarantine_path(src: Path, category: str, qroot: Path) -> Path:
    try:
        rel = src.relative_to(HOME)
    except ValueError:
        rel = Path(src.name)
    dest = qroot / category / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        dest = dest.with_name(f"{dest.name}.{int(time.time())}")
    return dest


def move(src: Path, category: str, qroot: Path) -> tuple[int, Path]:
    size = dir_size(src) if src.is_dir() else src.stat().st_size
    dest = quarantine_path(src, category, qroot)
    shutil.move(str(src), str(dest))
    log(f"QUARANTINE\t{category}\t{src}\t{size}\t{dest}")
    return size or 0, dest


def remove_dir_contents(path: Path, category: str) -> tuple[int, int]:
    if not path.exists():
        return 0, 0
    freed = 0
    count = 0
    for child in path.iterdir():
        if child.is_symlink() or not child.is_dir():
            continue
        size = dir_size(child, timeout=30) or 0
        shutil.rmtree(child)
        freed += size
        count += 1
        log(f"DELETE\t{category}\t{child}\t{size}")
    return freed, count


def quarantine_old(path: Path, category: str, days: int, qroot: Path) -> tuple[int, int]:
    if not path.exists():
        return 0, 0
    cutoff = time.time() - days * 86400
    freed = 0
    count = 0
    for child in path.iterdir():
        if child.is_symlink() or not child.is_file():
            continue
        try:
            if child.stat().st_mtime > cutoff:
                continue
        except OSError:
            continue
        size, _ = move(child, category, qroot)
        freed += size
        count += 1
    return freed, count


def quarantine_installers(path: Path, category: str, days: int, qroot: Path) -> tuple[int, int]:
    cutoff = time.time() - days * 86400
    freed = 0
    count = 0
    for child in path.iterdir():
        if child.is_symlink() or not child.is_file():
            continue
        if child.suffix.lower() not in {".dmg", ".pkg", ".mpkg", ".zip"}:
            continue
        try:
            stat = child.stat()
            if stat.st_mtime > cutoff or stat.st_size < 100 * 1024 ** 2:
                continue
        except OSError:
            continue
        size, _ = move(child, category, qroot)
        freed += size
        count += 1
    return freed, count


def disk_free() -> int:
    out, _, _ = run(["df", "-k", "/System/Volumes/Data"], timeout=10)
    for line in out.splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 4:
            try:
                return int(parts[3]) * 1024
            except ValueError:
                continue
    return 0


def run_command(category: str) -> tuple[int, int]:
    cmd = CATEGORIES[category]["cmd"]
    if not shutil.which(cmd[0]):
        log(f"SKIP\t{category}\tmissing\t{cmd[0]}")
        print(f"  skip: {cmd[0]} not found")
        return 0, 1
    path = CATEGORIES[category].get("path")
    before = dir_size(path) if path else disk_free()
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=600, check=False)
    log(f"COMMAND\t{category}\t{' '.join(cmd)}\trc={p.returncode}\t{p.stderr.strip()[:300]}")
    if p.returncode != 0:
        print(f"  command failed ({p.returncode}): {p.stderr.strip()[:200]}")
        return 0, 1
    after = dir_size(path) if path else disk_free()
    return max(0, (before or 0) - (after or 0)), 1


def apply_project_artifacts(roots: list[Path], whitelist_entries: list[str]) -> tuple[int, int]:
    artifacts = project_artifacts(limit=200)
    freed = 0
    count = 0
    for row in artifacts:
        path = Path(row["path"])
        if protected(path, whitelist_entries):
            print(f"  skip protected: {row['display_path']}")
            continue
        if path.name not in ARTIFACT_NAMES:
            continue
        if not any(root == path or root in path.parents for root in roots):
            continue
        if not path.is_dir() or path.is_symlink():
            continue
        size = dir_size(path) or row["bytes"]
        shutil.rmtree(path)
        freed += size
        count += 1
        log(f"DELETE\tproject-artifacts\t{path}\t{size}")
        print(f"  removed {row['display_path']} ({human_bytes(size)})")
    return freed, count


def main() -> None:
    ap = argparse.ArgumentParser(description="Apply one approved macOS maintenance category")
    ap.add_argument("--list", action="store_true", help="List categories and exit")
    ap.add_argument("--category", help="Category to apply")
    ap.add_argument("--apply", action="store_true", help="Actually change something")
    ap.add_argument("--yes", action="store_true", help="Confirm the category")
    ap.add_argument("--root", action="append", type=Path, help="Project root for project-artifacts (repeatable)")
    ap.add_argument("--days", type=int, help="Age threshold for logs/downloads/installers")
    ap.add_argument("--quarantine", type=Path, help="Quarantine root")
    args = ap.parse_args()

    if args.list:
        for cid, cfg in sorted(CATEGORIES.items()):
            print(f"{cid:22} {cfg['label']}")
        print("\nRefused categories:")
        for cid, reason in REFUSED.items():
            print(f"{cid:22} {reason}")
        return

    if not args.category:
        raise SystemExit("Use --category <id> or --list.")
    category = args.category
    if category in REFUSED:
        raise SystemExit(f"Refused: {REFUSED[category]}")
    if category not in CATEGORIES:
        raise SystemExit(f"Unknown category: {category}. Use --list.")

    cfg = CATEGORIES[category]
    if not args.apply:
        print(f"Dry run: {category} — {cfg['label']}")
        if category == "project-artifacts":
            rows = project_artifacts(limit=50)
            print(f"Would remove {len(rows)} artifact directories, {human_bytes(sum(r['bytes'] for r in rows))}.")
        elif category == "installers":
            rows = installers()
            print(f"Would quarantine {len(rows)} installer files, {human_bytes(sum(r['bytes'] for r in rows))}.")
        elif cfg["kind"] in {"delete-dir", "quarantine-dir"}:
            path = cfg["path"]
            print(f"Path: {path}")
            print(f"Size: {human_bytes(dir_size(path))}")
        elif cfg["kind"] in {"quarantine-old", "quarantine-installers"}:
            print(f"Path: {cfg['path']} · older than {args.days or cfg['days']} days")
        elif cfg["kind"] == "trash":
            print("WARNING: emptying Trash is irreversible and may include external volumes.")
        else:
            print(f"Command: {' '.join(cfg['cmd'])}")
        print("No changes made. Add --apply --yes to execute.")
        return

    if not args.yes:
        raise SystemExit("Refusing to change anything without --yes.")

    blocked = guard(category)
    if blocked:
        raise SystemExit(blocked)

    whitelist_entries = whitelist()
    qroot = args.quarantine or (QUARANTINE / datetime.now().strftime("%Y%m%d-%H%M%S"))
    qroot.mkdir(parents=True, exist_ok=True)
    freed = 0
    count = 0

    print(f"Applying {category} — {cfg['label']}")
    if cfg["kind"] == "command":
        freed, count = run_command(category)
    elif cfg["kind"] == "delete-dir":
        path = cfg["path"]
        if protected(path, whitelist_entries):
            raise SystemExit(f"Protected by whitelist: {path}")
        freed, count = remove_dir_contents(path, category)
    elif cfg["kind"] == "quarantine-dir":
        path = cfg["path"]
        if protected(path, whitelist_entries):
            raise SystemExit(f"Protected by whitelist: {path}")
        if path.exists():
            for child in list(path.iterdir()):
                if child.is_symlink():
                    continue
                size, _ = move(child, category, qroot)
                freed += size
                count += 1
    elif cfg["kind"] == "quarantine-old":
        freed, count = quarantine_old(cfg["path"], category, args.days or cfg["days"], qroot)
    elif cfg["kind"] == "quarantine-installers":
        freed, count = quarantine_installers(cfg["path"], category, args.days or cfg["days"], qroot)
    elif cfg["kind"] == "project-artifacts":
        roots = [p.expanduser().resolve() for p in (args.root or PROJECT_ROOTS)]
        roots = [p for p in roots if p.exists()]
        if not roots:
            raise SystemExit("No project roots found. Pass --root.")
        freed, count = apply_project_artifacts(roots, whitelist_entries)
    elif cfg["kind"] == "trash":
        print("WARNING: emptying Trash is irreversible and may include external volumes.")
        p = subprocess.run(
            ["osascript", "-e", 'tell application "Finder" to empty trash'],
            capture_output=True, text=True, timeout=120, check=False,
        )
        log(f"TRASH\tempty\trc={p.returncode}\t{p.stderr.strip()[:200]}")
        if p.returncode != 0:
            raise SystemExit(f"Finder refused: {p.stderr.strip()[:200]}")
        count = 1
    else:
        raise SystemExit(f"Unsupported kind: {cfg['kind']}")

    print(f"Category: {category}")
    print(f"Items: {count}")
    print(f"Measured: {human_bytes(freed)}")
    if cfg["kind"].startswith("quarantine"):
        print(f"Quarantine: {qroot}")
        print("Space is freed only after the quarantine is emptied deliberately.")
    print(f"Log: {LOG}")


if __name__ == "__main__":
    main()
