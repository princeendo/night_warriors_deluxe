"""EXP-0023: build a US image whose epilogue for given characters is English.

    ./invenv.sh python research/experiments/EXP-0023/build_en_epilogue.py \
        [--out build/us_en_epilogue] [--y0 0x10] [--step 13] [--move-list] \
        CHAR [CHAR ...]

CHAR is the Saturn roster number (D-018: 5 = Morrigan). Starts from the
DISC-002 version 2 patches (EXP-0018 ``PATCHES``). For each character it
takes the PSP *Chronicle* English (EXP-0020) from the local, uncommitted
transcript, applies the logged spelling and name edits (user decisions of
2026-11-15), re-wraps it to ``WIDTH`` characters (a speaker line starts a new
line, as on the PSP), encodes it as the win-quote Latin set (D-021), and
writes it as a new epilogue record into the part of ``ST1JPN.BIN`` the
ending never reads (EXP-0023: from the first non-epilogue record on), then
points the character's self-relative table entry at it. Each line record is
x, y, 0001, codes; ``FFFF`` between lines, ``0000`` at the end.
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import struct
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
_spec = importlib.util.spec_from_file_location(
    "build_epilogue", "research/experiments/EXP-0018/build_epilogue.py"
)
be = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(be)

ST1JPN = Path("local/extracted/saturn_us/ST1JPN.BIN")
TRANSCRIPT = Path("local/ref002/psp_epilogues/transcript.md")  # game text, not in git
TABLE = 0x0C  # 32-bit self-relative offsets, entry = roster number - 1
EPILOGUES = 14
WIDTH = 26  # about 26 characters fit from x = 0x2C (EXP-0022)
X = 0x2C
# PSP movie number -> Saturn roster number (EXP-0020, D-018)
PSP_TO_ROSTER = {1: 13, 2: 14, 3: 1, 4: 5, 5: 6, 6: 3, 7: 4, 8: 2, 9: 7}
PSP_TO_ROSTER |= {10: 9, 11: 10, 12: 8, 13: 11, 14: 12}
# Logged edits (user decisions 2026-11-15): spelling and missing words; names
# as the US Saturn spells them. (old, new) applied in order, whole words.
EDITS = [
    ("new without speakig", "knew without speaking"),
    ("power that lie dormant", "power that lies dormant"),
    ("exaulted", "exalted"),
    ("kindom's", "kingdom's"),
    ("nothing more a horrible", "nothing more than a horrible"),
    ("Rapter", "Raptor"),
]
SWAPPED = {",": 0x00AE, ".": 0x00AC}  # not ASCII + 0x80 (D-021)


def encode(text: str) -> list[int]:
    out = []
    for c in text:
        if c == " ":
            out.append(0x0020)
        elif c in SWAPPED:
            out.append(SWAPPED[c])
        elif "a" <= c <= "z":
            out.append(0x0201 + ord(c) - ord("a"))
        elif "!" <= c <= "Z":
            out.append(ord(c) + 0x80)
        else:
            raise ValueError(f"no code for {c!r}")
    return out


def paragraph(roster: int) -> tuple[list[str], list[str]]:
    """Return (paragraphs after edits, edits applied) for a roster number."""
    psp = next(k for k, v in PSP_TO_ROSTER.items() if v == roster)
    sections = re.split(r"^## ", TRANSCRIPT.read_text(), flags=re.M)
    body = next(s for s in sections if s.startswith(f"{psp:02d} "))
    paras = [p for p in body.splitlines()[1:] if p.strip()]
    applied = []
    for old, new in EDITS:
        if any(old in p for p in paras):
            paras = [p.replace(old, new) for p in paras]
            applied.append(f"{old} -> {new}")
    return paras, applied


# --move-list (EXP-0024): the epilogue's glyph list starts at sprite array 2
# slot 0 (0x06083744) instead of slot 82 (0x060839D4). Array 1 is drawn under
# the art, so it is not used. The list's entries 64-81 are the player sprite
# slots (0x06083944-0x060839D3), rewritten every frame; a hidden line of
# filler glyphs, placed off screen, takes them so no text lands there.
LIST_LITERAL = ("MAIN.BIN", 0x25A98, "060839D4", "06083744", 0x06037A98)
HOLE = (64, 18)  # first entry index, length
SLOTS = 320  # 0x06083744 to the end of array 3 (0x06084144), 8 bytes each
FILLER = 0x00AC  # any non-space code; drawn off screen or overwritten
HIDDEN = (0x170, 0x00E0)  # x right of the screen, y at the bottom


def record(
    paras: list[str], y0: int, step: int, hole: tuple[int, int] | None = None
) -> tuple[bytes, list[str]]:
    lines = [line for p in paras for line in textwrap.wrap(p, WIDTH)]
    words: list[int] = []
    glyphs = 0
    for i, line in enumerate(lines):
        codes = encode(line)
        n = sum(c != 0x0020 for c in codes)
        if hole and glyphs <= hole[0] < glyphs + n:
            pad = hole[0] - glyphs + hole[1]
            words += [*([0xFFFF] if words else []), *HIDDEN, 0x0001, *[FILLER] * pad]
            glyphs += pad
        if words:
            words.append(0xFFFF)
        words += [X, y0 + i * step, 0x0001, *codes]
        glyphs += n
    if hole and glyphs > SLOTS:
        raise ValueError(f"{glyphs} glyph entries > {SLOTS} slots")
    words.append(0x0000)
    return struct.pack(f">{len(words)}H", *words), lines


def patches(chars: list[int], y0: int, step: int, move: bool = False) -> list[tuple]:
    data = ST1JPN.read_bytes()

    def entry(i: int) -> int:
        return TABLE + 4 * i

    count = (0x5D8 - TABLE) // 4  # the table ends where record 0 starts
    target = [
        entry(i) + struct.unpack(">I", data[entry(i) : entry(i) + 4])[0]
        for i in range(count)
    ]
    last_epilogue = max(target[:EPILOGUES])
    free = min(t for t in target if t > last_epilogue)  # first non-epilogue record
    out, pos = (
        ([(*LIST_LITERAL, "epilogue glyph list -> array 2 slot 0")] if move else []),
        free,
    )
    for roster in chars:
        paras, applied = paragraph(roster)
        rec, lines = record(paras, y0, step, HOLE if move else None)
        if pos + len(rec) > len(data):
            raise ValueError("records do not fit in ST1JPN.BIN")
        out.append(
            (
                "ST1JPN.BIN",
                pos,
                data[pos : pos + len(rec)].hex().upper(),
                rec.hex().upper(),
                None,
                f"roster {roster}: {len(lines)} lines; edits {applied or 'none'}",
            )
        )
        e = entry(roster - 1)
        out.append(
            (
                "ST1JPN.BIN",
                e,
                data[e : e + 4].hex().upper(),
                struct.pack(">I", pos - e).hex().upper(),
                None,
                f"table entry {roster - 1} -> {pos:#x}",
            )
        )
        pos += len(rec)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("chars", nargs="+", type=int)
    ap.add_argument("--out", default="build/us_en_epilogue")
    ap.add_argument("--y0", type=lambda v: int(v, 0), default=0x10)
    ap.add_argument("--step", type=int, default=13)
    ap.add_argument("--move-list", action="store_true")
    args = ap.parse_args()
    extra = patches(args.chars, args.y0, args.step, args.move_list)
    for p in extra:
        print(f"{p[0]} {p[1]:#06x} {len(p[3]) // 2} bytes: {p[5]}")
    be.PATCHES = be.PATCHES + extra
    sys.argv = [sys.argv[0], args.out]
    return be.main()


if __name__ == "__main__":
    assert encode("Ma'a, I.") == [0xCD, 0x201, 0xA7, 0x201, 0xAE, 0x20, 0xC9, 0xAC]
    assert record(["ab"], 0x10, 13)[0] == bytes.fromhex("002C0010000102010202" + "0000")
    _r = record(["ab cd"], 0x10, 13, (1, 2))[0]  # hole after the first glyph
    assert _r == bytes.fromhex(
        "0170 00E0 0001 00AC 00AC 00AC FFFF "
        "002C 0010 0001 0201 0202 0020 0203 0204 0000"
    ), _r.hex()
    raise SystemExit(main())
