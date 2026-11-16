"""EXP-0037: map the zero and used runs of a WRAM-H range over save states.

    ./invenv.sh python research/experiments/EXP-0037/usage.py LO HI STATE...

Prints the runs of at least 64 bytes in [LO, HI) that are zero in every
state. A candidate only: an access watch confirms it.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

lo, hi = int(sys.argv[1], 16), int(sys.argv[2], 16)
used = bytearray(hi - lo)
for st in sys.argv[3:]:
    with tempfile.TemporaryDirectory() as t:
        subprocess.run(
            [
                sys.executable,
                "tools/memory/mcs_extract.py",
                "--region",
                "wram_h",
                "--out-dir",
                t,
                st,
            ],
            check=True,
            capture_output=True,
        )
        d = (Path(t) / "wram_h.bin").read_bytes()[lo - 0x06000000 : hi - 0x06000000]
    for i, b in enumerate(d):
        if b:
            used[i] = 1
i = 0
while i < len(used):
    j = i
    while j < len(used) and used[j] == used[i]:
        j += 1
    if not used[i] and j - i >= 64:
        print(f"zero {lo + i:#x}-{lo + j - 1:#x} {j - i}")
    i = j
