#!/usr/bin/env python3
"""pull_models — fetch the film-production model set into the HF cache.

Every model is downloaded into the shared Hugging Face hub cache
(`HF_HUB_CACHE`, `HF_HOME/hub`, or `~/.cache/huggingface/hub`). No second
model store is created. The script is idempotent: models already present are
skipped, partial downloads resume, and nothing is deleted.

    python3 pull_models.py --list
    python3 pull_models.py --check
    python3 pull_models.py --tier core --dry-run
    python3 pull_models.py --tier core --yes
    python3 pull_models.py --tier core,quality --yes
    python3 pull_models.py --model ltx-2.3-mlx-q4 --yes
    python3 pull_models.py --tier tools --via rapid-mlx --yes

Tiers:
    core      the minimum local production set (LLM, video, image, TTS, STT)
    quality   core-quality additions: Qwen-Image, Wan 2.2 I2V-A14B
    optional  LTX-2.5, Qwen-Image-Edit, HiDream
    tools     MuseTalk, LatentSync, ACE-Step, MusicGen

The sizes are approximate footprints from model metadata; the disk check uses
them plus a reserve. A real pull may be slightly larger because repos can ship
extra files.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

MODELS = [
    # tier, name, rapid-mlx alias, HF repo, approx GB, note
    ("core", "qwen3.6-35b-ud", "qwen3.6-35b-ud",
     "unsloth/Qwen3.6-35B-A3B-UD-MLX-4bit", 20.2, "LLM fast (cached on this machine)"),
    ("core", "qwen3.8-27b-4bit", "qwen3.8-27b-4bit",
     "rapid-mlx/Qwen3.8-27B-4bit-MTP-MLX", 20.0, "LLM quality, 4-bit + MTP"),
    ("core", "ltx-2.3-mlx-q4", "ltx-2.3-mlx-q4",
     "dgrauet/ltx-2.3-mlx-q4", 14.0,
     "video default, joint audio-video, q4 — the ltx-2-mlx author's own pack"),
    ("core", "wan2.2-ti2v-5b-q8", "wan2.2-ti2v-5b-q8",
     "Anes1032/Wan2.2-TI2V-5B-mlx-q8", 18.2, "video practical quality, q8"),
    ("core", "flux2-klein-4b", "flux2-klein-4b",
     "Runpod/FLUX.2-klein-4B-mflux-4bit", 4.3, "image fast (cached on this machine)"),
    ("core", "qwen3-tts-4bit", "qwen3-tts-4bit",
     "mlx-community/Qwen3-TTS-12Hz-1.7B-CustomVoice-4bit", 2.2, "TTS, multilingual"),
    ("core", "chatterbox-4bit", "chatterbox-4bit",
     "mlx-community/chatterbox-turbo-4bit", 0.4, "TTS, expressive"),
    ("core", "kokoro-4bit", "kokoro-4bit",
     "mlx-community/Kokoro-82M-4bit", 0.3, "TTS, scratch VO"),
    ("core", "whisper", "whisper",
     "mlx-community/whisper-large-v3-mlx", 2.9, "STT, captions"),
    ("core", "qwen3-forced-aligner", "qwen3-forced-aligner",
     "mlx-community/Qwen3-ForcedAligner-0.6B-8bit", 1.2, "word-level alignment"),

    ("quality", "qwen-image", "qwen-image",
     "mflux-community/qwen-image-mflux-q6", 28.9, "image with legible text, q6"),
    ("quality", "wan2.2-i2v-a14b-q8", "wan2.2-i2v-a14b-q8",
     "Anes1032/Wan2.2-I2V-A14B-mlx-q8", 39.7, "image-to-video, q8"),

    ("optional", "qwen-image-edit", "qwen-image-edit",
     "OsaurusAI/Qwen-Image-Edit-mflux-q8", 34.9, "image edits, q8"),
    ("optional", "ltx-2.5-mlx-q8", "ltx-2.5-mlx-q8",
     "MrMofer/ltx-2.5-mlx-q8", 63.0,
     "hero video + audio, q8 — needs ~63 GB free disk; revisit after a disk upgrade"),
    ("optional", "hidream-o1-dev", "hidream-o1-dev",
     "mlx-community/HiDream-O1-Image-Dev-mlx-bf16", 16.4, "image quality, bf16"),

    ("tools", "musetalk-1.5", None,
     "mlx-community/MuseTalk-1.5-fp16", 7.0, "lip-sync, realtime MLX"),
    ("tools", "latentsync-1.5", None,
     "ByteDance/LatentSync-1.5", 5.0, "lip-sync, quality"),
    ("tools", "ace-step-1.5", None,
     "ACE-Step/ACE-Step-v1-3.5B", 7.0, "music generation"),
    ("tools", "musicgen-medium", None,
     "facebook/musicgen-medium", 3.0, "score / beds"),
]

TIERS = ["core", "quality", "optional", "tools"]


def cache_root(arg: str | None) -> Path:
    if arg:
        return Path(arg).expanduser().resolve()
    if os.environ.get("HF_HUB_CACHE"):
        return Path(os.environ["HF_HUB_CACHE"]).expanduser().resolve()
    if os.environ.get("HF_HOME"):
        return (Path(os.environ["HF_HOME"]).expanduser() / "hub").resolve()
    return (Path.home() / ".cache" / "huggingface" / "hub").resolve()


def repo_dir(cache: Path, repo: str) -> Path:
    org, name = repo.split("/", 1)
    return cache / f"models--{org}--{name}"


def present(cache: Path, repo: str) -> bool:
    d = repo_dir(cache, repo)
    snap = d / "snapshots"
    blobs = d / "blobs"
    if not (d / "refs" / "main").is_file() or not snap.is_dir() or not blobs.is_dir():
        return False
    # a download in flight leaves .incomplete blobs; do not report it as present
    if any(blobs.glob("*.incomplete")):
        return False
    # a config-only snapshot is not a usable model
    if not any(p.is_file() and p.stat().st_size > 1_000_000 for p in blobs.iterdir()):
        return False
    return any(p.is_dir() and any(p.iterdir()) for p in snap.iterdir())


def select(args):
    chosen = []
    tiers = set()
    for t in args.tier:
        tiers.update(x.strip() for x in t.split(",") if x.strip())
    for t in tiers:
        if t not in TIERS:
            raise SystemExit(f"unknown tier: {t} (choose {', '.join(TIERS)})")
    if args.all:
        tiers = set(TIERS)
    if not tiers:
        tiers = {"core"}
    wanted = {m[1] for m in MODELS if m[0] in tiers}
    if args.model:
        wanted = set(args.model)
        unknown = wanted - {m[1] for m in MODELS}
        if unknown:
            raise SystemExit("unknown model(s): " + ", ".join(sorted(unknown)))
    for name in args.exclude:
        wanted.discard(name.strip())
    for m in MODELS:
        if m[1] in wanted:
            chosen.append(m)
    return chosen


def cmd_list():
    print(f"{'tier':8} {'name':24} {'~GB':>6}  repo")
    for tier, name, _alias, repo, size, _note in MODELS:
        print(f"{tier:8} {name:24} {size:6.1f}  {repo}")
    totals = {}
    for tier, _n, _a, _r, size, _note in MODELS:
        totals[tier] = totals.get(tier, 0) + size
    print("\nTotals: " + ", ".join(f"{t} {totals[t]:.1f} GB" for t in TIERS))


def main() -> None:
    ap = argparse.ArgumentParser(prog="pull_models", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tier", action="append", default=[],
                    help="tier to pull; repeatable or comma-separated (default: core)")
    ap.add_argument("--all", action="store_true", help="all tiers")
    ap.add_argument("--model", action="append", default=[], help="explicit model name; repeatable")
    ap.add_argument("--exclude", action="append", default=[], help="model name to skip")
    ap.add_argument("--cache-dir", help="HF hub cache (default: HF_HUB_CACHE / HF_HOME/hub)")
    ap.add_argument("--via", choices=["hf", "rapid-mlx"], default="hf",
                    help="download tool (default: hf; rapid-mlx only for aliases)")
    ap.add_argument("--reserve-gb", type=float, default=15.0,
                    help="free space to keep after the pull (default: 15)")
    ap.add_argument("--allow-tight", action="store_true",
                    help="proceed even if the disk check fails")
    ap.add_argument("--retries", type=int, default=2, help="retries per model (default: 2)")
    ap.add_argument("--log", help="log path (default: <cache>/../pull-film-models.log)")
    ap.add_argument("--force", action="store_true", help="re-download even if present")
    ap.add_argument("--check", action="store_true", help="report presence only")
    ap.add_argument("--dry-run", action="store_true", help="show the plan and commands")
    ap.add_argument("--yes", action="store_true", help="execute the downloads")
    ap.add_argument("--list", action="store_true", help="list models and tiers")
    args = ap.parse_args()

    if args.list:
        cmd_list()
        return

    cache = cache_root(args.cache_dir)
    cache.mkdir(parents=True, exist_ok=True)
    chosen = select(args)

    rows = []
    missing_gb = 0.0
    for tier, name, alias, repo, size, note in chosen:
        have = present(cache, repo) and not args.force
        if not have:
            missing_gb += size
        rows.append((tier, name, alias, repo, size, note, have))

    print(f"cache: {cache}")
    print(f"{'tier':8} {'name':24} {'~GB':>6}  {'status':8} note")
    for tier, name, _alias, _repo, size, note, have in rows:
        print(f"{tier:8} {name:24} {size:6.1f}  {'present' if have else 'missing':8} {note}")
    free_gb = shutil.disk_usage(cache).free / 1e9
    print(f"\nmissing: {missing_gb:.1f} GB  |  free: {free_gb:.1f} GB  |  "
          f"reserve: {args.reserve_gb:.1f} GB")

    if args.check:
        raise SystemExit(0 if missing_gb == 0 else 1)

    todo = [r for r in rows if not r[6]]
    if not todo:
        print("nothing to do; all selected models are present")
        return

    if missing_gb + args.reserve_gb > free_gb:
        msg = (f"disk check failed: need ~{missing_gb + args.reserve_gb:.1f} GB "
               f"including reserve, have {free_gb:.1f} GB")
        if not args.allow_tight:
            print(msg, file=sys.stderr)
            print("free space, choose fewer models, or pass --allow-tight", file=sys.stderr)
            raise SystemExit(2)
        print("warning: " + msg + " (continuing because --allow-tight)", file=sys.stderr)

    hf = shutil.which("hf") or shutil.which("huggingface-cli")
    rapid = shutil.which("rapid-mlx") if args.via == "rapid-mlx" else None
    if args.via == "rapid-mlx" and not rapid:
        print("rapid-mlx not found; falling back to hf", file=sys.stderr)
        args.via = "hf"
    if args.via == "hf" and not hf:
        print("hf CLI not found (install huggingface_hub / hf)", file=sys.stderr)
        raise SystemExit(2)

    env = os.environ.copy()
    env["HF_HUB_CACHE"] = str(cache)
    env.setdefault("HF_HOME", str(cache.parent))

    log_path = Path(args.log).expanduser() if args.log else cache.parent / "pull-film-models.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    def log(line: str):
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        with log_path.open("a", encoding="utf-8") as fh:
            fh.write(f"{stamp} {line}\n")

    if args.dry_run:
        for tier, name, alias, repo, size, _note, _have in todo:
            if args.via == "rapid-mlx" and alias:
                cmd = [rapid, "pull", alias]
            else:
                cmd = [hf, "download", repo, "--cache-dir", str(cache)]
            print(f"[{tier}] {name}: " + " ".join(cmd))
        print(f"\ntotal to download: {missing_gb:.1f} GB")
        return

    if not args.yes:
        print("\nplan is read-only. re-run with --yes to download.")
        return

    failed = []
    pulled = 0
    started = time.time()
    for tier, name, alias, repo, size, _note, _have in todo:
        if args.via == "rapid-mlx" and alias:
            cmd = [rapid, "pull", alias]
        else:
            cmd = [hf, "download", repo, "--cache-dir", str(cache)]
        print(f"\n[{tier}] {name} (~{size:.1f} GB)\n  " + " ".join(cmd))
        log(f"START {tier}/{name} repo={repo} size={size:.1f}GB via={args.via}")
        ok = False
        for attempt in range(1, args.retries + 2):
            t0 = time.time()
            proc = subprocess.run(cmd, env=env)
            took = time.time() - t0
            if proc.returncode == 0 and present(cache, repo):
                ok = True
                pulled += 1
                print(f"  ok ({took:.0f}s)")
                log(f"OK {tier}/{name} {took:.0f}s attempt={attempt}")
                break
            print(f"  attempt {attempt} failed (exit {proc.returncode}, {took:.0f}s)")
            log(f"FAIL {tier}/{name} exit={proc.returncode} attempt={attempt} {took:.0f}s")
            if attempt <= args.retries:
                time.sleep(min(30, 5 * attempt))
        if not ok:
            failed.append(name)

    elapsed = time.time() - started
    print(f"\ndone: {pulled} pulled, {len(failed)} failed, {elapsed/60:.1f} min")
    print(f"cache: {cache}")
    print(f"log:   {log_path}")
    if failed:
        print("failed: " + ", ".join(failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
