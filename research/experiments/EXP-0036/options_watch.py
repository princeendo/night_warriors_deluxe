"""EXP-0036: find the options screen's code with a write watch while the user plays.

    ./invenv.sh python research/experiments/EXP-0036/options_watch.py OUT_DIR [CUE]

Starts the agent Mednafen in the interactive home (the user's pad) on CUE
(default: the stock US image), sets a log-mode write watch on the first
settings variables the unpack routine fills and on the settings block's
option bytes, logs the load-and-unpack and pack routines (EXP-0036), and
waits for the user to close the window. Every write is logged with its PC in
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
        agent.breakpoints("write", WATCH)
        agent.breakpoints("pc", PCS)
        print(time.strftime("%H:%M:%S"), "watching", WATCH, flush=True)
        proc.wait()
    print(time.strftime("%H:%M:%S"), "closed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
