"""APP-001: enter the Appendix code, change settings, save, reboot and check.

Two cold boots per image with one fresh Mednafen home (empty backup memory):

1. Title -> OPTION MODE -> CONFIGURATION, enter B X Down A Y, check the unlock
   byte and the cursor range, change EDITION (Deluxe only), open APPENDIX,
   set the animation line to FULL, leave with Start, save with Start.
2. Cold boot again with the same home: OPTION MODE, then APPENDIX, and read
   the same bytes.

Every step is a ``drive.py`` step; screenshots and ``reads.txt`` go to the
run folders.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

DRIVE = "research/experiments/EXP-0042/drive.py"
START, A, B, X, Y = "0800", "0400", "0100", "0040", "0020"
UP, DOWN, RIGHT = "1000", "2000", "8000"


def addresses(region: str) -> dict[str, int]:
    shift = 0x50 if region == "jp" else 0
    return {
        "mode": 0x06080864 + shift,
        "cursor": 0x0608086C + shift,
        "appcursor": 0x06080870 + shift,
        "unlock": 0x06080A2B + shift,
        "code2": 0x06080A2A + shift,
        "animation": 0x06080A29 + shift,
    }


def reads(region: str, *names: str) -> list[str]:
    table = addresses(region)
    out = []
    for name in names:
        size = 2 if name in ("mode", "cursor", "appcursor") else 1
        out.append(f"read:{name}:{table[name]:08X}:{size}")
    return out


def press(button: str, wait: int = 10) -> list[str]:
    return [f"press:{button}", str(wait)]


def to_option(region: str) -> list[str]:
    steps = ["3900", *press(START, 120), *press(START, 30)]
    steps += [*press(DOWN), *press(DOWN), *press(START, 90)]
    return [*steps, *reads(region, "mode", "cursor", "unlock", "animation")]


def first_boot(region: str, deluxe: bool) -> list[str]:
    steps = [*to_option(region), "shot:01-option-locked"]
    for _ in range(8):
        steps += press(DOWN)
    steps += [*reads(region, "cursor"), "shot:02-configuration"]
    for button in (B, X, DOWN, A):
        steps += press(button, 4)
    steps += [*press(Y, 30), *reads(region, "unlock", "code2", "cursor")]
    steps += ["shot:03-unlocked", *press(DOWN), *reads(region, "cursor")]
    steps += ["shot:04-appendix-line", *press(DOWN), *reads(region, "cursor")]
    steps.append("shot:05-line-after-appendix")
    if deluxe:
        steps += [*press(RIGHT), "read:edition:060830C5:1", "shot:06-edition"]
    steps += [*press(UP), *reads(region, "cursor")]
    steps += [*press(A, 60), *reads(region, "mode", "appcursor"), "shot:07-appendix"]
    for _ in range(6):
        steps += press(DOWN)
    steps += [*reads(region, "appcursor", "animation"), *press(RIGHT)]
    steps += [*reads(region, "animation"), "shot:08-appendix-full"]
    steps += [*press(START, 60), *reads(region, "mode"), "shot:09-option-again"]
    steps += [*press(START, 120), *reads(region, "mode", "unlock", "animation")]
    if deluxe:
        steps.append("read:edition:060830C5:1")
    return [*steps, "shot:10-after-save", "300"]


def first_boot_unlocked(region: str) -> list[str]:
    """Deluxe with the Appendix unlocked by default: no code is entered."""
    steps = [*to_option(region), "shot:01-option-a", "20", "shot:01-option-b"]
    steps += ["20", "shot:01-option-c"]
    for _ in range(9):
        steps += press(DOWN)
    steps += [*reads(region, "cursor"), "shot:04-appendix-line", *press(DOWN)]
    steps += [*reads(region, "cursor"), *press(RIGHT), "read:edition:060830C5:1"]
    steps += ["shot:06-edition", *press(DOWN), *reads(region, "cursor")]
    steps += [*press(UP), *press(UP), *reads(region, "cursor")]
    steps += [*press(A, 60), *reads(region, "mode", "appcursor"), "shot:07-appendix"]
    for _ in range(6):
        steps += press(DOWN)
    steps += [*reads(region, "appcursor", "animation"), *press(RIGHT)]
    steps += [*reads(region, "animation"), "shot:08-appendix-full"]
    steps += [*press(START, 60), *reads(region, "mode"), "shot:09-option-again"]
    steps += [*press(START, 120), *reads(region, "mode", "unlock", "animation")]
    return [*steps, "read:edition:060830C5:1", "shot:10-after-save", "300"]


def second_boot(region: str, deluxe: bool) -> list[str]:
    steps = [*to_option(region), "shot:11-option-reboot"]
    if deluxe:
        steps.append("read:edition:060830C5:1")
    for _ in range(9):
        steps += press(DOWN)
    steps += [*reads(region, "cursor"), *press(A, 60)]
    for _ in range(6):
        steps += press(DOWN)
    return [*steps, *reads(region, "mode", "animation"), "shot:12-appendix-reboot"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cue", type=Path)
    parser.add_argument("out", type=Path, help="new directory")
    parser.add_argument("--region", choices=("us", "jp"), default="us")
    parser.add_argument("--deluxe", action="store_true")
    parser.add_argument("--cart", default="none")
    parser.add_argument(
        "--unlocked-default",
        action="store_true",
        help="image unlocks the Appendix itself (no code entered)",
    )
    args = parser.parse_args()
    args.out.mkdir(parents=True)
    home = args.out / "home"
    for name, steps in (
        (
            "boot1",
            first_boot_unlocked(args.region)
            if args.unlocked_default
            else first_boot(args.region, args.deluxe),
        ),
        ("boot2", second_boot(args.region, args.deluxe)),
    ):
        command = [sys.executable, DRIVE, str(args.cue), str(args.out / name)]
        command += [*steps, "--region", args.region, "--cart", args.cart]
        subprocess.run([*command, "--home", str(home)], check=True)


if __name__ == "__main__":
    main()
