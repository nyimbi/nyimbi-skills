#!/usr/bin/env python3
"""qc — technical QC sweep for a film delivery package.

Reads 05_post/deliver/, probes every media file, measures loudness, sanity-checks
captions, cross-checks the delivery manifest, and writes qc-report.md. Exit 1 if
any check fails, so it can gate a pipeline.

Usage: qc.py <project> [--target streaming|broadcast] [--lufs N]
       qc.py <project> --file path/to/master.mp4   # probe a single file
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

CHECKS = []  # (name, ok, detail)


def check(name: str, ok: bool, detail: str = "") -> None:
    CHECKS.append((name, ok, detail))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}{(' — ' + detail) if detail else ''}")


def run(cmd: list[str]) -> str:
    return subprocess.run(cmd, capture_output=True, text=True).stdout


def ffprobe(path: Path) -> dict | None:
    out = run([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration,size,bit_rate:stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels",
        "-of", "json", str(path),
    ])
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return None


def loudness(path: Path) -> dict | None:
    out = run([
        "ffmpeg", "-hide_banner", "-i", str(path),
        "-af", "loudnorm=print_format=json", "-f", "null", "-",
    ])
    m = re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", out, re.S)
    if not m:
        return None
    try:
        d = json.loads(m[-1])
        return {"integrated": float(d["input_i"]), "tp": float(d["input_tp"])}
    except (KeyError, ValueError, json.JSONDecodeError):
        return None


def probe_media(path: Path, want_lufs: float) -> None:
    info = ffprobe(path)
    if not info:
        check(f"{path.name}: probe", False, "ffprobe returned nothing")
        return
    streams = info.get("streams", [])
    vids = [s for s in streams if s.get("codec_type") == "video"]
    auds = [s for s in streams if s.get("codec_type") == "audio"]
    dur = float(info.get("format", {}).get("duration", 0))
    check(f"{path.name}: video stream", bool(vids),
          f"{vids[0].get('width')}x{vids[0].get('height')} @{vids[0].get('r_frame_rate')}" if vids else "none")
    check(f"{path.name}: audio stream", bool(auds),
          f"{auds[0].get('sample_rate')} Hz, {auds[0].get('channels')} ch" if auds else "none")
    check(f"{path.name}: duration", dur > 0, f"{dur:.1f} s")
    if path.suffix == ".mp4" and vids:
        check(f"{path.name}: bitrate", float(info.get("format", {}).get("bit_rate", 0)) > 1e6)
    if auds:
        ln = loudness(path)
        if ln:
            check(f"{path.name}: loudness", abs(ln["integrated"] - want_lufs) <= 1.0,
                  f"{ln['integrated']:.1f} LUFS (target {want_lufs:.0f}), peak {ln['tp']:.1f} dBTP")
            check(f"{path.name}: true peak", ln["tp"] <= -1.0, f"{ln['tp']:.1f} dBTP")
        else:
            check(f"{path.name}: loudness", False, "loudnorm gave no measurement")


def probe_captions(path: Path) -> None:
    text = path.read_text(encoding="utf-8", errors="replace")
    cues = re.findall(r"^\d+\s*$", text, re.M)
    times = re.findall(r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})", text)
    check(f"{path.name}: cue count", len(cues) >= 1, f"{len(cues)} cues")
    if times:
        last = max(int(h) * 3600 + int(m) * 60 + int(s) for h, m, s, _ in times)
        check(f"{path.name}: cue span", last > 0, f"last cue at {last}s")
    check(f"{path.name}: utf-8", "�" not in text, "no replacement characters")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("project", type=Path)
    ap.add_argument("--target", choices=["streaming", "broadcast"], default="streaming")
    ap.add_argument("--lufs", type=float, default=None)
    ap.add_argument("--file", type=Path, default=None)
    args = ap.parse_args()
    want_lufs = args.lufs if args.lufs is not None else (-14.0 if args.target == "streaming" else -23.0)

    if args.file:
        probe_media(args.file, want_lufs)
    else:
        deliver = args.project / "05_post" / "deliver"
        if not deliver.is_dir():
            print(f"no delivery dir at {deliver}", file=sys.stderr)
            return 2
        media = sorted(p for p in deliver.iterdir() if p.suffix in (".mp4", ".mov"))
        captions = sorted(p for p in deliver.iterdir() if p.suffix in (".srt", ".vtt"))
        for m in media:
            probe_media(m, want_lufs)
        for c in captions:
            probe_captions(c)
        # continuity: no master shorter than half the longest
        durs = []
        for m in media:
            info = ffprobe(m)
            if info:
                durs.append((float(info.get("format", {}).get("duration", 0)), m.name))
        if len(durs) >= 2:
            longest, shortest = max(durs), min(durs)
            check("aspect variants: duration spread", shortest[0] >= longest[0] * 0.5,
                  f"longest {longest[1]} {longest[0]:.0f}s, shortest {shortest[1]} {shortest[0]:.0f}s")
        # manifest cross-check
        manifest = deliver / "delivery-manifest.md"
        if manifest.is_file():
            text = manifest.read_text()
            listed = {m.name: (m.name in text) for m in media + captions}
            missing = [n for n, ok in listed.items() if not ok]
            check("manifest lists every deliverable", not missing,
                  ", ".join(missing) if missing else f"{len(listed)} files")
        else:
            check("delivery manifest exists", False, str(manifest))

    report = args.project / "05_post" / "deliver" / "qc-report.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    fails = [(n, d) for n, ok, d in CHECKS if not ok]
    lines = ["# QC Report", "",
             f"Target: {args.target} ({want_lufs:.0f} LUFS integrated, true peak <= -1 dBTP)", ""]
    for name, ok, detail in CHECKS:
        mark = "x" if ok else " "
        lines.append(f"- [{mark}] {name}" + (f" — {detail}" if detail else ""))
    lines += ["", f"Result: **{'PASS' if not fails else 'FAIL'}** ({len(fails)} failing)"]
    report.write_text("\n".join(lines) + "\n")
    print(f"\nqc-report: {report}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
