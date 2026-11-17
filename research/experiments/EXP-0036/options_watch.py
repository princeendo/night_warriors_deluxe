"""EXP-0036: find the options screen's code with a write watch while the user plays.

    ./invenv.sh python research/experiments/EXP-0036/options_watch.py \
        OUT_DIR [CUE [RANGE...]]

Starts the agent Mednafen in the interactive home (the user's pad) on CUE
(default: the stock US image), sets a log-mode write watch on the first
settings variables the unpack routine fills and on the settings block's
option bytes, logs the load-and-unpack and pack routines (EXP-0036), and
takes a screenshot and a save state each second, and waits for the user to
close the window. RANGEs (``LO-HI``, hex; EXP-0037) replace the default
watch and are watched for reads too; ``pc:ADDR`` arguments (EXP-0039)
replace the logged PCs. Every write is logged with its PC in
``OUT_DIR/agent/events.log``. Nothing is pressed for the user.
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
from tools.mednafen.agent import Agent, AgentError

BINARY = Path("vendor/mednafen/build-agent/src/mednafen")
CUE = Path(
    "local/disc_images/nw_saturn_us/Night Warriors - Darkstalkers' Revenge (USA).cue"
)
WATCH = [
    "0608089F-0608089F",
    "0608089E-0608089E",
    "06080881-06080881",
    "06080886-06080886",
    "060830B8-060830C4",  # the settings block's option bytes (second session)
]
PCS = ["06014718-06014718", "060148C4-060148C4"]  # load-and-unpack, pack


def main() -> int:
    out = Path(sys.argv[1])
    cue = Path(sys.argv[2]) if len(sys.argv) > 2 else CUE
    extra = sys.argv[3:]
    pcs = [f"{a[3:]}-{a[3:]}" for a in extra if a.startswith("pc:")]
    ranges = [a for a in extra if not a.startswith("pc:")] or (WATCH if not pcs else [])
    out.mkdir(parents=True)
    env = dict(
        os.environ,
        MEDNAFEN_HOME=str(Path("local/mednafen").resolve()),
        MEDNAFEN_AGENT_DIR=str((out / "agent").resolve()),
    )
    with (out / "mednafen.log").open("wb") as log:
        proc = subprocess.Popen(
            [str(BINARY), str(cue)], env=env, stdout=log, stderr=subprocess.STDOUT
        )
        agent = Agent((out / "agent").resolve(), 5)
        for _ in range(60):
            try:
                agent.status()
                break
            except AgentError:
                time.sleep(0.5)
        agent.bpmode("log")
        if ranges:
            agent.breakpoints("write", ranges)
        if ranges and extra:
            agent.breakpoints("read", ranges)
        agent.breakpoints("pc", pcs or PCS)
        print(time.strftime("%H:%M:%S"), "watching", ranges, flush=True)
        for d in ("shots", "states"):
            (out / d).mkdir()
        n = 0
        while proc.poll() is None:  # a screenshot and a state each second
            try:
                agent.screenshot((out / "shots" / f"{n:04d}.png").resolve())
                agent.savestate((out / "states" / f"{n:04d}.mcs").resolve())
            except AgentError:
                pass
            n += 1
            time.sleep(1)
    print(time.strftime("%H:%M:%S"), "closed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
