"""EXP-0033: the EXP-0032 image plus Donovan's two region-flag sound guards opened.

    ./invenv.sh python research/experiments/EXP-0033/build_donovan.py [OUT_DIR]

``PL14.O`` (and ``PL14.O2``, same offsets) skips two sound calls through
0x0603A76E (codes 0x1B4 and 0x1B2) when the region flag is non-zero
(EXP-0014). Their ``bf`` become ``nop``; the flag stays 2. OUT_DIR defaults to
``build/us_en_donovan``. That PL14 is Donovan is a HYPOTHESIS (roster order,
as PL05 is Morrigan) until a fight confirms it (EXP-0033).
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
_spec = importlib.util.spec_from_file_location(
    "b32", "research/experiments/EXP-0032/build_voices.py"
)
b32 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(b32)
be = b32.be

GUARDS = [  # (file offset, original bf, P1 address, guarded call)
    (0x111C, "8B08", 0x0600211C, "codes 0x1B4 (via 0x0603A76E)"),
    (0x23C4, "8B03", 0x060033C4, "codes 0x1B2 (via 0x0603A76E)"),
]


def patches() -> list[tuple]:
    return [
        (
            f,
            off,
            old,
            "0009",
            addr if f == "PL14.O" else addr + 0x8000,
            f"Donovan guard: {what}",
        )
        for f in ("PL14.O", "PL14.O2")
        for off, old, addr, what in GUARDS
    ]


def main() -> int:
    b31 = b32.b31
    extra = b31.b23.patches(list(range(1, 15)), 0x10, 0, "late") + b31.patches()
    be.PATCHES = be.PATCHES + extra + b32.patches() + patches()
    sys.argv = [
        sys.argv[0],
        sys.argv[1] if len(sys.argv) > 1 else "build/us_en_donovan",
    ]
    return be.main()


if __name__ == "__main__":
    raise SystemExit(main())
