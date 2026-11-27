"""EXP-0038: the US image with the edition switch (EDITION-002).

    ./invenv.sh python research/experiments/EXP-0038/build_edition.py [OUT_DIR]

From the stock US image (no earlier build's static patches):

- ``TITLE.O``: the title-time code (``title_code.py``: apply routine, EDITION
  line), relocated to the free tail of track 1.
- ``ST2HIS.BIN`` (language 2, never selected) becomes the English epilogue
  file: the EXP-0023/EXP-0027 English ``ST1JPN.BIN`` (records, late routine)
  with a second header entry, slot ``0x1BE`` = ``0x20000000`` + the routine
  (the loader stores base + offset, so the slot holds the routine's
  cache-through address). Relocated to the free tail.
- ``PL05``/``PL10``/``PL14`` (``.O``, ``.O2``): every flag literal
  ``0x0608089A`` (all are region guards, EXP-0014) -> C ``0x060830C6``.
- ``ENDING.O``: the two one-frame waits ``0x06007BBC(1)`` at ``0x0600CF86``
  and ``0x0600CF8C`` become one ``0x06007BBC(2)``; ``0x0600CF92``-``0x0600CFC1``
  move up 6 bytes (PC-relative loads re-encoded); the freed bytes take
  r12 = @slot ``0x1BE`` (literal ``0x0600D0B0``); both Japanese-branch tests
  read C (literal ``0x0600D0B8``).
- ``ST2USA.BIN``: Morrigan's two new records (EXP-0031), harmless elsewhere.

- ``ST1USA.BIN``: append the US Enhanced victory quote variants after the
  stock records, keeping all stock records addressable by the same IDs.
- ``ST2JPN.BIN``: append the new JP Enhanced ending records, preserving all
  records used by the retail Japanese scripts.

``ST1JPN.BIN`` and ``MAIN.BIN`` stay stock; the title code writes the
``MAIN.BIN`` changes in RAM. OUT_DIR defaults to
``build/us_edition``.
"""

from __future__ import annotations

import importlib.util
import struct
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
from tools.disc import patch_image


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


pan_fix = load("pan_fix", "research/experiments/EXP-0045/pan_fix.py")
tc = load("tc", "research/experiments/EXP-0038/title_code.py")
b31 = load("b31", "research/experiments/EXP-0031/build_morrigan_main.py")
b23, be = b31.b23, b31.be

SOURCE = Path("local/disc_images/nw_saturn_us")
TRACK = "Night Warriors - Darkstalkers' Revenge (USA) (Track 1).bin"
MANIFEST = Path("references/saturn_us/README.md")
EXTRACTED = Path("local/extracted/saturn_us")
ENDING_BASE = 0x06001000
FLAG, C = bytes.fromhex("0608089A"), struct.pack(">I", tc.C_ADDR)
SLOT_1BE = 0x06091E50


def apply(data: bytes, patches: list[tuple]) -> bytes:
    return be.apply(data, patches)


def english_file() -> bytes:
    """The English ST1JPN.BIN of the working build, with a slot 0x1BE entry."""
    pat = [p for p in be.PATCHES if p[0] == "ST1JPN.BIN"]
    pat += [
        p
        for p in b23.patches(list(range(1, 15)), 0x10, 0, "late")
        if p[0] == "ST1JPN.BIN"
    ]
    st1 = apply((EXTRACTED / "ST1JPN.BIN").read_bytes(), pat)
    routine = next(p for p in pat if p[5] == "late routine")[1]
    assert st1[:12] == struct.pack(">II", 0x1BC, 0xC) + b"\xff" * 4
    header = struct.pack(">IIII", 0x1BC, 0x14, 0x1BE, 0x20000000 + routine + 8)
    return header + b"\xff" * 4 + st1[12:]


def overlay(name: str) -> bytes:
    data = bytearray((EXTRACTED / name).read_bytes())
    hits = [i for i in range(0, len(data) - 3, 4) if data[i : i + 4] == FLAG]
    if not hits:
        raise ValueError(f"{name}: no flag literal")
    for i in hits:
        data[i : i + 4] = C
    pan_fix.apply(name, data)  # AUD-005 (EXP-0045): Morrigan's trail pan
    return bytes(data)


def reencode(w: int, pc: int, new_pc: int) -> int:
    """Re-encode a PC-relative mov.l/mov.w moved from pc to new_pc."""
    if w >> 12 == 0xD:
        target = ((pc + 4) & ~3) + 4 * (w & 0xFF)
        disp, rest = divmod(target - ((new_pc + 4) & ~3), 4)
    elif w >> 12 == 0x9:
        target = pc + 4 + 2 * (w & 0xFF)
        disp, rest = divmod(target - (new_pc + 4), 2)
    else:
        return w
    if rest or not 0 <= disp <= 0xFF:
        raise ValueError(f"{pc:#x}: cannot re-encode")
    return w & 0xFF00 | disp


