"""Inventory the Saturn text containers and find relative matches for UI labels."""

from __future__ import annotations

import hashlib
import sys
from collections import Counter
from pathlib import Path
from struct import iter_unpack, unpack_from

sys.path.insert(0, str(Path.cwd()))
from tools.text.search import find_all

DATA = Path("local/extracted")
TEXT_FILES = tuple(
    f"ST{series}{region}.BIN" for series in (1, 2) for region in ("JPN", "USA", "HIS")
)
LABELS = (
    "CONFIGURATION",
    "SOUND MODE",
    "PRESS START TO EXIT",
    "NOW LOADING",
    "MODE SELECT",
    "CONTINUE",
)


def offsets(data: bytes) -> tuple[int, ...]:
    """Decode the self-relative ST1 table up to its first record."""
    (first,) = unpack_from(">I", data, 12)
    if first % 4 or not 0 < first <= len(data) - 12:
        raise ValueError(f"invalid ST1 table size {first:#x}")
    pointers = tuple(
        entry + unpack_from(">I", data, entry)[0] for entry in range(12, 12 + first, 4)
    )
    if not all(12 + first <= p < len(data) for p in pointers):
        raise ValueError("ST1 record outside data")
    return pointers


def quote_lines(
    data: bytes, offset: int
) -> list[tuple[int, int, int, tuple[int, ...]]]:
    """Read ST1USA's line headers and glyphs, including control codes."""
    values = (v for (v,) in iter_unpack(">H", data[offset:]))
    lines = []
    while True:
        x, y, mode = (next(values) for _ in range(3))
        glyphs = []
        for word in values:
            if word in (0, 0xFFFF):
                break
            glyphs.append(word)
        else:
            raise ValueError("unterminated quote")
        lines.append((x, y, mode, tuple(glyphs)))
        if word == 0:
            return lines


def english_quote_comparison(jp: bytes, us: bytes) -> None:
    entries = offsets(us)
    if offsets(jp) != entries:
        raise ValueError("English-format quote table offsets differ")
    deltas: Counter[int] = Counter()
    adjusted_bytes = set()
    for start in sorted(set(entries)):
        jp_lines, us_lines = quote_lines(jp, start), quote_lines(us, start)
        pos = start
        for (jx, jy, jmode, jtext), (ux, uy, umode, utext) in zip(
            jp_lines, us_lines, strict=True
        ):
            if (jx, jmode, jtext) != (ux, umode, utext):
                raise ValueError(f"text or a non-Y header word differs at {pos:#x}")
            if jy != uy:
                deltas[uy - jy] += 1
                adjusted_bytes.update(o for o in (pos + 2, pos + 3) if jp[o] != us[o])
            pos += 2 * (4 + len(jtext))
    changed_bytes = {i for i, (a, b) in enumerate(zip(jp, us, strict=True)) if a != b}
    if adjusted_bytes != changed_bytes:
        raise ValueError("English-format files have differences outside quote lines")
    print(f"ST1USA Y-position changes: {sorted(deltas.items())}")


def main() -> int:
    by_region = {
        r: {name: (DATA / f"saturn_{r}" / name).read_bytes() for name in TEXT_FILES}
        for r in ("jp", "us")
    }
    for name in TEXT_FILES:
        jp, us = (by_region[r][name] for r in ("jp", "us"))
        slot, _, end = unpack_from(">3I", us)
        if end != 0xFFFFFFFF:
            raise ValueError(f"{name}: unexpected file header")
        print(
            name,
            f"slot={slot:#x}",
            f"bytes={len(us)}",
            f"changed={sum(a != b for a, b in zip(jp, us, strict=True))}",
            f"us_sha256={hashlib.sha256(us).hexdigest()}",
        )
        if name.startswith("ST1"):
            records = offsets(us)
            print(f"  entries={len(records)} unique_pointers={len(set(records))}")
    english_quote_comparison(
        by_region["jp"]["ST1USA.BIN"], by_region["us"]["ST1USA.BIN"]
    )

    files = by_region["us"] | {
        n: (DATA / "saturn_us" / n).read_bytes()
        for n in ("0.BIN", "MAIN.BIN", "TITLE.O", "ENDING.O")
    }
    for label in LABELS:
        raw = label.encode("ascii")
        matches = []
        for shift in range(-min(raw), 256 - max(raw)):
            pattern = bytes(code + shift for code in raw)
            for name, data in files.items():
                matches.extend((name, hex(o), shift) for o in find_all(data, pattern))
        print(f"{label}: {matches}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
