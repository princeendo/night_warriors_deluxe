"""AUD-004: dump sound RAM after a forced attract fight loads.

Cold-boot an image (no cart), press Start so the title runs, force the
attract fighters (one-based IDs written after the game's own write at
``--writer``), let the fight load, then dump all 512 KiB of sound RAM
(``scspram``) to ``OUT/scspram.bin`` and take a screenshot.
"""

from __future__ import annotations

import argparse
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

LAYOUT = {  # P1 ID, P2 ID, attract ID writer
    "us": (0x06076FD7, 0x060773DB, 0x06035908),
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cue", type=Path)
    parser.add_argument("out", type=Path, help="new directory")
    parser.add_argument("--ids", type=int, nargs=2, required=True)
    parser.add_argument("--region", choices=LAYOUT, default="us")
    parser.add_argument("--writer", type=lambda t: int(t, 16))
    parser.add_argument("--frames", type=int, default=900)
    args = parser.parse_args()
    p1, p2, writer = LAYOUT[args.region]
    writer = args.writer or writer

    out = args.out.resolve()
    out.mkdir(parents=True)
    process, agent = launch(args.cue, out, None, "none")
    try:
        start(agent, None)
        agent.frames(3600)
        agent.wait_halted(timeout=180)
        pad = PADS[args.region]
        run_steps(agent, ["press:0800", "600"], out, pad, WRITERS[args.region])
        agent.bpmode("halt")
        agent.breakpoints("write", [f"{p2:08X}-{p2:08X}"])
        for value, address in zip(args.ids, (p1, p2), strict=True):
            agent.onhit_write(writer, address, bytes([value]))
        agent.run()
        agent.wait_halted(timeout=300)
        agent.command("bp write")
        agent.step()
        agent.wait_halted()
        agent.onhit_clear()
        ids = agent.bus_read(p1, 1)[0], agent.bus_read(p2, 1)[0]
        agent.bpmode("log")
        agent.frames(args.frames)
        agent.wait_halted(timeout=180)
        (out / "scspram.bin").write_bytes(agent.read("scspram", 0, 0x80000))
        agent.screenshot(out / "fight.png")
        print(f"{out.name}: ids {ids}")
    finally:
        stop(process)


if __name__ == "__main__":
    main()
