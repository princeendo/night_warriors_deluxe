#!/usr/bin/env bash
# EXP-0019: tile every Kth screenshot of a run (default 7) into OUT.png.
#   research/experiments/EXP-0019/sheet.sh RUN_DIR OUT.png [K]
set -euo pipefail
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
i=0
for f in $(ls "$1/shots" | awk -v k="${3:-7}" '(NR-1)%k==0'); do
  cp "$1/shots/$f" "$tmp/$(printf %03d $i).png"; i=$((i+1))
done
ffmpeg -loglevel error -y -i "$tmp/%03d.png" -vf "scale=200:-1,tile=10x6" -frames:v 1 "$2"
