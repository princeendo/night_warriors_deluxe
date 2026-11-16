#!/usr/bin/env bash
# EXP-0029: force every character's ending in the Japanese release (1M image),
# as EXP-0019 forced the US ones: stage byte 0x0608097B = 9 (D-009) and the
# character byte 0x060809D0 = CHAR (the US 0x06080980 + 0x50, like the other
# Japanese addresses) at Morrigan's won-KO state. Run from the repository root:
#   research/experiments/EXP-0029/jp_endings.sh [CHAR ...]   (default 1-14)
set -euo pipefail
F=research/experiments/EXP-0010/force.py
S=local/aud001/jp-session/rec/states/f00023129.mcs
chars=("$@"); [ ${#chars[@]} -gt 0 ] || chars=(1 2 3 4 5 6 7 8 9 10 11 12 13 14)
for n in "${chars[@]}"; do
  x=$(printf %02X "$n"); t=$(printf %02d "$n")
  [ -d local/end003/jp-$t ] || ./invenv.sh python $F jp $S local/end003/jp-$t \
    --write 0608097B=09 --write 060809D0=$x --steps 420 > /dev/null 2>&1
  date "+%H:%M:%S $t done"
done
