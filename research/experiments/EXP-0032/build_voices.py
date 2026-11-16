"""EXP-0032: US Enhanced with Morrigan's Japanese-only voices opened.

    ./invenv.sh python research/experiments/EXP-0032/build_voices.py [OUT_DIR]

The EXP-0031 build (14 English epilogues, Morrigan's restored main-ending
lines) plus, in Morrigan's code for both player sides (``PL05.O`` at
0x06001000 and ``PL05.O2``, same offsets), the four region-flag guards that
skip her voice calls made ``nop`` (EXP-0014, AUD-002). The flag stays 2.
OUT_DIR defaults to ``build/us_en_voices``.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
_spec = importlib.util.spec_from_file_location(
    "b31", "research/experiments/EXP-0031/build_morrigan_main.py"
)
b31 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(b31)
be = b31.be

# (file offset, original bf, P1 address, what the guarded call plays)
GUARDS = [
    (0x1490, "8B0B", 0x06002490, "codes 0x137/0x136: the bat-seat win line (EXP-0032)"),
    (0x1A1E, "8B09", 0x06002A1E, "codes 0x134/0x136 via 0x0603A76E"),
    (0x3342, "8B05", 0x06004342, "code 0x139"),
    (0x5280, "8B04", 0x06006280, "code 0x135"),
]


def patches() -> list[tuple]:
    out = []
    for f in ("PL05.O", "PL05.O2"):
        for off, old, addr, what in GUARDS:
            ram = addr if f == "PL05.O" else addr + 0x8000
            out.append((f, off, old, "0009", ram, f"voice guard -> nop: {what}"))
    return out


def main() -> int:
    extra = b31.b23.patches(list(range(1, 15)), 0x10, 0, "late") + b31.patches()
    be.PATCHES = be.PATCHES + extra + patches()
    sys.argv = [sys.argv[0], sys.argv[1] if len(sys.argv) > 1 else "build/us_en_voices"]
    return be.main()


if __name__ == "__main__":
    raise SystemExit(main())
