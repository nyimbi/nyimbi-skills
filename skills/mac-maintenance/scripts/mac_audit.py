#!/usr/bin/env python3
"""Read-only macOS maintenance audit.

Collects disk, cache, memory, power, startup, update, security and network facts.
Writes audit.json and report.md. Never uses sudo, never deletes, never changes settings.

    python3 scripts/mac_audit.py
    python3 scripts/mac_audit.py --out ~/mac-maintenance/2026-11-02
    python3 scripts/mac_audit.py --quiet
"""
from __future__ import annotations

import argparse
import json
import platform
import re
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()
DEFAULT_OUT = HOME / "src/pjs/infra/local/mac-maintenance"
GIB = 1024 ** 3


def run(cmd: list[str], timeout: int = 15) -> tuple[str, str, int]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)
        return p.stdout.strip(), p.stderr.strip(), p.returncode
    except FileNotFoundError:
        return "", "not found", 127
    except subprocess.TimeoutExpired:
        return "", "timeout", 124
    except OSError as exc:
        return "", str(exc), 1


def human_bytes(value: int | float | None) -> str:
    if value is None:
        return "—"
    value = float(value)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if value < 1024 or unit == "TB":
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024
    return f"{value:.1f} TB"


def display_path(path: Path | str) -> str:
    text = str(path)
    home = str(HOME)
    return "~" + text[len(home):] if text.startswith(home) else text


def dir_size(path: Path, timeout: int = 20) -> int | None:
    if not path.exists():
        return None
    out, _, code = run(["du", "-sk", str(path)], timeout=timeout)
    if code not in (0, 124):
        return None
    if not out:
        return None
    try:
        return int(out.split()[0]) * 1024
    except (ValueError, IndexError):
        return None


def child_sizes(path: Path, timeout: int = 30) -> list[dict]:
    if not path.exists():
        return []
    out, _, code = run(["du", "-x", "-d", "1", "-k", str(path)], timeout=timeout)
    if code not in (0, 124):
        return []
    rows = []
    base = str(path).rstrip("/")
    for line in out.splitlines():
        parts = line.split("\t", 1)
        if len(parts) != 2:
            parts = line.split(None, 1)
        if len(parts) != 2:
            continue
        try:
            size = int(parts[0]) * 1024
        except ValueError:
            continue
        name = parts[1].strip()
        if name.rstrip("/") == base:
            continue
        rows.append({"path": name, "bytes": size})
    rows.sort(key=lambda row: row["bytes"], reverse=True)
    return rows


def parse_df() -> dict:
    out, _, _ = run(["df", "-k", "/"])
    result: dict[str, dict | None] = {"root": None, "data": None}
    for line in out.splitlines()[1:]:
        parts = line.split()
        if len(parts) < 6:
            continue
        try:
            total = int(parts[1]) * 1024
            used = int(parts[2]) * 1024
            free = int(parts[3]) * 1024
        except ValueError:
            continue
        result["root"] = {
            "filesystem": parts[0],
            "total_bytes": total,
            "used_bytes": used,
            "free_bytes": free,
            "capacity": parts[4],
            "mount": parts[-1],
        }
        break
    out, _, _ = run(["df", "-k", "/System/Volumes/Data"])
    for line in out.splitlines()[1:]:
        parts = line.split()
        if len(parts) < 6:
            continue
        try:
            total = int(parts[1]) * 1024
            used = int(parts[2]) * 1024
            free = int(parts[3]) * 1024
        except ValueError:
            continue
        result["data"] = {
            "filesystem": parts[0],
            "total_bytes": total,
            "used_bytes": used,
            "free_bytes": free,
            "capacity": parts[4],
            "mount": parts[-1],
        }
        break
    return result


def parse_snapshots() -> list[dict]:
    out, _, _ = run(["tmutil", "listlocalsnapshots", "/"], timeout=10)
    snaps = []
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        match = re.search(r"(\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2})", line)
        snaps.append({"name": line, "date": match.group(1) if match else None})
    return snaps


