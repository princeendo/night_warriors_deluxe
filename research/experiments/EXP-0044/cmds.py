"""AUD-004: rebuild sound-driver commands from vsmove.py ``--watch-sound`` logs.

The game's writer at ``0x06039586`` stores one 16-byte command at
``0x25A00700 + 16 * slot``: word 1 (R0 at ``0x060395BC``), word 2
(``0x060395C2``), words 3-7 (``0x060395C6``-``0x060395D6``), then word 0 =
command byte << 8 (R5 at ``0x060395D8``). Prints one line per command:
frame, the caller (PR), and the eight words.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ORDER = [0x060395BC, 0x060395C2, 0x060395C6, 0x060395CA, 0x060395CE]
ORDER += [0x060395D2, 0x060395D6]
FIELD = re.compile(r" (PC|R0|R5|PR)=([0-9A-F]{8})")


def commands(path: Path) -> list[tuple[int, str, list[int]]]:
    out, words = [], []
    for line in path.read_text().splitlines():
        if not line.startswith("hit "):
            continue
        frame = int(line.split()[2].split("=")[1])
        regs = dict(FIELD.findall(line))
        pc = int(regs["PC"], 16)
        if pc in ORDER:
            words.append(int(regs["R0"], 16) & 0xFFFF)
        elif pc == 0x060395D8:
            out.append((frame, regs["PR"], [int(regs["R5"], 16) & 0xFFFF, *words]))
            words = []
    return out


if __name__ == "__main__":
    for frame, caller, words in commands(Path(sys.argv[1])):
        print(frame, caller, " ".join(f"{w:04X}" for w in words))
