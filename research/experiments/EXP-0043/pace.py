"""ANI-003: does the cart-backed FULL fight run at the same game pace?

Two cold boots of the same image: no cart with the default setting (stock
CUT path), and a 4 MiB cart with ANIMATION set to FULL through the Appendix.
Both start Arcade with the default pick, wait for the first fight, then read
the round timer (``0x06080977``) at fixed frame intervals. A fight that lags
behind the emulated frame rate counts down more slowly.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from play import DRIVE, START, A, full_setup, press

TIMER = "06080977"


def fight(setup: list[str]) -> list[str]:
    steps = [*setup, *press(START, 300), *press(A, 60), *press(A, 60)]
    steps += [*press(A, 60), "1500", "read:slots:0609022C:2", "shot:fight"]
    for i in range(7):
        steps += [f"read:t{i}:{TIMER}:1", "300"]
    return steps


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cue", type=Path)
    parser.add_argument("out", type=Path, help="new directory")
    args = parser.parse_args()
    args.out.mkdir(parents=True)
    stock = ["3600", *press(START, 120), *press(START, 30)]  # cursor on ARCADE
    for name, cart, setup in (
        ("none-cut", "none", stock),
        ("4m-full", "extram4", full_setup()),
    ):
        command = [sys.executable, DRIVE, str(args.cue), str(args.out / name)]
        subprocess.run([*command, *fight(setup), "--cart", cart], check=True)


if __name__ == "__main__":
    main()
