"""Capture matching retail ending and cast surfaces from each Arcade checkpoint."""

from __future__ import annotations

import argparse
from pathlib import Path

from retail_run import frames, launch, quiet_home, start, stop, until


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("region", choices=("jp", "us"))
    parser.add_argument("cue", type=Path)
    parser.add_argument("checkpoint", type=Path)
    parser.add_argument("out", type=Path)
    parser.add_argument("--main-only", action="store_true")
    args = parser.parse_args()
    japanese = args.region == "jp"
    shift = 0x50 if japanese else 0
    ending = 0x0603701E if japanese else 0x060367C6
    page = 0x0603704E if japanese else 0x060367F6
    cast = 0x06044EE4 if japanese else 0x0604468C
    process, agent = launch(args.cue, args.out, quiet_home(args.out), "none", False)
    try:
        start(agent, args.checkpoint)
        agent.bus_write(0x0607706B + shift, bytes.fromhex("0101"))
        agent.bus_write(0x06080977 + shift, b"\x01")
        frames(agent, 240)
        agent.bus_write(0x0608092B + shift, b"\x09")
        until(agent, ending, 3200)
        until(agent, page, 1500)
        frames(agent, 110)
        agent.screenshot(args.out / "ending.png")
        if args.main_only:
            return 0
        until(agent, 0x0600CFCC, 10000)
        frames(agent, 680)
        agent.screenshot(args.out / "epilogue.png")
        until(agent, cast, 12000)
        frames(agent, 90)
        agent.screenshot(args.out / "cast-first.png")
        until(agent, cast, 1700)
        frames(agent, 90)
        agent.screenshot(args.out / "cast-second.png")
    finally:
        stop(process)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