def storage_categories(protected: list[str] | None = None) -> list[dict]:
    specs = [
        ("user-caches", "User caches", HOME / "Library/Caches", "caution", "cache", "App caches; some apps rebuild on next launch. Never delete the whole folder blind."),
        ("homebrew-cache", "Homebrew downloads", HOME / "Library/Caches/Homebrew", "safe", "command", "brew cleanup -s"),
        ("npm-cache", "npm cache", HOME / ".npm", "safe", "command", "npm cache clean --force"),
        ("npx-cache", "npx cache", HOME / ".npm/_npx", "safe", "delete", "Re-downloadable npx packages."),
        ("yarn-cache", "Yarn cache", HOME / "Library/Caches/Yarn", "safe", "command", "yarn cache clean"),
        ("pnpm-cache", "pnpm store", HOME / "Library/pnpm/store", "safe", "command", "pnpm store prune"),
        ("bun-cache", "Bun cache", HOME / ".bun/install/cache", "safe", "command", "bun pm cache rm"),
        ("pip-cache", "pip cache", HOME / "Library/Caches/pip", "safe", "command", "pip cache purge"),
        ("uv-cache", "uv cache", HOME / "Library/Caches/uv", "safe", "command", "uv cache clean"),
        ("go-build-cache", "Go build cache", HOME / "Library/Caches/go-build", "safe", "command", "go clean -cache"),
        ("gem-cache", "RubyGems cache", HOME / ".gem", "safe", "command", "gem cleanup"),
        ("conda-cache", "Conda package cache", HOME / "opt/anaconda3/pkgs", "caution", "command", "conda clean --all"),
        ("app-support", "Application Support", HOME / "Library/Application Support", "never", "review", "App data. Review only; never bulk-delete."),
        ("preferences", "Preferences", HOME / "Library/Preferences", "never", "review", "App settings. Review only; never bulk-delete."),
        ("playwright", "Playwright browsers", HOME / "Library/Caches/ms-playwright", "caution", "manual", "Re-downloadable, but large; remove only old revisions."),
        ("xcode-derived", "Xcode DerivedData", HOME / "Library/Developer/Xcode/DerivedData", "safe", "delete", "Regenerated on next build."),
        ("xcode-archives", "Xcode archives", HOME / "Library/Developer/Xcode/Archives", "move", "move", "Build history; quarantine before deleting."),
        ("xcode-device-support", "Xcode device support", HOME / "Library/Developer/Xcode/iOS DeviceSupport", "caution", "delete", "Rebuilt when a device is connected."),
        ("simulators", "Simulator devices", HOME / "Library/Developer/CoreSimulator/Devices", "caution", "command", "xcrun simctl delete unavailable"),
        ("ios-backups", "iOS backups", HOME / "Library/Application Support/MobileSync/Backup", "never", "move", "User data. Move only with explicit consent."),
        ("trash", "Trash", HOME / ".Trash", "caution", "empty", "Emptying is irreversible."),
        ("downloads", "Downloads", HOME / "Downloads", "caution", "move", "Move old files to quarantine; never delete."),
        ("logs", "User logs", HOME / "Library/Logs", "safe", "move", "Old logs only; move to quarantine."),
        ("docker", "Docker data", HOME / "Library/Containers/com.docker.docker/Data", "caution", "command", "docker system prune -f"),
        ("mail", "Mail data", HOME / "Library/Containers/com.apple.mail", "never", "never", "User data."),
        ("messages", "Messages data", HOME / "Library/Containers/com.apple.MobileSMS", "never", "never", "User data."),
        ("hf-cache", "Hugging Face cache", HOME / ".cache/huggingface/hub", "never", "never", "Model weights. Preserve the single-store rule."),
        ("system-caches", "System caches", Path("/Library/Caches"), "never", "never", "Requires sudo; not worth the risk."),
        ("swap", "Swap / VM", Path("/private/var/vm"), "never", "never", "macOS manages this."),
    ]
    rows = []
    from concurrent.futures import ThreadPoolExecutor

    with ThreadPoolExecutor(max_workers=6) as pool:
        sizes = list(pool.map(lambda spec: dir_size(spec[2], timeout=20), specs))
    for (cid, label, path, risk, action, note), size in zip(specs, sizes):
        rows.append({
            "id": cid,
            "label": label,
            "path": str(path),
            "display_path": display_path(path),
            "bytes": size,
            "exists": path.exists(),
            "risk": risk,
            "action": action,
            "note": note,
            "protected": is_protected(path, protected or []),
        })
    return rows


