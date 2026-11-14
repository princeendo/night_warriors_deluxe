"""EXP-0013: list the code that loads a 32-bit literal, with context.

    ./invenv.sh python research/experiments/EXP-0013/xref.py FILE BASE VALUE \
        [--before N] [--after N]

FILE is a program file loaded at BASE (hex). For every ``mov.l @(disp,PC),Rn``
whose literal equals VALUE (hex), prints the instructions around it with
``tools.sh2.disasm``. Static only; a literal reached another way is missed.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
from tools.sh2.disasm import decode


def loads_of(code: bytes, base: int, value: int) -> list[int]:
    hits = []
    for off in range(0, len(code) - 1, 2):
        op = int.from_bytes(code[off : off + 2], "big")
        if op & 0xF000 != 0xD000:  # mov.l @(disp,PC),Rn
            continue
        target = ((base + off) & ~3) + 4 + 4 * (op & 0xFF) - base
        if (
            target + 4 <= len(code)
            and int.from_bytes(code[target : target + 4], "big") == value
        ):
            hits.append(base + off)
    return hits


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("file", type=Path)
    p.add_argument("base", type=lambda v: int(v, 16))
    p.add_argument("value", type=lambda v: int(v, 16))
    p.add_argument("--before", type=int, default=4)
    p.add_argument("--after", type=int, default=8)
    a = p.parse_args()
    code = a.file.read_bytes()
    for pc in loads_of(code, a.base, a.value):
        print(f"-- load at {pc:08X}")
        for q in range(pc - 2 * a.before, pc + 2 * a.after + 2, 2):
            if a.base <= q < a.base + len(code) - 1:
                op, text = decode(code, a.base, q)
                print(f"{'>' if q == pc else ' '}{q:08X}: {op:04X}  {text}")
    return 0


if __name__ == "__main__":
    # Synthetic check: mov.l @(1,PC),r1 at 0x1000 loads the long at 0x1008.
    assert loads_of(
        bytes.fromhex("D101 0009 0009 0009 12345678".replace(" ", "")),
        0x1000,
        0x12345678,
    ) == [0x1000]
    raise SystemExit(main())
