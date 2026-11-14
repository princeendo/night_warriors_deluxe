"""EXP-0014: summarize every reader of a byte's address in a program file.

    ./invenv.sh python research/experiments/EXP-0014/readers.py FILE BASE VALUE \
        [-n 16]

For each ``mov.l @(disp,PC),Rn`` loading VALUE (see ``EXP-0013/xref.py``),
prints the next N instructions on one line, so the test and the call it
guards can be compared across readers. Static only.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path[:0] = [
    str(Path.cwd()),
    str(Path(__file__).resolve().parent.parent / "EXP-0013"),
]
from xref import loads_of  # noqa: E402

from tools.sh2.disasm import decode  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("file", type=Path)
    p.add_argument("base", type=lambda v: int(v, 16))
    p.add_argument("value", type=lambda v: int(v, 16))
    p.add_argument("-n", type=int, default=16)
    a = p.parse_args()
    code = a.file.read_bytes()
    for pc in loads_of(code, a.base, a.value):
        end = min(pc + 2 * a.n, a.base + len(code) - 2)
        ops = [decode(code, a.base, q)[1] for q in range(pc + 2, end, 2)]
        print(f"{pc:08X}: " + " ; ".join(" ".join(o.split()) for o in ops))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
