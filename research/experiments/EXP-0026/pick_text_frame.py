"""EXP-0026: pick the screenshot of a run that shows the most epilogue text.

    ./invenv.sh python research/experiments/EXP-0026/pick_text_frame.py RUN_DIR [...]

Counts, in each 8-bit RGB PNG under RUN_DIR/shots, the pixels of the Latin
font's light blue-green (R < 110, G > 150, B > 150; the win-quote font) in
the top 230 rows, and prints the best frame, its count and its SHA-256 per
run, among every third shot of the run's last 60 % (the epilogue's part).
Standard library only (zlib PNG decoding, filters 0-4).
"""

from __future__ import annotations

import hashlib
import struct
import sys
import zlib
from pathlib import Path


def decode_png(data: bytes) -> tuple[int, int, bytes]:
    pos, idat, width = 8, b"", 0
    height = 0
    while pos < len(data):
        n, kind = struct.unpack(">I4s", data[pos : pos + 8])
        body = data[pos + 8 : pos + 8 + n]
        if kind == b"IHDR":
            width, height, depth, color = struct.unpack(">IIBB", body[:10])
            if (depth, color) != (8, 2):
                raise ValueError("only 8-bit RGB")
        elif kind == b"IDAT":
            idat += body
        pos += 12 + n
    raw, stride, out, prev = zlib.decompress(idat), width * 3, bytearray(), None
    for y in range(height):
        f, line = (
            raw[y * (stride + 1)],
            bytearray(raw[y * (stride + 1) + 1 : (y + 1) * (stride + 1)]),
        )
        prev = prev or bytearray(stride)
        for i in range(stride):
            a = line[i - 3] if i >= 3 else 0
            b, c = prev[i], prev[i - 3] if i >= 3 else 0
            if f == 1:
                line[i] = (line[i] + a) & 255
            elif f == 2:
                line[i] = (line[i] + b) & 255
            elif f == 3:
                line[i] = (line[i] + (a + b) // 2) & 255
            elif f == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                line[i] = (
                    line[i] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)
                ) & 255
        out += line
        prev = line
    return width, height, bytes(out)


def text_pixels(path: Path) -> int:
    w, h, px = decode_png(path.read_bytes())
    n = 0
    for i in range(0, min(h, 230) * w * 3, 3):
        r, g, b = px[i], px[i + 1], px[i + 2]
        n += r < 110 and g > 150 and b > 150
    return n


def main() -> int:
    for run in map(Path, sys.argv[1:]):
        shots = sorted((run / "shots").glob("*.png"))
        late = shots[int(len(shots) * 0.4) :: 3]  # past the main ending; every 3rd
        best = max(late, key=text_pixels)
        digest = hashlib.sha256(best.read_bytes()).hexdigest()[:8]
        print(f"{run} {best.name} {text_pixels(best)} {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
