"""EXP-0037: find work-RAM runs that are zero in every sampled save state.

    ./invenv.sh python research/experiments/EXP-0037/free_ram.py MIN_LEN STATE...

Extracts WRAM-H and WRAM-L from each state (``tools/memory/mcs_extract.py``)
and prints the runs of at least MIN_LEN bytes that are zero in all of them.
A run that stays zero is only a candidate: never written in these states,
not proven unused (EXP-0037 confirms candidates with access watches).
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

REGIONS = {"wram_h": 0x06000000, "wram_l": 0x00200000}


def main() -> int:
    min_len, states = int(sys.argv[1]), [Path(p) for p in sys.argv[2:]]
    used = {r: bytearray(0x100000) for r in REGIONS}
    for st in states:
        with tempfile.TemporaryDirectory() as t:
            for r in REGIONS:
                subprocess.run(
                    [
                        sys.executable,
                        "tools/memory/mcs_extract.py",
                        "--region",
                        r,
                        "--out-dir",
                        t,
                        "--overwrite",
                        str(st),
                    ],
                    check=True,
                    capture_output=True,
                )
                data = (Path(t) / f"{r}.bin").read_bytes()
                u = used[r]
                for i, b in enumerate(data):
                    if b:
                        u[i] = 1
    for r, base in REGIONS.items():
        u, i = used[r], 0
        while i < len(u):
            if not u[i]:
                j = i
                while j < len(u) and not u[j]:
                    j += 1
                if j - i >= min_len:
                    print(f"{r} {base + i:#010x}-{base + j - 1:#010x} {j - i}")
                i = j
            else:
                i += 1
    print(f"{len(states)} states")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
