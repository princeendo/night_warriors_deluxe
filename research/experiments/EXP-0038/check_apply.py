"""EXP-0038: check what the title-time apply routine writes, edition by edition.

Note (EXP-0038): holding Start this way does not reach the title menu (the
replay drifts into the attract demo), so the check that worked writes the
code into RAM over a title-menu state instead (README, "Apply routine").

    ./invenv.sh python research/experiments/EXP-0038/check_apply.py CUE OUT_DIR

Boots CUE from the cold-session state ``f00000008`` with Start held (the raw
pad word ``0x06076AB6`` = ``0x0800`` each time ``0x0601CB8C`` runs) until the
title task has run, then for E = 0, 1, 2, 3 writes the settings block's
edition byte and reads back the flag, language, C, slot ``0x1BE`` and the
``MAIN.BIN`` patch sites after a few frames. Prints one line per edition.
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
from tools.mednafen.agent import Agent, AgentError

LAST = 0x0600979C  # title_code.py's "last applied" byte in this build
BINARY = Path("vendor/mednafen/build-agent/src/mednafen")
STATE = Path("local/aud004/cold-session/rec/states/f00000008.mcs")
READS = [
    ("flag", 0x0608089A, 1),
    ("lang", 0x06080882, 1),
    ("lang2", 0x060808A8, 1),
    ("C", 0x060830C6, 1),
    ("slot1BE", 0x06091E50, 4),
    ("st1call", 0x0603B902, 4),
    ("gate", 0x0603B908, 2),
    ("lits", 0x0603B9E4, 8),
    ("morr", 0x0605ADBC, 8),
    ("entry4", 0x0605B740, 4),
]


def run(agent: Agent, frames: int) -> None:
    agent.frames(frames)
    agent.wait_halted(120)


def main() -> int:
    cue, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True)
    env = dict(
        os.environ,
        MEDNAFEN_HOME=str(Path("local/mednafen_quiet").resolve()),
        MEDNAFEN_AGENT_DIR=str((out / "agent").resolve()),
    )
    with (out / "mednafen.log").open("wb") as log:
        proc = subprocess.Popen(
            [str(BINARY), str(cue)], env=env, stdout=log, stderr=log
        )
        try:
            agent = Agent((out / "agent").resolve(), 20)
            for _ in range(60):
                try:
                    agent.status()
                    break
                except AgentError:
                    time.sleep(0.5)
            agent.loadstate(STATE.resolve())
            agent.pause()
            agent.bpmode("log")
            agent.onhit_write(0x0601CB8C, 0x06076AB6, bytes.fromhex("0800"))
            agent.breakpoints("pc", ["0601CB8C-0601CB8C"])
            for _ in range(12):  # until the title task has run
                run(agent, 200)
                if agent.bus_read(0x06001000, 4) == bytes.fromhex("000004D4"):
                    break
            for _ in range(10):  # until the wrapper has applied once (last != 0xFF)
                run(agent, 60)
                if agent.bus_read(LAST, 1) != b"\xff":
                    break
            print(
                "slot 0x4D7 =",
                agent.bus_read(0x06092AB4, 4).hex(),
                "code =",
                agent.bus_read(0x06009568, 4).hex(),
                "mode =",
                agent.bus_read(0x06080864, 2).hex(),
            )
            for e in (None, 2, 1, 3, 0):
                if e is not None:
                    agent.bus_write(0x060830C5, bytes([e]))
                    run(agent, 10)
                vals = " ".join(
                    f"{n}={agent.bus_read(a, k).hex()}" for n, a, k in READS
                )
                print(
                    f"E={'boot' if e is None else e} "
                    f"frame={agent.status()['frame']} {vals}"
                )
            agent.screenshot((out / "end.png").resolve())
        finally:
            proc.terminate()
            proc.wait()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
