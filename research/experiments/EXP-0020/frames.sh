#!/usr/bin/env bash
# EXP-0020: extract frame 300 of each PSP Vampire Hunter epilogue movie
# (movie/hunend/HmovieNN_2.pmf) into the ignored local/ref002/psp_epilogues/.
# Run from the repository root after extracting the ISO (README, step 1).
# A PMF file is a 2,048-byte PSMF header followed by an MPEG program stream.
set -euo pipefail
M=local/psp_extract/chronicle_us/PSP_GAME/USRDIR/movie/hunend
O=local/ref002/psp_epilogues
mkdir -p "$O"
for n in 01 02 03 04 05 06 07 08 09 10 11 12 13 14; do
  tail -c +2049 "$M/Hmovie${n}_2.pmf" | ffmpeg -loglevel error -f mpeg -i - \
    -vf "select='eq(n\,300)'" -frames:v 1 -y "$O/H${n}_2_f300.png"
done
shasum -a 256 "$O"/H*_2_f300.png
