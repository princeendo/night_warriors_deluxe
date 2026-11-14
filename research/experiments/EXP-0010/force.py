"""EXP-0010: load a state, write bytes into WRAM-H, run, and take screenshots.

Run from the repository root:

    ./invenv.sh python research/experiments/EXP-0010/force.py {jp,us} STATE OUT_DIR \
        [--write 0608097B=09 ...] [--steps 120] [--step-frames 30] [--wav]
        [--onhit 0601D4A2:06076ABE=00 ...] [--log-pc 0601D4EC ...]
        [--setting ss.input.port1=none ...] [--image build/.../x.cue]

Launches the patched Mednafen (D-005) in the quiet home, loads STATE, pauses,
applies each ``--write ADDRESS=HEXBYTES`` to WRAM-H (address 0x06000000-
0x060FFFFF), runs, and saves a screenshot every ``--step-frames`` frames for
``--steps`` steps, plus a state every 10 steps (kept as checkpoints).
``--wav`` also records the sound. ``--onhit PC:ADDRESS=HEXBYTES`` (EXP-0016)
arms a PC breakpoint in log mode and applies the write each time PC has
executed; ``--log-pc`` logs hits (registers) at PC; ``--setting NAME=VALUE``
passes ``-NAME VALUE`` to Mednafen. No input is sent. Outputs stay under the
ignored OUT_DIR.
"""

from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
from tools.mednafen.agent import Agent, AgentError

BINARY = Path("vendor/mednafen/build-agent/src/mednafen")
HOME = Path("local/mednafen_quiet")
IMAGES = {
    "jp": Path(
        "local/disc_images/vh_saturn_jp_1m/"
        "Vampire Hunter - Darkstalkers' Revenge (Japan) (1M).cue"
    ),
    "us": Path(
        "local/disc_images/nw_saturn_us/"
        "Night Warriors - Darkstalkers' Revenge (USA).cue"
    ),
}


def parse_write(text: str) -> tuple[int, bytes]:
    address, data = text.split("=", 1)
    offset = int(address, 16) - 0x06000000
    if not 0 <= offset < 0x100000:
        raise ValueError(f"not a WRAM-H address: {address}")
    return offset, bytes.fromhex(data)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("release", choices=sorted(IMAGES))
    parser.add_argument("state", type=Path)
    parser.add_argument("out", type=Path)
    parser.add_argument("--write", action="append", default=[], type=parse_write)
    parser.add_argument("--steps", type=int, default=120)
    parser.add_argument("--step-frames", type=int, default=30)
    parser.add_argument("--wav", action="store_true")
    parser.add_argument(
        "--halt-pc", help="stop at the first hit, e.g. 06038166-06038166"
    )
    parser.add_argument("--onhit", action="append", default=[])
    parser.add_argument("--log-pc", action="append", default=[])
    parser.add_argument("--setting", action="append", default=[])
    parser.add_argument("--image", type=Path, help="a .cue instead of the release's")
    args = parser.parse_args()
    out: Path = args.out
    (out / "shots").mkdir(parents=True, exist_ok=False)
    (out / "states").mkdir()
    agent_dir = (out / "agent").resolve()
    env = {
        **os.environ,
        "MEDNAFEN_HOME": str(HOME.resolve()),
        "MEDNAFEN_AGENT_DIR": str(agent_dir),
    }
    for stale in (HOME / "sav").glob("*"):
        stale.unlink()
    command = [str(BINARY)]
    if args.wav:
        command += ["-soundrecord", str((out / "sound.wav").resolve())]
    for setting in args.setting:
        name, value = setting.split("=", 1)
        command += [f"-{name}", value]
    command.append(str(args.image or IMAGES[args.release]))
    # Mednafen saves command-line settings into its config on exit; restore it.
    config = HOME / "mednafen.cfg"
    saved_config = config.read_bytes()
    record: dict[str, object] = {
        "release": args.release,
        "image": str(args.image or IMAGES[args.release]),
        "state": str(args.state),
        "writes": [[hex(0x06000000 + o), d.hex()] for o, d in args.write],
        "onhit": args.onhit,
        "log_pc": args.log_pc,
        "settings": args.setting,
    }
    with (out / "mednafen.log").open("wb") as log:
        process = subprocess.Popen(
            command, env=env, stdout=log, stderr=subprocess.STDOUT
        )
        try:
            agent = Agent(agent_dir, timeout=20.0)
            deadline = time.monotonic() + 30
            while True:
                try:
                    agent.status()
                    break
                except AgentError:
                    if time.monotonic() > deadline:
                        raise
                    time.sleep(0.5)
            agent.loadstate(args.state)
            agent.pause()
            for offset, data in args.write:
                agent.write("workramh", offset, data)
            first = int(agent.status()["frame"])
            record["start_frame"] = first
            if args.halt_pc:
                agent.bpmode("halt")
                agent.breakpoints("pc", [args.halt_pc])
            elif args.onhit or args.log_pc:
                agent.bpmode("log")
                pcs = [spec.split(":")[0] for spec in args.onhit] + args.log_pc
                agent.breakpoints("pc", [f"{pc}-{pc}" for pc in pcs])
                for spec in args.onhit:
                    pc, write = spec.split(":")
                    address, data = write.split("=")
                    agent.onhit_write(
                        int(pc, 16), int(address, 16), bytes.fromhex(data)
                    )
            for step in range(args.steps):
                agent.frames(args.step_frames)
                status = agent.wait_halted(30.0)
                rel = int(status["frame"]) - first
                agent.screenshot(out / "shots" / f"r{rel:06d}.png")
                if args.halt_pc and int(status["hits"]) > 0:
                    # Halted on the PC breakpoint, not on the frame count.
                    regs = agent.regs()
                    sp = regs["R15"] - 0x06000000
                    record["halt"] = {
                        "frame": rel,
                        "regs": {k: f"{v:08X}" for k, v in regs.items()},
                        "stack": agent.read("workramh", sp, 64).hex(),
                        "events": agent.events()[-3:],
                    }
                    break
                if step % 10 == 9:
                    agent.run()
                    for _ in range(20):  # the halt clears on the next frame
                        try:
                            agent.savestate(out / "states" / f"r{rel:06d}.mc0")
                            break
                        except AgentError:
                            time.sleep(0.02)
                    agent.pause()
            record["end"] = agent.status()
        finally:
            process.send_signal(signal.SIGTERM)
            record["exit_code"] = process.wait(timeout=30)
            config.write_bytes(saved_config)
    (out / "run.json").write_text(json.dumps(record, indent=1) + "\n")
    print(json.dumps(record, indent=1))
    return 0


if __name__ == "__main__":
    assert parse_write("0608097B=09") == (0x8097B, b"\x09")
    raise SystemExit(main())
