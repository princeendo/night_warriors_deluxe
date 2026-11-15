"""EXP-0022: does the epilogue renderer draw ST1USA's Latin codes in English mode?

    ./invenv.sh python research/experiments/EXP-0022/build_en_test.py [OUT_DIR]

Applies the DISC-002 version 2 patches (EXP-0018 ``PATCHES``) and, in
``ST1JPN.BIN``, replaces the character codes of the first three lines of
Morrigan's epilogue record in place (same length, line headers untouched)
with PSP *Chronicle* English, encoded as ``ST1USA.BIN`` encodes its win
quotes: capitals and most punctuation = ASCII + 0x80, but comma = 0x00AE and
period = 0x00AC (swapped; found in the first run), a-z = 0x0201-0x021A,
space = 0x0020; each line padded with spaces. OUT_DIR defaults to
``build/us_en_test``.
"""

from __future__ import annotations

import importlib.util
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
_spec = importlib.util.spec_from_file_location(
    "build_epilogue", "research/experiments/EXP-0018/build_epilogue.py"
)
be = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(be)

ST1JPN = Path("local/extracted/saturn_us/ST1JPN.BIN")
FIRST_LINE = 0xE1A  # Morrigan's first line header (x, y, 1), EXP-0011/EXP-0022
# Three re-wrapped lines of PSP Chronicle Hmovie04_2 (EXP-0020), one per line,
# kept out of git (game text, AGENTS.md rule 21).
LINES_FILE = Path("local/end002/exp0022_lines.txt")


SWAPPED = {",": 0x00AE, ".": 0x00AC}  # not ASCII + 0x80 (EXP-0022, ST1USA.BIN)


def encode(text: str) -> list[int]:
    out = []
    for c in text:
        if c == " ":
            out.append(0x0020)
        elif c in SWAPPED:
            out.append(SWAPPED[c])
        elif "a" <= c <= "z":
            out.append(0x0201 + ord(c) - ord("a"))
        else:
            out.append(ord(c) + 0x80)
    return out


def line_spans(data: bytes, start: int, count: int) -> list[tuple[int, int]]:
    """(offset of first code, number of codes) for ``count`` lines from ``start``."""
    spans, pos = [], start
    for _ in range(count):
        first = pos + 6  # skip x, y, 0001
        end = first
        while struct.unpack(">H", data[end : end + 2])[0] not in (0xFFFF, 0x0000):
            end += 2
        spans.append((first, (end - first) // 2))
        pos = end + 2
    return spans


def patches() -> list[tuple]:
    data = ST1JPN.read_bytes()
    lines = LINES_FILE.read_text().splitlines()
    out = []
    spans = line_spans(data, FIRST_LINE, len(lines))
    for (off, n), text in zip(spans, lines, strict=True):
        codes = encode(text)
        if len(codes) > n:
            raise ValueError(f"{text!r}: {len(codes)} codes > {n}")
        codes += [0x0020] * (n - len(codes))
        old = data[off : off + 2 * n].hex().upper()
        new = struct.pack(f">{n}H", *codes).hex().upper()
        out.append(("ST1JPN.BIN", off, old, new, None, f"Morrigan line -> {text!r}"))
    return out


def main() -> int:
    be.PATCHES = be.PATCHES + patches()
    sys.argv = [sys.argv[0], sys.argv[1] if len(sys.argv) > 1 else "build/us_en_test"]
    return be.main()


if __name__ == "__main__":
    assert encode("Ma'a, I.") == [0xCD, 0x201, 0xA7, 0x201, 0xAE, 0x20, 0xC9, 0xAC]
    raise SystemExit(main())