def comfy_paths() -> list[dict]:
    candidates = [
        HOME / "ComfyUI/models",
        HOME / "src/ComfyUI/models",
        HOME / "src/pjs/infra/local/ComfyUI/models",
        HOME / "src/pjs/infra/local/films",
    ]
    rows = []
    for path in candidates:
        if path.exists():
            rows.append({"path": str(path), "display_path": display_path(path), "bytes": dir_size(path, timeout=10)})
    return rows


def large_files(limit: int = 25) -> list[dict]:
    out, _, code = run(
        ["find", str(HOME), "-xdev", "-type", "f", "-size", "+1G", "-print"],
        timeout=20,
    )
    if code not in (0, 124) or not out:
        return []
    rows = []
    for line in out.splitlines():
        path = Path(line)
        try:
            stat = path.stat()
            if stat.st_mtime > cutoff:
                continue
            size = stat.st_size
        except OSError:
            continue
        rows.append({"path": str(path), "display_path": display_path(path), "bytes": size})
    rows.sort(key=lambda row: row["bytes"], reverse=True)
    return rows[:limit]


PROJECT_ROOTS = [
    HOME / "src",
    HOME / "Developer",
    HOME / "Projects",
    HOME / "code",
    HOME / "repos",
    HOME / "work",
]
ARTIFACT_NAMES = [
    "node_modules", "target", "build", "dist", ".next", ".nuxt", ".gradle",
    "DerivedData", "Pods", ".venv", "venv", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", "coverage",
]


def whitelist() -> list[str]:
    path = HOME / ".config/mac-maintenance/whitelist"
    if not path.exists():
        return []
    entries = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            entries.append(str(Path(line).expanduser().resolve()))
    return entries


def is_protected(path: str | Path, protected: list[str]) -> bool:
    try:
        resolved = Path(path).expanduser().resolve()
    except OSError:
        return False
    for item in protected:
        base = Path(item)
        if resolved == base or base in resolved.parents:
            return True
    return False


def project_artifacts(limit: int = 50) -> list[dict]:
    paths: list[Path] = []
    for root in PROJECT_ROOTS:
        if not root.exists():
            continue
        find_args = ["find", str(root), "-maxdepth", "5", "-type", "d", "("]
        for i, name in enumerate(ARTIFACT_NAMES):
            if i:
                find_args.append("-o")
            find_args.extend(["-name", name])
        find_args.extend([")", "-prune", "-print"])
        out, _, code = run(find_args, timeout=45)
        if code not in (0, 124):
            continue
        for line in out.splitlines():
            path = Path(line)
            if path.is_dir() and not path.is_symlink():
                paths.append(path)
    paths = paths[:200]
    rows = []
    for start in range(0, len(paths), 40):
        chunk = paths[start:start + 40]
        out, _, code = run(["du", "-sk", *[str(p) for p in chunk]], timeout=30)
        if code not in (0, 124):
            continue
        for line in out.splitlines():
            parts = line.split("\t", 1)
            if len(parts) != 2:
                parts = line.split(None, 1)
            if len(parts) != 2:
                continue
            try:
                size = int(parts[0]) * 1024
            except ValueError:
                continue
            path = Path(parts[1].strip())
            if path in paths:
                rows.append({"path": str(path), "display_path": display_path(path), "bytes": size})
    rows.sort(key=lambda row: row["bytes"], reverse=True)
    return rows[:limit]


def installers(limit: int = 40, days: int = 30) -> list[dict]:
    cutoff = time.time() - days * 86400
    out, _, code = run(
        ["find", str(HOME / "Downloads"), "-maxdepth", "2", "-type", "f", "(",
         "-name", "*.dmg", "-o", "-name", "*.pkg", "-o", "-name", "*.mpkg",
         "-o", "-name", "*.zip", ")", "-size", "+100M", "-print"],
        timeout=20,
    )
    if code not in (0, 124):
        return []
    rows = []
    for line in out.splitlines():
        path = Path(line)
        try:
            stat = path.stat()
            if stat.st_mtime > cutoff:
                continue
            size = stat.st_size
        except OSError:
            continue
        rows.append({"path": str(path), "display_path": display_path(path), "bytes": size})
    rows.sort(key=lambda row: row["bytes"], reverse=True)
    return rows[:limit]


