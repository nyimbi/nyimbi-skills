#!/usr/bin/env bash
# render_shots — resumable overnight batch renderer for the local LTX stack.
#
# For every shot in <project>/04_gen/shots/ that has a compiled LTX prompt and
# no approved.mp4, generate VARIANTS takes with ltx-2-mlx (I2V when the shot
# directory holds keyframe.png, T2V otherwise). The first take that passes the
# mechanical checks — right duration, right resolution, non-frozen frames, an
# audio stream when the pack is joint audio-video — is copied to approved.mp4.
# Creative judgement (identity, palette, performance) is a morning task; this
# loop's job is to never block the queue on one shot.
#
# Usage: render_shots.sh <project> [--variants N] [--width W] [--height H]
#                          [--frames N] [--frame-rate N] [--model REPO] [--dry-run]
#
# Env:   LTX=path to the ltx-2-mlx checkout (default ~/src/ltx-2-mlx)
set -uo pipefail

PROJECT="${1:?usage: render_shots.sh <project> [options]}"; shift
VARIANTS=3; WIDTH=704; HEIGHT=512; FRAMES=121; RATE=24
MODEL="${LTX_MODEL:-dgrauet/ltx-2.3-mlx-q4}"
LTX="${LTX:-$HOME/src/ltx-2-mlx}"
DRY=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --variants) VARIANTS="$2"; shift 2;;
    --width) WIDTH="$2"; shift 2;;
    --height) HEIGHT="$2"; shift 2;;
    --frames) FRAMES="$2"; shift 2;;
    --frame-rate) RATE="$2"; shift 2;;
    --model) MODEL="$2"; shift 2;;
    --dry-run) DRY=1; shift;;
    *) echo "unknown option: $1" >&2; exit 2;;
  esac
done

SHOTS="$PROJECT/04_gen/shots"
PROMPTS="$PROJECT/04_gen/prompts/ltx"
LOG="$PROJECT/04_gen/render-log.csv"
FAIL="$PROJECT/04_gen/continuity-failures.md"
mkdir -p "$SHOTS"
touch "$LOG"; touch "$FAIL"

[[ -d "$LTX" ]] || { echo "ltx-2-mlx not found at $LTX (set \$LTX)" >&2; exit 1; }

# --- mechanical checks -------------------------------------------------------
# A take is mechanically valid when ffprobe says: stream 0 is the expected
# size, duration within half a second of the request, more than one distinct
# frame (guards against frozen output), and — for joint audio packs — an
# audio stream. Creative validity is human.
mech_ok() {
  local f="$1" want_d="$2"
  local info
  info=$(ffprobe -v error -show_entries format=duration \
           -show_entries stream=codec_type,width,height \
           -of json "$f" 2>/dev/null) || return 1
  python3 - "$info" "$want_d" <<'PY'
import json, sys
info, want_d = json.loads(sys.argv[1]), float(sys.argv[2])
dur = float(info.get("format", {}).get("duration", 0))
types = [s["codec_type"] for s in info.get("streams", [])]
vs = [s for s in info["streams"] if s["codec_type"] == "video"]
ok = abs(dur - want_d) < 0.75 and "video" in types
if any(s.get("height", 0) < 100 for s in vs):
    ok = False
if "audio" not in types:
    ok = False  # joint audio-video pack: a silent take is a failed take
sys.exit(0 if ok else 1)
PY
}

frame_count() {  # >1 distinct frame, cheaply: decode 5 frames, compare bytes
  ffmpeg -v error -i "$1" -vf "select='not(mod(n\,25))'" -frames:v 5 -f md5 - 2>/dev/null \
    | awk -F= 'NF' | sort -u | wc -l | tr -d ' '
}

render_one() {
  local sid="$1" pfile="$2" dir="$SHOTS/$sid"
  local prompt key=() take n verdict reason
  prompt=$(cat "$pfile")
  [[ -f "$dir/keyframe.png" ]] && key=(--image "$dir/keyframe.png")
  local want_s
  want_s=$(python3 -c "print(round($FRAMES/$RATE, 3))")

  for n in $(seq 1 "$VARIANTS"); do
    take="$dir/take_$n.mp4"
    [[ -s "$take" ]] || {
      echo "[$sid] take $n rendering (${#key[@]:+I2V}${key[@]:-T2V} ${WIDTH}x${HEIGHT} ${FRAMES}f)..."
      [[ -n "$DRY" ]] && continue
      # AGX_RELAX_CDM_CTXSTORE_TIMEOUT=1 relaxes the macOS GPU watchdog for this
      # process (MLX 0.31 + macOS 26.x kills sustained GPU work otherwise).
      # The 100%-reliable variant is a closed lid — which is where this script
      # runs. See ltx-2-mlx docs/PIPELINES.md.
      (cd "$LTX" && AGX_RELAX_CDM_CTXSTORE_TIMEOUT=1 uv run ltx-2-mlx generate \
        --distilled --model "$MODEL" \
        --prompt "$prompt" "${key[@]}" \
        -W "$WIDTH" -H "$HEIGHT" --frames "$FRAMES" --frame-rate "$RATE" \
        --seed $((RANDOM % 100000)) -o "$take") >>"$dir/prompt.log" 2>&1 \
        || { echo "[$sid] take $n: generation error (see prompt.log)"; \
             echo "$sid,take_$n,ltx-2-mlx,-,-,error" >> "$LOG"; continue; }
    }
    if mech_ok "$take" "$want_s" && [[ "$(frame_count "$take")" -gt 1 ]]; then
      cp "$take" "$dir/approved.mp4"
      echo "$sid,take_$n,ltx-2-mlx,$MODEL,$WIDTH x $HEIGHT,approved-mechanical" >> "$LOG"
      return 0
    fi
    echo "$sid,take_$n,ltx-2-mlx,-,-,mech-fail" >> "$LOG"
  done
  # Three-strike, autonomously: log the failure, approve nothing, move on.
  # The morning review redesigns the shot (cutaway, insert, silhouette) —
  # a blocked queue wastes the whole night on one stubborn shot.
  {
    echo "## $sid — overnight auto-fail $(date +%F_%T)"
    echo "- $VARIANTS takes failed mechanical checks or generation"
    echo "- action: morning redesign per three-strike rule (film-production SKILL.md)"
  } >> "$FAIL"
  echo "$sid,-,ltx-2-mlx,$MODEL,-,auto-failed-$VARIANTS" >> "$LOG"
  return 1
}

done_n=0; fail_n=0; skip_n=0
for pfile in "$PROMPTS"/*.txt; do
  [[ -e "$pfile" ]] || { echo "no compiled prompts in $PROMPTS — run: filmctl.py prompts $PROJECT --dialect ltx" >&2; exit 1; }
  sid=$(basename "$pfile" .txt)
  mkdir -p "$SHOTS/$sid"
  if [[ -s "$SHOTS/$sid/approved.mp4" && -z "$DRY" ]]; then skip_n=$((skip_n+1)); continue; fi
  if render_one "$sid" "$pfile"; then done_n=$((done_n+1)); else fail_n=$((fail_n+1)); fi
done

echo "rendered: $done_n approved, $fail_n auto-failed, $skip_n already approved"
