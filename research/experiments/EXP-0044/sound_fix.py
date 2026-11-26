"""AUD-004: with Anakaris on P1, shared sounds prefer the opponent's own entry.

    ./invenv.sh python research/experiments/EXP-0044/sound_fix.py   # self-check

The stock lookup for a shared sound (record type ``0xFE``, US ``MAIN.BIN``
``0x0603A1C8``-``0x0603A215``) checks P1's character (``0x0607663B``) in the
per-character table ``0x0606C10C[g]`` first, and plays P1's bank whenever
P1's character has an entry, even for a P2 request. Anakaris has entries for
17 of the 27 types, and every one is also owned by another character: they
are copies of other characters' sounds. So with him on P1, a P2 opponent's
fireball, dash or ice sound comes from his bank (EXP-0044). With him on P2
the opponent's own entry wins, which the playtester reported as correct.

The requester is not recorded in the queue (the dash uses ID ``0x75`` from
either side), so the replacement makes the P1-Anakaris case behave like the
P2-Anakaris case: when P1's character is Anakaris (6), P2's character is
tried first. Otherwise the order is stock (P1, then P2). The first character
with an entry plays its song from its own bank (1 for ``0x0607663B``, 2 for
``0x0607663C``).

It fills the same 78 bytes and keeps the stock literals (``0x0603A280`` =
``0x00FE``, ``0x0603A284`` = ``0x0607663B``, ``0x0603A288`` =
``0x0606C10C``) and exits (``0x0603A216`` not shared, ``0x0603A256`` play
with r0 = song and r14 = bank, ``0x0603A272`` no entry).
"""

from __future__ import annotations

import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
from tools.sh2.asm import Assembler

MAIN = Path("local/extracted/saturn_us/MAIN.BIN")
MAIN_BASE = 0x06012000
START, END = 0x0603A1C8, 0x0603A216
ANAKARIS = 6
EXTERNAL = {
    "W_FE": 0x0603A280,
    "L_P1CHR": 0x0603A284,
    "L_TABLE": 0x0603A288,
    "not_shared": 0x0603A216,
    "play": 0x0603A256,
    "none": 0x0603A272,
}
LITERALS = [(0x0603A280, 2, 0x00FE), (0x0603A284, 4, 0x0607663B)]
LITERALS.append((0x0603A288, 4, 0x0606C10C))


def build() -> bytes:
    """The replacement, padded with nops to the stock length."""
    a = Assembler(START)
    a.labels.update(EXTERNAL)
    a.mov_l_label("L_P1CHR", 14)  # r14 = 0x0607663B
    a.mov_w_label("W_FE", 2)
    a.mov(14, 5)  # r5 = P1 character byte
    a.mov(14, 6)
    a.cmp_eq(2, 4)
    a.branch("bf/s", "not_shared")
    a.add_imm(1, 6)  # r6 = P2 character byte (delay slot, as stock)
    a.mov_b_load(5, 0)  # P1 character
    a.op(0x8800 | ANAKARIS)  # cmp/eq #6,r0
    a.branch("bf", "order")
    a.mov(6, 5)  # Anakaris on P1: try P2 first
    a.mov(14, 6)
    a.label("order")
    a.op(0x84D4)  # mov.b @(4,r13),r0   (type g)
    a.op(0x4008)  # shll2 r0
    a.mov_l_label("L_TABLE", 4)
    a.op(0x044E)  # mov.l @(r0,r4),r4   (table[g])
    a.mov(5, 1)  # first candidate
    a.label("try")
    a.mov_b_load(1, 12)  # character (1-14)
    a.add_imm(-1, 12)
    a.shll(12)
    a.add(4, 12)  # r12 = &table[g][character - 1]
    a.mov_b_load(12, 3)  # flag
    a.tst(3, 3)
    a.branch("bf", "found")
    a.cmp_eq(1, 6)
    a.branch("bt", "none")  # neither character has the sound
    a.branch("bra", "try")
    a.mov(6, 1)  # second candidate (delay slot)
    a.label("found")
    a.op(0x31E8)  # sub r14,r1   (0 for P1, 1 for P2)
    a.add_imm(1, 1)
    a.mov(1, 14)  # r14 = bank
    a.branch("bra", "play")
    a.op(0x84C1)  # mov.b @(1,r12),r0   (song, delay slot)
    code = a.assemble()
    if len(code) > END - START:
        raise ValueError(f"{len(code)} bytes, room for {END - START}")
    return code + bytes.fromhex("0009") * ((END - START - len(code)) // 2)


def stock() -> bytes:
    data = MAIN.read_bytes()
    for address, width, value in LITERALS:
        o = address - MAIN_BASE
        if int.from_bytes(data[o : o + width], "big") != value:
            raise ValueError(f"unexpected literal at {address:#x}")
    if (
        struct.unpack(">H", data[START - MAIN_BASE : START - MAIN_BASE + 2])[0]
        != 0xDE2E
    ):
        raise ValueError("unexpected shared-sound code")
    return data[START - MAIN_BASE : END - MAIN_BASE]


if __name__ == "__main__":
    print(f"{len(build())} bytes at {START:#x} (stock {len(stock())}):")
    print(build().hex())
