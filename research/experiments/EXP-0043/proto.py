"""RAM prototype: cart-backed FULL for two different fighters (US code).

Cold-boot an image, run to the title, then in RAM only:

- animation byte ``0x06080A29`` = ``--setting`` (default 1, FULL);
- ``--branch``: ``0x0602192A`` ``890F`` -> ``A00F`` (FULL skips the
  reduced-set path for any pair);
- ``--pool LOW HIGH``: allocator pool 2 (live ``0x06076AE8`` and baseline
  ``0x06076AD0``) set to LOW..HIGH, and both loaded-set slots
  (``0x0609022C``/``D``) set to ``FF`` so the next load reloads both sides.

Then force the attract fighters (``--ids``, written after the game's own
write at ``0x06035908``), log the loader, allocator exits and the
out-of-memory calls, and take screenshots every ``--every`` frames.
"""

from __future__ import annotations

import argparse
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "EXP-0042"))
from drive import (  # type: ignore[import-not-found]
    PADS,
    WRITERS,
    launch,
    run_steps,
    start,
    stop,
)

SETTING, BRANCH = 0x06080A29, 0x0602192A
P1_ID, P2_ID, ID_WRITER = 0x06076FD7, 0x060773DB, 0x06035908
POOLS, BASELINE, SLOTS = 0x06076AD8, 0x06076AC0, 0x0609022C
TRACE = (
    0x0602194C,  # indexes chosen (R13, R14)
    0x06021892,  # P1 set load
    0x060218BA,  # P2 set load
    0x06013EC0,  # bottom-up exit (R6 address)
    0x06013EE8,  # top-down exit (R0 address)
    0x06013EEE,  # top-down failure
    0x06013F1C,  # out of memory
    0x06013F68,  # out of memory
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cue", type=Path)
    parser.add_argument("out", type=Path, help="new directory")
    parser.add_argument("--cart", default="extram4")
    parser.add_argument("--title-frames", type=int, default=3900)
    parser.add_argument("--branch", action="store_true")
    parser.add_argument("--pool", type=lambda t: int(t, 16), nargs=2)
    parser.add_argument("--ids", type=int, nargs=2, default=(6, 11))
    parser.add_argument("--frames", type=int, default=2400)
    parser.add_argument("--every", type=int, default=300)
    parser.add_argument("--setting", type=int, default=1, choices=(0, 1))
    parser.add_argument(
        "--start-press",
        action="store_true",
        help="press Start after --title-frames and wait 600 frames, so the "
        "title task runs before the attract demo",
    )
    args = parser.parse_args()

    out = args.out.resolve()
    out.mkdir(parents=True)
    process, agent = launch(args.cue, out, None, args.cart)
    notes = []
    try:
        start(agent, None)
        agent.frames(args.title_frames)
        agent.wait_halted(timeout=180)
        if args.start_press:
            run_steps(agent, ["press:0800", "600"], out, PADS["us"], WRITERS["us"])
        agent.bus_write(SETTING, bytes([args.setting]))
        if args.branch:
            assert agent.bus_read(BRANCH, 2) == bytes.fromhex("890F")
            agent.bus_write(BRANCH, bytes.fromhex("A00F"))
        if args.pool:
            pair = struct.pack(">II", *args.pool)
            agent.bus_write(POOLS + 16, pair)
            agent.bus_write(BASELINE + 16, pair)
            agent.bus_write(SLOTS, b"\xff\xff")
        notes.append(f"pools-before {agent.bus_read(POOLS, 24).hex()}")
        notes.append(f"baseline {agent.bus_read(BASELINE, 24).hex()}")
        # Halt on the attract code's P2 ID write, then force both IDs.
        agent.bpmode("halt")
        agent.breakpoints("write", [f"{P2_ID:08X}-{P2_ID:08X}"])
        for value, address in zip(args.ids, (P1_ID, P2_ID), strict=True):
            agent.onhit_write(ID_WRITER, address, bytes([value]))
        agent.run()
        agent.wait_halted(timeout=300)
        agent.command("bp write")
        agent.step()
        agent.wait_halted()
        ids = agent.bus_read(P1_ID, 1)[0], agent.bus_read(P2_ID, 1)[0]
        notes.append(f"ids-after-force {ids[0]} {ids[1]}")
        agent.onhit_clear()
        agent.clear_events()
        agent.bpmode("log")
        agent.breakpoints("pc", [f"{pc:08X}-{pc:08X}" for pc in TRACE])
        for shot in range(args.frames // args.every):
            agent.frames(args.every)
            agent.wait_halted(timeout=180)
            agent.screenshot(out / f"f{(shot + 1) * args.every:05}.png")
        notes.append(f"pools-after {agent.bus_read(POOLS, 24).hex()}")
        notes.append(f"slots {agent.bus_read(SLOTS, 2).hex()}")
        (out / "trace.log").write_text("\n".join([*notes, *agent.events()]) + "\n")
        print("\n".join(notes))
    finally:
        stop(process)


if __name__ == "__main__":
    main()
