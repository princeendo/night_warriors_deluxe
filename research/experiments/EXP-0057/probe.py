"""Create a cart-free VS checkpoint and trace one Demitri fireball."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

EXPERIMENTS = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(EXPERIMENTS / name) for name in ("EXP-0042", "EXP-0044")]
from drive import PADS, WRITERS, launch, run_steps, start, stop, wait_running  # noqa: E402
from vsmove import hold  # noqa: E402

from tools.mednafen.agent import Agent  # noqa: E402

P1 = 0x06076C66
P2 = 0x0607706A
TIMER = 0x06080977
WRITER = WRITERS["us"]
PAD = PADS["us"]
FIREBALL = "2000x4,A000x4,8000x2,8020x4,0000x2"


def prepare(agent: Agent, out: Path) -> None:
    title = ["3600", "press:0800", "120", "press:0800", "30"]
    vs = ["press:2000", "10", "press:0800", "120", "press2:0800", "60"]
    picks = ["press:0400", "60", "press2:0400", "60"] * 3
    picks += ["press:0400", "60"] * 3
    run_steps(agent, title + vs + picks, out, PAD, WRITER)
    # EXP-0044 established that this is after the picks and before the load.
    agent.bus_write(0x06076FD7, b"\x01")
    agent.bus_write(0x060773DB, b"\x03")
    run_steps(agent, ["1200", "shot:checkpoint"], out, PAD, WRITER)
    agent.run()
    wait_running(agent)
    agent.savestate(out / "vs.mc0")
    agent.pause()
    agent.wait_halted()


def sample(agent: Agent, out: Path, name: str) -> None:
    steps = [f"read:{name}-p1:{P1:08X}:2", f"read:{name}-p2:{P2:08X}:2"]
    steps += [
        f"read:{name}-p2-state:{P2 - 0x41:08X}:1",
        f"read:{name}-timer:{TIMER:08X}:1",
        f"read:{name}-knockout:06080981:2",
        f"shot:{name}",
    ]
    run_steps(agent, steps, out, PAD, WRITER)


def trial(
    agent: Agent, out: Path, low_vitality: bool, patch: tuple[int, bytes] | None
) -> None:
    run_steps(agent, ["1"], out, PAD, WRITER)  # render the loaded checkpoint
    sample(agent, out, "before")
    run_steps(
        agent,
        ["read:animation:06080A29:1", "read:fighter-assets:0609022C:2"],
        out,
        PAD,
        WRITER,
    )
    if low_vitality:
        agent.bus_write(P2, b"\x00\x01")
    if patch is not None:
        pc, data = patch
        original = agent.bus_read(pc, len(data))
        (out / "patch.txt").write_text(f"{pc:08X} {original.hex()} -> {data.hex()}\n")
        agent.bus_write(pc, data)
    sample(agent, out, "start")
    watch = [f"{P2 - 8:08X}-{P2 + 4:08X}"]
    agent.clear_events()
    agent.breakpoints("write", watch)
    for shot in (1, 2):
        hold(agent, PAD, WRITER, FIREBALL, [], watch)
        for elapsed, advance in ((20, 20), (40, 20), (90, 50), (180, 90)):
            run_steps(agent, [str(advance)], out, PAD, WRITER)
            sample(agent, out, f"hit{shot}-after-{elapsed}")
    agent.breakpoints("write")
    (out / "events.log").write_text("\n".join(agent.events()) + "\n")


def parse_patch(text: str) -> tuple[int, bytes]:
    address, data = text.split(":", maxsplit=1)
    return int(address, 16), bytes.fromhex(data)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cue", type=Path)
    parser.add_argument("out", type=Path)
    parser.add_argument("--state", type=Path, help="reuse a checkpoint from this image")
    parser.add_argument("--home", type=Path, help="optional isolated Mednafen home")
    parser.add_argument("--low-vitality", action="store_true")
    parser.add_argument("--patch", type=parse_patch, metavar="ADDRESS:HEX")
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True)
    process, agent = launch(args.cue, out, args.home, "none")
    try:
        start(agent, args.state)
        if args.state is None:
            prepare(agent, out)
            start(agent, out / "vs.mc0")
        trial(agent, out, args.low_vitality, args.patch)
    finally:
        stop(process)


if __name__ == "__main__":
    main()
