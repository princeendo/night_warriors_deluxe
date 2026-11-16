"""EXP-0029: decode ST2USA.BIN's records (both kinds) to text, for local reading.

    ./invenv.sh python research/experiments/EXP-0029/st2_text.py [OUT.txt]

Line records (x, y, 0001, codes, FFFF / 0000) use the win-quote Latin codes
(D-021); records whose fourth word is in 0x0140-0x015F hold ASCII after it,
ended by a zero byte. Writes "index offset text" per table entry to OUT
(default local/end003/st2usa.txt): game text, never committed.
"""

from __future__ import annotations

import struct
import sys
from pathlib import Path

ST2USA = Path("local/extracted/saturn_us/ST2USA.BIN")


def code(w: int) -> str:
    if w == 0x20:
        return " "
    if 0x201 <= w <= 0x21A:
        return chr(w - 0x201 + 97)
    if w == 0xAE:
        return ","
    if w == 0xAC:
        return "."
    if 0xA0 < w < 0xE0:
        return chr(w - 0x80)
    return f"{{{w:x}}}"


def record(d: bytes, o: int) -> str:
    first = struct.unpack(">H", d[o + 6 : o + 8])[0]
    if 0x140 <= first < 0x160:  # ASCII kind: byte-level lines, record ends 00 00
        end = d.find(b"\0\0", o + 7) % (len(d) + 1)  # last record: file end
        runs = [r for r in d[o + 7 : end].split(b"\0") if r]
        text = " | ".join(bytes(c for c in r if 32 <= c < 127).decode() for r in runs)
        return "[A] " + text
    lines = []
    while o + 6 <= len(d):
        o += 6
        line = []
        while o + 2 <= len(d):
            w = struct.unpack(">H", d[o : o + 2])[0]
            o += 2
            if w in (0xFFFF, 0):
                break
            line.append(code(w))
        lines.append("".join(line))
        if w == 0:
            break
    return " / ".join(lines)


def main() -> int:
    d = ST2USA.read_bytes()
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "local/end003/st2usa.txt")
    rows, i, end = [], 0, len(d)
    while 0x0C + 4 * i < end:
        e = 0x0C + 4 * i
        v = struct.unpack(">I", d[e : e + 4])[0]
        if v and e + v >= len(d):
            rows.append(f"{i:03x} beyond the file ({e + v:#x})")
        elif v:
            end = min(end, e + v)
            rows.append(f"{i:03x} {e + v:05x} {record(d, e + v)}")
        else:
            rows.append(f"{i:03x} null")
        i += 1
    out.write_text("\n".join(rows) + "\n")
    print(out, len(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
