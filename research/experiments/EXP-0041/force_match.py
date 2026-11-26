"""Force the US attract fight's fighters and log the loader and allocator.

From a retail title checkpoint, replay the first attract fight with no input.
Optional changes, each applied in emulator RAM only:

- ``--watch``: log writes to the two fighter ID bytes (discovery run).
- ``--ids P1 P2``: after the instruction at ``--force-pc`` writes the P2 ID,
  overwrite both one-based IDs.
- ``--setting``: the Appendix animation byte (0 = CUT, 1 = FULL).
- ``--branch-full``: replace the equality branch at ``0x0602192A`` with an
  unconditional branch, so ``FULL`` skips the reduced-set path for any pair.

Every allocator entry and exit is logged with its registers.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from struct import unpack

sys.path.insert(0, str(Path.cwd()))
from tools.mednafen.agent import Agent
from tools.mednafen.replay_state import BINARY, connect

SETTING = 0x06080A29
P1_ID = 0x06076FD7
P2_ID = 0x060773DB
POOLS = 0x06076AD8
BRANCH = 0x0602192A
LOADER = (0x0602190C, 0x06021928, 0x0602194C, 0x06021892, 0x060218BA)
ALLOCATOR = (
    0x06013E9C,  # bottom-up pool allocation entry (R4 size, R5 pool)
    0x06013EC0,  # its return (R6 address, 0 on failure)
    0x06013EC4,  # top-down pool allocation entry (R4 size, R5 pool)
    0x06013EE8,  # its success return (R0 address)
    0x06013EEE,  # its failure return
    0x06013F7C,  # VDP1 VRAM allocation entry (R4 size)
    0x06013F9E,  # VDP2 pool carve entry (R4 size)
    0x06013F1C,  # "Out Of Memory" after bottom-up search
    0x06013F68,  # "Out Of Memory" after top-down search
)


def wait_running(agent: Agent) -> None:
    deadline = time.monotonic() + 3
    while agent.halted():
        if time.monotonic() >= deadline:
            raise RuntimeError("Mednafen stayed halted after run")
        time.sleep(0.05)


def run(agent: Agent, args: argparse.Namespace, out: Path) -> None:
    agent.command("bp pc", "bp write", "onhit clear", "run")
    wait_running(agent)
    agent.command(f"loadstate {args.state.resolve()}", "pause")
    agent.wait_halted()
    agent.clear_events()
    agent.bus_write(SETTING, bytes([args.setting]))
    if args.watch:
        agent.bpmode("log")
        agent.breakpoints("write", [f"{P1_ID:08X}-{P1_ID:08X}", f"{P2_ID:08X}"])
        agent.frames(args.frames)
        agent.wait_halted(timeout=60)
        out.with_suffix(".log").write_text("\n".join(agent.events()) + "\n")
        return

    forced = ""
    if args.ids:
        # Halt on the game's P2 ID write; the queued writes follow it.
        agent.bpmode("halt")
        agent.breakpoints("write", [f"{P2_ID:08X}-{P2_ID:08X}"])
        for value, address in zip(args.ids, (P1_ID, P2_ID), strict=True):
            agent.onhit_write(args.force_pc, address, bytes([value]))
        agent.run()
        agent.wait_halted(timeout=60)
        hit = agent.events()[-1]
        if f" PC={args.force_pc:08X} " not in hit:
            raise RuntimeError(f"unexpected write hit: {hit[:80]}")
        agent.command("bp write")
        agent.step()
        agent.wait_halted()
        forced = f"ids-after-force {agent.bus_read(P1_ID, 1)[0]} "
        forced += str(agent.bus_read(P2_ID, 1)[0])
        print(f"{out.name}: {forced}")
        agent.onhit_clear()
    if args.branch_full:
        original = agent.bus_read(BRANCH, 2)
        if original != bytes.fromhex("890F"):
            raise RuntimeError(f"unexpected branch bytes {original.hex()}")
        agent.bus_write(BRANCH, bytes.fromhex("A00F"))

    # Halt at the loader entry to snapshot the pools before the fighters load.
    agent.bpmode("halt")
    agent.breakpoints("pc", [f"{LOADER[0]:08X}-{LOADER[0]:08X}"])
    agent.run()
    agent.wait_halted(timeout=60)
    before = unpack(">6I", agent.bus_read(POOLS, 24))
    ids = agent.bus_read(P1_ID, 1)[0], agent.bus_read(P2_ID, 1)[0]
    print(f"{out.name}: at loader, IDs {ids}, pools {[hex(p) for p in before]}")

    agent.bpmode("log")
    agent.breakpoints("pc", [f"{pc:08X}-{pc:08X}" for pc in LOADER + ALLOCATOR])
    agent.frames(args.frames)
    agent.wait_halted(timeout=60)
    agent.screenshot(out.with_suffix(".png"))
    after = unpack(">6I", agent.bus_read(POOLS, 24))
    events = agent.events()
    lines = [
        f"pools-before {' '.join(f'{p:08X}' for p in before)}",
        *([forced] if forced else []),
        f"ids-at-loader {ids[0]} {ids[1]}",
        *events,
        f"pools-after {' '.join(f'{p:08X}' for p in after)}",
    ]
    out.with_suffix(".log").write_text("\n".join(lines) + "\n")
    print(f"{out.name}: {len(events)} trace lines, pools {[hex(p) for p in after]}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cue", type=Path)
    parser.add_argument("state", type=Path)
    parser.add_argument("out", type=Path, help="new directory")
    parser.add_argument("--name", required=True)
    parser.add_argument("--setting", type=int, choices=(0, 1), default=0)
    parser.add_argument("--watch", action="store_true")
    parser.add_argument("--ids", type=int, nargs=2)
    parser.add_argument("--force-pc", type=lambda text: int(text, 16))
    parser.add_argument("--branch-full", action="store_true")
    parser.add_argument("--frames", type=int, default=1120)
    args = parser.parse_args()
    if args.ids and args.force_pc is None:
        parser.error("--ids needs --force-pc")

    out = args.out.resolve()
    out.mkdir(parents=True)
    home = out / "home"
    home.mkdir()
    source_home = Path("local/mednafen_quiet").resolve()
    shutil.copyfile(source_home / "mednafen.cfg", home / "mednafen.cfg")
    (home / "firmware").symlink_to(source_home / "firmware", target_is_directory=True)
    agent_dir = out / "agent"
    env = dict(os.environ, MEDNAFEN_HOME=str(home), MEDNAFEN_AGENT_DIR=str(agent_dir))
    command = [
        str(BINARY.resolve()),
        "-sound.volume",
        "0",
        "-ss.cart",
        "backup",
        str(args.cue.resolve()),
    ]
    with (out / "mednafen.log").open("wb") as log:
        process = subprocess.Popen(
            command, env=env, stdout=log, stderr=subprocess.STDOUT
        )
        try:
            run(connect(agent_dir), args, out / args.name)
        finally:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()


if __name__ == "__main__":
    main()
