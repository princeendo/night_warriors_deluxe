#!/usr/bin/env bash
# EXP-0007: one recorded play session per release, Japanese first, then US.
# Run from the repository root. The user plays; this records sound (WAV), a
# state every second (all kept) and a screenshot every half second, through
# the patched Mednafen's agent interface (D-005), in the interactive home.
# Each session ends when the user closes the Mednafen window.
set -euo pipefail

ROOT="$PWD"
OUT="local/aud001"
BIN="vendor/mednafen/build-agent/src/mednafen"
cue_for() {  # bash 3.2 (macOS) has no associative arrays
  case "$1" in
    jp) echo "local/disc_images/vh_saturn_jp_1m/Vampire Hunter - Darkstalkers' Revenge (Japan) (1M).cue" ;;
    us) echo "local/disc_images/nw_saturn_us/Night Warriors - Darkstalkers' Revenge (USA).cue" ;;
  esac
}

for r in jp us; do
  d="$OUT/$r-session"
  mkdir -p "$d"
  date "+%H:%M:%S start $r"
  MEDNAFEN_HOME="$ROOT/local/mednafen" MEDNAFEN_AGENT_DIR="$ROOT/$d/agent" \
    "$BIN" -soundrecord "$ROOT/$d/sound.wav" "$(cue_for "$r")" > "$d/mednafen.log" 2>&1 &
  pid=$!
  # Wait for the agent to answer before attaching the recorder.
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
  ./invenv.sh python -m tools.mednafen.session_recorder "$d/rec" --agent-dir "$d/agent" \
    --shot-interval 0.5 --state-interval 1 --keep-states 0 > "$d/recorder.log" 2>&1 || true
  wait "$pid" || true
  date "+%H:%M:%S end $r"
done
./invenv.sh python -m tools.mednafen.home
