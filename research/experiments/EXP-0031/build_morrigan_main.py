"""EXP-0031: US Enhanced with Morrigan's missing main-ending lines restored.

    ./invenv.sh python research/experiments/EXP-0031/build_morrigan_main.py [OUT_DIR]

Starts from the all-14 English epilogue build (EXP-0023 ``--late-array1
--step 0`` for rosters 1-14) and adds, for Morrigan's main ending only (user
decisions of 2026-11-16, END-004):

- two new ``ST2USA.BIN`` records, written in the file's unused tail
  (0x418-0x4BD: table entries past the highest page id the scripts use, and
  an "A" placeholder record nothing points at), reached by the unused table
  entries 0xB1 and 0xB2;
- a new US script for Morrigan (her nine US pages, the two new pages after
  "Hurry…" inside the butler scene, the scene timing kept), written over
  her Japanese script (0x0605ADBC, exactly 134 bytes,
  unread while the region flag is 2), and the US table entry 4 (0x0605B740)
  pointed at it.

The two English lines are a new translation (rule 29), approved by the user
on 2026-11-16; the PSP Chronicle has no English for them (EXP-0031).
OUT_DIR defaults to ``build/us_en_morrigan_main``.
"""

from __future__ import annotations

import importlib.util
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
_spec = importlib.util.spec_from_file_location(
    "b23", "research/experiments/EXP-0023/build_en_epilogue.py"
)
b23 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(b23)
be = b23.be

ST2USA = Path("local/extracted/saturn_us/ST2USA.BIN")
MAIN = Path("local/extracted/saturn_us/MAIN.BIN")
BASE = 0x06012000
NEW_LINES = {  # new translation (rule 29), user choices of 2026-11-16
    0xB1: ["I'm a little tired.", "Prepare my bed."],  # Morrigan (JP ST2JPN 36)
    0xB2: ["Certainly, mistress."],  # the butler (JP ST2JPN 37)
}
RECORD_AT = {0xB1: 0x418, 0xB2: 0x46C}
FREE = (0x418, 0x4BE)
X, Y0 = 0x1D, 0xB0  # as her other US pages
SCRIPT_AT = 0x0605ADBC  # Morrigan's Japanese script
US_TABLE_ENTRY = 0x0605B730 + 4 * 4
OLD_US_SCRIPT = 0x0605B344
# (page id, frames shown, wait after). The pictures run on their own timeline
# (EXP-0031: script time + 422 frames; the butler scene ends near 3,850, the
# bed scene runs 3,980-4,870), so the new pages fit inside the butler scene by
# shortening pages 33-36 there; from 37 on, every page starts and ends as
# shipped (37 at 3,980, B0 ending at 4,820). The Japanese pause page has no
# room; the shipped 140-frame wait before B0 stands for it.
PAGES = [
    (0x30, 0x118, 0x001),
    (0x31, 0x103, 0x49C),
    (0x32, 0x078, 0x078),
    (0x33, 0x1A4, 0x014),  # 480 -> 420 frames
    (0x34, 0x1E0, 0x028),  # 540 -> 480, wait 60 -> 40
    (0x35, 0x0F0, 0x01E),  # 300 -> 240, wait 60 -> 30
    (0x36, 0x0F0, 0x01E),  # 300 -> 240, wait 180 -> 30
    (0xB1, 0x0A0, 0x014),  # new: Morrigan, 160 frames
    (0xB2, 0x078, 0x08C),  # new: the butler, 120 frames; then the scene change
    (0x37, 0x12C, 0x08C),
    (0xB0, 0x190, 0x000),
]


def record(lines: list[str]) -> bytes:
    words: list[int] = []
    for i, line in enumerate(lines):
        if i:
            words.append(0xFFFF)
        words += [X, Y0 + 0x10 * i, 0x0001, *b23.encode(line)]
    words.append(0x0000)
    return struct.pack(f">{len(words)}H", *words)


def script() -> bytes:
    words = [0x0050]
    for pid, shown, wait in PAGES:
        words += [pid, 0, shown, pid | 0x8000, 0, wait]
    return struct.pack(f">{len(words)}H", *words)


def patches() -> list[tuple]:
    st2, main = ST2USA.read_bytes(), MAIN.read_bytes()
    out = []
    for pid, lines in NEW_LINES.items():
        rec, at = record(lines), RECORD_AT[pid]
        if not (FREE[0] <= at and at + len(rec) <= FREE[1]):
            raise ValueError("record outside the free tail")
        out.append(
            (
                "ST2USA.BIN",
                at,
                st2[at : at + len(rec)].hex().upper(),
                rec.hex().upper(),
                None,
                f"new record, page {pid:#x}",
            )
        )
        e = 0x0C + 4 * pid
        out.append(
            (
                "ST2USA.BIN",
                e,
                st2[e : e + 4].hex().upper(),
                struct.pack(">I", at - e).hex().upper(),
                None,
                f"entry {pid:#x}",
            )
        )
    s, o = script(), SCRIPT_AT - BASE
    if len(s) != 134:
        raise ValueError(f"script is {len(s)} bytes, the slot 134")
    out.append(
        (
            "MAIN.BIN",
            o,
            main[o : o + len(s)].hex().upper(),
            s.hex().upper(),
            SCRIPT_AT,
            "Morrigan's new US script (over her JP script)",
        )
    )
    o = US_TABLE_ENTRY - BASE
    out.append(
        (
            "MAIN.BIN",
            o,
            f"{OLD_US_SCRIPT:08X}",
            f"{SCRIPT_AT:08X}",
            US_TABLE_ENTRY,
            "US script table entry 4 -> the new script",
        )
    )
    return out


def main() -> int:
    extra = b23.patches(list(range(1, 15)), 0x10, 0, "late") + patches()
    be.PATCHES = be.PATCHES + extra
    sys.argv = [
        sys.argv[0],
        sys.argv[1] if len(sys.argv) > 1 else "build/us_en_morrigan_main",
    ]
    return be.main()


if __name__ == "__main__":
    assert len(script()) == 134 and record(["Ab"]).hex() == "001d00b0000100c102020000"
    raise SystemExit(main())