def memory() -> dict:
    page_size = 4096
    out, _, _ = run(["sysctl", "-n", "hw.pagesize"])
    if out.isdigit():
        page_size = int(out)
    out, _, _ = run(["sysctl", "-n", "hw.memsize"])
    total = int(out) if out.isdigit() else None
    vm, _, _ = run(["vm_stat"])
    pages = {}
    for line in vm.splitlines():
        match = re.match(r"(.+?):\s+(\d+)\.", line)
        if match:
            pages[match.group(1).strip()] = int(match.group(2))
    pressure, _, _ = run(["memory_pressure", "-Q"], timeout=10)
    free_pct = None
    match = re.search(r"System-wide memory free percentage:\s*(\d+)%", pressure)
    if match:
        free_pct = int(match.group(1))
    swap_out, _, _ = run(["sysctl", "-n", "vm.swapusage"])
    swap = {}
    for key in ("total", "used", "free"):
        m = re.search(rf"{key}\s*=\s*([\d.]+)([MG])", swap_out)
        if m:
            value = float(m.group(1)) * (1024 if m.group(2) == "G" else 1)
            swap[key + "_mb"] = round(value, 1)
    return {
        "total_bytes": total,
        "page_size": page_size,
        "pages": pages,
        "free_percentage": free_pct,
        "swap": swap,
        "raw_pressure": pressure.splitlines()[:8],
    }


def processes() -> dict:
    out, _, _ = run(["ps", "-Ao", "pid=,pcpu=,pmem=,etime=,comm="], timeout=10)
    rows = []
    for line in out.splitlines():
        parts = line.split(None, 4)
        if len(parts) != 5:
            continue
        try:
            rows.append({
                "pid": int(parts[0]),
                "cpu_pct": float(parts[1]),
                "mem_pct": float(parts[2]),
                "elapsed": parts[3],
                "command": parts[4],
            })
        except ValueError:
            continue
    return {
        "top_cpu": sorted(rows, key=lambda r: r["cpu_pct"], reverse=True)[:12],
        "top_mem": sorted(rows, key=lambda r: r["mem_pct"], reverse=True)[:12],
        "count": len(rows),
    }


def load() -> dict:
    out, _, _ = run(["sysctl", "-n", "vm.loadavg"])
    match = re.search(r"\{ ([^}]+) \}", out)
    values = [float(x) for x in match.group(1).split()] if match else []
    ncpu_out, _, _ = run(["sysctl", "-n", "hw.ncpu"])
    return {"load": values, "ncpu": int(ncpu_out) if ncpu_out.isdigit() else None}


def power() -> dict:
    settings, _, _ = run(["pmset", "-g"])
    custom, _, _ = run(["pmset", "-g", "custom"])
    assertions, _, _ = run(["pmset", "-g", "assertions"])
    batt, _, _ = run(["pmset", "-g", "batt"])
    therm, _, _ = run(["pmset", "-g", "therm"])
    profiler, _, _ = run(["system_profiler", "SPPowerDataType"], timeout=12)
    battery = {}
    for key, pattern in (
        ("cycle_count", r"Cycle Count:\s*(\d+)"),
        ("condition", r"Condition:\s*(.+)"),
        ("maximum_capacity", r"Maximum Capacity:\s*(.+)"),
        ("fully_charged", r"Fully Charged:\s*(.+)"),
    ):
        match = re.search(pattern, profiler)
        if match:
            battery[key] = match.group(1).strip()
    return {
        "settings": settings,
        "custom": custom,
        "battery": battery,
        "battery_raw": batt,
        "thermal": therm,
        "assertions_raw": assertions.splitlines()[:120],
    }


