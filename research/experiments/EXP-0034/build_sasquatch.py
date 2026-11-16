"""EXP-0034: the EXP-0033 image plus Sasquatch's six region-flag guards opened.

    ./invenv.sh python research/experiments/EXP-0034/build_sasquatch.py [OUT_DIR]

``PL10.O`` (and ``PL10.O2``, same offsets) picks his win pose in one state
machine (0x060044FC). With the region flag non-zero it skips the effect
objects of poses 0, 1 and 4 (the small snow creatures and their sample
0x53116) and plays pose 5 instead of pose 1 (EXP-0034). Each guard's ``bf``
or ``bf/s`` becomes ``nop`` (a ``bf/s`` delay-slot instruction then simply
runs next, as it did anyway); the flag stays 2. OUT_DIR defaults to
``build/us_en_sasquatch``.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
_spec = importlib.util.spec_from_file_location(
    "b33", "research/experiments/EXP-0033/build_donovan.py"
)
b33 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(b33)
be = b33.be

GUARDS = [  # (file offset, original branch, P1 address, what it skips)
    (0x32D0, "8F1D", 0x060042D0, "pose 1: four 0x01003900 objects"),
    (0x3354, "8F2B", 0x06004354, "poses 0 and 4: two 0x01007300 objects"),
    (0x33C2, "8F27", 0x060043C2, "pose 1: two 0x01003A00 objects"),
    (0x3460, "8B08", 0x06004460, "pose 0: Japanese timing, then the objects"),
    (0x34CA, "8B08", 0x060044CA, "pose 4: Japanese timing, then the objects"),
    (0x35B8, "8B04", 0x060045B8, "random pose: 1 instead of 5"),
]


def patches() -> list[tuple]:
    return [
        (
            f,
            off,
            old,
            "0009",
            addr if f == "PL10.O" else addr + 0x8000,
            f"Sasquatch guard: {what}",
        )
        for f in ("PL10.O", "PL10.O2")
        for off, old, addr, what in GUARDS
    ]


def main() -> int:
    b32 = b33.b32
    b31 = b32.b31
    extra = b31.b23.patches(list(range(1, 15)), 0x10, 0, "late") + b31.patches()
    be.PATCHES = be.PATCHES + extra + b32.patches() + b33.patches() + patches()
    sys.argv = [
        sys.argv[0],
        sys.argv[1] if len(sys.argv) > 1 else "build/us_en_sasquatch",
    ]
    return be.main()


if __name__ == "__main__":
    raise SystemExit(main())
