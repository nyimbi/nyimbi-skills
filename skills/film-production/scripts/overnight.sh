#!/usr/bin/env bash
# overnight — run a film project to a rough-cut master while nobody watches.
#
# Wraps the whole run in caffeinate so a closed lid or idle timer never pauses
# the queue, then walks the stages that can run unattended: prompt validation,
# shot rendering (render_shots.sh, resumable), rough-cut assembly. Everything
# creative that can be decided in advance must already be decided — every gate
# self-checked and logged in state.json (overnight mode, film-production
# SKILL.md). What remains in the morning: creative take review (swap any
# approval), the cut, sound, finish, delivery.
#
# Usage: overnight.sh <project> [--variants N] [--width W] [--height H]
set -uo pipefail
PROJECT="${1:?usage: overnight.sh <project> [render options]}"; shift
HERE="$(cd "$(dirname "$0")" && pwd)"

free_gb=$(df -g "$PROJECT" | awk 'NR==2 {print $4}')
echo "overnight: $free_gb GB free at $(date +%T)"
[[ "$free_gb" -lt 40 ]] && echo "overnight: WARNING — under 40 GB free; a 75-shot" \
  "vertical at 704x512 needs ~15-25 GB of takes plus masters" >&2

# Validate the queue before burning the night on a broken plan.
python3 "$HERE/filmctl.py" validate "$PROJECT" --stage prepare \
  || { echo "overnight: stage validation failed — fix and re-run" >&2; exit 1; }

caffeinate -dims bash -c '
  python3 "'"$HERE"'/filmctl.py" prompts "'"$PROJECT"'" --dialect ltx
  bash "'"$HERE"'/render_shots.sh" "'"$PROJECT"'" "$@"
  python3 "'"$HERE"'/filmctl.py" assemble "'"$PROJECT"'"
' _ "$@"

python3 "$HERE/filmctl.py" status "$PROJECT"
cat <<EOF

Morning report
--------------
- approved takes:  $(find "$PROJECT/04_gen/shots" -name approved.mp4 | wc -l | tr -d ' ')
- auto-failed:     see $PROJECT/04_gen/continuity-failures.md (redesign these first)
- rough cut:       $PROJECT/05_post/rough-cut.mp4 (if assemble completed)
- log:             $PROJECT/04_gen/render-log.csv
Next: creative review of approvals, then film-postproduction.
EOF
