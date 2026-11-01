#!/usr/bin/env python3
"""filmctl — scaffold, validate, compile prompts, and assemble a film project.

It never generates and never spends money. It creates the directory contract,
checks that stage artifacts exist, compiles canonical shot records into model
dialects, and concatenates approved takes into a rough cut.

Commands:
    new <slug> [--format short] [--runtime 480] [--aspect 16:9] [--tier local]
    status <project>
    validate <project> [--stage development]
    doctor
    prompts <project> [--dialect veo]
    assemble <project> [--width 1280] [--height 720] [--fps 24]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import NoReturn

STAGES = [
    "development",
    "design",
    "preproduction",
    "prepare",
    "generation",
    "assemble",
    "sound",
    "finish",
    "deliver",
]

REQUIRED_SHOT_FIELDS = [
    "id",
    "scene",
    "duration_s",
    "function",
    "shot_size",
    "subject",
    "action",
    "environment",
    "camera_move",
    "lighting",
    "negative",
    "dialect",
    "control",
    "priority",
]

STAGE_ARTIFACTS = {
    "development": [
        "01_story/logline.md",
        "01_story/beats.md",
        "01_story/screenplay.fountain",
    ],
    "design": [
        "02_design/style-lock.md",
        "02_design/world-bible.md",
        "continuity-ledger.md",
    ],
    "preproduction": [
        "03_plan/shots.json",
        "03_plan/shot-list.csv",
        "03_plan/animatic.mp4",
    ],
    "prepare": [],
    "generation": [],
    "assemble": ["05_post/rough-cut.mp4"],
    "sound": ["05_post/sound/mix.wav"],
    "finish": ["05_post/deliver/captions.srt"],
    "deliver": [
        "05_post/deliver/qc-report.md",
        "05_post/deliver/delivery-manifest.md",
        "06_marketing/poster/poster-manifest.md",
    ],
}

PRODUCTION_TEMPLATE = """# {slug}

**Format:** {fmt} · **Runtime:** {runtime} s · **Aspect:** {aspect} · **Tier:** {tier}
**Stage:** development · **Next gate:** premise

## Logline

_One sentence: when ..., <protagonist> must ..., before ..., but ..._

## Approvals

| Gate | Date | Decision |
|---|---|---|
| Premise | | |
| Script | | |
| Design | | |
| Shot plan | | |
| Picture lock | | |
| Delivery | | |

## Open risks

| Risk | Owner | Mitigation |
|---|---|---|

## Links

- Script:
- Style:
- Shot list:
- Generation log:
- Cut:
"""

DECISION_TEMPLATE = """# Decision Log

One entry per irreversible choice. State the decision, the alternatives, the reason,
and the cost of reversing it.

## YYYY-MM-DD — <decision>

- Alternatives:
- Reason:
- Reversal cost:
"""

LEDGER_TEMPLATE = """# Continuity Ledger

## Canonical

- Style: 02_design/style-lock.md
- Characters:
- Locations:
- Model versions:

## Characters

## Locations

## Props

