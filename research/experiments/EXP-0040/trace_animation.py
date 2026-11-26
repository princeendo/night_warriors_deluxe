"""Trace stock fighter selection with CUT and FULL from a title checkpoint."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from struct import unpack

sys.path.insert(0, str(Path.cwd()))
from tools.mednafen.agent import Agent
from tools.mednafen.replay_state import BINARY, connect

LAYOUTS = {
    "us": (
        0x06080A29,
        0x06076AD8,
        (0x0602191C, 0x06021922, 0x06021928, 0x0602194C, 0x06021892, 0x060218BA),
    ),
    "jp": (
        0x06080A79,
        0x06076B28,
        (0x06022188, 0x0602218E, 0x06022194, 0x060221B8, 0x060220FE, 0x06022126),
    ),
}


def trace(
    agent: Agent, state: Path, out: Path, region: str, setting: int, frames: int
) -> None:
    agent.command("bp pc", "onhit clear", "run")
    deadline = time.monotonic() + 3
    while agent.halted():
        if time.monotonic() >= deadline:
            raise RuntimeError("Mednafen stayed halted after run")
        time.sleep(0.05)
    agent.command(f"loadstate {state}", "pause")
    agent.wait_halted()
    agent.clear_events()
    agent.bpmode("log")
    setting_address, pool_address, pcs = LAYOUTS[region]
    agent.breakpoints("pc", [f"{pc:08X}-{pc:08X}" for pc in pcs])
    agent.bus_write(setting_address, bytes([setting]))
    agent.frames(frames)
    agent.wait_halted(timeout=45)
    agent.screenshot(out.with_suffix(".png"))
    events = agent.events()
    out.with_suffix(".log").write_text("\n".join(events) + "\n")
    flag_read = next((line for line in events if f" PC={pcs[1]:08X} " in line), "")
    if f"R1={setting:08X}" not in flag_read.split():
        raise RuntimeError(f"{out.name}: loader did not read animation value {setting}")
    pools = unpack(">6I", agent.bus_read(pool_address, 24))
    print(f"{out.name}: {len(events)} trace lines, pools {pools}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cue", type=Path)
    parser.add_argument("state", type=Path)
    parser.add_argument("out", type=Path)
    parser.add_argument("--region", choices=LAYOUTS, default="us")
    parser.add_argument("--frames", type=int, default=1120)
    args = parser.parse_args()

    out = args.out.resolve()
    out.mkdir(parents=True)
    home = out / "home"
    home.mkdir()
    source_home = Path("local/mednafen_quiet").resolve()
    shutil.copyfile(source_home / "mednafen.cfg", home / "mednafen.cfg")
    (home / "firmware").symlink_to(source_home / "firmware", target_is_directory=True)
    agent_dir = out / "agent"
    env = dict(os.environ, MEDNAFEN_HOME=str(home), MEDNAFEN_AGENT_DIR=str(agent_dir))
    command = [
        str(BINARY.resolve()),
        "-sound.volume",
        "0",
        "-ss.cart",
        "backup",
        str(args.cue.resolve()),
    ]
    with (out / "mednafen.log").open("wb") as log:
        process = subprocess.Popen(
            command, env=env, stdout=log, stderr=subprocess.STDOUT
        )
        try:
            agent = connect(agent_dir)
            for setting, name in enumerate(("cut", "full")):
                trace(
                    agent,
                    args.state.resolve(),
                    out / name,
                    args.region,
                    setting,
                    args.frames,
                )
        finally:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()


if __name__ == "__main__":
    main()
