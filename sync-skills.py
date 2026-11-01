#!/usr/bin/env python3
"""sync-skills — mirror the skill bundle into every agent's skill root.

Syncs <bundle>/skills/* to one or more agent skill roots using symlinks by
default (single source of truth: edit the bundle, every agent sees it live).

    python3 sync-skills.py                 # sync all detected default roots
    python3 sync-skills.py --dry-run       # show what would change
    python3 sync-skills.py --prune         # also remove managed links whose
                                           # skill no longer exists in the bundle
    python3 sync-skills.py --copy          # copy instead of symlink
    python3 sync-skills.py --root ~/custom/skills   # extra root (repeatable)
    python3 sync-skills.py --only claude pi         # restrict roots
    python3 sync-skills.py --force         # back up conflicts as <name>.conflict-<ts>

Safety model:
- A target entry is ours only if it is listed in the root's manifest
  (<root>/.skill-bundle-manifest.json) or is a symlink whose resolved path
  lives inside this bundle. Such entries are adopted and managed.
- Anything else (a real directory, a foreign symlink) is a CONFLICT: it is
  never touched without --force (which moves it aside, does not delete).
- Pruning only removes entries the manifest says are ours.

Exit codes: 0 clean, 1 conflicts skipped (see report), 2 fatal.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import time
from pathlib import Path

BUNDLE_DIR = Path(__file__).resolve().parent
SKILLS_DIR = BUNDLE_DIR / "skills"
MANIFEST_NAME = ".skill-bundle-manifest.json"

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def default_roots() -> list[tuple[str, Path]]:
    home = Path.home()
    return [
        ("claude", home / ".claude" / "skills"),
        ("opencode", home / ".config" / "opencode" / "skill"),
        ("agents", home / ".agents" / "skills"),
        ("pi", home / ".pi" / "agent" / "skills"),
        ("codex", home / ".codex" / "skills"),
    ]


def bundle_skills() -> dict[str, Path]:
    """name -> skill dir, validated."""
    skills: dict[str, Path] = {}
    if not SKILLS_DIR.is_dir():
        sys.exit(f"bundle skills dir not found: {SKILLS_DIR}")
    for d in sorted(SKILLS_DIR.iterdir()):
        if not d.is_dir() or d.name.startswith("_"):
            continue
        skill_md = d / "SKILL.md"
        if not skill_md.is_file():
            print(f"  warn: {d.name}/ has no SKILL.md — skipped", file=sys.stderr)
            continue
        head = skill_md.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"^name:\s*(\S+)", head, re.M)
        if not m:
            print(f"  warn: {d.name}/SKILL.md has no name: — skipped", file=sys.stderr)
            continue
        if m.group(1) != d.name:
            print(f"  warn: {d.name}/ name={m.group(1)!r} != dir — skipped", file=sys.stderr)
            continue
        if not NAME_RE.match(d.name):
            print(f"  warn: {d.name}/ not a valid skill name — skipped", file=sys.stderr)
            continue
        skills[d.name] = d
    return skills


def load_manifest(root: Path) -> dict:
    p = root / MANIFEST_NAME
    if p.is_file():
        try:
            data = json.loads(p.read_text())
            if isinstance(data, dict) and isinstance(data.get("skills"), dict):
                return data["skills"]
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def save_manifest(root: Path, managed: dict) -> None:
    p = root / MANIFEST_NAME
    p.write_text(
        json.dumps(
            {"bundle": str(BUNDLE_DIR), "updated": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "skills": managed},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def in_bundle(path: Path) -> bool:
    try:
        return SKILLS_DIR in path.resolve().parents
    except OSError:
        return False


def sync_root(
    label: str,
    root: Path,
    skills: dict[str, Path],
    copy: bool,
    prune: bool,
    force: bool,
    dry: bool,
    create: bool,
) -> int:
    """Returns number of conflicts."""
    print(f"\n[{label}] {root}")
    if not root.exists():
        if not create or dry:
            print(f"  missing (would create)" if dry else "  missing — skipped (use default --create behavior or pass a --root)")
            return 0
        root.mkdir(parents=True, exist_ok=True)
        print(f"  created root")

    managed = load_manifest(root)
    report = {"linked": [], "current": [], "updated": [], "conflict": [], "pruned": [], "stale": []}

    def entry_state(name: str) -> str:
        """'ours' | 'foreign' | 'absent' for the existing entry at root/name."""
        p = root / name
        if name in managed:
            return "ours"
        if p.is_symlink():
            return "ours" if in_bundle(p) else "foreign"
        if p.exists():
            return "foreign"
        return "absent"

    for name, src in skills.items():
        state = entry_state(name)
        link = root / name
        if state == "foreign":
            kind = "symlink" if link.is_symlink() else "directory"
            if force:
                backup = root / f"{name}.conflict-{int(time.time())}"
                if not dry:
                    link.rename(backup)
                report["updated"].append(f"{name} (conflicting {kind} moved to {backup.name})")
                state = "absent"
            else:
                report["conflict"].append(f"{name} (existing {kind} left untouched)")
                continue
        if state == "ours":
            if link.is_dir() and not link.is_symlink():
                # a managed name is now occupied by a real directory — refuse, do not rmtree
                report["conflict"].append(f"{name} (manifest says ours but entry is a real directory)")
                continue
            if link.is_symlink() and not copy:
                target_ok = link.resolve() == src.resolve()
                if target_ok:
                    report["current"].append(name)
                else:
                    if not dry:
                        link.unlink()
                        link.symlink_to(src)
                    report["updated"].append(f"{name} (re-linked to {src})")
            else:  # stale copy or copied entry being replaced
                if not dry:
                    if link.exists():
                        shutil.rmtree(link)
                    shutil.copytree(src, link)
                report["updated"].append(f"{name} (re-copied from {src})")
        elif state == "absent":
            if not dry:
                if copy:
                    shutil.copytree(src, link)
                else:
                    link.symlink_to(src)
            report["linked"].append(name)
        managed[name] = str(src)

    if prune:
        for name in list(managed):
            if name in skills:
                continue
            p = root / name
            if p.is_symlink() and not p.exists():
                if not dry:
                    p.unlink()
                report["stale"].append(name)
            elif p.is_symlink() and in_bundle(p):
                if not dry:
                    p.unlink()
                report["pruned"].append(name)
            elif p.is_dir() and not (p / MANIFEST_NAME).exists():
                if not dry:
                    shutil.rmtree(p)
                report["pruned"].append(name)
            del managed[name]

    if not dry:
        save_manifest(root, managed)

    for key in ("linked", "updated", "current", "conflict", "pruned", "stale"):
        items = report[key]
        if not items:
            continue
        head = f"  {key:9s} {len(items):3d}"
        if len(items) <= 6 or key == "conflict":
            print(head)
            for i in items:
                print(f"            - {i}")
        else:
            print(f"{head}  (e.g. {items[0]})")
    return len(report["conflict"])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="report changes without making them")
    ap.add_argument("--prune", action="store_true", help="remove managed entries whose skill is gone from the bundle")
    ap.add_argument("--copy", action="store_true", help="copy skill dirs instead of symlinking")
    ap.add_argument("--force", action="store_true", help="move conflicting entries aside as <name>.conflict-<ts>")
    ap.add_argument("--create", action="store_true", default=True, help=argparse.SUPPRESS)
    ap.add_argument("--no-create", dest="create", action="store_false", help="skip roots that do not exist yet")
    ap.add_argument("--root", action="append", default=[], metavar="PATH", help="extra skill root (repeatable)")
    ap.add_argument("--only", nargs="*", default=[], metavar="NAME", help="restrict to these root names")
    ap.add_argument("--list", action="store_true", help="list bundle skills and exit")
    args = ap.parse_args()

    skills = bundle_skills()
    if args.list:
        for name in skills:
            print(name)
        return 0
    if not skills:
        sys.exit("no valid skills found in the bundle")
    print(f"bundle: {BUNDLE_DIR}  ({len(skills)} skills)  mode={'copy' if args.copy else 'symlink'}{'  DRY-RUN' if args.dry_run else ''}")

    roots = default_roots()
    extra = [(f"custom:{Path(p).name}", Path(p).expanduser()) for p in args.root]
    if args.only:
        wanted = set(args.only)
        roots = [r for r in roots if r[0] in wanted] + [r for r in extra if r[0] in wanted]
        if not roots:
            sys.exit(f"no matching roots for --only {args.only} (available: {[r[0] for r in default_roots() + extra]})")
    else:
        roots = roots + extra

    total_conflicts = 0
    for label, root in roots:
        total_conflicts += sync_root(label, root, skills, args.copy, args.prune, args.force, args.dry_run, args.create)

    print(f"\n{'DRY-RUN: ' if args.dry_run else ''}done — {len(skills)} skills, roots: {len(roots)}, conflicts: {total_conflicts}")
    if total_conflicts:
        print("conflicts were skipped — re-run with --force to move them aside, or resolve by hand")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
