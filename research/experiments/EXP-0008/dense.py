"""EXP-0008: sample SCSP slots densely while a state replays.

Run from the repository root:

    ./invenv.sh python research/experiments/EXP-0008/dense.py \
        {jp,us} STATE FRAMES OUT_DIR [IMAGE|- [ADDRESS=HEX ...]]

Launches the patched Mednafen (D-005) in the quiet home, loads STATE, and
while the game runs saves a state as often as the agent allows (every 2-4
frames in practice) until FRAMES frames have passed. Each state is parsed at
once for its active SCSP slots (``slots.active_slots``) and deleted.
Writes ``OUT_DIR/slots.jsonl`` (frame, slots) and ``OUT_DIR/scspram.bin``
(all 512 KiB of sound RAM at the start, to locate each character's data).
No input is sent. Outputs stay under the ignored OUT_DIR.
"""

from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
sys.path.insert(0, str(Path(__file__).parent))
from slots import active_slots

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


def main(
    release: str,
    state: Path,
    frames: int,
    out: Path,
    image: Path | None = None,
    writes: tuple[str, ...] = (),
) -> int:
    out.mkdir(parents=True, exist_ok=False)
    agent_dir = (out / "agent").resolve()
    env = {
        **os.environ,
        "MEDNAFEN_HOME": str(HOME.resolve()),
        "MEDNAFEN_AGENT_DIR": str(agent_dir),
    }
    for stale in (HOME / "sav").glob("*"):
        stale.unlink()
    tmp = (out / "tmp.mc0").resolve()
    with (out / "mednafen.log").open("wb") as log:
        process = subprocess.Popen(
            [str(BINARY), str(image or IMAGES[release])],
            env=env,
            stdout=log,
            stderr=subprocess.STDOUT,
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
            agent.loadstate(state)
            agent.pause()
            for w in writes:  # EXP-0033: ADDRESS=HEX into WRAM-H after the load
                address, data = w.split("=", 1)
                agent.write(
                    "workramh", int(address, 16) - 0x06000000, bytes.fromhex(data)
                )
            (out / "scspram.bin").write_bytes(agent.read("scspram", 0, 0x80000))
            first = int(agent.status()["frame"])
            agent.run()
            with (out / "slots.jsonl").open("w") as rows:
                while True:
                    replies = agent.command(f"savestate {tmp}", "status")
                    frame = int(replies[-1].split("frame=")[1].split()[0])
                    rows.write(
                        json.dumps(
                            {
                                "frame": frame - first,
                                "slots": active_slots(tmp.read_bytes()),
                            }
                        )
                        + "\n"
                    )
                    if frame - first >= frames:
                        break
            tmp.unlink()
        finally:
            process.send_signal(signal.SIGTERM)
            process.wait(timeout=30)
    return 0


if __name__ == "__main__":
    raise SystemExit(
        main(
            sys.argv[1],
            Path(sys.argv[2]),
            int(sys.argv[3]),
            Path(sys.argv[4]),
            Path(sys.argv[5]) if len(sys.argv) > 5 and sys.argv[5] != "-" else None,
            tuple(sys.argv[6:]),
        )
    )
