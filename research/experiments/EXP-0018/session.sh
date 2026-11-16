#!/usr/bin/env bash
# EXP-0018: one recorded play session on the patched US image (cold boot).
# Run from the repository root after build_epilogue.py: session.sh [OUT_DIR] [CUE]
# (CUE defaults to the version 2 image; EXP-0026 passes its own). The user plays
# Morrigan and wins one match; this records a state every second (all kept)
# and a screenshot every half second, as EXP-0007 did, in the interactive
# home. The session ends when the user closes the Mednafen window.
set -euo pipefail

ROOT="$PWD"
d="${1:-local/disc002/us-enhanced-session}"  # output folder; one per session
V2="build/us_enhanced_epilogue/Night Warriors - Darkstalkers' Revenge (USA).cue"
CUE="${2:-$V2}"
BIN="vendor/mednafen/build-agent/src/mednafen"
mkdir -p "$d"
date "+%H:%M:%S start"
MEDNAFEN_HOME="$ROOT/local/mednafen" MEDNAFEN_AGENT_DIR="$ROOT/$d/agent" \
  "$BIN" "$CUE" > "$d/mednafen.log" 2>&1 &
pid=$!
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
date "+%H:%M:%S end"
