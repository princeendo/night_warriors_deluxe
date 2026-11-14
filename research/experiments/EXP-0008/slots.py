"""EXP-0008: list the SCSP slots playing in Mednafen save states.

Run from the repository root:

    ./invenv.sh python research/experiments/EXP-0008/slots.py STATE [STATE ...]

For each state prints its name and every slot whose key-on bit is set and
whose envelope is not in release, with the sample start address (SA, a byte
address in sound RAM), loop start/end, and 8-bit flag. Reads the ``SCSP``
section's ``SlotRegs`` (32 slots x 16 little-endian 16-bit registers, as
Mednafen 1.32.1 stores them) and ``Slots->EnvPhase`` (one byte per slot; 3 is
release, HYPOTHESIS from the SCSP envelope order attack/decay1/decay2/release).
"""

from __future__ import annotations

import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
from tools.memory.mcs_extract import parse_state


def active_slots(raw: bytes) -> list[dict[str, int]]:
    scsp = parse_state(raw).sections["SCSP"]
    regs = struct.unpack("<512H", scsp["SlotRegs"])
    phases = scsp["Slots->EnvPhase"]
    out = []
    for slot in range(32):
        r = regs[slot * 16 : slot * 16 + 16]
        key_on = (r[0] >> 11) & 1
        if not key_on or phases[slot] == 3:
            continue
        out.append(
            {
                "slot": slot,
                "sa": ((r[0] & 0xF) << 16) | r[1],
                "lsa": r[2],
                "lea": r[3],
                "pcm8": (r[0] >> 4) & 1,
                "phase": phases[slot],
            }
        )
    return out


def main(paths: list[str]) -> int:
    for path in paths:
        slots = active_slots(Path(path).read_bytes())
        text = " ".join(
            f"{s['slot']:02d}:SA={s['sa']:05X}/{s['lea']:04X}"
            + ("b" if s["pcm8"] else "w")
            for s in slots
        )
        print(f"{Path(path).name} {text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
