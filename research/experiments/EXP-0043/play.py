"""ANI-003: drive Arcade and VS on the cart build with injected presses.

Every scenario starts from a cold boot with one fresh Mednafen home: title,
OPTION, APPENDIX, ANIMATION set to FULL, save. Rounds are ended by time-over:
the loser's vitality (P1 ``0x06076C67``, P2 ``0x0607706B``, two bytes each)
is set to 1 and the timer (``0x06080977``) to 1. After each round and
each load, the loaded-set slots (``0x0609022C``/``D``), fighter IDs and the
allocator pools are read, and a screenshot is taken.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

DRIVE = "research/experiments/EXP-0042/drive.py"
START, A, UP, DOWN, RIGHT = "0800", "0400", "1000", "2000", "8000"
P1_VIT, P2_VIT, TIMER = "06076C67", "0607706B", "06080977"


def press(button: str, wait: int = 10, pad: int = 1) -> list[str]:
    return [f"press{'2' if pad == 2 else ''}:{button}", str(wait)]


def state(name: str) -> list[str]:
    return [
        f"read:{name}-slots:0609022C:2",
        f"read:{name}-ids:06076FD7:1",
        f"read:{name}-id2:060773DB:1",
        f"read:{name}-pools:06076AD8:24",
        f"read:{name}-anim:06080A29:1",
        f"shot:{name}",
    ]


def full_setup() -> list[str]:
    steps = ["3600", *press(START, 120), *press(START, 30)]
    steps += [*press(DOWN), *press(DOWN), *press(START, 90)]
    for _ in range(9):
        steps += press(DOWN)
    steps += press(A, 60)
    for _ in range(6):
        steps += press(DOWN)
    steps += [*press(RIGHT), *press(START, 60), *press(START, 120)]
    return [*steps, *press(UP), *press(UP)]  # title menu cursor back to ARCADE


def round_end(winner: int, name: str, wait: int) -> list[str]:
    loser = P2_VIT if winner == 1 else P1_VIT
    steps = [str(wait), f"write:{loser}:0101", f"write:{TIMER}:01"]
    return [*steps, "420", *state(name)]


def arcade(stages: int, lose_at: int | None) -> list[str]:
    steps = [*full_setup(), *press(START, 300), *press(A, 60), *press(A, 60)]
    steps += [*press(A, 60), "1500", *state("stage1-start")]
    for stage in range(1, stages + 1):
        first = 0 if stage == 1 else 1200
        if stage == lose_at:
            steps += round_end(2, f"stage{stage}-r1-lost", first + 300)
            steps += round_end(2, f"stage{stage}-r2-lost", 600)
            # continue: Start on the continue screen, then the same pick
            steps += ["300", "shot:continue", *press(START, 900), "shot:reselect"]
            steps += [*press(A, 60), *press(A, 60), *press(A, 60), "1500"]
            steps += state(f"stage{stage}-rematch")
            first = 0
        steps += round_end(1, f"stage{stage}-r1", first + 300)
        steps += round_end(1, f"stage{stage}-r2", 600)
        steps += ["1500", *state(f"stage{stage + 1}-start")]
    return steps


def vs() -> list[str]:
    steps = [*full_setup(), *press(DOWN), *press(START, 300)]
    steps += ["shot:vs-select", *press(START, 60, pad=2), "shot:vs-joined"]
    steps += [*press(A, 60), *press(A, 60, pad=2)]
    steps += [*press(A, 60), *press(A, 60, pad=2)]
    steps += [*press(A, 60), *press(A, 60, pad=2), "1500", *state("vs1-start")]
    steps += round_end(1, "vs1-r1", 300)
    steps += round_end(2, "vs1-r2", 600)
    steps += round_end(1, "vs1-r3", 600)
    return [*steps, "1500", *state("vs-after")]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cue", type=Path)
    parser.add_argument("out", type=Path, help="new directory")
    parser.add_argument("scenario", choices=("arcade", "vs"))
    parser.add_argument("--stages", type=int, default=3)
    parser.add_argument("--lose-at", type=int)
    parser.add_argument("--cart", default="extram4")
    args = parser.parse_args()
    steps = arcade(args.stages, args.lose_at) if args.scenario == "arcade" else vs()
    command = [sys.executable, DRIVE, str(args.cue), str(args.out), *steps]
    subprocess.run([*command, "--cart", args.cart], check=True)


if __name__ == "__main__":
    main()
