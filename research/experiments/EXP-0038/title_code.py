"""EXP-0038: the title-time edition code appended to a relocated ``TITLE.O``.

    ./invenv.sh python research/experiments/EXP-0038/title_code.py   # self-check

``title_o()`` returns the new ``TITLE.O``: the stock file, zero padding over
``0x0600951C``-``0x06009567`` (``0x06009564`` is the title's frame counter,
which must start at zero), then the code below, and the header entry of the
title task (slot ``0x4D7``, header offset ``0x18``) pointed at the wrapper.

- **Wrapper** (the task runner jumps here each title frame, r4 = task): set
  the Appendix unlock byte ``0x06080A2B`` to 1 (user decision 2026-11-26,
  ``APP-001``/``EXP-0042``), call ``apply``, then jump to the stock task
  ``0x06004FAC`` with r4 and pr intact.
- **apply** (uses r0-r3 and r5-r7 only): E = settings block byte ``0x11``
  (``0x060830C5``; 0 US Enhanced, 1 US original, 2 JP original, 3 JP
  Enhanced; above 3 counts as 0). If E equals the last applied value (a byte
  here, 0xFF in the file, so each load of ``TITLE.O`` applies once), return.
  Otherwise write the flag ``0x0608089A``, language ``0x06080882`` and
  ``0x060808A8``, the content byte C ``0x060830C6`` (block byte ``0x12``),
  slot ``0x1BE`` (``0x06091E50``) = ``0x26020766``, and the ``MAIN.BIN`` patch
  list, choosing the bytes for US Enhanced, original, or JP Enhanced.
"""

from __future__ import annotations

import importlib.util
import struct
import sys
from pathlib import Path
from types import ModuleType

sys.path.insert(0, str(Path.cwd()))
from tools.sh2.asm import Assembler

TITLE = Path("local/extracted/saturn_us/TITLE.O")
MAIN = Path("local/extracted/saturn_us/MAIN.BIN")
BASE, MAIN_BASE = 0x06001000, 0x06012000
CODE = 0x06009568
TASK, TASK_SLOT_HEADER = 0x06004FAC, 0x18
E_ADDR, C_ADDR = 0x060830C5, 0x060830C6
NAME_OPTION, NAME_FLAG = 0x060830C7, 0x060830C8
NAME_OPTIONS = ("EDITION", "US", "JAPANESE")
# Name-only region readers: round HUD, results, loading, VS/Arcade wins, cast.
NAME_FLAG_LITERALS = (
    0x0601A198,
    0x0601A250,
    0x0601F244,
    0x06034188,
    0x060342F0,
    0x06042D30,
    0x06042F60,
    0x060446E4,
)
FLAG, LANG, LANG2 = 0x0608089A, 0x06080882, 0x060808A8
SLOT_1BE, R12_ORIG = 0x06091E50, 0x26020766
APPENDIX_FLAG, APPENDIX_STR = 0x06080A2B, 0x06001BE0
HANDLER_EXIT, APPENDIX_HANDLER = 0x06005622, 0x06005600
# ANI-003 (EXP-0043): cart-backed FULL animation
CART_ID, CART_4M = 0x24FFFFFF, 0x5C
CART_LO, CART_HI = 0x22400000, 0x22800000  # 4 MiB, cache-through
POOL2, BASE2, SLOTS = 0x06076AE8, 0x06076AD0, 0x0609022C
FULL_BRANCH = 0x0602192A  # bt 0x0602194C (FULL, same fighter) / bra (any pair)
CART_TESTS = (0x22400000, 0x22480000, 0x225FFFFC, 0x227FFFFC)
CART_PATTERN = 0x5AA5C33C
EDITION_NAMES = ["US ENHANCED", "US ORIGINAL", "JP ORIGINAL", "JP ENHANCED"]
LABEL_X, VALUE_X = 128, 200  # labels end at x 184 ("TIME LIMIT" at 104); values at 200
# per E: flag, language, C, and the index into each MAIN.BIN patch entry
VALUES = [(2, 1, 0, 0), (2, 1, 2, 1), (0, 0, 0, 1), (0, 0, 0, 2)]


def morrigan_enhanced_script() -> bytes:
    spec = importlib.util.spec_from_file_location(
        "b31", "research/experiments/EXP-0031/build_morrigan_main.py"
    )
    b31 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(b31)
    return b31.script()