def startup() -> dict:
    def plists(path: Path) -> list[str]:
        if not path.exists():
            return []
        return sorted(p.name for p in path.glob("*.plist"))

    launchctl, _, _ = run(["launchctl", "list"], timeout=10)
    labels = []
    for line in launchctl.splitlines()[1:]:
        parts = line.split("\t")
        if len(parts) >= 3:
            label = parts[2].strip()
            if label and not label.startswith("com.apple."):
                labels.append({"pid": parts[0], "status": parts[1], "label": label})
    brew, _, code = run(["brew", "services", "list"], timeout=15)
    return {
        "user_agents": plists(HOME / "Library/LaunchAgents"),
        "global_agents": plists(Path("/Library/LaunchAgents")),
        "global_daemons": plists(Path("/Library/LaunchDaemons")),
        "non_apple_launchctl": labels[:60],
        "brew_services": brew.splitlines()[:40] if code == 0 else [],
    }


def updates() -> dict:
    sw, _, sw_code = run(["softwareupdate", "-l", "--no-scan"], timeout=20)
    brew, _, brew_code = run(["brew", "outdated", "--quiet"], timeout=30)
    mas, _, mas_code = run(["mas", "outdated"], timeout=20)
    return {
        "macos_raw": sw.splitlines()[:40],
        "macos_ok": sw_code == 0,
        "brew_outdated": [line for line in brew.splitlines() if line.strip()] if brew_code == 0 else [],
        "mas_outdated": mas.splitlines()[:20] if mas_code == 0 else [],
    }


def security() -> dict:
    def first(cmd: list[str], timeout: int = 15) -> str:
        out, err, _ = run(cmd, timeout=timeout)
        return (out or err).splitlines()[0] if (out or err) else ""

    return {
        "filevault": first(["fdesetup", "status"]),
        "sip": first(["csrutil", "status"]),
        "gatekeeper": first(["spctl", "--status"]),
        "firewall": first(["/usr/libexec/ApplicationFirewall/socketfilterfw", "--getglobalstate"]),
        "timemachine": first(["tmutil", "latestbackup"], timeout=10),
    }


def network() -> dict:
    ifc, _, _ = run(["ifconfig", "-a"], timeout=10)
    interfaces = []
    for line in ifc.splitlines():
        if re.match(r"^[a-z0-9]+:", line):
            interfaces.append(line.split(":")[0])
    dns, _, _ = run(["scutil", "--dns"], timeout=10)
    nameservers = sorted(set(re.findall(r"nameserver\[\d+\]\s*:\s*(\S+)", dns)))
    listen, _, _ = run(["lsof", "-nP", "-iTCP", "-sTCP:LISTEN"], timeout=12)
    ports = []
    for line in listen.splitlines()[1:21]:
        parts = line.split()
        if len(parts) >= 9:
            ports.append({"command": parts[0], "pid": parts[1], "address": parts[8]})
    route, _, _ = run(["netstat", "-rn", "-f", "inet"], timeout=10)
    default = next((line for line in route.splitlines() if line.startswith("default")), "")
    return {
        "interfaces": interfaces,
        "dns": nameservers,
        "listening": ports,
        "default_route": " ".join(default.split()[:4]),
    }


def system_info() -> dict:
    boot_out, _, _ = run(["sysctl", "-n", "kern.boottime"])
    match = re.search(r"sec\s*=\s*(\d+)", boot_out)
    boot_seconds = int(match.group(1)) if match else 0
    uptime = time.time() - boot_seconds if boot_seconds else 0
    return {
        "hostname": platform.node(),
        "model": run(["sysctl", "-n", "hw.model"])[0],
        "chip": run(["sysctl", "-n", "machdep.cpu.brand_string"])[0],
        "macos": platform.mac_ver()[0],
        "kernel": platform.release(),
        "python": platform.python_version(),
        "uptime_hours": round(uptime / 3600, 1) if uptime > 0 else None,
    }


