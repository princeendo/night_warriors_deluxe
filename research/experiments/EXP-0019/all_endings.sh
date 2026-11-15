#!/usr/bin/env bash
# EXP-0019: force each character's ending on the DISC-002 version 2 image and,
# as control, on the unpatched US image. Run from the repository root:
#   research/experiments/EXP-0019/all_endings.sh [CHAR ...]   (default 1-14 but 5)
# The stage byte (0x0608092B = 9, D-009) and the ending-character byte
# (0x06080980 = CHAR, 1-based roster order) are written at a won-KO state.
set -euo pipefail
F=research/experiments/EXP-0010/force.py
C="build/us_enhanced_epilogue/Night Warriors - Darkstalkers' Revenge (USA).cue"
V2=local/disc002/us-enhanced-session-v2/rec/states/f00007741.mcs
US=local/aud001/us-session/rec/states/f00011016.mcs
chars=("$@"); [ ${#chars[@]} -gt 0 ] || chars=(1 2 3 4 6 7 8 9 10 11 12 13 14)
for n in "${chars[@]}"; do
  x=$(printf %02X "$n"); t=$(printf %02d "$n")
  [ -d local/disc002/end-v2-$t ] || ./invenv.sh python $F us $V2 local/disc002/end-v2-$t \
    --image "$C" --write 0608092B=09 --write 06080980=$x --steps 420 > /dev/null 2>&1
  [ -d local/disc002/end-us-$t ] || ./invenv.sh python $F us $US local/disc002/end-us-$t \
    --write 0608092B=09 --write 06080980=$x --steps 420 > /dev/null 2>&1
  date "+%H:%M:%S $t done"
done