## Timeline
"""


def fail(msg: str, code: int = 1) -> NoReturn:
    print(f"filmctl: {msg}", file=sys.stderr)
    raise SystemExit(code)


def project_path(arg: str) -> Path:
    p = Path(arg).expanduser().resolve()
    if not p.is_dir():
        fail(f"project not found: {p}")
    return p


def load_json(path: Path, default=None):
    if not path.is_file():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{path}: invalid JSON ({exc})")


def cmd_new(args) -> None:
    root = Path(args.root).expanduser().resolve()
    project = (root / args.slug).resolve()
    if project.exists() and any(project.iterdir()):
        fail(f"{project} already exists and is not empty")

    dirs = [
        "01_story/characters",
        "02_design/characters",
        "02_design/refs/characters",
        "02_design/refs/locations",
        "02_design/refs/props",
        "02_design/floorplans",
        "03_plan/storyboards",
        "04_gen/prompts",
        "04_gen/keyframes",
        "04_gen/shots",
        "04_gen/lipsync",
        "04_gen/normalized",
        "05_post/edit",
        "05_post/sound/stems",
        "05_post/deliver",
        "06_marketing/poster/art",
    ]
    for d in dirs:
        (project / d).mkdir(parents=True, exist_ok=True)

    state = {
        "project": args.slug,
        "format": args.format,
        "runtime_s": args.runtime,
        "aspect": args.aspect,
        "fps": args.fps,
        "tier": args.tier,
        "stage": "development",
        "stages": {s: "pending" for s in STAGES},
        "approvals": {
            "premise": None,
            "script": None,
            "design": None,
            "shot_plan": None,
            "picture_lock": None,
            "delivery": None,
        },
        "models": {},
        "capabilities": {"probed": None, "comfyui": False, "cloud_keys": []},
        "budget": {"cap_usd": 0, "reserved_usd": 0, "spent_usd": 0, "gpu_minutes": 0},
    }
    state["stages"]["development"] = "in_progress"

    (project / "state.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    (project / "PRODUCTION.md").write_text(
        PRODUCTION_TEMPLATE.format(
            slug=args.slug,
            fmt=args.format,
            runtime=args.runtime,
            aspect=args.aspect,
            tier=args.tier,
        ),
        encoding="utf-8",
    )
    (project / "decision-log.md").write_text(DECISION_TEMPLATE, encoding="utf-8")
    (project / "continuity-ledger.md").write_text(LEDGER_TEMPLATE, encoding="utf-8")

    print(f"created {project}")
    print("next: write 01_story/logline.md, beats.md, screenplay.fountain")


def cmd_status(args) -> None:
    project = project_path(args.project)
    state = load_json(project / "state.json")
    if not state:
        fail(f"{project}/state.json missing")
    assert isinstance(state, dict)
    print(f"{state.get('project')} — stage: {state.get('stage')}")
    print(f"format={state.get('format')} runtime={state.get('runtime_s')}s "
          f"aspect={state.get('aspect')} tier={state.get('tier')}")
    print("\nstages:")
    for s in STAGES:
        print(f"  {s:14} {state.get('stages', {}).get(s, 'pending')}")
    print("\napprovals:")
    for k, v in state.get("approvals", {}).items():
        print(f"  {k:14} {v or '—'}")
    shots = (load_json(project / "03_plan/shots.json") or {}).get("shots", [])
    if shots:
        approved = sum(
            1 for s in shots
            if (project / "04_gen/shots" / s["id"] / "approved.mp4").is_file()
        )
        print(f"\nshots: {len(shots)} planned, {approved} approved")
    budget = state.get("budget", {})
    print(f"budget: cap ${budget.get('cap_usd', 0)} "
          f"spent ${budget.get('spent_usd', 0)} "
          f"gpu {budget.get('gpu_minutes', 0)} min")


def cmd_validate(args) -> None:
    project = project_path(args.project)
    state = load_json(project / "state.json") or {}
    stage = args.stage or state.get("stage", "development")
    if stage not in STAGES:
        fail(f"unknown stage: {stage}")

    problems = []
    for rel in STAGE_ARTIFACTS.get(stage, []):
        if not (project / rel).is_file():
            problems.append(f"missing {rel}")

    shots_file = project / "03_plan/shots.json"
    if stage in {"preproduction", "prepare", "generation", "assemble"}:
        data = load_json(shots_file)
        if not data:
            problems.append("missing 03_plan/shots.json")
        else:
            shots = data.get("shots", [])
            if not shots:
                problems.append("shots.json has no shots")
            for i, shot in enumerate(shots):
                missing = [f for f in REQUIRED_SHOT_FIELDS if not shot.get(f)]
                if missing:
                    problems.append(f"shot #{i} {shot.get('id', '?')} missing: {', '.join(missing)}")
                if stage in {"generation", "assemble"}:
                    sid = shot.get("id")
                    if sid and not (project / "04_gen/shots" / sid / "approved.mp4").is_file():
                        problems.append(f"{sid}: no approved.mp4")
            if stage == "prepare":
                prompt_dirs = list((project / "04_gen/prompts").glob("*/*.txt"))
                if not prompt_dirs:
                    problems.append("04_gen/prompts has no compiled prompts")

    if problems:
        print(f"FAIL {stage} ({project})")
        for p in problems:
            print(f"  - {p}")
        raise SystemExit(1)
    print(f"PASS {stage} ({project})")


def probe_url(url: str, timeout: float = 2.0):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return True, r.status
    except (urllib.error.URLError, TimeoutError, OSError):
        return False, None


def cmd_doctor(_args) -> None:
    home = Path.home()
    print("filmctl doctor")

    for binary in ("ffmpeg", "ffprobe", "whisper"):
        path = shutil.which(binary)
        print(f"  {binary:10} {'ok ' + path if path else 'MISSING'}")

    ok, _ = probe_url("http://127.0.0.1:8188/system_stats")
    print(f"  comfyui    {'ok :8188' if ok else 'not running :8188'}")
    ok, _ = probe_url("http://localhost:11434/api/tags")
    print(f"  ollama     {'ok :11434' if ok else 'not running :11434'}")
    ok, _ = probe_url("http://127.0.0.1:8000/v1/models")
    print(f"  omlx       {'ok :8000' if ok else 'not running :8000'}")

    rapid = shutil.which("rapid-mlx")
    if rapid:
        proc = subprocess.run([rapid, "--version"], capture_output=True, text=True)
        print(f"  rapid-mlx  ok {proc.stdout.strip() or proc.stderr.strip()}")
    else:
        print("  rapid-mlx  MISSING")

    ltx = home / "src/ComfyUI/models/checkpoints/ltxv"
    print(f"  ltx models {'ok' if ltx.is_dir() and any(ltx.iterdir()) else 'not found'}")
    minimax = home / "src/ComfyUI/models/diffusion_models"
    has_minimax = minimax.is_dir() and any(minimax.glob("MiniMax-H3-*.gguf"))
    print(f"  minimax h3 {'ok' if has_minimax else 'not found'}")
    mlx = home / ".mlx-serve/models/dgrauet/ltx-2.3-mlx-q4"
    print(f"  ltx-2.3 mlx {'ok' if mlx.is_dir() else 'not found'}")

    usage = shutil.disk_usage(str(home))
    free_gb = usage.free / (1024 ** 3)
    print(f"  disk free  {free_gb:.1f} GB")

    keys = [
        "FAL_KEY",
        "MINIMAX_API_KEY",
        "KLING_API_KEY",
        "GOOGLE_API_KEY",
        "ELEVENLABS_API_KEY",
        "OPENAI_API_KEY",
        "SUNO_API_KEY",
        "RUNWAY_API_KEY",
    ]
    dotenv = home / "Developer/openmontage/.env"
    present = {k for k in keys if os.environ.get(k)}
    if dotenv.is_file():
        for line in dotenv.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            if k in keys and v.strip():
                present.add(k)
    print(f"  cloud keys {', '.join(sorted(present)) if present else 'none set'}")

    if not shutil.which("ffmpeg"):
        fail("ffmpeg is required for assembly", 2)


# --------------------------------------------------------------------------
# Prompt compilation


def extract_block(path: Path, marker: str):
    """Return the line or short block that starts with marker, if any."""
    if not path.is_file():
        return None
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith(marker):
            block = [line.strip()]
            for nxt in lines[i + 1:]:
                if not nxt.strip():
                    break
                if nxt.lstrip().startswith(("#", "<!--", "**")):
                    break
                block.append(nxt.strip())
            return " ".join(block)
    return None


def compile_prompt(shot: dict, style_block: str, identities: list[str], dialect: str) -> str:
    s = shot
    ident = " ".join(identities)
    # Negatives are owned by the shot record; drop any trailing negative clause
    # copied in from the style lock so it is not appended twice.
    style = re.sub(r"\bNegative:.*$", "", style_block or "", flags=re.I).strip()
    neg = s.get("negative", "").strip()
    audio = s.get("audio", "").strip()

    if dialect == "veo":
        parts = [
            f"{s['subject']}. {s['action']}. {s['environment']}.",
            f"{s['shot_size']} shot, {s['lens_mm']}mm. Camera: {s['camera_move']}.",
            f"Light: {s['lighting']}.",
            style,
            ident,
            f"Audio: {audio}." if audio else "",
            f"Negative: {neg}." if neg else "",
        ]
    elif dialect == "omni":
        parts = [
            f"{s['subject']}. {s['action']}. {s['environment']}.",
            f"{s['shot_size']}, {s['lens_mm']}mm, camera {s['camera_move']}.",
            f"Light: {s['lighting']}.",
            style,
            ident,
            "Continuous shot, no scene cuts." if s.get("control") == "t2v" else "",
            f"Audio: {audio}." if audio else "",
            f"Avoid: {neg}." if neg else "",
        ]
    elif dialect == "kling_t2v":
        parts = [
            f"{s['subject']} {s['action']} {s['environment']}.",
            f"{s['shot_size']}, {s['lens_mm']}mm, camera {s['camera_move']}, {s['lighting']}.",
            style,
            ident,
            f"Audio: {audio}." if audio else "",
            f"Negative: {neg}." if neg else "",
        ]
    elif dialect == "kling_i2v":
        # Kling I2V wants 15-40 words of motion only; the image owns identity,
        # style and light, so do not append the style and identity blocks.
        parts = [
            f"From the approved frame: {s['action']}.",
            f"Camera: {s['camera_move']}, {s['lens_mm']}mm.",
            "Do not change face, wardrobe, or light direction.",
            f"Avoid: {neg}." if neg else "",
        ]
    elif dialect == "runway":
        parts = [
            f"{s['camera_move']} shot of {s['subject']}, {s['action']}, in {s['environment']}.",
            f"{s['shot_size']}, {s['lens_mm']}mm. {s['lighting']}.",
            style,
            ident,
            f"Audio: {audio}." if audio else "",
            "No negative field on this model: restate the constraint positively in the prompt."
            if neg else "",
        ]
    elif dialect == "wan":
        parts = [
            f"Reference roles: {', '.join(f'[Image {i+1}] {r}' for i, r in enumerate(s.get('refs', [])))}."
            if s.get("refs") else "",
            f"{s['subject']}. {s['action']}. {s['environment']}.",
            f"{s['shot_size']}, {s['lens_mm']}mm, camera {s['camera_move']}, {s['lighting']}.",
            style,
            ident,
            f"Audio: {audio}." if audio else "",
            f"Negative: {neg}." if neg else "",
        ]
    elif dialect == "seedance":
        beats = [b.strip() for b in s["action"].replace(";", ",").split(",") if b.strip()]
        beat_line = ""
        if len(beats) >= 2:
            labels = ["First", "then", "finally"]
            beat_line = " ".join(
                f"{labels[min(i, 2)]}, {b}." for i, b in enumerate(beats[:3])
            )
        parts = [
            f"{s['subject']}. {beat_line or s['action'] + '.'}",
            f"{s['shot_size']}, {s['lens_mm']}mm, camera {s['camera_move']}.",
            f"{s['environment']}. Light: {s['lighting']}.",
            style,
            ident,
            f"Audio: {audio}." if audio else "",
            f"Negative: {neg}." if neg else "",
        ]
    elif dialect == "ltx":
        parts = [
            f"{s['subject']}, {s['action']}, {s['environment']}.",
            f"{s['shot_size']}, {s['lens_mm']}mm, {s['camera_move']}, {s['lighting']}.",
            style,
            ident,
            f"Negative: {neg}." if neg else "",
        ]
    elif dialect == "minimax":
        parts = [
            f"{s['shot_size']}, {s['lens_mm']}mm. Subject: {s['subject']}.",
            f"Action: {s['action']}. Location: {s['environment']}.",
            f"Camera: {s['camera_move']}. Light: {s['lighting']}.",
            style,
            ident,
            f"Audio: {audio}." if audio else "",
            f"Negative: {neg}." if neg else "",
        ]
    else:
        fail(f"unknown dialect: {dialect}")

    return " ".join(p for p in parts if p).strip() + "\n"


def cmd_prompts(args) -> None:
    project = project_path(args.project)
    data = load_json(project / "03_plan/shots.json")
    if not data:
        fail("03_plan/shots.json missing")
    shots = data.get("shots", [])
    if not shots:
        fail("shots.json has no shots")

    style_block = data.get("style_block", "").strip()
    if not style_block:
        style_block = extract_block(project / "02_design/style-lock.md", "STYLE —") or ""
    if not style_block:
        print("warning: no style_block in shots.json and no 'STYLE —' block in "
              "02_design/style-lock.md", file=sys.stderr)

    override = args.dialect
    count = 0
    outdirs = set()
    for shot in shots:
        missing = [f for f in REQUIRED_SHOT_FIELDS if not shot.get(f)]
        if missing:
            fail(f"{shot.get('id', '?')}: missing {', '.join(missing)}")
        dialect = override or shot.get("dialect") or data.get("dialect", "veo")
        outdir = project / "04_gen/prompts" / dialect
        outdir.mkdir(parents=True, exist_ok=True)
        outdirs.add(dialect)
        identities = []
        for tag in shot.get("characters", []):
            name = tag.lstrip("@")
            block = extract_block(
                project / "02_design/characters" / f"{name}.md", "IDENTITY LOCK"
            )
            if block:
                identities.append(block)
        prompt = compile_prompt(shot, style_block, identities, dialect)
        (outdir / f"{shot['id']}.txt").write_text(prompt, encoding="utf-8")
        meta = {
            "shot": shot["id"],
            "dialect": dialect,
            "model_params": shot.get("model_params", {}),
            "refs": shot.get("refs", []),
            "ref_order": data.get("ref_order", []),
            "seed": shot.get("seed"),
            "compiled_from": "03_plan/shots.json",
        }
        (outdir / f"{shot['id']}.json").write_text(
            json.dumps(meta, indent=2) + "\n", encoding="utf-8"
        )
        count += 1

    where = ", ".join(sorted(outdirs)) if outdirs else "none"
    print(f"compiled {count} prompts into 04_gen/prompts/ ({where})")


# --------------------------------------------------------------------------
# Assembly


def run(cmd: list[str]) -> None:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        fail("command failed:\n" + " ".join(cmd) + "\n" + proc.stderr[-2000:])


def cmd_assemble(args) -> None:
    project = project_path(args.project)
    data = load_json(project / "03_plan/shots.json")
    if not data:
        fail("03_plan/shots.json missing")
    shots = data.get("shots", [])
    if not shots:
        fail("shots.json has no shots")

    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        fail("ffmpeg not found", 2)

    norm = project / "04_gen/normalized"
    norm.mkdir(parents=True, exist_ok=True)
    ordered = []
    for shot in shots:
        sid = shot["id"]
        src = project / "04_gen/shots" / sid / "approved.mp4"
        if not src.is_file():
            fail(f"{sid}: approved.mp4 missing")
        dst = norm / f"{sid}.mp4"
        if not dst.is_file() or dst.stat().st_mtime < src.stat().st_mtime:
            vf = (
                f"scale={args.width}:{args.height}:force_original_aspect_ratio=decrease,"
                f"pad={args.width}:{args.height}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps={args.fps}"
            )
            run([
                ffmpeg, "-y", "-i", str(src),
                "-vf", vf,
                "-an",
                "-c:v", "libx264", "-crf", "18", "-preset", "fast",
                "-pix_fmt", "yuv420p",
                str(dst),
            ])
        ordered.append(dst)

    concat_list = project / "04_gen/normalized/concat.txt"
    concat_list.write_text(
        "".join(f"file '{p.as_posix()}'\n" for p in ordered), encoding="utf-8"
    )
    out = project / "05_post/rough-cut.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    run([
        ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-c", "copy", "-movflags", "+faststart", str(out),
    ])

    mix = project / "05_post/sound/mix.wav"
    if mix.is_file():
        muxed = project / "05_post/rough-cut_mix.mp4"
        run([
            ffmpeg, "-y", "-i", str(out), "-i", str(mix),
            "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
            "-shortest", "-movflags", "+faststart", str(muxed),
        ])
        print(f"wrote {muxed}")
    else:
        print(f"wrote {out} (silent; add 05_post/sound/mix.wav to mux)")


# --------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(prog="filmctl")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("new", help="scaffold a project")
    p.add_argument("slug")
    p.add_argument("--root", default=".")
    p.add_argument("--format", default="short",
                   choices=["short", "episode", "feature", "vertical", "trailer"])
    p.add_argument("--runtime", type=int, default=480)
    p.add_argument("--aspect", default="16:9")
    p.add_argument("--fps", type=int, default=24)
    p.add_argument("--tier", default="local", choices=["local", "standard", "premium"])
    p.set_defaults(func=cmd_new)

    p = sub.add_parser("status")
    p.add_argument("project")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("validate")
    p.add_argument("project")
    p.add_argument("--stage", choices=STAGES)
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("doctor")
    p.set_defaults(func=cmd_doctor)

    p = sub.add_parser("prompts")
    p.add_argument("project")
    p.add_argument("--dialect", default=None)
    p.set_defaults(func=cmd_prompts)

    p = sub.add_parser("assemble")
    p.add_argument("project")
    p.add_argument("--width", type=int, default=1280)
    p.add_argument("--height", type=int, default=720)
    p.add_argument("--fps", type=int, default=24)
    p.set_defaults(func=cmd_assemble)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
