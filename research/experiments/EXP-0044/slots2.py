"""AUD-004: active SCSP slots in a Mednafen state, with pitch, level and pan.

Copied from ``research/experiments/EXP-0008/slots.py`` (this repository) and
extended. Reads the ``SCSP`` section's ``SlotRegs`` (32 slots x 16
little-endian 16-bit registers, as Mednafen 1.32.1 stores them) and
``Slots->EnvPhase`` (3 = release, HYPOTHESIS from the envelope order). Slot
register layout (word index) from the SCSP register map: 0 key-on and
SA(19:16), 1 SA(15:0), 2 LSA, 3 LEA, 6 TL (low 8 bits), 8 OCT (bits 14-11,
signed) and FNS (bits 9-0), 11 DISDL (15-13), DIPAN (12-8), EFSDL (7-5),
EFPAN (4-0).
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
        if not (r[0] >> 11) & 1 or phases[slot] == 3:
            continue
        octave = (r[8] >> 11) & 0xF
        out.append(
            {
                "slot": slot,
                "sa": ((r[0] & 0xF) << 16) | r[1],
                "lsa": r[2],
                "lea": r[3],
                "pcm8": (r[0] >> 4) & 1,
                "tl": r[6] & 0xFF,
                "oct": octave - 16 if octave & 8 else octave,
                "fns": r[8] & 0x3FF,
                "disdl": r[11] >> 13,
                "dipan": (r[11] >> 8) & 0x1F,
                "efsdl": (r[11] >> 5) & 7,
                "efpan": r[11] & 0x1F,
                "phase": phases[slot],
            }
        )
    return out
