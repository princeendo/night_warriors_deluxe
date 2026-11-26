"""AUD-005: Morrigan's Soul Fist trail follows the fireball instead of the left edge.

    ./invenv.sh python research/experiments/EXP-0045/pan_fix.py   # self-check

Before queuing the trail sound (shared types ``g=2`` and ``g=5``), Morrigan's
overlay gets the screen position from ``0x0603AC44`` (0 to ``0x1F``) and
should combine it with the flags ``0x00030020`` or ``0x00040020``. It uses
``and r4,r5`` (``2549``), which leaves 0, the far-left slot, for every
position. Every other character's matching call uses ``or`` (``254B`` or
``253B``). The same ``and`` is at two sites in both copies of her code,
``PL05.O`` (P1, base ``0x06001000``) and ``PL05.O2`` (P2, base ``0x06009000``),
on both retail releases. The fix writes ``or r4,r5`` (``254B``) at each.
Applied to every edition (user decision 2026-11-26).
"""

from __future__ import annotations

from pathlib import Path

# file offsets (same in PL05.O and PL05.O2): 0x06004BE2 / 0x0600CBE2 and
# 0x06004DBA / 0x0600CDBA
SITES = (0x3BE2, 0x3DBA)
AND_R4_R5, OR_R4_R5 = bytes.fromhex("2549"), bytes.fromhex("254B")
FILES = ("PL05.O", "PL05.O2")


def apply(name: str, data: bytearray) -> None:
    """Patch one copy of Morrigan's overlay in place."""
    if name not in FILES:
        return
    for offset in SITES:
        if data[offset : offset + 2] != AND_R4_R5:
            raise ValueError(f"{name} {offset:#x}: expected and r4,r5")
        data[offset : offset + 2] = OR_R4_R5


if __name__ == "__main__":
    for region in ("us", "jp"):
        for name in FILES:
            data = bytearray(
                Path(f"local/extracted/saturn_{region}/{name}").read_bytes()
            )
            apply(name, data)
            print(f"{region} {name}: {len(SITES)} sites patched")
