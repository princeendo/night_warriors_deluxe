#!/usr/bin/env bash
# EXP-0009: one throw session per release, Japanese first, then US. The user
# plays; live.py logs the sound chip's active slots about 15 times a second
# and a screenshot every half second, through the patched Mednafen's agent
# interface (D-005), in the interactive home with sound recorded to WAV. Each
# session ends when the user closes the Mednafen window.
set -euo pipefail

ROOT="$PWD"
OUT="local/aud001/throws"
BIN="vendor/mednafen/build-agent/src/mednafen"
cue_for() {  # bash 3.2 (macOS) has no associative arrays
  case "$1" in
    jp) echo "local/disc_images/vh_saturn_jp_1m/Vampire Hunter - Darkstalkers' Revenge (Japan) (1M).cue" ;;
    us) echo "local/disc_images/nw_saturn_us/Night Warriors - Darkstalkers' Revenge (USA).cue" ;;
  esac
}

for r in jp us; do
  d="$OUT/$r"
  mkdir -p "$d"
  date "+%H:%M:%S start $r"
  MEDNAFEN_HOME="$ROOT/local/mednafen" MEDNAFEN_AGENT_DIR="$ROOT/$d/agent" \
    "$BIN" -soundrecord "$ROOT/$d/sound.wav" "$(cue_for "$r")" > "$d/mednafen.log" 2>&1 &
  pid=$!
  # Wait for the agent to answer before attaching the logger.
  ./invenv.sh python -c "
import sys, time
sys.path.insert(0, '.')
from pathlib import Path
from tools.mednafen.agent import Agent, AgentError
a = Agent(Path('$d/agent').resolve(), 5)
for _ in range(60):
    try:
        a.status(); break
    except AgentError:
        time.sleep(0.5)
"
  ./invenv.sh python research/experiments/EXP-0009/live.py "$d/agent" "$d/live" \
    > "$d/live.log" 2>&1 || true
  wait "$pid" || true
  date "+%H:%M:%S end $r"
done
./invenv.sh python -m tools.mednafen.home
