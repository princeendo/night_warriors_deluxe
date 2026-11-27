"""Exercise the names preference, edition isolation and a saved HUD change."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "EXP-0042"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "EXP-0046"))
from check_endings import quiet_home, read  # type: ignore[import-not-found]
from drive import launch, run_steps, start, stop  # type: ignore[import-not-found]

from tools.mednafen.agent import Agent

START, A, UP, DOWN, LEFT, RIGHT = "0800", "0400", "1000", "2000", "4000", "8000"
STATE = "read:settings:060830C5:4"


def press(word: str, frames: int = 10) -> list[str]:
    return [f"press:{word}", str(frames)]


def option() -> list[str]:
    return [
        "3600",
        *press(START, 120),
        *press(START, 30),
        *press(DOWN),
        *press(DOWN),
        *press(START, 90),
    ]


def verify(agent: Agent, edition: int, preference: int, name_flag: int) -> None:
    assert read(agent, 0x060830C5, 1) == edition
    assert read(agent, 0x060830C7, 1) == preference
    assert read(agent, 0x060830C8, 1) == name_flag
    assert read(agent, 0x0608089A, 1) == (0 if edition >= 2 else 2)
    assert read(agent, 0x06080882, 1) == (0 if edition >= 2 else 1)


def check(cue: Path, root: Path, reboot: bool = False) -> None:
    out = root / ("reboot" if reboot else "fresh")
    out.mkdir()
    process, agent = launch(cue, out, root / "home", "backup", False)

    def run(*steps: str) -> None:
        run_steps(agent, steps, out, 0x06076AB6, 0x06013C74)

    try:
        start(agent, None)
        run(*option(), *press(UP), STATE)
        assert read(agent, 0x0608086C, 2) == 11
        if reboot:
            verify(agent, 0, 2, 0)
            run(
                "shot:saved-option-a",
                "16",
                "shot:saved-option-b",
                "16",
                "shot:saved-option-c",
                "16",
                "shot:saved-option-d",
                *press(START, 120),
                *press(UP),
                *press(UP),
                *press(START, 300),
                "shot:select",
                *press(A, 60),
                *press(A, 60),
                *press(A, 60),
                "1200",
                "read:p1-fighter:06076FD7:1",
                "shot:fight",
                "write:0607706B:0101",
                "write:06080977:01",
                "850",
                "write:0607706B:0101",
                "write:06080977:01",
            )
            agent.bpmode("halt")
            agent.breakpoints("pc", ["0603798E-0603798E"])
            agent.frames(1600)
            status = agent.wait_halted(200)
            assert status["pc"] == "0603798E", status
            agent.breakpoints("pc")
            run("110", "shot:win")
            verify(agent, 0, 2, 0)
            return
        verify(agent, 0, 0, 2)
        run("shot:default", *press(LEFT), "shot:jp-names", STATE)
        verify(agent, 0, 2, 0)
        run(*press(UP), *press(RIGHT), *press(DOWN), *press(LEFT), STATE)
        verify(agent, 1, 2, 2)
        run("shot:original-locked", *press(UP), *press(RIGHT), STATE)
        verify(agent, 2, 2, 0)
        run(*press(RIGHT), *press(DOWN), *press(RIGHT), *press(RIGHT), STATE)
        verify(agent, 3, 1, 2)
        run("shot:jp-enhanced-us-names")
        run(*press(UP), *press(RIGHT), *press(DOWN), *press(RIGHT), STATE)
        verify(agent, 0, 2, 0)
        run(*press(START, 240))
    finally:
        stop(process)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cue", type=Path)
    parser.add_argument("out", type=Path)
    parser.add_argument("--saved-home", type=Path)
    args = parser.parse_args()
    if args.saved_home:
        args.out.mkdir(parents=True)
        (args.out / "home").symlink_to(
            args.saved_home.resolve(), target_is_directory=True
        )
    else:
        quiet_home(args.out)
        check(args.cue, args.out)
    check(args.cue, args.out, reboot=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