def build_report(audit: dict) -> str:
    disk = audit["disk"]["data"] or audit["disk"]["root"] or {}
    total = disk.get("total_bytes") or 1
    free = disk.get("free_bytes") or 0
    free_pct = free / total * 100 if total else 0
    categories = [c for c in audit["storage"]["categories"] if c.get("bytes")]
    safe = [c for c in categories if c["risk"] == "safe" and not c["protected"]]
    protected = [c for c in categories if c["protected"]]
    caution = [c for c in categories if c["risk"] == "caution" and not c["protected"]]
    never = [c for c in categories if c["risk"] == "never"]
    project_bytes = sum(p["bytes"] for p in audit["storage"].get("project_artifacts", []))
    safe_bytes = sum(c["bytes"] for c in safe) + project_bytes
    caution_bytes = sum(c["bytes"] for c in caution)
    protected_bytes = sum(c["bytes"] for c in protected)
    top = sorted(categories, key=lambda c: c["bytes"], reverse=True)[:10]

    lines = [
        f"# Mac maintenance audit — {audit['timestamp'][:10]}",
        "",
        f"**Host:** {audit['system']['hostname']} · {audit['system']['model']} · "
        f"{audit['system']['chip'] or 'Apple Silicon'} · macOS {audit['system']['macos']}",
        f"**Uptime:** {audit['system']['uptime_hours']} h",
        "",
        "## Bottom line",
        "",
        f"- Free space: **{human_bytes(free)} of {human_bytes(total)} ({free_pct:.1f}%)**",
        f"- Reclaimable from safe caches and build artifacts: **{human_bytes(safe_bytes)}**",
        f"- Caution categories (quarantine, do not blind-delete): **{human_bytes(caution_bytes)}**",
        f"- Protected by whitelist: **{human_bytes(protected_bytes)}**",
        f"- Preserved by policy: **{human_bytes(sum(c['bytes'] for c in never))}**",
        "",
    ]

    tm = (audit["security"].get("timemachine") or "").lower()
    if "failed" in tm or "error" in tm:
        lines.append("- **Attention:** Time Machine reported an error. Check the backup destination before relying on snapshots.")
    swap = audit["memory"].get("swap") or {}
    if swap.get("total_mb") and swap.get("used_mb", 0) / swap["total_mb"] > 0.75 and swap.get("used_mb", 0) > 4096:
        lines.append(f"- **Attention:** swap is {swap['used_mb']:.0f} MB of {swap['total_mb']:.0f} MB used. Check the top memory processes before adding more concurrent work.")

    if free < 10 * GIB or (free_pct < 2 and free < 50 * GIB):
        lines.append("- **Critical:** free space is below 10 GB or 2% of the volume. Clear a safe category before installing models or updating Xcode.")
    elif free < 20 * GIB or (free_pct < 5 and free < 50 * GIB):
        lines.append("- **Warning:** free space is below 20 GB or 5% of the volume. Plan a cleanup before the next large download.")
    else:
        lines.append("- Disk headroom is adequate for ordinary work; keep 20 GB free for model downloads and updates.")

    lines += ["", "## Disk", "", "| Volume | Total | Used | Free | Capacity |", "|---|---:|---:|---:|---:|"]
    for key in ("root", "data"):
        vol = audit["disk"].get(key)
        if vol:
            lines.append(
                f"| {vol['mount']} | {human_bytes(vol['total_bytes'])} | {human_bytes(vol['used_bytes'])} | "
                f"{human_bytes(vol['free_bytes'])} | {vol['capacity']} |"
            )
    if audit["disk"]["snapshots"]:
        lines += ["", f"Local Time Machine snapshots: **{len(audit['disk']['snapshots'])}**. They may hold purgeable space; do not delete without a recent backup."]

    lines += ["", "## Largest storage categories", "", "| Category | Size | Risk | Path |", "|---|---:|---|---|"]
    for c in top:
        lines.append(f"| {c['label']} | {human_bytes(c['bytes'])} | {c['risk']} | `{c['display_path']}` |")

    lines += ["", "## Safe cleanup candidates", ""]
    if safe:
        for c in sorted(safe, key=lambda x: x["bytes"], reverse=True):
            lines.append(f"- **{c['label']}** — {human_bytes(c['bytes'])} — `{c['display_path']}` — {c['note']}")
    else:
        lines.append("- None identified.")
    projects = audit["storage"].get("project_artifacts", [])
    if projects:
        lines.append(f"- **Project build artifacts** — {human_bytes(project_bytes)} — registered project roots — regenerable build output.")
    if projects:
        lines += ["", "## Project build artifacts", "",
                  "Regenerable build output in registered project roots. Review each root before purging; "
                  "`node_modules` is reinstallable but takes time.", "",
                  "| Project artifact | Size |", "|---|---:|"]
        for row in projects[:15]:
            lines.append(f"| `{row['display_path']}` | {human_bytes(row['bytes'])} |")

    installers = audit["storage"].get("installers", [])
    if installers:
        lines += ["", "## Installer files", "", "| File | Size |", "|---|---:|"]
        for row in installers[:10]:
            lines.append(f"| `{row['display_path']}` | {human_bytes(row['bytes'])} |")

    app_support = audit["storage"].get("app_support_top", [])
    if app_support:
        lines += ["", "## Application Support review", "",
                  "Largest entries. These are app data, not cache; review manually and never bulk-delete.", "",
                  "| Entry | Size |", "|---|---:|"]
        for row in app_support[:10]:
            lines.append(f"| `{display_path(row['path'])}` | {human_bytes(row['bytes'])} |")

    lines += ["", "## Memory and CPU", ""]
    mem = audit["memory"]
    lines.append(f"- RAM: {human_bytes(mem['total_bytes'])}")
    lines.append(f"- System-wide free memory: {mem['free_percentage'] if mem['free_percentage'] is not None else 'unknown'}%")
    if mem["swap"]:
        lines.append(f"- Swap used: {mem['swap'].get('used_mb', '?')} MB of {mem['swap'].get('total_mb', '?')} MB")
    loads = audit["load"]
    lines.append(f"- Load average: {', '.join(str(x) for x in loads['load']) or 'unknown'} across {loads['ncpu'] or '?'} CPUs")
    lines += ["", "| PID | CPU % | MEM % | Elapsed | Command |", "|---:|---:|---:|---|---|"]
    for p in audit["processes"]["top_cpu"][:8]:
        lines.append(f"| {p['pid']} | {p['cpu_pct']:.1f} | {p['mem_pct']:.1f} | {p['elapsed']} | `{p['command'][:80]}` |")

    lines += ["", "## Power", ""]
    bat = audit["power"]["battery"]
    if bat:
        lines.append(f"- Battery: {bat.get('condition', 'unknown')}; cycle count {bat.get('cycle_count', '?')}; maximum capacity {bat.get('maximum_capacity', '?')}")
    lines.append(f"- Thermal: {audit['power']['thermal'].splitlines()[0] if audit['power']['thermal'] else 'no thermal warning'}")
    assertions = audit["power"]["assertions_raw"]
    prevent = [line for line in assertions if "PreventSleep" in line or "PreventUserIdleSystemSleep" in line]
    lines.append(f"- Sleep assertions: {len(prevent)} lines mention PreventSleep.")
    if prevent:
        lines.append("")
        lines.append("```text")
        lines.extend(prevent[:8])
        lines.append("```")

    lines += ["", "## Startup and services", ""]
    st = audit["startup"]
    lines.append(f"- User LaunchAgents: {len(st['user_agents'])}")
    lines.append(f"- Global LaunchAgents: {len(st['global_agents'])}")
    lines.append(f"- Global LaunchDaemons: {len(st['global_daemons'])}")
    lines.append(f"- Non-Apple launchctl entries: {len(st['non_apple_launchctl'])}")
    if st["brew_services"]:
        lines += ["", "Brew services:", "", "```text", *st["brew_services"][:12], "```"]

    lines += ["", "## Updates", ""]
    up = audit["updates"]
    mac_lines = [line for line in up["macos_raw"] if line.strip()]
    lines.append(f"- macOS softwareupdate: {len(mac_lines)} lines; see raw report.")
    lines.append(f"- Homebrew outdated: {len(up['brew_outdated'])} formulae.")
    if up["mas_outdated"]:
        lines.append(f"- App Store outdated: {len(up['mas_outdated'])} apps.")

    lines += ["", "## Security and backup", ""]
    sec = audit["security"]
    lines.append(f"- FileVault: {sec['filevault']}")
    lines.append(f"- SIP: {sec['sip']}")
    lines.append(f"- Gatekeeper: {sec['gatekeeper']}")
    lines.append(f"- Firewall: {sec['firewall']}")
    lines.append(f"- Time Machine latest: {sec['timemachine'] or 'none reported'}")

    lines += ["", "## Network", ""]
    net = audit["network"]
    lines.append(f"- Interfaces: {', '.join(net['interfaces']) or 'none'}")
    lines.append(f"- DNS: {', '.join(net['dns']) or 'none'}")
    lines.append(f"- Default route: {net['default_route'] or 'none'}")
    if net["listening"]:
        lines += ["", "| Command | PID | Listen address |", "|---|---:|---|"]
        for row in net["listening"][:10]:
            lines.append(f"| {row['command']} | {row['pid']} | `{row['address']}` |")

    if audit["storage"]["large_files"]:
        lines += ["", "## Largest files", "", "| File | Size |", "|---|---:|"]
        for row in audit["storage"]["large_files"][:15]:
            lines.append(f"| `{row['display_path']}` | {human_bytes(row['bytes'])} |")

    lines += [
        "",
        "## Policy",
        "",
        "- This audit is read-only. It did not use sudo, delete files, or change settings.",
        "- Hugging Face weights, model stores, Mail, Messages, Photos, `~/src`, documents, and system caches are preserved.",
        "- Any cleanup must run one category at a time through `mac_apply.py --category <id> --apply --yes`, and moves user files to quarantine rather than deleting them.",
        "",
        f"Raw data: `{audit['out_dir']}/audit.json`",
        "",
    ]
    return "\n".join(lines)


