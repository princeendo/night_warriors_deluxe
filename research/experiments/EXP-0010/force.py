"""EXP-0010: load a state, write bytes into WRAM-H, run, and take screenshots.

Run from the repository root:

    ./invenv.sh python research/experiments/EXP-0010/force.py {jp,us} STATE OUT_DIR \
        [--write 0608097B=09 ...] [--steps 120] [--step-frames 30] [--wav]

Launches the patched Mednafen (D-005) in the quiet home, loads STATE, pauses,
applies each ``--write ADDRESS=HEXBYTES`` to WRAM-H (address 0x06000000-
0x060FFFFF), runs, and saves a screenshot every ``--step-frames`` frames for
``--steps`` steps, plus a state every 10 steps (kept as checkpoints).
``--wav`` also records the sound. No input is sent. Outputs stay under the
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
    command.append(str(IMAGES[args.release]))
    record: dict[str, object] = {
        "release": args.release,
        "state": str(args.state),
        "writes": [[hex(0x06000000 + o), d.hex()] for o, d in args.write],
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
            for step in range(args.steps):
                agent.frames(args.step_frames)
                status = agent.wait_halted(30.0)
                rel = int(status["frame"]) - first
                agent.screenshot(out / "shots" / f"r{rel:06d}.png")
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
    (out / "run.json").write_text(json.dumps(record, indent=1) + "\n")
    print(json.dumps(record, indent=1))
    return 0


if __name__ == "__main__":
    assert parse_write("0608097B=09") == (0x8097B, b"\x09")
    raise SystemExit(main())
