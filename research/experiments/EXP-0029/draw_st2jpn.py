"""EXP-0029: draw ST2JPN.BIN records from the MOJI font, for local reading.

    ./invenv.sh python research/experiments/EXP-0029/draw_st2jpn.py OUT.png \
        INDEX [INDEX ...]

Each table entry (hex index) becomes a block of its text lines drawn from
MOJI.CHR (glyph = MOJI.TBL position, 16x16, 4 bpp), one line per record line,
with a thin bar between entries. Game text: the image stays local.
"""

from __future__ import annotations

import struct
import subprocess
import sys
from pathlib import Path

D = Path("local/extracted/saturn_us")
COLS = 30  # glyphs per drawn line


def main() -> int:
    out, idx = sys.argv[1], [int(x, 16) for x in sys.argv[2:]]
    st2 = (D / "ST2JPN.BIN").read_bytes()
    tbl = (D / "MOJI.TBL").read_bytes()
    chr_ = (D / "MOJI.CHR").read_bytes()
    glyph = {
        struct.unpack(">H", tbl[i * 4 : i * 4 + 2])[0]: i for i in range(len(tbl) // 4)
    }
    rows: list[list[int]] = []
    for i in idx:
        e = 0x0C + 4 * i
        o = e + struct.unpack(">I", st2[e : e + 4])[0]
        while True:
            o += 6
            line = []
            while True:
                w = struct.unpack(">H", st2[o : o + 2])[0]
                o += 2
                if w in (0xFFFF, 0):
                    break
                line.append(w)
            rows.append(line[:COLS])
            if w == 0:
                break
        rows.append([-1])  # separator
    W, H = COLS * 16, len(rows) * 18
    img = bytearray(W * H)
    for r, line in enumerate(rows):
        if line == [-1]:
            img[(r * 18 + 8) * W : (r * 18 + 9) * W] = b"\x60" * W
            continue
        for k, c in enumerate(line):
            g = glyph.get(c)
            if g is None or c == 0x20:
                continue
            gd = chr_[g * 128 : (g + 1) * 128]
            for y in range(16):
                for x in range(16):
                    b = gd[y * 8 + x // 2]
                    v = (b >> 4) if x % 2 == 0 else (b & 15)
                    img[(r * 18 + y) * W + k * 16 + x] = min(255, v * 40)
    pgm = Path(out).with_suffix(".pgm")
    pgm.write_bytes(b"P5 %d %d 255\n" % (W, H) + bytes(img))
    subprocess.run(
        ["ffmpeg", "-loglevel", "error", "-y", "-i", str(pgm), out], check=True
    )
    pgm.unlink()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
