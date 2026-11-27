"""Cold-boot JP Enhanced, checkpoint a win, then capture the new ending pages."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from struct import unpack

sys.path.insert(0, str(Path.cwd()))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "EXP-0042"))
from drive import launch, run_steps, start, stop  # type: ignore[import-not-found]

from tools.mednafen.agent import Agent

TABLE_LITERAL = 0x06036840
TABLES = (0x0605B1C0, 0x0605B1F8)
CHECKPOINT = "before-ending.mc0"


def quiet_home(out: Path) -> Path:
    home = out / "home"
    home.mkdir(parents=True)
    quiet = Path("local/mednafen_quiet").resolve()
    config = (quiet / "mednafen.cfg").read_text()
    config = config.replace("\nsound 1\n", "\nsound 0\n")
    config = config.replace("\nnothrottle 0\n", "\nnothrottle 1\n")
    (home / "mednafen.cfg").write_text(config)
    (home / "firmware").symlink_to(quiet / "firmware", target_is_directory=True)
    return home


def boot(cue: Path, out: Path) -> Path:
    process, agent = launch(cue, out, quiet_home(out), "backup", False)

    def run(*steps: str) -> None:
        run_steps(agent, steps, out, 0x06076AB6, 0x06013C74)

    def press(word: str, frames: int = 10) -> None:
        run(f"press:{word}", str(frames))

    try:
        start(agent, None)
        run("3600")
        press("0800", 120)
        press("0800", 30)
        press("2000")
        press("2000")
        press("0800", 90)
        for _ in range(3):
            if read(agent, 0x0608086C, 2) == 10:
                break
            press("1000")
        else:
            raise RuntimeError("EDITION row was not reached")
        press("4000")  # US Enhanced left to JP Enhanced
        run("read:menu-edition:060830C5:1", "shot:options")
        press("0800", 120)
        press("1000")
        press("1000")
        run("read:after-option:060830C5:1", "read:jp-table:06036840:4")
        assert read(agent, TABLE_LITERAL, 4) == TABLES[1]
        press("0800", 300)
        for _ in range(3):
            press("0400", 60)
        run("1200", "shot:round-1")
        run("write:0607706B:0101", "write:06080977:01", "850", "shot:round-2")
        run("write:0607706B:0101", "write:06080977:01", "240", "shot:ko")
        agent.run()
        checkpoint = out / CHECKPOINT
        agent.savestate(checkpoint)
        agent.pause()
        agent.wait_halted()
        if not checkpoint.is_file():
            raise RuntimeError("win checkpoint was not written")
        return checkpoint
    finally:
        stop(process)


def read(agent: Agent, addr: int, size: int) -> int:
    return int.from_bytes(agent.bus_read(addr, size), "big")


def capture_pages(agent: Agent, out: Path, roster: int, table: int) -> None:
    agent.bus_write(0x0608092B, b"\x09")
    agent.bus_write(0x06080980, bytes([roster]))
    agent.bus_write(0x0608096E, bytes([roster]))
    if table == TABLES[0]:
        agent.bus_write(TABLE_LITERAL, table.to_bytes(4, "big"))
    assert read(agent, TABLE_LITERAL, 4) == table
    addr = read(agent, table + (roster - 1) * 4, 4) + 2
    captures = []
    for _ in range(14):
        page, _, shown, hide, _, wait = unpack(">6H", agent.bus_read(addr, 12))
        assert hide == page | 0x8000
        if 0xA1 <= page <= 0xA6 or not wait:
            captures.append((page, addr, shown))
        if not wait:
            break
        addr += 12
    else:
        raise ValueError(f"unterminated script for roster {roster}")

    agent.bpmode("halt")
    for page, addr, shown in captures:
        agent.breakpoints("read", [f"{addr:08X}-{addr + 1:08X}"])
        before = int(agent.status()["hits"])
        agent.frames(12000)
        status = agent.wait_halted(240)
        if int(status["hits"]) != before + 1:
            raise RuntimeError(f"roster {roster} page {page:#x} did not load: {status}")
        agent.breakpoints("read")
        agent.frames(shown - 12)
        agent.wait_halted(240)
        assert read(agent, 0x06076462, 2) == page
        agent.screenshot(out / f"{roster:02x}-{table:08x}-{page:03x}.png")
        print(
            f"Roster {roster}, table {table:#x}, displayed page {page:#x}", flush=True
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cue", type=Path)
    parser.add_argument("out", type=Path)
    parser.add_argument("rosters", nargs="*", type=int)
    parser.add_argument("--checkpoint", type=Path)
    args = parser.parse_args()
    checkpoint = args.checkpoint or boot(args.cue, args.out / "boot")
    out = args.out / "pages"
    process, agent = launch(args.cue, out, quiet_home(out), "backup", False)
    try:
        for roster in args.rosters or (5, 8, 9, 11):
            for table in TABLES:
                start(agent, checkpoint)
                assert read(agent, 0x060830C5, 1) == 3
                capture_pages(agent, out, roster, table)
    finally:
        stop(process)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
