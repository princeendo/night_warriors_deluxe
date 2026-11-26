"""AUD-004: run a battery of motions in a forced VS match and list shared sounds.

For each run, ``vsmove.py`` plays the motions on one pad (the other player
idle) and traces the shared-sound path (``0x0603A1D6``, record pointer in
R13) and the sequence start (``0x0603B270``, bank in R5, song in R6). The
summary lists every shared-sound request: frame, type g (record byte 4), the
owners of g in the table at ``0x0606C10C``, and the bank and song played.

    ./invenv.sh python research/experiments/EXP-0044/battery.py run CUE OUT \
        --ids 6 12 --pad 2
    ./invenv.sh python research/experiments/EXP-0044/battery.py summary OUT
"""

from __future__ import annotations

import argparse
import re
import struct
import subprocess
import sys
from pathlib import Path

VSMOVE = "research/experiments/EXP-0044/vsmove.py"
MAIN = Path("local/extracted/saturn_us/MAIN.BIN")
MAIN_BASE, TABLE = 0x06012000, 0x0606C10C
NAMES = ["Demitri", "Jon", "Victor", "Raptor", "Morrigan", "Anakaris", "Felicia"]
NAMES += ["Bishamon", "Rikuo", "Sasquatch", "Huitzil", "Pyron", "Hsien-Ko", "Donovan"]
FIELD = re.compile(r" (PC|R5|R6|R13)=([0-9A-F]{8})")


def battery(pad: int) -> list[str]:
    fwd, back = (0x4000, 0x8000) if pad == 2 else (0x8000, 0x4000)
    down, up = 0x2000, 0x1000
    lp, mp, hp, lk, mk = 0x0040, 0x0020, 0x0010, 0x0400, 0x0100
    moves = []
    for button in (lp, mp, hp, lk, mk):  # quarter circle forward
        moves.append([down, down | fwd, fwd, fwd | button])
    for button in (mp, mk):  # quarter circle back
        moves.append([down, down | back, back, back | button])
    for button in (mp, mk):  # dragon punch
        moves.append([fwd, 0, down, down | fwd | button])
    scripts = []
    for steps in moves:
        script = ",".join(f"{word:04X}x4" for word in steps[:-1])
        scripts.append(f"{pad}:{script},{steps[-1]:04X}x4,0000x2,wait:100")
    scripts.append(f"{pad}:{back:04X}x45,{fwd | mp:04X}x4,0000x2,wait:100")
    scripts.append(f"{pad}:{down:04X}x45,{up | mk:04X}x4,0000x2,wait:100")
    scripts.append(f"{pad}:{fwd:04X}x3,0000x3,{fwd:04X}x10,0000x2,wait:100")
    return scripts


def owners(g: int) -> str:
    data = MAIN.read_bytes()
    (pointer,) = struct.unpack_from(">I", data, TABLE - MAIN_BASE + 4 * g)
    o = pointer - MAIN_BASE
    return ",".join(NAMES[i] for i in range(14) if data[o + 2 * i])


def summary(out: Path) -> list[str]:
    data = MAIN.read_bytes()
    lines, pending = [], None
    for line in (out / "events.log").read_text().splitlines():
        if not line.startswith("hit "):
            continue
        frame = line.split()[2].split("=")[1]
        regs = dict(FIELD.findall(line))
        pc = int(regs["PC"], 16)
        if pc == 0x0603A1D6:
            record = int(regs["R13"], 16)
            pending = (frame, data[record - MAIN_BASE + 4])
        elif pc == 0x0603B270 and pending:
            frame0, g = pending
            bank, song = int(regs["R5"], 16), int(regs["R6"], 16)
            lines.append(
                f"{frame0} g={g:2d} owners={owners(g)} bank={bank} song={song}"
            )
            pending = None
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run")
    run.add_argument("cue", type=Path)
    run.add_argument("out", type=Path)
    run.add_argument("--ids", type=int, nargs=2, required=True)
    run.add_argument("--pad", type=int, choices=(1, 2), default=2)
    run.add_argument("--patch", nargs="*", default=[], help="passed to vsmove.py")
    show = sub.add_parser("summary")
    show.add_argument("out", type=Path)
    args = parser.parse_args()
    if args.command == "run":
        command = [sys.executable, VSMOVE, str(args.cue), str(args.out)]
        command += ["--ids", *map(str, args.ids), "--fight-wait", "2400"]
        command += ["--trace", "0603A1D6", "0603B270"]
        if args.patch:
            command += ["--patch", *args.patch]
        command += ["--moves", *battery(args.pad)]
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL)
    out_lines = summary(args.out)
    (args.out / "shared.txt").write_text("\n".join(out_lines) + "\n")
    print("\n".join(out_lines))


if __name__ == "__main__":
    main()