def _load(name: str, path: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


sound_fix = _load("sound_fix", "research/experiments/EXP-0044/sound_fix.py")
jp_enhanced = _load("jp_enhanced", "research/experiments/EXP-0046/jp_enhanced.py")
us_quotes = _load("us_quotes", "research/experiments/EXP-0049/us_enhanced_quotes.py")


def main_bytes(addr: int, n: int) -> bytes:
    o = addr - MAIN_BASE
    return MAIN.read_bytes()[o : o + n]


def patch_list() -> list[tuple[int, bytes, bytes, bytes]]:
    """(address, US Enhanced, original, JP Enhanced) bytes in MAIN.BIN RAM."""
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
    enh.extend(us_quotes.patches(MAIN.read_bytes()))
    every = [
        # AUD-004 (EXP-0044): with Anakaris on P1, shared sounds prefer P2's
        # entry. Every edition (user decision 2026-11-26).
        (sound_fix.START, sound_fix.build()),
    ]
    patches = []
    for addr, enhanced in enh:
        original = main_bytes(addr, len(enhanced))
        patches.append((addr, enhanced, original, original))
    patches.extend((a, e, e, e) for a, e in every)
    for addr in NAME_FLAG_LITERALS:
        if main_bytes(addr, 4) != struct.pack(">I", FLAG):
            raise ValueError(f"{addr:#x}: unexpected name-region literal")
        pointer = struct.pack(">I", NAME_FLAG)
        patches.append((addr, pointer, pointer, pointer))
    for addr, replacement in jp_enhanced.patches(MAIN.read_bytes()):
        original = main_bytes(addr, len(replacement))
        patches.append((addr, original, original, replacement))
    return patches


def color(a: Assembler, idx_reg: int) -> None:
    """r6 = 3 if the cursor (@r12) equals idx_reg, else 1."""
    a.mov_w_load(12, 0)
    a.cmp_eq(idx_reg, 0)
    a.op(0x0629)  # movt r6
    a.shll(6)
    a.add_imm(1, 6)


def draw_line(a: Assembler, string_label: str | None, x: int) -> None:
    """Draw r7 (or string_label) at (x, r9) in colour r8, as TITLE.O does."""
    a.op(0x2FE6)  # mov.l r14,@-r15
    a.mov_imm(0, 2)
    a.op(0x2F26)  # mov.l r2,@-r15
    if string_label:
        a.mov_l_label(string_label, 7)
    a.mov(8, 6)
    a.mov(9, 5)
    a.mov_imm(x // 2, 4)
    a.shll(4)
    a.jsr(13)
    a.nop()
    a.add_imm(8, 15)


def resolve_name_region(a: Assembler) -> None:
    """Resolve the saved name preference without changing the region flag."""
    a.label("resolve_name_region")
    a.mov_l_label("L_flag", 1)
    a.mov_b_load(1, 2)
    a.mov_l_label("L_E", 1)
    a.mov_b_load(1, 0)
    a.tst(0, 0)
    a.branch("bt", "n_preference")
    a.op(0x8803)  # cmp/eq #3,r0: JP Enhanced
    a.branch("bf", "n_store")
    a.label("n_preference")
    a.mov_l_label("L_N", 1)
    a.mov_b_load(1, 0)
    a.op(0x8801)  # US name preference
    a.branch("bf", "n_check_jp")
    a.mov_imm(2, 2)
    a.branch("bra", "n_store")
    a.nop()
    a.label("n_check_jp")
    a.op(0x8802)  # Japanese name preference
    a.branch("bf", "n_store")
    a.mov_imm(0, 2)
    a.label("n_store")
    a.mov_l_label("L_nameflag", 1)
    a.mov_b_store(2, 1)
    a.rts()
    a.nop()


def menu(a: Assembler) -> None:
    """The EDITION line: drawing (from 0x06004B84) and input (from 0x06005400).

    draw: in OPTION MODE's draw function (r12 = cursor 0x0608086C, r13 = text
    routine 0x06018A1A, r14 = its first stack argument); draws APPENDIX as the
    stock code does when unlocked, then EDITION and its value in the next
    slot (index 9 at y 0xB8 locked, 10 at y 0xC8 unlocked).
    dispatch: reached for cursor values 9 and up (r0 = cursor; r10 = the
    left/right mask, r13 = 1, r14 = the pad words); APPENDIX keeps index 9
    when unlocked; on EDITION, left/right cycle E over 0-3, then r11 = r9 = 1
    as the other lines do (redraw), and all leave through 0x06005622.
    """
    a.label("draw")
    a.push_pr()
    a.op(0x2F86)  # mov.l r8,@-r15
    a.op(0x2F96)  # mov.l r9,@-r15
    a.op(0x2FA6)  # mov.l r10,@-r15
    a.mov_l_label("L_app", 0)
    a.mov_b_load(0, 0)
    a.tst(0, 0)
    a.branch("bt", "d_locked")
    a.mov_imm(9, 8)
    color(a, 8)
    a.mov(6, 8)
    a.mov_imm(0x5A, 9)
    a.shll(9)  # y 0xB4
    a.mov_l_label("L_appstr", 7)
    a.op(0x2FE6)
    a.mov_imm(0, 2)
    a.op(0x2F26)
    a.mov(8, 6)
    a.mov(9, 5)
    a.mov_imm(120, 4)
    a.jsr(13)
    a.nop()
    a.add_imm(8, 15)
    a.mov_imm(10, 8)
    a.mov_imm(0x60, 9)
    a.shll(9)  # y 0xC0
    a.branch("bra", "d_edition")
    a.nop()
    a.label("d_locked")
    a.mov_imm(9, 8)
    a.mov_imm(0x5A, 9)
    a.shll(9)  # y 0xB4
    a.label("d_edition")
    a.mov(8, 10)
    color(a, 8)
    a.mov(6, 8)
    draw_line(a, "L_label", LABEL_X)
    a.mov_l_label("L_E", 1)
    a.mov_b_load(1, 0)
    a.extu_b(0, 0)
    a.mov_imm(4, 1)
    a.cmp_hs(1, 0)
    a.branch("bf", "d_name")
    a.mov_imm(0, 0)
    a.label("d_name")
    a.op(0x4008)  # shll2 r0
    a.mov_l_label("L_names", 1)
    a.op(0x071E)  # mov.l @(r0,r1),r7
    draw_line(a, None, VALUE_X)
    a.add_imm(1, 10)
    a.add_imm(12, 9)
    color(a, 10)
    a.mov(6, 8)
    a.mov_l_label("L_E", 1)
    a.mov_b_load(1, 0)
    a.tst(0, 0)
    a.branch("bt", "d_pref")
    a.op(0x8803)
    a.branch("bt", "d_pref")
    a.mov_imm(1, 8)  # Original editions use the edition default.
    a.branch("bra", "d_picked")
    a.mov_imm(0, 10)  # delay slot
    a.label("d_pref")
    a.mov_l_label("L_N", 1)
    a.mov_b_load(1, 10)
    a.extu_b(10, 10)
    a.mov_imm(len(NAME_OPTIONS), 1)
    a.cmp_hs(1, 10)
    a.branch("bf", "d_picked")
    a.mov_imm(0, 10)
    a.label("d_picked")
    draw_line(a, "L_name_label", LABEL_X)
    a.mov(10, 0)
    a.op(0x4008)  # shll2 r0
    a.mov_l_label("L_name_values", 1)
    a.op(0x071E)  # mov.l @(r0,r1),r7
    draw_line(a, None, VALUE_X)
    a.op(0x6AF6)  # mov.l @r15+,r10
    a.op(0x69F6)  # mov.l @r15+,r9
    a.op(0x68F6)  # mov.l @r15+,r8
    a.pop_pr()
    a.rts()
    a.nop()

    a.label("dispatch")
    a.mov_l_label("L_app", 1)
    a.mov_b_load(1, 1)
    a.tst(1, 1)
    a.branch("bt", "x_locked")
    a.op(0x8809)  # cmp/eq #9,r0
    a.branch("bt", "x_appendix")
    a.op(0x880A)  # cmp/eq #10,r0
    a.branch("bt", "x_edition")
    a.op(0x880B)
    a.branch("bt", "x_names")
    a.branch("bra", "x_exit")
    a.nop()
    a.label("x_locked")
    a.op(0x8809)  # cmp/eq #9,r0
    a.branch("bt", "x_edition")
    a.op(0x880A)
    a.branch("bt", "x_names")
    a.label("x_exit")
    a.mov_l_label("L_exit", 1)
    a.op(0x412B)  # jmp @r1
    a.nop()
    a.label("x_appendix")
    a.mov_l_label("L_apphandler", 1)
    a.op(0x412B)
    a.nop()
    a.label("x_edition")
    a.mov_l_label("L_E", 1)
    a.branch("bra", "x_cycle")
    a.mov_imm(len(EDITION_NAMES), 5)  # delay slot
    a.label("x_names")
    a.mov_l_label("L_E", 1)
    a.mov_b_load(1, 0)
    a.tst(0, 0)
    a.branch("bt", "x_edit_names")
    a.op(0x8803)
    a.branch("bf", "x_exit")
    a.label("x_edit_names")
    a.mov_l_label("L_N", 1)
    a.mov_imm(len(NAME_OPTIONS), 5)
    a.label("x_cycle")
    a.mov_w_r0_disp(2, 14)
    a.op(0x600D)  # extu.w r0,r0
    a.tst(10, 0)
    a.branch("bt", "x_exit")
    a.mov_b_load(1, 2)
    a.extu_b(2, 2)
    a.cmp_hs(5, 2)  # invalid saved value counts as 0
    a.branch("bf", "x_e_ok")
    a.mov_imm(0, 2)
    a.label("x_e_ok")
    a.mov_imm(0x40, 3)
    a.shll8(3)  # 0x4000: left
    a.tst(3, 0)
    a.branch("bt", "x_right")
    a.add_imm(-1, 2)
    a.op(0x4211)  # cmp/pz r2
    a.branch("bt", "x_right")
    a.mov(5, 2)
    a.add_imm(-1, 2)
    a.label("x_right")
    a.mov_imm(-128, 3)
    a.shll8(3)  # ...8000: right
    a.tst(3, 0)
    a.branch("bt", "x_store")
    a.add_imm(1, 2)
    a.cmp_hs(5, 2)
    a.branch("bf", "x_store")
    a.mov_imm(0, 2)
    a.label("x_store")
    a.mov_b_store(2, 1)
    a.mov(13, 11)
    a.mov(13, 9)
    a.branch("bra", "x_exit")
    a.nop()


def cart(a: Assembler) -> None:
    """ANI-003 (EXP-0043): FULL for any pair when a 4 MiB cart is present.

    Uses r0-r3 and r5-r7 only. The cart ID (``0x24FFFFFF``) must read
    ``0x5C`` four times, and a non-destructive RAM test at four cache-through
    addresses must pass (once per ``TITLE.O`` load). Then, once per boot,
    allocator pool 2 (live and baseline) becomes the 4 MiB cart and both
    loaded-set slots are cleared, so the next load reloads both sides; and the
    ``FULL`` same-fighter branch becomes a ``bra``. Without the cart the stock
    branch is written back, so ``FULL`` and ``CUT`` behave as shipped.
    """
    a.label("cart")
    a.mov_l_label("L_cartid", 3)
    a.mov_imm(4, 5)
    a.label("c_id")
    a.mov_b_load(3, 0)
    a.extu_b(0, 0)
    a.op(0x8800 | CART_4M)  # cmp/eq #0x5C,r0
    a.branch("bf", "c_nocart")
    a.dt(5)
    a.branch("bf", "c_id")
    a.mov_l_label("L_cartok", 1)
    a.mov_b_load(1, 0)
    a.op(0x8801)  # cmp/eq #1,r0
    a.branch("bt", "c_ok")
    a.tst(0, 0)
    a.branch("bt", "c_nocart")  # failed earlier
    # RAM test: save, write address ^ pattern, verify, restore
    a.mov_l_label("L_tests", 6)
    a.mov_l_label("L_saves", 7)
    a.mov_imm(len(CART_TESTS), 5)
    a.label("t_write")
    a.mov_l_load(6, 2, post=True)
    a.mov_l_load(2, 0)
    a.mov_l_store(0, 7)
    a.add_imm(4, 7)
    a.mov_l_label("L_pattern", 0)
    a.op(0x202A)  # xor r2,r0
    a.mov_l_store(0, 2)
    a.dt(5)
    a.branch("bf", "t_write")
    a.mov_l_label("L_tests", 6)
    a.mov_imm(len(CART_TESTS), 5)
    a.mov_imm(1, 3)
    a.label("t_check")
    a.mov_l_load(6, 2, post=True)
    a.mov_l_label("L_pattern", 0)
    a.op(0x202A)  # xor r2,r0
    a.mov_l_load(2, 1)
    a.cmp_eq(1, 0)
    a.branch("bt", "t_next")
    a.mov_imm(0, 3)
    a.label("t_next")
    a.dt(5)
    a.branch("bf", "t_check")
    a.mov_l_label("L_tests", 6)
    a.mov_l_label("L_saves", 7)
    a.mov_imm(len(CART_TESTS), 5)
    a.label("t_restore")
    a.mov_l_load(6, 2, post=True)
    a.mov_l_load(7, 0, post=True)
    a.mov_l_store(0, 2)
    a.dt(5)
    a.branch("bf", "t_restore")
    a.mov_l_label("L_cartok", 1)
    a.mov_b_store(3, 1)
    a.tst(3, 3)
    a.branch("bt", "c_nocart")
    a.label("c_ok")
    a.mov_l_label("L_base2", 1)
    a.mov_l_load(1, 0)
    a.mov_l_label("L_cartlo", 2)
    a.cmp_eq(2, 0)
    a.branch("bt", "c_full")  # already redirected this boot
    a.mov_l_label("L_carthi", 3)
    a.mov_l_store(2, 1)
    a.op(0x1131)  # mov.l r3,@(4,r1)
    a.mov_l_label("L_pool2", 1)
    a.mov_l_store(2, 1)
    a.op(0x1131)  # mov.l r3,@(4,r1)
    a.mov_l_label("L_slots", 1)
    a.mov_imm(-1, 0)
    a.mov_b_store(0, 1)
    a.op(0x8011)  # mov.b r0,@(1,r1)
    a.label("c_full")
    a.mov_w_label("W_bra", 0)
    a.branch("bra", "c_store")
    a.nop()
    a.label("c_nocart")
    a.mov_w_label("W_bt", 0)
    a.label("c_store")
    a.mov_l_label("L_branch", 1)
    a.mov_w_store(0, 1)
    a.rts()
    a.nop()
    a.label("W_bra")
    a.word(0xA00F)
    a.label("W_bt")
    a.word(0x890F)


def code() -> bytes:
    a = Assembler(CODE)
    # wrapper
    a.label("wrapper")
    a.mov_l_label("L_app", 0)  # APP-001 (EXP-0042): Appendix unlocked by default
    a.mov_imm(1, 1)
    a.mov_b_store(1, 0)
    a.push_pr()
    a.mov_l_label("L_cart", 0)  # ANI-003 (EXP-0043)
    a.jsr(0)
    a.nop()
    a.mov_l_label("L_apply", 0)
    a.jsr(0)
    a.nop()
    a.mov_l_label("L_resolve_names", 0)
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
    a.mov_b_load(1, 7)  # patch column for this edition
    a.mov_l_label("L_slot", 3)
    a.mov_l_label("L_r12", 2)
    a.mov_l_store(2, 3)
    a.mov_l_label("L_list", 1)
    a.label("loop")
    a.mov_l_load(1, 5, post=True)  # address
    a.tst(5, 5)
    a.branch("bt", "done")
    a.mov_l_load(1, 6, post=True)  # length
    a.mov_l_load(1, 3, post=True)  # padded length
    a.mov(1, 2)
    a.tst(7, 7)
    a.branch("bt", "copy")
    a.add(3, 2)
    a.mov_imm(2, 0)
    a.cmp_eq(7, 0)
    a.branch("bf", "copy")
    a.add(3, 2)
    a.label("copy")
    a.mov_b_load(2, 0, post=True)
    a.mov_b_store(0, 5)
    a.add_imm(1, 5)
    a.dt(6)
    a.branch("bf", "copy")
    a.add(3, 1)
    a.add(3, 1)
    a.add(3, 1)
    a.branch("bra", "loop")
    a.nop()
    a.label("done")
    a.rts()
    a.nop()
    cart(a)
    resolve_name_region(a)
    menu(a)
    a.align4()
    for name, value in [
        ("L_apply", "apply"),
        ("L_task", TASK),
        ("L_E", E_ADDR),
        ("L_N", NAME_OPTION),
        ("L_nameflag", NAME_FLAG),
        ("L_resolve_names", "resolve_name_region"),
        ("L_last", "last"),
        ("L_values", "values"),
        ("L_flag", FLAG),
        ("L_lang", LANG),
        ("L_lang2", LANG2),
        ("L_C", C_ADDR),
        ("L_slot", SLOT_1BE),
        ("L_r12", R12_ORIG),
        ("L_list", "list"),
        ("L_app", APPENDIX_FLAG),
        ("L_appstr", APPENDIX_STR),
        ("L_exit", HANDLER_EXIT),
        ("L_apphandler", APPENDIX_HANDLER),
        ("L_names", "names"),
        ("L_label", "s_label"),
        ("L_name_label", "s_name_label"),
        ("L_name_values", "name_values"),
        ("L_cart", "cart"),
        ("L_cartid", CART_ID),
        ("L_cartok", "cartok"),
        ("L_tests", "tests"),
        ("L_saves", "saves"),
        ("L_pattern", CART_PATTERN),
        ("L_base2", BASE2),
        ("L_pool2", POOL2),
        ("L_cartlo", CART_LO),
        ("L_carthi", CART_HI),
        ("L_slots", SLOTS),
        ("L_branch", FULL_BRANCH),
    ]:
        a.label(name)
        a.long(value)
    a.label("values")
    a.data(b"".join(bytes(values) for values in VALUES))
    a.label("list")
    for addr, enh, orig, jp in patch_list():
        pad = (len(enh) + 3) & ~3
        a.data(struct.pack(">III", addr, len(enh), pad))
        a.data(b"".join(data.ljust(pad, b"\0") for data in (enh, orig, jp)))
    a.data(bytes(4))
    a.label("last")
    a.data(b"\xff\0\0\0")
    a.label("cartok")  # 0xFF untested, 1 passed, 0 failed (per TITLE.O load)
    a.data(b"\xff\0\0\0")
    a.label("tests")
    a.data(b"".join(struct.pack(">I", x) for x in CART_TESTS))
    a.label("saves")
    a.data(bytes(4 * len(CART_TESTS)))
    a.label("names")
    for i in range(4):
        a.long(f"s_{i}")
    a.label("name_values")
    for i in range(len(NAME_OPTIONS)):
        a.long(f"s_name_{i}")
    strings = [("s_label", "EDITION"), ("s_name_label", "NAMES")]
    strings += [(f"s_{i}", text) for i, text in enumerate(EDITION_NAMES)]
    strings += [(f"s_name_{i}", text) for i, text in enumerate(NAME_OPTIONS)]
    for name, text in strings:
        a.label(name)
        a.data(text.encode() + b"\0")
    out = a.assemble()
    _LAST_LABELS.clear()
    _LAST_LABELS.update(a.labels)
    return out


_LAST_LABELS: dict[str, int] = {}


def _labels() -> dict[str, int]:
    """The routine addresses, from a fresh assembly."""
    code()
    return dict(_LAST_LABELS)


def static_patches() -> list[tuple[int, bytes, bytes]]:
    """(address, stock bytes, new bytes) inside the stock TITLE.O."""
    lab = _labels()
    return [
        # OPTION MODE draw: the APPENDIX block becomes a call to "draw"
        (0x06004B84, bytes.fromhex("60302008"), bytes.fromhex("430B7F08")),
        (0x06004B88, bytes.fromhex("8D0E7F08"), bytes.fromhex("A00E0009")),
        (0x06004C54, struct.pack(">I", APPENDIX_FLAG), struct.pack(">I", lab["draw"])),
        # cursor bounds: last index 9/8 -> 11/10 (NAMES)
        (0x0600536A, bytes.fromhex("E109E108"), bytes.fromhex("E10BE10A")),
        (0x06005384, bytes.fromhex("E209E208"), bytes.fromhex("E20BE20A")),
        # Space the bottom rows by 12 pixels within the text renderer's bounds.
        (0x06004C46, bytes.fromhex("00D0"), bytes.fromhex("00D8")),
        # line dispatch: cursor 9 and up go to "dispatch"
        (
            0x060053FE,
            bytes.fromhex("88098B01A0FD0009A10C"),
            bytes.fromhex("D101412B0009") + struct.pack(">I", lab["dispatch"]),
        ),
    ]


def title_o() -> bytes:
    stock = bytearray(TITLE.read_bytes())
    slot, off = struct.unpack(">II", stock[TASK_SLOT_HEADER : TASK_SLOT_HEADER + 8])
    assert (slot, off) == (0x4D7, TASK - BASE), (hex(slot), hex(off))
    out = stock + bytes(CODE - BASE - len(stock)) + code()
    struct.pack_into(">I", out, TASK_SLOT_HEADER + 4, CODE - BASE)  # wrapper first
    for addr, old, new in static_patches():
        o = addr - BASE
        if out[o : o + len(old)] != old:
            raise ValueError(f"{addr:#x}: expected {old.hex()}")
        out[o : o + len(new)] = new
    if BASE + len(out) > 0x06010000:
        raise ValueError("title code past the free title-time RAM")
    return bytes(out)


if __name__ == "__main__":
    t = title_o()
    print(f"TITLE.O {len(TITLE.read_bytes())} -> {len(t)} bytes; code {len(code())}")
