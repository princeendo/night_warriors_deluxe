"""EXP-0038: the title-time edition code appended to a relocated ``TITLE.O``.

    ./invenv.sh python research/experiments/EXP-0038/title_code.py   # self-check

``title_o()`` returns the new ``TITLE.O``: the stock file, zero padding over
``0x0600951C``-``0x06009567`` (``0x06009564`` is the title's frame counter,
which must start at zero), then the code below, and the header entry of the
title task (slot ``0x4D7``, header offset ``0x18``) pointed at the wrapper.

- **Wrapper** (the task runner jumps here each title frame, r4 = task): call
  ``apply``, then jump to the stock task ``0x06004FAC`` with r4 and pr intact.
- **apply** (uses r0-r3 and r5-r7 only): E = settings block byte ``0x11``
  (``0x060830C5``; 0 US Enhanced, 1 US original, 2 JP original, 3 JP
  Enhanced; above 3 counts as 0). If E equals the last applied value (a byte
  here, 0xFF in the file, so each load of ``TITLE.O`` applies once), return.
  Otherwise write the flag ``0x0608089A``, language ``0x06080882`` and
  ``0x060808A8``, the content byte C ``0x060830C6`` (block byte ``0x12``),
  slot ``0x1BE`` (``0x06091E50``) = ``0x26020766``, and the ``MAIN.BIN`` patch
  list, choosing each entry's US Enhanced or original bytes.
"""

from __future__ import annotations

import importlib.util
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
from tools.sh2.asm import Assembler

TITLE = Path("local/extracted/saturn_us/TITLE.O")
MAIN = Path("local/extracted/saturn_us/MAIN.BIN")
BASE, MAIN_BASE = 0x06001000, 0x06012000
CODE = 0x06009568
TASK, TASK_SLOT_HEADER = 0x06004FAC, 0x18
E_ADDR, C_ADDR = 0x060830C5, 0x060830C6
FLAG, LANG, LANG2 = 0x0608089A, 0x06080882, 0x060808A8
SLOT_1BE, R12_ORIG = 0x06091E50, 0x26020766
# per E: flag, language, C
VALUES = [(2, 1, 0), (2, 1, 2), (0, 0, 0), (0, 0, 0)]


def morrigan_enhanced_script() -> bytes:
    spec = importlib.util.spec_from_file_location(
        "b31", "research/experiments/EXP-0031/build_morrigan_main.py"
    )
    b31 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(b31)
    return b31.script()


def main_bytes(addr: int, n: int) -> bytes:
    o = addr - MAIN_BASE
    return MAIN.read_bytes()[o : o + n]


def patch_list() -> list[tuple[int, bytes, bytes]]:
    """(address, US Enhanced bytes, original bytes) in MAIN.BIN's RAM."""
    st2his = 0x0605B780  # MAIN.BIN's own "ST2HIS.BIN" (the HIS name array)
    assert MAIN.read_bytes()[st2his - MAIN_BASE : st2his - MAIN_BASE + 11] == (
        b"ST2HIS.BIN\0"
    )
    enh = [
        # the ending's ST1 call loads ST2HIS.BIN (the English file) by name, ungated
        (0x0603B902, bytes.fromhex("D4380009")),
        (0x0603B908, bytes.fromhex("0009")),
        (0x0603B9E4, struct.pack(">II", st2his, 0x06013DF8)),
        # Morrigan's Enhanced main-ending script over her Japanese one (EXP-0031)
        (0x0605ADBC, morrigan_enhanced_script()),
        (0x0605B740, struct.pack(">I", 0x0605ADBC)),
    ]
    return [(a, e, main_bytes(a, len(e))) for a, e in enh]


