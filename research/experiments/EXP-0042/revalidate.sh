#!/usr/bin/env bash
# Re-run the agent interface validations V1-V4 (EXP-0005) on the agent build
# with patch 0002 (cache-coherent writes), on both releases.
set -euo pipefail
OUT=local/exp0042/revalidate
mkdir -p "$OUT"
cue() {
  case $1 in
  jp) echo "local/disc_images/vh_saturn_jp_1m/Vampire Hunter - Darkstalkers' Revenge (Japan) (1M).cue" ;;
  us) echo "local/disc_images/nw_saturn_us/Night Warriors - Darkstalkers' Revenge (USA).cue" ;;
  esac
}
for r in jp us; do
  env -u MEDNAFEN_AGENT_DIR ./invenv.sh python -m tools.mednafen.cold_boot "$(cue $r)" \
    "$OUT/$r-v1-equiv" --seconds 120 --mednafen vendor/mednafen/build-agent/src/mednafen \
    > "$OUT/$r-v1-equiv.stdout" 2>&1
  ./invenv.sh python research/experiments/EXP-0005/validate.py $r "$OUT/$r-run1" \
    > "$OUT/$r-run1.stdout" 2>&1
  ./invenv.sh python -m tools.memory.mcs_extract "$OUT/$r-run1/v2.mc0" \
    --region wram_l --region wram_h --region vdp1_vram --region vdp2_vram \
    --out-dir "$OUT/$r-run1-v2" > "$OUT/$r-extract.txt" 2>&1
  for m in wram_l wram_h vdp1_vram vdp2_vram; do
    cmp "$OUT/$r-run1/$m.bin" "$OUT/$r-run1-v2/$m.bin" && echo "$r V2 $m equal"
  done
  n=0; same=0
  for f in "$OUT/$r-v1-equiv"/frames/*.png; do
    n=$((n + 1))
    cmp -s "$f" "local/emu021/$r-v1-equiv/frames/$(basename "$f")" && same=$((same + 1))
  done
  echo "$r V1 $same of $n frames equal local/emu021/$r-v1-equiv"
done
