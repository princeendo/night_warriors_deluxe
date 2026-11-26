"""Tally successful allocations per pool from force_match.py logs."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path

HIT = re.compile(r"^hit n=\d+ frame=(\d+) mode=log PC=([0-9A-F]{8}) ")
REG = re.compile(r" (R\d+|PR)=([0-9A-F]{8})")
POOL_NAMES = ("WRAM-H", "WRAM-L", "VDP2")


def tally(path: Path) -> None:
    pending: dict[str, tuple[int, int]] = {}
    used: Counter[str] = Counter()
    failed = 0
    loads: list[str] = []
    for line in path.read_text().splitlines():
        match = HIT.match(line)
        if not match:
            continue
        frame, pc = int(match[1]), int(match[2], 16)
        regs = {name: int(value, 16) for name, value in REG.findall(line)}
        size = (regs["R4"] + 3) & ~3
        if pc in (0x06013E9C, 0x06013EC4):
            pending[f"{pc:X}"] = (size, regs["R5"])
        elif pc == 0x06013EC0:
            size, pool = pending.pop("6013E9C")
            if regs["R6"]:
                used[POOL_NAMES[pool]] += size
        elif pc == 0x06013EE8:
            size, pool = pending.pop("6013EC4")
            used[POOL_NAMES[pool]] += size
        elif pc == 0x06013EEE:
            pending.pop("6013EC4")
        elif pc == 0x06013F7C:
            used["VDP1"] += (regs["R4"] + 7) & ~7
        elif pc == 0x06013F9E:
            used["VDP2 carve"] += size
        elif pc in (0x06013F1C, 0x06013F68):
            failed = regs["R13"]
            loads.append(f"frame {frame}: Out Of Memory for {failed:,} bytes")
        elif pc in (0x06021892, 0x060218BA):
            index = regs["R14"]
            suffix = "_" if index >= 14 else ""
            loads.append(f"frame {frame}: load P{index % 14 + 1:02}{suffix}")
    print(path)
    for line in loads:
        print(f"  {line}")
    for name, total in sorted(used.items()):
        print(f"  {name:11}{total:11,d}")
    pools = sum(used[name] for name in POOL_NAMES)
    print(f"  {'pools':11}{pools:11,d}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("logs", type=Path, nargs="+")
    for path in parser.parse_args().logs:
        tally(path)


if __name__ == "__main__":
    main()
