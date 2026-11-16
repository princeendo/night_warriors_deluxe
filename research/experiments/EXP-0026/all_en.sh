#!/usr/bin/env bash
# EXP-0026: force every character's ending on the all-14 English build.
#   research/experiments/EXP-0026/all_en.sh [CHAR ...]   (default 1-14)
# Run from the repository root after:
#   ./invenv.sh python research/experiments/EXP-0023/build_en_epilogue.py \
#     --late-array1 --step 0 --out build/us_en_epilogue_all 1 2 3 4 5 6 7 8 9 10 11 12 13 14
# The state comes from a boot of the version 2 image, so its RAM holds the
# old MAIN.BIN; the one MAIN.BIN literal is written in RAM too (EXP-0024).
set -euo pipefail
F=research/experiments/EXP-0010/force.py
C="build/us_en_epilogue_all/Night Warriors - Darkstalkers' Revenge (USA).cue"
S=local/disc002/us-enhanced-session-v2/rec/states/f00007741.mcs
chars=("$@"); [ ${#chars[@]} -gt 0 ] || chars=(1 2 3 4 5 6 7 8 9 10 11 12 13 14)
for n in "${chars[@]}"; do
  x=$(printf %02X "$n"); t=$(printf %02d "$n")
  [ -d local/end002/all-$t ] || ./invenv.sh python $F us $S local/end002/all-$t \
    --image "$C" --write 0608092B=09 --write 06080980=$x --write 06037A98=060833CC \
    --steps 330 > /dev/null 2>&1
  date "+%H:%M:%S $t done"
done
