"""Drive Mednafen with injected pad presses, screenshots and memory reads.

Needs the agent build with patch 0002 (cache-coherent writes); without it, an
injected press is often not seen by the game (``EXP-0042``).

Steps, in order:

- ``N``: run N frames.
- ``shot:NAME``: screenshot ``NAME.png``.
- ``press:HEX``: one press. After the game next stores the P1 pad words
  (``--writer``), overwrite the raw and the pressed word with HEX. The game
  computes the release itself on the next frame. ``press:HEX@PC`` hooks PC
  instead, for this press. ``press2:HEX`` presses on pad 2 (words + 4).
- ``read:NAME:ADDR:LEN``: append ``NAME frame=F ADDR=hex`` to ``reads.txt``.
- ``dump:NAME:ADDR:HEXLEN``: write memory to ``NAME.bin``.
- ``write:ADDR:HEX``: write bytes now.
- ``readers:N``: log reads of the P1 pad words for N frames.

``--watch`` logs every write to the P1 pad words for the whole run.
Without a state, the image is cold-booted. ``--home`` reuses (or creates) a
Mednafen home, so a second run sees the backup memory the first one saved.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import time
from collections.abc import Sequence
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
from tools.mednafen.agent import Agent
from tools.mednafen.replay_state import BINARY, connect

PADS = {"us": 0x06076AB6, "jp": 0x06076B06}
WRITERS = {"us": 0x06013C74, "jp": 0x06013CD8}


def wait_running(agent: Agent) -> None:
    deadline = time.monotonic() + 3
    while agent.halted():
        if time.monotonic() >= deadline:
            raise RuntimeError("Mednafen stayed halted after run")
        time.sleep(0.05)


def run_steps(
    agent: Agent,
    steps: Sequence[str],
    out: Path,
    pad: int,
    writer: int | None,
) -> None:
    for step in steps:
        kind, _, rest = step.partition(":")
        if kind == "shot":
            agent.screenshot(out / f"{rest}.png")
        elif kind in ("press", "press2"):
            word, _, at = rest.partition("@")
            value = int(word, 16).to_bytes(2, "big")
            hook = int(at, 16) if at else writer
            words = pad + (4 if kind == "press2" else 0)
            if hook is None:
                raise RuntimeError("press needs a writer or @PC")
            if at:
                agent.breakpoints("pc", [f"{hook:08X}-{hook:08X}"])
            else:
                agent.breakpoints("write", [f"{words + 2:08X}-{words + 3:08X}"])
            agent.onhit_write(hook, words, value + value)
            agent.frames(1)
            agent.wait_halted()
            agent.command("bp write", "bp pc", "onhit clear")
        elif kind == "read":
            name, address, length = rest.split(":")
            data = agent.bus_read(int(address, 16), int(length))
            frame = agent.status()["frame"]
            with (out / "reads.txt").open("a") as reads:
                reads.write(f"{name} frame={frame} {address}={data.hex()}\n")
        elif kind == "dump":
            name, address, length = rest.split(":")
            data = agent.bus_read(int(address, 16), int(length, 16))
            (out / f"{name}.bin").write_bytes(data)
        elif kind == "write":
            address, _, hex_bytes = rest.partition(":")
            agent.bus_write(int(address, 16), bytes.fromhex(hex_bytes))
        elif kind == "readers":
            agent.breakpoints("read", [f"{pad:08X}-{pad + 7:08X}"])
            agent.frames(int(rest))
            agent.wait_halted()
            agent.command("bp read")
        else:
            agent.frames(int(step))
            agent.wait_halted(timeout=180)


def start(agent: Agent, state: Path | None) -> None:
    if state is None:
        agent.pause()
    else:
        agent.command("bp pc", "bp write", "onhit clear", "run")
        wait_running(agent)
        agent.command(f"loadstate {state.resolve()}", "pause")
    agent.wait_halted()
    agent.clear_events()
    agent.bpmode("log")


def launch(
    cue: Path, out: Path, home: Path | None, cart: str, wav: bool = False
) -> tuple[subprocess.Popen[bytes], Agent]:
    if home is None:
        home = out / "home"
    if not home.exists():
        home.mkdir(parents=True)
        source_home = Path("local/mednafen_quiet").resolve()
        shutil.copyfile(source_home / "mednafen.cfg", home / "mednafen.cfg")
        (home / "firmware").symlink_to(
            source_home / "firmware", target_is_directory=True
        )
    agent_dir = out / "agent"
    env = dict(os.environ, MEDNAFEN_HOME=str(home), MEDNAFEN_AGENT_DIR=str(agent_dir))
    command = [str(BINARY.resolve()), "-sound.volume", "0", "-ss.cart", cart]
    if wav:
        command += ["-soundrecord", str(out / "sound.wav")]
    log = (out / "mednafen.log").open("wb")
    process = subprocess.Popen(
        [*command, str(cue.resolve())], env=env, stdout=log, stderr=subprocess.STDOUT
    )
    return process, connect(agent_dir)


def stop(process: subprocess.Popen[bytes]) -> None:
    process.terminate()
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cue", type=Path)
    parser.add_argument("out", type=Path, help="new directory")
    parser.add_argument("steps", nargs="+")
    parser.add_argument("--state", type=Path, help="checkpoint (default: cold boot)")
    parser.add_argument("--region", choices=PADS, default="us")
    parser.add_argument("--writer", type=lambda text: int(text, 16))
    parser.add_argument("--home", type=Path)
    parser.add_argument("--cart", default="backup")
    parser.add_argument("--watch", action="store_true")
    parser.add_argument("--wav", action="store_true", help="record sound.wav")
    args = parser.parse_args()

    out = args.out.resolve()
    out.mkdir(parents=True)
    home = args.home.resolve() if args.home else None
    pad = PADS[args.region]
    writer = args.writer or WRITERS.get(args.region)
    process, agent = launch(args.cue, out, home, args.cart, args.wav)
    try:
        start(agent, args.state)
        if args.watch:
            agent.breakpoints("write", [f"{pad:08X}-{pad + 3:08X}"])
        run_steps(agent, args.steps, out, pad, writer)
        (out / "events.log").write_text("\n".join(agent.events()) + "\n")
    finally:
        stop(process)


if __name__ == "__main__":
    main()