def audit(out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    protected = whitelist()
    data = {
        "timestamp": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "out_dir": str(out_dir),
        "whitelist": protected,
        "system": system_info(),
        "disk": {"df": parse_df(), "snapshots": parse_snapshots()},
        "storage": {
            "categories": storage_categories(protected),
            "app_support_top": child_sizes(HOME / "Library/Application Support", timeout=12)[:20],
            "comfy": comfy_paths(),
            "large_files": large_files(),
            "project_artifacts": project_artifacts(),
            "installers": installers(),
        },
        "memory": memory(),
        "load": load(),
        "processes": processes(),
        "power": power(),
        "startup": startup(),
        "updates": updates(),
        "security": security(),
        "network": network(),
    }
    data["disk"]["data"] = data["disk"]["df"]["data"]
    data["disk"]["root"] = data["disk"]["df"]["root"]

    (out_dir / "audit.json").write_text(json.dumps(data, indent=2) + "\n")
    (out_dir / "report.md").write_text(build_report(data))
    return data


def main() -> None:
    ap = argparse.ArgumentParser(description="Read-only macOS maintenance audit")
    ap.add_argument("--out", type=Path, help="Output directory (default: ~/src/pjs/infra/local/mac-maintenance/<date>)")
    ap.add_argument("--quiet", action="store_true", help="Print only the report path")
    args = ap.parse_args()
    out_dir = args.out or (DEFAULT_OUT / datetime.now().strftime("%Y-%m-%d"))
    data = audit(out_dir)
    if args.quiet:
        print(out_dir / "report.md")
        return
    disk = data["disk"]["data"] or data["disk"]["root"] or {}
    free = disk.get("free_bytes", 0)
    total = disk.get("total_bytes", 1) or 1
    print(f"Report: {out_dir / 'report.md'}")
    print(f"Free: {human_bytes(free)} of {human_bytes(total)} ({free / total * 100:.1f}%)")
    safe_total = sum(c['bytes'] or 0 for c in data['storage']['categories'] if c['risk'] == 'safe')
    safe_total += sum(p['bytes'] for p in data['storage'].get('project_artifacts', []))
    print(f"Safe cache candidates: {human_bytes(safe_total)}")
    print(f"Caution categories: {human_bytes(sum(c['bytes'] or 0 for c in data['storage']['categories'] if c['risk'] == 'caution'))}")


if __name__ == "__main__":
    main()
