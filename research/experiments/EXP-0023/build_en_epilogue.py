"""EXP-0023: build a US image whose epilogue for given characters is English.

    ./invenv.sh python research/experiments/EXP-0023/build_en_epilogue.py \
        [--out build/us_en_epilogue] [--y0 0x10] [--step 13] \
        [--move-list | --late-array1] CHAR [CHAR ...]

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
LIST_LITERAL = ("MAIN.BIN", 0x25A98, "060839D4")  # + new value, 0x06037A98
# name: (list start, HOLE (first entry, length), SLOTS to the end of array 3)
LAYOUTS = {
    "array2": (0x06083744, (64, 18), 320),  # EXP-0024
    "late": (0x060833CC, (175, 18), 431),  # EXP-0025: array 1 slot 17 on
}
# --late-array1 (EXP-0025, EXP-0026): ENDING.O calls r12 = 0x06020766 each
# frame, which ends by drawing arrays 2-3 after the art. A routine placed in
# ST1JPN.BIN calls it, then draws array 1 slots 17-127 again, last, so text
# there is on top. ST1JPN.BIN's load address depends on the character
# (0x060CB408 for Morrigan, 0x060C7C14 for Pyron), so r12 is computed when
# the epilogue starts: the loader stores the file's table address (slot
# 0x1BC) at 0x06091E48, and the three flag-test instructions the EXP-0018
# patch left unused become r12 = @0x06091E48 + (routine - 0x0C), through the
# cache-through mirror (0x2...).
SLOT_1BC = 0x06091E48  # 0x06091758 + 4 * 0x1BC
R12_PATCHES = [  # (file, offset, original, new, address); None = the delta
    ("ENDING.O", 0xC0B0, "06020766", f"{SLOT_1BC:08X}", 0x0600D0B0),
    ("ENDING.O", 0xBFC6, "D33C60302008", "6CC2D33B3C3C", 0x0600CFC6),
    ("ENDING.O", 0xC0B8, "0608089A", None, 0x0600D0B8),
]
LATE_ROUTINE = (
    "4F22 D305 430B 0009"  # sts.l pr,@-r15; mov.l main,r3; jsr @r3; nop
    "D404 D305 430B E56F"  # mov.l base,r4; mov.l reader,r3; jsr @r3; mov #111,r5
    "4F26 000B 0009 0009"  # lds.l @r15+,pr; rts; nop; (pad)
    "06020766 060833CC 060188D4"  # main, base (array 1 slot 17), reader
)
FILLER = 0x00AC  # any non-space code; drawn off screen or overwritten
HIDDEN = (0x170, 0x00E0)  # x right of the screen, y at the bottom


def record(
    paras: list[str],
    y0: int,
    step: int,
    hole: tuple[int, int] | None = None,
    slots: int = 0,
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
    if hole and glyphs > slots:
        raise ValueError(f"{glyphs} glyph entries > {slots} slots")
    words.append(0x0000)
    return struct.pack(f">{len(words)}H", *words), lines


def patches(chars: list[int], y0: int, step: int, layout: str = "") -> list[tuple]:
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
    out, pos = [], free
    hole, slots = None, 0
    if layout:
        start, hole, slots = LAYOUTS[layout]
        f, off, old = LIST_LITERAL
        out.append(
            (f, off, old, f"{start:08X}", 0x06037A98, f"glyph list -> {start:#x}")
        )
    for roster in chars:
        paras, applied = paragraph(roster)
        n_lines = len([x for p in paras for x in textwrap.wrap(p, WIDTH)])
        # step 0 (--auto-step, EXP-0026): 13 px up to 16 lines, else 12 px
        line_step = step or (13 if n_lines <= 16 else 12)
        rec, lines = record(paras, y0, line_step, hole, slots)
        if pos + len(rec) > len(data):
            raise ValueError("records do not fit in ST1JPN.BIN")
        out.append(
            (
                "ST1JPN.BIN",
                pos,
                data[pos : pos + len(rec)].hex().upper(),
                rec.hex().upper(),
                None,
                f"roster {roster}: {len(lines)} lines at {line_step} px; "
                f"edits {applied or 'none'}",
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
    if layout == "late":
        pos = (pos + 3) & ~3
        code = bytes.fromhex(LATE_ROUTINE)
        old = data[pos : pos + len(code)].hex().upper()
        out.append(("ST1JPN.BIN", pos, old, code.hex().upper(), None, "late routine"))
        delta = f"{0x20000000 | (pos - TABLE):08X}"  # + table address = routine
        for f, off, orig, new, ram in R12_PATCHES:
            out.append((f, off, orig, new or delta, ram, "r12 = @0x06091E48 + delta"))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("chars", nargs="+", type=int)
    ap.add_argument("--out", default="build/us_en_epilogue")
    ap.add_argument("--y0", type=lambda v: int(v, 0), default=0x10)
    ap.add_argument("--step", type=int, default=13)  # 0: by line count (EXP-0026)
    ap.add_argument("--move-list", action="store_true")  # EXP-0024
    ap.add_argument("--late-array1", action="store_true")  # EXP-0025
    args = ap.parse_args()
    layout = "late" if args.late_array1 else "array2" if args.move_list else ""
    extra = patches(args.chars, args.y0, args.step, layout)
    for p in extra:
        print(f"{p[0]} {p[1]:#06x} {len(p[3]) // 2} bytes: {p[5]}")
    be.PATCHES = be.PATCHES + extra
    sys.argv = [sys.argv[0], args.out]
    return be.main()


if __name__ == "__main__":
    assert encode("Ma'a, I.") == [0xCD, 0x201, 0xA7, 0x201, 0xAE, 0x20, 0xC9, 0xAC]
    assert record(["ab"], 0x10, 13)[0] == bytes.fromhex("002C0010000102010202" + "0000")
    _r = record(["ab cd"], 0x10, 13, (1, 2), 9)[0]  # hole after the first glyph
    assert _r == bytes.fromhex(
        "0170 00E0 0001 00AC 00AC 00AC FFFF "
        "002C 0010 0001 0201 0202 0020 0203 0204 0000"
    ), _r.hex()
    raise SystemExit(main())
