"""EXP-0013: log every write to given WRAM-H bytes from power-on.

    ./invenv.sh python research/experiments/EXP-0013/boot_watch.py {jp,us} OUT_DIR \
        RANGE [RANGE ...] [--frames 2400]

Boots the release in the patched Mednafen (quiet home, no state loaded),
pauses as soon as the agent answers, arms write breakpoints on each RANGE
(``06080898-0608089B``) in log mode, runs FRAMES frames with no input, and
saves the hits (``events.log``), a screenshot, and WRAM-H. Outputs stay
under the ignored OUT_DIR.
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
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "EXP-0010"))
from force import BINARY, HOME, IMAGES

from tools.mednafen.agent import Agent, AgentError


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("release", choices=sorted(IMAGES))
    p.add_argument("out", type=Path)
    p.add_argument("ranges", nargs="+")
    p.add_argument("--frames", type=int, default=2400)
    a = p.parse_args()
    a.out.mkdir(parents=True, exist_ok=False)
    agent_dir = (a.out / "agent").resolve()
    env = {
        **os.environ,
        "MEDNAFEN_HOME": str(HOME.resolve()),
        "MEDNAFEN_AGENT_DIR": str(agent_dir),
    }
    for stale in (HOME / "sav").glob("*"):
        stale.unlink()
    record: dict[str, object] = {
        "release": a.release,
        "ranges": a.ranges,
        "frames": a.frames,
    }
    with (a.out / "mednafen.log").open("wb") as log:
        proc = subprocess.Popen(
            [str(BINARY), str(IMAGES[a.release])],
            env=env,
            stdout=log,
            stderr=subprocess.STDOUT,
        )
        try:
            agent = Agent(agent_dir, timeout=20.0)
            deadline = time.monotonic() + 30
            while True:
                try:
                    agent.pause()
                    break
                except AgentError:
                    if time.monotonic() > deadline:
                        raise
                    time.sleep(0.05)
            record["armed_frame"] = int(agent.status()["frame"])
            agent.bpmode("log")
            agent.breakpoints("write", a.ranges)
            agent.frames(a.frames)
            agent.wait_halted(600.0)
            record["end"] = agent.status()
            agent.screenshot(a.out / "end.png")
            (a.out / "workramh.bin").write_bytes(agent.read("workramh", 0, 0x100000))
        finally:
            proc.send_signal(signal.SIGTERM)
            record["exit_code"] = proc.wait(timeout=30)
    hits = (
        [line for line in (agent_dir / "events.log").read_text().splitlines()]
        if (agent_dir / "events.log").exists()
        else []
    )
    record["hits"] = len(hits)
    (a.out / "run.json").write_text(json.dumps(record, indent=1) + "\n")
    print(json.dumps(record, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