def code() -> bytes:
    a = Assembler(CODE)
    # wrapper
    a.label("wrapper")
    a.push_pr()
    a.mov_l_label("L_apply", 0)
    a.jsr(0)
    a.nop()
    a.pop_pr()
    a.mov_l_label("L_task", 0)
    a.op(0x402B)  # jmp @r0
    a.nop()
    # apply
    a.label("apply")
    a.mov_l_label("L_E", 1)
    a.mov_b_load(1, 0)
    a.extu_b(0, 0)
    a.mov_imm(4, 2)
    a.cmp_hs(2, 0)  # E >= 4 ?
    a.branch("bf", "e_ok")
    a.mov_imm(0, 0)
    a.label("e_ok")
    a.mov_l_label("L_last", 1)
    a.mov_b_load(1, 2)
    a.extu_b(2, 2)
    a.cmp_eq(0, 2)
    a.branch("bt", "done")
    a.mov_b_store(0, 1)  # last = E
    a.mov_l_label("L_values", 1)
    a.mov(0, 3)
    a.op(0x4308)  # shll2 r3
    a.add(3, 1)
    a.mov_b_load(1, 2, post=True)  # flag
    a.mov_l_label("L_flag", 3)
    a.mov_b_store(2, 3)
    a.mov_b_load(1, 2, post=True)  # language
    a.mov_l_label("L_lang", 3)
    a.mov_b_store(2, 3)
    a.mov_l_label("L_lang2", 3)
    a.mov_b_store(2, 3)
    a.mov_b_load(1, 2, post=True)  # C
    a.mov_l_label("L_C", 3)
    a.mov_b_store(2, 3)
    a.mov_l_label("L_slot", 3)
    a.mov_l_label("L_r12", 2)
    a.mov_l_store(2, 3)
    a.tst(0, 0)  # T = (E == 0): US Enhanced
    a.op(0x0729)  # movt r7
    a.mov_l_label("L_list", 1)
    a.label("loop")
    a.mov_l_load(1, 5, post=True)  # address
    a.tst(5, 5)
    a.branch("bt", "done")
    a.mov_l_load(1, 6, post=True)  # length
    a.mov_l_load(1, 3, post=True)  # padded length
    a.mov(1, 2)
    a.tst(7, 7)
    a.branch("bf", "copy")  # r7 != 0: the US Enhanced bytes come first
    a.add(3, 2)
    a.label("copy")
    a.mov_b_load(2, 0, post=True)
    a.mov_b_store(0, 5)
    a.add_imm(1, 5)
    a.dt(6)
    a.branch("bf", "copy")
    a.add(3, 1)
    a.add(3, 1)
    a.branch("bra", "loop")
    a.nop()
    a.label("done")
    a.rts()
    a.nop()
    a.align4()
    for name, value in [
        ("L_apply", "apply"),
        ("L_task", TASK),
        ("L_E", E_ADDR),
        ("L_last", "last"),
        ("L_values", "values"),
        ("L_flag", FLAG),
        ("L_lang", LANG),
        ("L_lang2", LANG2),
        ("L_C", C_ADDR),
        ("L_slot", SLOT_1BE),
        ("L_r12", R12_ORIG),
        ("L_list", "list"),
    ]:
        a.label(name)
        a.long(value)
    a.label("values")
    a.data(b"".join(bytes([f, lang, c, 0]) for f, lang, c in VALUES))
    a.label("list")
    for addr, enh, orig in patch_list():
        pad = (len(enh) + 3) & ~3
        a.data(struct.pack(">III", addr, len(enh), pad))
        a.data(enh.ljust(pad, b"\0") + orig.ljust(pad, b"\0"))
    a.data(bytes(4))
    a.label("last")
    a.data(b"\xff\0\0\0")
    return a.assemble()


def title_o() -> bytes:
    stock = bytearray(TITLE.read_bytes())
    slot, off = struct.unpack(">II", stock[TASK_SLOT_HEADER : TASK_SLOT_HEADER + 8])
    assert (slot, off) == (0x4D7, TASK - BASE), (hex(slot), hex(off))
    out = stock + bytes(CODE - BASE - len(stock)) + code()
    struct.pack_into(">I", out, TASK_SLOT_HEADER + 4, CODE - BASE)  # wrapper first
    if BASE + len(out) > 0x06010000:
        raise ValueError("title code past the free title-time RAM")
    return bytes(out)


if __name__ == "__main__":
    t = title_o()
    print(f"TITLE.O {len(TITLE.read_bytes())} -> {len(t)} bytes; code {len(code())}")
