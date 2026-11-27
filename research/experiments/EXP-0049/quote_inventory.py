"""Compare the two stock quote selectors' 14 roster tables and record offsets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from struct import unpack_from

EXTRACTED = Path("local/extracted")
RELEASES = {
    "us": (0x06012000, 0x06054714, 0x060547BC),
    "jp": (0x06013A00, 0x060547F4, 0x0605489C),
}
CONDITIONS = ("mirror", "high", "mid", "low")


def groups(
    main: bytes, base: int, table: int, count: int
) -> tuple[tuple[int, ...], ...]:
    pointers = unpack_from(">14I", main, table - base)
    return tuple(unpack_from(f">{4 * count}H", main, p - base) for p in pointers)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out", type=Path, help="record offsets and indices as JSON")
    args = parser.parse_args()
    us = EXTRACTED / "saturn_us"
    jp = EXTRACTED / "saturn_jp"
    main_us = (us / "MAIN.BIN").read_bytes()
    main_jp = (jp / "MAIN.BIN").read_bytes()
    base_us, *tables_us = RELEASES["us"]
    base_jp, *tables_jp = RELEASES["jp"]
    inventory = {}
    for language, count, table_us, table_jp in zip(
        ("JPN", "USA"), (8, 1), tables_us, tables_jp, strict=True
    ):
        left = groups(main_us, base_us, table_us, count)
        right = groups(main_jp, base_jp, table_jp, count)
        if left != right:
            raise ValueError(f"{language} quote selector tables differ")
        data = (us / f"ST1{language}.BIN").read_bytes()
        entries = {}
        roster = []
        for character, row in enumerate(left, 1):
            variants = {}
            for i, condition in enumerate(CONDITIONS):
                ids = row[i * count : (i + 1) * count]
                for idx in ids:
                    entry = 12 + 4 * idx
                    offset = entry + unpack_from(">I", data, entry)[0]
                    if not entry < offset < len(data):
                        raise ValueError(f"{language} quote {idx:#x} out of range")
                    entries[idx] = offset
                variants[condition] = ids
            roster.append({"fighter": character, **variants})
        print(f"{language}: {len(entries)} IDs, {len(set(entries.values()))} offsets")
        inventory[language] = {"selectable": entries, "roster": roster}
    args.out.write_text(json.dumps(inventory, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
