"""EXP-0029: decode the per-character main-ending scripts of both regions.

    ./invenv.sh python research/experiments/EXP-0029/scripts.py [--text]

Reads the US MAIN.BIN (both tables are in it, chosen by the region flag at
0x060367A4: Japanese 0x0605B1C0, US 0x0605B730; 14 pointers each, roster
order). A script is an initial wait, then groups of six words (page id,
mode, frames shown, page id | 0x8000, mode, wait); the group whose wait is 0
is the last. Prints each
character's pages per region, ids only in one region, and shown frames.
With --text, also the US ST2USA.BIN record for each US page id (game text:
prints to the terminal only, never committed).
"""

from __future__ import annotations

import struct
import sys
from pathlib import Path

MAIN = Path("local/extracted/saturn_us/MAIN.BIN")
ST2USA = Path("local/extracted/saturn_us/ST2USA.BIN")
BASE = 0x06012000
TABLES = {"JP": 0x0605B1C0, "US": 0x0605B730}
ROSTER = [
    "Demitri",
    "Jon Talbain",
    "Victor",
    "Lord Raptor",
    "Morrigan",
    "Anakaris",
    "Felicia",
    "Bishamon",
    "Rikuo",
    "Sasquatch",
    "Huitzil",
    "Pyron",
    "Hsien-Ko",
    "Donovan",
]


def script(data: bytes, addr: int) -> tuple[int, list[tuple[int, int, int, int]]]:
    o = addr - BASE
    first = struct.unpack(">H", data[o : o + 2])[0]
    pages, o = [], o + 2
    while True:
        pid, mode, shown, hide, _mode2, wait = struct.unpack(">6H", data[o : o + 12])
        if hide != pid | 0x8000:
            raise ValueError(f"unexpected group at {addr:#x}+{o - (addr - BASE):#x}")
        pages.append((pid, mode, shown, wait))
        if wait == 0:
            return first, pages
        o += 12


def us_text(i: int) -> str:
    d = ST2USA.read_bytes()
    e = 0x0C + 4 * i
    v = struct.unpack(">I", d[e : e + 4])[0]
    if not v:
        return "(null entry)"
    o = e + v
    return d[o : d.index(b"\0", o)].decode("latin-1")


def main() -> int:
    data = MAIN.read_bytes()
    tables = {
        r: struct.unpack(">14I", data[a - BASE : a - BASE + 56])
        for r, a in TABLES.items()
    }
    for n, name in enumerate(ROSTER):
        jp, us = (script(data, tables[r][n]) for r in ("JP", "US"))
        jid, uid = [p[0] for p in jp[1]], [p[0] for p in us[1]]
        print(f"{n + 1:2} {name}: JP {len(jid)} pages, US {len(uid)} pages")
        print("   JP " + " ".join(f"{p:02x}:{s}" for p, _, s, _ in jp[1]))
        print("   US " + " ".join(f"{p:02x}:{s}" for p, _, s, _ in us[1]))
        only_jp = [f"{p:02x}" for p in jid if p not in uid]
        only_us = [f"{p:02x}" for p in uid if p not in jid]
        if only_jp or only_us or jid != [p for p in uid if p in jid]:
            print(f"   only JP {only_jp}  only US {only_us}  same order {jid == uid}")
        if "--text" in sys.argv:
            for p in uid:
                print(f"      {p:02x} {us_text(p)!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
