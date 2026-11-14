"""EXP-0015: which code addresses run, from power-on or from each of many states.

    ./invenv.sh python research/experiments/EXP-0015/pc_census.py {jp,us} OUT_DIR \
        --pc 06018032 [--pc ...] (--boot FRAMES | --states DIR [--frames 60])

One patched Mednafen (quiet home). Arms PC breakpoints in log mode on each
address, then either runs FRAMES frames from power-on, or for each ``*.mcs``
state in DIR (sorted) loads it and runs ``--frames`` frames with no input.
Writes ``census.tsv``: source (``boot`` or state name), PC, hit count, first
and last frame. Outputs stay under the ignored OUT_DIR.
"""

from __future__ import annotations

import argparse
import os
import re
import signal
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path

sys.path[:0] = [
    str(Path.cwd()),
    str(Path(__file__).resolve().parent.parent / "EXP-0010"),
]
from force import BINARY, HOME, IMAGES  # noqa: E402

from tools.mednafen.agent import Agent, AgentError  # noqa: E402

HIT = re.compile(r"frame=(\d+) .*? PC=([0-9A-F]{8}) ")


def tally(lines: list[str]) -> dict[str, list[int]]:
    out: dict[str, list[int]] = defaultdict(lambda: [0, 1 << 62, 0])
    for line in lines:
        m = HIT.search(line)
        if m:
            frame, pc = int(m[1]), m[2]
            row = out[pc]
            row[0] += 1
            row[1] = min(row[1], frame)
            row[2] = max(row[2], frame)
    return out


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("release", choices=sorted(IMAGES))
    p.add_argument("out", type=Path)
    p.add_argument("--pc", action="append", required=True)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--boot", type=int)
    g.add_argument("--states", type=Path)
    p.add_argument("--frames", type=int, default=60)
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
    rows = []
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
            agent.bpmode("log")
            agent.breakpoints("pc", [f"{x}-{x}" for x in a.pc])
            jobs = (
                [("boot", None)]
                if a.boot
                else [(s.stem, s) for s in sorted(a.states.glob("*.mcs"))]
            )
            for name, state in jobs:
                agent.clear_events()
                if state is not None:
                    agent.run()
                    agent.loadstate(state)
                    agent.pause()
                agent.frames(a.boot or a.frames)
                agent.wait_halted(900.0)
                for pc, (n, f0, f1) in sorted(tally(agent.events()).items()):
                    rows.append(f"{name}\t{pc}\t{n}\t{f0}\t{f1}")
        finally:
            proc.send_signal(signal.SIGTERM)
            proc.wait(timeout=30)
    (a.out / "census.tsv").write_text(
        "source\tpc\thits\tfirst\tlast\n" + "".join(r + "\n" for r in rows)
    )
    print(f"{len(rows)} rows")
    return 0


if __name__ == "__main__":
    assert tally(["hit n=1 frame=9 mode=log PC=06018032 RPC=0"])["06018032"] == [
        1,
        9,
        9,
    ]
    raise SystemExit(main())