def ending() -> bytes:
    d = bytearray((EXTRACTED / "ENDING.O").read_bytes())

    def at(a: int, n: int) -> bytes:
        return bytes(d[a - ENDING_BASE : a - ENDING_BASE + n])

    def put(a: int, b: bytes) -> None:
        d[a - ENDING_BASE : a - ENDING_BASE + len(b)] = b

    assert at(0x0600CF86, 12) == bytes.fromhex("D33F430BE401D23D420BE401")
    assert at(0x0600CFC2, 12) == bytes.fromhex("DC3BDD3BD33C603020088B2F")
    assert at(0x0600D0B0, 4) == bytes.fromhex("06020766") and at(0x0600D0B8, 4) == FLAG
    put(0x0600CF86, bytes.fromhex("D33F430BE402"))  # one 0x06007BBC(2)
    moved = []
    for pc in range(0x0600CF92, 0x0600CFC2, 2):
        (w,) = struct.unpack(">H", at(pc, 2))
        if w >> 12 in (0x8, 0xA, 0xB) or (w & 0xFF00) in (0xC700,):
            raise ValueError(f"{pc:#x}: branch or mova in the moved block")
        moved.append(struct.pack(">H", reencode(w, pc, pc - 6)))
    put(0x0600CF8C, b"".join(moved))  # now 0x0600CF8C-0x0600CFBB
    # 0x0600CFBC-0x0600CFCD: r12 = @slot 0x1BE; r13; the C test; bf as before
    new = [
        ("D", 12, 0x0600D0B0),  # mov.l @(D0B0),r12 (literal -> slot 0x1BE)
        0x6CC2,  # mov.l @r12,r12
        ("D", 13, 0x0600D0B4),  # mov.l @(D0B4),r13
        ("D", 3, 0x0600D0B8),  # mov.l @(D0B8),r3 (literal -> C)
        0x6030,  # mov.b @r3,r0
        0x2008,  # tst r0,r0
        ("bf", 0x0600D02E),
        0x0009,
        0x0009,
    ]
    pc = 0x0600CFBC
    for item in new:
        if isinstance(item, int):
            w = item
        elif item[0] == "D":
            disp, rest = divmod(item[2] - ((pc + 4) & ~3), 4)
            assert not rest and 0 <= disp <= 0xFF
            w = 0xD000 | item[1] << 8 | disp
        else:
            disp, rest = divmod(item[1] - (pc + 4), 2)
            assert not rest and -0x80 <= disp < 0x80
            w = 0x8B00 | disp & 0xFF
        put(pc, struct.pack(">H", w))
        pc += 2
    assert pc == 0x0600CFCE
    put(0x0600D0B0, struct.pack(">I", SLOT_1BE))
    put(0x0600D0B8, C)
    return bytes(d)


def files() -> dict[str, bytes]:
    st2usa = [p for p in b31.patches() if p[0] == "ST2USA.BIN"]
    out = {
        "TITLE.O": tc.title_o(),
        "ST2HIS.BIN": english_file(),
        "ENDING.O": ending(),
        "ST1USA.BIN": tc.us_quotes.english_file(b23.encode),
        "ST2JPN.BIN": tc.jp_enhanced.ending_file(),
        "ST2USA.BIN": apply((EXTRACTED / "ST2USA.BIN").read_bytes(), st2usa),
    }
    for c in ("05", "10", "14"):
        for ext in ("O", "O2"):
            out[f"PL{c}.{ext}"] = overlay(f"PL{c}.{ext}")
    return out


def main() -> int:
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "build/us_edition"
    args = ["--source-dir", str(SOURCE), "--manifest", str(MANIFEST), "--track", TRACK]
    with tempfile.TemporaryDirectory(dir="build") as tmp:
        for name, data in files().items():
            (Path(tmp) / name).write_bytes(data)
            args += ["--file", name + ";1", "--data", str(Path(tmp) / name)]
        args += [
            "--relocate",
            "TITLE.O;1",
            "--relocate",
            "ST2HIS.BIN;1",
            "--relocate",
            "ST2JPN.BIN;1",
            "--relocate",
            "ST1USA.BIN;1",
        ]
        return patch_image.main([*args, "--out-dir", out_dir])


if __name__ == "__main__":
    raise SystemExit(main())
